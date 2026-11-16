"""Paso 1: raíz unitaria en niveles (reproducción del apéndice A.3) y en primeras diferencias.

Misma especificación que codigo/modelos/fase24b_propiedades_series.py: ADF con constante y rezagos
por AIC (máximo de Schwert, el valor por defecto de statsmodels), KPSS con constante y ancho de banda
automático (Hobijn et al., 2004). Estacionaria si ADF rechaza y KPSS no rechaza al 5%.

Uso: python codigo/modelos/robustez_diferencias/raiz_diferencias.py
"""
from __future__ import annotations

import pathlib
import sys
import warnings

import pandas as pd

repo = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(repo / "codigo" / "modelos"))
import fase24_svarx_1996_2025 as f24  # noqa: E402
from statsmodels.tsa.stattools import adfuller, kpss  # noqa: E402

NIVEL = 0.05


def clasificar(p_adf: float, p_kpss: float) -> str:
    if p_adf < NIVEL and p_kpss >= NIVEL:
        return "estacionaria"
    if p_adf >= NIVEL and p_kpss < NIVEL:
        return "raíz unitaria"
    return "ambigua"


def probar(s: pd.Series) -> tuple[int, float, float, str]:
    s = s.dropna()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p_adf = adfuller(s, regression="c", autolag="AIC")[1]
        p_kpss = kpss(s, regression="c", nlags="auto")[1]
    return len(s), p_adf, p_kpss, clasificar(p_adf, p_kpss)


Y, X, _ = f24.cargar_datos("federal", 2)
_, Xc, _ = f24.cargar_datos("consolidada", 2)
series = {
    "Resultado primario": Y["pb_pib"],
    "Crecimiento real": Y["crec"],
    "EMBI": Y["EMBI"],
    "TCRM": Y["TCRM"],
    "Deuda federal bruta": X["deuda_l1"].shift(-1).dropna(),
    "Deuda consolidada con el BCRA": Xc["deuda_l1"].shift(-1).dropna(),
    "Tasa de la FED (nivel)": X["dFED_l0"].cumsum(),
    "VIX": X["VIX"],
}
filas = []
for nombre, s in series.items():
    n0, a0, k0, c0 = probar(s)
    n1, a1, k1, c1 = probar(s.dropna().diff())
    filas.append({"serie": nombre, "n_niv": n0, "adf_niv": a0, "kpss_niv": k0, "clas_niv": c0,
                  "n_dif": n1, "adf_dif": a1, "kpss_dif": k1, "clas_dif": c1})
out = pd.DataFrame(filas)
pd.set_option("display.width", 250)
print(out.round(3).to_string(index=False))
out.to_csv(repo / "resultados" / "tablas" / "robustez_diferencias" / "raiz_unitaria_niveles_y_diferencias.csv", index=False)
