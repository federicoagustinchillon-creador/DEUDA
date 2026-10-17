"""
empalme_embi_tcrm_1996_1998.py
==============================
Completa con fuentes oficiales y publicadas los trimestres de 1996-1998 en los que no hay dato
directo de dos variables del SVARX, y documenta la validacion de cada empalme.

1. EMBI (riesgo pais de J.P. Morgan para Argentina). La serie diaria publica empieza el
   11-12-1998 (Ambito Financiero). Para 1996T1-1998T3 se usa el diferencial entre la tasa de
   interes por prestamos interfinancieros en dolares hasta 15 dias del BCRA (serie oficial
   174.1_T_INTERUS_0_0_59 de datos.gob.ar, mensual desde octubre de 1994) y la tasa de fondos
   federales. Durante la convertibilidad, el costo del dolar en el sistema financiero argentino
   por encima de la tasa de Estados Unidos refleja el riesgo argentino. La relacion lineal
   EMBI = a + b * diferencial se estima en la superposicion 1998T4-2001T3 (el corralito de
   diciembre de 2001 rompe el mercado interbancario en dolares) y se valida con:
     - R2 y correlacion en la superposicion;
     - error cuadratico medio de validacion cruzada dejando uno afuera;
     - pronostico fuera de muestra de 2001T1-2001T3 estimando solo con 1998T4-2000T4.
2. TCRM (indice de tipo de cambio real multilateral del BCRA). La serie del BCRA empieza en enero
   de 1997. Para 1996 se encadena hacia atras con las variaciones del tipo de cambio real
   efectivo amplio de Argentina que publica el BIS (WS_EER, M.R.B.AR, mensual desde 1994). El
   indice del BIS sube cuando la moneda se aprecia y el del BCRA cuando se deprecia, de modo que
   se usa su inversa. Se valida con la correlacion de las variaciones trimestrales de ambos
   indices desde 1997.

Salidas:
  datos/crudos/empalmes/*.csv                      descargas originales
  datos/procesados/empalmes_1996_1998.csv          valores empalmados con su fuente
  resultados/tablas/empalmes_validacion.csv        estadisticos de validacion
  datos/dataset_consolidado_1996_2025.csv          EMBI y TCRM de 1996-1998 reemplazados, con
                                                   columnas EMBI_fuente y TCRM_fuente

Uso: python codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py
"""

from __future__ import annotations

import io
import json
import pathlib
import urllib.request

import numpy as np
import pandas as pd

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
DATOS = BASE / "datos"
CRUDOS = DATOS / "crudos" / "empalmes"
TABLAS = BASE / "resultados" / "tablas"
UA = {"User-Agent": "Mozilla/5.0"}
ID_INTERBANCARIA_USD = "174.1_T_INTERUS_0_0_59"
URL_BIS = "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_EER/1.0/M.R.B.AR?format=csv"
SUPERPOSICION = ("1998-12-31", "2001-09-30")


def descargar(url: str, accept: str = "*/*") -> bytes:
    req = urllib.request.Request(url, headers={**UA, "Accept": accept})
    return urllib.request.urlopen(req, timeout=120).read()


def tasa_interbancaria_usd() -> pd.Series:
    """Serie mensual oficial (datos.gob.ar), guardada en crudos."""
    url = f"https://apis.datos.gob.ar/series/api/series/?ids={ID_INTERBANCARIA_USD}&limit=5000&format=json"
    r = json.loads(descargar(url))
    s = pd.Series({pd.Timestamp(f): float(v) for f, v in r["data"] if v is not None}, name="tasa_interbancaria_usd")
    s.rename_axis("Date").to_csv(CRUDOS / "bcra_tasa_interbancaria_usd_mensual.csv")
    return s


def reer_bis() -> pd.Series:
    """Tipo de cambio real efectivo amplio de Argentina (BIS), mensual, guardado en crudos."""
    d = pd.read_csv(io.BytesIO(descargar(URL_BIS, "text/csv")))
    s = pd.Series(d["OBS_VALUE"].values, index=pd.to_datetime(d["TIME_PERIOD"]) + pd.offsets.MonthEnd(0), name="reer_bis")
    s = s.sort_index()
    s.rename_axis("Date").to_csv(CRUDOS / "bis_reer_amplio_argentina_mensual.csv")
    return s


def embi_diario() -> pd.Series:
    e = pd.read_csv(DATOS / "crudos" / "no_referenciados" / "embicsv.csv", sep=";", decimal=",")
    e["Fecha"] = pd.to_datetime(e["Fecha"], dayfirst=True)
    return e.set_index("Fecha")["Puntos"]


def trimestral(s: pd.Series) -> pd.Series:
    return s.resample("QE").mean()


def ajuste(x: pd.Series, y: pd.Series) -> tuple[float, float]:
    b, a = np.polyfit(x.values, y.values, 1)
    return float(a), float(b)


def main() -> None:
    CRUDOS.mkdir(parents=True, exist_ok=True)
    TABLAS.mkdir(parents=True, exist_ok=True)
    base = pd.read_csv(DATOS / "dataset_consolidado_1996_2025.csv", parse_dates=["Date"], index_col="Date")
    fed = pd.read_csv(DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv", parse_dates=["Date"], index_col="Date")["fedfunds"]

    # ---- EMBI
    dif = (trimestral(tasa_interbancaria_usd()) - fed) * 100  # puntos basicos
    embi = trimestral(embi_diario())
    z = pd.DataFrame({"dif": dif, "embi": embi}).loc[SUPERPOSICION[0]:SUPERPOSICION[1]].dropna()
    a, b = ajuste(z["dif"], z["embi"])
    r = float(np.corrcoef(z["dif"], z["embi"])[0, 1])
    loo = []
    for k in z.index:
        aa, bb = ajuste(z.drop(k)["dif"], z.drop(k)["embi"])
        loo.append(aa + bb * z.loc[k, "dif"] - z.loc[k, "embi"])
    ent, prueba = z.loc[:"2000-12-31"], z.loc["2001-01-01":]
    aa, bb = ajuste(ent["dif"], ent["embi"])
    pred = aa + bb * prueba["dif"]
    trims = pd.date_range("1996-03-31", "1998-09-30", freq="QE")
    embi_emp = (a + b * dif.reindex(trims)).rename("EMBI")

    # ---- TCRM
    reer = 1.0 / trimestral(reer_bis())  # inversa: sube con la depreciacion real, como el BCRA
    t_bcra = base["TCRM"]
    v = pd.DataFrame({"bis": np.log(reer).diff(), "bcra": np.log(t_bcra).diff()}).loc["1997-06-30":].dropna()
    v_conv = v.loc[:"2001-12-31"]
    r_tcrm, r_tcrm_conv = float(v["bis"].corr(v["bcra"])), float(v_conv["bis"].corr(v_conv["bcra"]))
    ancla = pd.Timestamp("1997-03-31")
    trims_t = pd.date_range("1996-03-31", "1996-12-31", freq="QE")
    tcrm_emp = (t_bcra.loc[ancla] * reer.reindex(trims_t) / reer.loc[ancla]).rename("TCRM")

    val = pd.DataFrame([
        {"empalme": "EMBI", "variable_puente": "tasa interbancaria en dolares (BCRA) menos tasa de fondos federales",
         "superposicion": "1998T4-2001T3", "n": len(z), "a": a, "b": b, "correlacion": r, "r2": r ** 2,
         "rmse_dejando_uno_afuera": float(np.sqrt(np.mean(np.square(loo)))), "desvio_embi_superposicion": float(z["embi"].std()),
         "fuera_de_muestra_2001_real": "; ".join(f"{x:.0f}" for x in prueba["embi"]),
         "fuera_de_muestra_2001_pronostico": "; ".join(f"{x:.0f}" for x in pred)},
        {"empalme": "TCRM", "variable_puente": "tipo de cambio real efectivo amplio de Argentina (BIS)",
         "superposicion": "1997T2-2025T4 (variaciones trimestrales)", "n": len(v), "correlacion": r_tcrm, "r2": r_tcrm ** 2,
         "correlacion_1997_2001": r_tcrm_conv, "n_1997_2001": len(v_conv)},
    ])
    val.to_csv(TABLAS / "empalmes_validacion.csv", index=False)

    emp = pd.concat([embi_emp, tcrm_emp], axis=1).rename_axis("Date")
    emp["EMBI_fuente"] = np.where(emp["EMBI"].notna(), "empalme con tasa interbancaria en dolares (BCRA)", None)
    emp["TCRM_fuente"] = np.where(emp["TCRM"].notna(), "empalme con tipo de cambio real efectivo del BIS", None)
    emp.to_csv(DATOS / "procesados" / "empalmes_1996_1998.csv")

    base.loc[embi_emp.index, "EMBI"] = embi_emp.values
    base.loc[tcrm_emp.index, "TCRM"] = tcrm_emp.values
    base["EMBI_fuente"] = "J.P. Morgan (serie diaria publicada por Ambito Financiero), promedio trimestral"
    base.loc[embi_emp.index, "EMBI_fuente"] = "empalme con tasa interbancaria en dolares (BCRA)"
    base["TCRM_fuente"] = "BCRA, indice de tipo de cambio real multilateral, promedio trimestral"
    base.loc[tcrm_emp.index, "TCRM_fuente"] = "empalme con tipo de cambio real efectivo del BIS"
    base.to_csv(DATOS / "dataset_consolidado_1996_2025.csv")

    pd.set_option("display.width", 200)
    print(val.T.to_string())
    print(pd.concat([emp[["EMBI", "TCRM"]], base.loc["1998-12-31":"1999-06-30", ["EMBI", "TCRM"]]]).round(3).to_string())


if __name__ == "__main__":
    main()
