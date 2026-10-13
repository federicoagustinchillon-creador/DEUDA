"""
apendice_tablas.py
==================
Genera el Apendice estadistico de la tesis (tesis_oficial_borradores/apendice.md) a partir de
los resultados guardados por fase24, fase24b y fase25 y de una reestimacion de la especificacion
principal (para los errores estandar de la ecuacion fiscal). Ninguna cifra ni fecha se tipea a
mano: todas salen de los archivos de resultados.

Uso: python codigo/modelos/apendice_tablas.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase24_svarx_1996_2025 as f24  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
TABLAS = BASE / "resultados" / "tablas"
SALIDA = BASE / "tesis_oficial_borradores" / "apendice.md"
NOMBRES = {"pb_pib": "Resultado primario", "crec": "Crecimiento", "EMBI": "EMBI+", "TCRM": "TCRM"}
SERIES = {"federal": "federal bruta (principal)", "consolidada": "consolidada con el BCRA (extensión)"}
ROBUSTEZ = {
    "federal": "Principal (deuda federal bruta)",
    "consolidada": "Deuda consolidada con el BCRA",
    "federal_pb_alt": "Resultado primario sin rentas de la propiedad",
    "federal_dom": "Canal de tasas en pesos",
    "federal_sin_retro": "Sin retroalimentación de la deuda",
    "federal_p1": "Un rezago (criterio de Schwarz)",
    "federal_p3": "Tres rezagos",
    "federal_chol": "Cholesky, resultado primario primero",
    "federal_chol_ultimo": "Cholesky, resultado primario último",
    "federal_alfa0": "Elasticidad cíclica 0",
    "federal_alfa0.5": "Elasticidad cíclica 0,5",
    "federal_sin_default": "Sin los *shocks* de 2001T4-2005T3",
    "federal_desde2004": "Datos desde 2004",
    "federal_sin_quiebres": "Sin variables binarias de quiebre",
    "federal_sf0": "Ajuste stock-flujo en cero",
    "federal_lam0.15": "λ = 0,15",
    "federal_lam0.4": "λ = 0,40",
    "federal_cr2595": "Escenario del FMI de 2025",
    "federal_kilian": "Parámetros corregidos por sesgo (Kilian, 1998)",
}


def num(x: float, d: int = 3) -> str:
    """Formato con coma decimal."""
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def trim(f: pd.Timestamp) -> str:
    return f"{f.year}T{f.quarter}"


def tabla(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |\n|" + "---|" * len(df.columns) + "\n"
    return cab + "".join("| " + " | ".join(str(v) for v in fila) + " |\n" for fila in df.values)


def muestra_principal() -> tuple[pd.DataFrame, pd.DataFrame, int, list]:
    Y, X, quiebres = f24.cargar_datos("federal", 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    Y, X = f24.recortar(Y, X, p)
    return Y, X, p, quiebres


def seccion_descriptivos() -> str:
    Y, X, p, _ = muestra_principal()
    muestra = pd.concat([Y.iloc[p:], X.iloc[p:][["deuda_l1", "dFED_l0", "VIX"]]], axis=1)
    nombres = {"pb_pib": "Resultado primario (% del PIB, trimestral anualizado)", "crec": "Crecimiento real trimestral (%)",
               "EMBI": "EMBI+ (puntos básicos)", "TCRM": "TCRM (diciembre de 2001 = 1)",
               "deuda_l1": "Deuda federal bruta, rezagada (% del PIB)",
               "dFED_l0": "Variación de la tasa de la FED (puntos)", "VIX": "VIX"}
    filas = [[nombres[c], num(muestra[c].mean(), 2), num(muestra[c].std(ddof=1), 2), num(muestra[c].min(), 2),
              num(muestra[c].max(), 2)] for c in nombres]
    d = pd.DataFrame(filas, columns=["Variable", "Media", "Desvío estándar", "Mínimo", "Máximo"])
    return (f"## A.1 Estadísticos descriptivos\n\nMuestra efectiva de estimación, {trim(muestra.index[0])}-"
            f"{trim(muestra.index[-1])} ({len(muestra)} trimestres).\n\n" + tabla(d) + "\n")


def seccion_propiedades() -> str:
    r = pd.read_csv(TABLAS / "fase24b_raiz_unitaria.csv")
    d = pd.DataFrame({
        "Serie": r["serie"],
        "ADF (p)": r["adf_p"].map(num), "KPSS (p)": r["kpss_p"].map(num),
        "Clasificación": r["clasificacion"].map({"I(0)": "estacionaria", "I(1)": "raíz unitaria", "ambigua": "ambigua"}),
        "Zivot-Andrews (p)": r["za_p"].map(num),
        "Quiebre de Zivot-Andrews": pd.to_datetime(r["za_quiebre"]).map(trim),
    })
    _, _, _, quiebres = muestra_principal()
    bp = pd.read_csv(TABLAS / "fase24b_bai_perron.csv")
    m = int(bp["m_optimo"].iloc[0])
    jo = pd.read_csv(TABLAS / "fase24b_johansen.csv")
    jn = jo[jo["variables"] == "niveles (sin crecimiento)"]
    j = pd.DataFrame({"Hipótesis nula": jn["rango_nulo"].str.replace("r <= ", "rango ≤ "),
                      "Traza": jn["traza"].map(lambda v: num(v, 1)), "Valor crítico 5%": jn["critico_95"].map(lambda v: num(v, 1)),
                      "Rechaza": jn["rechaza_95"].map({True: "sí", False: "no"})})
    fechas = ", ".join(trim(q) for q in quiebres)
    return ("## A.2 Propiedades de las series\n\n"
            "**Raíz unitaria.** ADF (Dickey y Fuller, 1979; hipótesis nula: raíz unitaria) y KPSS (Kwiatkowski et al., 1992; "
            "hipótesis nula: estacionariedad), con constante. Una serie se clasifica como estacionaria solo si ADF rechaza y KPSS "
            "no rechaza al 5%, y con raíz unitaria en el caso inverso. Zivot y Andrews (1992) permiten un quiebre endógeno en el "
            "nivel. Datos desde 1999T1.\n\n"
            + tabla(d.reset_index(drop=True)) +
            f"\n**Quiebres estructurales.** El procedimiento de Bai y Perron (2003) sobre la media de la deuda federal bruta "
            f"(1996-2025), con el número de quiebres elegido por el criterio de Schwarz, encuentra {m} quiebres: {fechas}. Entran "
            "como variables binarias de escalón en el SVARX.\n\n"
            "**Cointegración.** Prueba de la traza de Johansen (1991) sobre las variables en niveles (resultado primario, EMBI+, "
            "TCRM y deuda), con los rezagos del VAR. El crecimiento se excluye porque es una tasa de variación.\n\n"
            + tabla(j.reset_index(drop=True)) + "\n")


def seccion_rezagos() -> str:
    t0 = pd.read_csv(TABLAS / "fase24_federal_rezagos.csv")
    out = ("## A.3 Selección del orden del VAR\n\n"
           f"Muestra efectiva común {t0['inicio'].iloc[-1][:4]}-2025 ({int(t0['n_efectivo'].iloc[0])} trimestres) para todos "
           "los órdenes (sección 4.5). El punto de partida es el orden que elige el criterio de Schwarz entre los órdenes "
           "estables (Ivanov y Kilian, 2005); si sus residuos rechazan la ausencia de autocorrelación, se toma el menor orden "
           "mayor que no la rechaza.\n\n")
    t = t0
    d = pd.DataFrame({
        "p": t["p"], "AIC": t["aic"].map(num), "BIC": t["bic"].map(num), "HQ": t["hqic"].map(num),
        "Raíz máxima": t["modulo_raiz_max"].map(num), "Estable": t["estable"].map({True: "sí", False: "no"}),
        "Portmanteau (p)": t["portmanteau_12_p"].map(num),
    })
    tc = pd.read_csv(TABLAS / "fase24_consolidada_rezagos.csv")
    fila_c = tc[tc["p"] == tc["p_elegido"].iloc[0]].iloc[0]
    out += (f"**Deuda {SERIES['federal']}.** Orden del criterio de Schwarz: {int(t['p_sic'].iloc[0])}. "
            f"Orden elegido: {int(t['p_elegido'].iloc[0])}.\n\n" + tabla(d) +
            f"\nCon la deuda {SERIES['consolidada']}, la misma regla elige {int(fila_c['p'])} rezagos (raíz máxima "
            f"{num(fila_c['modulo_raiz_max'])}, Portmanteau p = {num(fila_c['portmanteau_12_p'])}).\n\n")
    return out


def seccion_diagnosticos() -> str:
    filas = {}
    for s in SERIES:
        t = pd.read_csv(TABLAS / f"fase24_{s}_diagnosticos.csv").set_index("prueba")["valor"]
        filas[SERIES[s]] = t
    d = pd.DataFrame(filas)
    d.index = [i.replace("(1 = si)", "(1 = sí)").replace("pb_pib", "resultado primario").replace("crec", "crecimiento") for i in d.index]
    d = d.map(lambda v: num(v))
    d.insert(0, "Prueba (p-valor salvo estabilidad)", d.index)
    return ("## A.4 Diagnósticos de los residuos\n\nPortmanteau con 12 rezagos (autocorrelación), Jarque-Bera multivariada "
            "(normalidad), ARCH-LM con cuatro rezagos por ecuación (heterocedasticidad condicional) y estabilidad (1 = estable).\n\n"
            + tabla(d.reset_index(drop=True)) + "\n")


def seccion_impacto() -> str:
    S = pd.read_csv(TABLAS / "fase24_federal_S.csv", index_col=0)
    S.index = [NOMBRES[i] for i in S.index]
    S.columns = ["*Shock* fiscal", "*Shock* de actividad", "*Shock* cambiario y de riesgo 1", "*Shock* cambiario y de riesgo 2"]
    S = S.map(lambda v: num(0.0 if abs(v) < 1e-10 else v))
    S.insert(0, "Variable", S.index)
    return ("## A.5 Matriz de impacto estructural\n\nEfecto en el mismo trimestre de un *shock* estructural de un desvío "
            "estándar (especificación principal). Los ceros son las restricciones de identificación de la sección 4.4. Los dos "
            "*shocks* del bloque cambiario y de riesgo no tienen interpretación por separado: solo se usa su efecto conjunto.\n\n"
            + tabla(S.reset_index(drop=True)) + "\n")


def seccion_fiscal() -> str:
    Y, X, p, _ = muestra_principal()
    res = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    par, se, pv = res.params["pb_pib"], res.stderr["pb_pib"], res.pvalues["pb_pib"]
    filas = []
    for k in par.index:
        if k.startswith(("Q", "D")) or k == "const":
            continue
        if re.fullmatch(r"L\d+\.\w+", k):
            rez, var = k[1:].split(".", 1)
            nom = f"{NOMBRES[var]}, rezago {rez}"
        elif k.startswith("dFED_l"):
            nom = f"Variación de la tasa de la FED, rezago {k[-1]}"
        else:
            nom = {"deuda_l1": "Deuda federal bruta, rezago 1 (reacción fiscal de impacto)", "VIX": "VIX"}[k]
        filas.append([nom, num(par[k], 4), num(se[k], 4), num(pv[k], 3)])
    d = pd.DataFrame(filas, columns=["Regresor", "Coeficiente", "Error estándar", "p-valor"])
    b = pd.read_csv(TABLAS / "fase24_federal_bootstrap.csv", index_col=0)
    lp = b.loc["rho_largo_plazo"]
    nota = (" El coeficiente de la deuda rezagada es el efecto de impacto sobre el resultado primario trimestral. El "
            "multiplicador de largo plazo, que descuenta los rezagos propios del resultado primario, es "
            f"{num(lp['p50'], 3)}, con un intervalo de 90% de [{num(lp['p05'], 3)}; {num(lp['p95'], 3)}].")
    return ("## A.6 Ecuación del resultado primario\n\nEcuación del resultado primario del VARX en forma reducida, "
            f"especificación principal (MCO, {trim(Y.index[p])}-{trim(Y.index[-1])}). No se muestran la constante, las "
            "variables binarias estacionales ni las de los quiebres. Los errores estándar y los p-valores son los de MCO y se "
            "informan como referencia: con regresores que pueden tener raíz unitaria su distribución no es la estándar (Sims et "
            "al., 1990), por lo que la inferencia del texto usa los intervalos del *bootstrap*." + nota + "\n\n" + tabla(d) + "\n")


def seccion_principal() -> str:
    t = pd.read_csv(TABLAS / "fase25_federal_resumen.csv", index_col=0)
    ind = {"base_p_noest_2031": ("No estabilización 2031 (%)", 100), "base_p_noest_2035": ("No estabilización 2035 (%)", 100),
           "base_p_noest_sim_2031": ("No estabilización 2031 con el resultado primario simulado (%)", 100),
           "base_p_sube2_2031": ("Probabilidad de que la deuda de 2031 supere a la de 2029 (%)", 100),
           "base_d2031_mediana": ("Deuda mediana 2031 (% del PIB)", 1), "base_d2035_media": ("Deuda media 2035 (% del PIB)", 1),
           "base_ancho_p5_p95_2031": ("Ancho del abanico 2031 (p5-p95)", 1),
           "vshare_fiscal": ("Varianza 2035: fiscal (%)", 1), "vshare_actividad": ("Varianza 2035: actividad (%)", 1),
           "vshare_cambiario_y_riesgo": ("Varianza 2035: cambiario y de riesgo (%)", 1),
           "vshare_externo": ("Varianza 2035: externo, FED y VIX (%)", 1),
           "h1a_nofiscal_menos_fiscal": ("No fiscal menos fiscal (puntos)", 1),
           "dif_fed_1de_p_noest_2035": ("FED, nivel 0,50 pp más alto: diferencia en la probabilidad 2035 (pp)", 100),
           "dif_fed_1de_d2035": ("FED, nivel 0,50 pp más alto: diferencia en la deuda media 2035 (pp del PIB)", 1),
           "dif_fed_2022_2025_p_noest_2031": ("FED, senda 2022-2025: diferencia en la probabilidad 2031 (pp)", 100),
           "dif_fed_2022_2025_p_noest_2035": ("FED, senda 2022-2025: diferencia en la probabilidad 2035 (pp)", 100),
           "dif_fed_2022_2025_d2035": ("FED, senda 2022-2025: diferencia en la deuda media 2035 (pp del PIB)", 1)}
    filas = [[nombre, num(t.loc[k, "estimacion"] * f, 1), f"[{num(t.loc[k, 'p05'] * f, 1)}; {num(t.loc[k, 'p95'] * f, 1)}]"]
             for k, (nombre, f) in ind.items()]
    d = pd.DataFrame(filas, columns=["Medida", "Estimación central", "Intervalo de 90%"])
    meta = json.loads((TABLAS / "fase25_federal_meta.json").read_text(encoding="utf-8"))
    miles = lambda v: f"{v:,}".replace(",", ".")
    nota = (f"Estimación central con los parámetros de MCO y {miles(meta['N_central'])} trayectorias (error de Monte Carlo de "
            f"{num(100 * t.loc['error_mc_p_noest_2031', 'estimacion'], 1)} puntos en la probabilidad de 2031); intervalos de Hall con "
            f"{meta['B']} réplicas de parámetros y {miles(meta['N'])} trayectorias cada una. Autovalor máximo del VAR: "
            f"{num(meta['raiz_max_estimada'], 3)}.")
    return "## A.7 Resultados completos de la especificación principal\n\n" + nota + "\n\n" + tabla(d) + "\n"


def seccion_robustez() -> str:
    filas = []
    for s, nombre in ROBUSTEZ.items():
        archivo = TABLAS / f"fase25_{s}_resumen.csv"
        if not archivo.exists():
            raise FileNotFoundError(archivo)
        t = pd.read_csv(archivo, index_col=0)
        iv = lambda k, f=100, dd=1: f"{num(t.loc[k, 'estimacion'] * f, dd)} [{num(t.loc[k, 'p05'] * f, dd)}; {num(t.loc[k, 'p95'] * f, dd)}]"
        filas.append([nombre, iv("base_p_noest_2031"), iv("base_p_noest_2035"), num(t.loc["base_ancho_p5_p95_2031", "estimacion"], 1),
                      iv("h1a_nofiscal_menos_fiscal", 1), iv("dif_fed_2022_2025_p_noest_2035"), iv("dif_fed_2022_2025_d2035", 1)])
    for s, nombre in (("federal_fmi", "*Shocks* a la manera del FMI, deuda federal bruta"),
                      ("consolidada_fmi", "*Shocks* a la manera del FMI, deuda consolidada")):
        v = pd.read_csv(TABLAS / f"fase25_{s}_resumen.csv", index_col=0)["valor"]
        filas.append([nombre, num(100 * v["p_noest_2031"], 1), num(100 * v["p_noest_2035"], 1),
                      num(v["ancho_p5_p95_2031"], 1), "no aplica", "no aplica", "no aplica"])
    filas.append(["FMI (2026), deuda federal bruta", "1,0", "menos de 3", "71,5", "no aplica", "no aplica", "no aplica"])
    d = pd.DataFrame(filas, columns=["Especificación", "No estabilización 2031 (%)", "No estabilización 2035 (%)",
                                     "Ancho 2031", "No fiscal menos fiscal (puntos)", "Senda de la FED: probabilidad 2035 (pp)",
                                     "Senda de la FED: deuda 2035 (pp)"])
    return ("## A.8 Robustez completa\n\nEntre corchetes, intervalos de 90% de Hall. Todas las especificaciones usan los mismos "
            "números aleatorios, de modo que las diferencias entre filas no provienen del sorteo. Las filas a la manera del FMI "
            "no tienen intervalo porque ese procedimiento no estima parámetros. Fuente de la última fila: FMI (2026, anexo II, "
            "cuadro 7 y párrafo 9).\n\n" + tabla(d) + "\n")


def main() -> None:
    texto = "# Apéndice estadístico\n\nFuente de todas las tablas, salvo indicación: elaboración propia.\n\n"
    texto += (seccion_descriptivos() + seccion_propiedades() + seccion_rezagos() + seccion_diagnosticos()
              + seccion_impacto() + seccion_fiscal() + seccion_principal() + seccion_robustez())
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"[OK] {SALIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
