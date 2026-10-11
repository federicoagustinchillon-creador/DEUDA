"""Ingesta de la tasa de politica de la Fed, trimestral 1996Q1-2025Q4.

Fuentes:
  * FEDFUNDS (FRED): https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS
  * Wu-Xia shadow federal funds rate (Atlanta Fed):
    https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/datafiles/cqer/research/wu-xia-shadow-federal-funds-rate/WuXiaShadowRate.xlsx

Serie combinada ``tasa_politica_fed``: tasa sombra si el trimestre esta en el
piso cero (FEDFUNDS trimestral < 0.25) y el trimestre tiene los 3 meses de la
tasa sombra; tasa efectiva en los demas casos.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path
from typing import Dict

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
CRUDOS = RAIZ / "datos" / "crudos" / "tasa_fed"
SALIDA = RAIZ / "datos" / "procesados" / "tasa_fed_trimestral_1996_2025.csv"
URL_FF = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS"
URL_WX = ("https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/datafiles/"
          "cqer/research/wu-xia-shadow-federal-funds-rate/WuXiaShadowRate.xlsx")
UMBRAL_ZLB = 0.25
INICIO, FIN = "1996Q1", "2025Q4"


def _descargar(url: str, destino: Path, intentos: int = 3) -> bytes:
    """Descarga ``url`` (con reintentos) y guarda copia cruda en ``destino``.

    Si todos los intentos fallan y existe una copia previa en ``destino``, la
    reutiliza (la copia cruda fue bajada de la misma URL).
    """
    destino.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for _ in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                datos = r.read()
            destino.write_bytes(datos)
            return datos
        except OSError:
            continue
    if destino.exists():
        return destino.read_bytes()
    raise RuntimeError(f"No se pudo descargar {url}")


def trimestralizar(mensual: pd.Series) -> pd.DataFrame:
    """Promedio trimestral y numero de meses observados por trimestre.

    q_t = (1/n_t) * sum_{m in t} x_m, con n_t el numero de meses disponibles.
    """
    p = mensual.dropna().copy()
    p.index = p.index.to_period("Q")
    g = p.groupby(level=0)
    return pd.DataFrame({"valor": g.mean(), "n": g.count()})


def construir(descargar: bool = True) -> pd.DataFrame:
    """Construye el DataFrame trimestral con las cuatro columnas de salida."""
    if descargar:
        ff_b = _descargar(URL_FF, CRUDOS / "FEDFUNDS.csv")
        wx_b = _descargar(URL_WX, CRUDOS / "WuXiaShadowRate.xlsx")
    else:
        ff_b = (CRUDOS / "FEDFUNDS.csv").read_bytes()
        wx_b = (CRUDOS / "WuXiaShadowRate.xlsx").read_bytes()
    ff = pd.read_csv(io.BytesIO(ff_b), parse_dates=["observation_date"], index_col=0)["FEDFUNDS"]
    wx = pd.read_excel(io.BytesIO(wx_b), header=None, skiprows=1, usecols=[0, 2])
    wx = wx.dropna().set_index(0)[2].astype(float)
    wx.index = pd.to_datetime(wx.index)

    qf, qw = trimestralizar(ff), trimestralizar(wx)
    idx = pd.period_range(INICIO, FIN, freq="Q")
    df = pd.DataFrame(index=idx)
    df["fedfunds"] = qf["valor"].reindex(idx)
    df["shadow_wu_xia"] = qw["valor"].where(qw["n"] == 3).reindex(idx)
    zlb = df["fedfunds"] < UMBRAL_ZLB
    usa_sombra = zlb & df["shadow_wu_xia"].notna()
    df["tasa_politica_fed"] = df["fedfunds"].where(~usa_sombra, df["shadow_wu_xia"])
    flag = pd.Series("fedfunds", index=idx)
    flag[usa_sombra] = "shadow_wu_xia"
    flag[zlb & ~usa_sombra] = "fedfunds_zlb_sin_shadow"
    df["fuente_flag"] = flag
    df.insert(0, "Date", idx.to_timestamp(how="end").normalize())
    return df.reset_index(drop=True)


def estadisticas(df: pd.DataFrame) -> Dict[str, float]:
    """Media y desvio (ddof=1) de la variacion trimestral y magnitud de ciclos."""
    s = df.set_index(pd.PeriodIndex(df["Date"], freq="Q"))["tasa_politica_fed"]
    d = s.diff().dropna()
    def ciclo(base: str, ini: str, fin: str) -> float:
        return float(s[ini:fin].max() - s[base])
    return {
        "n_dif": float(len(d)), "media_dq": float(d.mean()), "sd_dq": float(d.std(ddof=1)),
        "sd_dq_ddof0": float(d.std(ddof=0)),
        "ciclo_2022_23": ciclo("2021Q4", "2022Q1", "2024Q4"),
        "pico_2022_23": float(s["2022Q1":"2024Q4"].max()),
        "pico_trim_2022_23": str(s["2022Q1":"2024Q4"].idxmax()),
        "base_2021Q4": float(s["2021Q4"]),
        "ciclo_2004_06": ciclo("2003Q4", "2004Q1", "2007Q4"),
        "pico_2004_06": float(s["2004Q1":"2007Q4"].max()),
        "pico_trim_2004_06": str(s["2004Q1":"2007Q4"].idxmax()),
        "base_2003Q4": float(s["2003Q4"]),
    }


if __name__ == "__main__":
    out = construir()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(SALIDA, index=False, date_format="%Y-%m-%d", float_format="%.6f")
    print(out["fuente_flag"].value_counts().to_string())
    print(out[out.fuente_flag != "fedfunds"][["Date", "fedfunds", "shadow_wu_xia", "fuente_flag"]].to_string())
    for k, v in estadisticas(out).items():
        print(k, v)
