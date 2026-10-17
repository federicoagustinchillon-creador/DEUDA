"""
fase24b_propiedades_series.py
=============================
Propiedades estocasticas de las series del SVARX (objetivo especifico 2 de la tesis; protocolo
propuesto en la metodologia de Paez, 2026):

  1. Raiz unitaria: ADF (H0: raiz unitaria) y KPSS (H0: estacionariedad), con constante. Una serie
     se clasifica I(0) solo si ADF rechaza y KPSS no rechaza al 5%; I(1) si ADF no rechaza y KPSS
     rechaza; en los demas casos el resultado es ambiguo.
  2. Zivot y Andrews (1992): raiz unitaria con un quiebre endogeno en el intercepto, para los casos
     en que un quiebre puede hacer que ADF no rechace por error (Perron, 1989).
  3. Bai y Perron (2003): quiebres multiples en la media de la deuda federal bruta, con el numero
     de quiebres elegido por BIC. Son los que entran como variables binarias en el SVARX.
  4. Johansen: prueba de la traza sobre las variables en niveles de la muestra de estimacion.

Las series son las de la muestra tal como entran al modelo (fase24.cargar_datos).

Uso: python codigo/modelos/fase24b_propiedades_series.py
Salida: resultados/tablas/fase24b_raiz_unitaria.csv, fase24b_bai_perron.csv, fase24b_johansen.csv
"""

from __future__ import annotations

import pathlib
import sys
import warnings

import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews
from statsmodels.tsa.vector_ar.vecm import coint_johansen

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase24_svarx_1996_2025 as f24  # noqa: E402
from bai_perron import bai_perron_breaks  # noqa: E402

TABLAS = f24.TABLAS
NIVEL = 0.05


def clasificar(p_adf: float, p_kpss: float) -> str:
    if p_adf < NIVEL and p_kpss >= NIVEL:
        return "I(0)"
    if p_adf >= NIVEL and p_kpss < NIVEL:
        return "I(1)"
    return "ambigua"


def main() -> None:
    Y, X, quiebres = f24.cargar_datos("federal", 2)
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
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for nombre, s in series.items():
            s = s.dropna()
            adf = adfuller(s, regression="c", autolag="AIC")
            kp = kpss(s, regression="c", nlags="auto")
            za = zivot_andrews(s, regression="c", autolag="AIC")
            filas.append({
                "serie": nombre, "n": len(s),
                "adf_estadistico": adf[0], "adf_p": adf[1],
                "kpss_estadistico": kp[0], "kpss_p": kp[1],
                "clasificacion": clasificar(adf[1], kp[1]),
                "za_estadistico": za[0], "za_p": za[1], "za_quiebre": s.index[za[4]].date(),
            })
    raiz = pd.DataFrame(filas)
    raiz.to_csv(TABLAS / "fase24b_raiz_unitaria.csv", index=False)

    # Misma serie y mismo periodo (1996-2025) que usa fase24.cargar_datos para fechar los quiebres.
    archivo, col = f24.SERIES_DEUDA["federal"]
    deuda = pd.read_csv(f24.DATOS / "procesados" / archivo, parse_dates=["Date"], index_col="Date")[col].dropna()
    bp = bai_perron_breaks(deuda)
    bp["bic_por_m"].assign(m_optimo=bp["m_optimo"]).to_csv(TABLAS / "fase24b_bai_perron.csv", index=False)

    p, _, _ = f24.elegir_rezagos(Y, X)
    Yr, Xr = f24.recortar(Y, X, p)
    # El crecimiento es una tasa de variacion, estacionaria por construccion: incluida en la prueba,
    # genera por si sola un "vector de cointegracion" trivial. La prueba relevante es sobre las
    # variables en niveles; la version con las cinco variables se guarda como referencia.
    todas = pd.concat([Yr, Xr["deuda_l1"]], axis=1).dropna()
    bloques = []
    for etiqueta, cols in (("niveles (sin crecimiento)", ["pb_pib", "EMBI", "TCRM", "deuda_l1"]),
                           ("las cinco variables", list(todas.columns))):
        jo = coint_johansen(todas[cols].values, det_order=0, k_ar_diff=p - 1)
        bloques.append(pd.DataFrame({
            "variables": etiqueta, "rango_nulo": [f"r <= {r}" for r in range(len(jo.lr1))],
            "traza": jo.lr1, "critico_95": jo.cvt[:, 1], "rechaza_95": jo.lr1 > jo.cvt[:, 1],
        }))
    johansen = pd.concat(bloques, ignore_index=True)
    johansen.to_csv(TABLAS / "fase24b_johansen.csv", index=False)
    niveles = todas

    pd.set_option("display.width", 200)
    print(raiz.round(3).to_string(index=False))
    print(f"Bai-Perron (deuda): m* = {bp['m_optimo']}, quiebres = {[str(f.date()) for f in bp['fechas_quiebre']]}")
    print(f"Johansen ({', '.join(niveles.columns)}), {len(niveles)} obs, {p - 1} rezagos en diferencias:")
    print(johansen.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
