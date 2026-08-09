"""
fase12_diagnosticos_complementarios.py
======================================
Diagnosticos complementarios exigidos por la revision academica:

  (a) Seleccion del orden de rezagos del VAR subyacente al procedimiento de
      Johansen mediante criterios de informacion (AIC, BIC/SC y HQ), y
      sensibilidad del rango de cointegracion estimado al orden elegido.

  (b) Multicolinealidad de la ecuacion de reaccion fiscal: factores de
      inflacion de la varianza (VIF) y numero de condicion de la matriz de
      regresores.

Ambos bloques operan sobre el mismo panel trimestral que el resto del
protocolo, de modo que sus resultados son directamente comparables con los
del Capitulo de Resultados.
"""

import os
import pathlib
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen

warnings.filterwarnings("ignore")

# Sistema de cuatro variables sometido al contraste de Johansen.
SISTEMA = ["deuda_pib", "pb_pib", "EMBI", "TCRM"]

# Valores criticos de Johansen al 5% (columna 1 de la salida de statsmodels).
NIVEL_CRITICO = 1  # 0 -> 10%, 1 -> 5%, 2 -> 1%


def seleccionar_rezagos(df, maxlags=8):
    """Orden de rezagos del VAR en niveles segun AIC, BIC(SC), HQ y FPE."""
    modelo = VAR(df[SISTEMA])
    sel = modelo.select_order(maxlags=maxlags)

    print("\n[a] Seleccion del orden de rezagos del VAR (niveles)")
    print("    " + "-" * 62)
    print(sel.summary())

    elegidos = {k: int(v) for k, v in sel.selected_orders.items()}
    print(f"\n    Ordenes seleccionados: {elegidos}")
    return elegidos


def sensibilidad_johansen(df, ordenes):
    """Rango de cointegracion estimado para cada orden de rezagos plausible."""
    print("\n[b] Sensibilidad del rango de cointegracion al orden de rezagos")
    print("    (det_order=0: constante en la relacion de cointegracion)")
    print("    " + "-" * 62)

    filas = []
    for k in ordenes:
        # coint_johansen recibe k_ar_diff = rezagos del VAR en diferencias = p - 1
        k_diff = max(k - 1, 0)
        res = coint_johansen(df[SISTEMA].values, det_order=0, k_ar_diff=k_diff)

        rango_traza = int(np.sum(res.lr1 > res.cvt[:, NIVEL_CRITICO]))
        rango_maxeig = int(np.sum(res.lr2 > res.cvm[:, NIVEL_CRITICO]))

        filas.append({
            "p_var": k,
            "k_ar_diff": k_diff,
            "rango_traza_5pct": rango_traza,
            "rango_maxeig_5pct": rango_maxeig,
        })
        print(f"    p={k} (k_ar_diff={k_diff}) -> rango Traza={rango_traza}, "
              f"rango Max-Autovalor={rango_maxeig}")

    tabla = pd.DataFrame(filas)
    coincide = tabla["rango_traza_5pct"].nunique() == 1 and tabla["rango_maxeig_5pct"].nunique() == 1
    print(f"\n    Diagnostico: el rango estimado {'NO varia' if coincide else 'VARIA'} "
          f"con el orden de rezagos en el rango explorado.")
    return tabla


def diagnostico_multicolinealidad(df):
    """VIF y numero de condicion de la ecuacion de reaccion fiscal."""
    print("\n[c] Multicolinealidad de la ecuacion de reaccion fiscal")
    print("    " + "-" * 62)

    especificaciones = {
        "DOLS (nucleo de Bohn)": ["d_t_1", "g_gap"],
        "Ampliada (Bohn + EMBI + TCRM)": ["d_t_1", "g_gap", "EMBI", "TCRM"],
    }

    filas = []
    for nombre, cols in especificaciones.items():
        sub = df.dropna(subset=cols)
        X = sm.add_constant(sub[cols])
        Xv = X.values

        # Numero de condicion sobre regresores estandarizados (excluye constante).
        Z = sub[cols].values
        Z = (Z - Z.mean(axis=0)) / Z.std(axis=0, ddof=1)
        cond = float(np.linalg.cond(Z))

        print(f"\n    {nombre}  (n={len(sub)})")
        for i, c in enumerate(X.columns):
            if c == "const":
                continue
            vif = float(variance_inflation_factor(Xv, i))
            print(f"      VIF {c:<10} = {vif:7.3f}")
            filas.append({"especificacion": nombre, "regresor": c,
                          "VIF": vif, "num_condicion": cond})
        print(f"      Numero de condicion  = {cond:7.3f}")

    tabla = pd.DataFrame(filas)
    max_vif = tabla["VIF"].max()
    print(f"\n    VIF maximo del conjunto: {max_vif:.3f} "
          f"({'por debajo' if max_vif < 10 else 'por encima'} del umbral convencional de 10).")
    return tabla


def run(csv_path):
    print("=" * 78)
    print(" FASE 12: Diagnosticos complementarios (rezagos VAR, VIF, condicion) ")
    print("=" * 78)

    df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
    df["d_t_1"] = df["deuda_pib"].shift(1)

    sistema = df[SISTEMA].dropna()
    print(f"\nPanel del sistema de Johansen: n={len(sistema)} "
          f"({sistema.index.min():%Y-%m} a {sistema.index.max():%Y-%m})")

    elegidos = seleccionar_rezagos(sistema)

    ordenes = sorted({max(v, 1) for v in elegidos.values()} | {1, 2, 3, 4})
    tabla_joh = sensibilidad_johansen(sistema, ordenes)

    tabla_vif = diagnostico_multicolinealidad(df)

    os.makedirs("resultados/tablas", exist_ok=True)
    tabla_joh.to_csv("resultados/tablas/fase12_johansen_sensibilidad_rezagos.csv", index=False)
    tabla_vif.to_csv("resultados/tablas/fase12_vif.csv", index=False)
    pd.Series(elegidos).to_csv("resultados/tablas/fase12_orden_rezagos.csv",
                               header=["orden"])
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase12_*.csv'")
    return elegidos, tabla_joh, tabla_vif


if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.parent.parent
    run(base_dir / "datos" / "dataset_consolidado_real.csv")
