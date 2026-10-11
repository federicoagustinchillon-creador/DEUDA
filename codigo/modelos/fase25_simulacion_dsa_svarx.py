"""
fase25_simulacion_dsa_svarx.py
==============================
Simulacion de Monte Carlo de la deuda consolidada neta 2026-2035 a partir del SVARX
(fase24), con el escenario base del FMI (CR 25/95, anexo II, cuadro 6). Contrasta H1a
(segunda parte), H1b y H2 (Capitulo 4, seccion 4.7).

Arquitectura (Celasun, Debrun y Ostry, 2006; FMI, 2021, parr. 52):
  1. Escenario base: senderos del FMI para crecimiento real g, deflactor pi, tasa de interes
     nominal efectiva i, resultado primario pb y residuo stock-flujo sf (2026-2035).
  2. Desvios respecto del escenario base: el VARX estimado se simula trimestralmente en
     desvios (40 trimestres), con shocks remuestreados de los residuos y la deuda rezagada
     como regresor (Favero y Giavazzi, 2007). Los desvios se anualizan.
  3. Identidad anual de la deuda (% PIB), con separacion de monedas:
        d_t = d_{t-1} * (1 + i_t + (1-a) * x_t) * (1 + (1-a) * e_t) / ((1 + pi_t)(1 + g_t))
              - pb_t + sf_t
     a: proporcion de deuda en pesos (dic-2025); e_t: desvio de la depreciacion real (TCRM);
     x_t: desvio de la tasa efectiva en dolares, que reprecia gradualmente:
        x_t = (1 - lam) x_{t-1} + lam * (dEMBI_t/1e4 + dFED_t/1e2),
     con lam = necesidades brutas de financiamiento / deuda del escenario base del FMI
     (13% del PIB / 64,1% del PIB promedio 2025-2030; FMI 2025, anexo II, parr. 5 y cuadro 6),
     es decir, la fraccion de la deuda que se refinancia cada anio a tasas de mercado.
  4. Metrica del FMI (2021, parr. 53): la deuda no se estabiliza en T si el resultado primario
     del ESCENARIO BASE en T es menor que el que estabiliza la deuda en la trayectoria, pb*_T = d_{T-1} * (M_T - 1) (formula estandar,
     sin el ajuste stock-flujo), donde M_T
     es el factor de crecimiento de la deuda de la identidad. Se mide en T = 2030 (t+5, como el
     FMI) y T = 2035.

Variantes (misma ventana de datos 1996-2025, misma identidad y misma metrica):
  --canal-domestico: el desvio del EMBI tambien reprecia la deuda en pesos (tasa de interes
     del pais, Neumeyer y Perri, 2005; Uribe y Yue, 2006), con la misma velocidad lam.
  --shocks fmi: en lugar del SVARX, shocks como los del abanico del FMI (2021, anexo VI;
     FMI y ESM, 2023): vectores anuales de desvios respecto de la media historica de la tasa
     real efectiva r, el crecimiento g, la depreciacion real z y el resultado primario pb,
     remuestreados en bloques de dos anios consecutivos y sumados al escenario base.

Incertidumbre: B replicas de parametros (bootstrap salvaje de fase24) x N trayectorias.
H1b: limite inferior del intervalo de 90% de P(no estabilizacion) > 3% (FMI, 2025).
H2: intervalo de 90% de la diferencia (shock FED - base) excluye el cero.
H1a: contribucion de cada bloque de shocks estructurales a la varianza de d_2035.

Uso: python codigo/modelos/fase25_simulacion_dsa_svarx.py [--deuda neta] [--B 300] [--N 400]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase24_svarx_1996_2025 as f24  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
DATOS = BASE / "datos"
TABLAS = BASE / "resultados" / "tablas"

ANIOS = list(range(2026, 2036))
TRIM = 4 * len(ANIOS)
LAM = 13.0 / 64.1
UMBRAL_FMI = 0.03  # FMI (2025), anexo II, cuadro 7: probabilidad de no estabilizacion 3,0%
SEMILLA = 20261012
# Identificacion: "bp" (Blanchard-Perotti + bloque sin orden, seccion 4.4) o "cholesky_fiscal_primero"
# (robustez: Cholesky en el orden pb, crec, EMBI, TCRM, que le atribuye al shock fiscal toda la
# covarianza contemporanea con las demas variables; es el orden mas desfavorable para H1a).
IDENT = "bp"
# Arquitectura A (Paez, 2026): sin retroalimentacion de la deuda sobre el VARX (gamma_d = 0);
# la diferencia con la especificacion principal (arquitectura B) mide cuanto pesa esa retroalimentacion.
SIN_RETRO = False
BLOQUES = {"fiscal": [0], "actividad": [1], "cambiario_y_riesgo": [2, 3]}


def escenario_fmi() -> pd.DataFrame:
    """Senderos anuales del escenario base del FMI (CR 25/95, anexo II, cuadro 6), en %."""
    d = pd.read_csv(DATOS / "procesados" / "escenario_base_fmi_cr2595.csv")
    def serie(v: str) -> pd.Series:
        return d[d.variable == v].drop_duplicates("anio").set_index("anio")["valor"]
    esc = pd.DataFrame({
        "g": serie("srd_pib_real_crecimiento"),
        "pi": serie("srd_inflacion_deflactor"),
        "i": serie("srd_tasa_interes_efectiva"),
        "pb": serie("srd_ingresos_no_intereses") - serie("srd_gastos_no_intereses"),
        "sf": serie("srd_residuo"),
    }).loc[ANIOS]
    if esc.isna().any().any():
        raise ValueError(f"Faltan valores del escenario FMI:\n{esc[esc.isna().any(axis=1)]}")
    return esc


def condiciones_iniciales(tipo: str) -> tuple[float, float, float]:
    """Deuda inicial (dic-2025, % PIB), proporcion en pesos (dic-2025) y TCRM dic-2025."""
    archivo, col = f24.SERIES_DEUDA[tipo]
    d0 = float(pd.read_csv(DATOS / "procesados" / archivo)[col].iloc[-1])
    sh = pd.read_csv(DATOS / "procesados" / "deuda_consolidada_1996_2025.csv")["share_pesos_consolidada_dic"].dropna()
    tcrm = float(pd.read_csv(DATOS / "dataset_consolidado_1996_2025.csv")["TCRM"].iloc[-1])
    return d0, float(sh.iloc[-1]), tcrm


def simular(par: dict, shocks: np.ndarray, fed_path: np.ndarray, esc: pd.DataFrame,
            d0: float, alfa: float, tcrm0: float, dom: bool = False) -> dict[str, np.ndarray]:
    """Simula N trayectorias.

    Args:
        par: coefs (p,k,k), gamma_fed (k,q+1), gamma_d (k,), S (k,k).
        shocks: (N, TRIM, k) shocks estructurales estandarizados (se mapean con S).
        fed_path: (TRIM,) desvio de dFED (p.p.) respecto del escenario base.
    Returns:
        d (N, 11) deuda 2025-2035 y flags de no estabilizacion en 2030 y 2035.
    """
    coefs, gf, gd, S = par["coefs"], par["gamma_fed"], par["gamma_d"], par["S"]
    p, k, _ = coefs.shape
    N = shocks.shape[0]
    u = shocks @ S.T
    y = np.zeros((N, TRIM + p, k))
    fed_nivel = np.cumsum(fed_path)
    d = np.zeros((N, len(ANIOS) + 1))
    d[:, 0] = d0
    x = np.zeros(N)
    x_pes = np.zeros(N)  # desvio de la tasa de la deuda en pesos (solo con dom=True)
    no_est = {}
    d_dev_q = np.zeros(N)
    for t in range(TRIM):
        din = sum(y[:, p + t - 1 - i] @ coefs[i].T for i in range(p))
        fed_t = sum(gf[:, j] * fed_path[t - j] for j in range(gf.shape[1]) if t - j >= 0)
        y[:, p + t] = din + fed_t + np.outer(d_dev_q, gd) + u[:, t]
        if (t + 1) % 4 == 0:
            a = (t + 1) // 4
            yy = y[:, p + t - 3: p + t + 1]
            fila = esc.iloc[a - 1]
            g = fila.g / 100 + yy[:, :, 1].sum(axis=1) / 100
            pb = fila.pb + yy[:, :, 0].mean(axis=1)
            tc_prev = y[:, p + t - 4, 3]
            e = (yy[:, -1, 3] - tc_prev) / tcrm0
            mercado = yy[:, :, 2].mean(axis=1) / 1e4 + fed_nivel[t] / 1e2
            x = (1 - LAM) * x + LAM * mercado
            if dom:
                x_pes = (1 - LAM) * x_pes + LAM * yy[:, :, 2].mean(axis=1) / 1e4
            M = (1 + fila.i / 100 + (1 - alfa) * x + alfa * x_pes) * (1 + (1 - alfa) * e) / ((1 + fila.pi / 100) * (1 + g))
            d[:, a] = d[:, a - 1] * M - pb + fila.sf
            d_base = d[:, a - 1] * (1 + fila.i / 100) / ((1 + fila.pi / 100) * (1 + fila.g / 100)) - fila.pb + fila.sf
            d_dev_q = d[:, a] - d_base
            if ANIOS[a - 1] in (2030, 2035):
                pb_estab = d[:, a - 1] * (M - 1)
                # Definicion literal del FMI (2021, parr. 53): resultado primario del ESCENARIO
                # BASE en T contra el que estabiliza la deuda en cada trayectoria.
                no_est[ANIOS[a - 1]] = fila.pb < pb_estab
                # Variante: resultado primario simulado (incluye el ruido fiscal del anio T).
                no_est[f"sim_{ANIOS[a - 1]}"] = pb < pb_estab
    return {"d": d, "no_est_2030": no_est[2030], "no_est_2035": no_est[2035],
            "no_est_sim_2030": no_est["sim_2030"], "no_est_sim_2035": no_est["sim_2035"]}


def drivers_historicos() -> pd.DataFrame:
    """Impulsores anuales de la deuda 1997-2025 (%), como en el abanico del FMI:
    g: crecimiento real (PIB real anual, INDEC empalmado);
    r: tasa real efectiva = (1 + i)/(1 + pi) - 1, con i = intereses pagados por el SPN en el
       anio (resultado primario menos resultado financiero, MECON, dataset 379) sobre la deuda
       bruta del SPNF a fin del anio anterior, y pi = variacion del deflactor del PIB;
    z: depreciacion real (TCRM del cuarto trimestre contra el del anio anterior);
    pb: resultado primario del SPN (% del PIB, suma de 4 trimestres al cuarto trimestre)."""
    leer = lambda f: pd.read_csv(DATOS / f, parse_dates=["Date"], index_col="Date")
    base = leer("dataset_consolidado_1996_2025.csv")
    pib_pre = leer("procesados/pib_real_empalme_indec_1996_2003.csv")["PIB_real"]
    pib_r = pd.concat([pib_pre, base["PIB_real"][base.index > pib_pre.index.max()]])
    dc = leer("procesados/deuda_consolidada_1996_2025.csv")
    real_a = pib_r.groupby(pib_r.index.year).sum()
    nom_a = dc["pib_4t_mm"][dc.index.quarter == 4]
    nom_a.index = nom_a.index.year
    crudos = DATOS / "crudos" / "resultado_primario"
    tramos = {(1996, 2006): ("379.7_SUPERAVIT_006__28_65", "379.7_RESULTADO_006__23_14"),
              (2007, 2014): ("379.8_SUPERAVIT_014__28_7", "379.8_RESULTADO_014__23_17"),
              (2015, 2025): ("379.9_SUPERAVIT_017__23_94", "379.9_RESULTADO_017__18_38")}
    intereses = {}
    for (a0, a1), (prim, fin) in tramos.items():
        lp = pd.read_csv(crudos / f"{prim}.csv", index_col=0, parse_dates=True).iloc[:, 0]
        lf = pd.read_csv(crudos / f"{fin}.csv", index_col=0, parse_dates=True).iloc[:, 0]
        anual = (lp - lf).groupby(lp.index.year).agg(["sum", "count"])
        for anio in range(a0, a1 + 1):
            if anio in anual.index and anual.loc[anio, "count"] == 12:
                intereses[anio] = anual.loc[anio, "sum"]
    # 2015-2025: la serie mensual del resultado financiero (379.9) tiene meses vacios en la API;
    # se usa la anual oficial del mismo esquema (379.3_RESULTADO_017__18_83).
    fin_a = pd.read_csv(crudos / "379.3_RESULTADO_017__18_83.csv", index_col=0, parse_dates=True).iloc[:, 0]
    prim_m = pd.read_csv(crudos / "379.9_SUPERAVIT_017__23_94.csv", index_col=0, parse_dates=True).iloc[:, 0]
    prim_a = prim_m.groupby(prim_m.index.year).agg(["sum", "count"])
    for fecha, v in fin_a.items():
        if prim_a.loc[fecha.year, "count"] == 12:
            intereses[fecha.year] = prim_a.loc[fecha.year, "sum"] - v
    intereses = pd.Series(intereses)
    deuda_ars = dc["deuda_spnf_ars_mm"][dc.index.quarter == 4]
    deuda_ars.index = deuda_ars.index.year
    tcrm = base["TCRM"][base.index.quarter == 4]
    tcrm.index = tcrm.index.year
    pb = pd.read_csv(DATOS / "procesados" / "resultado_primario_1996_2025.csv", index_col=0, parse_dates=True)["pb_pib"]
    pb = pb[pb.index.quarter == 4]
    pb.index = pb.index.year
    infl = (nom_a / real_a).pct_change()
    i_ef = intereses / deuda_ars.shift(1)
    dr = pd.DataFrame({
        "g": 100 * real_a.pct_change(),
        "r": 100 * ((1 + i_ef) / (1 + infl) - 1),
        "z": 100 * tcrm.pct_change(),
        "pb": pb,
    }).loc[1997:2025]
    if dr.isna().any().any():
        raise ValueError(f"Faltan impulsores historicos:\n{dr[dr.isna().any(axis=1)]}")
    return dr


def simular_fmi(dr: pd.DataFrame, esc: pd.DataFrame, d0: float, alfa: float, N: int, rng) -> dict[str, np.ndarray]:
    """Abanico con shocks a la FMI (2021, anexo VI): desvios de la media historica, remuestreo
    conjunto (mantiene la correlacion entre impulsores) en bloques de dos anios consecutivos
    (mantiene parte de la autocorrelacion), sumados al escenario base. Misma identidad y misma
    metrica de no estabilizacion que simular()."""
    sh = (dr - dr.mean()).values  # (T, 4): g, r, z, pb
    T = len(sh)
    ini = rng.integers(0, T - 1, size=(N, len(ANIOS) // 2))
    s = sh[np.stack([ini, ini + 1], axis=2).reshape(N, -1)]  # (N, 10, 4)
    d = np.zeros((N, len(ANIOS) + 1))
    d[:, 0] = d0
    no_est = {}
    for a, fila in enumerate(esc.itertuples(), start=1):
        g = fila.g / 100 + s[:, a - 1, 0] / 100
        i = fila.i / 100 + s[:, a - 1, 1] / 100 * (1 + fila.pi / 100)
        e = s[:, a - 1, 2] / 100
        pb = fila.pb + s[:, a - 1, 3]
        M = (1 + i) * (1 + (1 - alfa) * e) / ((1 + fila.pi / 100) * (1 + g))
        d[:, a] = d[:, a - 1] * M - pb + fila.sf
        if ANIOS[a - 1] in (2030, 2035):
            no_est[ANIOS[a - 1]] = fila.pb < d[:, a - 1] * (M - 1)
    return {"d": d, "no_est_2030": no_est[2030], "no_est_2035": no_est[2035]}


def impacto(u: np.ndarray) -> np.ndarray:
    """Matriz S (u = S eps) segun la identificacion elegida en IDENT."""
    if IDENT == "cholesky_fiscal_primero":
        return np.linalg.cholesky(np.cov(u, rowvar=False))
    if IDENT == "cholesky_santiago":
        # Orden propuesto en la metodologia de Paez (2026): crecimiento, TCRM, EMBI, resultado
        # primario. Se calcula Cholesky en ese orden y se devuelven filas (variables) y columnas
        # (shocks) al orden de ENDOG (pb, crec, EMBI, TCRM), para que BLOQUES siga valiendo.
        orden = [1, 3, 2, 0]
        L = np.linalg.cholesky(np.cov(u[:, orden], rowvar=False))
        S = np.zeros_like(L)
        S[np.ix_(orden, orden)] = L
        return S
    return f24.identificar(u)


def parametros(res, X_cols: list[str]) -> dict:
    """Extrae del VARX estimado los objetos que usa la simulacion."""
    fed_cols = [c for c in X_cols if c.startswith("dFED")]
    return {"coefs": res.coefs, "gamma_fed": res.params.loc[fed_cols].values.T,
            "gamma_d": 0.0 * res.params.loc["deuda_l1"].values if SIN_RETRO else res.params.loc["deuda_l1"].values, "S": impacto(res.resid.values)}


def replicas(Y: pd.DataFrame, X: pd.DataFrame, p: int, B: int, rng) -> list[dict]:
    """Replicas de parametros por bootstrap salvaje de diseno recursivo (como fase24)."""
    base = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    u = base.resid.values
    Xv = X.values[p:]
    nu = base.params.loc["const"].values
    gamma = base.params.loc[X.columns].values.T
    out = [parametros(base, list(X.columns))]
    while len(out) < B:
        ub = u * rng.choice([-1.0, 1.0], size=(len(u), 1))
        y = Y.values.copy()
        for t in range(p, len(y)):
            y[t] = nu + sum(base.coefs[i] @ y[t - 1 - i] for i in range(p)) + gamma @ Xv[t - p] + ub[t - p]
        try:
            rb = f24.VAR(pd.DataFrame(y, index=Y.index, columns=Y.columns), exog=X).fit(maxlags=p, ic=None, trend="c")
            if rb.is_stable():
                out.append(parametros(rb, list(X.columns)))
        except (np.linalg.LinAlgError, ValueError):
            continue
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deuda", default="neta", choices=list(f24.SERIES_DEUDA))
    ap.add_argument("--B", type=int, default=300)
    ap.add_argument("--N", type=int, default=400)
    ap.add_argument("--canal-domestico", action="store_true")
    ap.add_argument("--shocks", choices=["svarx", "fmi"], default="svarx")
    ap.add_argument("--sin-retroalimentacion", action="store_true")
    ap.add_argument("--identificacion", choices=["bp", "cholesky_fiscal_primero", "cholesky_santiago"], default="bp")
    a = ap.parse_args()
    rng = np.random.default_rng(SEMILLA)
    TABLAS.mkdir(parents=True, exist_ok=True)

    if a.shocks == "fmi":
        esc = escenario_fmi()
        d0, alfa, _ = condiciones_iniciales(a.deuda)
        dr = drivers_historicos()
        dr.to_csv(TABLAS / "fase25_impulsores_historicos_1997_2025.csv")
        s = simular_fmi(dr, esc, d0, alfa, 10_000, rng)
        pct = np.percentile(s["d"], [5, 10, 25, 50, 75, 90, 95], axis=0)
        pd.DataFrame(pct.T, index=[2025] + ANIOS, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]
                     ).rename_axis("anio").to_csv(TABLAS / f"fase25_{a.deuda}_fmi_fanchart.csv")
        out = pd.Series({"p_noest_2030": s["no_est_2030"].mean(), "p_noest_2035": s["no_est_2035"].mean(),
                         "d2035_media": s["d"][:, -1].mean(),
                         "ancho_p5_p95_2030": np.subtract(*np.percentile(s["d"][:, 5], [95, 5])),
                         "ancho_p5_p95_2035": np.subtract(*np.percentile(s["d"][:, -1], [95, 5]))})
        out.to_csv(TABLAS / f"fase25_{a.deuda}_fmi_resumen.csv", header=["valor"])
        print(f"shocks=fmi deuda={a.deuda} d0={d0:.1f}% alfa_pesos={alfa:.3f} N=10000")
        print(dr.describe().round(2).to_string())
        print(out.round(4).to_string())
        return

    Y, X, _ = f24.cargar_datos(a.deuda, 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    Y, X = f24.recortar(Y, X, p)  # muestra efectiva comun 1998T2-2025T4
    dom = a.canal_domestico
    global IDENT, SIN_RETRO
    IDENT = a.identificacion
    SIN_RETRO = a.sin_retroalimentacion
    suf = (f"{a.deuda}_dom" if dom else a.deuda) + {"bp": "", "cholesky_fiscal_primero": "_chol", "cholesky_santiago": "_chol_santiago"}[IDENT] + ("_sin_retro" if SIN_RETRO else "")
    esc = escenario_fmi()
    d0, alfa, tcrm0 = condiciones_iniciales(a.deuda)
    sd_fed = float(pd.read_csv(DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv")["tasa_politica_fed"].diff().std(ddof=1))
    escenarios_fed = {
        "base": np.zeros(TRIM),
        "fed_1de": np.r_[sd_fed, np.zeros(TRIM - 1)],
        "fed_2022_2023": np.r_[np.full(8, 5.25 / 8), np.zeros(TRIM - 8)],
    }
    reps = replicas(Y, X, p, a.B, rng)
    eps_hist = np.linalg.solve(reps[0]["S"], f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c").resid.values.T).T

    filas, varshare = [], []
    for r_i, par in enumerate(reps):
        idx = rng.integers(0, len(eps_hist), size=(a.N, TRIM))
        shocks = eps_hist[idx]  # remuestreo conjunto de shocks estructurales historicos
        fila = {"replica": r_i}
        for nom, path in escenarios_fed.items():
            s = simular(par, shocks, path, esc, d0, alfa, tcrm0, dom)
            fila[f"{nom}_p_noest_2030"] = s["no_est_2030"].mean()
            fila[f"{nom}_p_noest_2035"] = s["no_est_2035"].mean()
            fila[f"{nom}_p_noest_sim_2030"] = s["no_est_sim_2030"].mean()
            fila[f"{nom}_d2035_media"] = s["d"][:, -1].mean()
            if nom == "base":
                fila["base_ancho_p5_p95_2030"] = np.subtract(*np.percentile(s["d"][:, 5], [95, 5]))
                if r_i == 0:
                    pct = np.percentile(s["d"], [5, 10, 25, 50, 75, 90, 95], axis=0)
                    pd.DataFrame(pct.T, index=[2025] + ANIOS, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]
                                 ).rename_axis("anio").to_csv(TABLAS / f"fase25_{suf}_fanchart.csv")
        var_bloque = {}
        for b, cols in BLOQUES.items():
            sh_b = np.zeros_like(shocks)
            sh_b[:, :, cols] = shocks[:, :, cols]
            var_bloque[b] = simular(par, sh_b, escenarios_fed["base"], esc, d0, alfa, tcrm0, dom)["d"][:, -1].var()
        tot = sum(var_bloque.values())
        varshare.append({f"vshare_{b}": 100 * v / tot for b, v in var_bloque.items()})
        filas.append(fila)

    res = pd.concat([pd.DataFrame(filas), pd.DataFrame(varshare)], axis=1)
    res["dif_fed_1de_p_noest_2035"] = res["fed_1de_p_noest_2035"] - res["base_p_noest_2035"]
    res["dif_fed_2022_2023_p_noest_2035"] = res["fed_2022_2023_p_noest_2035"] - res["base_p_noest_2035"]
    res["dif_fed_2022_2023_d2035"] = res["fed_2022_2023_d2035_media"] - res["base_d2035_media"]
    res["h1a_nofiscal_menos_fiscal"] = res["vshare_actividad"] + res["vshare_cambiario_y_riesgo"] - res["vshare_fiscal"]
    TABLAS.mkdir(parents=True, exist_ok=True)
    res.to_csv(TABLAS / f"fase25_{suf}_replicas.csv", index=False)
    resumen = res.drop(columns="replica").agg(["mean", lambda s: s.quantile(0.05), lambda s: s.quantile(0.95)]).T
    resumen.columns = ["media", "p05", "p95"]
    resumen.to_csv(TABLAS / f"fase25_{suf}_resumen.csv")
    print(f"deuda={a.deuda} canal_domestico={dom} p={p} d0={d0:.1f}% alfa_pesos={alfa:.3f} replicas={len(reps)} N={a.N}")
    print(resumen.round(4).to_string())
    print("H1b respaldada (p05 > 3%):", bool(resumen.loc["base_p_noest_2030", "p05"] > UMBRAL_FMI),
          "| 2035:", bool(resumen.loc["base_p_noest_2035", "p05"] > UMBRAL_FMI))


if __name__ == "__main__":
    main()
