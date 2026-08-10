"""
construir_dataset_ampliado.py
===============================
Ensambla dataset_consolidado_real_ext.csv: el panel ampliado que reemplaza
al de 88 observaciones (2004T1-2025T4) para el VAR/VECM pedido por el
director. Fusiona:

  - deuda_pib, pb_pib, PIB_real: empalmados 1996T1-2003T4 (Denton +
    Compendio Fiscal / tasas de crecimiento) + reales 2004T1-2025T4.
  - TCRM: serie real BCRA (ITCRM, rebaseada a dic-2001=1) 1997T1-2025T4,
    reemplaza el fallback previo en todo el panel.
  - EMBI: serie real ámbito.com (riesgo país) 1999T1-2025T4, reemplaza el
    fallback previo en todo el panel.

Ventana final: 1999T1-2025T4 (108 observaciones) — el límite lo pone EMBI,
que es la serie real con el arranque más tardío (ámbito.com no tiene datos
verificables antes de dic-1998). VIX y CER quedan en su ventana actual
(desde 2004) y no se extienden en este paso: no forman parte del sistema
de cointegración (deuda_pib, pb_pib, EMBI, TCRM) y su extensión se trata
por separado si hace falta para las etapas de robustez (IV-2SLS, DSA).

g_gap se recalcula sobre el PIB_real ampliado (mismo filtro HP, lambda=1600),
no se empalma por separado.
"""

import pandas as pd
import numpy as np
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ingesta_mecon_indec import compute_output_gap

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS = BASE_DIR / "datos"

VENTANA_INICIO = "1999-01-01"
VENTANA_FIN = "2025-12-31"


def cargar_serie_empalmada(nombre_col, path_empalme):
    """Concatena el tramo empalmado (pre-2004) con el tramo real (real.csv)."""
    emp = pd.read_csv(path_empalme, parse_dates=["Date"], index_col="Date")[nombre_col]
    real = pd.read_csv(
        DATOS / "dataset_consolidado_real.csv", parse_dates=["Date"], index_col="Date"
    )[nombre_col]
    serie = pd.concat([emp, real]).sort_index()
    serie = serie[~serie.index.duplicated(keep="last")]
    return serie


def main():
    real = pd.read_csv(
        DATOS / "dataset_consolidado_real.csv", parse_dates=["Date"], index_col="Date"
    )

    # 1. deuda_pib, pb_pib, PIB_real: empalmados + reales
    deuda_pib = cargar_serie_empalmada("deuda_pib", DATOS / "empalme_pre2004_deuda_pb.csv")
    pb_pib = cargar_serie_empalmada("pb_pib", DATOS / "empalme_pre2004_deuda_pb.csv")
    pib_real = cargar_serie_empalmada("PIB_real", DATOS / "pib_real_empalme_1996_2003.csv")

    # 2. TCRM y EMBI: series reales completas (reemplazan el fallback)
    tcrm = pd.read_csv(
        DATOS / "tcrm_real_bcra_1997_2025.csv", parse_dates=["Date"], index_col="Date"
    )["TCRM"]
    embi = pd.read_csv(
        DATOS / "embi_real_ambito_1999_2025.csv", parse_dates=["Date"], index_col="Date"
    )["EMBI"]

    # 3. VIX, CER: sin extender (quedan en su ventana real actual, 2004+)
    vix = real["VIX"]
    cer = real["CER"]

    df = pd.DataFrame({
        "deuda_pib": deuda_pib, "pb_pib": pb_pib, "PIB_real": pib_real,
        "TCRM": tcrm, "EMBI": embi, "VIX": vix, "CER": cer,
    })

    df = df.loc[VENTANA_INICIO:VENTANA_FIN]

    # Flag de trazabilidad: 1 si el trimestre viene de un empalme
    # (deuda_pib/pb_pib/PIB_real 1996-2003), 0 si es dato real de fuente
    # primaria (incluye TCRM y EMBI reales, que sustituyen al fallback).
    df["es_interpolado"] = (df.index < "2004-01-01").astype(int)

    # g_gap recalculado sobre el PIB_real ampliado (mismo filtro que antes)
    df["g_gap"] = compute_output_gap(df["PIB_real"])

    print("Dataset ampliado:")
    print(f"  Ventana: {df.index.min().date()} -> {df.index.max().date()}")
    print(f"  Observaciones: {len(df)}")
    print(f"  Trimestres empalmados (es_interpolado=1): {df['es_interpolado'].sum()}")
    print(f"  NaN por columna:\n{df.isna().sum()}")

    out = DATOS / "dataset_consolidado_real_ext.csv"
    df.to_csv(out, index_label="Date")
    print(f"\n[OK] Guardado en {out}")


if __name__ == "__main__":
    main()
