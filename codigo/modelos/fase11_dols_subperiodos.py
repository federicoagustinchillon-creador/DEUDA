"""
fase11_dols_subperiodos.py
==========================
Reestimacion de la Funcion de Reaccion Fiscal por subperiodos mediante DOLS.

Motivacion
----------
La Seccion de sensibilidad temporal del Capitulo de Resultados reportaba
originalmente solo una especificacion estatica MCO-HAC por subperiodo
(2004T1-2014T4 y 2015T1-2025T4), que arrojaba coeficientes rho positivos y
significativos, en contraste con el DOLS de muestra completa (rho<0, no
significativo). Descalificar el MCO estatico por sesgo de simultaneidad sin
mostrar la alternativa corregida deja abierta la objecion de que el descarte
es retorico antes que empirico.

Este modulo cierra esa brecha: reestima cada subperiodo con la augmentacion
dinamica de Stock-Watson, reduciendo el orden de adelantos/rezagos (m=1 y m=2
en lugar de m=4) para que el ejercicio sea factible con n~43 observaciones.
El resultado permite decidir si el signo positivo del MCO estatico sobrevive
a la correccion de endogeneidad de corto plazo.
"""

import os
import pathlib
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")

CORTE = "2015-01-01"
SUBPERIODOS = [
    ("2004T1-2014T4", None, CORTE),
    ("2015T1-2025T4", CORTE, None),
]


def newey_west_lags(n):
    """Lags de Newey-West segun m = 4*(T/100)^(2/9)."""
    return int(np.ceil(4 * (n / 100) ** (2 / 9)))


def estimar_estatico(sub):
    """MCO estatico pb_t = a + rho*d_{t-1} + gamma*y_gap + e_t, errores HAC."""
    sub = sub.dropna(subset=["pb_pib", "d_t_1", "g_gap"])
    y = sub["pb_pib"]
    X = sm.add_constant(sub[["d_t_1", "g_gap"]])
    res = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": newey_west_lags(len(sub))})
    return {
        "n": int(len(sub)),
        "rho": float(res.params["d_t_1"]),
        "se": float(res.bse["d_t_1"]),
        "p": float(res.pvalues["d_t_1"]),
    }


def estimar_dols(sub, m):
    """DOLS con m adelantos y m rezagos de Delta d, errores HAC."""
    sub = sub.copy()
    sub["diff_d"] = sub["d_t_1"].diff()
    feats = ["d_t_1", "g_gap", "diff_d"]
    for i in range(1, m + 1):
        sub[f"diff_d_lag_{i}"] = sub["diff_d"].shift(i)
        sub[f"diff_d_lead_{i}"] = sub["diff_d"].shift(-i)
        feats += [f"diff_d_lag_{i}", f"diff_d_lead_{i}"]

    sub = sub.dropna(subset=["pb_pib"] + feats)
    n = len(sub)
    k = len(feats) + 1  # + constante
    if n <= k + 2:
        return None  # grados de libertad insuficientes

    y = sub["pb_pib"]
    X = sm.add_constant(sub[feats])
    res = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": newey_west_lags(n)})
    return {
        "n": int(n),
        "gl": int(n - k),
        "rho": float(res.params["d_t_1"]),
        "se": float(res.bse["d_t_1"]),
        "p": float(res.pvalues["d_t_1"]),
    }


def run(csv_path):
    print("=" * 78)
    print(" FASE 11: DOLS por subperiodo (robustez de la sensibilidad temporal) ")
    print("=" * 78)

    df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
    df["d_t_1"] = df["deuda_pib"].shift(1)
    df = df.dropna(subset=["pb_pib", "d_t_1", "g_gap"])

    filas = []
    for etiqueta, ini, fin in SUBPERIODOS:
        sub = df.loc[ini:fin] if ini else df.loc[:fin]
        if fin is None:
            sub = df.loc[ini:]
        # .loc con fin abierto incluye el corte; se excluye explicitamente
        if fin is not None:
            sub = sub[sub.index < pd.Timestamp(fin)]

        print(f"\n--- {etiqueta} ---")
        est = estimar_estatico(sub)
        print(f"  MCO estatico   : n={est['n']:>3}  rho={est['rho']:+.4f}  "
              f"EE={est['se']:.4f}  p={est['p']:.4f}")
        filas.append({"subperiodo": etiqueta, "especificacion": "MCO estatico (HAC)", **est, "gl": np.nan})

        for m in (1, 2):
            d = estimar_dols(sub, m)
            if d is None:
                print(f"  DOLS (m={m})     : grados de libertad insuficientes")
                continue
            print(f"  DOLS (m={m})     : n={d['n']:>3}  gl={d['gl']:>3}  rho={d['rho']:+.4f}  "
                  f"EE={d['se']:.4f}  p={d['p']:.4f}")
            filas.append({"subperiodo": etiqueta, "especificacion": f"DOLS (m={m}, HAC)", **d})

    tabla = pd.DataFrame(filas)[
        ["subperiodo", "especificacion", "n", "gl", "rho", "se", "p"]
    ]

    print("\n" + "=" * 78)
    print(" SINTESIS ")
    print("=" * 78)
    print(tabla.to_string(index=False,
                          float_format=lambda x: f"{x:.4f}" if pd.notna(x) else "--"))

    signos_dols = tabla[tabla["especificacion"].str.startswith("DOLS")]
    if len(signos_dols):
        n_sig = int((signos_dols["p"] < 0.05).sum())
        print(f"\n -> Especificaciones DOLS por subperiodo estimadas: {len(signos_dols)}")
        print(f" -> De ellas, con rho significativo al 5%: {n_sig}")
        if n_sig == 0:
            print(" -> Veredicto: la significatividad del MCO estatico NO sobrevive a la")
            print("    augmentacion dinamica. El signo positivo por subperiodo es atribuible")
            print("    al sesgo de simultaneidad de corto plazo, no a una reaccion fiscal.")
        else:
            print(" -> Veredicto: al menos un subperiodo conserva reaccion significativa bajo")
            print("    DOLS; el hallazgo debe reportarse como tal en el Capitulo de Resultados.")

    os.makedirs("resultados/tablas", exist_ok=True)
    salida = "resultados/tablas/fase11_dols_subperiodos.csv"
    tabla.to_csv(salida, index=False)
    print(f"\n[OK] Resultados guardados en '{salida}'")
    return tabla


if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.parent.parent
    run(base_dir / "datos" / "dataset_consolidado_real.csv")
