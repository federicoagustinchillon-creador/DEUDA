"""
construir_deuda_consolidada_1996_2025.py
=========================================
Serie trimestral 1996T1-2025T4 de deuda publica consolidada de Argentina:

    deuda_consolidada_pib_t = deuda_spnf_pib_t + pasivos_bcra_pib_t

con UN solo denominador para ambos terminos (ver informe_deuda_consolidada_v1.md):

    PIB4T_t = (1/4) * sum_{j=0..3} Y_{t-j},   Y = PIB nominal trimestral anualizado

Como la serie de INDEC esta expresada a tasa anual (el promedio de los cuatro
trimestres de un anio reproduce exactamente el PIB anual del mismo dataset),
PIB4T_t equivale a la suma de los cuatro ultimos flujos trimestrales: es el PIB
nominal de los ultimos 4 trimestres, y en el cuarto trimestre coincide con el
"PIB promedio del periodo" que usa el FMI (CR 25/95, Annex II, Table 2).

Fuentes (todas reales, descargadas o leidas de archivos del repo):
  * PIB nominal 2004T1+: datos.gob.ar / INDEC, serie 4.4_OGP_2004_T_17
    (PIB a precios de comprador, millones de pesos corrientes, base 2004).
  * PIB nominal 1993T1-2013T3: datos.gob.ar / INDEC, serie 2.4_OGP_1993_T_17
    (base 1993). Empalme por coeficiente de enlace sobre 2004 (cuatro
    trimestres solapados, razon de medias), retropolando 1993-2003.
  * Pasivos remunerados BCRA: API BCRA v4.0, idVariable 1258 (LEBAC/NOBAC),
    1260 (LELIQ/NOTALIQ), 1261 (posicion neta de pases), en millones de ARS.
  * Deuda bruta SPN/Administracion Central en USD: MECON, Informe de Deuda
    Publica al 31/12/2025, hoja A.4.5 (serie trimestral por residencia del
    tenedor, 1998T1-2025T4; 1994-1997 solo cierre de diciembre) y tipo de
    cambio de fin de trimestre de la hoja A.2.4 (U$S/Peso). Antes de 2002 la
    paridad legal era 1 ARS = 1 USD (Ley 23.928); no se asume otra cosa.

Salida: datos/procesados/deuda_consolidada_1996_2025.csv
        datos/procesados/deuda_consolidada_1996_2025_control_fmi.csv
        resultados/figuras_borrador/deuda_consolidada_1996_2025.png
"""

from __future__ import annotations

import pathlib
import time
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import requests

BASE = pathlib.Path(__file__).resolve().parents[2]
RAW_DIR = BASE / "datos" / "crudos" / "deuda_consolidada_1996"
OUT_CSV = BASE / "datos" / "procesados" / "deuda_consolidada_1996_2025.csv"
OUT_CTRL = BASE / "datos" / "procesados" / "deuda_consolidada_1996_2025_control_fmi.csv"
OUT_FIG = BASE / "resultados" / "figuras_borrador" / "deuda_consolidada_1996_2025.png"
MECON_2025 = BASE / "datos" / "crudos" / "mecon_deuda" / "deuda_publica_31-12-2025.xlsx"

SERIES_API = "https://apis.datos.gob.ar/series/api/series"
GDP_ID_04 = "4.4_OGP_2004_T_17"
GDP_ID_93 = "2.4_OGP_1993_T_17"
BCRA_BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias"
BCRA_IDS: Dict[str, int] = {"lebac_nobac": 1258, "leliq_notaliq": 1260, "pases_neto": 1261}
HEADERS = {"User-Agent": "Mozilla/5.0"}


# ---------------------------------------------------------------------------
# Descargas con cache (si la API falla se usa el crudo guardado; si no hay, error)
# ---------------------------------------------------------------------------
def _cache_or_raise(path: pathlib.Path, err: Exception) -> pd.DataFrame:
    """Devuelve el crudo cacheado o relanza el error original (sin aproximar)."""
    if path.exists():
        print(f"[WARN] API inaccesible ({err}); se usa crudo guardado {path.name}")
        return pd.read_csv(path, index_col=0, parse_dates=True)
    raise RuntimeError(f"Fuente inaccesible y sin cache: {path.name}") from err


def fetch_gdp(series_id: str) -> pd.Series:
    """PIB nominal trimestral (millones ARS, tasa anual) de datos.gob.ar."""
    path = RAW_DIR / f"{series_id}.csv"
    try:
        r = requests.get(SERIES_API, params={"ids": series_id, "limit": 1000, "format": "json"}, timeout=40)
        r.raise_for_status()
        df = pd.DataFrame(r.json()["data"], columns=["fecha", "valor"])
        df["fecha"] = pd.to_datetime(df["fecha"])
        df = df.set_index("fecha").dropna()
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(path)
    except Exception as err:  # noqa: BLE001 - se reporta y se usa cache o se aborta
        df = _cache_or_raise(path, err)
    s = df["valor"].astype(float)
    s.index = s.index.to_period("Q").to_timestamp("Q").normalize()
    return s


def build_gdp() -> pd.DataFrame:
    """Empalma base 1993 con base 2004. Devuelve Y (anualizado), PIB4T y origen."""
    y04 = fetch_gdp(GDP_ID_04)
    y93 = fetch_gdp(GDP_ID_93)
    solap = y04.index.intersection(y93.index)
    ref = solap[(solap >= "2004-01-01") & (solap <= "2004-12-31")]
    if len(ref) != 4:
        raise RuntimeError("No hay 4 trimestres solapados en 2004 para el enlace")
    link = y04.loc[ref].mean() / y93.loc[ref].mean()
    pre = y93[y93.index < y04.index.min()] * link
    y = pd.concat([pre, y04]).sort_index()
    origen = pd.Series("base2004_INDEC", index=y.index)
    origen[y.index < y04.index.min()] = "base1993_empalmada"
    out = pd.DataFrame({"pib_anualizado_mm": y, "pib_origen": origen})
    out["pib_4t_mm"] = y.rolling(4).mean()
    out.attrs["link"] = float(link)
    return out


def fetch_bcra(id_variable: int, desde: str, hasta: str) -> pd.Series:
    """Serie diaria BCRA v4.0 (millones ARS) con paginacion; cache en crudos."""
    path = RAW_DIR / f"bcra_{id_variable}.csv"
    try:
        rows: List[dict] = []
        offset = 0
        while True:
            r = requests.get(f"{BCRA_BASE}/{id_variable}", headers=HEADERS, timeout=40,
                             params={"desde": desde, "hasta": hasta, "limit": 3000, "offset": offset})
            r.raise_for_status()
            p = r.json()
            det = p["results"][0].get("detalle", []) if p.get("results") else []
            rows.extend(det)
            count = p.get("metadata", {}).get("resultset", {}).get("count", 0)
            offset += 3000
            if not det or offset >= count:
                break
            time.sleep(0.2)
        df = pd.DataFrame(rows, columns=["fecha", "valor"])
        if len(df):
            df["fecha"] = pd.to_datetime(df["fecha"])
            df = df.drop_duplicates("fecha", keep="last").set_index("fecha").sort_index()
        else:
            df = pd.DataFrame({"valor": pd.Series(dtype=float)})
            df.index.name = "fecha"
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(path)
    except Exception as err:  # noqa: BLE001
        df = _cache_or_raise(path, err)
    return df["valor"].astype(float)


def build_bcra(idx: pd.DatetimeIndex) -> pd.DataFrame:
    """Stock de fin de trimestre de cada componente. Cero SOLO si la API confirma
    que no hay registros hasta esa fecha (respuesta valida, primera obs. posterior);
    la bandera `*_sin_serie` queda en 1 en esos trimestres."""
    out = pd.DataFrame(index=idx)
    for label, vid in BCRA_IDS.items():
        s = fetch_bcra(vid, "1996-01-01", "2025-12-31")
        first = s.index.min() if len(s) else pd.NaT
        print(f"[BCRA] {label} (id {vid}): {len(s)} obs, primera={first}, ultima={s.index.max() if len(s) else None}")
        q = s.resample("QE").last().ffill()
        q.index = q.index.to_period("Q").to_timestamp("Q").normalize()
        col = q.reindex(idx)
        sin = col.isna()
        out[label] = col.fillna(0.0)
        out[f"{label}_sin_serie"] = sin.astype(int)
    out["pasivos_bcra_ars_mm"] = out[list(BCRA_IDS)].sum(axis=1)
    return out


# ---------------------------------------------------------------------------
# MECON: deuda bruta en USD (A.4.5) y tipo de cambio (A.2.4)
# ---------------------------------------------------------------------------
def read_mecon_debt_usd() -> pd.DataFrame:
    """Hoja A.4.5: deuda bruta total (miles de millones USD) por fecha."""
    d = pd.read_excel(MECON_2025, sheet_name="A.4.5", header=None)
    hdr = d.index[d[1].astype(str).str.contains("Per", na=False) & d[2].astype(str).str.contains("Total", na=False)][0]
    body = d.iloc[hdr + 1:, 1:3].copy()
    body.columns = ["fecha", "total_mmusd"]
    body = body[pd.to_numeric(body["total_mmusd"], errors="coerce").notna()]
    body["fecha"] = pd.to_datetime(body["fecha"], errors="coerce")
    body = body.dropna(subset=["fecha"])
    body["total_mmusd"] = body["total_mmusd"].astype(float)
    body["fecha"] = body["fecha"].dt.to_period("Q").dt.to_timestamp("Q").dt.normalize()
    return body.drop_duplicates("fecha", keep="last").set_index("fecha")


def read_mecon_fx() -> pd.Series:
    """Hoja A.2.4: ARS por USD a fin de trimestre (la hoja trae U$S/Peso).
    Una fila fuera de secuencia (fecha 2022-03-31 entre 2002-02 y 2002-06,
    CER 1.0481) es un error de tipeo del MECON y se reasigna a 2002-03-31; se
    detecta porque 2022-03-31 aparece dos veces."""
    d = pd.read_excel(MECON_2025, sheet_name="A.2.4", header=None)
    body = d.iloc[9:, [1, 4]].copy()
    body.columns = ["fecha", "fx"]
    body["fx"] = pd.to_numeric(body["fx"], errors="coerce")
    body["fecha"] = pd.to_datetime(body["fecha"], errors="coerce")
    body = body.dropna()
    dup = body["fecha"].duplicated(keep=False)
    if dup.any():
        first_pos = body.index[dup][0]
        body.loc[first_pos, "fecha"] = body.loc[first_pos, "fecha"] - pd.DateOffset(years=20)
    body["fecha"] = body["fecha"].dt.to_period("Q").dt.to_timestamp("Q").dt.normalize()
    return body.drop_duplicates("fecha", keep="last").set_index("fecha")["fx"]


def build_spnf(idx: pd.DatetimeIndex) -> pd.DataFrame:
    """Stock en ARS de la deuda bruta. 1996-1997: solo hay cierre de diciembre en
    A.4.5, los trimestres intermedios se interpolan linealmente en USD (flag)."""
    usd = read_mecon_debt_usd()["total_mmusd"] * 1000.0  # millones USD
    fx = read_mecon_fx()
    s = usd.reindex(idx)
    origen = pd.Series("informe_trimestral", index=idx)
    faltan = s.isna()
    # interpolacion lineal solo dentro del rango cubierto por cierres de diciembre
    full = usd.reindex(usd.index.union(idx)).sort_index().interpolate(method="time", limit_area="inside")
    s = full.reindex(idx)
    origen[faltan & s.notna()] = "interpolado_lineal_usd"
    origen[s.isna()] = "sin_dato"
    tc = pd.Series(np.nan, index=idx)
    pre = idx < pd.Timestamp("2002-01-01")
    tc[pre] = 1.0
    tc[~pre] = fx.reindex(idx[~pre])
    out = pd.DataFrame({"spnf_usd_mm": s, "tc_ars_usd": tc, "spnf_origen": origen,
                        "tc_origen": np.where(pre, "paridad_legal_ley_23928", "MECON_A.2.4")})
    out["deuda_spnf_ars_mm"] = out["spnf_usd_mm"] * out["tc_ars_usd"]
    return out


def read_peso_shares() -> pd.Series:
    """Participacion de la moneda local (pesos, incl. CER) en la deuda bruta al
    cierre de diciembre, de los informes MECON disponibles en datos/crudos/mecon_deuda
    (2007-2009: hoja A.7 fila '1. Peso Argentino'; 2013-2025: hoja 'POR MONEDA' fila
    'Moneda local'). Cociente local/total de la MISMA tabla. No hay dato para
    2010-2012 (informes no descargados) ni para fechas distintas de diciembre."""
    import re
    out: Dict[pd.Timestamp, float] = {}
    for f in sorted((BASE / "datos" / "crudos" / "mecon_deuda").glob("deuda_publica_31-12-*.xls*")):
        year = int(re.search(r"31-12-(\d{4})", f.name).group(1))
        x = pd.ExcelFile(f)
        for sh in x.sheet_names[1:]:
            d = x.parse(sh, header=None)
            head = " ".join(str(v) for v in d.iloc[:14, 1].dropna())
            if not re.search(r"POR MONEDA|^Moneda", head, re.I):
                continue
            lab = d[1].astype(str)
            tot = d.index[lab.str.match(r"\s*(TOTAL)", case=False)]
            loc = d.index[lab.str.match(r"\s*(Moneda local|1\. Peso Argentino)", case=False)]
            if len(tot) and len(loc):
                t = pd.to_numeric(d.loc[tot[0], 2], errors="coerce")
                l = pd.to_numeric(d.loc[loc[0], 2], errors="coerce")
                if pd.notna(t) and pd.notna(l) and t > 0:
                    out[pd.Timestamp(year=year, month=12, day=31)] = float(l / t)
                    break
    return pd.Series(out, name="share_pesos_spnf")


def main() -> None:
    gdp = build_gdp()
    print(f"[PIB] coeficiente de enlace base2004/base1993 (2004) = {gdp.attrs['link']:.4f}")
    idx = pd.date_range("1996-03-31", "2025-12-31", freq="QE").normalize()
    idx.name = "Date"
    df = pd.concat([gdp.reindex(idx), build_bcra(idx), build_spnf(idx)], axis=1)
    df["deuda_spnf_pib"] = df["deuda_spnf_ars_mm"] / df["pib_4t_mm"] * 100
    df["pasivos_bcra_pib"] = df["pasivos_bcra_ars_mm"] / df["pib_4t_mm"] * 100
    df["deuda_consolidada_pib"] = df["deuda_spnf_pib"] + df["pasivos_bcra_pib"]
    sh = read_peso_shares().reindex(idx)
    df["share_pesos_spnf_dic"] = sh
    df["share_pesos_consolidada_dic"] = (sh * df["deuda_spnf_ars_mm"] + df["pasivos_bcra_ars_mm"]) / (
        df["deuda_spnf_ars_mm"] + df["pasivos_bcra_ars_mm"])
    df["pasivos_bcra_neto_negativo"] = (df["pasivos_bcra_ars_mm"] < 0).astype(int)
    df["denominador_tipo"] = "PIB_nominal_ultimos_4_trimestres"
    # referencia: ratio contra PIB anualizado del trimestre (lo que usaba ingesta_bcra_pasivos)
    df["pasivos_bcra_pib_pib_anualizado_t"] = df["pasivos_bcra_ars_mm"] / df["pib_anualizado_mm"] * 100
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = ["deuda_spnf_pib", "pasivos_bcra_pib", "deuda_consolidada_pib", "denominador_tipo",
            "pib_4t_mm", "pib_anualizado_mm", "pib_origen", "deuda_spnf_ars_mm", "spnf_usd_mm",
            "tc_ars_usd", "tc_origen", "spnf_origen", "pasivos_bcra_ars_mm", "lebac_nobac",
            "leliq_notaliq", "pases_neto", "lebac_nobac_sin_serie", "leliq_notaliq_sin_serie",
            "pases_neto_sin_serie", "pasivos_bcra_neto_negativo", "share_pesos_spnf_dic",
            "share_pesos_consolidada_dic", "pasivos_bcra_pib_pib_anualizado_t"]
    df[cols].round(6).to_csv(OUT_CSV, float_format="%.6f")
    print(f"[OK] {OUT_CSV} ({len(df)} trimestres)")
    print(df.loc[["2023-12-31", "2024-12-31"], ["deuda_spnf_pib", "pasivos_bcra_pib", "deuda_consolidada_pib",
                                                "pasivos_bcra_pib_pib_anualizado_t"]].round(2).to_string())

    # --- control vs FMI CR 25/95 Annex II Table 2 (valores transcriptos del PDF) ---
    fmi = pd.DataFrame({"bruta_federal": [155.4, 85.3], "bcra": [18.4, 2.2], "consolidada_neta": [110.8, 51.5]},
                       index=pd.to_datetime(["2023-12-31", "2024-12-31"]))
    ctrl = pd.DataFrame({
        "spnf_bruta_nuestra": df.loc[fmi.index, "deuda_spnf_pib"], "spnf_bruta_fmi": fmi["bruta_federal"],
        "bcra_nuestra": df.loc[fmi.index, "pasivos_bcra_pib"], "bcra_fmi": fmi["bcra"],
        "bcra_nuestra_pib_anualizado_Q4": df.loc[fmi.index, "pasivos_bcra_pib_pib_anualizado_t"],
        "consolidada_bruta_nuestra": df.loc[fmi.index, "deuda_consolidada_pib"],
        "consolidada_neta_fmi": fmi["consolidada_neta"]})
    ctrl.round(2).to_csv(OUT_CTRL)
    print(ctrl.round(2).T.to_string())

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.stackplot(df.index, df["deuda_spnf_pib"], df["pasivos_bcra_pib"].fillna(0),
                 labels=["Deuda bruta SPN (MECON)", "Pasivos remunerados BCRA"],
                 colors=["#1f3b5c", "#c8793a"], alpha=0.9)
    ax.set_ylabel("% del PIB nominal de los ultimos 4 trimestres")
    ax.set_title("Deuda publica consolidada bruta, 1996T1-2025T4")
    ax.legend(loc="upper left", frameon=False)
    ax.grid(alpha=0.25)
    fig.text(0.01, 0.01, "Fuentes: MECON (A.4.5, A.2.4), BCRA API v4.0 (1258/1260/1261), INDEC (datos.gob.ar). "
             "Concepto bruto, sin neteo de tenencias intra-sector publico.", fontsize=7)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT_FIG, dpi=200)
    print(f"[OK] {OUT_FIG}")


if __name__ == "__main__":
    main()
