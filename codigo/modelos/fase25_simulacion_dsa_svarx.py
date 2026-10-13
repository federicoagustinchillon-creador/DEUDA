"""
fase25_simulacion_dsa_svarx.py
==============================
Simulacion de Monte Carlo de la deuda publica 2026-2035 a partir del SVARX (fase24), alrededor
del escenario base del FMI (Informe de Pais 26/105, mayo de 2026, anexo II, cuadro 6).
Contrasta H1a, H1b y H2 (Capitulo 4, seccion 4.7).

Perimetros:
  - federal (principal): deuda bruta del gobierno federal, el perimetro del analisis de
    sostenibilidad del FMI. Punto de partida: el stock del FMI a fines de 2025 (80,3% del PIB,
    cuadro 2), de modo que escenario, perimetro, punto de partida y metrica son los del FMI.
  - consolidada (extension): deuda del sector publico consolidado con el BCRA en la definicion
    del FMI (cuadro 2, linea 5: 52,1% del PIB, 68,5% en moneda extranjera).

Arquitectura (Celasun, Debrun y Ostry, 2006; FMI, 2021, parr. 52):
  1. Escenario base del FMI: crecimiento real g, deflactor pi, tasa efectiva i, resultado primario
     pb, ajuste stock-flujo sf e inflacion relativa ri, 2026-2035. Antes de simular se verifica
     que la identidad reproduzca la senda de deuda del FMI partiendo de su propio stock.
  2. Desvios: el SVARX se simula trimestralmente en desvios respecto del escenario base (40
     trimestres). Los shocks estructurales historicos y las innovaciones de las variables
     externas (VIX y tasa de la FED, cada una con su proceso AR(1)) se remuestrean juntos, por
     fecha, en bloques de ocho trimestres consecutivos, como los bloques de dos anios del FMI
     (2021, anexo VI). La deuda acumulada vuelve a entrar como desvio respecto de la senda base
     (retroalimentacion, Favero y Giavazzi, 2007).
  3. Identidad anual (% del PIB), con separacion de monedas:
        d_t = d_{t-1} M_t - pb_t + sf_t + ri_t
        M_t = (1 + i_t + (1-a) x_t)(1 + (1-a) e_t) / ((1 + pi_t)(1 + g_t))
     a: proporcion en pesos (fija en el escenario, como en el FMI, 2021, anexo VI, parr. 6);
     e_t: desvio de la depreciacion real; x_t: desvio de la tasa en dolares (EMBI+ y FED), que
     se reprecia a la velocidad lam. El ajuste stock-flujo del FMI (sobre todo capitalizacion de
     deuda indexada) se escala por la deuda en pesos y la inflacion relativa por la deuda en
     moneda extranjera, ambas relativas a las del FMI. El desvio del crecimiento anual es la
     variacion del promedio anual del nivel del PIB, no la suma de las tasas trimestrales.
  4. Metrica del FMI (2021, parr. 53): la deuda no se estabiliza en T si el resultado primario
     del escenario base es menor que el que estabiliza la deuda en T,
        pb*_T = d_{T-1} (M_T - 1) + sf_T + ri_T.
     Se mide en T = 2031 (t+5 del informe del FMI) y T = 2035 (abanico de diez anios del FMI).

Inferencia:
  - Estimacion central: parametros de minimos cuadrados, 20.000 trayectorias; se informa el
    error de Monte Carlo. Todas las especificaciones usan los mismos numeros aleatorios.
  - Intervalos de 90%: B replicas de parametros con un bootstrap de bloques moviles de diseno
    recursivo (Bruggemann, Jentsch y Trenkler, 2016) en el que la deuda tambien se regenera, y
    percentiles de Hall (1992). Variante --kilian: parametros corregidos por sesgo (Kilian, 1998).

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
# (archivo, probabilidad del FMI a mediano plazo, a 2035, primer anio de proyeccion del informe)
# CR 26/105: no estabilizacion 1,0% (cuadro 7) y estabilizacion superior a 97% a 2035 (parr. 9).
# CR 25/95: no estabilizacion 3,0% (cuadro 7) y alrededor de 97% a 2034.
ESCENARIOS = {
    "cr26105": ("escenario_base_fmi_cr26105.csv", 0.010, 0.030, 2026),
    "cr2595": ("escenario_base_fmi_cr2595.csv", 0.030, 0.030, 2025),
}
# Deuda consolidada del FMI a fines de 2025 (CR 26/105, anexo II, cuadro 2, linea 5) y su
# proporcion en pesos (linea 5b / linea 5).
CONSOLIDADA_FMI_2025 = 52.1
PESOS_CONSOLIDADA_FMI_2025 = 16.4 / 52.1
ESC = "cr26105"
LAM = 0.28
SEMILLA = 20261012
IDENT = "bp"
SIN_RETRO = False
KILIAN = False
BLOQUE_SIM = 8   # trimestres: bloques de dos anios, como el abanico del FMI
BLOQUE_INF = 4   # trimestres: bootstrap de bloques de la inferencia (~T^(1/3))
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
    """Senderos anuales del escenario base (%, cuadro 6), con la deuda del FMI del anio anterior."""
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
    })
    esc["dfmi_prev"] = [deuda.get(a - 1, np.nan) for a in esc.index]
    esc = esc.loc[ANIOS]
    if esc.isna().any().any():
        raise ValueError(f"Faltan valores del escenario FMI:\n{esc[esc.isna().any(axis=1)]}")
    return esc


def flujos_escalados(fila, d_prev: np.ndarray | float, a: float, a_fmi: float) -> tuple:
    """Ajuste stock-flujo e inflacion relativa del FMI escalados al stock simulado: el primero
    por la deuda en pesos (capitalizacion de deuda indexada) y la segunda por la deuda en moneda
    extranjera, cada una relativa a la del FMI del anio anterior."""
    sf = fila.sf * (a * d_prev) / (a_fmi * fila.dfmi_prev)
    ri = fila.ri * ((1 - a) * d_prev) / ((1 - a_fmi) * fila.dfmi_prev)
    return sf, ri


def senda_base(esc: pd.DataFrame, d0: float, a: float, a_fmi: float, dpb: float = 0.0,
               sf_cero: bool = False) -> np.ndarray:
    """Senda determinista de la deuda con el escenario base (sin shocks), 2025-2035."""
    d = [d0]
    for fila in esc.itertuples():
        M = (1 + fila.i / 100) / ((1 + fila.pi / 100) * (1 + fila.g / 100))
        sf, ri = flujos_escalados(fila, d[-1], a, a_fmi)
        d.append(d[-1] * M - (fila.pb + dpb) + (0.0 if sf_cero else sf) + ri)
    return np.array(d)


def verificar_escenario(esc: pd.DataFrame, a_fmi: float, tolerancia: float = 0.5) -> float:
    """Reproduce la senda de deuda del FMI partiendo de su propio stock. Si la identidad no la
    reproduce dentro de la tolerancia (pp del PIB), el escenario esta mal cargado y se aborta."""
    senda = senda_base(esc, float(esc["dfmi_prev"].iloc[0]), a_fmi, a_fmi)[1:]
    dif = float(np.max(np.abs(senda - esc["dfmi"].values)))
    if dif > tolerancia:
        raise ValueError(f"La identidad no reproduce la senda del FMI (desvio maximo {dif:.2f} pp)")
    return dif


def condiciones_iniciales(tipo: str, esc: pd.DataFrame) -> tuple[float, float, float, float]:
    """Deuda inicial (dic-2025, % PIB), proporcion en pesos, proporcion en pesos de la deuda del
    FMI (federal bruta) y TCRM de dic-2025.
    federal: el stock del FMI (cuadro 2, linea 1), que incluye intereses capitalizados y deuda
    no presentada al canje; proporcion en pesos de la deuda de la Administracion Central (MECON).
    consolidada: el stock consolidado del FMI (linea 5) y su proporcion en pesos (5b / 5).
    Otras series (robustez): el ultimo valor propio y la proporcion de la deuda bruta con el BCRA."""
    dc = pd.read_csv(DATOS / "procesados" / "deuda_consolidada_1996_2025.csv")
    a_fmi = float(dc["share_pesos_spnf_dic"].dropna().iloc[-1])
    tcrm = float(pd.read_csv(DATOS / "dataset_consolidado_1996_2025.csv")["TCRM"].iloc[-1])
    if tipo == "federal":
        return float(esc["dfmi_prev"].iloc[0]), a_fmi, a_fmi, tcrm
    if tipo == "consolidada":
        return CONSOLIDADA_FMI_2025, PESOS_CONSOLIDADA_FMI_2025, a_fmi, tcrm
    archivo, col = f24.SERIES_DEUDA[tipo]
    d0 = float(pd.read_csv(DATOS / "procesados" / archivo)[col].iloc[-1])
    return d0, float(dc["share_pesos_consolidada_dic"].dropna().iloc[-1]), a_fmi, tcrm


# ---------------------------------------------------------------------------- variables externas
def procesos_externos(fechas: pd.DatetimeIndex) -> tuple[dict, pd.DataFrame]:
    """AR(1) del VIX y del nivel de la tasa de politica de la FED (reconstruido con las
    variaciones empalmadas), estimados en la muestra; devuelve los coeficientes y las
    innovaciones en las fechas de los residuos del SVARX, para remuestrearlas juntas."""
    leer = lambda f: pd.read_csv(DATOS / f, parse_dates=["Date"], index_col="Date")
    vix = leer("procesados/instrumentos_1996_2025.csv")["VIX"]
    fed = f24.dfed_empalmado(leer("procesados/tasa_fed_trimestral_1996_2025.csv")).cumsum()
    phi, innov = {}, {}
    for nombre, s in {"vix": vix, "fed": fed}.items():
        z = pd.concat([s, s.shift(1)], axis=1).dropna()
        z = z[z.index >= fechas.min() - pd.offsets.QuarterEnd(1)]
        Xr = np.column_stack([np.ones(len(z)), z.iloc[:, 1].values])
        b = np.linalg.lstsq(Xr, z.iloc[:, 0].values, rcond=None)[0]
        phi[nombre] = float(b[1])
        innov[nombre] = pd.Series(z.iloc[:, 0].values - Xr @ b, index=z.index)
    return phi, pd.DataFrame(innov).reindex(fechas)


def indices_bloques(rng, n: int, N: int, T: int, L: int) -> np.ndarray:
    """(N, T) indices de remuestreo por bloques moviles de L trimestres consecutivos."""
    k = -(-T // L)
    ini = rng.integers(0, n - L + 1, size=(N, k))
    return (ini[:, :, None] + np.arange(L)).reshape(N, -1)[:, :T]


# ---------------------------------------------------------------------------- simulacion
def simular(par: dict, shocks: np.ndarray, ext: np.ndarray, fed_path: np.ndarray, esc: pd.DataFrame,
            d0: float, alfa: float, a_fmi: float, tcrm0: float, dom: bool = False, dpb: float = 0.0,
            sf_cero: bool = False) -> dict[str, np.ndarray]:
    """Simula N trayectorias de la deuda.

    Args:
        par: coefs (p,k,k), gamma_fed (k,q+1), gamma_vix (k,), gamma_d (k,), S (k,k), phi.
        shocks: (N, TRIM, k) shocks estructurales estandarizados (u = S eps).
        ext: (N, TRIM, 2) innovaciones del VIX y del nivel de la tasa de la FED.
        fed_path: (TRIM,) variacion trimestral de la tasa de la FED que agrega el escenario (pp).
        dpb: puntos del PIB que se suman al resultado primario del escenario base en todos los
             anios (contraste de suficiencia de H1a); se aplican a la senda y a la metrica.
    Returns:
        d (N, 11) deuda 2025-2035 y, para cada T de METRICA: no_est_T (metrica del FMI),
        no_est_sim_T (con el resultado primario simulado) y sube2_T (d_T > d_{T-2}).
    """
    coefs, gf, gv, gd, S = par["coefs"], par["gamma_fed"], par["gamma_vix"], par["gamma_d"], par["S"]
    phi_v, phi_f = par["phi"]["vix"], par["phi"]["fed"]
    p, k, _ = coefs.shape
    N = shocks.shape[0]
    u = shocks @ S.T
    y = np.zeros((N, TRIM + p, k))
    q = gf.shape[1]
    dfed = np.zeros((N, TRIM))
    fed_esc = np.cumsum(fed_path)
    base = senda_base(esc, d0, alfa, a_fmi, dpb, sf_cero)
    d = np.zeros((N, len(ANIOS) + 1))
    d[:, 0] = d0
    x = np.zeros(N)
    x_pes = np.zeros(N)
    d_dev = np.zeros(N)
    v_dev = np.zeros(N)
    f_dev = np.zeros(N)
    nivel = np.zeros(N)       # desvio del logaritmo del PIB (puntos porcentuales)
    prom_ant = np.zeros(N)    # promedio anual del desvio del nivel del anio anterior
    niveles: list[np.ndarray] = []
    out: dict[str, np.ndarray] = {}
    for t in range(TRIM):
        v_dev = phi_v * v_dev + ext[:, t, 0]
        f_nuevo = phi_f * f_dev + ext[:, t, 1]
        dfed[:, t] = (f_nuevo - f_dev) + fed_path[t]
        f_dev = f_nuevo
        din = sum(y[:, p + t - 1 - i] @ coefs[i].T for i in range(p))
        fed_t = sum(np.outer(dfed[:, t - j], gf[:, j]) for j in range(q) if t - j >= 0)
        y[:, p + t] = din + fed_t + np.outer(v_dev, gv) + np.outer(d_dev, gd) + u[:, t]
        nivel = nivel + y[:, p + t, 1]
        niveles.append(nivel)
        if (t + 1) % 4:
            continue
        a = (t + 1) // 4
        yy = y[:, p + t - 3: p + t + 1]
        fila = esc.iloc[a - 1]
        prom = np.mean(niveles[-4:], axis=0)
        g = fila.g / 100 + (prom - prom_ant) / 100
        prom_ant = prom
        pb_base = fila.pb + dpb
        pb = pb_base + yy[:, :, 0].mean(axis=1)
        e = (yy[:, -1, 3] - y[:, p + t - 4, 3]) / tcrm0
        x = (1 - LAM) * x + LAM * (yy[:, :, 2].mean(axis=1) / 1e4 + (f_dev + fed_esc[t]) / 1e2)
        if dom:
            x_pes = (1 - LAM) * x_pes + LAM * yy[:, :, 2].mean(axis=1) / 1e4
        M = (1 + fila.i / 100 + (1 - alfa) * x + alfa * x_pes) * (1 + (1 - alfa) * e) / ((1 + fila.pi / 100) * (1 + g))
        sf, ri = flujos_escalados(fila, d[:, a - 1], alfa, a_fmi)
        sf = 0.0 * sf if sf_cero else sf
        d[:, a] = d[:, a - 1] * M - pb + sf + ri
        d_dev = d[:, a] - base[a]  # desvio acumulado respecto de la senda base
        anio = ANIOS[a - 1]
        if anio in METRICA:
            pb_estab = d[:, a - 1] * (M - 1) + sf + ri
            out[f"no_est_{anio}"] = pb_base < pb_estab
            out[f"no_est_sim_{anio}"] = pb < pb_estab
            out[f"sube2_{anio}"] = d[:, a] > d[:, a - 2]
    out["d"] = d
    return out


# ---------------------------------------------------------------------------- variante FMI
def drivers_historicos() -> pd.DataFrame:
    """Impulsores anuales de la deuda (%), como en el abanico del FMI, en los anios de la muestra:
    g: crecimiento real; r: tasa real efectiva (intereses pagados del SPN sobre deuda bruta del
    Tesoro del anio anterior, deflactada por el deflactor del PIB); z: depreciacion real (TCRM del
    cuarto trimestre); pb: resultado primario del SPN (% PIB, suma de cuatro trimestres), con la
    misma definicion que la especificacion."""
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
    col_pb = "pb_pib" if f24.columna_pb(DEUDA) == "pb_pib_trim" else "pb_pib_sin_rentas"
    pb = pd.read_csv(DATOS / "procesados" / "resultado_primario_1996_2025.csv", index_col=0, parse_dates=True)[col_pb]
    pb = pb[pb.index.quarter == 4]
    pb.index = pb.index.year
    infl = (nom_a / real_a).pct_change()
    i_ef = intereses / deuda_ars.shift(1)
    inicio = pd.Timestamp(f24.DESDE).year + 1 if f24.DESDE else 1997
    dr = pd.DataFrame({"g": 100 * real_a.pct_change(), "r": 100 * ((1 + i_ef) / (1 + infl) - 1),
                       "z": 100 * tcrm.pct_change(), "pb": pb}).loc[inicio:2025]
    if dr.isna().any().any():
        raise ValueError(f"Faltan impulsores historicos:\n{dr[dr.isna().any(axis=1)]}")
    return dr


def simular_fmi(dr: pd.DataFrame, esc: pd.DataFrame, d0: float, alfa: float, a_fmi: float, N: int,
                rng) -> dict[str, np.ndarray]:
    """Abanico con shocks a la manera del FMI (2021, anexo VI): desvios de la media historica,
    remuestreados como vectores en bloques de dos anios consecutivos y sumados al escenario base.
    Misma identidad y misma metrica que simular()."""
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
        sf, ri = flujos_escalados(fila, d[:, a - 1], alfa, a_fmi)
        d[:, a] = d[:, a - 1] * M - (fila.pb + s[:, a - 1, 3]) + sf + ri
        if ANIOS[a - 1] in METRICA:
            out[f"no_est_{ANIOS[a - 1]}"] = fila.pb < d[:, a - 1] * (M - 1) + sf + ri
    out["d"] = d
    return out


# ---------------------------------------------------------------------------- parametros
def impacto(u: np.ndarray) -> np.ndarray:
    """Matriz S (u = S eps) segun la identificacion elegida en IDENT."""
    if IDENT == "cholesky_fiscal_primero":
        return np.linalg.cholesky(np.cov(u, rowvar=False))
    if IDENT == "cholesky_fiscal_ultimo":
        # Orden crecimiento, TCRM, EMBI+, resultado primario; filas y columnas vuelven al orden
        # de ENDOG (pb, crec, EMBI, TCRM) para que los bloques sigan valiendo.
        orden = [1, 3, 2, 0]
        L = np.linalg.cholesky(np.cov(u[:, orden], rowvar=False))
        S = np.zeros_like(L)
        S[np.ix_(orden, orden)] = L
        return S
    return f24.identificar(u)


def raiz_maxima(coefs: np.ndarray) -> float:
    """Modulo maximo de los autovalores de la matriz companera."""
    p, k, _ = coefs.shape
    comp = np.zeros((k * p, k * p))
    comp[:k] = np.hstack(list(coefs))
    comp[k:, :-k] = np.eye(k * (p - 1))
    return float(np.max(np.abs(np.linalg.eigvals(comp))))


def estable(coefs: np.ndarray) -> bool:
    return raiz_maxima(coefs) < 1


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


def parametros(res, X_cols: list[str], phi: dict, coefs: np.ndarray | None = None) -> dict:
    """Objetos que usa la simulacion; coefs permite pasar coeficientes corregidos por sesgo."""
    fed_cols = [c for c in X_cols if c.startswith("dFED")]
    gd = res.params.loc["deuda_l1"].values
    return {"coefs": res.coefs if coefs is None else coefs, "gamma_fed": res.params.loc[fed_cols].values.T,
            "gamma_vix": res.params.loc["VIX"].values, "gamma_d": 0.0 * gd if SIN_RETRO else gd,
            "S": impacto(res.resid.values), "phi": phi}


def generador(Y: pd.DataFrame, X: pd.DataFrame, deuda: pd.Series, p: int):
    """Proceso generador del bootstrap: VAR auxiliar con la deuda como quinta variable, para que
    la deuda se regenere en cada replica (diseno recursivo). Los residuos centrados se remuestrean
    en bloques moviles de BLOQUE_INF trimestres (Bruggemann, Jentsch y Trenkler, 2016), lo que
    conserva la autocorrelacion y la heterocedasticidad condicional remanentes.
    Devuelve el ajuste auxiliar, las exogenas sin la deuda y una funcion muestra(rng, A)."""
    Xa = X.drop(columns="deuda_l1")
    Z = pd.concat([Y, deuda.reindex(Y.index).rename("deuda")], axis=1)
    aux = f24.VAR(Z, exog=Xa).fit(maxlags=p, ic=None, trend="c")
    nu = aux.params.loc["const"].values
    G = aux.params.loc[Xa.columns].values.T
    U = aux.resid.values - aux.resid.values.mean(axis=0)
    Xav = Xa.values

    def muestra(rng, A: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        ub = U[indices_bloques(rng, len(U), 1, len(U), BLOQUE_INF)[0]]
        z = Z.values.copy()
        for t in range(p, len(z)):
            z[t] = nu + sum(A[i] @ z[t - 1 - i] for i in range(p)) + G @ Xav[t] + ub[t - p]
        Yb = pd.DataFrame(z[:, :4], index=Y.index, columns=Y.columns)
        Xb = X.copy()
        Xb["deuda_l1"] = np.r_[X["deuda_l1"].iloc[0], z[:-1, 4]]
        return Yb, Xb, pd.DataFrame(z, index=Z.index, columns=Z.columns)
    return aux, Xa, muestra


def replicas(Y: pd.DataFrame, X: pd.DataFrame, deuda: pd.Series, p: int, B: int, B1: int, phi: dict,
             rng) -> tuple[dict, list[dict], dict]:
    """Parametros centrales y B replicas. Sin --kilian: minimos cuadrados y replicas generadas con
    el proceso estimado. Con --kilian: bootstrap-after-bootstrap de Kilian (1998), en el que el
    central, el proceso generador y cada replica se corrigen por el sesgo medido en B1 muestras."""
    base = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    aux, Xa, muestra = generador(Y, X, deuda, p)
    cols = list(X.columns)
    sesgo, A_gen, coefs_c, delta_c = None, aux.coefs, base.coefs, 1.0
    if KILIAN:
        est_m, est_a = [], []
        while len(est_m) < B1:
            Yb, Xb, Zb = muestra(rng, aux.coefs)
            try:
                est_m.append(f24.VAR(Yb, exog=Xb).fit(maxlags=p, ic=None, trend="c").coefs)
                est_a.append(f24.VAR(Zb, exog=Xa).fit(maxlags=p, ic=None, trend="c").coefs)
            except (np.linalg.LinAlgError, ValueError):
                continue
        sesgo = np.mean(est_m, axis=0) - base.coefs
        coefs_c, delta_c = corregir_sesgo(base.coefs, sesgo)
        A_gen, _ = corregir_sesgo(aux.coefs, np.mean(est_a, axis=0) - aux.coefs)
    central = parametros(base, cols, phi, coefs_c)
    out, fallidas = [], 0
    while len(out) < B:
        Yb, Xb, _ = muestra(rng, A_gen)
        try:
            rb = f24.VAR(Yb, exog=Xb).fit(maxlags=p, ic=None, trend="c")
        except (np.linalg.LinAlgError, ValueError):
            fallidas += 1
            continue
        c = rb.coefs
        if KILIAN:
            c, _ = corregir_sesgo(rb.coefs, sesgo)
        if not estable(c):
            fallidas += 1
            continue
        out.append(parametros(rb, cols, phi, c))
    meta = {"kilian": KILIAN, "delta_central": delta_c, "raiz_max_estimada": raiz_maxima(base.coefs),
            "raiz_max_central": raiz_maxima(coefs_c),
            "raiz_max_mediana_replicas": float(np.median([raiz_maxima(r["coefs"]) for r in out])),
            "replicas_fallidas_o_inestables": fallidas}
    return central, out, meta


# ---------------------------------------------------------------------------- medidas
BLOQUES = {"fiscal": [0], "actividad": [1], "cambiario_y_riesgo": [2, 3]}


def medidas(par: dict, shocks: np.ndarray, ext: np.ndarray, fed: dict[str, np.ndarray], esc: pd.DataFrame,
            d0: float, alfa: float, a_fmi: float, tcrm0: float, dom: bool, sf_cero: bool) -> dict[str, float]:
    """Todas las medidas de H1a, H1b y H2 para un juego de parametros."""
    f: dict[str, float] = {}
    sim = lambda sh, ex, path: simular(par, sh, ex, path, esc, d0, alfa, a_fmi, tcrm0, dom, sf_cero=sf_cero)
    sims = {nom: sim(shocks, ext, path) for nom, path in fed.items()}
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
    # Varianza de la deuda en 2035 por bloque: cada bloque simulado solo (el externo agrupa las
    # innovaciones del VIX y de la tasa de la FED).
    var = {}
    cero_sh, cero_ex = np.zeros_like(shocks), np.zeros_like(ext)
    for nombre, cols in BLOQUES.items():
        sh = cero_sh.copy()
        sh[:, :, cols] = shocks[:, :, cols]
        var[nombre] = float(sim(sh, cero_ex, fed["base"])["d"][:, -1].var())
    var["externo"] = float(sim(cero_sh, ext, fed["base"])["d"][:, -1].var())
    tot = sum(var.values())
    for nombre, v in var.items():
        f[f"vshare_{nombre}"] = 100 * v / tot
    f["var_total_2035"] = float(b["d"][:, -1].var())
    f["var_suma_bloques_2035"] = tot
    f["h1a_nofiscal_menos_fiscal"] = 100 - 2 * f["vshare_fiscal"]
    return f


def resumen_hall(cen: dict, res: pd.DataFrame) -> pd.DataFrame:
    """Estimacion central e intervalo de 90% de Hall, acotado al rango posible de cada medida."""
    h = f24.intervalo_hall(pd.Series(cen), res.drop(columns="replica").reindex(columns=list(cen)))
    return acotar(h).rename(columns={"inf": "p05", "sup": "p95"})


def acotar(h: pd.DataFrame, cols: tuple[str, str] = ("inf", "sup")) -> pd.DataFrame:
    """El intervalo de Hall puede salir del rango posible de la medida; se acota: probabilidades a
    [0, 1], participaciones en la varianza a [0, 100] y su diferencia a [-100, 100]."""
    h = h.copy()
    cols = list(cols)
    es_p = h.index.str.contains("_p_noest_|_p_sube2_") & ~h.index.str.startswith("dif_")
    h.loc[es_p, cols] = h.loc[es_p, cols].clip(0, 1)
    es_v = h.index.str.startswith("vshare_")
    h.loc[es_v, cols] = h.loc[es_v, cols].clip(0, 100)
    es_d = h.index.str.startswith("h1a_")
    h.loc[es_d, cols] = h.loc[es_d, cols].clip(-100, 100)
    return h


DEUDA = "federal"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deuda", default="federal", choices=list(f24.SERIES_DEUDA))
    ap.add_argument("--B", type=int, default=200)
    ap.add_argument("--B1", type=int, default=100, help="replicas para medir el sesgo (--kilian)")
    ap.add_argument("--N", type=int, default=1000)
    ap.add_argument("--N-central", type=int, default=20000)
    ap.add_argument("--kilian", action="store_true", help="parametros corregidos por sesgo (robustez)")
    ap.add_argument("--canal-domestico", action="store_true")
    ap.add_argument("--shocks", choices=["svarx", "fmi"], default="svarx")
    ap.add_argument("--sin-retroalimentacion", action="store_true")
    ap.add_argument("--identificacion", choices=["bp", "cholesky_fiscal_primero", "cholesky_fiscal_ultimo"], default="bp")
    ap.add_argument("--escenario", choices=list(ESCENARIOS), default="cr26105")
    ap.add_argument("--sin-default", action="store_true", help="excluye 2001T4-2005T3 del remuestreo de shocks")
    ap.add_argument("--sf-cero", action="store_true", help="ajuste stock-flujo del FMI en cero")
    ap.add_argument("--pb-alternativa", action="store_true", help="la otra definicion del resultado primario")
    ap.add_argument("--sin-quiebres", action="store_true")
    ap.add_argument("--desde", default=None, help="primer trimestre de los datos (robustez)")
    ap.add_argument("--lam", type=float, default=None)
    ap.add_argument("--alpha-y", type=float, default=None)
    ap.add_argument("--d0", type=float, default=None)
    ap.add_argument("--p", type=int, default=None, help="orden del VAR (robustez); por defecto, la regla de fase24")
    ap.add_argument("--suficiencia", action="store_true", help="contraste de suficiencia del superavit (H1a)")
    a = ap.parse_args()
    global ESC, LAM, IDENT, SIN_RETRO, KILIAN, DEUDA
    ESC, IDENT, SIN_RETRO, KILIAN, DEUDA = a.escenario, a.identificacion, a.sin_retroalimentacion, a.kilian, a.deuda
    LAM = a.lam if a.lam is not None else velocidad_refinanciacion(ESC)
    if a.alpha_y is not None:
        f24.ALPHA_Y = a.alpha_y
    if a.pb_alternativa:
        f24.PB_COLUMNA = "pb_pib_trim_sin_rentas" if a.deuda == "federal" else "pb_pib_trim"
    if a.desde:
        f24.DESDE = a.desde
    f24.SIN_QUIEBRES = a.sin_quiebres
    _, p_mp, p_lp, _ = ESCENARIOS[ESC]
    rng_est = np.random.default_rng(SEMILLA)      # bootstrap de parametros
    rng_c = np.random.default_rng(SEMILLA + 1)    # trayectorias de la estimacion central
    rng_r = np.random.default_rng(SEMILLA + 2)    # trayectorias de las replicas
    TABLAS.mkdir(parents=True, exist_ok=True)
    esc = escenario_fmi()
    d0, alfa, a_fmi, tcrm0 = condiciones_iniciales(a.deuda, esc)
    desvio_fmi = verificar_escenario(esc, a_fmi)
    if a.d0 is not None:
        d0 = a.d0
    etiquetas = [a.deuda, "dom" if a.canal_domestico else "", {"bp": "", "cholesky_fiscal_primero": "chol",
                 "cholesky_fiscal_ultimo": "chol_ultimo"}[IDENT], "sin_retro" if SIN_RETRO else "",
                 "" if ESC == "cr26105" else ESC, "sin_default" if a.sin_default else "", "sf0" if a.sf_cero else "",
                 "pb_alt" if a.pb_alternativa else "", f"desde{a.desde[:4]}" if a.desde else "",
                 "sin_quiebres" if a.sin_quiebres else "", "kilian" if KILIAN else "",
                 f"lam{a.lam:g}" if a.lam is not None else "", f"alfa{a.alpha_y:g}" if a.alpha_y is not None else "",
                 f"d0_{a.d0:g}" if a.d0 is not None else "", f"p{a.p}" if a.p is not None else ""]
    suf = "_".join(e for e in etiquetas if e)

    if a.shocks == "fmi":
        dr = drivers_historicos()
        dr.to_csv(TABLAS / f"fase25_{suf}_impulsores_historicos.csv")
        s = simular_fmi(dr, esc, d0, alfa, a_fmi, a.N_central, rng_c)
        i31 = ANIOS.index(2031) + 1
        out = pd.Series({**{f"p_noest_{T}": s[f"no_est_{T}"].mean() for T in METRICA},
                         "d2035_media": s["d"][:, -1].mean(),
                         "ancho_p5_p95_2031": np.subtract(*np.percentile(s["d"][:, i31], [95, 5]))})
        pct = np.percentile(s["d"], [5, 10, 25, 50, 75, 90, 95], axis=0)
        pd.DataFrame(pct.T, index=[2025] + ANIOS, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]
                     ).rename_axis("anio").to_csv(TABLAS / f"fase25_{suf}_fmi_fanchart.csv")
        out.to_csv(TABLAS / f"fase25_{suf}_fmi_resumen.csv", header=["valor"])
        print(f"shocks=fmi {suf} d0={d0:.1f} anios {dr.index.min()}-{dr.index.max()} N={a.N_central}")
        print(out.round(4).to_string())
        return

    Y, X, _ = f24.cargar_datos(a.deuda, 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    if a.p is not None:
        p = a.p
    Y, X = f24.recortar(Y, X, p)
    archivo, col = f24.SERIES_DEUDA[a.deuda]
    deuda = pd.read_csv(DATOS / "procesados" / archivo, parse_dates=["Date"], index_col="Date")[col]
    resid = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c").resid
    phi, innov = procesos_externos(resid.index)
    central, reps, meta = replicas(Y, X, deuda, p, a.B, a.B1, phi, rng_est)
    eps = pd.DataFrame(np.linalg.solve(central["S"], resid.values.T).T, index=resid.index)
    hist = pd.concat([eps, innov], axis=1).dropna()
    if a.sin_default:
        hist = hist[(hist.index < DEFAULT[0]) | (hist.index > DEFAULT[1])]
    H = hist.values
    k = eps.shape[1]

    def sortear(rng, N: int) -> tuple[np.ndarray, np.ndarray]:
        z = H[indices_bloques(rng, len(H), N, TRIM, BLOQUE_SIM)]
        return z[:, :, :k], z[:, :, k:]

    sd_fed = float(X["dFED_l0"].iloc[p:].std(ddof=1))
    ffr = pd.read_csv(DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv", parse_dates=["Date"], index_col="Date")
    ciclo = ffr["fedfunds"].diff().loc["2022-01-01":"2025-12-31"].values
    fed = {"base": np.zeros(TRIM), "fed_1de": np.r_[sd_fed, np.zeros(TRIM - 1)],
           "fed_2022_2025": np.r_[ciclo, np.zeros(TRIM - len(ciclo))]}

    # Estimacion central
    shocks_c, ext_c = sortear(rng_c, a.N_central)
    cen = medidas(central, shocks_c, ext_c, fed, esc, d0, alfa, a_fmi, tcrm0, a.canal_domestico, a.sf_cero)
    sb = simular(central, shocks_c, ext_c, fed["base"], esc, d0, alfa, a_fmi, tcrm0, a.canal_domestico, sf_cero=a.sf_cero)
    pct = np.percentile(sb["d"], [5, 10, 25, 50, 75, 90, 95], axis=0)
    pd.DataFrame(pct.T, index=[2025] + ANIOS, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]
                 ).rename_axis("anio").to_csv(TABLAS / f"fase25_{suf}_fanchart.csv")
    # Canal directo de la FED: misma estimacion central sin respuesta de las variables domesticas.
    sin_ind = dict(central, gamma_fed=np.zeros_like(central["gamma_fed"]))
    sd = simular(sin_ind, shocks_c, ext_c, fed["fed_2022_2025"], esc, d0, alfa, a_fmi, tcrm0, a.canal_domestico, sf_cero=a.sf_cero)
    sd0 = simular(sin_ind, shocks_c, ext_c, fed["base"], esc, d0, alfa, a_fmi, tcrm0, a.canal_domestico, sf_cero=a.sf_cero)
    cen["dif_fed_2022_2025_d2035_solo_costo_directo"] = float(sd["d"][:, -1].mean() - sd0["d"][:, -1].mean())
    senda = senda_base(esc, d0, alfa, a_fmi, sf_cero=a.sf_cero)
    cen["senda_base_d2031"] = float(senda[ANIOS.index(2031) + 1])
    cen["senda_base_d2035"] = float(senda[-1])

    if a.suficiencia:
        filas = []
        for dpb in np.arange(0, 8.01, 0.25):
            s = simular(central, shocks_c, ext_c, fed["base"], esc, d0, alfa, a_fmi, tcrm0, a.canal_domestico,
                        dpb=dpb, sf_cero=a.sf_cero)
            filas.append({"dpb": dpb, "pb_2026": float(esc.loc[2026, "pb"] + dpb),
                          "pb_2031": float(esc.loc[2031, "pb"] + dpb),
                          "p_noest_2031": float(s["no_est_2031"].mean()), "p_noest_2035": float(s["no_est_2035"].mean())})
        pd.DataFrame(filas).to_csv(TABLAS / f"fase25_{suf}_suficiencia.csv", index=False)

    filas = []
    for r_i, par in enumerate(reps):
        shocks, ext = sortear(rng_r, a.N)
        filas.append({"replica": r_i, **medidas(par, shocks, ext, fed, esc, d0, alfa, a_fmi, tcrm0,
                                                  a.canal_domestico, a.sf_cero)})
    res = pd.DataFrame(filas)
    res.to_csv(TABLAS / f"fase25_{suf}_replicas.csv", index=False)
    resumen = resumen_hall(cen, res)
    for T in METRICA:
        pr = cen[f"base_p_noest_{T}"]
        resumen.loc[f"error_mc_p_noest_{T}", "estimacion"] = np.sqrt(pr * (1 - pr) / a.N_central)
    resumen.to_csv(TABLAS / f"fase25_{suf}_resumen.csv")
    meta.update({"escenario": ESC, "deuda": a.deuda, "lam": LAM, "alpha_y": f24.ALPHA_Y, "d0": d0,
                 "alfa_pesos": alfa, "alfa_pesos_fmi": a_fmi, "p": p, "pb": f24.columna_pb(a.deuda),
                 "desde": f24.DESDE, "sin_quiebres": f24.SIN_QUIEBRES, "B": a.B, "N": a.N,
                 "N_central": a.N_central, "bloque_sim": BLOQUE_SIM, "bloque_inf": BLOQUE_INF,
                 "phi_vix": phi["vix"], "phi_fed": phi["fed"], "sd_dfed": sd_fed,
                 "desvio_max_senda_fmi": desvio_fmi, "prob_fmi_mediano_plazo": p_mp, "prob_fmi_2035": p_lp,
                 "trimestres_historicos": len(H), "muestra": [str(Y.index[p].date()), str(Y.index[-1].date())]})
    (TABLAS / f"fase25_{suf}_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"{suf}: {json.dumps(meta)}")
    print(resumen.round(4).to_string())


if __name__ == "__main__":
    main()
