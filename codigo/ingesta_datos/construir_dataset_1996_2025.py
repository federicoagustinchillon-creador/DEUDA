"""
construir_dataset_1996_2025.py
================================
Ensambla dataset_consolidado_1996_2025.csv: ventana de 30 años (n=120),
extendiendo dataset_consolidado_real_ext.csv (1999T1-2025T4) hacia atras
hasta 1996T1. Fusiona:

  - deuda_pib, pb_pib, PIB_real: ya empalmados 1996T1-2003T4 en
    construir_dataset_ampliado.py (Denton + Compendio Fiscal), sin cambios.
  - EMBI (riesgo soberano): Spread_Empalmado_pb de
    datos/procesados/spread_soberano_historico_1983_2025.csv (Fase 22),
    que ya es electricamente identico al EMBI+ real de ambito.com desde
    1999T1 en adelante (verificado punto a punto) y lo extiende hacia atras
    con el spread stripped de bonos Brady (1994-1997) y EMBI+/EMBI Global
    Oficial (1998). No hace falta empalmar nada nuevo, ya esta hecho.
  - TCRM: el BCRA solo publica el Indice de Tipo de Cambio Real Multilateral
    desde enero de 1997 (verificado contra el archivo crudo
    datos/crudos/ITCRMSerie.xlsx). Para 1996 (4 trimestres de 120, 3.3% del
    panel) se aproxima por extrapolacion de tendencia: OLS de log(TCRM)
    sobre 1997T1-1999T4 (12 obs), proyectado hacia atras. Es una
    aproximacion declarada, no una reconstruccion de fuente primaria: la
    columna es_interpolado_tcrm la identifica para que cualquier ejercicio
    de robustez pueda excluirla si hace falta.

Ventana final: 1996T1-2025T4 (120 observaciones, 30 anios exactos).
"""

import pandas as pd
import numpy as np
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ingesta_mecon_indec import compute_output_gap

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS = BASE_DIR / "datos"

VENTANA_INICIO = "1996-01-01"
VENTANA_FIN = "2025-12-31"


def cargar_serie_empalmada(nombre_col, path_empalme):
    emp = pd.read_csv(path_empalme, parse_dates=["Date"], index_col="Date")[nombre_col]
    real = pd.read_csv(
        DATOS / "dataset_consolidado_real.csv", parse_dates=["Date"], index_col="Date"
    )[nombre_col]
    serie = pd.concat([emp, real]).sort_index()
    serie = serie[~serie.index.duplicated(keep="last")]
    return serie


def backcast_tcrm_1996():
    tcrm = pd.read_csv(
        DATOS / "tcrm_real_bcra_1997_2025.csv", parse_dates=["Date"], index_col="Date"
    )["TCRM"]
    ventana_ajuste = tcrm["1997-01-01":"1999-12-31"]
    t = np.arange(len(ventana_ajuste))
    logy = np.log(ventana_ajuste.values)
    slope, intercept = np.polyfit(t, logy, 1)
    fechas_1996 = pd.date_range("1996-03-31", "1996-12-31", freq="QE")
    t_back = np.array([-4, -3, -2, -1])
    valores_1996 = np.exp(intercept + slope * t_back)
    backcast = pd.Series(valores_1996, index=fechas_1996, name="TCRM")
    return pd.concat([backcast, tcrm]).sort_index()


def main():
    real = pd.read_csv(
        DATOS / "dataset_consolidado_real.csv", parse_dates=["Date"], index_col="Date"
    )

    deuda_pib = cargar_serie_empalmada("deuda_pib", DATOS / "empalme_pre2004_deuda_pb.csv")
    pb_pib = cargar_serie_empalmada("pb_pib", DATOS / "empalme_pre2004_deuda_pb.csv")
    pib_real = cargar_serie_empalmada("PIB_real", DATOS / "pib_real_empalme_1996_2003.csv")

    tcrm = backcast_tcrm_1996()

    spread = pd.read_csv(
        DATOS / "procesados" / "spread_soberano_historico_1983_2025.csv",
        parse_dates=["Date"], index_col="Date"
    )["Spread_Empalmado_pb"].rename("EMBI")

    vix = real["VIX"]
    cer = real["CER"]

    df = pd.DataFrame({
        "deuda_pib": deuda_pib, "pb_pib": pb_pib, "PIB_real": pib_real,
        "TCRM": tcrm, "EMBI": spread, "VIX": vix, "CER": cer,
    })

    df = df.loc[VENTANA_INICIO:VENTANA_FIN]

    df["es_interpolado"] = (df.index < "2004-01-01").astype(int)
    df["es_interpolado_tcrm"] = (df.index < "1997-01-01").astype(int)

    df["g_gap"] = compute_output_gap(df["PIB_real"])

    print("Dataset 1996-2025 (30 anios):")
    print(f"  Ventana: {df.index.min().date()} -> {df.index.max().date()}")
    print(f"  Observaciones: {len(df)}")
    print(f"  Trimestres empalmados (deuda/pb/PIB, es_interpolado=1): {df['es_interpolado'].sum()}")
    print(f"  Trimestres TCRM extrapolado (es_interpolado_tcrm=1): {df['es_interpolado_tcrm'].sum()}")
    print(f"  NaN por columna:\n{df.isna().sum()}")

    out = DATOS / "dataset_consolidado_1996_2025.csv"
    df.to_csv(out, index_label="Date")
    print(f"\n[OK] Guardado en {out}")


if __name__ == "__main__":
    main()
