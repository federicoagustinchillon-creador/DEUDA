"""
fase2_cointegracion.py
=====================
Fase 2 del Protocolo Econométrico: Análisis de Cointegración.

Realiza el Test de Johansen para verificar si existe una relación de equilibrio
de largo plazo entre las variables I(1) del sistema, como pre-requisito
para aplicar modelos como DOLS.

Incluye selección de rezagos (lags) mediante criterios de información (AIC, BIC).
"""

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.vector_ar.var_model import VAR
import warnings

warnings.filterwarnings("ignore")

def select_var_lags(df, maxlags=6):
    """Selecciona el número óptimo de rezagos para el VAR usando AIC/BIC."""
    model = VAR(df)
    res = model.select_order(maxlags)
    print("\n[Selección de Rezagos VAR]")
    print(res.summary())
    # Preferimos AIC para muestras medianas/pequeñas
    return res.aic

def johansen_test(df, det_order=-1, k_ar_diff=1):
    """
    Realiza el test de cointegración de Johansen.
    det_order: -1 (sin terminos deterministicos), 0 (constante), 1 (tendencia)
    k_ar_diff: número de rezagos en primeras diferencias
    """
    res = coint_johansen(df, det_order=det_order, k_ar_diff=k_ar_diff)
    
    # Extraer resultados (Traza y Máximo Autovalor)
    traces = res.lr1
    traces_crit = res.cvt  # Columnas: 90%, 95%, 99%
    maxeig = res.lr2
    maxeig_crit = res.cvm
    
    n_vars = df.shape[1]
    
    results = []
    for i in range(n_vars):
        # i es el número de relaciones de cointegración bajo H0
        results.append({
            "H0: r<=": i,
            "Traza Stat": round(traces[i], 2),
            "Traza Crit 95%": round(traces_crit[i, 1], 2),
            "Signif (Traza)": traces[i] > traces_crit[i, 1],
            "MaxEig Stat": round(maxeig[i], 2),
            "MaxEig Crit 95%": round(maxeig_crit[i, 1], 2),
            "Signif (MaxEig)": maxeig[i] > maxeig_crit[i, 1]
        })
        
    return pd.DataFrame(results)

def main():
    print("=" * 65)
    print(" FASE 2: TEST DE COINTEGRACIÓN (JOHANSEN)")
    print("=" * 65)
    
    file_path = "datos/dataset_consolidado_real.csv"
    if not os.path.exists(file_path):
        print(f"[!] Archivo no encontrado: {file_path}")
        return
        
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    
    # Variables de la Función de Reacción Fiscal de largo plazo
    # Típicamente: Deuda/PIB y PB/PIB. A veces se incluye el output gap o shocks externos
    coint_vars = ['deuda_pib', 'pb_pib', 'EMBI', 'TCRM']
    
    # Verificar si están en el dataset
    vars_to_test = [v for v in coint_vars if v in df.columns]
    df_coint = df[vars_to_test].dropna()
    
    print(f"\nAnalizando sistema: {vars_to_test}")
    print(f"Observaciones disponibles: {len(df_coint)}")
    
    # 1. Selección de rezagos óptimos
    opt_lags = select_var_lags(df_coint, maxlags=6)
    print(f"Rezago óptimo (AIC): {opt_lags}")
    
    # Si opt_lags es 0, usamos 1 para el test (k_ar_diff requiere lags >= 1)
    k_ar_diff = max(1, opt_lags - 1) 
    
    # 2. Test de Johansen
    # Usamos det_order=0 (constante en el vector de cointegración)
    johansen_results = johansen_test(df_coint, det_order=0, k_ar_diff=k_ar_diff)
    
    print("\nRESULTADOS TEST JOHANSEN (Traza y Max. Autovalor):")
    print(johansen_results.to_string(index=False))
    
    num_coint = sum(johansen_results['Signif (Traza)'])
    print(f"\nCONCLUSIÓN: Se hallaron {num_coint} vector(es) de cointegración (al 95%).")
    if num_coint > 0:
        print(" -> ES VÁLIDO aplicar DOLS/VECM para el análisis de largo plazo.")
    else:
        print(" -> ADVERTENCIA: No se encontró cointegración robusta. DOLS podría ser espurio.")
    
    # Guardar resultados
    os.makedirs("resultados/tablas", exist_ok=True)
    johansen_results.to_csv("resultados/tablas/fase2_cointegracion.csv", index=False)
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase2_cointegracion.csv'")

if __name__ == "__main__":
    main()
