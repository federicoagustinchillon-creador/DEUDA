"""
ingesta_instrumentos_1996_2025.py
===================================
Extiende los dos instrumentos de IV-2SLS (Fase 4) a la ventana unica de
referencia (1996-2025), reemplazando el instrumento regional que solo
cubria 2004-2025.

VIX: se extiende con datos reales de Yahoo Finance (^VIX), que cotiza
desde 1990. No hace falta ninguna aproximacion.

Instrumento regional: el ETF EMB (iShares JPMorgan USD EM Bond) usado
hasta ahora cotiza recien desde diciembre de 2007 (verificado via
yfinance, sin datos antes de esa fecha) y no se puede extender. Se
investigaron alternativas con historia real mas larga: ni EWZ (iShares
MSCI Brasil, ETF de renta variable) ni PCY ni BZF tienen datos antes de
2000 o directamente no cotizan en el periodo. El indice Bovespa (^BVSP),
en cambio, si tiene serie diaria real desde 1994 en Yahoo Finance. Se
reemplaza el proxy de riesgo regional por la volatilidad realizada
trimestral de los retornos diarios del Bovespa (BOVESPA_VOL), un
instrumento de mercado brasileno, no de deuda soberana como el EMB
original, pero con la misma logica de identificacion: captura apetito
de riesgo regional/emergente sin ser causado por el resultado fiscal
argentino, y con cobertura real completa para 1996-2025.

Salida: datos/procesados/instrumentos_1996_2025.csv
  - VIX          : nivel, promedio trimestral (^VIX).
  - BOVESPA_VOL   : desvio estandar de los retornos logaritmicos diarios
                    del Bovespa dentro de cada trimestre, anualizado
                    (x sqrt(252)), en puntos porcentuales.
"""

import pathlib
import numpy as np
import pandas as pd
import yfinance as yf

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
OUT_PATH = BASE_DIR / "datos" / "procesados" / "instrumentos_1996_2025.csv"

START = "1996-01-01"
END = "2025-12-31"


def download_vix():
    print(f"[VIX] Descargando ^VIX ({START} -> {END})...")
    hist = yf.Ticker("^VIX").history(start=START, end=END)
    if hist.empty:
        raise ValueError("Respuesta vacia de Yahoo Finance para ^VIX")
    df = hist[["Close"]].rename(columns={"Close": "VIX"})
    df.index = df.index.tz_localize(None)
    df.index.name = "Date"
    trimestral = df.resample("QE").mean()
    print(f"  [OK] VIX: {len(trimestral)} trimestres ({trimestral.index.min().date()} -> {trimestral.index.max().date()}).")
    return trimestral


def download_bovespa_vol():
    print(f"[BOVESPA] Descargando ^BVSP ({START} -> {END})...")
    hist = yf.Ticker("^BVSP").history(start=START, end=END)
    if hist.empty:
        raise ValueError("Respuesta vacia de Yahoo Finance para ^BVSP")
    close = hist["Close"]
    close.index = close.index.tz_localize(None)
    log_ret = np.log(close).diff()
    vol_trimestral = log_ret.resample("QE").std() * np.sqrt(252) * 100
    vol_trimestral.name = "BOVESPA_VOL"
    vol_trimestral.index.name = "Date"
    print(f"  [OK] BOVESPA_VOL: {len(vol_trimestral)} trimestres "
          f"({vol_trimestral.index.min().date()} -> {vol_trimestral.index.max().date()}).")
    return vol_trimestral.to_frame()


def main():
    (BASE_DIR / "datos" / "procesados").mkdir(parents=True, exist_ok=True)
    print("=" * 70)
    print(" INGESTION DE INSTRUMENTOS IV-2SLS, VENTANA 1996-2025 ")
    print("=" * 70)

    vix = download_vix()
    bovespa = download_bovespa_vol()

    df = vix.join(bovespa, how="outer")
    df = df.loc[START:END]

    print(f"\n[OK] {len(df)} trimestres, NaN por columna:\n{df.isna().sum()}")

    df.to_csv(OUT_PATH, index_label="Date")
    print(f"\n[OK] Guardado en {OUT_PATH}")


if __name__ == "__main__":
    main()
