"""
fase23_reestimacion_1996_2025.py
==================================
Reestima el protocolo central (estacionariedad, rango de cointegracion,
VECM, SVAR restringido, TVECM) sobre la ventana de 30 anios 1996T1-2025T4
(n=120, dataset_consolidado_1996_2025.csv), en lugar de las ventanas
previas (88 obs 2004-2025 para SVAR/TVECM, 108 obs 1999-2025 para VECM).

No duplica la logica de estimacion: importa las funciones ya usadas y
verificadas en fase16 (VECM), fase19 (SVAR restringido), fase21 (TVECM) y
fase3b (seleccion de rango de cointegracion), y las corre sobre el dataset
nuevo. Solo difiere el dato de entrada.

Exporta a resultados/tablas/fase23_*.
"""

import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import select_order

warnings.filterwarnings("ignore")

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS_DIR = BASE_DIR / "datos"
TABLAS_DIR = BASE_DIR / "resultados" / "tablas"
TABLAS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fase16_vecm_dataset_ampliado import adf_test, kpss_test  # noqa: E402
from fase3b_reaccion_fiscal_vecm import seleccionar_rango_cointegracion, estimar_vecm  # noqa: E402
from fase19_var_restringido_macro import estimar_svar_restringido  # noqa: E402
from fase21_tvecm_hansen_seo import estimar_tvecm  # noqa: E402

COINT_VARS = ["deuda_pib", "pb_pib", "EMBI", "TCRM"]
EXOG_VARS = ["g_gap"]
SVAR_VARS = ["g_gap", "pb_pib", "EMBI", "TCRM", "deuda_pib"]


def cargar_datos():
    ruta = DATOS_DIR / "dataset_consolidado_1996_2025.csv"
    df = pd.read_csv(ruta, parse_dates=["Date"], index_col="Date")
    return df


def main():
    print("=" * 78)
    print(" FASE 23: REESTIMACION SOBRE LA VENTANA 1996-2025 (n=120, 30 anios) ")
    print("=" * 78)

    df = cargar_datos()
    print(f"\nObservaciones: {len(df)}  ({df.index.min().date()} a {df.index.max().date()})")

    # ------------------------------------------------------------------
    # 1. Estacionariedad (ADF / KPSS) de las variables del sistema
    # ------------------------------------------------------------------
    print("\n[1/4] Estacionariedad (ADF / KPSS) ...")
    filas_estac = []
    for col in COINT_VARS + EXOG_VARS:
        p_adf, adf_rechaza_raiz = adf_test(df[col])
        p_kpss, kpss_no_rechaza_estac = kpss_test(df[col])
        filas_estac.append({
            "variable": col, "adf_p": round(p_adf, 4), "adf_estacionaria": adf_rechaza_raiz,
            "kpss_p": round(p_kpss, 4), "kpss_estacionaria": kpss_no_rechaza_estac,
        })
        print(f"  {col:12s}  ADF p={p_adf:.4f} (estac={adf_rechaza_raiz})   "
              f"KPSS p={p_kpss:.4f} (estac={kpss_no_rechaza_estac})")
    pd.DataFrame(filas_estac).to_csv(TABLAS_DIR / "fase23_estacionariedad.csv", index=False)

    # ------------------------------------------------------------------
    # 2. Orden de rezagos y rango de cointegracion (Johansen, Traza)
    # ------------------------------------------------------------------
    print("\n[2/4] Orden de rezagos (criterios de informacion) y cointegracion de Johansen ...")
    sel = select_order(df[COINT_VARS], maxlags=8, deterministic="ci")
    print(f"  AIC={sel.aic}  BIC={sel.bic}  FPE={sel.fpe}  HQIC={sel.hqic}")

    r, res_johansen = seleccionar_rango_cointegracion(df[COINT_VARS], det_order=0, k_ar_diff=sel.bic)
    print(f"  Rango de cointegracion (Traza, 95%, k_ar_diff=BIC={sel.bic}): r={r}")
    print(f"  Traza: {np.round(res_johansen.lr1, 2)}")
    print(f"  Critico 95%: {np.round(res_johansen.cvt[:, 1], 2)}")

    pd.DataFrame([{
        "k_ar_diff_bic": sel.bic, "k_ar_diff_aic": sel.aic, "k_ar_diff_fpe": sel.fpe,
        "k_ar_diff_hqic": sel.hqic, "rango_cointegracion_bic": r,
    }]).to_csv(TABLAS_DIR / "fase23_johansen_resumen.csv", index=False)

    # ------------------------------------------------------------------
    # 3. VECM final (rango impuesto r=1 por motivo teorico, consistente
    #    con el resto del protocolo; k_ar_diff = BIC)
    # ------------------------------------------------------------------
    print("\n[3/4] VECM final (coint_rank=1, k_ar_diff=BIC) ...")
    k_ar_diff_final = max(1, int(sel.bic))
    vecm_res = estimar_vecm(df, COINT_VARS, EXOG_VARS, k_ar_diff=k_ar_diff_final, coint_rank=1)
    print(vecm_res.summary())

    beta = pd.DataFrame(vecm_res.beta, index=COINT_VARS, columns=["beta"])
    alpha = pd.DataFrame(vecm_res.alpha, index=COINT_VARS, columns=["alpha"])
    beta.to_csv(TABLAS_DIR / "fase23_vecm_beta.csv")
    alpha.to_csv(TABLAS_DIR / "fase23_vecm_alpha.csv")
    with open(TABLAS_DIR / "fase23_vecm_resumen.txt", "w", encoding="utf-8") as f:
        f.write(f"n_obs={len(df)}  k_ar_diff={k_ar_diff_final}  coint_rank=1\n\n")
        f.write(str(vecm_res.summary()))

    # ------------------------------------------------------------------
    # 4. SVAR restringido (5 variables) y TVECM (4 variables)
    # ------------------------------------------------------------------
    print("\n[4/4] SVAR restringido y TVECM ...")
    data_svar = df[SVAR_VARS].dropna()
    res_svar = estimar_svar_restringido(data_svar, nlags=2, n_boot=1000, horizon=20)

    df_S = pd.DataFrame(res_svar["S_matrix"], index=SVAR_VARS, columns=[f"Shock_{v}" for v in SVAR_VARS])
    df_S.to_csv(TABLAS_DIR / "fase23_svar_matriz_impacto_S.csv")
    print("\n  Matriz de impacto S:")
    print(df_S.round(4))

    filas_fevd = []
    for h in [1, 4, 8, 12, 20]:
        h_idx = h - 1
        for i, var_resp in enumerate(SVAR_VARS):
            fila = {"Horizonte_Trimestres": h, "Variable_Explicada": var_resp}
            for j, var_shock in enumerate(SVAR_VARS):
                fila[f"Shock_{var_shock}"] = round(res_svar["fevd"][h_idx, i, j], 2)
            filas_fevd.append(fila)
    df_fevd = pd.DataFrame(filas_fevd)
    df_fevd.to_csv(TABLAS_DIR / "fase23_fevd.csv", index=False)
    print("\n  FEVD deuda_pib, h=20:")
    print(df_fevd[(df_fevd.Horizonte_Trimestres == 20) & (df_fevd.Variable_Explicada == "deuda_pib")])

    data_tvecm = df[COINT_VARS].dropna()
    res_tvecm = estimar_tvecm(data_tvecm, trimming=0.15, n_boot=1000)
    filas_tvecm = {k: v for k, v in res_tvecm.items() if np.isscalar(v)}
    print("\n  TVECM (escalares):", filas_tvecm)
    pd.DataFrame([filas_tvecm]).to_csv(TABLAS_DIR / "fase23_tvecm_resumen.csv", index=False)
    for k, v in res_tvecm.items():
        if isinstance(v, np.ndarray):
            np.savetxt(TABLAS_DIR / f"fase23_tvecm_{k}.csv", np.atleast_1d(v), delimiter=",")

    print(f"\n[OK] Tablas exportadas a {TABLAS_DIR} (prefijo fase23_)")


if __name__ == "__main__":
    main()
