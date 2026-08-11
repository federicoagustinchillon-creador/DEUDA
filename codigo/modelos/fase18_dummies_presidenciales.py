"""
fase18_dummies_presidenciales.py
==================================
Robustez solicitada por el director: evaluar si la VELOCIDAD DE AJUSTE del
VECM (alpha_pb, no un regresor en niveles I(1) crudo) difiere por
administración presidencial, como alternativa/complemento al umbral de
Hansen basado en riesgo soberano.

Corrección metodológica respecto de la primera versión de este script: la
primera versión interactuaba dummies con d_t_1 (I(1)) en un MCO simple, lo
que arriesgaba confundir "efecto de administración" con la propia tendencia
no estacionaria de la deuda (el problema de regresión espuria que el resto
de la tesis evita explícitamente con DOLS/VECM). Esta versión, en cambio,
interactúa las dummies con el TÉRMINO DE CORRECCIÓN DE ERROR del VECM
(ect_{t-1} = beta' x_{t-1}), que es estacionario por construcción (es la
combinación lineal cointegrante). Así se testea si la velocidad de ajuste
alpha_pb del VECM ya estimado en la tesis (Sección 6, Tabla vecm_beta_alpha)
varía por administración, sin reintroducir el problema de no estacionariedad.

Ventana: 2004T1-2025T4 (n=87 tras rezagar), la ventana ORIGINAL con datos
reales en su totalidad (no se usa la ventana ampliada 1999-2025 porque el
tramo 1996-2003 es empalmado/interpolado, y las administraciones de ese
tramo -Menem, De la Rúa, Duhalde- suman apenas 20 trimestres repartidos en
3-4 gobiernos muy breves, insuficiente para un dummy confiable).

No se fuerza ningún resultado: se reporta el veredicto tal como sale.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.vector_ar.vecm import VECM
import os
import pathlib

COINT_VARS = ["deuda_pib", "pb_pib", "EMBI", "TCRM"]
EXOG_VARS = ["g_gap"]

def newey_west_lags(n):
    return int(np.ceil(4 * (n / 100) ** (2 / 9)))

def construir_dummies_presidenciales(df):
    periodos = {
        "cfk1":  ("2007-10-01", "2011-09-30"),
        "cfk2":  ("2011-10-01", "2015-09-30"),
        "macri": ("2015-10-01", "2019-09-30"),
        "af":    ("2019-10-01", "2023-09-30"),
        "milei": ("2023-10-01", "2025-12-31"),
    }
    for nombre, (ini, fin) in periodos.items():
        df[f"pres_{nombre}"] = ((df.index >= ini) & (df.index <= fin)).astype(int)
    return df, [f"pres_{nombre}" for nombre in periodos.keys()]

def ejecutar_fase18(csv_path):
    print("=" * 78)
    print(" FASE 18 (v2): Robustez por Administración vía Término de Corrección de Error del VECM ")
    print("=" * 78)

    df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
    df = df.dropna(subset=COINT_VARS + EXOG_VARS)

    # --- 1. Reestimar el VECM de referencia sobre la ventana original (k_ar_diff=1, rango=1) ---
    vecm = VECM(df[COINT_VARS], exog=df[EXOG_VARS], k_ar_diff=1, coint_rank=1, deterministic="ci")
    fit = vecm.fit()
    beta = fit.beta[:, 0]
    const_coint = float(fit.det_coef_coint[0, 0])
    print("\nVector de cointegración beta (normalizado sobre deuda_pib) y constante restringida:")
    for var, b in zip(COINT_VARS, beta):
        print(f"  {var}: {b:.4f}")
    print(f"  const: {const_coint:.4f}")

    # ect_{t-1} = beta' x_{t-1} + const (constante restringida al espacio de cointegración,
    # "ci" en la terminología de Johansen/statsmodels)
    ect = df[COINT_VARS].dot(beta) + const_coint
    df["ect_lag1"] = ect.shift(1)
    df["d_pb"] = df["pb_pib"].diff()

    df, dummy_cols = construir_dummies_presidenciales(df)
    df = df.dropna(subset=["d_pb", "ect_lag1", "g_gap"])
    n = len(df)
    hac_lags = newey_west_lags(n)
    print(f"\nn={n} observaciones (2004T1 en adelante, tras rezagar). HAC maxlags={hac_lags}.")
    print("Distribución de trimestres por administración (Néstor Kirchner = referencia):")
    print(f"  nestor_kirchner (ref.): {n - sum(int(df[c].sum()) for c in dummy_cols)}")
    for c in dummy_cols:
        print(f"  {c}: {int(df[c].sum())}")

    # --- 2. Interacción dummy_i * ect_{t-1}: ¿la velocidad de ajuste alpha_pb difiere por administración? ---
    print("\n--- Interacción dummy_i * ect_{t-1} (¿alpha_pb difiere por administración?) ---")
    inter_cols = []
    for c in dummy_cols:
        col = f"{c}_x_ect"
        df[col] = df[c] * df["ect_lag1"]
        inter_cols.append(col)

    X = sm.add_constant(df[["ect_lag1", "g_gap"] + inter_cols])
    model = sm.OLS(df["d_pb"], X).fit(cov_type="HAC", cov_kwds={"maxlags": hac_lags})
    print(model.summary().tables[1])

    f_test = model.f_test([f"{c}=0" for c in inter_cols])
    print(f"\nTest F conjunto (H0: todas las interacciones administración*ect = 0): "
          f"F={float(f_test.fvalue):.3f}, p={float(f_test.pvalue):.4f}")

    print("\n--- alpha_pb IMPLÍCITO por administración (ect_lag1 + interacción) ---")
    alpha_base = model.params["ect_lag1"]
    print(f"  nestor_kirchner (ref.): alpha_pb = {alpha_base:.4f}  (p={model.pvalues['ect_lag1']:.4f})")
    for c, col in zip(dummy_cols, inter_cols):
        alpha_admin = alpha_base + model.params[col]
        p_inter = model.pvalues[col]
        print(f"  {c}: alpha_pb = {alpha_admin:.4f}  (p de la interacción individual = {p_inter:.4f})")

    print("\n" + "=" * 78)
    print(" VEREDICTO ")
    print("=" * 78)
    sig = f_test.pvalue < 0.05
    print(f" La velocidad de ajuste del VECM (alpha_pb) difiere por administración: "
          f"{'SI, p<0.05' if sig else 'NO se rechaza homogeneidad'} (p={float(f_test.pvalue):.4f})")

    os.makedirs("resultados/tablas", exist_ok=True)
    with open("resultados/tablas/fase18_dummies_vecm_ect.csv", "w") as f:
        f.write(model.summary().as_csv())
    print("\n[OK] Resultados guardados en resultados/tablas/fase18_dummies_vecm_ect.csv")

if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.parent.parent
    csv_file = base_dir / "datos" / "dataset_consolidado_real.csv"
    ejecutar_fase18(csv_file)
