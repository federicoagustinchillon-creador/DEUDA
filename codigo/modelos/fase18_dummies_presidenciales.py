"""
fase18_dummies_presidenciales.py
==================================
Robustez solicitada por el director: evaluar si la reacción fiscal (o el
nivel del resultado primario) difiere significativamente por administración
presidencial, como alternativa/complemento al umbral de Hansen basado en
riesgo soberano.

Períodos presidenciales dentro de la ventana 2004T1-2025T4 (n=88), aproximados
a inicio de trimestre según la fecha de asunción (25/05 y 10/12 caen en Q2/Q4):
  - Néstor Kirchner:      2004T1-2007T3  (referencia, se omite para evitar colinealidad perfecta)
  - CFK I:                2007T4-2011T3
  - CFK II:                2011T4-2015T3
  - Macri:                2015T4-2019T3
  - Alberto Fernández:    2019T4-2023T3
  - Milei:                2023T4-2025T4

Dos especificaciones:
  (A) Nivel: dummies como regresores aditivos (¿difiere el resultado primario
      medio por administración, controlando por deuda y ciclo?)
  (B) Interacción: dummy_i * d_t_1 (¿difiere la REACCIÓN fiscal -pendiente-
      por administración, no solo el nivel?), que es la pregunta
      econométricamente más cercana a la de Hansen pero con quiebres de
      régimen político en vez de régimen de riesgo soberano.

No se fuerza ningún resultado: se reporta el veredicto tal como sale.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import os
import pathlib

def newey_west_lags(n):
    return int(np.ceil(4 * (n / 100) ** (2 / 9)))

def construir_dummies_presidenciales(df):
    periodos = {
        "cfk1":   ("2007-10-01", "2011-09-30"),
        "cfk2":   ("2011-10-01", "2015-09-30"),
        "macri":  ("2015-10-01", "2019-09-30"),
        "af":     ("2019-10-01", "2023-09-30"),
        "milei":  ("2023-10-01", "2025-12-31"),
    }
    for nombre, (ini, fin) in periodos.items():
        df[f"pres_{nombre}"] = ((df.index >= ini) & (df.index <= fin)).astype(int)
    return df, [f"pres_{nombre}" for nombre in periodos.keys()]

def ejecutar_fase18(csv_path):
    print("=" * 78)
    print(" FASE 18: Robustez por Administración Presidencial ")
    print("=" * 78)

    df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
    df["d_t_1"] = df["deuda_pib"].shift(1)
    df = df.dropna(subset=["pb_pib", "d_t_1", "g_gap"])
    df, dummy_cols = construir_dummies_presidenciales(df)

    n = len(df)
    hac_lags = newey_west_lags(n)
    print(f"\nn={n} observaciones. HAC maxlags={hac_lags}.")
    print("Distribución de trimestres por administración (Néstor Kirchner = referencia):")
    print(f"  nestor_kirchner (ref.): {n - sum(df[c].sum() for c in dummy_cols)}")
    for c in dummy_cols:
        print(f"  {c}: {int(df[c].sum())}")

    # --- Especificación A: dummies de nivel ---
    print("\n--- (A) Dummies de NIVEL (resultado primario medio por administración) ---")
    Xa = sm.add_constant(df[["d_t_1", "g_gap"] + dummy_cols])
    model_a = sm.OLS(df["pb_pib"], Xa).fit(cov_type="HAC", cov_kwds={"maxlags": hac_lags})
    print(model_a.summary().tables[1])

    f_test_a = model_a.f_test([f"{c}=0" for c in dummy_cols])
    print(f"\nTest F conjunto (H0: todas las dummies de nivel = 0): "
          f"F={float(f_test_a.fvalue):.3f}, p={float(f_test_a.pvalue):.4f}")

    # --- Especificación B: interacción dummy * d_t_1 (reacción por administración) ---
    print("\n--- (B) Interacción dummy_i * d_t_1 (¿la REACCIÓN fiscal difiere por administración?) ---")
    df_b = df.copy()
    inter_cols = []
    for c in dummy_cols:
        col = f"{c}_x_dt1"
        df_b[col] = df_b[c] * df_b["d_t_1"]
        inter_cols.append(col)

    Xb = sm.add_constant(df_b[["d_t_1", "g_gap"] + inter_cols])
    model_b = sm.OLS(df_b["pb_pib"], Xb).fit(cov_type="HAC", cov_kwds={"maxlags": hac_lags})
    print(model_b.summary().tables[1])

    f_test_b = model_b.f_test([f"{c}=0" for c in inter_cols])
    print(f"\nTest F conjunto (H0: todas las interacciones administración*deuda = 0): "
          f"F={float(f_test_b.fvalue):.3f}, p={float(f_test_b.pvalue):.4f}")

    print("\n--- Coeficiente de reacción IMPLÍCITO por administración (d_t_1 + interacción) ---")
    beta_base = model_b.params["d_t_1"]
    print(f"  nestor_kirchner (ref.): rho = {beta_base:.4f}  (p={model_b.pvalues['d_t_1']:.4f})")
    for c, col in zip(dummy_cols, inter_cols):
        rho_admin = beta_base + model_b.params[col]
        p_inter = model_b.pvalues[col]
        print(f"  {c}: rho = {rho_admin:.4f}  (p de la interacción individual = {p_inter:.4f})")

    print("\n" + "=" * 78)
    print(" VEREDICTO ")
    print("=" * 78)
    sig_a = f_test_a.pvalue < 0.05
    sig_b = f_test_b.pvalue < 0.05
    print(f" (A) Nivel medio del resultado primario difiere por administración: "
          f"{'SI, p<0.05' if sig_a else 'NO se rechaza homogeneidad'} (p={float(f_test_a.pvalue):.4f})")
    print(f" (B) Reacción fiscal (pendiente) difiere por administración: "
          f"{'SI, p<0.05' if sig_b else 'NO se rechaza homogeneidad'} (p={float(f_test_b.pvalue):.4f})")

    os.makedirs("resultados/tablas", exist_ok=True)
    with open("resultados/tablas/fase18_dummies_nivel.csv", "w") as f:
        f.write(model_a.summary().as_csv())
    with open("resultados/tablas/fase18_dummies_interaccion.csv", "w") as f:
        f.write(model_b.summary().as_csv())
    print("\n[OK] Resultados guardados en resultados/tablas/fase18_dummies_*.csv")

if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.parent.parent
    csv_file = base_dir / "datos" / "dataset_consolidado_real.csv"
    ejecutar_fase18(csv_file)
