"""
fase3_reaccion_fiscal.py
=========================
Fase 3 del Protocolo Econométrico: Estimación de la Función de Reacción Fiscal (FRF).
Estima la reacción del superávit primario frente a la acumulación de deuda.

Implementa:
  - MCO con errores consistentes HAC (selección automática de lags).
  - Test de Hausman Aumentado para endogeneidad (usando instrumentos válidos).
  - DOLS (Dynamic OLS) en caso de endogeneidad o por la super-consistencia con I(1) cointegradas.
  - Criterios de información para seleccionar m rezagos y adelantos en DOLS.
  - Pruebas de especificación post-estimación (RESET, Breusch-Godfrey, Jarque-Bera).
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.stats.diagnostic as smd
import statsmodels.stats.api as sms
import os
import warnings
from scipy import stats

warnings.filterwarnings("ignore")

def newey_west_lags(n):
    """Calcula lags óptimos de Newey-West según m = 4*(T/100)^(2/9)."""
    return int(np.ceil(4 * (n / 100)**(2/9)))

def select_dols_lags(df, y_col, x_cols, d_col, max_m=4):
    """
    Selecciona el número de rezagos y adelantos (m) para DOLS 
    minimizando el Criterio de Información de Akaike (AIC).
    """
    best_aic = np.inf
    best_m = 1
    
    for m in range(1, max_m + 1):
        df_temp = df.copy()
        dols_features = list(x_cols)
        
        # Agregar diferencias contemporáneas, rezagos y adelantos
        df_temp['diff_d'] = df_temp[d_col].diff()
        dols_features.append('diff_d')
        
        for i in range(1, m + 1):
            df_temp[f'diff_d_lag_{i}'] = df_temp['diff_d'].shift(i)
            df_temp[f'diff_d_lead_{i}'] = df_temp['diff_d'].shift(-i)
            dols_features.extend([f'diff_d_lag_{i}', f'diff_d_lead_{i}'])
            
        df_temp = df_temp.dropna(subset=[y_col] + dols_features)
        
        Y = df_temp[y_col]
        X = sm.add_constant(df_temp[dols_features])
        
        try:
            model = sm.OLS(Y, X).fit()
            if model.aic < best_aic:
                best_aic = model.aic
                best_m = m
        except:
            pass
            
    return best_m

def ejecutar_fase3_econometria(csv_path):
    print("=" * 75)
    print(" FASE 3: Función de Reacción Fiscal Base (MCO-HAC y DOLS) ")
    print("=" * 75)
    
    if not os.path.exists(csv_path):
        print(f"[!] ERROR: No se encontró el dataset en {csv_path}")
        return
        
    df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
    
    # 1. Variables rezagadas y diferencias
    df['d_t_1'] = df['deuda_pib'].shift(1)
    
    # Instrumentos externos (EMBI y TCRM) rezagados para evitar instrumentación circular
    df['embi_t_1'] = df['EMBI'].shift(1)
    df['tcrm_t_1'] = df['TCRM'].shift(1)
    
    # Filtrar NA de las variables base
    base_cols = ['pb_pib', 'd_t_1', 'g_gap', 'embi_t_1', 'tcrm_t_1']
    df = df.dropna(subset=base_cols)
    n_obs = len(df)
    hac_lags = newey_west_lags(n_obs)
    
    print(f"\n[1/4] Estimando MCO con Errores Robustos (HAC maxlags={hac_lags})...")
    # pb_pib = beta_0 + beta_1 * d_t_1 + beta_2 * g_gap + u_t
    y = df['pb_pib']
    X_base = df[['d_t_1', 'g_gap']]
    X = sm.add_constant(X_base)
    
    model_mco = sm.OLS(y, X)
    results_mco = model_mco.fit(cov_type='HAC', cov_kwds={'maxlags': hac_lags})
    
    print(results_mco.summary().tables[1])
    
    print("\n[2/4] Pruebas de Diagnóstico Post-Estimación...")
    # Breusch-Godfrey (Autocorrelación)
    bg_test = smd.acorr_breusch_godfrey(results_mco, nlags=4)
    print(f" -> Breusch-Godfrey (LM p-value): {bg_test[1]:.4f}")
    
    # Breusch-Pagan (Heterocedasticidad)
    bp_test = sms.het_breuschpagan(results_mco.resid, X)
    print(f" -> Breusch-Pagan (p-value): {bp_test[1]:.4f}")
    
    # Jarque-Bera (Normalidad de residuos)
    jb_test = sm.stats.stattools.jarque_bera(results_mco.resid)
    print(f" -> Jarque-Bera (p-value): {jb_test[1]:.4f}")
    
    # RESET de Ramsey (Especificación)
    reset_test = sm.stats.diagnostic.linear_reset(results_mco, power=2, test_type="fitted", use_f=True)
    print(f" -> RESET Ramsey (p-value): {reset_test.pvalue:.4f}")
    
    print("\n[3/4] Evaluando Endogeneidad (Test de Hausman Aumentado)...")
    # Usamos EMBI_t-1 y TCRM_t-1 como instrumentos (variables externas) en lugar de rezagos propios d_t_2
    Z = df[['embi_t_1', 'tcrm_t_1', 'g_gap']]
    Z = sm.add_constant(Z)
    fs_model = sm.OLS(df['d_t_1'], Z).fit()
    df['v_hat'] = fs_model.resid
    
    X_aug = X.copy()
    X_aug['v_hat'] = df['v_hat']
    hausman_model = sm.OLS(y, X_aug).fit()
    hausman_pvalue = hausman_model.pvalues['v_hat']
    print(f" -> Hausman Test p-value (v_hat): {hausman_pvalue:.4f}")
    
    endogeneity = hausman_pvalue < 0.10
    if endogeneity:
        print("    [!] Endogeneidad detectada (p < 0.10). Es obligatorio usar DOLS / IV.")
    else:
        print("    [OK] No se rechaza exogeneidad, pero DOLS es preferible por la relación de cointegración (super-consistencia).")
        
    print("\n[4/4] Estimación DOLS (Dynamic OLS)...")
    # Selección de lags/leads óptimos
    m_opt = select_dols_lags(df, 'pb_pib', ['d_t_1', 'g_gap'], 'd_t_1', max_m=4)
    print(f" -> Rezagos/adelantos óptimos seleccionados por AIC: m = {m_opt}")
    
    df_dols = df.copy()
    df_dols['diff_d'] = df_dols['d_t_1'].diff()
    dols_features = ['d_t_1', 'g_gap', 'diff_d']
    
    for i in range(1, m_opt + 1):
        df_dols[f'diff_d_lag_{i}'] = df_dols['diff_d'].shift(i)
        df_dols[f'diff_d_lead_{i}'] = df_dols['diff_d'].shift(-i)
        dols_features.extend([f'diff_d_lag_{i}', f'diff_d_lead_{i}'])
        
    df_dols = df_dols.dropna(subset=['pb_pib'] + dols_features)
    y_dols = df_dols['pb_pib']
    X_dols = sm.add_constant(df_dols[dols_features])
    
    dols_model = sm.OLS(y_dols, X_dols).fit(cov_type='HAC', cov_kwds={'maxlags': hac_lags})
    
    print("\n--- RESULTADOS DOLS (Largo Plazo) ---")
    print(dols_model.summary().tables[1])
    
    beta_1 = dols_model.params['d_t_1']
    p_val = dols_model.pvalues['d_t_1']
    
    print("\n===============================================================================")
    print(" Veredicto de Sostenibilidad Intertemporal (H0: beta_1 <= 0) ")
    print("===============================================================================")
    if beta_1 > 0 and p_val < 0.05:
        print(f" [RECHAZO H0] Se verifica reacción marginal positiva y significativa.")
        print(f" -> Coeficiente estimado beta_1 = {beta_1:.4f} (p-value = {p_val:.4f})")
        print(" -> Condición de sostenibilidad débil de Bohn (1998) satisfecha para el período completo.")
    else:
        print(f" [NO SE RECHAZA H0] No hay evidencia robusta de reacción marginal positiva.")
        print(f" -> Coeficiente estimado beta_1 = {beta_1:.4f} (p-value = {p_val:.4f})")
        print(" -> La política fiscal promedio del período no garantiza la solvencia intertemporal (riesgo de Ponzi).")
        print(" -> Requiere análisis de fatiga fiscal (Fase 5).")
        
    # Guardar resultados
    os.makedirs("resultados/tablas", exist_ok=True)
    with open("resultados/tablas/fase3_resultados_dols.csv", "w") as f:
        f.write(dols_model.summary().as_csv())
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase3_resultados_dols.csv'")

if __name__ == "__main__":
    import pathlib
    base_dir = pathlib.Path(__file__).parent.parent.parent
    csv_file = base_dir / "datos" / "dataset_consolidado_real.csv"
    ejecutar_fase3_econometria(csv_file)
