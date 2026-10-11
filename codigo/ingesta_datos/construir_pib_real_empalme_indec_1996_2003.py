"""
construir_pib_real_empalme_indec_1996_2003.py
===============================================
PIB real trimestral 1996T1-2003T4 desde el PIB a precios constantes TRIMESTRAL
de INDEC base 1993, empalmado a base 2004. Reemplaza el procedimiento de
empalme_pib_real_pre2004.py (tasas de crecimiento anuales tipeadas + Denton).

Fuentes (datos.gob.ar, INDEC, "Oferta y Demanda Globales"):
  - Base 1993: 2.2_OGP_1993_T_17  PIB a precios de comprador, millones de $ de 1993 (1993T1-2013T3)
  - Base 2004: 4.2_OGP_2004_T_17  PIB a precios de comprador, millones de $ de 2004 (2004T1-)

Empalme (retropolacion por coeficiente de enlace, igual criterio que el PIB
nominal en construir_deuda_consolidada_1996_2025.build_gdp):

    k = media_{t in 2004T1..2004T4}( Y04_t / Y93_t )
    Y_t = k * Y93_t     para t < 2004T1;     Y_t = Y04_t   para t >= 2004T1

Esto preserva las tasas de crecimiento trimestrales (incluida la estacionalidad)
de la base 1993 antes de 2004. La serie del dataset (PIB_real) esta en una unidad
distinta (Y04 * c, con c constante); c se estima como mediana de PIB_real/Y04 en
2004T1-2025T4 y se verifica que su dispersion sea nula.

Salida: datos/procesados/pib_real_empalme_indec_1996_2003.csv y comparacion
contra datos/pib_real_empalme_1996_2003.csv (version previa, Denton + tasas tipeadas).

Uso:  python codigo/ingesta_datos/construir_pib_real_empalme_indec_1996_2003.py
"""
from __future__ import annotations

import io
import pathlib
from typing import Tuple

import pandas as pd
import requests

BASE = pathlib.Path(__file__).resolve().parents[2]
RAW_DIR = BASE / "datos" / "crudos" / "resultado_primario"
OUT_CSV = BASE / "datos" / "procesados" / "pib_real_empalme_indec_1996_2003.csv"
DATASET = BASE / "datos" / "dataset_consolidado_real.csv"
OLD = BASE / "datos" / "pib_real_empalme_1996_2003.csv"
SERIES_API = "https://apis.datos.gob.ar/series/api/series/"
ID_93 = "2.2_OGP_1993_T_17"
ID_04 = "4.2_OGP_2004_T_17"


def fetch(series_id: str) -> pd.Series:
    """Serie trimestral de datos.gob.ar con cache; indice = fin de trimestre."""
    path = RAW_DIR / f"{series_id}.csv"
    try:
        r = requests.get(SERIES_API, params={"ids": series_id, "format": "csv", "limit": 1000}, timeout=60)
        r.raise_for_status()
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(r.text, encoding="utf-8")
        text = r.text
    except Exception as err:  # noqa: BLE001
        if not path.exists():
            raise RuntimeError(f"Fuente inaccesible y sin cache: {series_id}") from err
        text = path.read_text(encoding="utf-8")
    s = pd.read_csv(io.StringIO(text), index_col=0, parse_dates=True).iloc[:, 0].astype(float)
    s.index = s.index.to_period("Q").to_timestamp("Q").normalize()
    return s


def splice() -> Tuple[pd.Series, float, pd.Series]:
    """Devuelve (Y empalmado en millones de $ de 2004, k, ratio Y04/Y93 en el solape)."""
    y93, y04 = fetch(ID_93), fetch(ID_04)
    solape = y04.index.intersection(y93.index)
    ratio = (y04.loc[solape] / y93.loc[solape])
    ref = ratio.loc["2004-01-01":"2004-12-31"]
    if len(ref) != 4:
        raise RuntimeError("No hay 4 trimestres solapados en 2004")
    k = float(ref.mean())
    pre = y93[y93.index < y04.index.min()] * k
    return pd.concat([pre, y04]).sort_index(), k, ratio


def main() -> None:
    y, k, ratio = splice()
    y04 = fetch(ID_04)
    ds = pd.read_csv(DATASET, index_col=0, parse_dates=True)["PIB_real"]
    c = (ds / y04.reindex(ds.index)).dropna()
    if c.std() / c.mean() > 1e-9:
        raise RuntimeError("PIB_real del dataset no es proporcional a 4.2_OGP_2004_T_17")
    c0 = float(c.median())
    idx = pd.date_range("1996-03-31", "2003-12-31", freq="QE").normalize()
    out = pd.DataFrame(index=idx)
    out.index.name = "Date"
    out["pib_real_mm_pesos2004"] = y.reindex(idx)
    out["PIB_real"] = out["pib_real_mm_pesos2004"] * c0
    out["fuente"] = f"INDEC_{ID_93}_x_k_enlace_a_{ID_04}"
    out["es_interpolado"] = 0
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, float_format="%.6f")
    print(f"[OK] {OUT_CSV} | k={k:.5f} (rango solape {ratio.min():.5f}-{ratio.max():.5f}) | c={c0:.6e}")

    old = pd.read_csv(OLD, index_col=0, parse_dates=True)["PIB_real"].reindex(idx)
    d = pd.DataFrame({"nuevo": out["PIB_real"], "viejo": old})
    d["dif_pct"] = (d["viejo"] / d["nuevo"] - 1) * 100
    print(f"Nivel trimestral viejo vs nuevo: max|dif|={d['dif_pct'].abs().max():.2f}% "
          f"({d['dif_pct'].abs().idxmax().date()}), media|dif|={d['dif_pct'].abs().mean():.2f}%")
    an = pd.DataFrame({"nuevo": d["nuevo"].groupby(d.index.year).mean(), "viejo": d["viejo"].groupby(d.index.year).mean()})
    an["g_nuevo"] = an["nuevo"].pct_change() * 100
    an["g_viejo"] = an["viejo"].pct_change() * 100
    an["dif_nivel_anual_pct"] = (an["viejo"] / an["nuevo"] - 1) * 100
    print("\nPromedios anuales (unidad PIB_real del dataset) y crecimiento %:")
    print(an.round(2).to_string())
    ds04 = ds.iloc[0]
    print(f"\nSalto al empalme 2003T4 -> 2004T1: nuevo {out['PIB_real'].iloc[-1]:.3f} -> {ds04:.3f} "
          f"(var {100 * (ds04 / out['PIB_real'].iloc[-1] - 1):.2f}%, T4->T1 con estacionalidad); viejo {old.iloc[-1]:.3f} -> {ds04:.3f}")


if __name__ == "__main__":
    main()
