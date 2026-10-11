"""Construye la serie de tenencias del sector publico (FGS y agencias) 1996-2025.

Fuentes
-------
* Secretaria de Finanzas, "Presentacion grafica" trimestral de la deuda, cuadro
  "Deuda Bruta de la Administracion Central por acreedor" (pagina 10) y grafico
  "Evolucion ... por acreedor en % del PBI" (pagina 11, anual 2004-2025).
  Las cifras se PARSEAN de los PDF en datos/crudos/fgs/finanzas_pres/; no hay
  valores tipeados, solo el mapa archivo -> fechas (a)/(b) de las dos columnas.
* FGS (ANSES): www.anses.gob.ar esta detras de proteccion anti-bot (Incapsula,
  HTTP 403) y no pudo descargarse. Si existen PDF/CSV del FGS en
  datos/crudos/fgs/ se pueden cargar via FGS_ANCLAS (vacio por defecto: no se
  inventan valores). Las columnas FGS quedan vacias.

Salida: datos/procesados/tenencias_fgs_1996_2025.csv

Definicion: agencias_sp_pib (anual, Q4) = % PBI con TC de fin de periodo
publicado por Finanzas; agencias_sp_pib_propio = agencias_usd * tc / pib_4t.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz  # PyMuPDF
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PDF_DIR = RAIZ / "datos" / "crudos" / "fgs" / "finanzas_pres"
SALIDA = RAIZ / "datos" / "procesados" / "tenencias_fgs_1996_2025.csv"
BASE = RAIZ / "datos" / "procesados" / "deuda_consolidada_1996_2025.csv"

# archivo -> (fecha columna (a), fecha columna (b)); fuente: encabezado de la pag. 10
# de cada presentacion (el 4T23 etc. no imprimen fechas en texto: se deducen del
# nombre del informe; (a) es siempre el cierre del ano anterior).
FECHAS: Dict[str, Tuple[str, str]] = {
    "presentacion_grafica_1t22.pdf": ("2021-12-31", "2022-03-31"),
    "presentacio768n_gra769fica_2t22_-_final.pdf": ("2021-12-31", "2022-06-30"),
    "presentacion_gra769fica_3t222_-ppt.pdf": ("2021-12-31", "2022-09-30"),
    "presentacion_grafica_ivt22.pdf": ("2021-12-31", "2022-12-31"),
    "presentacion_gra_fica_1t23.pdf": ("2022-12-31", "2023-03-31"),
    "presentacion_gra_fica_2t23.pdf": ("2022-12-31", "2023-06-30"),
    "presentacion_grafica_3t23.pdf": ("2022-12-31", "2023-09-30"),
    "presentacion_grafica_4t23.pdf": ("2022-12-31", "2023-12-31"),
    "presentacion_grafica_it_2024_2.pdf": ("2023-12-31", "2024-03-31"),
    "presentacion_grafica_iit2024_2.pdf": ("2023-12-31", "2024-06-30"),
    "presentacion_grafica_iiit_2024_2.pdf": ("2023-12-31", "2024-09-30"),
    "presentacion_grafica_ivt_2024.pdf": ("2023-12-31", "2024-12-31"),
    "presentacion_grafica_it_2025.pdf": ("2024-12-31", "2025-03-31"),
    "presentacion_grafica_ii_t_25.pdf": ("2024-12-31", "2025-06-30"),
    "presentacion_grafica_iii_t_25_2.pdf": ("2024-12-31", "2025-09-30"),
    "presentacion_grafica_ivt_25.pdf": ("2024-12-31", "2025-12-31"),
}
PDF_ANUAL = "presentacion_grafica_ivt_25.pdf"  # pagina 11: serie anual % PBI 2004-2025

# Anclas FGS (fecha -> (ars_mm, usd_mm, "fuente exacta pag./cuadro")). Vacio: ANSES
# bloqueo la descarga; completar solo con cifras leidas de un PDF/Excel oficial.
FGS_ANCLAS: Dict[str, Tuple[Optional[float], Optional[float], str]] = {}

_NUM = re.compile(r"^\(?-?\d[\d.,]*%?\)?$")


def _num(tok: str) -> float:
    """Convierte '217.298' o '38,4%' (formato es-AR) a float."""
    t = tok.replace("%", "").replace(".", "").replace(",", ".")
    return float(t)


def _fila_agencias(pdf: Path) -> List[float]:
    """Devuelve [usd_a, pct_a, usd_b, pct_b] de la fila 'Agencias del Sector Publico'."""
    pag = fitz.open(pdf)[9]
    words = pag.get_text("words")
    y = [w[1] for w in words if w[4] == "Agencias"][0]
    toks = [w[4] for w in sorted(words, key=lambda w: w[0]) if abs(w[1] - y) < 8 and _NUM.match(w[4])]
    if len(toks) < 8:
        raise ValueError(f"fila de agencias incompleta en {pdf.name}: {toks}")
    v = [_num(t) for t in toks[:8]]
    return [v[0], v[2], v[4], v[6]]  # USD (a), %PBI fin (a), USD (b), %PBI fin (b)


def _serie_anual() -> Dict[int, float]:
    """% PBI de agencias por ano (segmento superior del grafico de la pag. 11)."""
    pag = fitz.open(PDF_DIR / PDF_ANUAL)[10]
    w = pag.get_text("words")
    yrs = [((x0 + x1) / 2, t) for x0, y0, x1, y1, t, *_ in w if re.fullmatch(r"20\d\d", t)]
    cols: Dict[str, List[Tuple[float, str]]] = {}
    for x0, y0, x1, y1, t, *_ in w:
        if re.fullmatch(r"\d[\d,]*%", t) and not re.fullmatch(r"\d+%", t):
            xc = (x0 + x1) / 2
            yr = min(yrs, key=lambda q: abs(q[0] - xc))[1]
            cols.setdefault(yr, []).append((y0, t))
    out: Dict[int, float] = {}
    for yr, lst in cols.items():
        vals = [t for _, t in sorted(lst)]
        out[int(yr)] = _num(vals[1])  # [0]=total, [1]=agencias
    return out


def construir() -> pd.DataFrame:
    base = pd.read_csv(BASE, parse_dates=["Date"])[["Date", "pib_4t_mm", "tc_ars_usd"]]
    ancl: Dict[pd.Timestamp, Tuple[float, float, str]] = {}
    for arch, (da, db) in FECHAS.items():
        usd_a, pct_a, usd_b, pct_b = _fila_agencias(PDF_DIR / arch)
        src = f"Finanzas, Presentacion grafica ({arch}), pag.10"
        for d, u, p in ((da, usd_a, pct_a), (db, usd_b, pct_b)):
            ts = pd.Timestamp(d)
            if ts in ancl and abs(ancl[ts][0] - u) > 1e-9:
                # el ultimo informe publicado prevalece (revision de PIB/TC)
                pass
            ancl[ts] = (u, p, src)
    anual = _serie_anual()

    df = base.copy()
    df["fgs_titulos_ars_mm"] = np.nan
    df["fgs_titulos_usd_mm"] = np.nan
    for d, (ars, usd, _) in FGS_ANCLAS.items():
        m = df["Date"] == pd.Timestamp(d)
        df.loc[m, "fgs_titulos_ars_mm"] = ars
        df.loc[m, "fgs_titulos_usd_mm"] = usd
    df["agencias_sp_usd_mm"] = df["Date"].map(lambda d: ancl.get(d, (np.nan,))[0])
    df["agencias_sp_pib"] = df["Date"].map(lambda d: ancl.get(d, (np.nan, np.nan))[1])
    df["fuente"] = df["Date"].map(lambda d: ancl[d][2] if d in ancl else "")
    # Q4 anual 2004-2025 (grafico pag.11 ivt_25) cuando no hay ancla trimestral
    for yr, p in anual.items():
        m = (df["Date"] == pd.Timestamp(f"{yr}-12-31")) & df["agencias_sp_pib"].isna()
        df.loc[m, "agencias_sp_pib"] = p
        df.loc[m, "fuente"] = f"Finanzas, {PDF_ANUAL}, pag.11 (% PBI anual)"
    # interpolacion en USD entre anclas (solo dentro del rango anclado)
    s = df["agencias_sp_usd_mm"]
    interp = s.interpolate(limit_area="inside")
    df["flag_interpolado"] = (s.isna() & interp.notna()).astype(int)
    df["agencias_sp_usd_mm"] = interp
    df["agencias_sp_pib_propio"] = df["agencias_sp_usd_mm"] * df["tc_ars_usd"] / df["pib_4t_mm"] * 100
    df["fgs_pib_propio"] = df["fgs_titulos_ars_mm"] / df["pib_4t_mm"] * 100
    cols = ["Date", "fgs_titulos_ars_mm", "fgs_titulos_usd_mm", "agencias_sp_usd_mm",
            "agencias_sp_pib", "fuente", "flag_interpolado", "agencias_sp_pib_propio", "fgs_pib_propio"]
    return df[cols]


if __name__ == "__main__":
    out = construir()
    out.to_csv(SALIDA, index=False)
    print(out.dropna(subset=["agencias_sp_pib", "agencias_sp_usd_mm"], how="all").to_string())
