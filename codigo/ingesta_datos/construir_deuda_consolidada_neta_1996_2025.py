"""
construir_deuda_consolidada_neta_1996_2025.py
==============================================
Serie trimestral 1996T1-2025T4 de deuda publica CONSOLIDADA NETA de Argentina,
lo mas cerca posible de la definicion del FMI (CR 25/95, Annex II, Table 2;
FMI 2021, "Review of the DSF for MACs", Annex II, nota 2):

    D_neta_t = ( B_t - T^BCRA_t - T^FGS_t + L^BCRA_t - DEP_t ) / PIB4T_t * 100

    B      deuda bruta federal (MECON A.4.5 en USD x TC)           [reuso v1]
    T^BCRA deuda del Tesoro en poder del BCRA: letras intransferibles,
           titulos publicos, adelantos transitorios, letras en USD
           (BCRA, Balance del Banco Central, balbcrhis.xls, col. "Sector
           oficial - Total" = pesos + moneda extranjera)
    T^FGS  deuda del Tesoro en poder del FGS-ANSES. SIN FUENTE PRIMARIA
           ACCESIBLE: queda como faltante (NaN) y se marca; la serie "neta"
           resultante es "neta excepto FGS" (cota superior de la neta FMI).
    L^BCRA pasivos remunerados del BCRA: LEBAC/NOBAC + LELIQ/NOTALIQ + pases
           netos (API BCRA v4.0 ids 1258, 1260, 1261; reuso v1) en pesos, mas
           letras en moneda extranjera LEBAC-USD/LEDIV/BOPREAL (id 1259).
           Swap PBoC activado: sin serie publica -> faltante, no se aproxima.
    DEP    depositos del Gobierno Nacional en el BCRA (API v4.0 id 1264).

Denominador: PIB nominal de los ultimos 4 trimestres (reuso de
construir_deuda_consolidada_1996_2025.build_gdp). Todos los stocks son de
fin de trimestre, en millones de ARS corrientes.

Uso:  python codigo/ingesta_datos/construir_deuda_consolidada_neta_1996_2025.py
"""
from __future__ import annotations

import pathlib
import sys
from typing import Dict, List

import numpy as np
import pandas as pd
import requests

BASE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import construir_deuda_consolidada_1996_2025 as v1  # noqa: E402  (reuso de PIB, bruta, BCRA pesos)

RAW_NETA = BASE / "datos" / "crudos" / "deuda_consolidada_neta"
BAL_XLS = RAW_NETA / "balbcrhis.xls"
BAL_URL = "https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/balbcrhis.xls"
OUT_CSV = BASE / "datos" / "procesados" / "deuda_consolidada_neta_1996_2025.csv"
OUT_CTRL = BASE / "datos" / "procesados" / "deuda_consolidada_neta_1996_2025_control_fmi.csv"
OUT_FIG = BASE / "resultados" / "figuras_borrador" / "deuda_consolidada_neta_1996_2025.png"
SPNF_CSV = BASE / "datos" / "procesados" / "financiero_trimestral.csv"

ID_DEP_GOB = 1264   # Depositos del gobierno en el BCRA (millones ARS)
ID_LETRAS_FX = 1259  # LEBAC/LEDIV/BOPREAL en moneda extranjera, valuadas en ARS (millones)
MESES: Dict[str, int] = {"Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, "Jun": 6,
                         "Jul": 7, "Ago": 8, "Set": 9, "Oct": 10, "Nov": 11, "Dic": 12}

# Control FMI CR 25/95 Annex II Table 2 (% PIB; transcripto del PDF local)
FMI: Dict[str, Dict[str, float]] = {
    "2023-12-31": {"federal_sin_intra": 92.9, "intra_publico_tesoro": 62.5, "bruta_total": 155.4,
                   "bcra_pasivos": 18.4, "bcra_fx": 2.1, "bcra_lc": 16.2, "dep_tesoro_bcra": 0.5, "neta": 110.8},
    "2024-12-31": {"federal_sin_intra": 51.4, "intra_publico_tesoro": 33.9, "bruta_total": 85.3,
                   "bcra_pasivos": 2.2, "bcra_fx": 2.1, "bcra_lc": 0.0, "dep_tesoro_bcra": 2.1, "neta": 51.5},
}


def download_balance() -> pathlib.Path:
    """Descarga el Balance historico del BCRA si no esta en cache; error si falla."""
    if BAL_XLS.exists():
        return BAL_XLS
    RAW_NETA.mkdir(parents=True, exist_ok=True)
    r = requests.get(BAL_URL, headers=v1.HEADERS, timeout=60)
    r.raise_for_status()
    BAL_XLS.write_bytes(r.content)
    return BAL_XLS


def read_bcra_holdings(idx: pd.DatetimeIndex) -> pd.DataFrame:
    """Credito del BCRA al Tesoro (balbcrhis.xls, hoja B.C.R.A., miles de ARS).

    Columnas (indice 0-based): 12 = Sector oficial Total; 13 = en moneda
    nacional Total; 14 = Gobierno Nacional Total (15 adelantos transitorios,
    16 titulos publicos); 20 = en moneda extranjera Total (letras
    intransferibles/titulos en USD). Se valida col12 == col13 + col20.
    Devuelve millones ARS al cierre de cada trimestre de ``idx``.
    """
    d = pd.read_excel(download_balance(), sheet_name=0, header=None)
    body = d.iloc[16:, [0, 1, 12, 13, 14, 15, 16, 20]].copy()
    body.columns = ["ym", "mes", "oficial", "oficial_mn", "gob_mn", "adelantos", "titulos_mn", "oficial_me"]
    body["mes"] = body["mes"].astype(str).str[:3]
    body = body[body["mes"].isin(MESES)].copy()
    body["year"] = body["ym"].astype(str).str.split(".").str[0].astype(int)
    body["month"] = body["mes"].map(MESES)
    body = body[body["month"].isin([3, 6, 9, 12]) & body["year"].between(1996, 2025)]
    body["Date"] = pd.to_datetime(dict(year=body["year"], month=body["month"], day=1)) + pd.offsets.MonthEnd(0)
    for c in ["oficial", "oficial_mn", "gob_mn", "adelantos", "titulos_mn", "oficial_me"]:
        body[c] = pd.to_numeric(body[c], errors="coerce") / 1000.0  # miles -> millones
    body = body.set_index("Date")
    gap = (body["oficial"] - body["oficial_mn"] - body["oficial_me"]).abs()
    if gap.max() > 1.0:
        raise RuntimeError(f"col12 != col13+col20 (max gap {gap.max():.1f} mm ARS)")
    out = pd.DataFrame(index=idx)
    out["bcra_tenencia_tesoro_ars_mm"] = body["oficial"].reindex(idx)
    out["bcra_adelantos_ars_mm"] = body["adelantos"].reindex(idx)
    out["bcra_titulos_mn_ars_mm"] = body["titulos_mn"].reindex(idx)
    out["bcra_letras_me_ars_mm"] = body["oficial_me"].reindex(idx)
    return out


def api_quarter_end(vid: int, idx: pd.DatetimeIndex) -> pd.Series:
    """Stock diario BCRA v4.0 llevado a fin de trimestre (ultimo dato, ffill).
    NaN antes de la primera observacion de la serie (no se imputan ceros)."""
    s = v1.fetch_bcra(vid, "1996-01-01", "2025-12-31")
    q = s.resample("QE").last().ffill()
    q.index = q.index.to_period("Q").to_timestamp("Q").normalize()
    return q.reindex(idx)


def main() -> None:
    gdp = v1.build_gdp()
    idx = pd.date_range("1996-03-31", "2025-12-31", freq="QE").normalize()
    idx.name = "Date"
    spnf = v1.build_spnf(idx)
    pesos = v1.build_bcra(idx)          # LEBAC/NOBAC + LELIQ + pases netos (ARS mm)
    hold = read_bcra_holdings(idx)
    dep = api_quarter_end(ID_DEP_GOB, idx)
    fx = api_quarter_end(ID_LETRAS_FX, idx)
    fx_sin = fx.isna()
    # Letras en USD del BCRA: la serie API empieza 2002-03-15; antes no hay instrumento
    # (LEBAC se crean en 2002) -> 0 con bandera, igual criterio que v1.
    fx = fx.fillna(0.0)

    df = pd.concat([gdp.reindex(idx)[["pib_4t_mm", "pib_origen"]], spnf[["deuda_spnf_ars_mm", "spnf_origen"]],
                    pesos[["pasivos_bcra_ars_mm"]], hold], axis=1)
    df["bcra_letras_fx_ars_mm"] = fx
    df["dep_tesoro_bcra_ars_mm"] = dep

    pib = df["pib_4t_mm"]
    pct = lambda c: df[c] / pib * 100.0  # noqa: E731
    df["bruta_federal_pib"] = pct("deuda_spnf_ars_mm")
    df["tenencia_bcra_tesoro_pib"] = pct("bcra_tenencia_tesoro_ars_mm")
    df["tenencia_fgs_tesoro_pib"] = np.nan   # sin fuente primaria accesible (ver informe)
    df["pasivos_bcra_lc_pib"] = pct("pasivos_bcra_ars_mm")
    df["pasivos_bcra_fx_pib"] = pct("bcra_letras_fx_ars_mm")
    df["pasivos_bcra_pib"] = df["pasivos_bcra_lc_pib"] + df["pasivos_bcra_fx_pib"]
    df["dep_tesoro_bcra_pib"] = pct("dep_tesoro_bcra_ars_mm")
    df["deuda_consolidada_neta_pib"] = (df["bruta_federal_pib"] - df["tenencia_bcra_tesoro_pib"]
                                        + df["pasivos_bcra_pib"] - df["dep_tesoro_bcra_pib"])
    # Bandera: la neta incluye todo salvo FGS y swap PBoC -> "neta excepto FGS"
    df["deuda_consolidada_neta_ex_fgs_pib"] = df["deuda_consolidada_neta_pib"]
    df["flag_fgs_faltante"] = 1
    df["flag_swap_pboc_faltante"] = (df.index >= "2020-01-01").astype(int)  # swap activado desde 2020
    df["flag_bruta_interpolada"] = (df["spnf_origen"] != "informe_trimestral").astype(int)
    df["flag_letras_fx_sin_serie"] = fx_sin.astype(int)
    df["flag_tenencia_bcra_faltante"] = df["bcra_tenencia_tesoro_ars_mm"].isna().astype(int)
    df["flag_pases_neto_negativo"] = (pesos["pases_neto"] < 0).astype(int)
    # FGS creado por Decreto 897/2007 (13-jul-2007): antes no existe el fondo como tenedor.
    df["flag_fgs_fondo_inexistente"] = (df.index < "2007-07-01").astype(int)
    # Componentes completos vs. definicion FMI: hay FGS (inexistente) y no hay swap PBoC activado.
    df["comparable_fmi"] = ((df["flag_fgs_fondo_inexistente"] == 1) & (df["flag_swap_pboc_faltante"] == 0)
                            & (df["flag_tenencia_bcra_faltante"] == 0)).astype(int)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = ["bruta_federal_pib", "tenencia_bcra_tesoro_pib", "tenencia_fgs_tesoro_pib", "pasivos_bcra_lc_pib",
            "pasivos_bcra_fx_pib", "pasivos_bcra_pib", "dep_tesoro_bcra_pib", "deuda_consolidada_neta_pib",
            "flag_fgs_faltante", "flag_swap_pboc_faltante", "flag_bruta_interpolada", "flag_letras_fx_sin_serie",
            "flag_tenencia_bcra_faltante", "flag_pases_neto_negativo", "flag_fgs_fondo_inexistente", "comparable_fmi", "pib_4t_mm", "pib_origen",
            "deuda_spnf_ars_mm", "bcra_tenencia_tesoro_ars_mm", "bcra_adelantos_ars_mm", "bcra_titulos_mn_ars_mm",
            "bcra_letras_me_ars_mm", "pasivos_bcra_ars_mm", "bcra_letras_fx_ars_mm", "dep_tesoro_bcra_ars_mm"]
    df[cols].to_csv(OUT_CSV, float_format="%.6f")
    print(f"[OK] {OUT_CSV} ({len(df)} trimestres)")

    # --- control FMI ---
    rows: List[dict] = []
    for k, f in FMI.items():
        t = pd.Timestamp(k)
        r = df.loc[t]
        rows.append({
            "fecha": k,
            "bruta_total_nuestra": r["bruta_federal_pib"], "bruta_total_fmi": f["bruta_total"],
            "intra_publico_nuestra_solo_bcra": r["tenencia_bcra_tesoro_pib"], "intra_publico_fmi": f["intra_publico_tesoro"],
            "pasivos_bcra_nuestra": r["pasivos_bcra_pib"], "pasivos_bcra_fmi": f["bcra_pasivos"],
            "bcra_lc_nuestra": r["pasivos_bcra_lc_pib"], "bcra_lc_fmi": f["bcra_lc"],
            "bcra_fx_nuestra": r["pasivos_bcra_fx_pib"], "bcra_fx_fmi": f["bcra_fx"],
            "dep_tesoro_nuestra": r["dep_tesoro_bcra_pib"], "dep_tesoro_fmi": f["dep_tesoro_bcra"],
            "neta_ex_fgs_nuestra": r["deuda_consolidada_neta_pib"], "neta_fmi": f["neta"],
        })
    ctrl = pd.DataFrame(rows).set_index("fecha").round(2)
    ctrl.to_csv(OUT_CTRL)
    print(ctrl.T.to_string())

    # --- figura ---
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    spnf_ref = pd.read_csv(SPNF_CSV, index_col=0, parse_dates=True) if SPNF_CSV.exists() else None
    fig, ax = plt.subplots(figsize=(9, 4.8))
    gross_cons = v1_gross_consolidada(df)
    ax.plot(df.index, gross_cons, color="#c8793a", lw=1.6, label="Consolidada bruta (v1: bruta + pasivos BCRA)")
    ax.plot(df.index, df["deuda_consolidada_neta_pib"], color="#1f3b5c", lw=2.0,
            label="Consolidada neta, excepto FGS (esta serie)")
    ax.plot(df.index, df["bruta_federal_pib"], color="#888888", lw=1.2, ls="--", label="Bruta federal (MECON)")
    if spnf_ref is not None:
        cand = [c for c in spnf_ref.columns if "spnf" in c.lower() and "pib" in c.lower()]
        if cand:
            ax.plot(spnf_ref.index, spnf_ref[cand[0]], color="#4c9a5b", lw=1.0, label=f"SPNF ({cand[0]})")
    for k, f in FMI.items():
        ax.scatter([pd.Timestamp(k)], [f["neta"]], marker="D", color="red", zorder=5,
                   label="Neta FMI CR 25/95" if k == "2023-12-31" else None)
    ax.set_ylabel("% del PIB nominal de los ultimos 4 trimestres")
    ax.set_title("Deuda publica consolidada neta (excepto FGS), 1996T1-2025T4")
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ax.grid(alpha=0.25)
    fig.text(0.01, 0.01, "Fuentes: MECON A.4.5/A.2.4; BCRA Balance (balbcrhis.xls) y API v4.0 (1258/1259/1260/1261/1264); "
             "INDEC. Sin FGS-ANSES ni swap PBoC.", fontsize=7)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_FIG, dpi=200)
    print(f"[OK] {OUT_FIG}")


def v1_gross_consolidada(df: pd.DataFrame) -> pd.Series:
    """Consolidada bruta de v1 = bruta federal + pasivos BCRA en pesos (% PIB)."""
    return df["bruta_federal_pib"] + df["pasivos_bcra_lc_pib"]


if __name__ == "__main__":
    main()
