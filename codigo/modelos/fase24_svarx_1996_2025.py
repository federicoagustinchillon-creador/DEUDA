"""
fase24_svarx_1996_2025.py
=========================
SVARX trimestral 1996T1-2025T4 sobre la deuda consolidada, con la tasa de
politica de la FED y el VIX como variables exogenas.

Reemplaza a fase19 (SVAR restringido) y corrige dos diferencias entre aquel
codigo y lo que dice el capitulo de Metodologia:
  1. fase19 ordenaba EMBI+ antes que TCRM (recursivo). Aqui EMBI+ y TCRM forman
     un bloque sin orden interno: se reporta la contribucion CONJUNTA del bloque
     a la varianza de la deuda, que es invariante a cualquier rotacion dentro
     del bloque (ver `contribucion_bloque`).
  2. fase19 trataba u_pb - alpha*u_y como shock ortogonal sin estimar la
     respuesta del producto al shock fiscal. Aqui se aplica Blanchard y Perotti
     (2002): el shock fiscal es el residuo ciclicamente ajustado
     e_pb = u_pb - alpha_y * u_y (alpha_y = 0,25, elasticidad citada en fase19:
     Girouard y Andre, 2005), y el producto responde a el en el trimestre:
     u_y = c * e_pb + e_y.

Modelo en forma reducida (Y_t endogeno, X_t exogeno):
    Y_t = nu + sum_{i=1..p} A_i Y_{t-i} + Gamma X_t + u_t,
    Y_t = (pb_t, g_gap_t, EMBI_t, TCRM_t, d_t),
    X_t = (dFED_t, dFED_{t-1}, ..., dFED_{t-q}, VIX_t, D^{(1)}_t, ..., D^{(m)}_t),
donde dFED es la variacion trimestral de la tasa de politica (FEDFUNDS, con la
tasa sombra de Wu-Xia en el piso cero) y D^{(k)} son dummies escalon en los
quiebres de Bai-Perron estimados sobre la propia serie de deuda.

Identificacion (u_t = S eps_t, E[eps eps'] = I):
    eps_pb  ~ e_pb = u_pb - alpha_y u_y
    eps_y   ~ residuo de u_y sobre e_pb
    (eps_e, eps_t) ~ residuos de (u_EMBI, u_TCRM) sobre (e_pb, e_y),
                     ortonormalizados por Cholesky (orden interno irrelevante
                     para las cifras de bloque que se reportan)
    eps_d   ~ residuo de u_d sobre todos los anteriores
S se obtiene por MCO de u sobre eps estandarizados.

Efecto de la FED (H2): multiplicador dinamico de un aumento de un desvio
estandar en dFED en t=0 (aumento permanente del nivel de la tasa), calculado
recursivamente con los A_i y Gamma estimados. No depende de la identificacion.

Intervalos: bootstrap de residuos (semilla fija). Las replicas que fallan se
cuentan y se reportan; no se rellenan con la estimacion puntual.

Uso:
    python codigo/modelos/fase24_svarx_1996_2025.py --deuda neta|bruta
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import het_arch
from statsmodels.tsa.api import VAR

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bai_perron import bai_perron_breaks  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
DATOS = BASE / "datos"
TABLAS = BASE / "resultados" / "tablas"

ALPHA_Y: float = 0.25
SEMILLA: int = 20261011
ENDOG: list[str] = ["pb_pib", "g_gap", "EMBI", "TCRM", "deuda"]
BLOQUES: dict[str, list[int]] = {
    "fiscal": [0],
    "actividad": [1],
    "cambiario_y_riesgo": [2, 3],
    "deuda_propia": [4],
}
SERIES_DEUDA: dict[str, tuple[str, str]] = {
    "neta": ("deuda_consolidada_neta_1996_2025.csv", "deuda_consolidada_neta_pib"),
    "bruta": ("deuda_consolidada_1996_2025.csv", "deuda_consolidada_pib"),
}


def cargar_datos(tipo_deuda: str, rezagos_fed: int) -> tuple[pd.DataFrame, pd.DataFrame, list[pd.Timestamp]]:
    """Arma Y (endogenas) y X (exogenas) alineadas por trimestre.

    Returns:
        (Y, X, fechas_quiebre) sin valores faltantes.
    """
    base = pd.read_csv(DATOS / "dataset_consolidado_1996_2025.csv", parse_dates=["Date"], index_col="Date")
    archivo, columna = SERIES_DEUDA[tipo_deuda]
    deuda = pd.read_csv(DATOS / "procesados" / archivo, parse_dates=["Date"], index_col="Date")[columna]
    fed = pd.read_csv(DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv",
                      parse_dates=["Date"], index_col="Date")["tasa_politica_fed"]

    Y = base[["pb_pib", "g_gap", "EMBI", "TCRM"]].join(deuda.rename("deuda"), how="inner")
    dfed = fed.diff().rename("dFED")
    X = pd.concat([dfed.shift(k).rename(f"dFED_l{k}") for k in range(rezagos_fed + 1)], axis=1)
    # VIX completo 1996-2025 (Yahoo Finance ^VIX, ingesta_instrumentos_1996_2025.py);
    # la columna VIX de dataset_consolidado_1996_2025.csv solo cubre desde 2004.
    vix = pd.read_csv(DATOS / "procesados" / "instrumentos_1996_2025.csv",
                      parse_dates=["Date"], index_col="Date")["VIX"]
    X = X.join(vix, how="inner")

    quiebres = bai_perron_breaks(Y["deuda"].dropna())["fechas_quiebre"]
    for k, fecha in enumerate(quiebres, start=1):
        X[f"D{k}_{fecha.date()}"] = (X.index > fecha).astype(float)

    datos = Y.join(X, how="inner").dropna()
    return datos[ENDOG], datos[X.columns], list(quiebres)


def identificar(u: np.ndarray) -> np.ndarray:
    """Matriz de impacto S (u_t = S eps_t) con el esquema descripto en el modulo.

    Args:
        u: residuos en forma reducida, T x 5, columnas en el orden de ENDOG.
    """
    def resid(y: np.ndarray, X: np.ndarray) -> np.ndarray:
        return y - X @ np.linalg.lstsq(X, y, rcond=None)[0]

    e_pb = u[:, 0] - ALPHA_Y * u[:, 1]
    e_y = resid(u[:, 1], e_pb[:, None])
    v = resid(u[:, 2:4], np.column_stack([e_pb, e_y]))
    w = v @ np.linalg.inv(np.linalg.cholesky(np.cov(v, rowvar=False)).T)
    e_d = resid(u[:, 4], np.column_stack([e_pb, e_y, w]))
    eps = np.column_stack([e_pb, e_y, w, e_d])
    eps = (eps - eps.mean(axis=0)) / eps.std(axis=0, ddof=1)
    return np.linalg.lstsq(eps, u, rcond=None)[0].T


def fevd_bloques(irf: np.ndarray, h: int, var: int = 4) -> dict[str, float]:
    """Contribucion (%) de cada bloque de shocks a la varianza del error de
    pronostico de la variable `var` a h trimestres:
        sum_{s<h} sum_{j in bloque} theta_{var,j}(s)^2 / sum_{s<h} sum_j theta_{var,j}(s)^2.
    La suma sobre j dentro de un bloque es invariante a rotaciones del bloque.
    """
    acum = (irf[:h, var, :] ** 2).sum(axis=0)
    total = acum.sum()
    return {b: 100.0 * acum[idx].sum() / total for b, idx in BLOQUES.items()}


def multiplicador_fed(coefs: np.ndarray, gamma: np.ndarray, tam: float, rezagos_fed: int,
                      horizonte: int) -> np.ndarray:
    """Respuesta de Y a un aumento de `tam` p.p. en dFED en t=0 (los demas
    exogenos fijos). gamma: k x n_exog con las primeras columnas = dFED_l0..l_q.
    """
    p, k, _ = coefs.shape
    resp = np.zeros((horizonte + 1, k))
    for t in range(horizonte + 1):
        x_eff = sum(gamma[:, j] * tam for j in range(rezagos_fed + 1) if t - j == 0)
        din = sum(coefs[i] @ resp[t - 1 - i] for i in range(p) if t - 1 - i >= 0)
        resp[t] = (x_eff if isinstance(x_eff, np.ndarray) else np.zeros(k)) + (
            din if isinstance(din, np.ndarray) else np.zeros(k))
    return resp


def estimar(Y: pd.DataFrame, X: pd.DataFrame, p: int, rezagos_fed: int, tam_fed: float,
            horizonte: int) -> dict:
    """Estima el VARX, identifica y calcula FEVD por bloques y multiplicador FED."""
    res = VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    S = identificar(res.resid.values)
    irf = np.array([res.ma_rep(maxn=horizonte)[h] @ S for h in range(horizonte + 1)])
    gamma = res.params.loc[X.columns].values.T  # k x n_exog
    return {
        "res": res, "S": S, "irf": irf,
        "fevd": {h: fevd_bloques(irf, h) for h in (4, 8, 20)},
        "fed": multiplicador_fed(res.coefs, gamma, tam_fed, rezagos_fed, horizonte),
    }


def bootstrap(Y: pd.DataFrame, X: pd.DataFrame, base: dict, p: int, rezagos_fed: int,
              tam_fed: float, horizonte: int, n_boot: int) -> tuple[pd.DataFrame, int]:
    """Bootstrap de residuos con exogenos fijos. Devuelve las replicas validas
    (FEVD de la deuda a 20 trimestres por bloque y multiplicador FED sobre la
    deuda a 4, 8 y 20 trimestres) y la cantidad de replicas fallidas."""
    rng = np.random.default_rng(SEMILLA)
    res = base["res"]
    u = res.resid.values
    Xv = X.values[p:]
    nu = res.params.loc["const"].values
    gamma = res.params.loc[X.columns].values.T
    filas, fallidas = [], 0
    for _ in range(n_boot):
        ub = u[rng.integers(0, len(u), len(u))]
        y = np.zeros_like(Y.values)
        y[:p] = Y.values[:p]
        for t in range(p, len(y)):
            y[t] = nu + sum(res.coefs[i] @ y[t - 1 - i] for i in range(p)) + gamma @ Xv[t - p] + ub[t - p]
        try:
            rb = estimar(pd.DataFrame(y, index=Y.index, columns=Y.columns), X, p, rezagos_fed,
                         tam_fed, horizonte)
        except (np.linalg.LinAlgError, ValueError):
            fallidas += 1
            continue
        fila = {f"fevd20_{b}": v for b, v in rb["fevd"][20].items()}
        fila.update({f"fed_deuda_h{h}": rb["fed"][h, 4] for h in (4, 8, 20)})
        filas.append(fila)
    return pd.DataFrame(filas), fallidas


def diagnosticos(res, p: int) -> pd.DataFrame:
    """Autocorrelacion (Portmanteau), normalidad (Jarque-Bera multivariado),
    estabilidad (raices) y ARCH-LM por ecuacion."""
    filas = [
        {"prueba": "Portmanteau (12 rezagos)", "p_valor": res.test_whiteness(nlags=12).pvalue},
        {"prueba": "Normalidad multivariada (Jarque-Bera)", "p_valor": res.test_normality().pvalue},
        {"prueba": "Estable (todas las raices fuera del circulo unitario)", "p_valor": float(res.is_stable())},
    ]
    for c in res.resid.columns:
        filas.append({"prueba": f"ARCH-LM (4) ecuacion {c}", "p_valor": het_arch(res.resid[c], nlags=4)[1]})
    return pd.DataFrame(filas)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deuda", choices=list(SERIES_DEUDA), default="neta")
    ap.add_argument("--rezagos-fed", type=int, default=2)
    ap.add_argument("--horizonte", type=int, default=20)
    ap.add_argument("--n-boot", type=int, default=1000)
    a = ap.parse_args()

    Y, X, quiebres = cargar_datos(a.deuda, a.rezagos_fed)
    fed = pd.read_csv(DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv")["tasa_politica_fed"]
    tam_fed = float(fed.diff().std(ddof=1))  # un desvio estandar de dFED (informe_tasa_fed_v1.md)

    sel = VAR(Y, exog=X).select_order(maxlags=6, trend="c")
    p = int(max(1, sel.selected_orders["bic"]))
    base = estimar(Y, X, p, a.rezagos_fed, tam_fed, a.horizonte)
    boot, fallidas = bootstrap(Y, X, base, p, a.rezagos_fed, tam_fed, a.horizonte, a.n_boot)

    TABLAS.mkdir(parents=True, exist_ok=True)
    pre = f"fase24_{a.deuda}"
    pd.DataFrame(sel.selected_orders, index=["rezagos"]).to_csv(TABLAS / f"{pre}_seleccion_rezagos.csv")
    pd.DataFrame(base["S"], index=ENDOG, columns=[f"shock_{c}" for c in ENDOG]).to_csv(TABLAS / f"{pre}_S.csv")
    fevd = pd.DataFrame(base["fevd"]).T
    fevd.index.name = "horizonte_trimestres"
    fevd.to_csv(TABLAS / f"{pre}_fevd_deuda_bloques.csv")
    pd.DataFrame(base["fed"], columns=ENDOG).rename_axis("trimestre").to_csv(TABLAS / f"{pre}_respuesta_fed.csv")
    q = boot.quantile([0.05, 0.5, 0.95]).T
    q.columns = ["p05", "p50", "p95"]
    q.to_csv(TABLAS / f"{pre}_bootstrap.csv")
    diag = diagnosticos(base["res"], p)
    diag.to_csv(TABLAS / f"{pre}_diagnosticos.csv", index=False)

    print(f"SVARX deuda={a.deuda}  n={len(Y)}  p={p} (BIC)  shock FED={tam_fed:.4f} pp")
    print(f"Quiebres Bai-Perron: {[str(f.date()) for f in quiebres]}")
    print(f"Bootstrap: {len(boot)} validas, {fallidas} fallidas")
    print("FEVD deuda (%):\n", fevd.round(1))
    print("Respuesta de la deuda al shock FED (pp PIB), h=4/8/20:",
          [round(base['fed'][h, 4], 3) for h in (4, 8, 20)])
    print("Bootstrap p05/p50/p95:\n", q.round(3))
    print("Diagnosticos:\n", diag.round(4))


if __name__ == "__main__":
    main()
