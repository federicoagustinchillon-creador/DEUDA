"""
construir_resultado_primario_1996_2025.py
==========================================
Resultado primario del Sector Publico Nacional (SPN), base caja, trimestral
1996T1-2025T4, reconstruido desde fuente primaria (reemplaza al diccionario
PB_PIB_TRIM escrito a mano en ingesta_mecon_indec.py y al empalme de Denton
anual 1996-2003 de empalme_historico_pre2004.py).

Fuente primaria
---------------
Secretaria de Hacienda, Ministerio de Economia (MECON), Subsecretaria de
Programacion Macroeconomica: "Esquema Ahorro-Inversion-Financiamiento. Sector
Publico Nacional. Base Caja" (datos.gob.ar, API de series de tiempo, dataset 379),
frecuencia MENSUAL, tres tramos metodologicos (millones de ARS corrientes):

    1993-01..2006-12  Metodologia 1993-2006
        con rentas : 379.7_SUPERAVIT_006__28_65    ("Superavit primario")
        sin rentas : 379.7_RESULTADO_006__36_94    ("Resultado primario sin renta")
        rentas     : 379.7_ING_CORR_R006__42_86    (total rentas de la propiedad)
    2007-01..2014-12  Metodologia 2007-2014
        con rentas : 379.8_SUPERAVIT_014__28_7
        sin rentas : 379.8_RESULTADO_014__36_23
        rentas     : 379.8_ING_CORR_R014__42_59
    2015-01..2026-08  Metodologia 2017
        con rentas : 379.9_SUPERAVIT_017__23_94
        sin rentas : 379.9_RESULTADO_017__31_73
        rentas     : 379.9_ING_CORR_R017_I_0_M_37_10 (rentas de la propiedad netas)

Identidad verificada en codigo: con_rentas - sin_rentas == rentas de la
propiedad (error maximo reportado). "Rentas de la propiedad" agrega TODAS las
rentas del SPN (utilidades del BCRA, rentas del FGS-ANSES, intereses cobrados
por organismos, etc.); la API publica NO desglosa la transferencia de utilidades
del BCRA, de modo que "sin rentas" excluye mas que la serie del FMI (que excluye
solo las transferencias del BCRA). Ver informe.

Control cruzado 2016+: IMIG (Informe Mensual de Ingresos y Gastos del SPNF,
452.3_RESULTADO_RIO_0_M_18_54), distinta compilacion del mismo resultado.

Medida de flujo (decision documentada en el informe)
----------------------------------------------------
Denominador: PIB nominal de los ultimos 4 trimestres (pib_4t_mm, columna del
dataset de deuda consolidada; = suma de los 4 flujos trimestrales de INDEC).

    pb_pib      = 100 * (suma de los 4 ultimos resultados primarios trimestrales)
                        / pib_4t_mm                       [serie PRINCIPAL]
    pb_pib_trim = 100 * 4 * PB_trimestre / pib_4t_mm      [alternativa, anualizada]

La principal usa la suma movil de 4 trimestres porque (i) el resultado primario
SPN tiene fuerte estacionalidad (aguinaldo en T2/T4, ingresos de Ganancias en T2),
(ii) es el numerador homologo del denominador 4T usado en la razon deuda/PIB y por
lo tanto consistente con la dinamica d_t - d_{t-1} de la identidad de deuda, y
(iii) coincide con la definicion anual del FMI en los T4. Costo: por construccion
es una media movil MA(3) de flujos trimestrales (autocorrelacion inducida), por lo
que se entrega tambien la alternativa anualizada sin superposicion como robustez.

Uso:  python codigo/ingesta_datos/construir_resultado_primario_1996_2025.py
"""
from __future__ import annotations

import io
import pathlib
import re
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import requests

BASE = pathlib.Path(__file__).resolve().parents[2]
RAW_DIR = BASE / "datos" / "crudos" / "resultado_primario"
PROC = BASE / "datos" / "procesados"
OUT_CSV = PROC / "resultado_primario_1996_2025.csv"
OUT_CTRL = PROC / "resultado_primario_1996_2025_control.csv"
GDP_CSV = PROC / "deuda_consolidada_1996_2025.csv"
OLD_POST = BASE / "datos" / "dataset_consolidado_real.csv"        # pb_pib 2004+ (diccionario manual)
OLD_PRE = BASE / "datos" / "empalme_pre2004_deuda_pb.csv"         # pb_pib 1996-2003 (Denton anual)
IMF_PDF = BASE / "Bibliografia" / "descargas_verificacion" / "1argea2025002-print-pdf.pdf"
SERIES_API = "https://apis.datos.gob.ar/series/api/series/"

# IDs de serie (datos.gob.ar). Tramo -> (con rentas, sin rentas, rentas, ultimo mes usable)
SERIES: Dict[str, Dict[str, str]] = {
    "met_1993_2006": {"con": "379.7_SUPERAVIT_006__28_65", "sin": "379.7_RESULTADO_006__36_94",
                      "rentas": "379.7_ING_CORR_R006__42_86"},
    "met_2007_2014": {"con": "379.8_SUPERAVIT_014__28_7", "sin": "379.8_RESULTADO_014__36_23",
                      "rentas": "379.8_ING_CORR_R014__42_59"},
    "met_2017": {"con": "379.9_SUPERAVIT_017__23_94", "sin": "379.9_RESULTADO_017__31_73",
                 "rentas": "379.9_ING_CORR_R017_I_0_M_37_10"},
}
ID_IMIG = "452.3_RESULTADO_RIO_0_M_18_54"
START, END = "1996-03-31", "2025-12-31"


def fetch_series(series_id: str) -> pd.Series:
    """Serie mensual de datos.gob.ar (millones ARS), con cache en crudos.

    Si la API falla se usa el crudo guardado; si no existe, se aborta (no se aproxima).
    """
    path = RAW_DIR / f"{series_id}.csv"
    try:
        r = requests.get(SERIES_API, params={"ids": series_id, "format": "csv", "limit": 1000}, timeout=60)
        r.raise_for_status()
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(r.text, encoding="utf-8")
        text = r.text
    except Exception as err:  # noqa: BLE001
        if not path.exists():
            raise RuntimeError(f"Fuente inaccesible y sin cache: {series_id}") from err
        print(f"[WARN] API inaccesible ({err}); crudo guardado {path.name}")
        text = path.read_text(encoding="utf-8")
    df = pd.read_csv(io.StringIO(text), index_col=0, parse_dates=True)
    s = df.iloc[:, 0].astype(float)
    s.index = s.index.to_period("M")
    return s


def monthly_spn() -> pd.DataFrame:
    """Concatena los tres tramos metodologicos (mensual, millones ARS).

    Columnas: con_rentas, sin_rentas, rentas, metodologia. Valida la identidad
    con - sin == rentas dentro de cada tramo y devuelve el error maximo en attrs.
    """
    parts: List[pd.DataFrame] = []
    max_err = 0.0
    for met, ids in SERIES.items():
        con, sin, ren = (fetch_series(ids[k]) for k in ("con", "sin", "rentas"))
        d = pd.concat({"con_rentas": con, "sin_rentas_pub": sin, "rentas": ren}, axis=1)
        d = d.dropna(subset=["con_rentas", "rentas"])
        # La serie publicada "sin rentas" tiene huecos en 1993-2006 (62 meses); donde falta se
        # deriva por identidad (con - rentas). Donde existe se usa la publicada y se mide la
        # discrepancia contra la identidad (maxima en el tramo 2017: rentas "netas").
        ident = d["con_rentas"] - d["rentas"]
        err = float((ident - d["sin_rentas_pub"]).abs().max())
        d["sin_rentas"] = d["sin_rentas_pub"].fillna(ident)
        d["sin_rentas_derivada"] = d["sin_rentas_pub"].isna().astype(int)
        d = d.drop(columns="sin_rentas_pub")
        max_err = max(max_err, err)
        d["metodologia"] = met
        parts.append(d)
    out = pd.concat(parts).sort_index()
    if out.index.has_duplicates:
        raise RuntimeError("Meses duplicados entre tramos metodologicos")
    out.attrs["max_err_identidad"] = max_err
    return out


def to_quarterly(m: pd.DataFrame) -> pd.DataFrame:
    """Suma mensual -> trimestral exigiendo los 3 meses; fin de trimestre como indice."""
    q = m[["con_rentas", "sin_rentas", "rentas"]].copy()
    q["n"] = 1
    g = q.groupby(q.index.asfreq("Q")).sum()
    g = g[g["n"] == 3].drop(columns="n")
    met = m["metodologia"].groupby(m.index.asfreq("Q")).agg(lambda x: "/".join(sorted(set(x))))
    g["metodologia"] = met.reindex(g.index)
    g.index = g.index.to_timestamp("Q").normalize()
    return g


def imf_table_3b() -> pd.DataFrame:
    """Lee del PDF local (FMI CR 25/95, Table 3b) 'Primary Balance' y 'BCRA transfers'.

    Devuelve DataFrame index 2023..2030 (% PIB, gobierno federal). El texto se parsea
    por regex; si el formato cambia se levanta error (no hay valores tipeados).
    """
    import pypdf  # import local: solo para el control

    rd = pypdf.PdfReader(str(IMF_PDF))
    txt = ""
    for p in rd.pages:
        t = p.extract_text() or ""
        if "Table 3b" in t and "Primary Balance" in t:
            txt = t
            break
    if not txt:
        raise RuntimeError("Tabla 3b no encontrada en el PDF del FMI")
    head = re.search(r"Table 3b.*?\n\s*\n?\s*(?:\n)?\s*((?:20\d\d\s*){6,8})", txt, flags=re.S)
    years = [int(y) for y in re.findall(r"20\d\d", head.group(1))] if head else list(range(2023, 2031))

    def row(label: str) -> List[float]:
        m = re.search(label + r"[^\n]*?((?:-?\d+\s?\.\s?\d\s*){%d})" % len(years), txt)
        if not m:
            raise RuntimeError(f"Fila '{label}' no encontrada")
        return [float(x.replace(" ", "")) for x in re.findall(r"-?\d+\s?\.\s?\d", m.group(1))]

    return pd.DataFrame({"pb_federal_fmi": row(r"Primary Balance"),
                         "transf_bcra_fmi": row(r"of which: BCRA transfers 9/")}, index=years)


def main() -> None:
    m = monthly_spn()
    q = to_quarterly(m)
    gdp = pd.read_csv(GDP_CSV, index_col=0, parse_dates=True)[["pib_4t_mm", "pib_anualizado_mm"]]
    idx = pd.date_range(START, END, freq="QE").normalize()
    # Necesitamos 3 trimestres previos a 1996T1 para la suma movil: vienen de la misma fuente (1995)
    q = q.reindex(pd.date_range(q.index.min(), END, freq="QE").normalize())
    if q.loc[:END, ["con_rentas", "sin_rentas"]].isna().any().any():
        faltan = q.index[q[["con_rentas", "sin_rentas"]].isna().any(axis=1)]
        raise RuntimeError(f"Trimestres sin 3 meses de dato: {list(faltan.date)}")

    df = pd.DataFrame(index=idx)
    df["pib_4t_mm"] = gdp["pib_4t_mm"].reindex(idx)
    for suf, col in (("", "con_rentas"), ("_sin_rentas", "sin_rentas")):
        df[f"pb_trim_ars_mm{suf}"] = q[col].reindex(idx)
        roll = q[col].rolling(4).sum().reindex(idx)
        df[f"pb_4t_ars_mm{suf}"] = roll
        df[f"pb_pib{suf}"] = roll / df["pib_4t_mm"] * 100.0
        df[f"pb_pib_trim{suf}"] = 4.0 * df[f"pb_trim_ars_mm{suf}"] / df["pib_4t_mm"] * 100.0
    df["rentas_pib"] = df["pb_pib"] - df["pb_pib_sin_rentas"]
    df["metodologia"] = q["metodologia"].reindex(idx)
    df["fuente"] = "MECON_AIF_SPN_base_caja_datos.gob.ar_dataset379"
    df["flag_pre2004_mensual_primario"] = (df.index < "2004-01-01").astype(int)

    # --- control cruzado IMIG (2016+): misma variable, otra compilacion (SPNF IMIG) ---
    imig = fetch_series(ID_IMIG)
    qi = imig.groupby(imig.index.asfreq("Q")).agg(["sum", "count"])
    qi = qi[qi["count"] == 3]["sum"]
    qi.index = qi.index.to_timestamp("Q").normalize()
    df["pb_trim_imig_ars_mm"] = qi.reindex(idx)
    df["dif_aif_vs_imig_pct_pib"] = (df["pb_trim_ars_mm"] - df["pb_trim_imig_ars_mm"]) * 4 / df["pib_4t_mm"] * 100

    PROC.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, float_format="%.6f")
    print(f"[OK] {OUT_CSV} ({len(df)} trimestres) | identidad con-sin=rentas, error max = "
          f"{m.attrs['max_err_identidad']:.3e} mm ARS")

    # --- comparacion contra series previas y FMI ---
    old_post = pd.read_csv(OLD_POST, index_col=0, parse_dates=True)["pb_pib"]
    old_pre = pd.read_csv(OLD_PRE, index_col=0, parse_dates=True)["pb_pib"]
    old = pd.concat([old_pre[old_pre.index < "2004-01-01"], old_post]).reindex(idx)
    cmp_ = pd.DataFrame({"viejo": old, "nuevo_con_rentas": df["pb_pib"], "nuevo_sin_rentas": df["pb_pib_sin_rentas"]})
    cmp_["dif"] = cmp_["nuevo_con_rentas"] - cmp_["viejo"]
    print("\nViejo vs nuevo (pb_pib, % PIB 4T): correlacion y diferencia absoluta")
    for lab, sl in (("1996-2003", slice("1996", "2003")), ("2004-2025", slice("2004", "2025"))):
        c = cmp_.loc[sl]
        print(f"  {lab}: corr={c['viejo'].corr(c['nuevo_con_rentas']):.3f}  "
              f"MAE={c['dif'].abs().mean():.2f} pp  max|dif|={c['dif'].abs().max():.2f} pp")

    imf = imf_table_3b()
    rows: List[dict] = []
    for y in (2023, 2024):
        t = pd.Timestamp(f"{y}-12-31")
        rows.append({
            "anio": y,
            "nuevo_con_rentas": df.loc[t, "pb_pib"],
            "nuevo_sin_rentas": df.loc[t, "pb_pib_sin_rentas"],
            "nuevo_con_rentas_menos_transf_bcra_fmi": df.loc[t, "pb_pib"] - imf.loc[y, "transf_bcra_fmi"],
            "rentas_pib": df.loc[t, "rentas_pib"],
            "viejo_dic": cmp_.loc[t, "viejo"],
            "fmi_federal_cr2595": imf.loc[y, "pb_federal_fmi"],
            "fmi_transf_bcra": imf.loc[y, "transf_bcra_fmi"],
        })
    ctrl = pd.DataFrame(rows).set_index("anio").round(2)
    ctrl.to_csv(OUT_CTRL)
    print("\nControl FMI (CR 25/95 Tabla 3b, gobierno federal, % PIB):")
    print(ctrl.T.to_string())
    brk = df.loc[["2006-12-31", "2007-03-31", "2014-12-31", "2015-03-31"], ["pb_trim_ars_mm", "pb_pib", "metodologia"]]
    print("\nEmpalmes metodologicos:\n", brk.to_string())
    d = df["dif_aif_vs_imig_pct_pib"].dropna()
    print(f"\nAIF vs IMIG (2016+, pp PIB anualizado): n={len(d)} media={d.mean():.3f} max|dif|={d.abs().max():.3f}")


if __name__ == "__main__":
    main()
