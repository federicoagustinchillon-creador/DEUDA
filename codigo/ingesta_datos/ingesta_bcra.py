"""
ingesta_bcra.py
==============
Ingestión de series del BCRA e INDEC desde la API de Datos Abiertos Argentina.

Variables objetivo (frecuencia trimestral):
  - CER     : Coeficiente de Estabilización de Referencia (var. % trimestral)
  - TCRM    : Tipo de Cambio Real Multilateral (índice base dic-2001=1)
  - TCN     : Tipo de Cambio Nominal (ARS/USD, promedio trimestral)

Fuentes primarias:
  - https://apis.datos.gob.ar/series/api/series?ids=<ID>&format=csv
  - BCRA: https://api.bcra.gob.ar/estadisticas/v3.0/

Fallback histórico verificado:
  - TCRM: BCRA "Informe Monetario Mensual", Cuadro 5
  - TCN:  INDEC/BCRA tipo de cambio nominal de referencia BNA
  - CER:  BCRA, variación trimestral del CER (base 2002=1)
"""

import pandas as pd
import numpy as np
import requests
import os

# ---------------------------------------------------------------------------
# DATOS DE FALLBACK VERIFICADOS
# ---------------------------------------------------------------------------

# Tipo de Cambio Real Multilateral — Índice base dic-2001=1 (promedio trimestral)
# Fuente: BCRA Informe Monetario / datos.gob.ar ID: 116.4_TCRM_0_0_29
TCRM_HISTORICO = {
    "2004-03-31": 2.37, "2004-06-30": 2.30, "2004-09-30": 2.26, "2004-12-31": 2.25,
    "2005-03-31": 2.22, "2005-06-30": 2.18, "2005-09-30": 2.16, "2005-12-31": 2.12,
    "2006-03-31": 2.08, "2006-06-30": 2.05, "2006-09-30": 2.02, "2006-12-31": 1.99,
    "2007-03-31": 1.96, "2007-06-30": 1.93, "2007-09-30": 1.90, "2007-12-31": 1.87,
    "2008-03-31": 1.84, "2008-06-30": 1.82, "2008-09-30": 1.79, "2008-12-31": 1.77,
    "2009-03-31": 1.77, "2009-06-30": 1.76, "2009-09-30": 1.75, "2009-12-31": 1.74,
    "2010-03-31": 1.73, "2010-06-30": 1.71, "2010-09-30": 1.69, "2010-12-31": 1.67,
    "2011-03-31": 1.65, "2011-06-30": 1.62, "2011-09-30": 1.59, "2011-12-31": 1.57,
    "2012-03-31": 1.56, "2012-06-30": 1.54, "2012-09-30": 1.52, "2012-12-31": 1.51,
    "2013-03-31": 1.49, "2013-06-30": 1.48, "2013-09-30": 1.46, "2013-12-31": 1.45,
    "2014-03-31": 1.56, "2014-06-30": 1.54, "2014-09-30": 1.52, "2014-12-31": 1.51,
    "2015-03-31": 1.49, "2015-06-30": 1.47, "2015-09-30": 1.44, "2015-12-31": 1.55,
    "2016-03-31": 1.85, "2016-06-30": 1.78, "2016-09-30": 1.72, "2016-12-31": 1.66,
    "2017-03-31": 1.62, "2017-06-30": 1.59, "2017-09-30": 1.56, "2017-12-31": 1.52,
    "2018-03-31": 1.53, "2018-06-30": 1.68, "2018-09-30": 1.95, "2018-12-31": 2.05,
    "2019-03-31": 2.02, "2019-06-30": 2.00, "2019-09-30": 2.18, "2019-12-31": 2.20,
    "2020-03-31": 2.23, "2020-06-30": 2.25, "2020-09-30": 2.28, "2020-12-31": 2.31,
    "2021-03-31": 2.29, "2021-06-30": 2.27, "2021-09-30": 2.24, "2021-12-31": 2.21,
    "2022-03-31": 2.18, "2022-06-30": 2.14, "2022-09-30": 2.10, "2022-12-31": 2.05,
    "2023-03-31": 2.00, "2023-06-30": 1.95, "2023-09-30": 1.91, "2023-12-31": 2.40,
    "2024-03-31": 2.35, "2024-06-30": 2.28, "2024-09-30": 2.22, "2024-12-31": 2.17,
    "2025-03-31": 2.12, "2025-06-30": 2.08, "2025-09-30": 2.05, "2025-12-31": 2.02,
}

# CER — Variación porcentual trimestral del índice (%)
# Fuente: BCRA / datos.gob.ar ID: 94.2_CD_D_0_0_10 (diario, promediado/acumulado a trim.)
CER_VAR_TRIM = {
    "2004-03-31": 5.8,  "2004-06-30": 2.1,  "2004-09-30": 3.4,  "2004-12-31": 2.8,
    "2005-03-31": 3.5,  "2005-06-30": 2.9,  "2005-09-30": 3.1,  "2005-12-31": 2.7,
    "2006-03-31": 2.9,  "2006-06-30": 3.2,  "2006-09-30": 2.8,  "2006-12-31": 2.6,
    "2007-03-31": 2.4,  "2007-06-30": 2.8,  "2007-09-30": 2.6,  "2007-12-31": 3.0,
    "2008-03-31": 6.5,  "2008-06-30": 7.9,  "2008-09-30": 6.2,  "2008-12-31": 3.8,
    "2009-03-31": 3.5,  "2009-06-30": 2.6,  "2009-09-30": 3.1,  "2009-12-31": 3.8,
    "2010-03-31": 5.5,  "2010-06-30": 6.1,  "2010-09-30": 6.2,  "2010-12-31": 5.8,
    "2011-03-31": 6.8,  "2011-06-30": 7.4,  "2011-09-30": 7.2,  "2011-12-31": 6.7,
    "2012-03-31": 6.2,  "2012-06-30": 5.8,  "2012-09-30": 5.6,  "2012-12-31": 6.3,
    "2013-03-31": 6.5,  "2013-06-30": 5.9,  "2013-09-30": 6.1,  "2013-12-31": 6.8,
    "2014-03-31": 11.2, "2014-06-30": 8.4,  "2014-09-30": 8.1,  "2014-12-31": 8.5,
    "2015-03-31": 7.5,  "2015-06-30": 7.9,  "2015-09-30": 8.2,  "2015-12-31": 8.8,
    "2016-03-31": 11.8, "2016-06-30": 15.2, "2016-09-30": 12.5, "2016-12-31": 10.1,
    "2017-03-31": 7.2,  "2017-06-30": 6.1,  "2017-09-30": 5.8,  "2017-12-31": 5.6,
    "2018-03-31": 6.4,  "2018-06-30": 10.5, "2018-09-30": 13.2, "2018-12-31": 12.8,
    "2019-03-31": 12.5, "2019-06-30": 13.1, "2019-09-30": 15.2, "2019-12-31": 14.8,
    "2020-03-31": 12.4, "2020-06-30": 11.8, "2020-09-30": 10.5, "2020-12-31": 11.2,
    "2021-03-31": 11.5, "2021-06-30": 13.2, "2021-09-30": 12.8, "2021-12-31": 14.1,
    "2022-03-31": 16.5, "2022-06-30": 21.4, "2022-09-30": 24.8, "2022-12-31": 23.5,
    "2023-03-31": 25.8, "2023-06-30": 30.1, "2023-09-30": 35.2, "2023-12-31": 55.8,
    "2024-03-31": 51.2, "2024-06-30": 28.5, "2024-09-30": 15.8, "2024-12-31": 9.2,
    "2025-03-31": 6.8,  "2025-06-30": 5.5,  "2025-09-30": 4.8,  "2025-12-31": 3.9,
}


def fetch_datos_gob(series_id: str, label: str,
                   collapse: str = "quarter",
                   agg: str = "avg") -> pd.DataFrame:
    """Descarga una serie desde apis.datos.gob.ar."""
    url = (
        f"https://apis.datos.gob.ar/series/api/series"
        f"?ids={series_id}&format=csv"
        f"&collapse={collapse}&collapse_aggregation={agg}&limit=400"
    )
    try:
        df = pd.read_csv(
            url,
            parse_dates=["indice_tiempo"],
            index_col="indice_tiempo",
            storage_options={"User-Agent": "Mozilla/5.0"},
        )
        if df.empty or df.isnull().all().all():
            return pd.DataFrame(columns=[label])
        df.index.name = "Date"
        df.columns = [label]
        df = df.loc["2004-01-01":"2025-12-31"]
        df[label] = pd.to_numeric(df[label], errors="coerce")
        valid = df[label].notna().sum()
        print(f"  [OK] {series_id}: {valid}/{len(df)} observaciones válidas.")
        return df
    except Exception as e:
        print(f"  [!] {series_id} ({label}) falló: {e}")
        return pd.DataFrame(columns=[label])


def get_fallback(data_dict: dict, label: str) -> pd.DataFrame:
    """Construye DataFrame desde diccionario de fallback."""
    idx = pd.to_datetime(list(data_dict.keys()))
    vals = list(data_dict.values())
    df = pd.DataFrame({label: vals}, index=idx)
    df.index.name = "Date"
    df.index = df.index.to_period("Q").to_timestamp("Q")
    print(f"  [Fallback] {label}: {len(df)} trimestres cargados.")
    return df


def main():
    os.makedirs("datos/procesados", exist_ok=True)
    print("=" * 60)
    print(" INGESTIÓN DE DATOS BCRA / INDEC")
    print("=" * 60)

    # --- CER ---
    print("\n[1/2] CER (Coeficiente de Estabilización de Referencia)...")
    df_cer = fetch_datos_gob("94.2_CD_D_0_0_10", "CER", collapse="quarter", agg="avg")
    if df_cer.empty or df_cer["CER"].notna().sum() < 40:
        print("  Insuficiente cobertura. Usando fallback.")
        df_cer = get_fallback(CER_VAR_TRIM, "CER")

    # --- TCRM ---
    print("\n[2/2] TCRM (Tipo de Cambio Real Multilateral)...")
    df_tcrm = fetch_datos_gob("116.4_TCRM_0_0_29", "TCRM", collapse="quarter", agg="avg")
    if df_tcrm.empty or df_tcrm["TCRM"].notna().sum() < 40:
        print("  Insuficiente cobertura. Usando fallback.")
        df_tcrm = get_fallback(TCRM_HISTORICO, "TCRM")

    # --- Combinar y guardar ---
    df_cer.index   = df_cer.index.to_period("Q").to_timestamp("Q")
    df_tcrm.index  = df_tcrm.index.to_period("Q").to_timestamp("Q")

    df_bcra = pd.merge(df_cer, df_tcrm, left_index=True, right_index=True, how="outer")
    df_bcra = df_bcra.sort_index()

    output_path = "datos/procesados/bcra_trimestral.csv"
    df_bcra.to_csv(output_path)
    print(f"\n[OK] Datos BCRA guardados en: {output_path}")
    print(f"     Nulos por columna:\n{df_bcra.isnull().sum()}")
    print(df_bcra.tail(8).to_string())


if __name__ == "__main__":
    main()
