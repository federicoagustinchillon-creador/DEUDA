"""
fase1_estacionariedad.py
========================
Fase 1 del Protocolo Econométrico: Análisis de Integración (Series Temporales).
Ejecuta pruebas de raíz unitaria y estacionariedad sobre el dataset empírico real.

Pruebas implementadas:
  1. ADF (Augmented Dickey-Fuller) - H0: Raíz unitaria
  2. PP (Phillips-Perron)          - H0: Raíz unitaria (requiere 'arch', opcional)
  3. KPSS (Kwiatkowski-Phillips-Schmidt-Shin) - H0: Estacionariedad
  4. DF-GLS (Elliott-Rothenberg-Stock, 1996)  - H0: Raíz unitaria (requiere 'arch')
  5. Test de Quiebre Estructural (CUSUM) para evaluar estabilidad paramétrica.

Criterio de integración: Una serie es I(1) si es no estacionaria en niveles
y estacionaria en su primera diferencia.
"""

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
import warnings

# Suprimir warnings de KPSS (ej: p-value bounds)
warnings.filterwarnings("ignore")

def adf_test(series, signif=0.05):
    """Test Augmented Dickey-Fuller."""
    res = adfuller(series.dropna(), autolag='AIC')
    p_val = res[1]
    is_stat = p_val < signif
    return p_val, is_stat

def kpss_test(series, signif=0.05):
    """Test KPSS."""
    res = kpss(series.dropna(), regression='c', nlags="auto")
    p_val = res[1]
    is_stat = p_val >= signif # H0 es estacionariedad
    return p_val, is_stat

def phillips_perron_test(series, signif=0.05):
    """Test Phillips-Perron (intenta usar arch.unitroot si está disponible)."""
    try:
        from arch.unitroot import PhillipsPerron
        pp = PhillipsPerron(series.dropna())
        p_val = pp.pvalue
        is_stat = p_val < signif
        return p_val, is_stat
    except ImportError:
        return np.nan, np.nan

def dfgls_test(series, trend='c'):
    """Test DF-GLS (Elliott, Rothenberg y Stock, 1996), vía arch.unitroot.DFGLS.
    trend='ct' (tendencia + constante) para niveles, trend='c' (solo constante)
    para primeras diferencias, siguiendo la especificación reportada en la
    Tabla 6.1 de la tesis."""
    try:
        from arch.unitroot import DFGLS
        res = DFGLS(series.dropna(), trend=trend)
        return res.stat, res.critical_values['5%']
    except ImportError:
        return np.nan, np.nan


def zivot_andrews_test(series, lags=4, trend='ct', trim=0.15):
    """Test de Zivot-Andrews (1992) con quiebre estructural endógeno, Modelo C
    (quiebre simultáneo en intercepto y pendiente), vía arch.unitroot.ZivotAndrews.
    Reporta el estadístico t óptimo, la fecha de quiebre (el candidato que
    minimiza el estadístico t, según el propio algoritmo) y los valores
    críticos asintóticos del Modelo C, tal como se reportan en la
    Sección 5.6.1 de la tesis."""
    import numpy as np
    from arch.unitroot import ZivotAndrews
    clean = series.dropna()
    res = ZivotAndrews(clean, lags=lags, trend=trend, trim=trim)
    _ = res.stat  # fuerza el cómputo interno antes de leer _all_stats
    break_idx = np.nanargmin(res._all_stats)
    break_date = clean.index[break_idx]
    return res.stat, break_date, res.critical_values


def analyze_dfgls(df, columns):
    """Aplica DF-GLS en nivel (tendencia+constante) y primera diferencia
    (solo constante) a cada columna, replicando la Tabla 6.1 del Capítulo 6."""
    results = []
    for col in columns:
        series = df[col]
        stat_niv, crit_niv = dfgls_test(series, trend='ct')
        diff_series = series.diff().dropna()
        stat_diff, crit_diff = dfgls_test(diff_series, trend='c')

        rechaza_niv = stat_niv < crit_niv
        rechaza_diff = stat_diff < crit_diff
        if rechaza_niv:
            orden = "I(0)"
        elif rechaza_diff:
            orden = "I(1)"
        else:
            orden = "Ambiguo"

        results.append({
            "Variable": col,
            "DFGLS_stat (Nivel)": round(stat_niv, 2),
            "DFGLS_crit5% (Nivel)": round(crit_niv, 2),
            "DFGLS_stat (Diff)": round(stat_diff, 2),
            "DFGLS_crit5% (Diff)": round(crit_diff, 2),
            "Conclusion": orden,
        })
    return pd.DataFrame(results)


def analyze_stationarity(df, columns):
    """Realiza análisis completo I(0) vs I(1) para las columnas dadas."""
    results = []
    
    for col in columns:
        series = df[col]
        # Niveles
        adf_p_niv, adf_stat_niv = adf_test(series)
        kpss_p_niv, kpss_stat_niv = kpss_test(series)
        pp_p_niv, pp_stat_niv = phillips_perron_test(series)
        
        # Primeras diferencias
        diff_series = series.diff().dropna()
        adf_p_diff, adf_stat_diff = adf_test(diff_series)
        kpss_p_diff, kpss_stat_diff = kpss_test(diff_series)
        pp_p_diff, pp_stat_diff = phillips_perron_test(diff_series)
        
        # Determinación heurística simple del orden de integración
        if adf_stat_niv and kpss_stat_niv:
            orden = "I(0)"
        elif adf_stat_diff and kpss_stat_diff:
            orden = "I(1)"
        else:
            orden = "Ambiguo / I(1)"

        results.append({
            "Variable": col,
            "ADF_p (Nivel)": round(adf_p_niv, 4),
            "KPSS_p (Nivel)": round(kpss_p_niv, 4),
            "PP_p (Nivel)": round(pp_p_niv, 4) if not np.isnan(pp_p_niv) else "N/A",
            "ADF_p (Diff)": round(adf_p_diff, 4),
            "KPSS_p (Diff)": round(kpss_p_diff, 4),
            "Orden Inferido": orden
        })
        
    return pd.DataFrame(results)

def structural_break_cusum(df, col_y='pb_pib', col_x='deuda_pib'):
    """Test CUSUM de residuos OLS para detectar inestabilidad estructural."""
    try:
        from statsmodels.stats.diagnostic import breaks_cusumolsresid
        Y = df[col_y].dropna()
        X = sm.add_constant(df[col_x].loc[Y.index])
        model = sm.OLS(Y, X).fit()
        test_stat, p_val, crit = breaks_cusumolsresid(model.resid)
        print(f"\n[CUSUM Test] {col_y} ~ {col_x}: p-value = {p_val:.4f}")
        if p_val < 0.05:
            print("  -> Existe evidencia de quiebre estructural (rechazo de H0 param. estables).")
        else:
            print("  -> No hay evidencia suficiente de quiebre estructural en la regresión simple.")
    except Exception as e:
        print(f"\n[!] Error en CUSUM test: {e}")

def main():
    print("=" * 65)
    print(" FASE 1: TEST DE RAÍZ UNITARIA Y ESTACIONARIEDAD (DATOS REALES)")
    print("=" * 65)
    
    file_path = "datos/dataset_consolidado_real.csv"
    if not os.path.exists(file_path):
        print(f"[!] Archivo no encontrado: {file_path}")
        return
        
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    
    # Variables clave para el análisis
    target_vars = ['deuda_pib', 'pb_pib', 'g_gap', 'EMBI', 'TCRM', 'CER']
    
    # Verificar si están en el dataset
    vars_to_test = [v for v in target_vars if v in df.columns]
    
    print(f"\nRealizando pruebas para: {vars_to_test}")
    results_df = analyze_stationarity(df, vars_to_test)
    
    print("\nRESULTADOS (p-values):")
    print(results_df.to_string(index=False))
    
    # Test CUSUM de quiebre estructural en relación bivariada (ej. Bohn simple)
    if 'pb_pib' in df.columns and 'deuda_pib' in df.columns:
        structural_break_cusum(df)

    # DF-GLS (Elliott, Rothenberg y Stock, 1996), Tabla 6.1 del Capítulo 6:
    # pb_t, d_t, risk_t (EMBI+) y la brecha del producto.
    dfgls_vars = ['pb_pib', 'deuda_pib', 'EMBI', 'g_gap']
    dfgls_vars = [v for v in dfgls_vars if v in df.columns]
    dfgls_df = analyze_dfgls(df, dfgls_vars)
    print("\nRESULTADOS DF-GLS (Elliott-Rothenberg-Stock, 1996):")
    print(dfgls_df.to_string(index=False))

    # Zivot-Andrews (1992) con quiebre endógeno, Modelo C, sobre la ratio
    # Deuda/PIB, Sección 5.6.1.
    za_stat, za_break, za_crit = zivot_andrews_test(df['deuda_pib'], lags=4, trend='ct', trim=0.15)
    print("\nRESULTADO ZIVOT-ANDREWS (Modelo C, quiebre endógeno, deuda_pib):")
    print(f"  Estadistico t: {za_stat:.2f}  |  Quiebre optimo: {za_break.date()}")
    print(f"  Criticos: 1%={za_crit['1%']:.2f}  5%={za_crit['5%']:.2f}  10%={za_crit['10%']:.2f}")
    za_df = pd.DataFrame([{
        "Variable": "deuda_pib",
        "Modelo": "C (intercepto + pendiente)",
        "Estadistico_t": round(za_stat, 2),
        "Quiebre_optimo": za_break.date().isoformat(),
        "Critico_1%": round(za_crit['1%'], 2),
        "Critico_5%": round(za_crit['5%'], 2),
        "Critico_10%": round(za_crit['10%'], 2),
    }])

    # Guardar resultados
    os.makedirs("resultados/tablas", exist_ok=True)
    results_df.to_csv("resultados/tablas/fase1_estacionariedad.csv", index=False)
    dfgls_df.to_csv("resultados/tablas/fase1_dfgls.csv", index=False)
    za_df.to_csv("resultados/tablas/fase1_zivot_andrews.csv", index=False)
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase1_estacionariedad.csv', 'fase1_dfgls.csv' y 'fase1_zivot_andrews.csv'")

if __name__ == "__main__":
    main()
