"""
fase24_svarx_1996_2025.py
=========================
SVARX trimestral (Capitulo 4 de la tesis, metodologia.md). Datos desde 1999T1 (todas las series
de fuentes publicadas; el EMBI+ anterior a 1999 se reconstruia con valores transcriptos y se deja
afuera); muestra efectiva comun 2000T3-2025T4.

Forma reducida (Y_t endogeno, X_t exogeno):
    Y_t = nu + sum_{i=1..p} A_i Y_{t-i} + Gamma X_t + u_t
    Y_t = (pb_t, crec_t, EMBI_t, TCRM_t)
    X_t = (dFED_t, ..., dFED_{t-q}, VIX_t, Q1_t, Q2_t, Q3_t, D^(k)_t, d_{t-1})
- crec_t = 100 * dln(PIB_real_t): crecimiento trimestral. El PIB real de la base no
  esta desestacionalizado, por eso X incluye dummies estacionales (Lutkepohl, 2005).
- d_{t-1}: deuda rezagada (% PIB): la federal bruta (perimetro del FMI) en la especificacion
  principal; la consolidada con el BCRA como extension. Siguiendo a Favero y Giavazzi
  (2007), la deuda entra rezagada en todas las ecuaciones y en la simulacion evoluciona
  por la identidad de acumulacion (fase25). El coeficiente de d_{t-1} en la ecuacion de
  pb es la reaccion fiscal de Bohn (1998) que contrasta H1a.
- dFED: variacion trimestral de la tasa de politica (FEDFUNDS; Wu-Xia en el piso cero). En el
  trimestre de salida del piso (2022T1) la variacion se calcula con la tasa efectiva en los dos
  trimestres, para no confundir el cambio de serie con un cambio de politica.
- D^(k): dummies escalon en los quiebres de Bai-Perron de la serie de deuda.

Identificacion (u_t = S eps_t, E[eps eps'] = I):
    eps_pb  ~ e_pb = u_pb - alpha_y * u_crec      (Blanchard y Perotti, 2002; alpha_y = 0,25,
                                                    Girouard y Andre, 2005)
    eps_y   ~ residuo de u_crec sobre e_pb         (el producto responde al shock fiscal)
    bloque  ~ residuos de (u_EMBI, u_TCRM) sobre (e_pb, e_y), ortonormalizados; solo se
              reportan magnitudes de bloque, invariantes al orden interno
              (Christiano, Eichenbaum y Evans, 1999).

Rezagos: el criterio de Schwarz (SIC), que Ivanov y Kilian (2005) recomiendan para datos
trimestrales con menos de 120 observaciones, y, si sus residuos tienen autocorrelacion, el
menor orden mayor que pasa la prueba de Portmanteau (Lutkepohl, 2005, cap. 4); siempre estable.
Inferencia: bootstrap de bloques moviles sobre los residuos, de diseno recursivo (Bruggemann,
Jentsch y Trenkler, 2016), valido con autocorrelacion residual remanente y heterocedasticidad
condicional; intervalos de percentil de Hall (1992), que corrigen el sesgo de la distribucion
bootstrap. Semilla fija. Las replicas fallidas se cuentan, no se rellenan.

Uso:
    python codigo/modelos/fase24_svarx_1996_2025.py --deuda federal|consolidada [--n-boot 1000]
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import het_arch
from statsmodels.tsa.api import VAR

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bai_perron import bai_perron_breaks  # noqa: E402

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*frequency.*")

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
DATOS = BASE / "datos"
TABLAS = BASE / "resultados" / "tablas"

ALPHA_Y: float = 0.25
SEMILLA: int = 20261011
# Orden maximo considerado. Todas las especificaciones (cualquier p, cualquier serie de deuda)
# se estiman sobre la MISMA muestra efectiva: las primeras PMAX observaciones se reservan como
# condiciones iniciales (Lutkepohl, 2005, sec. 4.3: los criterios de informacion se comparan
# sobre un periodo comun). Con datos desde 1999T1 la muestra efectiva es 2000T3-2025T4.
PMAX: int = 6
ENDOG: list[str] = ["pb_pib", "crec", "EMBI", "TCRM"]
SERIES_DEUDA: dict[str, tuple[str, str]] = {
    # Principal: deuda bruta del gobierno federal (Administracion Central), el perimetro del
    # analisis de sostenibilidad del FMI (2026, anexo II): permite comparar con su probabilidad.
    "federal": ("deuda_consolidada_neta_nominal_1996_2025.csv", "bruta_federal_pib"),
    # Extension: consolidacion con el BCRA (FMI, 2021, anexo II), Letras a valor nominal.
    "consolidada": ("deuda_consolidada_neta_nominal_1996_2025.csv", "deuda_consolidada_neta_nominal_pib"),
    # Principal: consolidacion con el BCRA (FMI, 2021, anexo II) con las Letras
    # Intransferibles a valor nominal, variante "piso" (informe_resultado_primario_y_valuacion.md).
    "neta": ("deuda_consolidada_neta_nominal_1996_2025.csv", "deuda_consolidada_neta_nominal_piso_pib"),
    "neta_libros": ("deuda_consolidada_neta_1996_2025.csv", "deuda_consolidada_neta_pib"),
    "bruta": ("deuda_consolidada_1996_2025.csv", "deuda_consolidada_pib"),
    # Solo la deuda bruta del Tesoro (Administracion Central), sin el BCRA: contrasta el argumento
    # de la vacancia (seccion 2.9) de que omitir al BCRA cambia la sensibilidad de la deuda.
    "tesoro": ("deuda_consolidada_neta_nominal_1996_2025.csv", "bruta_federal_pib"),
}
# Opciones de robustez de la estimacion (se fijan desde fase25 antes de cargar los datos):
#   PB_COLUMNA: None elige la definicion coherente con el perimetro de la deuda:
#               - federal: "pb_pib_trim" (con rentas de la propiedad). Es la definicion del FMI
#                 para el gobierno federal (2025: 1,4% en el FMI y 1,38% en esta serie): las
#                 utilidades que el BCRA transfiere al Tesoro son ingreso del Tesoro.
#               - consolidada y demas: "pb_pib_trim_sin_rentas", porque en el perimetro
#                 consolidado las utilidades del BCRA son un flujo interno.
#               Un valor explicito fuerza la otra definicion (robustez).
#   DESDE: primer trimestre de los datos; "1999-01-01" (principal) o "2004-01-01" (robustez).
#   SIN_QUIEBRES: True quita las variables binarias de quiebre (robustez).
PB_COLUMNA: str | None = None
DESDE: str | None = "1999-01-01"
SIN_QUIEBRES: bool = False


def dfed_empalmado(fed: pd.DataFrame) -> pd.Series:
    """Variacion trimestral de la tasa de politica. En el trimestre en que la serie pasa de la
    tasa sombra a la efectiva, la variacion se calcula con la efectiva en ambos trimestres."""
    d = fed["tasa_politica_fed"].diff()
    cambio = (fed["fuente_flag"] != "shadow_wu_xia") & (fed["fuente_flag"].shift(1) == "shadow_wu_xia")
    d[cambio] = fed["fedfunds"].diff()[cambio]
    return d


def columna_pb(tipo_deuda: str) -> str:
    """Definicion del resultado primario coherente con el perimetro (ver PB_COLUMNA)."""
    if PB_COLUMNA is not None:
        return PB_COLUMNA
    return "pb_pib_trim" if tipo_deuda == "federal" else "pb_pib_trim_sin_rentas"


def cargar_datos(tipo_deuda: str, rezagos_fed: int) -> tuple[pd.DataFrame, pd.DataFrame, list[pd.Timestamp]]:
    """Arma Y y X alineadas por trimestre, sin faltantes."""
    leer = lambda f: pd.read_csv(DATOS / f, parse_dates=["Date"], index_col="Date")
    base = leer("dataset_consolidado_1996_2025.csv")
    archivo, col = SERIES_DEUDA[tipo_deuda]
    deuda = leer(f"procesados/{archivo}")[col]
    dfed = dfed_empalmado(leer("procesados/tasa_fed_trimestral_1996_2025.csv"))
    vix = leer("procesados/instrumentos_1996_2025.csv")["VIX"]  # ^VIX completo desde 1996

    # Resultado primario SPN base caja (MECON, datos.gob.ar dataset 379): flujo trimestral
    # anualizado (4 x trimestre / PIB nominal de 4 trimestres). Se usa el flujo trimestral y
    # no la suma movil de 4 trimestres porque esta induce autocorrelacion MA(3) artificial;
    # la estacionalidad la absorben las dummies Q1-Q3.
    pb = pd.read_csv(DATOS / "procesados" / "resultado_primario_1996_2025.csv",
                     index_col=0, parse_dates=True)[columna_pb(tipo_deuda)]
    # PIB real: INDEC base 1993 empalmado a base 2004 para 1996-2003; base 2004 desde 2004.
    pib_pre = leer("procesados/pib_real_empalme_indec_1996_2003.csv")["PIB_real"]
    pib = pd.concat([pib_pre, base["PIB_real"][base.index > pib_pre.index.max()]])
    Y = pd.DataFrame({
        "pb_pib": pb,
        "crec": 100.0 * np.log(pib).diff(),
        "EMBI": base["EMBI"],
        "TCRM": base["TCRM"],
    })
    X = pd.concat([dfed.shift(k).rename(f"dFED_l{k}") for k in range(rezagos_fed + 1)], axis=1)
    X["VIX"] = vix
    for q in (1, 2, 3):
        X[f"Q{q}"] = (X.index.quarter == q).astype(float)
    quiebres = [] if SIN_QUIEBRES else bai_perron_breaks(deuda.dropna())["fechas_quiebre"]
    for k, fecha in enumerate(quiebres, start=1):
        X[f"D{k}_{fecha.date()}"] = (X.index > fecha).astype(float)
    X["deuda_l1"] = deuda.shift(1)

    datos = Y.join(X, how="inner").dropna()
    if DESDE is not None:
        datos = datos[datos.index >= pd.Timestamp(DESDE)]
        constantes = [c for c in X.columns if c.startswith("D") and datos[c].nunique() < 2]
        datos = datos.drop(columns=constantes)
        quiebres = [q for q in quiebres if q >= pd.Timestamp(DESDE)]
        cols_x = [c for c in X.columns if c not in constantes]
        return datos[ENDOG], datos[cols_x], list(quiebres)
    return datos[ENDOG], datos[X.columns], list(quiebres)


def identificar(u: np.ndarray) -> np.ndarray:
    """Matriz S (u = S eps) segun el esquema del modulo; u es T x 4 en el orden de ENDOG."""
    def resid(y: np.ndarray, Z: np.ndarray) -> np.ndarray:
        return y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]

    e_pb = u[:, 0] - ALPHA_Y * u[:, 1]
    e_y = resid(u[:, 1], e_pb[:, None])
    v = resid(u[:, 2:4], np.column_stack([e_pb, e_y]))
    w = v @ np.linalg.inv(np.linalg.cholesky(np.cov(v, rowvar=False)).T)
    eps = np.column_stack([e_pb, e_y, w])
    eps = (eps - eps.mean(axis=0)) / eps.std(axis=0, ddof=1)
    return np.linalg.lstsq(eps, u, rcond=None)[0].T


def recortar(Y: pd.DataFrame, X: pd.DataFrame, p: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Deja PMAX - p observaciones fuera para que el VAR(p) use la muestra efectiva comun
    (t = PMAX+1, ..., T), igual para todo p."""
    return Y.iloc[PMAX - p:], X.iloc[PMAX - p:]


def elegir_rezagos(Y: pd.DataFrame, X: pd.DataFrame, pmax: int = PMAX) -> tuple[int, int, pd.DataFrame]:
    """Regla de seleccion del orden p:
    1. p_SIC = orden que minimiza el criterio de Schwarz entre los ordenes estables. Ivanov y
       Kilian (2005) muestran que, con datos trimestrales y menos de 120 observaciones, es el
       criterio que estima con mas precision las respuestas al impulso.
    2. Si los residuos del VAR(p_SIC) rechazan la ausencia de autocorrelacion (Portmanteau con
       12 rezagos, 5%), p es el menor orden mayor que p_SIC, estable, que no la rechaza: el
       remuestreo de shocks supone residuos sin autocorrelacion (Lutkepohl, 2005, sec. 4.4).
    La estabilidad (raices del polinomio caracteristico fuera del circulo unitario) es condicion
    para la representacion de medias moviles y la simulacion de largo plazo.
    Devuelve (p, p_AIC sin restriccion, tabla de diagnosticos por orden)."""
    filas = []
    for p in range(1, pmax + 1):
        Yp, Xp = recortar(Y, X, p)
        r = VAR(Yp, exog=Xp).fit(maxlags=p, ic=None, trend="c")
        filas.append({"p": p, "n_efectivo": int(r.nobs), "inicio": str(Yp.index[p].date()),
                      **{"aic": r.aic, "bic": r.bic, "hqic": r.hqic,
                      "modulo_raiz_max": float(np.max(1.0 / np.abs(r.roots))),
                      "estable": bool(r.is_stable()),
                      "portmanteau_12_p": r.test_whiteness(nlags=12).pvalue}})
    tabla = pd.DataFrame(filas)
    p_aic = int(tabla.loc[tabla["aic"].idxmin(), "p"])
    estables = tabla[tabla["estable"]]
    if estables.empty:
        raise ValueError("Ningun orden p produce un VAR estable.")
    p_sic = int(estables.loc[estables["bic"].idxmin(), "p"])
    blancos = estables[(estables["p"] >= p_sic) & (estables["portmanteau_12_p"] >= 0.05)]["p"]
    p = int(blancos.min()) if not blancos.empty else p_sic
    tabla["p_sic"] = p_sic
    return p, p_aic, tabla


def respuesta_fed(coefs: np.ndarray, gamma_fed: np.ndarray, tam: float, horizonte: int) -> np.ndarray:
    """Multiplicador dinamico de un aumento permanente de `tam` p.p. en el nivel de la tasa
    (dFED = tam en t=0). gamma_fed: k x (q+1), columnas dFED_l0..l_q."""
    p, k, _ = coefs.shape
    resp = np.zeros((horizonte + 1, k))
    for t in range(horizonte + 1):
        directo = gamma_fed[:, t] * tam if t < gamma_fed.shape[1] else np.zeros(k)
        resp[t] = directo + sum((coefs[i] @ resp[t - 1 - i] for i in range(p) if t - 1 - i >= 0), np.zeros(k))
    return resp


def multiplicador_largo_plazo(res) -> float:
    """Respuesta de largo plazo del resultado primario a la deuda en su propia ecuacion:
    rho / (1 - suma de los coeficientes de los rezagos del resultado primario)."""
    propios = sum(res.coefs[i][0, 0] for i in range(res.k_ar))
    return float(res.params.loc["deuda_l1", "pb_pib"] / (1.0 - propios))


def intervalo_hall(est: pd.Series, rep: pd.DataFrame, nivel: float = 0.90) -> pd.DataFrame:
    """Intervalo de percentil de Hall (1992): [2 est - q_sup, 2 est - q_inf]. Corrige el sesgo
    de la distribucion bootstrap respecto de la estimacion puntual."""
    a = (1 - nivel) / 2
    q = rep.quantile([a, 1 - a]).T.reindex(est.index)
    return pd.DataFrame({"estimacion": est, "inf": 2 * est - q[1 - a], "sup": 2 * est - q[a]})


def estimar(Y: pd.DataFrame, X: pd.DataFrame, p: int, tam_fed: float, horizonte: int) -> dict:
    """VARX, identificacion, reaccion fiscal (Bohn) y respuesta a la FED."""
    res = VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    fed_cols = [c for c in X.columns if c.startswith("dFED")]
    gamma_fed = res.params.loc[fed_cols].values.T
    return {
        "res": res,
        "S": identificar(res.resid.values),
        "rho": float(res.params.loc["deuda_l1", "pb_pib"]),
        "rho_lp": multiplicador_largo_plazo(res),
        "rho_p": float(res.pvalues.loc["deuda_l1", "pb_pib"]),
        "fed": respuesta_fed(res.coefs, gamma_fed, tam_fed, horizonte),
    }


def bootstrap(Y: pd.DataFrame, X: pd.DataFrame, p: int, tam_fed: float, horizonte: int,
              n_boot: int, deuda: pd.Series) -> tuple[pd.DataFrame, int]:
    """Bootstrap de bloques moviles de diseno recursivo (Bruggemann et al., 2016) en el que la
    deuda tambien se regenera (VAR auxiliar con la deuda como quinta variable). Usa el mismo
    generador que la simulacion (fase25). Devuelve las replicas y las fallidas."""
    import fase25_simulacion_dsa_svarx as f25  # import diferido: fase25 importa este modulo

    rng = np.random.default_rng(SEMILLA)
    aux, _, muestra = f25.generador(Y, X, deuda, p)
    filas, fallidas = [], 0
    while len(filas) < n_boot:
        Yb, Xb, _ = muestra(rng, aux.coefs)
        try:
            rb = estimar(Yb, Xb, p, tam_fed, horizonte)
        except (np.linalg.LinAlgError, ValueError):
            fallidas += 1
            continue
        fila = {"rho_bohn": rb["rho"], "rho_largo_plazo": rb["rho_lp"],
                **{f"deuda_a_{v}": rb["res"].params.loc["deuda_l1", v] for v in ENDOG}}
        for h in range(horizonte + 1):
            for jj, v in enumerate(ENDOG):
                fila[f"fed_{v}_h{h}"] = rb["fed"][h, jj]
        filas.append(fila)
    return pd.DataFrame(filas), fallidas


def diagnosticos(res) -> pd.DataFrame:
    """Portmanteau, normalidad multivariada, estabilidad y ARCH-LM por ecuacion."""
    filas = [
        {"prueba": "Portmanteau (12 rezagos)", "valor": res.test_whiteness(nlags=12).pvalue},
        {"prueba": "Normalidad multivariada (p-valor)", "valor": res.test_normality().pvalue},
        {"prueba": "Estable (1 = si)", "valor": float(res.is_stable())},
    ]
    filas += [{"prueba": f"ARCH-LM(4) {c} (p-valor)", "valor": het_arch(res.resid[c], nlags=4)[1]}
              for c in res.resid.columns]
    return pd.DataFrame(filas)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deuda", choices=list(SERIES_DEUDA), default="federal")
    ap.add_argument("--desde", default=None, help="primer trimestre de los datos (robustez)")
    ap.add_argument("--pb-alternativa", action="store_true", help="la otra definicion del resultado primario")
    ap.add_argument("--sin-quiebres", action="store_true")
    ap.add_argument("--rezagos-fed", type=int, default=2)
    ap.add_argument("--horizonte", type=int, default=20)
    ap.add_argument("--n-boot", type=int, default=1000)
    a = ap.parse_args()
    global DESDE, PB_COLUMNA, SIN_QUIEBRES
    if a.desde:
        DESDE = a.desde
    if a.pb_alternativa:
        PB_COLUMNA = "pb_pib_trim_sin_rentas" if a.deuda == "federal" else "pb_pib_trim"
    SIN_QUIEBRES = a.sin_quiebres

    Y, X, quiebres = cargar_datos(a.deuda, a.rezagos_fed)

    p, p_aic, tabla_p = elegir_rezagos(Y, X)
    Y, X = recortar(Y, X, p)
    tam_fed = float(X["dFED_l0"].iloc[p:].std(ddof=1))  # un desvio estandar de dFED en la muestra
    base = estimar(Y, X, p, tam_fed, a.horizonte)
    archivo, col = SERIES_DEUDA[a.deuda]
    deuda = pd.read_csv(DATOS / "procesados" / archivo, parse_dates=["Date"], index_col="Date")[col]
    boot, fallidas = bootstrap(Y, X, p, tam_fed, a.horizonte, a.n_boot, deuda)
    est = {"rho_bohn": base["rho"], "rho_largo_plazo": base["rho_lp"],
           **{f"deuda_a_{v}": base["res"].params.loc["deuda_l1", v] for v in ENDOG}}
    for h in range(a.horizonte + 1):
        for jj, v in enumerate(ENDOG):
            est[f"fed_{v}_h{h}"] = base["fed"][h, jj]
    hall = intervalo_hall(pd.Series(est), boot)
    q = hall.rename(columns={"inf": "p05", "estimacion": "p50", "sup": "p95"})[["p05", "p50", "p95"]]

    TABLAS.mkdir(parents=True, exist_ok=True)
    sufijo = "".join([f"_desde{a.desde[:4]}" if a.desde else "", "_pb_alternativa" if a.pb_alternativa else "",
                      "_sin_quiebres" if a.sin_quiebres else ""])
    pre = f"fase24_{a.deuda}{sufijo}"
    tabla_p.assign(p_aic=p_aic, p_elegido=p).to_csv(TABLAS / f"{pre}_rezagos.csv", index=False)
    pd.DataFrame(base["S"], index=ENDOG, columns=[f"shock_{c}" for c in ENDOG]).to_csv(TABLAS / f"{pre}_S.csv")
    pd.DataFrame(base["fed"], columns=ENDOG).rename_axis("trimestre").to_csv(TABLAS / f"{pre}_respuesta_fed.csv")
    q.to_csv(TABLAS / f"{pre}_bootstrap.csv")
    diag = diagnosticos(base["res"])
    diag.to_csv(TABLAS / f"{pre}_diagnosticos.csv", index=False)
    with open(TABLAS / f"{pre}_resumen_var.txt", "w", encoding="utf-8") as fh:
        fh.write(str(base["res"].summary()))

    print(f"SVARX deuda={a.deuda} muestra efectiva {Y.index[p].date()}-{Y.index[-1].date()} n={len(Y) - p} p={p} (AIC={p_aic}) shock FED={tam_fed:.4f} pp")
    print(f"Quiebres: {[str(f.date()) for f in quiebres]} | bootstrap validas={len(boot)} fallidas={fallidas}")
    print(f"Reaccion fiscal (Bohn) rho={base['rho']:.4f} p={base['rho_p']:.4f} | Hall 90%: "
          f"[{q.loc['rho_bohn','p05']:.4f}, {q.loc['rho_bohn','p95']:.4f}] | largo plazo "
          f"{base['rho_lp']:.4f} [{q.loc['rho_largo_plazo','p05']:.4f}, {q.loc['rho_largo_plazo','p95']:.4f}]")
    print("Respuesta a +1 desvio FED (h=0,4,8,20) con banda 90%:")
    sel = [i for i in q.index if i.startswith("fed_") and i.rsplit("_h", 1)[1] in ("0", "4", "8", "20")]
    print(q.loc[sel].round(3))
    print("Diagnosticos:\n", diag.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
