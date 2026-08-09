"""
ingesta_spread_regional.py
===========================
Mejora Dimensión III: nuevo instrumento de riesgo soberano regional para la
Función de Reacción Fiscal (IV-2SLS), en reemplazo del TCRM rezagado.

Motivación: en `fase4_variables_instrumentales.py`, el TCRM rezagado fue
rechazado por el test de Sargan (p<0.001) porque el tipo de cambio real
impacta directamente sobre la recaudación y el resultado primario argentino,
violando la restricción de exclusión. Un spread soberano regional (de un par
emergente sin exposición fiscal directa a la economía argentina) captura el
mismo canal de riesgo sistémico de mercados emergentes que castiga al EMBI+
argentino sin ser causado por -ni causar- el resultado primario doméstico.

Serie utilizada: iShares J.P. Morgan USD Emerging Markets Bond ETF (EMB,
NASDAQ), que replica el JPMorgan EMBI Global Diversified —el mismo proveedor
y familia de índices que el EMBI+ Argentina ya usado en el dataset—. Se usa
el nivel trimestral (precio de cierre promedio) como proxy de mercado del
riesgo soberano emergente agregado, exactamente en el mismo sentido en que
el VIX ya se usa como instrumento en niveles (no en "puntos básicos").

Limitaciones declaradas honestamente (no ocultas):
  1. Cobertura: EMB cotiza desde dic-2007. No existe serie diaria gratuita
     para 2004T1-2007T3 (15 trimestres), que quedan como NaN y se excluyen
     de la estimación IV-2SLS por dropna(), tal como ya ocurre con otras
     variables del protocolo.
  2. Composición: Argentina integra (con peso variable, ~1-3% en la mayoría
     de los años) el índice subyacente de EMB. Esto introduce una violación
     de exclusión de segundo orden, mucho más débil que el efecto directo
     del TCRM sobre pb_pib, pero se declara explícitamente como limitación
     de la estrategia de identificación en los resultados de Fase 4.
  3. Una serie específica de Brasil ("EMBI+ Brasil" de JP Morgan/Bloomberg)
     no está disponible sin suscripción paga; se evaluaron IPEADATA, Banco
     Central do Brasil (SGS) y FRED sin encontrar una serie equivalente de
     acceso gratuito y cobertura completa 2004-2025.

Salida: datos/procesados/spread_regional_trimestral.csv
  - EMB_price   : precio de cierre, promedio trimestral (USD).
  - EMBI_BRASIL : nivel invertido y reescalado de EMB_price para que se mueva
                  en el mismo sentido que un spread (sube cuando sube el
                  riesgo EM), usado como el instrumento propiamente dicho:
                  EMBI_BRASIL = (max(EMB_price) - EMB_price), en USD.
"""

import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime


def download_emb(start_date: str = "2004-01-01", end_date: str = None) -> pd.DataFrame:
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")
    print(f"[EMB] Descargando iShares JPMorgan USD EM Bond ETF ({start_date} -> {end_date})...")
    ticker = yf.Ticker("EMB")
    hist = ticker.history(start=start_date, end=end_date)
    if hist.empty:
        raise ValueError("Respuesta vacía de Yahoo Finance para EMB")
    df = hist[["Close"]].rename(columns={"Close": "EMB_price"})
    df.index = df.index.tz_localize(None)
    df.index.name = "Date"
    trimestral = df.resample("QE").mean()
    print(f"  [OK] EMB: {len(trimestral)} trimestres descargados "
          f"({trimestral.index.min().date()} -> {trimestral.index.max().date()}).")
    return trimestral


def main():
    os.makedirs("datos/procesados", exist_ok=True)
    print("=" * 70)
    print(" INGESTIÓN DEL SPREAD SOBERANO REGIONAL (EMB -> proxy EMBI regional)")
    print("=" * 70)

    df = download_emb()
    df.index = df.index.to_period("Q").to_timestamp("Q")

    full_index = pd.period_range("2004-01-01", "2025-12-31", freq="Q").to_timestamp("Q")
    df = df.reindex(full_index)
    df.index.name = "Date"

    df["EMBI_BRASIL"] = df["EMB_price"].max() - df["EMB_price"]


    n_valid = df["EMBI_BRASIL"].notna().sum()
    print(f"\n[OK] Cobertura: {n_valid}/{len(df)} trimestres con dato real "
          f"({df['EMB_price'].dropna().index.min().date()} -> "
          f"{df['EMB_price'].dropna().index.max().date()}).")
    print(f"     Trimestres sin cobertura (pre iShares EMB, dic-2007): "
          f"{len(df) - n_valid} (2004T1-2007T3, quedan como NaN, sin imputar).")

    output_path = "datos/procesados/spread_regional_trimestral.csv"
    df.to_csv(output_path)
    print(f"\n[OK] Guardado: {output_path}")
    print(df.tail(8).round(2).to_string())


if __name__ == "__main__":
    main()
