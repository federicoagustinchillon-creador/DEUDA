"""
fase16_vecm_dataset_ampliado.py
================================
Re-ejecuta el protocolo de estacionariedad, selección de rezagos, cointegración
de Johansen y estimación VECM (Fases 1, 2 y 3b) sobre el dataset ampliado de
108 observaciones (1999T1-2025T4, dataset_consolidado_real_ext.csv), pedido
por el director para reemplazar la ventana de 88 observaciones (2004T1-2025T4)
por una muestra mayor, aun a costa de incorporar el tramo empalmado 1996-2003
con quiebres estructurales extremos (hiperinflación relativa de fin de
convertibilidad, default de 2001-2002).

No reemplaza fase1_estacionariedad.py, fase2_cointegracion.py ni
fase3b_reaccion_fiscal_vecm.py, que documentan el mismo protocolo sobre el
dataset de 88 observaciones. Este script aísla el efecto de ampliar la
ventana muestral, tres bloques:

  1. Estacionariedad (ADF/KPSS) de las cuatro variables del sistema de
     cointegración (deuda_pib, pb_pib, EMBI, TCRM) sobre la ventana ampliada.
  2. Selección de rezagos del VAR en niveles (AIC, BIC, FPE, HQIC) y
     sensibilidad de la estimación VECM (beta de largo plazo, alpha de
     ajuste) a esa elección, dado que los cuatro criterios no coinciden en
     esta muestra.
  3. Sensibilidad del rango de cointegración de Johansen al punto de inicio
     de la ventana muestral, para aislar si la ambigüedad del rango proviene
     específicamente del tramo 1999-2001 (pre-crisis de convertibilidad).
"""

import pandas as pd
import numpy as np
import os
import pathlib
import sys
import warnings
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.vector_ar.vecm import VECM, select_order, coint_johansen

warnings.filterwarnings("ignore")

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fase3b_reaccion_fiscal_vecm import seleccionar_rango_cointegracion, estimar_vecm

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS = BASE_DIR / "datos"
RESULTADOS = BASE_DIR / "resultados" / "tablas"

COINT_VARS = ["deuda_pib", "pb_pib", "EMBI", "TCRM"]
EXOG_VARS = ["g_gap"]


def adf_test(series, signif=0.05):
    res = adfuller(series.dropna(), autolag="AIC")
    p_val = res[1]
    return p_val, p_val < signif


def kpss_test(series, signif=0.05):
    res = kpss(series.dropna(), regression="c", nlags="auto")
    p_val = res[1]
    return p_val, p_val >= signif


def analizar_estacionariedad(df, columns):
    filas = []
    for col in columns:
        serie = df[col]
        adf_p_niv, adf_stat_niv = adf_test(serie)
        kpss_p_niv, kpss_stat_niv = kpss_test(serie)
        diff = serie.diff().dropna()
        adf_p_diff, adf_stat_diff = adf_test(diff)
        kpss_p_diff, kpss_stat_diff = kpss_test(diff)

        if adf_stat_niv and kpss_stat_niv:
            orden = "I(0)"
        elif adf_stat_diff and kpss_stat_diff:
            orden = "I(1)"
        else:
            orden = "Ambiguo / I(1)"

        filas.append({
            "Variable": col,
            "ADF_p (Nivel)": round(adf_p_niv, 4),
            "KPSS_p (Nivel)": round(kpss_p_niv, 4),
            "ADF_p (Diff)": round(adf_p_diff, 4),
            "KPSS_p (Diff)": round(kpss_p_diff, 4),
            "Orden Inferido": orden,
        })
    return pd.DataFrame(filas)


def tabla_orden_rezagos(df, maxlags=8):
    sel = select_order(df[COINT_VARS], maxlags=maxlags, deterministic="ci")
    resumen = sel.summary()
    criterios = {"AIC": sel.aic, "BIC": sel.bic, "FPE": sel.fpe, "HQIC": sel.hqic}
    return pd.DataFrame([criterios]), resumen


def tabla_sensibilidad_lags(df, k_ar_diffs):
    filas = []
    for k in k_ar_diffs:
        resultado = estimar_vecm(df, COINT_VARS, EXOG_VARS, k, coint_rank=1)
        b = resultado.beta[:, 0]
        idx_pb = COINT_VARS.index("pb_pib")
        idx_deuda = COINT_VARS.index("deuda_pib")
        beta_deuda_norm = -b[idx_deuda] / b[idx_pb]
        alpha_pb = resultado.alpha[idx_pb, 0]
        se_alpha_pb = resultado.stderr_alpha[idx_pb, 0]
        z_alpha_pb = alpha_pb / se_alpha_pb
        from scipy.stats import norm
        p_alpha_pb = 2 * (1 - norm.cdf(abs(z_alpha_pb)))
        filas.append({
            "k_ar_diff": k,
            "lag_VAR": k + 1,
            "beta_deuda_normalizado": round(beta_deuda_norm, 4),
            "alpha_pb": round(alpha_pb, 4),
            "p_valor_alpha_pb": round(p_alpha_pb, 4),
        })
    return pd.DataFrame(filas)


def tabla_sensibilidad_inicio_muestra(df_completo, k_ar_diff, fechas_inicio):
    filas = []
    for fecha in fechas_inicio:
        sub = df_completo.loc[fecha:, COINT_VARS].dropna()
        if len(sub) < 20:
            continue
        r, res = seleccionar_rango_cointegracion(sub, det_order=0, k_ar_diff=k_ar_diff)
        traza_r0 = res.lr1[0]
        crit_r0 = res.cvt[0, 1]
        filas.append({
            "Inicio_muestra": fecha,
            "n_obs": len(sub),
            "Traza (H0: r=0)": round(traza_r0, 2),
            "Critico_95%": round(crit_r0, 2),
            "Rango_hallado": r,
        })
    return pd.DataFrame(filas)


def main():
    print("=" * 78)
    print(" FASE 16: ESTACIONARIEDAD, REZAGOS Y COINTEGRACIÓN SOBRE DATASET AMPLIADO")
    print(" (108 obs, 1999T1-2025T4)")
    print("=" * 78)

    csv_path = DATOS / "dataset_consolidado_real_ext.csv"
    df_completo = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
    cols = COINT_VARS + EXOG_VARS
    df = df_completo[cols].dropna()
    print(f"\nObservaciones disponibles: {len(df)} ({df.index.min().date()} a {df.index.max().date()})")

    # 0. Estadísticos descriptivos de la ventana ampliada (Cap. 5)
    desc = df_completo[cols].agg(["mean", "std", "min", "max"]).T
    desc["skew"] = df_completo[cols].skew()
    desc = desc.round(2)
    print("\n--- 0. Estadísticos descriptivos (ventana ampliada, n=108) ---")
    print(desc.to_string())

    # 1. Estacionariedad
    print("\n--- 1. Estacionariedad (ADF/KPSS) sobre ventana ampliada ---")
    tabla_est = analizar_estacionariedad(df, COINT_VARS + EXOG_VARS)
    print(tabla_est.to_string(index=False))

    # 2. Selección de rezagos del VAR en niveles
    print("\n--- 2. Selección de rezagos VAR en niveles (AIC/BIC/FPE/HQIC) ---")
    tabla_rezagos, resumen_rezagos = tabla_orden_rezagos(df)
    print(resumen_rezagos)
    print(tabla_rezagos.to_string(index=False))

    # 3. Sensibilidad VECM a la elección de rezagos
    print("\n--- 3. Sensibilidad de beta/alpha a k_ar_diff (rango de cointegración = 1) ---")
    # k_ar_diff = lag_VAR - 1. Incluye los valores que surgen de los cuatro
    # criterios de información (AIC/BIC/FPE/HQIC, Bloque 2) más la grilla
    # 1..5 para cubrir el rango completo de especificaciones razonables
    # dado n=108.
    k_desde_criterios = [max(1, int(v) - 1) for v in tabla_rezagos.iloc[0].values]
    k_candidatos = sorted(set(k_desde_criterios + [1, 2, 3, 4, 5]))
    tabla_sens = tabla_sensibilidad_lags(df, k_candidatos)
    print(tabla_sens.to_string(index=False))

    # 4. Sensibilidad del rango de Johansen al inicio de la ventana muestral
    print("\n--- 4. Sensibilidad del rango de Johansen al inicio de la muestra ---")
    print("    (k_ar_diff fijo = 1, correspondiente al criterio BIC)")
    fechas_candidatas = ["1999-01-01", "2000-01-01", "2001-01-01", "2002-01-01",
                          "2003-01-01", "2004-01-01"]
    tabla_inicio = tabla_sensibilidad_inicio_muestra(df_completo, k_ar_diff=1,
                                                       fechas_inicio=fechas_candidatas)
    print(tabla_inicio.to_string(index=False))

    # 5. Especificación final: k_ar_diff=1 (BIC, más parsimoniosa dado n=108)
    print("\n--- 5. Estimación VECM final (k_ar_diff=1, rango de cointegración=1) ---")
    resultado_final = estimar_vecm(df, COINT_VARS, EXOG_VARS, k_ar_diff=1, coint_rank=1)
    beta_index = COINT_VARS if resultado_final.beta.shape[0] == len(COINT_VARS) else COINT_VARS + ["const"]
    beta_final = pd.DataFrame(resultado_final.beta, index=beta_index, columns=["beta"])
    alpha_final = pd.DataFrame(resultado_final.alpha, index=COINT_VARS, columns=["alpha"])
    print(beta_final.to_string())
    print(alpha_final.to_string())

    # Guardar todo
    os.makedirs(RESULTADOS, exist_ok=True)
    desc.to_csv(RESULTADOS / "fase16_descriptivos_ampliado.csv")
    tabla_est.to_csv(RESULTADOS / "fase16_estacionariedad_ampliado.csv", index=False)
    tabla_rezagos.to_csv(RESULTADOS / "fase16_orden_rezagos_ampliado.csv", index=False)
    tabla_sens.to_csv(RESULTADOS / "fase16_sensibilidad_rezagos_vecm.csv", index=False)
    tabla_inicio.to_csv(RESULTADOS / "fase16_sensibilidad_inicio_muestra.csv", index=False)
    beta_final.to_csv(RESULTADOS / "fase16_vecm_final_beta.csv")
    alpha_final.to_csv(RESULTADOS / "fase16_vecm_final_alpha.csv")
    with open(RESULTADOS / "fase16_vecm_final_resumen.txt", "w", encoding="utf-8") as f:
        f.write(resultado_final.summary().as_text())
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase16_*'")


if __name__ == "__main__":
    main()
