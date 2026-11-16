"""Rezagos, diagnóstico de residuos y pronóstico fuera de muestra de las tres especificaciones.

Pronóstico: origen recursivo (ventana creciente) desde 2015T4; en cada origen se reestima el VARX
con los datos hasta ese trimestre y el orden p de la muestra completa, y se pronostican h = 1..8
trimestres condicionando en las exógenas observadas (variación de la tasa de la FED, VIX,
estacionales, binarias y deuda rezagada), igual en las tres especificaciones. Las binarias que
todavía no tienen variación en la ventana (Milei, el escalón de 2018) se excluyen y su efecto en el
pronóstico es cero. Los pronósticos de las variables diferenciadas se acumulan para compararlos en
nivel con el dato observado. Comparación: raíz del error cuadrático medio y prueba de Diebold y
Mariano (1995) con la corrección de Harvey, Leybourne y Newbold (1997) y varianza de Newey y West
con h-1 rezagos.
"""
from __future__ import annotations

import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
AQUI = pathlib.Path(__file__).parent
sys.path.insert(0, str(AQUI))
import specs  # noqa: E402

f24 = specs.f24
ORIGEN0 = pd.Timestamp("2015-12-31")
H = 8


def datos(spec: str):
    specs.activar(spec, specs.SALIDA / spec)
    Y, X, _ = f24.cargar_datos("federal", 2)
    return Y, X


def regla_hq(tabla: pd.DataFrame) -> int:
    """Regla propuesta en el plan: Schwarz entre estables; si autocorrelación, el menor orden mayor
    que la elimina; si ninguno, Hannan-Quinn entre estables."""
    est = tabla[tabla["estable"]]
    p_sic = int(est.loc[est["bic"].idxmin(), "p"])
    ok = est[(est["p"] >= p_sic) & (est["portmanteau_12_p"] >= 0.05)]["p"]
    return int(ok.min()) if not ok.empty else int(est.loc[est["hqic"].idxmin(), "p"])


def dm(e1: np.ndarray, e2: np.ndarray, h: int) -> tuple[float, float]:
    """Diebold-Mariano con corrección HLN; H0: igual error cuadrático. Estadístico > 0: e2 mejor."""
    d = e1 ** 2 - e2 ** 2
    n = len(d)
    dbar = d.mean()
    g = [np.mean((d[k:] - dbar) * (d[:n - k] - dbar)) for k in range(h)]
    var = (g[0] + 2 * sum((1 - k / h) * g[k] for k in range(1, h))) / n
    if var <= 0:
        var = g[0] / n
    stat = dbar / np.sqrt(var) * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    return float(stat), float(2 * stats.t.sf(abs(stat), n - 1))


def main() -> None:
    niveles_obs = datos("niveles")[0]  # niveles observados, misma muestra
    resumen, errores = [], {}
    corridas = [("niveles", "niveles", None), ("mixto", "mixto", None), ("diferencias", "diferencias", None),
                ("mixto_p1", "mixto", 1), ("diferencias_p4", "diferencias", 4)]
    for etiqueta, spec, p_forzado in corridas:
        Y, X = datos(spec)
        p_tesis, p_aic, tabla = f24.elegir_rezagos(Y, X)
        p_hq = regla_hq(tabla)
        p = p_forzado or p_tesis
        Yr, Xr = f24.recortar(Y, X, p)
        res = f24.VAR(Yr, exog=Xr).fit(maxlags=p, ic=None, trend="c")
        diag = f24.diagnosticos(res).set_index("prueba")["valor"]
        resumen.append({"spec": etiqueta, "p_usado": p, "p_regla_tesis": p_tesis, "p_regla_plan_hq": p_hq,
                        "p_sic": int(tabla["p_sic"].iloc[0]), "n": int(res.nobs),
                        "portmanteau12_p": diag["Portmanteau (12 rezagos)"],
                        "raiz_max": float(np.max(1 / np.abs(res.roots))),
                        "normalidad_p": diag["Normalidad multivariada (p-valor)"],
                        "rho_bohn": float(res.params.loc["deuda_l1", "pb_pib"]),
                        "rho_bohn_p": float(res.pvalues.loc["deuda_l1", "pb_pib"]),
                        **{f"portm_p_orden{q}": float(tabla.loc[tabla.p == q, "portmanteau_12_p"].iloc[0]) for q in (1, 2, 3, 4)}})
        tabla.to_csv(specs.SALIDA / f"rezagos_{etiqueta}.csv", index=False)

        # Pronóstico fuera de muestra
        fechas = Yr.index
        origenes = [o for o in fechas if o >= ORIGEN0 and fechas.get_loc(o) + 1 < len(fechas)]
        filas = []
        for o in origenes:
            i = fechas.get_loc(o)
            Ye, Xe = Yr.iloc[: i + 1], Xr.iloc[: i + 1]
            keep = [c for c in Xe.columns if not ((c.startswith("P_") or (c[:1] == "D" and c[1:2].isdigit()))
                                                  and Xe[c].iloc[p:].nunique() < 2)]
            r = f24.VAR(Ye, exog=Xe[keep]).fit(maxlags=p, ic=None, trend="c")
            hh = min(H, len(fechas) - 1 - i)
            Xf = Xr[keep].iloc[i + 1: i + 1 + hh].values
            fc = r.forecast(Ye.values[-p:], steps=hh, exog_future=Xf)
            fc = pd.DataFrame(fc, columns=Y.columns, index=fechas[i + 1: i + 1 + hh])
            for c in specs.DIF[spec]:
                fc[c] = niveles_obs.loc[o, c] + fc[c].cumsum()
            for h_, (fecha, fila) in enumerate(fc.iterrows(), start=1):
                for v in f24.ENDOG:
                    filas.append({"origen": o, "h": h_, "fecha": fecha, "var": v,
                                  "error": float(niveles_obs.loc[fecha, v] - fila[v])})
        errores[etiqueta] = pd.DataFrame(filas)
        errores[etiqueta].to_csv(specs.SALIDA / f"errores_{etiqueta}.csv", index=False)

    pd.set_option("display.width", 250)
    r = pd.DataFrame(resumen).set_index("spec")
    r.to_csv(specs.SALIDA / "resumen_estimacion.csv")
    print(r.round(4).T.to_string())

    out = []
    for excl in (False, True):
        for v in f24.ENDOG:
            for h_ in (1, 4, 8):
                fila = {"sin_2020": excl, "var": v, "h": h_}
                base = errores["niveles"]
                sel = lambda e: e[(e["var"] == v) & (e["h"] == h_) & (~e["fecha"].dt.year.eq(2020) if excl else True)].sort_values("origen")
                e0 = sel(base)["error"].values
                fila["n"] = len(e0)
                fila["rmse_niveles"] = np.sqrt(np.mean(e0 ** 2))
                for spec in ("mixto", "diferencias", "mixto_p1", "diferencias_p4"):
                    e1 = sel(errores[spec])["error"].values
                    fila[f"rmse_{spec}"] = np.sqrt(np.mean(e1 ** 2))
                    fila[f"dm_{spec}"], fila[f"dm_p_{spec}"] = dm(e0, e1, h_)
                out.append(fila)
    comp = pd.DataFrame(out)
    comp.to_csv(specs.SALIDA / "comparacion_pronostico.csv", index=False)
    print(comp.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
