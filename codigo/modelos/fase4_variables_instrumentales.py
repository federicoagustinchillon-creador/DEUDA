"""
fase4_variables_instrumentales.py
=================================
Fase 4 del Protocolo Econométrico: Estimación por Variables Instrumentales (IV/2SLS).
Aborda la endogeneidad del riesgo país (EMBI+) en la Función de Reacción Fiscal.

Implementa:
  - 2SLS (Two-Stage Least Squares) usando `linearmodels.iv.IV2SLS` para obtener
    errores estándar consistentes (corrigiendo el HC-02 de la auditoría).
  - VIX (Índice de volatilidad global) y un spread soberano regional
    (EMBI_BRASIL, proxy de mercado construida en
    `codigo/ingesta_datos/ingesta_spread_regional.py` a partir del ETF EMB -iShares
    JPMorgan USD EM Bond, misma familia de índices que el EMBI+ argentino-)
    como instrumentos del EMBI+, en reemplazo del TCRM rezagado (Mejora
    Dimensión III): el TCRM impacta directamente sobre la recaudación y el
    resultado primario argentino y por eso fue rechazado por Sargan; un
    spread soberano regional captura el mismo riesgo sistémico de mercados
    emergentes sin ese canal presupuestario directo.
  - Diagnósticos de Primera Etapa (F-test para instrumentos débiles).
  - Test de Sobreidentificación de Sargan.
  - Test de Endogeneidad de Wu-Hausman.
"""

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import warnings

# Se requiere linearmodels para IV robusto
try:
    from linearmodels.iv import IV2SLS
except ImportError:
    print("[!] ERROR: 'linearmodels' no está instalado. Ejecute: pip install linearmodels")
    import sys
    sys.exit(1)

warnings.filterwarnings("ignore")

def ejecutar_fase4_econometria(csv_path):
    print("=" * 75)
    print(" FASE 4: Estimación IV (2SLS) para EMBI+ Endógeno ")
    print("=" * 75)
    
    if not os.path.exists(csv_path):
        print(f"[!] ERROR: No se encontró el dataset en {csv_path}")
        return
        
    df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
    
    print("\n[1/4] Preparando variables e instrumentos...")
    # Lags necesarios
    df['d_t_1'] = df['deuda_pib'].shift(1)

    # Verificar presencia del instrumento EMBI_BRASIL (spread regional ETF EMB)
    if 'EMBI_BRASIL' not in df.columns or df['EMBI_BRASIL'].dropna().empty:
        spread_path = os.path.join(os.path.dirname(os.path.abspath(csv_path)), "..", "procesados", "spread_regional_trimestral.csv")
        if not os.path.exists(spread_path):
            spread_path = "datos/procesados/spread_regional_trimestral.csv"
        if not os.path.exists(spread_path):
            try:
                import ingesta_spread_regional as spread
                spread.main()
            except Exception as e:
                print(f"[!] Aviso al generar spread regional: {e}")
        if os.path.exists(spread_path):
            spread_df = pd.read_csv(spread_path, index_col=0, parse_dates=True)
            spread_df.index = pd.to_datetime(spread_df.index).to_period("Q").to_timestamp("Q")
            df.index = pd.to_datetime(df.index).to_period("Q").to_timestamp("Q")
            if 'EMBI_BRASIL' in df.columns:
                df = df.drop(columns=['EMBI_BRASIL'])
            df = df.join(spread_df[['EMBI_BRASIL']], how='left')


    subset_cols = ['pb_pib', 'd_t_1', 'g_gap', 'EMBI', 'VIX', 'EMBI_BRASIL']
    df = df.dropna(subset=subset_cols)


    y = df['pb_pib']
    exog = sm.add_constant(df[['d_t_1', 'g_gap']])
    endog = df[['EMBI']]
    instr = df[['VIX', 'EMBI_BRASIL']]

    print(f" -> Observaciones válidas: {len(df)}")
    print(" -> Ecuación Estructural: pb_pib ~ 1 + d_t_1 + g_gap + [EMBI ~ VIX + EMBI_BRASIL]")
    
    print("\n[2/4] Estimando 2SLS (linearmodels.iv)...")
    # Utilizamos cov_type='robust' o 'kernel' (HAC) 
    iv_model = IV2SLS(dependent=y, exog=exog, endog=endog, instruments=instr)
    iv_res = iv_model.fit(cov_type='kernel', kernel='newey-west')
    
    print("\n--- RESULTADOS 2SLS ---")
    print(iv_res.summary.tables[1])
    
    print("\n[3/4] Diagnósticos de Primera Etapa (Instrumentos Débiles)...")
    # Test F de instrumentos excluidos
    first_stage = iv_res.first_stage
    f_stat = first_stage.diagnostics.loc['EMBI', 'f.stat']
    f_pval = first_stage.diagnostics.loc['EMBI', 'f.pval']
    
    print(f" -> Estadístico F (Instrumentos Excluidos): {f_stat:.4f} (p-value: {f_pval:.4f})")
    if f_stat > 10:
        print("    [OK] F > 10. Se supera el criterio de Staiger y Stock. Instrumentos relevantes.")
    else:
        print("    [!] F < 10. Riesgo de instrumentos débiles. Precaución con la inferencia.")
        
    print("\n[4/4] Pruebas de Endogeneidad y Sobreidentificación...")
    
    # Wu-Hausman (Endogeneidad)
    wu_hausman = iv_res.wu_hausman()
    print(f" -> Test de Endogeneidad Wu-Hausman: stat={wu_hausman.stat:.4f}, p-value={wu_hausman.pval:.4f}")
    if wu_hausman.pval < 0.10:
        print("    [!] Se rechaza exogeneidad (p < 0.10). El uso de IV/2SLS es apropiado.")
    else:
        print("    [OK] No se rechaza exogeneidad firme. EMBI podría ser exógeno empíricamente, aunque teóricamente no lo sea.")

    # Sargan (Sobreidentificación)
    sargan = iv_res.sargan
    print(f" -> Test de Sargan (Sobreidentificación): stat={sargan.stat:.4f}, p-value={sargan.pval:.4f}")
    if sargan.pval > 0.05:
        print("    [OK] No se rechaza H0. Los instrumentos son válidos (no correlacionados con error estructural).")
    else:
        print("    [!] Se rechaza H0. Posible correlación de los instrumentos con el error estructural.")
        
    print("\n=======================================================================================================")
    print(" Impacto del Riesgo Soberano (EMBI+) en la Reacción Fiscal ")
    print("=======================================================================================================")
    beta_embi = iv_res.params['EMBI']
    pval_embi = iv_res.pvalues['EMBI']
    
    print(f" -> Coeficiente beta_EMBI: {beta_embi:.6f} (p-value: {pval_embi:.4f})")
    if pval_embi < 0.05:
        if beta_embi > 0:
            print(" -> CONCLUSIÓN: Ante incrementos del riesgo país, hay un ajuste positivo del superávit primario.")
        else:
            print(" -> CONCLUSIÓN: El incremento del riesgo país deteriora significativamente el superávit primario.")
    else:
        print(" -> CONCLUSIÓN: No hay evidencia estadísticamente significativa de que el superávit responda de manera estructural a cambios en el EMBI+.")

    # Guardar resultados
    os.makedirs("resultados/tablas", exist_ok=True)
    with open("resultados/tablas/fase4_resultados_iv.csv", "w") as f:
        f.write(iv_res.summary.as_csv())

    with open("resultados/tablas/fase4_diagnosticos_iv.csv", "w") as f:
        f.write("statistic,value,pvalue\n")
        f.write(f"first_stage_F_excluded_instruments,{f_stat:.4f},{f_pval:.6f}\n")
        f.write(f"wu_hausman_endogeneity,{wu_hausman.stat:.4f},{wu_hausman.pval:.6f}\n")
        f.write(f"sargan_overidentification,{sargan.stat:.4f},{sargan.pval:.6f}\n")
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase4_resultados_iv.csv'")
    print("[OK] Diagnósticos guardados en 'resultados/tablas/fase4_diagnosticos_iv.csv'")

if __name__ == "__main__":
    import pathlib
    base_dir = pathlib.Path(__file__).parent.parent.parent
    csv_file = base_dir / "datos" / "dataset_consolidado_real.csv"
    ejecutar_fase4_econometria(csv_file)
