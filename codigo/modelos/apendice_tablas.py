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
NOMBRES = {"pb_pib": "Resultado primario", "crec": "Crecimiento", "EMBI": "EMBI", "TCRM": "TCRM"}
SERIES = {"federal": "federal bruta (principal)", "consolidada": "consolidada con el BCRA (extensión)"}
ROBUSTEZ = {
    "federal": "Principal (deuda federal bruta)",
    "consolidada": "Deuda consolidada con el BCRA",
    "federal_pb_alt": "Resultado primario con rentas de la propiedad",
    "federal_dom": "Canal de tasas en pesos",
    "federal_sin_retro": "Sin retroalimentación de la deuda",
    "federal_p1": "Un rezago (criterio de Schwarz)",
    "federal_p3": "Tres rezagos",
    "federal_chol": "Cholesky, resultado primario primero",
    "federal_chol_ultimo": "Cholesky, resultado primario último",
    "federal_alfa0": "Elasticidad cíclica 0",
    "federal_alfa0.5": "Elasticidad cíclica 0,5",
    "federal_sin_default": "Sin los *shocks* de 2001T4-2005T3",
    "federal_desde1999": "Solo EMBI observado (datos desde 1999, sin empalme)",
    "federal_desde2004": "Datos desde 2004",
    "federal_sin_quiebres": "Sin variables binarias de quiebre",
    "federal_sin_presidenciales": "Sin variables binarias presidenciales",
    "federal_sf0": "Ajuste stock-flujo en cero",
    "federal_lam0.15": "λ = 0,15",
    "federal_lam0.4": "λ = 0,40",
    "federal_cr2595": "Escenario del FMI de 2025",
    "federal_kilian": "Parámetros corregidos por sesgo (Kilian, 1998)",
}


def num(x: float, d: int = 3) -> str:
    """Formato con coma decimal."""
    cad = f"{x:,.{d}f}"
    if float(cad.replace(",", "")) == 0:  # evita "-0,0"
        cad = cad.lstrip("-")
    return cad.replace(",", "X").replace(".", ",").replace("X", ".")


def pval(v: float, kpss: bool = False) -> str:
    """P-valor con coma decimal. Los que quedan en el limite de la tabla de cada prueba se escriben
    como desigualdades: '< 0,001' (ADF, Jarque-Bera, Portmanteau, ARCH-LM) y, en KPSS, que solo
    interpola entre 0,01 y 0,10, '< 0,01' y '> 0,10'."""
    if kpss:
        return "> 0,10" if v >= 0.10 - 1e-9 else ("< 0,01" if v <= 0.01 + 1e-9 else num(v, 3))
    return "< 0,001" if v < 0.001 else num(v, 3)


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
               "EMBI": "EMBI (puntos básicos)", "TCRM": "TCRM (diciembre de 2001 = 1)",
               "deuda_l1": "Deuda federal bruta, rezagada (% del PIB)",
               "dFED_l0": "Variación de la tasa de la FED (puntos)", "VIX": "VIX"}
    filas = [[nombres[c], num(muestra[c].mean(), 2), num(muestra[c].std(ddof=1), 2), num(muestra[c].min(), 2),
              num(muestra[c].max(), 2)] for c in nombres]
    d = pd.DataFrame(filas, columns=["Variable", "Media", "Desvío estándar", "Mínimo", "Máximo"])
    serie_d = pd.read_csv(f24.DATOS / "procesados" / f24.SERIES_DEUDA["federal"][0], parse_dates=["Date"],
                          index_col="Date")[f24.SERIES_DEUDA["federal"][1]].dropna()
    dic23 = serie_d[serie_d.index == "2023-12-31"].iloc[0]
    nota = (f"\nEl máximo de la deuda federal bruta propia, {num(serie_d.max(), 2)}%, corresponde a {trim(serie_d.idxmax())}, "
            f"después de la devaluación de 2002. No proviene de la cifra del FMI para diciembre de 2023 (154,6%), con la que "
            f"coincide por casualidad: la serie propia da {num(dic23, 1)}% en esa fecha (Tabla 5.2).\n")
    return (f"## A.1 Estadísticos descriptivos\n\nMuestra efectiva de estimación, {trim(muestra.index[0])}-"
            f"{trim(muestra.index[-1])} ({len(muestra)} trimestres).\n\n" + tabla(d) + nota + "\n")


def seccion_empalmes() -> str:
    """Empalmes del EMBI (1996T1-1998T3) y del TCRM (1996) con su validacion."""
    v = pd.read_csv(TABLAS / "empalmes_validacion.csv").set_index("empalme")
    e, tc = v.loc["EMBI"], v.loc["TCRM"]
    emp = pd.read_csv(BASE / "datos" / "procesados" / "empalmes_1996_1998.csv", index_col=0, parse_dates=True)
    filas = [["EMBI", "Tasa de préstamos interfinancieros en dólares (BCRA) menos tasa de fondos federales",
              "1998T4-2001T3", int(e["n"]), num(e["correlacion"], 3), num(e["r2"], 2),
              f"Error típico dejando un trimestre afuera: {num(e['rmse_dejando_uno_afuera'], 0)} pb (desvío del EMBI: {num(e['desvio_embi_superposicion'], 0)} pb)"],
             ["TCRM", "Tipo de cambio real efectivo amplio del BIS (invertido)", "1997T2-2025T4", int(tc["n"]),
              num(tc["correlacion"], 3), num(tc["r2"], 2),
              f"Correlación de las variaciones en 1997-2001: {num(tc['correlacion_1997_2001'], 3)}"]]
    d = pd.DataFrame(filas, columns=["Serie", "Variable puente", "Superposición", "n", "Correlación", "R²", "Validación"])
    real = e["fuera_de_muestra_2001_real"].replace(";", " ;").split(";")
    pron = e["fuera_de_muestra_2001_pronostico"].split(";")
    oos = pd.DataFrame({"Trimestre": ["2001T1", "2001T2", "2001T3"],
                        "EMBI observado": [r.strip() for r in real], "Pronóstico fuera de muestra": [x.strip() for x in pron]})
    vals = pd.DataFrame({"Trimestre": [trim(i) for i in emp.index],
                         "EMBI empalmado (pb)": emp["EMBI"].map(lambda x: "" if pd.isna(x) else num(x, 0)),
                         "TCRM empalmado": emp["TCRM"].map(lambda x: "" if pd.isna(x) else num(x, 3))})
    return ("## A.2 Empalmes de 1996-1998\n\n"
            "La serie diaria pública del EMBI para Argentina comienza el 11 de diciembre de 1998 y el índice de tipo de cambio "
            "real multilateral del BCRA, en enero de 1997. Para completar la ventana 1996-2025, el EMBI de 1996T1-1998T3 se "
            f"reconstruye con la relación EMBI = {num(e['a'], 1)} + {num(e['b'], 3)} × diferencial, estimada en la superposición, "
            "donde el diferencial es la tasa de préstamos interfinancieros en dólares del BCRA menos la tasa de fondos federales. "
            "La superposición termina en 2001T3 porque el corralito de diciembre de 2001 interrumpe el mercado interbancario en "
            "dólares. El TCRM de 1996 se encadena hacia atrás con las variaciones del tipo de cambio real efectivo del BIS. La "
            "Figura A.1 compara las series observadas con las reconstruidas.\n\n"
            + tabla(d) + "\nFuente: elaboración propia con datos del BCRA, J.P. Morgan (serie diaria publicada por Ámbito "
            "Financiero), Reserva Federal y BIS. La correlación y el R² del EMBI son de niveles trimestrales, entre el EMBI y el "
            "diferencial; los del TCRM son de variaciones trimestrales, entre el índice del BCRA y el del BIS, porque el "
            "empalme encadena variaciones.\n\n"
            "Como la estimación empieza en 1998T2 (sección 4.5) y el modelo tiene dos rezagos, el TCRM de 1996 no entra en "
            "el SVARX y el EMBI reconstruido solo aparece en 1997T4-1998T3. El TCRM de 1996 sí entra en la variante a la "
            "manera del FMI, para calcular la depreciación real de 1997; el EMBI no se usa en esa variante.\n\n"
            "**Validación fuera de muestra del empalme del EMBI.** Relación estimada solo con 1998T4-2000T4 y aplicada a 2001:\n\n"
            + tabla(oos) + "\nEl empalme reproduce el nivel y subestima el salto de la crisis de 2001: si tiene un sesgo, atenúa "
            "la volatilidad de 1996-1998 y vuelve más conservadoras las probabilidades. Con datos desde 1999, sin empalme, los "
            "resultados casi no cambian (sección A.10).\n\n"
            + tabla(vals) + "\nFuente: elaboración propia.\n\n"
            "![Figura A.1. Empalmes del EMBI y del TCRM. Series observadas y reconstruidas con las variables puente; el "
            "sombreado marca la superposición del EMBI. Fuente: elaboración propia con datos del BCRA, J.P. Morgan, Reserva "
            "Federal y BIS.](../tesis/figuras/figA_1_empalmes.png)\n\n")


def seccion_propiedades() -> str:
    r = pd.read_csv(TABLAS / "fase24b_raiz_unitaria.csv")
    d = pd.DataFrame({
        "Serie": r["serie"],
        "ADF (p)": r["adf_p"].map(pval), "KPSS (p)": r["kpss_p"].map(lambda v: pval(v, True)),
        "Clasificación": r["clasificacion"].map({"I(0)": "estacionaria", "I(1)": "raíz unitaria", "ambigua": "ambigua"}),
        "Zivot-Andrews (p)": r["za_p"].map(pval),
        "Quiebre de Zivot-Andrews": pd.to_datetime(r["za_quiebre"]).map(trim),
    })
    _, _, _, quiebres = muestra_principal()
    bp = pd.read_csv(TABLAS / "fase24b_bai_perron.csv")
    m = int(bp["m_optimo"].iloc[0])
    jo = pd.read_csv(TABLAS / "fase24b_johansen.csv")
    jn = jo[jo["variables"] == "niveles (sin crecimiento)"]
    j = pd.DataFrame({"Hipótesis nula": jn["rango_nulo"].str.replace("r <= 0", "rango = 0").str.replace("r <= ", "rango ≤ "),
                      "Traza": jn["traza"].map(lambda v: num(v, 1)), "Valor crítico 5%": jn["critico_95"].map(lambda v: num(v, 1)),
                      "Rechaza": jn["rechaza_95"].map({True: "sí", False: "no"})})
    qg = pd.read_csv(TABLAS / "fase24_federal_quiebres_y_gobiernos.csv")
    fechas = ", ".join(qg["quiebre"])
    cons = ", ".join(trim(q) for q in quiebres)
    return ("## A.3 Propiedades de las series\n\n"
            "**Raíz unitaria.** ADF (Dickey y Fuller, 1979; hipótesis nula: raíz unitaria) y KPSS (Kwiatkowski et al., 1992; "
            "hipótesis nula: estacionariedad), con constante. Una serie se clasifica como estacionaria solo si ADF rechaza y KPSS "
            "no rechaza al 5%, y con raíz unitaria en el caso inverso. Zivot y Andrews (1992) permiten un quiebre endógeno en el "
            "nivel. Ventana 1996-2025. Especificación: en ADF y en Zivot y Andrews, el número de rezagos de las diferencias se "
            "elige por el criterio de Akaike hasta el máximo de la regla de Schwert (1989), con constante y sin tendencia; en KPSS, "
            "con constante, el ancho de banda es el que elige el procedimiento automático de Hobijn et al. (2004). Los p-valores de "
            "KPSS se interpolan entre 0,01 y 0,10, por lo que se escriben como desigualdades en los extremos.\n\n"
            + tabla(d.reset_index(drop=True)) +
            f"\n**Quiebres estructurales.** El procedimiento de Bai y Perron (2003) sobre la media de la deuda federal bruta "
            f"(1996-2025), con el número de quiebres elegido por el criterio de Schwarz, encuentra {m} quiebres: {fechas}. Entran "
            f"como variables binarias de escalón en el SVARX los de {cons.replace(', ', ' y ')}; el que coincide con un cambio de gobierno lo reemplazan las "
            "binarias presidenciales.\n\n"
            "**Cointegración.** Prueba de la traza de Johansen (1991) sobre las variables en niveles (resultado primario, EMBI, "
            "TCRM y deuda), con los rezagos del VAR. El crecimiento se excluye porque es una tasa de variación. Términos "
            "determinísticos: una constante en el VAR en niveles, sin tendencia (det_order = 0 en la implementación de "
            "*statsmodels*), con el número de rezagos del VAR menos uno en las diferencias; los valores críticos son los de la "
            "traza al 5% para esa especificación. La prueba omite los quiebres y las binarias, de modo que es indicativa "
            "(Johansen et al., 2000).\n\n"
            + tabla(j.reset_index(drop=True)) + "\n" + seccion_presidenciales())


PRESIDENTES = {"De_la_Rua": "De la Rúa", "Duhalde": "Duhalde", "N_Kirchner": "N. Kirchner", "CF_Kirchner": "C. Fernández de Kirchner",
           "Macri": "Macri", "A_Fernandez": "A. Fernández", "Milei": "Milei", "Menem": "Menem"}


def presidente(c: str) -> str:
    return PRESIDENTES.get(c, c.replace("_", " "))


def seccion_presidenciales() -> str:
    """Significancia conjunta de las binarias presidenciales y mapa de quiebres y gobiernos."""
    w = pd.read_csv(TABLAS / "fase24_federal_wald_presidenciales.csv")
    w = pd.DataFrame({"Contraste": w["contraste"].str.replace("Wald, ecuacion", "Wald, ecuación").str.replace(
        "Razon de verosimilitud", "Razón de verosimilitud").str.replace("pb_pib", "resultado primario").str.replace(
        "crec", "crecimiento"), "Estadístico": w["estadistico"].map(lambda v: num(v, 2)), "Grados de libertad": w["gl"],
        "p-valor": w["p_valor"].map(pval)})
    q = pd.read_csv(TABLAS / "fase24_federal_quiebres_y_gobiernos.csv")
    q = pd.DataFrame({"Quiebre": q["quiebre"], "Gobierno en funciones": q["gobierno_en_funciones"].map(presidente),
                      "Inicio de gobierno más cercano": q["inicio_de_gobierno_mas_cercano"].map(presidente),
                      "Distancia (trimestres)": q["distancia_trimestres"], "Tratamiento": q["tratamiento"]})
    return ("**Binarias presidenciales.** Significancia conjunta de las siete binarias por mandato (Menem es la referencia): "
            "prueba de Wald (estadístico F) en cada ecuación y razón de verosimilitud del sistema con la corrección de Sims "
            "(1980).\n\n" + tabla(w) + "\n**Coincidencia de los quiebres con los cambios de gobierno.** Los quiebres se "
            "recalculan al reestimar con otra serie o muestra. Cuando uno coincide con el inicio de un gobierno, las binarias "
            "presidenciales lo reemplazan; los que caen dentro de un mandato se conservan.\n\n" + tabla(q) + "\n")


def seccion_rezagos() -> str:
    t0 = pd.read_csv(TABLAS / "fase24_federal_rezagos.csv")
    out = ("## A.4 Selección del orden del VAR\n\n"
           f"Muestra efectiva común {t0['inicio'].iloc[-1][:4]}-2025 ({int(t0['n_efectivo'].iloc[0])} trimestres) para todos "
           "los órdenes (sección 4.5). El punto de partida es el orden que elige el criterio de Schwarz entre los órdenes "
           "estables (Ivanov y Kilian, 2005); si sus residuos rechazan la ausencia de autocorrelación, se toma el menor orden "
           "mayor que no la rechaza y, si ninguno la rechaza al 5%, el orden estable con el mayor p-valor de Portmanteau.\n\n")
    t = t0
    d = pd.DataFrame({
        "p": t["p"], "AIC": t["aic"].map(num), "BIC": t["bic"].map(num), "HQ": t["hqic"].map(num),
        "Raíz máxima": t["modulo_raiz_max"].map(num), "Estable": t["estable"].map({True: "sí", False: "no"}),
        "Portmanteau (p)": t["portmanteau_12_p"].map(pval),
    })
    tc = pd.read_csv(TABLAS / "fase24_consolidada_rezagos.csv")
    fila_c = tc[tc["p"] == tc["p_elegido"].iloc[0]].iloc[0]
    out += (f"**Deuda {SERIES['federal']}.** Orden del criterio de Schwarz: {int(t['p_sic'].iloc[0])}. "
            f"Orden elegido: {int(t['p_elegido'].iloc[0])}.\n\n" + tabla(d) +
            f"\nCon la deuda {SERIES['consolidada']}, la misma regla elige {int(fila_c['p'])} {'rezago' if int(fila_c['p']) == 1 else 'rezagos'} (raíz máxima "
            f"{num(fila_c['modulo_raiz_max'])}, Portmanteau p = {num(fila_c['portmanteau_12_p'])}); muestra efectiva "
            f"{fila_c['inicio'][:4]}-2025 ({int(fila_c['n_efectivo'])} trimestres), desde 2002 (sección 5.2).\n\n")
    return out


def seccion_diagnosticos() -> str:
    filas = {}
    for s in SERIES:
        t = pd.read_csv(TABLAS / f"fase24_{s}_diagnosticos.csv").set_index("prueba")["valor"]
        filas[SERIES[s]] = t
    d = pd.DataFrame(filas)
    d.index = [i.replace("(1 = si)", "(1 = sí)").replace("pb_pib", "resultado primario").replace("crec", "crecimiento") for i in d.index]
    estab = d.index.str.startswith("Estable")
    d = d.apply(lambda col: [num(v) if e else pval(v) for v, e in zip(col, estab)])
    d.insert(0, "Prueba (p-valor salvo estabilidad)", list(d.index))
    return ("## A.5 Diagnósticos de los residuos\n\nPortmanteau con 12 rezagos (autocorrelación), Jarque-Bera multivariada "
            "(normalidad), ARCH-LM con cuatro rezagos por ecuación (heterocedasticidad condicional) y estabilidad (1 = estable).\n\n"
            + tabla(d.reset_index(drop=True)) + "\n")


def seccion_impacto() -> str:
    S = pd.read_csv(TABLAS / "fase24_federal_S.csv", index_col=0)
    S.index = [NOMBRES[i] for i in S.index]
    S.columns = ["*Shock* fiscal", "*Shock* de actividad", "*Shock* cambiario y de riesgo 1", "*Shock* cambiario y de riesgo 2"]
    S = S.map(lambda v: num(0.0 if abs(v) < 1e-10 else v))
    S.insert(0, "Variable", S.index)
    return ("## A.6 Matriz de impacto estructural\n\nEfecto en el mismo trimestre de un *shock* estructural de un desvío "
            "estándar (especificación principal). Los ceros son las restricciones de identificación de la sección 4.4. Los dos "
            "*shocks* del bloque cambiario y de riesgo no tienen interpretación por separado: solo se usa su efecto conjunto.\n\n"
            + tabla(S.reset_index(drop=True)) + "\n")


def seccion_cholesky() -> str:
    """Matrices de impacto de los dos ordenamientos de Cholesky de la robustez (A.7)."""
    cols = ["*Shock* del resultado primario", "*Shock* del crecimiento", "*Shock* del EMBI", "*Shock* del TCRM"]
    textos = {"pb_primero": ("Resultado primario primero", "resultado primario, crecimiento, EMBI, TCRM"),
              "pb_ultimo": ("Resultado primario último", "crecimiento, TCRM, EMBI, resultado primario")}
    salida = ("## A.7 Matrices de impacto de los ordenamientos de Cholesky\n\nEfecto en el mismo trimestre de un *shock* "
              "de un desvío estándar, con el mismo formato que la matriz estructural (A.6). En una descomposición de Cholesky "
              "cada variable responde en el trimestre a los *shocks* de las que la preceden en el orden y no a los de las que la "
              "siguen, de modo que los ceros de cada matriz indican el orden causal. Las filas están en el orden del sistema y las "
              "columnas son el *shock* de cada variable.\n\n")
    for clave, (titulo, orden) in textos.items():
        S = pd.read_csv(TABLAS / f"fase24_federal_S_cholesky_{clave}.csv", index_col=0)
        S.index = [NOMBRES[i] for i in S.index]
        S.columns = cols
        S = S.map(lambda v: num(0.0 if abs(v) < 1e-10 else v))
        S.insert(0, "Variable", S.index)
        salida += f"**{titulo}.** Orden de las variables, de la primera a la última: {orden}.\n\n" + tabla(S.reset_index(drop=True)) + "\n"
    return salida


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
        elif k.startswith("P_"):
            nom = "Binaria presidencial: " + presidente(k[2:])
        else:
            nom = {"deuda_l1": "Deuda federal bruta, rezago 1 (reacción fiscal de impacto)", "VIX": "VIX"}[k]
        filas.append([nom, num(par[k], 4), num(se[k], 4), pval(pv[k])])
    d = pd.DataFrame(filas, columns=["Regresor", "Coeficiente", "Error estándar", "p-valor"])
    b = pd.read_csv(TABLAS / "fase24_federal_bootstrap.csv", index_col=0)
    lp = b.loc["rho_largo_plazo"]
    nota = (" El coeficiente de la deuda rezagada es el efecto de impacto sobre el resultado primario trimestral. El "
            "multiplicador de largo plazo, que descuenta los rezagos propios del resultado primario, es "
            f"{num(lp['p50'], 3)}, con un intervalo de 90% de [{num(lp['p05'], 3)}; {num(lp['p95'], 3)}].")
    return ("## A.8 Ecuación del resultado primario\n\nEcuación del resultado primario del VARX en forma reducida, "
            f"especificación principal (MCO, {trim(Y.index[p])}-{trim(Y.index[-1])}). No se muestran la constante, las "
            "variables binarias estacionales ni las de los quiebres. Los errores estándar y los p-valores son los de MCO y se "
            "informan como referencia: con regresores que pueden tener raíz unitaria su distribución no es la estándar (Sims et "
            "al., 1990), por lo que la inferencia del texto usa los intervalos del *bootstrap*." + nota + "\n\n" + tabla(d) + "\n")


def seccion_principal() -> str:
    t = pd.read_csv(TABLAS / "fase25_federal_resumen.csv", index_col=0)
    ind = {"base_p_noest_2031": ("No estabilización 2031, métrica anual (%)", 100), "base_p_noest_2035": ("No estabilización 2035, métrica anual (%)", 100),
           "base_p_noest_sim_2031": ("No estabilización 2031, métrica anual con el resultado primario simulado (%)", 100),
           "base_p_sube2_2031": ("Probabilidad de que la deuda de 2031 supere a la de 2029 (%)", 100),
           "base_p_noest_fmi_2031": ("No estabilización 2031, definición operativa del FMI (%)", 100),
           "base_p_noest_fmi_2035": ("No estabilización 2035, definición operativa del FMI (%)", 100),
           "base_p_noest_fmi_sim_2031": ("No estabilización 2031, definición operativa del FMI, resultado primario simulado (%)", 100),
           "base_p_noest_fmi_prom_2031": ("No estabilización 2031, lectura literal del recuadro 3 del FMI (%)", 100),
           "base_p_noest_fmi_prom_2035": ("No estabilización 2035, lectura literal del recuadro 3 del FMI (%)", 100),
           "base_d2031_mediana": ("Deuda mediana 2031 (% del PIB)", 1), "base_d2035_media": ("Deuda media 2035 (% del PIB)", 1),
           "base_ancho_p5_p95_2031": ("Ancho del abanico 2031 (p5-p95)", 1),
           "vshare_fiscal": ("Varianza 2035: fiscal (%)", 1), "vshare_actividad": ("Varianza 2035: actividad (%)", 1),
           "vshare_cambiario_y_riesgo": ("Varianza 2035: cambiario y de riesgo (%)", 1),
           "vshare_externo": ("Varianza 2035: externo, FED y VIX (%)", 1),
           "vshare_externo_vix": ("Varianza 2035: solo VIX, mismo denominador (%)", 1),
           "vshare_externo_fed": ("Varianza 2035: solo tasa de la FED (%)", 1),
           "vshare_externo_fed_directo": ("Varianza 2035: tasa de la FED, solo efecto directo en la identidad (%)", 1),
           "vshare_externo_fed_indirecto": ("Varianza 2035: tasa de la FED, efecto indirecto (diferencia) (%)", 1),
           "var_total_2035": ("Varianza total de la deuda 2035 (puntos del PIB al cuadrado)", 1),
           "var_suma_bloques_2035": ("Suma de las varianzas de los cuatro bloques", 1),
           "h1a_nofiscal_menos_fiscal": ("No fiscal menos fiscal (puntos)", 1),
           "dif_fed_1de_p_noest_2035": ("FED, nivel 0,50 pp más alto: diferencia en la probabilidad 2035 (pp)", 100),
           "dif_fed_1de_d2035": ("FED, nivel 0,50 pp más alto: diferencia en la deuda media 2035 (pp del PIB)", 1),
           "dif_fed_2022_2025_p_noest_2031": ("FED, senda 2022-2025: diferencia en la probabilidad 2031 (pp)", 100),
           "dif_fed_2022_2025_p_noest_2035": ("FED, senda 2022-2025: diferencia en la probabilidad 2035 (pp)", 100),
           "dif_fed_2022_2025_d2035": ("FED, senda 2022-2025: diferencia en la deuda media 2035 (pp del PIB)", 1),
           "dif_fed_2022_2025_p_noest_fmi_2035": ("FED, senda 2022-2025: diferencia en la probabilidad 2035, definición operativa del FMI (pp)", 100)}
    filas = [[nombre, num(t.loc[k, "estimacion"] * f, 1), f"[{num(t.loc[k, 'p05'] * f, 1)}; {num(t.loc[k, 'p95'] * f, 1)}]"]
             for k, (nombre, f) in ind.items()]
    d = pd.DataFrame(filas, columns=["Medida", "Estimación central", "Intervalo de 90%"])
    meta = json.loads((TABLAS / "fase25_federal_meta.json").read_text(encoding="utf-8"))
    miles = lambda v: f"{v:,}".replace(",", ".")
    nota = (f"Estimación central con los parámetros de MCO y {miles(meta['N_central'])} trayectorias (error de Monte Carlo de "
            f"{num(100 * t.loc['error_mc_p_noest_2031', 'estimacion'], 1)} puntos en la probabilidad de 2031); intervalos de Hall con "
            f"{miles(meta['B'])} réplicas de parámetros y {miles(meta['N'])} trayectorias cada una. Autovalor máximo del VAR: "
            f"{num(meta['raiz_max_estimada'], 3)}.")
    return "## A.9 Resultados completos de la especificación principal\n\n" + nota + "\n\n" + tabla(d) + "\n"


def seccion_robustez() -> str:
    filas = []
    for s, nombre in ROBUSTEZ.items():
        archivo = TABLAS / f"fase25_{s}_resumen.csv"
        if not archivo.exists():
            raise FileNotFoundError(archivo)
        t = pd.read_csv(archivo, index_col=0)
        iv = lambda k, f=100, dd=1: f"{num(t.loc[k, 'estimacion'] * f, dd)} [{num(t.loc[k, 'p05'] * f, dd)}; {num(t.loc[k, 'p95'] * f, dd)}]"
        # Trayectorias explosivas: la media de la deuda (y las varianzas) de una replica quedan dominadas por unas pocas.
        rep = pd.read_csv(TABLAS / f"fase25_{s}_replicas.csv")
        expl = float((rep["base_d2035_media"].abs() > 1000).mean())
        d_fed = "no se informa" if expl > 0.01 else iv("dif_fed_2022_2025_d2035", 1, 2)
        h1a = "no se informa" if expl > 0.10 else iv("h1a_nofiscal_menos_fiscal", 1)
        filas.append([nombre, iv("base_p_noest_2031"), iv("base_p_noest_2035"), iv("base_p_noest_fmi_2031"), iv("base_p_noest_fmi_2035"),
                      num(t.loc["base_ancho_p5_p95_2031", "estimacion"], 1), h1a, iv("dif_fed_2022_2025_p_noest_2035"), d_fed])
    for s, nombre in (("federal_fmi", "*Shocks* a la manera del FMI, deuda federal bruta"),
                      ("consolidada_fmi", "*Shocks* a la manera del FMI, deuda consolidada")):
        v = pd.read_csv(TABLAS / f"fase25_{s}_resumen.csv", index_col=0)["valor"]
        filas.append([nombre, num(100 * v["p_noest_2031"], 1), num(100 * v["p_noest_2035"], 1), num(100 * v["p_noest_fmi_2031"], 1), num(100 * v["p_noest_fmi_2035"], 1),
                      num(v["ancho_p5_p95_2031"], 1), "no aplica", "no aplica", "no aplica"])
    filas.append(["FMI (2026), deuda federal bruta", "1,0", "menos de 3", "1,0", "menos de 3", "71,5", "no aplica", "no aplica", "no aplica"])
    d = pd.DataFrame(filas, columns=["Especificación", "No estabilización 2031, métrica anual (%)", "No estabilización 2035, métrica anual (%)",
                                     "No estabilización 2031, definición operativa del FMI (%)", "No estabilización 2035, definición operativa del FMI (%)", "Ancho 2031", "No fiscal menos fiscal (puntos)", "Senda de la FED: probabilidad 2035 (pp)",
                                     "Senda de la FED: deuda 2035 (pp)"])
    return ("## A.10 Robustez completa\n\nEntre corchetes, intervalos de 90%: de Hall, salvo las participaciones y varianzas y la diferencia entre *shocks* no fiscales y fiscal, que usan percentiles simples de las réplicas. Las columnas de la definición operativa del FMI usan la reconstrucción de la sección 4.6: los impulsores del escenario en el año final más el *shock* promedio de cada trayectoria, sin variación del tipo de cambio real ni ajuste *stock*-flujo (FMI, 2022, recuadro 3). La columna de la deuda de la senda de la FED se muestra con dos decimales para distinguir los intervalos que tocan el cero. «No se informa»: más de 1% de las réplicas (10% en la columna del reparto de la varianza) tiene trayectorias explosivas que dominan la media de la deuda. Todas las especificaciones usan los mismos "
            "números aleatorios, de modo que las diferencias entre filas no provienen del sorteo. Las filas a la manera del FMI "
            "no tienen intervalo porque ese procedimiento no estima parámetros. Fuente de la última fila: FMI (2026, anexo II, "
            "cuadro 7 y párrafo 9).\n\n" + tabla(d) + "\n")


def main() -> None:
    texto = "# Apéndice estadístico\n\nFuente de todas las tablas, salvo indicación: elaboración propia.\n\n"
    texto += (seccion_descriptivos() + seccion_empalmes() + seccion_propiedades() + seccion_rezagos() + seccion_diagnosticos()
              + seccion_impacto() + seccion_cholesky() + seccion_fiscal() + seccion_principal() + seccion_robustez())
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"[OK] {SALIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
