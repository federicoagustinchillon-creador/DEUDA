"""
fase25_simulacion_dsa_svarx.py
==============================
Simulacion de Monte Carlo de la deuda consolidada 2026-2035 a partir del SVARX (fase24), alrededor
del escenario base del FMI (Informe de Pais 26/105, mayo de 2026, anexo de sostenibilidad, Table 6).
Contrasta H1a, H1b y H2 (Capitulo 4, seccion 4.7).

Arquitectura (Celasun, Debrun y Ostry, 2006; FMI, 2021, parr. 52):
  1. Escenario base del FMI: crecimiento real g, deflactor pi, tasa efectiva i, resultado primario
     pb, residuo stock-flujo sf e inflacion relativa ri (valuacion de la deuda en moneda extranjera
     por la depreciacion nominal del propio escenario), 2026-2035. Antes de simular se verifica que
     la identidad reproduzca la senda de deuda del FMI partiendo de su propio stock (+-0,5 pp).
  2. Desvios: el VARX se simula trimestralmente en desvios respecto del escenario base (40
     trimestres) con shocks estructurales historicos remuestreados; la deuda acumulada vuelve a
     entrar como desvio respecto de la senda base (retroalimentacion, Favero y Giavazzi, 2007).
  3. Identidad anual (% PIB), con separacion de monedas:
        d_t = d_{t-1} * M_t - pb_t + sf_t + ri_t * d_{t-1} / dFMI_{t-1}
        M_t = (1 + i_t + (1-a) x_t) (1 + (1-a) e_t) / ((1 + pi_t)(1 + g_t))
     a: proporcion en pesos; e_t: desvio de la depreciacion real; x_t: desvio de la tasa en dolares
     (EMBI+ y FED), que reprecia a la velocidad lam (necesidades de financiamiento / deuda del FMI).
     La inflacion relativa del FMI se escala por la razon entre la deuda simulada y la del FMI.
  4. Metrica del FMI (2021, parr. 53 y anexo VI, nota 9): la deuda no se estabiliza en T si el
     resultado primario del escenario base es menor que el que la estabiliza,
        pb*_T = d_{T-1} (M_T - 1) + ri_T d_{T-1} / dFMI_{T-1}.
     Se mide en T = 2031 (t+5 del informe del FMI) y T = 2035 (abanico de diez anios del FMI).

Inferencia:
  - Estimacion central: parametros puntuales con correccion de sesgo de Kilian (1998) en los
    coeficientes de rezago, 20.000 trayectorias; se informa el error de Monte Carlo.
  - Intervalos: B replicas de parametros (bootstrap salvaje de diseno recursivo en el que la deuda
    tambien se regenera, con un VAR auxiliar que la incluye como variable), cada una corregida por
    el mismo sesgo y con N trayectorias. La replica de la estimacion puntual no se incluye.

Uso: python codigo/modelos/fase25_simulacion_dsa_svarx.py [opciones]  (ver --help)
"""

from __future__ import annotations

import argparse
import json
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
METRICA = (2031, 2035)
# (archivo, umbral a mediano plazo, umbral a 2035, primer anio de proyeccion del informe)
# CR 26/105: no estabilizacion 1,0% (Table 7) y estabilizacion superior a 97% a 2035 (parr. 9).
# CR 25/95: no estabilizacion 3,0% (cuadro 7) y alrededor de 97% a 2034.
ESCENARIOS = {
    "cr26105": ("escenario_base_fmi_cr26105.csv", 0.010, 0.030, 2026),
    "cr2595": ("escenario_base_fmi_cr2595.csv", 0.030, 0.030, 2025),
}
ESC = "cr26105"
LAM = 0.28
SEMILLA = 20261012
IDENT = "bp"
SIN_RETRO = False
BLOQUES = {"fiscal": [0], "actividad": [1], "cambiario_y_riesgo": [2, 3]}
DEFAULT = (pd.Timestamp("2001-12-31"), pd.Timestamp("2005-09-30"))  # default y canje


# ---------------------------------------------------------------------------- escenario base
def _serie(d: pd.DataFrame, v: str) -> pd.Series:
    return d[d.variable == v].drop_duplicates("anio").set_index("anio")["valor"]


def velocidad_refinanciacion(esc_id: str) -> float:
    """lam = GFN promedio / deuda promedio en los seis primeros anios de proyeccion del informe."""
    archivo, _, _, inicio = ESCENARIOS[esc_id]
    d = pd.read_csv(DATOS / "procesados" / archivo)
    anios = list(range(inicio, inicio + 6))
    return float(_serie(d, "srd_necesidades_financiamiento_brutas").loc[anios].mean()
                 / _serie(d, "srd_deuda_publica").loc[anios].mean())


def escenario_fmi() -> pd.DataFrame:
    """Senderos anuales del escenario base (%, Table 6), con la deuda del FMI del anio anterior."""
    d = pd.read_csv(DATOS / "procesados" / ESCENARIOS[ESC][0])
    deuda = _serie(d, "srd_deuda_publica")
    esc = pd.DataFrame({
        "g": _serie(d, "srd_pib_real_crecimiento"),
        "pi": _serie(d, "srd_inflacion_deflactor"),
        "i": _serie(d, "srd_tasa_interes_efectiva"),
        "pb": _serie(d, "srd_ingresos_no_intereses") - _serie(d, "srd_gastos_no_intereses"),
        "sf": _serie(d, "srd_residuo"),
        "ri": _serie(d, "srd_inflacion_relativa"),
        "dfmi": deuda,
        "dfmi_prev": deuda.shift(1, freq=None).reindex(deuda.index).fillna(np.nan),
    })
    esc["dfmi_prev"] = [deuda.get(a - 1, np.nan) for a in esc.index]
    esc = esc.loc[ANIOS]
    if esc.isna().any().any():
        raise ValueError(f"Faltan valores del escenario FMI:\n{esc[esc.isna().any(axis=1)]}")
    return esc


def senda_base(esc: pd.DataFrame, d0: float, dpb: float = 0.0, sf_cero: bool = False) -> np.ndarray:
    """Senda determinista de la deuda con el escenario base (sin shocks), 2025-2035."""
    d = [d0]
    for fila in esc.itertuples():
        M = (1 + fila.i / 100) / ((1 + fila.pi / 100) * (1 + fila.g / 100))
        d.append(d[-1] * M - (fila.pb + dpb) + (0.0 if sf_cero else fila.sf) + fila.ri * d[-1] / fila.dfmi_prev)
    return np.array(d)


def verificar_escenario(esc: pd.DataFrame, tolerancia: float = 0.5) -> float:
    """Reproduce la senda de deuda del FMI partiendo de su propio stock. Si la identidad no la
    reproduce dentro de la tolerancia (pp del PIB), el escenario esta mal cargado y se aborta."""
    senda = senda_base(esc, float(esc["dfmi_prev"].iloc[0]))[1:]
    dif = float(np.max(np.abs(senda - esc["dfmi"].values)))
    if dif > tolerancia:
        raise ValueError(f"La identidad no reproduce la senda del FMI (desvio maximo {dif:.2f} pp)")
    return dif


def condiciones_iniciales(tipo: str) -> tuple[float, float, float]:
    """Deuda inicial (dic-2025, % PIB), proporcion en pesos (dic-2025) y TCRM dic-2025."""
    archivo, col = f24.SERIES_DEUDA[tipo]
    d0 = float(pd.read_csv(DATOS / "procesados" / archivo)[col].iloc[-1])
    sh = pd.read_csv(DATOS / "procesados" / "deuda_consolidada_1996_2025.csv")["share_pesos_consolidada_dic"].dropna()
    tcrm = float(pd.read_csv(DATOS / "dataset_consolidado_1996_2025.csv")["TCRM"].iloc[-1])
    return d0, float(sh.iloc[-1]), tcrm


# ---------------------------------------------------------------------------- simulacion
def simular(par: dict, shocks: np.ndarray, fed_path: np.ndarray, esc: pd.DataFrame, d0: float,
            alfa: float, tcrm0: float, dom: bool = False, dpb: float = 0.0,
            sf_cero: bool = False) -> dict[str, np.ndarray]:
    """Simula N trayectorias de la deuda.

    Args:
        par: coefs (p,k,k), gamma_fed (k,q+1), gamma_d (k,), S (k,k).
        shocks: (N, TRIM, k) shocks estructurales estandarizados (u = S eps).
        fed_path: (TRIM,) desvio de la variacion trimestral de la tasa de la FED (pp).
        dpb: puntos del PIB que se suman al resultado primario del escenario base (contraste de
             suficiencia de H1a); se aplican a la senda y a la metrica.
    Returns:
        d (N, 11) deuda 2025-2035 y, para cada T de METRICA: no_est_T (metrica del FMI),
        no_est_sim_T (con el resultado primario simulado) y sube2_T (d_T > d_{T-2}).
    """
    coefs, gf, gd, S = par["coefs"], par["gamma_fed"], par["gamma_d"], par["S"]
    p, k, _ = coefs.shape
    N = shocks.shape[0]
    u = shocks @ S.T
    y = np.zeros((N, TRIM + p, k))
    fed_nivel = np.cumsum(fed_path)
    base = senda_base(esc, d0, dpb, sf_cero)
    d = np.zeros((N, len(ANIOS) + 1))
    d[:, 0] = d0
    x = np.zeros(N)
    x_pes = np.zeros(N)
    d_dev = np.zeros(N)
    out: dict[str, np.ndarray] = {}
    for t in range(TRIM):
        din = sum(y[:, p + t - 1 - i] @ coefs[i].T for i in range(p))
        fed_t = sum(gf[:, j] * fed_path[t - j] for j in range(gf.shape[1]) if t - j >= 0)
        y[:, p + t] = din + fed_t + np.outer(d_dev, gd) + u[:, t]
        if (t + 1) % 4:
            continue
        a = (t + 1) // 4
        yy = y[:, p + t - 3: p + t + 1]
        fila = esc.iloc[a - 1]
        g = fila.g / 100 + yy[:, :, 1].sum(axis=1) / 100
        pb_base = fila.pb + dpb
        pb = pb_base + yy[:, :, 0].mean(axis=1)
        e = (yy[:, -1, 3] - y[:, p + t - 4, 3]) / tcrm0
        x = (1 - LAM) * x + LAM * (yy[:, :, 2].mean(axis=1) / 1e4 + fed_nivel[t] / 1e2)
        if dom:
            x_pes = (1 - LAM) * x_pes + LAM * yy[:, :, 2].mean(axis=1) / 1e4
        M = (1 + fila.i / 100 + (1 - alfa) * x + alfa * x_pes) * (1 + (1 - alfa) * e) / ((1 + fila.pi / 100) * (1 + g))
        ri = fila.ri * d[:, a - 1] / fila.dfmi_prev
        d[:, a] = d[:, a - 1] * M - pb + (0.0 if sf_cero else fila.sf) + ri
        d_dev = d[:, a] - base[a]  # desvio acumulado respecto de la senda base
        anio = ANIOS[a - 1]
        if anio in METRICA:
            pb_estab = d[:, a - 1] * (M - 1) + ri
            out[f"no_est_{anio}"] = pb_base < pb_estab
            out[f"no_est_sim_{anio}"] = pb < pb_estab
            out[f"sube2_{anio}"] = d[:, a] > d[:, a - 2]
    out["d"] = d
    return out


# ---------------------------------------------------------------------------- variante FMI
def drivers_historicos() -> pd.DataFrame:
    """Impulsores anuales de la deuda 1997-2025 (%), como en el abanico del FMI:
    g: crecimiento real; r: tasa real efectiva (intereses pagados del SPN sobre deuda bruta del
    Tesoro del anio anterior, deflactada por el deflactor del PIB); z: depreciacion real (TCRM del
    cuarto trimestre); pb: resultado primario del SPN (% PIB, suma de cuatro trimestres)."""
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
              (2007, 2014): ("379.8_SUPERAVIT_014__28_7", "379.8_RESULTADO_014__23_17")}
    intereses = {}
    for (a0, a1), (prim, fin) in tramos.items():
        lp = pd.read_csv(crudos / f"{prim}.csv", index_col=0, parse_dates=True).iloc[:, 0]
        lf = pd.read_csv(crudos / f"{fin}.csv", index_col=0, parse_dates=True).iloc[:, 0]
        anual = (lp - lf).groupby(lp.index.year).agg(["sum", "count"])
        for anio in range(a0, a1 + 1):
            if anio in anual.index and anual.loc[anio, "count"] == 12:
                intereses[anio] = anual.loc[anio, "sum"]
    # 2015-2025: resultado financiero anual oficial (la serie mensual tiene meses vacios en la API).
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
    dr = pd.DataFrame({"g": 100 * real_a.pct_change(), "r": 100 * ((1 + i_ef) / (1 + infl) - 1),
                       "z": 100 * tcrm.pct_change(), "pb": pb}).loc[1997:2025]
    if dr.isna().any().any():
        raise ValueError(f"Faltan impulsores historicos:\n{dr[dr.isna().any(axis=1)]}")
    return dr


def simular_fmi(dr: pd.DataFrame, esc: pd.DataFrame, d0: float, alfa: float, N: int, rng) -> dict[str, np.ndarray]:
    """Abanico con shocks a la manera del FMI (2021, anexo VI): desvios de la media historica,
    remuestreados como vectores en bloques de dos anios consecutivos y sumados al escenario base.
    Misma identidad (incluida la inflacion relativa) y misma metrica que simular()."""
    sh = (dr - dr.mean()).values
    ini = rng.integers(0, len(sh) - 1, size=(N, len(ANIOS) // 2))
    s = sh[np.stack([ini, ini + 1], axis=2).reshape(N, -1)]
    d = np.zeros((N, len(ANIOS) + 1))
    d[:, 0] = d0
    out: dict[str, np.ndarray] = {}
    for a, fila in enumerate(esc.itertuples(), start=1):
        g = fila.g / 100 + s[:, a - 1, 0] / 100
        i = fila.i / 100 + s[:, a - 1, 1] / 100 * (1 + fila.pi / 100)
        e = s[:, a - 1, 2] / 100
        M = (1 + i) * (1 + (1 - alfa) * e) / ((1 + fila.pi / 100) * (1 + g))
        ri = fila.ri * d[:, a - 1] / fila.dfmi_prev
        d[:, a] = d[:, a - 1] * M - (fila.pb + s[:, a - 1, 3]) + fila.sf + ri
        if ANIOS[a - 1] in METRICA:
            out[f"no_est_{ANIOS[a - 1]}"] = fila.pb < d[:, a - 1] * (M - 1) + ri
    out["d"] = d
    return out


# ---------------------------------------------------------------------------- parametros
def impacto(u: np.ndarray) -> np.ndarray:
    """Matriz S (u = S eps) segun la identificacion elegida en IDENT."""
    if IDENT == "cholesky_fiscal_primero":
        return np.linalg.cholesky(np.cov(u, rowvar=False))
    if IDENT == "cholesky_fiscal_ultimo":
        # Orden crecimiento, TCRM, EMBI+, resultado primario; filas y columnas vuelven al orden
        # de ENDOG (pb, crec, EMBI, TCRM) para que BLOQUES siga valiendo.
        orden = [1, 3, 2, 0]
        L = np.linalg.cholesky(np.cov(u[:, orden], rowvar=False))
        S = np.zeros_like(L)
        S[np.ix_(orden, orden)] = L
        return S
    return f24.identificar(u)


def estable(coefs: np.ndarray) -> bool:
    """Todos los autovalores de la matriz companera con modulo menor que uno."""
    p, k, _ = coefs.shape
    comp = np.zeros((k * p, k * p))
    comp[:k] = np.hstack(list(coefs))
    comp[k:, :-k] = np.eye(k * (p - 1))
    return bool(np.max(np.abs(np.linalg.eigvals(comp))) < 1)


def corregir_sesgo(coefs: np.ndarray, sesgo: np.ndarray) -> tuple[np.ndarray, float]:
    """Correccion de Kilian (1998): coefs - delta * sesgo, con delta que se reduce de a 0,01
    hasta que el VAR corregido sea estable (delta = 1 si ya lo es)."""
    delta = 1.0
    while delta > 0:
        c = coefs - delta * sesgo
        if estable(c):
            return c, delta
        delta = round(delta - 0.01, 2)
    return coefs, 0.0


def parametros(res, X_cols: list[str], coefs: np.ndarray | None = None) -> dict:
    """Objetos que usa la simulacion; coefs permite pasar los coeficientes corregidos por sesgo."""
    fed_cols = [c for c in X_cols if c.startswith("dFED")]
    gd = res.params.loc["deuda_l1"].values
    return {"coefs": res.coefs if coefs is None else coefs, "gamma_fed": res.params.loc[fed_cols].values.T,
            "gamma_d": 0.0 * gd if SIN_RETRO else gd, "S": impacto(res.resid.values)}


def generador(Y: pd.DataFrame, X: pd.DataFrame, deuda: pd.Series, p: int):
    """Proceso generador del bootstrap: VAR auxiliar con la deuda como quinta variable, para que
    la deuda se regenere en cada replica (diseno recursivo, Goncalves y Kilian, 2004).
    Devuelve el ajuste auxiliar y una funcion muestra(rng, A) que genera datos con los
    coeficientes de rezago A (los estimados o los corregidos por sesgo)."""
    Xa = X.drop(columns="deuda_l1")
    Z = pd.concat([Y, deuda.reindex(Y.index).rename("deuda")], axis=1)
    aux = f24.VAR(Z, exog=Xa).fit(maxlags=p, ic=None, trend="c")
    nu = aux.params.loc["const"].values
    G = aux.params.loc[Xa.columns].values.T
    U = aux.resid.values
    Xav = Xa.values

    def muestra(rng, A: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        ub = U * rng.choice([-1.0, 1.0], size=(len(U), 1))
        z = Z.values.copy()
        for t in range(p, len(z)):
            z[t] = nu + sum(A[i] @ z[t - 1 - i] for i in range(p)) + G @ Xav[t] + ub[t - p]
        Yb = pd.DataFrame(z[:, :4], index=Y.index, columns=Y.columns)
        Xb = X.copy()
        Xb["deuda_l1"] = np.r_[X["deuda_l1"].iloc[0], z[:-1, 4]]
        return Yb, Xb, pd.DataFrame(z, index=Z.index, columns=Z.columns)
    return aux, Xa, muestra


def replicas(Y: pd.DataFrame, X: pd.DataFrame, deuda: pd.Series, p: int, B: int, B1: int, rng) -> tuple[dict, list[dict], dict]:
    """Bootstrap-after-bootstrap de Kilian (1998).
    Etapa 1: B1 muestras del proceso generador estimado; con ellas se mide el sesgo de los
    coeficientes de rezago del SVARX y del VAR auxiliar. Ambos se corrigen (con reduccion del
    factor si la correccion vuelve inestable al VAR). Etapa 2: B muestras generadas con el VAR
    auxiliar corregido; cada estimacion del SVARX se corrige por el mismo sesgo."""
    base = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    aux, Xa, muestra = generador(Y, X, deuda, p)
    est_m, est_a = [], []
    while len(est_m) < B1:
        Yb, Xb, Zb = muestra(rng, aux.coefs)
        try:
            est_m.append(f24.VAR(Yb, exog=Xb).fit(maxlags=p, ic=None, trend="c").coefs)
            est_a.append(f24.VAR(Zb, exog=Xa).fit(maxlags=p, ic=None, trend="c").coefs)
        except (np.linalg.LinAlgError, ValueError):
            continue
    sesgo = np.mean(est_m, axis=0) - base.coefs
    sesgo_aux = np.mean(est_a, axis=0) - aux.coefs
    coefs_c, delta_c = corregir_sesgo(base.coefs, sesgo)
    aux_c, delta_aux = corregir_sesgo(aux.coefs, sesgo_aux)
    central = parametros(base, list(X.columns), coefs_c)
    out, deltas, fallidas = [], [], 0
    while len(out) < B:
        Yb, Xb, _ = muestra(rng, aux_c)
        try:
            rb = f24.VAR(Yb, exog=Xb).fit(maxlags=p, ic=None, trend="c")
        except (np.linalg.LinAlgError, ValueError):
            fallidas += 1
            continue
        c, dl = corregir_sesgo(rb.coefs, sesgo)
        if dl == 0.0 and not estable(c):
            fallidas += 1
            continue
        deltas.append(dl)
        out.append(parametros(rb, list(X.columns), c))

    def raiz(c: np.ndarray) -> float:
        k = c.shape[1]
        comp = np.zeros((k * p, k * p))
        comp[:k] = np.hstack(list(c))
        comp[k:, :-k] = np.eye(k * (p - 1))
        return float(np.max(np.abs(np.linalg.eigvals(comp))))
    meta = {"delta_central": delta_c, "delta_auxiliar": delta_aux,
            "raiz_max_estimada": raiz(base.coefs), "raiz_max_corregida": raiz(coefs_c),
            "raiz_max_mediana_replicas": float(np.median([raiz(r["coefs"]) for r in out])),
            "replicas_fallidas_o_inestables": fallidas, "delta_medio_replicas": float(np.mean(deltas)),
            "replicas_con_delta_menor_a_1": int(sum(d < 1 for d in deltas))}
    return central, out, meta


# ---------------------------------------------------------------------------- medidas
def medidas(par: dict, shocks: np.ndarray, fed: dict[str, np.ndarray], esc: pd.DataFrame, d0: float,
            alfa: float, tcrm0: float, dom: bool, sf_cero: bool) -> dict[str, float]:
    """Todas las medidas de H1a, H1b y H2 para un juego de parametros."""
    f: dict[str, float] = {}
    sims = {nom: simular(par, shocks, path, esc, d0, alfa, tcrm0, dom, sf_cero=sf_cero) for nom, path in fed.items()}
    for nom, s in sims.items():
        for T in METRICA:
            f[f"{nom}_p_noest_{T}"] = float(s[f"no_est_{T}"].mean())
        f[f"{nom}_d2035_media"] = float(s["d"][:, -1].mean())
    b = sims["base"]
    for T in METRICA:
        f[f"base_p_noest_sim_{T}"] = float(b[f"no_est_sim_{T}"].mean())
        f[f"base_p_sube2_{T}"] = float(b[f"sube2_{T}"].mean())
    i31 = ANIOS.index(2031) + 1
    f["base_ancho_p5_p95_2031"] = float(np.subtract(*np.percentile(b["d"][:, i31], [95, 5])))
    f["base_d2031_mediana"] = float(np.median(b["d"][:, i31]))
    for nom in fed:
        if nom != "base":
            for T in METRICA:
                f[f"dif_{nom}_p_noest_{T}"] = f[f"{nom}_p_noest_{T}"] - f[f"base_p_noest_{T}"]
            f[f"dif_{nom}_d2035"] = f[f"{nom}_d2035_media"] - f["base_d2035_media"]
    # Varianza de la deuda en 2035 por shock y por bloque (cada uno simulado solo).
    var = {}
    for nombre, cols in {"fiscal": [0], "actividad": [1], "shock_3": [2], "shock_4": [3], "cambiario_y_riesgo": [2, 3]}.items():
        sh = np.zeros_like(shocks)
        sh[:, :, cols] = shocks[:, :, cols]
        var[nombre] = float(simular(par, sh, fed["base"], esc, d0, alfa, tcrm0, dom, sf_cero=sf_cero)["d"][:, -1].var())
    tot = var["fiscal"] + var["actividad"] + var["cambiario_y_riesgo"]
    for nombre in ("fiscal", "actividad", "cambiario_y_riesgo"):
        f[f"vshare_{nombre}"] = 100 * var[nombre] / tot
    f["var_total_2035"] = float(b["d"][:, -1].var())
    f["var_suma_bloques_2035"] = tot
    f["h1a_cambiario_menos_fiscal"] = f["vshare_cambiario_y_riesgo"] - f["vshare_fiscal"]
    f["h1a_nofiscal_menos_fiscal"] = f["vshare_actividad"] + f["vshare_cambiario_y_riesgo"] - f["vshare_fiscal"]
    # Por shock: promedio de los dos shocks del bloque cambiario y de riesgo contra el fiscal.
    f["h1a_por_shock_cambiario_menos_fiscal"] = 100 * ((var["shock_3"] + var["shock_4"]) / 2 - var["fiscal"]) / tot
    return f


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deuda", default="neta", choices=list(f24.SERIES_DEUDA))
    ap.add_argument("--B", type=int, default=200)
    ap.add_argument("--B1", type=int, default=100, help="replicas de la primera etapa (sesgo)")
    ap.add_argument("--N", type=int, default=1000)
    ap.add_argument("--N-central", type=int, default=20000)
    ap.add_argument("--canal-domestico", action="store_true")
    ap.add_argument("--shocks", choices=["svarx", "fmi"], default="svarx")
    ap.add_argument("--sin-retroalimentacion", action="store_true")
    ap.add_argument("--identificacion", choices=["bp", "cholesky_fiscal_primero", "cholesky_fiscal_ultimo"], default="bp")
    ap.add_argument("--escenario", choices=list(ESCENARIOS), default="cr26105")
    ap.add_argument("--sin-default", action="store_true", help="excluye 2001T4-2005T3 del remuestreo de shocks")
    ap.add_argument("--sf-cero", action="store_true", help="ajuste stock-flujo del FMI en cero")
    ap.add_argument("--pb-sin-rentas", action="store_true")
    ap.add_argument("--desde-2004", action="store_true")
    ap.add_argument("--lam", type=float, default=None)
    ap.add_argument("--alpha-y", type=float, default=None)
    ap.add_argument("--d0", type=float, default=None, help="deuda inicial (p. ej. 52,1: la del FMI)")
    ap.add_argument("--p", type=int, default=None, help="orden del VAR (robustez); por defecto, la regla de fase24")
    ap.add_argument("--suficiencia", action="store_true", help="contraste de suficiencia del superavit (H1a)")
    a = ap.parse_args()
    global ESC, LAM, IDENT, SIN_RETRO
    ESC, IDENT, SIN_RETRO = a.escenario, a.identificacion, a.sin_retroalimentacion
    LAM = a.lam if a.lam is not None else velocidad_refinanciacion(ESC)
    if a.alpha_y is not None:
        f24.ALPHA_Y = a.alpha_y
    if a.pb_sin_rentas:
        f24.PB_COLUMNA = "pb_pib_trim_sin_rentas"
    if a.desde_2004:
        f24.DESDE = "2004-01-01"
    _, umbral_mp, umbral_lp, _ = ESCENARIOS[ESC]
    rng = np.random.default_rng(SEMILLA)
    TABLAS.mkdir(parents=True, exist_ok=True)
    esc = escenario_fmi()
    desvio_fmi = verificar_escenario(esc)
    d0, alfa, tcrm0 = condiciones_iniciales(a.deuda)
    if a.d0 is not None:
        d0 = a.d0
    etiquetas = [a.deuda, "dom" if a.canal_domestico else "", {"bp": "", "cholesky_fiscal_primero": "chol",
                 "cholesky_fiscal_ultimo": "chol_ultimo"}[IDENT], "sin_retro" if SIN_RETRO else "",
                 "" if ESC == "cr26105" else ESC, "sin_default" if a.sin_default else "", "sf0" if a.sf_cero else "",
                 "sin_rentas" if a.pb_sin_rentas else "", "desde2004" if a.desde_2004 else "",
                 f"lam{a.lam:g}" if a.lam is not None else "", f"alfa{a.alpha_y:g}" if a.alpha_y is not None else "",
                 f"d0_{a.d0:g}" if a.d0 is not None else "", f"p{a.p}" if a.p is not None else ""]
    suf = "_".join(e for e in etiquetas if e)

    if a.shocks == "fmi":
        dr = drivers_historicos()
        dr.to_csv(TABLAS / "fase25_impulsores_historicos_1997_2025.csv")
        s = simular_fmi(dr, esc, d0, alfa, a.N_central, rng)
        i31 = ANIOS.index(2031) + 1
        out = pd.Series({**{f"p_noest_{T}": s[f"no_est_{T}"].mean() for T in METRICA},
                         "d2035_media": s["d"][:, -1].mean(),
                         "ancho_p5_p95_2031": np.subtract(*np.percentile(s["d"][:, i31], [95, 5]))})
        pct = np.percentile(s["d"], [5, 10, 25, 50, 75, 90, 95], axis=0)
        pd.DataFrame(pct.T, index=[2025] + ANIOS, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]
                     ).rename_axis("anio").to_csv(TABLAS / f"fase25_{suf}_fmi_fanchart.csv")
        out.to_csv(TABLAS / f"fase25_{suf}_fmi_resumen.csv", header=["valor"])
        print(f"shocks=fmi {suf} d0={d0:.1f} N={a.N_central}")
        print(out.round(4).to_string())
        return

    Y, X, _ = f24.cargar_datos(a.deuda, 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    if a.p is not None:
        p = a.p
    Y, X = f24.recortar(Y, X, p)
    archivo, col = f24.SERIES_DEUDA[a.deuda]
    deuda = pd.read_csv(DATOS / "procesados" / archivo, parse_dates=["Date"], index_col="Date")[col]
    central, reps, meta = replicas(Y, X, deuda, p, a.B, a.B1, rng)
    resid = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c").resid
    eps = pd.DataFrame(np.linalg.solve(central["S"], resid.values.T).T, index=resid.index)
    if a.sin_default:
        eps = eps[(eps.index < DEFAULT[0]) | (eps.index > DEFAULT[1])]
    eps_hist = eps.values

    fedfunds = pd.read_csv(DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv", parse_dates=["Date"], index_col="Date")
    sd_fed = float(fedfunds["tasa_politica_fed"].diff().std(ddof=1))
    ciclo = fedfunds["fedfunds"].diff().loc["2022-01-01":"2025-12-31"].values
    fed = {"base": np.zeros(TRIM), "fed_1de": np.r_[sd_fed, np.zeros(TRIM - 1)],
           "fed_2022_2025": np.r_[ciclo, np.zeros(TRIM - len(ciclo))]}

    # Estimacion central
    shocks_c = eps_hist[rng.integers(0, len(eps_hist), size=(a.N_central, TRIM))]
    cen = medidas(central, shocks_c, fed, esc, d0, alfa, tcrm0, a.canal_domestico, a.sf_cero)
    sb = simular(central, shocks_c, fed["base"], esc, d0, alfa, tcrm0, a.canal_domestico, sf_cero=a.sf_cero)
    pct = np.percentile(sb["d"], [5, 10, 25, 50, 75, 90, 95], axis=0)
    pd.DataFrame(pct.T, index=[2025] + ANIOS, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]
                 ).rename_axis("anio").to_csv(TABLAS / f"fase25_{suf}_fanchart.csv")
    # Canal directo de la FED: misma estimacion central sin respuesta de las variables domesticas.
    sin_ind = dict(central, gamma_fed=np.zeros_like(central["gamma_fed"]))
    sd = simular(sin_ind, shocks_c, fed["fed_2022_2025"], esc, d0, alfa, tcrm0, a.canal_domestico, sf_cero=a.sf_cero)
    cen["dif_fed_2022_2025_d2035_solo_costo_directo"] = float(sd["d"][:, -1].mean()) - cen["base_d2035_media"]
    cen["senda_base_d2031"] = float(senda_base(esc, d0, sf_cero=a.sf_cero)[ANIOS.index(2031) + 1])
    cen["senda_base_d2035"] = float(senda_base(esc, d0, sf_cero=a.sf_cero)[-1])

    if a.suficiencia:
        filas = []
        sh_s = shocks_c[: a.N_central // 2]
        for dpb in np.arange(0, 6.01, 0.25):
            s = simular(central, sh_s, fed["base"], esc, d0, alfa, tcrm0, a.canal_domestico, dpb=dpb, sf_cero=a.sf_cero)
            filas.append({"dpb": dpb, "pb_2031": float(esc.loc[2031, "pb"] + dpb),
                          "p_noest_2031": float(s["no_est_2031"].mean()), "p_noest_2035": float(s["no_est_2035"].mean())})
        pd.DataFrame(filas).to_csv(TABLAS / f"fase25_{suf}_suficiencia.csv", index=False)

    filas = []
    for r_i, par in enumerate(reps):
        shocks = eps_hist[rng.integers(0, len(eps_hist), size=(a.N, TRIM))]
        filas.append({"replica": r_i, **medidas(par, shocks, fed, esc, d0, alfa, tcrm0, a.canal_domestico, a.sf_cero)})
    res = pd.DataFrame(filas)
    res.to_csv(TABLAS / f"fase25_{suf}_replicas.csv", index=False)
    resumen = pd.DataFrame({"estimacion": pd.Series(cen),
                            "p05": res.drop(columns="replica").quantile(0.05),
                            "p95": res.drop(columns="replica").quantile(0.95)})
    for T in METRICA:
        pr = cen[f"base_p_noest_{T}"]
        resumen.loc[f"error_mc_p_noest_{T}", "estimacion"] = np.sqrt(pr * (1 - pr) / a.N_central)
    resumen.to_csv(TABLAS / f"fase25_{suf}_resumen.csv")
    meta.update({"escenario": ESC, "lam": LAM, "alpha_y": f24.ALPHA_Y, "d0": d0, "alfa_pesos": alfa, "p": p,
                 "B": a.B, "B1": a.B1, "N": a.N, "N_central": a.N_central, "desvio_max_senda_fmi": desvio_fmi,
                 "umbral_mediano_plazo": umbral_mp, "umbral_2035": umbral_lp, "trimestres_de_shocks": len(eps_hist)})
    (TABLAS / f"fase25_{suf}_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"{suf}: {json.dumps(meta)}")
    print(resumen.round(4).to_string())
    print(f"H1b: 2031 p05 > {umbral_mp:.0%}: {resumen.loc['base_p_noest_2031', 'p05'] > umbral_mp} | "
          f"2035 p05 > {umbral_lp:.0%}: {resumen.loc['base_p_noest_2035', 'p05'] > umbral_lp}")


if __name__ == "__main__":
    main()
