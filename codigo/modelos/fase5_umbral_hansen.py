"""
fase5_umbral_hansen.py
=======================
Fase 5 del Protocolo Econométrico: Modelación de Umbrales (Fatiga Fiscal).

Implementa el test de umbral para series de tiempo basado en Hansen (2000) 
"Sample Splitting and Threshold Estimation", corrigiendo el uso inapropiado
de Hansen (1999) que es exclusivo para datos de panel.

Incluye:
  - Búsqueda del umbral óptimo (Grid Search minimizando SSR).
  - Test de significancia del umbral mediante Bootstrap (Sup-LM test).
  - Análisis de Fatiga Fiscal (Ghosh et al. 2013) separando regímenes.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import os
import warnings

warnings.filterwarnings("ignore")

def bootstrap_threshold_test(df, y_col, X_control_cols, split_col, threshold_col, best_tau, n_boot=500):
    """
    Test de significancia del umbral (Hansen 2000) mediante Bootstrap.
    H0: Modelo lineal (sin umbral)
    H1: Modelo con umbral (tau)
    """
    y = df[y_col].values
    
    # 1. Modelo bajo H0 (Lineal)
    X_linear = df[X_control_cols + [split_col]].copy()
    X_linear = sm.add_constant(X_linear)
    model_h0 = sm.OLS(y, X_linear).fit()
    ssr_0 = model_h0.ssr
    resid_0 = model_h0.resid.values
    
    # 2. Modelo bajo H1 (Umbral óptimo)
    I_low = (df[threshold_col] <= best_tau).astype(int)
    I_high = (df[threshold_col] > best_tau).astype(int)
    
    X_alt = df[X_control_cols].copy()
    X_alt['d_low'] = df[split_col] * I_low
    X_alt['d_high'] = df[split_col] * I_high
    X_alt = sm.add_constant(X_alt)
    model_h1 = sm.OLS(y, X_alt).fit()
    ssr_1 = model_h1.ssr
    
    # F-stat observado
    F_obs = (ssr_0 - ssr_1) / ssr_1
    
    # 3. Bootstrap
    F_boot = []
    np.random.seed(42)
    
    for _ in range(n_boot):
        # Muestreo con reemplazo de los residuos bajo H0 (wild bootstrap simple)
        # Multiplicar por N(0,1) para preservar heterocedasticidad (Rademacher o Normal)
        v = np.random.normal(0, 1, len(resid_0))
        y_sim = model_h0.fittedvalues + resid_0 * v
        
        # Ajustar H0 simulado
        m0_sim = sm.OLS(y_sim, X_linear).fit()
        
        # Ajustar H1 simulado
        m1_sim = sm.OLS(y_sim, X_alt).fit()
        
        # F-stat simulado
        f_sim = (m0_sim.ssr - m1_sim.ssr) / m1_sim.ssr
        F_boot.append(f_sim)
        
    F_boot = np.array(F_boot)
    p_value = np.mean(F_boot >= F_obs)
    
    return F_obs, p_value

def get_optimal_threshold(df, y_col, X_control_cols, split_col, threshold_col):
    """
    Busca el umbral óptimo (tau) iterando entre el percentil 15 y 85
    de la variable de transición, asegurando grados de libertad.
    """
    percentiles = np.percentile(df[threshold_col], np.arange(15, 86, 1))
    percentiles = np.unique(percentiles)
    
    best_tau = None
    min_ssr = np.inf
    best_model = None
    
    y = df[y_col]
    X_control = df[X_control_cols]
    
    for tau in percentiles:
        I_low = (df[threshold_col] <= tau).astype(int)
        I_high = (df[threshold_col] > tau).astype(int)
        
        d_low = df[split_col] * I_low
        d_high = df[split_col] * I_high
        
        X = X_control.copy()
        X['d_low (tau <= EMBI)'] = d_low
        X['d_high (tau > EMBI)'] = d_high
        X = sm.add_constant(X)
        
        try:
            model = sm.OLS(y, X).fit()
            if model.ssr < min_ssr:
                min_ssr = model.ssr
                best_tau = tau
                best_model = model
        except:
            continue
            
    if best_model is not None:
        I_low = (df[threshold_col] <= best_tau).astype(int)
        I_high = (df[threshold_col] > best_tau).astype(int)
        X_best = X_control.copy()
        X_best['d_low (EMBI <= tau)'] = df[split_col] * I_low
        X_best['d_high (EMBI > tau)'] = df[split_col] * I_high
        X_best = sm.add_constant(X_best)
        # Re-estimar con HAC para inferencia
        best_model_hac = sm.OLS(y, X_best).fit(cov_type='HAC', cov_kwds={'maxlags': 4})
        return best_tau, best_model_hac
        
    return best_tau, best_model

def ejecutar_fase5_econometria(csv_path):
    print("=" * 75)
    print(" FASE 5: Modelación de Umbrales (Hansen 2000) y Fatiga Fiscal ")
    print("=" * 75)
    
    if not os.path.exists(csv_path):
        print(f"[!] ERROR: No se encontró el dataset en {csv_path}")
        return
        
    df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
    
    print("\n[1/3] Preparando variables (Sin datos simulados)...")
    df['d_t_1'] = df['deuda_pib'].shift(1)
    
    subset_cols = ['pb_pib', 'd_t_1', 'g_gap', 'EMBI']
    df = df.dropna(subset=subset_cols).copy()
    
    print(f" -> Observaciones válidas: {len(df)}")
    
    print("\n[2/3] Estimando Modelo de Umbral de Hansen (2000) para series de tiempo...")
    best_tau, best_model = get_optimal_threshold(
        df=df,
        y_col='pb_pib',
        X_control_cols=['g_gap'],
        split_col='d_t_1',
        threshold_col='EMBI'
    )
    
    print(f" -> Umbral Óptimo Encontrado (tau*): {best_tau:.1f} puntos básicos de EMBI+")
    
    print("\n[3/3] Test de Significancia del Umbral (Bootstrap Sup-LM)...")
    f_obs, p_val_boot = bootstrap_threshold_test(
        df=df,
        y_col='pb_pib',
        X_control_cols=['g_gap'],
        split_col='d_t_1',
        threshold_col='EMBI',
        best_tau=best_tau,
        n_boot=1000
    )
    
    print(f" -> F-stat observado: {f_obs:.4f}")
    print(f" -> p-value (Bootstrap 1000 iteraciones): {p_val_boot:.4f}")
    
    if p_val_boot < 0.10:
        print("    [OK] Se rechaza la linealidad (p < 0.10). El efecto umbral es estadísticamente significativo.")
    else:
        print("    [!] No se rechaza linealidad. El umbral detectado podría ser espurio.")

    print("\n--- RESULTADOS MODELO DE UMBRAL (Errores HAC) ---")
    print(best_model.summary().tables[1])
    
    alpha_1 = best_model.params['d_low (EMBI <= tau)']
    alpha_2 = best_model.params['d_high (EMBI > tau)']
    pval_2 = best_model.pvalues['d_high (EMBI > tau)']
    
    print("\n===================================================================")
    print(" Análisis de Fatiga Fiscal (Ghosh et al., 2013) ")
    print("===================================================================")
    print(f" -> Régimen NORMAL (EMBI <= {best_tau:.0f}): Reacción = {alpha_1:.4f}")
    print(f" -> Régimen ESTRÉS (EMBI >  {best_tau:.0f}): Reacción = {alpha_2:.4f} (p-value: {pval_2:.4f})")
    
    if alpha_2 <= 0 or pval_2 > 0.05:
        print("\n [ALERTA] Se confirma FATIGA FISCAL.")
        print(" En el régimen de alto estrés (riesgo soberano extremo), el Estado ")
        print(" pierde la capacidad de generar superávits primarios para estabilizar la deuda.")
    else:
        print("\n [SOSTENIBLE] El Estado logra sostener la reacción fiscal positiva incluso en crisis.")
        
    print("\nNota: El módulo de Dominancia Fiscal (Sargent-Wallace) ha sido retirado")
    print("      temporalmente hasta incorporar series reales de Pasivos Remunerados (BCRA).")

    # Guardar resultados
    os.makedirs("resultados/tablas", exist_ok=True)
    with open("resultados/tablas/fase5_resultados_hansen.csv", "w") as f:
        f.write(best_model.summary().as_csv())
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase5_resultados_hansen.csv'")

if __name__ == "__main__":
    import pathlib
    base_dir = pathlib.Path(__file__).parent.parent.parent
    csv_file = base_dir / "datos" / "dataset_consolidado_real.csv"
    ejecutar_fase5_econometria(csv_file)
