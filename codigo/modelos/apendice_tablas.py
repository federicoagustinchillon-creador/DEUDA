"""
apendice_tablas.py
==================
Genera el Apendice estadistico de la tesis (tesis_oficial_borradores/apendice.md) a partir de
los resultados guardados por fase24 y fase25 y de una reestimacion de la especificacion
principal (para los errores estandar de la ecuacion fiscal). Ninguna cifra se tipea a mano.

Uso: python codigo/modelos/apendice_tablas.py
"""

from __future__ import annotations

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
SERIES = {"neta": "neta, valor nominal (principal)", "neta_libros": "neta, valor libros", "bruta": "bruta"}


def num(x: float, d: int = 3) -> str:
    """Formato con coma decimal."""
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tabla(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |\n|" + "---|" * len(df.columns) + "\n"
    return cab + "".join("| " + " | ".join(str(v) for v in fila) + " |\n" for fila in df.values)


def seccion_descriptivos() -> str:
    """Estadisticos descriptivos de la muestra efectiva de estimacion (1998T2-2025T4)."""
    Y, X, _ = f24.cargar_datos("neta", 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    Y, X = f24.recortar(Y, X, p)
    muestra = pd.concat([Y.iloc[p:], X.iloc[p:][["deuda_l1", "dFED_l0", "VIX"]]], axis=1)
    nombres = {"pb_pib": "Resultado primario (% del PIB, trimestral anualizado)", "crec": "Crecimiento real trimestral (%)",
               "EMBI": "EMBI+ (puntos básicos)", "TCRM": "TCRM (diciembre de 2001 = 1)",
               "deuda_l1": "Deuda consolidada neta, rezagada (% del PIB)",
               "dFED_l0": "Variación de la tasa de la FED (puntos)", "VIX": "VIX"}
    filas = [[nombres[c], num(muestra[c].mean(), 2), num(muestra[c].std(ddof=1), 2), num(muestra[c].min(), 2),
              num(muestra[c].max(), 2)] for c in nombres]
    d = pd.DataFrame(filas, columns=["Variable", "Media", "Desvío estándar", "Mínimo", "Máximo"])
    return (f"## A.0 Estadísticos descriptivos\n\nMuestra efectiva de estimación, {muestra.index[0].year}T{muestra.index[0].quarter}-"
            f"{muestra.index[-1].year}T{muestra.index[-1].quarter} ({len(muestra)} trimestres).\n\n" + tabla(d) + "\n")


def seccion_rezagos() -> str:
    out = "## A.1 Selección del orden del VAR\n\nMuestra efectiva común 1998T2-2025T4 (111 trimestres) para todos los órdenes (sección 4.5). El orden elegido es el mayor orden estable que no supera al que minimiza el AIC.\n\n"
    for s, nombre in SERIES.items():
        t = pd.read_csv(TABLAS / f"fase24_{s}_rezagos.csv")
        d = pd.DataFrame({
            "p": t["p"], "AIC": t["aic"].map(num), "BIC": t["bic"].map(num), "HQ": t["hqic"].map(num),
            "Raíz máxima": t["modulo_raiz_max"].map(num), "Estable": t["estable"].map({True: "sí", False: "no"}),
            "Portmanteau (p)": t["portmanteau_12_p"].map(num),
        })
        out += f"**Deuda consolidada {nombre}.** Orden elegido: {int(t['p_elegido'].iloc[0])}.\n\n" + tabla(d) + "\n"
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
    return ("## A.2 Diagnósticos de los residuos\n\nPortmanteau con 12 rezagos (autocorrelación), Jarque-Bera multivariada (normalidad), ARCH-LM con cuatro rezagos por ecuación (heterocedasticidad condicional) y estabilidad (1 = estable).\n\n"
            + tabla(d.reset_index(drop=True)) + "\n")


def seccion_impacto() -> str:
    S = pd.read_csv(TABLAS / "fase24_neta_S.csv", index_col=0)
    S.index = [NOMBRES[i] for i in S.index]
    S.columns = ["Shock fiscal", "Shock de actividad", "Shock cambiario y de riesgo 1", "Shock cambiario y de riesgo 2"]
    S = S.map(lambda v: num(0.0 if abs(v) < 1e-10 else v))
    S.insert(0, "Variable", S.index)
    return ("## A.3 Matriz de impacto estructural\n\nEfecto en el mismo trimestre de un shock estructural de un desvío estándar (especificación principal). Los ceros son las restricciones de identificación de la sección 4.4. Los dos shocks del bloque cambiario y de riesgo no tienen interpretación por separado: solo se usa su efecto conjunto.\n\n"
            + tabla(S.reset_index(drop=True)) + "\n")


def seccion_fiscal() -> str:
    Y, X, _ = f24.cargar_datos("neta", 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    Y, X = f24.recortar(Y, X, p)
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
            nom = {"deuda_l1": "Deuda consolidada neta, rezago 1 (reacción de Bohn)", "VIX": "VIX"}[k]
        filas.append([nom, num(par[k], 4), num(se[k], 4), num(pv[k], 3)])
    d = pd.DataFrame(filas, columns=["Regresor", "Coeficiente", "Error estándar", "p-valor"])
    return ("## A.4 Ecuación del resultado primario\n\nEcuación del resultado primario del VARX en forma reducida, especificación principal (MCO, 1998T2-2025T4). No se muestran la constante, las variables binarias estacionales ni las de los quiebres. Los p-valores son los de MCO; el intervalo de la reacción de Bohn que se usa en el texto es el del bootstrap.\n\n"
            + tabla(d) + "\n")


def seccion_robustez() -> str:
    specs = {"neta": "Neta (principal)", "neta_libros": "Neta en libros", "bruta": "Bruta", "neta_dom": "Neta con tasas en pesos", "neta_sin_retro": "Neta sin retroalimentación"}
    ind = {"base_p_noest_2030": ("No estabilización 2030 (%)", 100), "base_p_noest_2035": ("No estabilización 2035 (%)", 100),
           "base_d2035_media": ("Deuda media 2035 (% PIB)", 1), "base_ancho_p5_p95_2030": ("Ancho p5-p95 2030", 1),
           "vshare_fiscal": ("Varianza 2035: fiscal (%)", 1), "vshare_actividad": ("Varianza 2035: actividad (%)", 1),
           "vshare_cambiario_y_riesgo": ("Varianza 2035: cambiario y de riesgo (%)", 1),
           "h1a_nofiscal_menos_fiscal": ("H1a: no fiscal menos fiscal", 1),
           "dif_fed_1de_p_noest_2035": ("H2: FED 1 desvío, Δ probabilidad 2035 (pp)", 100),
           "dif_fed_2022_2023_p_noest_2035": ("H2: FED 2022-2023, Δ probabilidad 2035 (pp)", 100),
           "dif_fed_2022_2023_d2035": ("H2: FED 2022-2023, Δ deuda 2035 (pp PIB)", 1)}
    cols = {}
    for s, n in specs.items():
        t = pd.read_csv(TABLAS / f"fase25_{s}_resumen.csv", index_col=0)
        cols[n] = [f"{num(t.loc[k, 'media'] * f, 1)} [{num(t.loc[k, 'p05'] * f, 1)}; {num(t.loc[k, 'p95'] * f, 1)}]"
                   for k, (_, f) in ind.items()]
    d = pd.DataFrame(cols)
    d.insert(0, "Indicador", [v[0] for v in ind.values()])
    return ("## A.5 Resultados completos de la simulación por especificación\n\nMedia entre réplicas de parámetros y, entre corchetes, percentiles 5 y 95 (300 réplicas por 400 trayectorias).\n\n"
            + tabla(d) + "\n")


def main() -> None:
    texto = "# Apéndice estadístico\n\nTablas generadas con `codigo/modelos/apendice_tablas.py` a partir de los resultados de `fase24_svarx_1996_2025.py` y `fase25_simulacion_dsa_svarx.py`.\n\n"
    texto += seccion_descriptivos() + seccion_rezagos() + seccion_diagnosticos() + seccion_impacto() + seccion_fiscal() + seccion_robustez()
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"[OK] {SALIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
