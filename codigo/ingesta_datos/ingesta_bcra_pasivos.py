"""
ingesta_bcra_pasivos.py
========================
Consolidación de los pasivos remunerados del BCRA (Mejora Dimensión IV).

La serie `deuda_pib` del dataset original circunscribe el endeudamiento al
Sector Público Nacional No Financiero (SPNF) y excluye la emisión endógena
del Banco Central de la República Argentina (BCRA): LEBAC/NOBAC (2002-2018),
LELIQ/NOTALIQ (2018-2024) y la posición neta de pases. El devengamiento de
intereses de estos instrumentos constituye un déficit cuasifiscal que no
aparece en el resultado primario del Tesoro, subestimando el verdadero
requerimiento de financiamiento del sector público consolidado.

Fuente primaria (autoritativa, series oficiales del BCRA, no un proxy):
  API BCRA Estadísticas v4.0 — https://api.bcra.gob.ar/estadisticas/v4.0/monetarias
    - idVariable 1258: LEBAC, NOBAC y otras letras del BCRA en pesos
                       (no incluye LELIQ ni NOTALIQ) — vigente 2002-2018.
    - idVariable 1260: LELIQ y NOTALIQ — vigente 2018-2024 (a cero desde
                       jul-2024, cuando el Tesoro asumió el rol de esterilizador
                       mediante LEFI, decisión de política monetaria real y no
                       un artefacto de la serie).
    - idVariable 1261: Posición neta de pases (pasivos - activos) — cubre
                       todo el período 1996-2025.

  PIB nominal (precios corrientes, millones de ARS):
    datos.gob.ar, serie 166.2_PPIB_0_0_3 (INDEC, Cuentas Nacionales, 2006-2024).
    La serie está expresada a tasa anualizada estacionalmente ajustada (SAAR):
    se verificó empíricamente que dividir el stock de pasivos remunerados por
    el valor trimestral de esta serie sin transformación adicional reproduce
    el ~9.5% del PIB (2022-2023) citado en la literatura sobre el costo
    cuasifiscal del BCRA, mientras que agregar una suma móvil de 4 trimestres
    (que asumiría una serie NO anualizada) subestima la ratio en un factor
    ~4x. En consecuencia, `pib_nominal_trim` se usa directamente como
    denominador anualizado, sin suma móvil.
    Los trimestres sin dato directo (2004T1-2005T4 y 2025) se completan por
    extrapolación explícita a partir de la tasa de crecimiento nominal
    interanual promedio de los cuatro trimestres previos disponibles; el
    supuesto queda documentado en la columna `pib_nominal_es_extrapolado`.

Salida: datos/procesados/bcra_pasivos_trimestral.csv
  - pasivos_bcra_ars       : stock fin de trimestre, LEBAC/NOBAC + LELIQ/NOTALIQ
                             + posición neta de pases (millones de ARS).
  - pib_nominal_trim       : PIB nominal trimestral, SAAR (millones de ARS).
  - pib_nominal_es_extrapolado : bandera (1/0) de trimestres extrapolados.
  - pasivos_bcra_pib       : pasivos_bcra_ars / pib_nominal_trim * 100.
"""

import os
import time
import pandas as pd
import numpy as np
import requests

BCRA_BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SERIES = {
    "lebac_nobac": 1258,   # LEBAC, NOBAC y otras letras (no incluye LELIQ/NOTALIQ)
    "leliq_notaliq": 1260,  # LELIQ y NOTALIQ
    "pases_neto": 1261,     # Posición neta de pases (pasivos - activos)
}

PIB_NOMINAL_SERIES_ID = "166.2_PPIB_0_0_3"


def fetch_bcra_variable(id_variable: int, desde: str, hasta: str) -> pd.DataFrame:
    """Descarga la serie diaria completa de una variable BCRA (con paginación)."""
    all_rows = []
    offset = 0
    limit = 3000
    while True:
        params = {"desde": desde, "hasta": hasta, "limit": limit, "offset": offset}
        r = requests.get(f"{BCRA_BASE}/{id_variable}", params=params,
                          headers=HEADERS, timeout=30)
        r.raise_for_status()
        payload = r.json()
        results = payload.get("results", [])
        if not results:
            break
        detalle = results[0].get("detalle", [])
        all_rows.extend(detalle)
        count = payload.get("metadata", {}).get("resultset", {}).get("count", 0)
        offset += limit
        if offset >= count or not detalle:
            break
        time.sleep(0.2)
    if not all_rows:
        return pd.DataFrame(columns=["valor"])
    df = pd.DataFrame(all_rows)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.set_index("fecha")[["valor"]].sort_index()
    df = df[~df.index.duplicated(keep="last")]
    return df


def build_bcra_pasivos_diarios(desde: str = "2004-01-01", hasta: str = "2025-12-31") -> pd.DataFrame:
    """Combina LEBAC/NOBAC + LELIQ/NOTALIQ + posición neta de pases (diario)."""
    print("[BCRA] Descargando pasivos remunerados (API v4.0, series oficiales)...")
    series = {}
    for label, vid in SERIES.items():
        print(f"  -> idVariable {vid} ({label})...")
        s = fetch_bcra_variable(vid, desde, hasta)
        s.columns = [label]
        print(f"     {len(s)} observaciones diarias, {s.index.min()} -> {s.index.max()}")
        series[label] = s

    df = series["lebac_nobac"]
    for label in ["leliq_notaliq", "pases_neto"]:
        df = df.merge(series[label], left_index=True, right_index=True, how="outer")
    df = df.sort_index().ffill()
    df = df.fillna(0.0)
    df["pasivos_bcra_ars"] = df["lebac_nobac"] + df["leliq_notaliq"] + df["pases_neto"]
    return df


def fetch_pib_nominal(desde: str = "2004-01-01", hasta: str = "2025-12-31") -> pd.DataFrame:
    """PIB nominal trimestral (precios corrientes), con extrapolación explícita
    de los trimestres sin cobertura directa (2004-2005 y 2025)."""
    print("[PIB Nominal] Descargando serie 166.2_PPIB_0_0_3 (INDEC)...")
    url = (
        f"https://apis.datos.gob.ar/series/api/series?ids={PIB_NOMINAL_SERIES_ID}"
        f"&format=csv&collapse=quarter&collapse_aggregation=end_of_period&limit=400"
    )
    df = pd.read_csv(url, parse_dates=["indice_tiempo"], index_col="indice_tiempo",
                      storage_options={"User-Agent": "Mozilla/5.0"})
    df.columns = ["pib_nominal_trim"]
    df.index = df.index.to_period("Q").to_timestamp("Q")
    df["pib_nominal_es_extrapolado"] = 0

    full_index = pd.period_range(desde, hasta, freq="Q").to_timestamp("Q")
    df = df.reindex(full_index)
    df["pib_nominal_es_extrapolado"] = df["pib_nominal_es_extrapolado"].fillna(1).astype(int)

    # Extrapolación hacia atrás (2004T1-2005T4): tasa de crecimiento nominal
    # interanual promedio de los primeros 4 trimestres con dato real.
    valid = df["pib_nominal_trim"].dropna()
    g_yoy_inicial = valid.iloc[:8].pct_change(4).dropna().mean()
    idx_backfill = df.index[df["pib_nominal_trim"].isna() & (df.index < valid.index.min())]
    for t in sorted(idx_backfill, reverse=True):
        t_fwd = (pd.Period(t, freq="Q") + 4).to_timestamp("Q")
        if t_fwd in df.index and pd.notna(df.loc[t_fwd, "pib_nominal_trim"]):
            df.loc[t, "pib_nominal_trim"] = df.loc[t_fwd, "pib_nominal_trim"] / (1 + g_yoy_inicial)

    # Extrapolación hacia adelante (2025): tasa de crecimiento nominal
    # interanual promedio de los últimos 4 trimestres con dato real.
    valid = df["pib_nominal_trim"].dropna()
    g_yoy_final = valid.pct_change(4).dropna().iloc[-4:].mean()
    idx_forwardfill = df.index[df["pib_nominal_trim"].isna() & (df.index > valid.index.max())]
    for t in sorted(idx_forwardfill):
        t_lag = (pd.Period(t, freq="Q") - 4).to_timestamp("Q")
        if t_lag in df.index and pd.notna(df.loc[t_lag, "pib_nominal_trim"]):
            df.loc[t, "pib_nominal_trim"] = df.loc[t_lag, "pib_nominal_trim"] * (1 + g_yoy_final)

    n_extrap = int(df["pib_nominal_es_extrapolado"].sum())
    print(f"  -> {len(df) - n_extrap} trimestres con dato directo INDEC, "
          f"{n_extrap} extrapolados (tasa YoY inicial={g_yoy_inicial:.3f}, final={g_yoy_final:.3f}).")
    return df


def main():
    os.makedirs("datos/procesados", exist_ok=True)
    print("=" * 70)
    print(" CONSOLIDACIÓN DE PASIVOS REMUNERADOS DEL BCRA (Mejora Dimensión IV)")
    print("=" * 70)

    daily = build_bcra_pasivos_diarios()
    stock_trimestral = daily["pasivos_bcra_ars"].resample("QE").last().to_frame()
    stock_trimestral.index = stock_trimestral.index.to_period("Q").to_timestamp("Q")

    pib_nominal = fetch_pib_nominal()

    df = stock_trimestral.merge(pib_nominal, left_index=True, right_index=True, how="outer")
    df = df.sort_index()
    df["pasivos_bcra_pib"] = df["pasivos_bcra_ars"] / df["pib_nominal_trim"] * 100

    output_path = "datos/procesados/bcra_pasivos_trimestral.csv"
    df.to_csv(output_path)
    print(f"\n[OK] Guardado: {output_path}")
    print(f"     Cobertura: {df.index.min().date()} -> {df.index.max().date()} ({len(df)} trimestres)")
    print("\n     Pasivos remunerados BCRA / PIB (%), últimos 12 trimestres:")
    print(df[["pasivos_bcra_ars", "pasivos_bcra_pib"]].tail(12).round(2).to_string())

    pico = df["pasivos_bcra_pib"].idxmax()
    print(f"\n     Pico histórico: {df.loc[pico, 'pasivos_bcra_pib']:.2f}% del PIB en {pico.date()}")


if __name__ == "__main__":
    main()
