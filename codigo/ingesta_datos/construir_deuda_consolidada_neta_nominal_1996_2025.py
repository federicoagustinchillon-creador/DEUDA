"""
construir_deuda_consolidada_neta_nominal_1996_2025.py
=======================================================
Variante de la deuda consolidada neta (construir_deuda_consolidada_neta_1996_2025.py)
que netea las Letras Intransferibles en poder del BCRA a VALOR NOMINAL (coherente
con la deuda bruta, que se mide a nominal), en vez de al valor contable del
balance del BCRA (balbcrhis.xls, columna "Sector oficial - moneda extranjera").

    T^BCRA_nom_t = T^BCRA_libros_t - L^ME_libros_t + N_t * TC_t           (ARS mm)
    D_neta_nom_t = ( B_t - T^BCRA_nom_t - T^FGS_t + L^BCRA_t - DEP_t ) / PIB4T_t * 100

    N_t   : Letras adquiridas por el BCRA, valor nominal residual (miles de USD
            -> millones), Ministerio de Economia / Secretaria de Finanzas,
            "Deuda Publica, Estado de la Deuda" (datos/crudos/mecon_deuda/*), hoja
            A.1.9 (A.1.10/A.1.11 en 2013-2017, bloque "LETRAS ADQUIRIDAS POR EL
            BCRA"; A.12.3 "LETRA INTRANSFERIBLE" en 2007-2010).
    L^ME  : tenencia del BCRA en moneda extranjera segun balance (libros).
    TC_t  : tipo de cambio del dataset de deuda consolidada (MECON A.2.4).
Todo lo demas (B, T^FGS, L^BCRA, DEP, PIB4T) se reutiliza sin cambios del CSV de
la serie contable. Donde no hay dato nominal (hasta 2005T4) se conserva el valor
contable y se marca ``flag_nominal_disponible = 0``.

Cobertura de N_t (las planillas MECON son de cierre de ano, mas 2010T1):
  - Anclas: 2007-12, 2008-12, 2009-12, 2010-03, 2013-12 ... 2025-12. NO hay planilla
    para 2010-12, 2011-12 ni 2012-12 en el repositorio.
  - Trimestres entre dos anclas A y B (B posterior):
      * ``reconstruccion_emisiones``: si todo instrumento de A sigue en B con el mismo
        monto (las Letras son bullet, sin amortizacion), el stock es el de A mas los
        instrumentos de B emitidos hasta el cierre del trimestre (fecha de emision
        publicada). Exacto salvo cancelaciones/emisiones intra-trimestre invisibles.
      * ``interpolacion_lineal``: si hubo bajas o cambios de monto entre A y B (canjes,
        vencimientos, ampliaciones sin fecha publicada) se interpola linealmente el stock
        total en USD entre las dos anclas. Es una aproximacion explicita y marcada.
  - 2006T1-2007T3: reconstruccion hacia atras con la unica Letra emitida el 2006-01-03
    (aparece en la planilla 2007-12 y es la primera emision de la serie).
  - <= 2005T4: sin dato nominal -> valor contable.

Uso:  python codigo/ingesta_datos/construir_deuda_consolidada_neta_nominal_1996_2025.py
"""
from __future__ import annotations

import datetime
import glob
import pathlib
import re
import sys
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

BASE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import construir_deuda_consolidada_neta_1996_2025 as v2  # noqa: E402  (FMI, nombres de columnas)

RAW_MECON = BASE / "datos" / "crudos" / "mecon_deuda"
PROC = BASE / "datos" / "procesados"
NETA_CSV = PROC / "deuda_consolidada_neta_1996_2025.csv"
GROSS_CSV = PROC / "deuda_consolidada_1996_2025.csv"
OUT_CSV = PROC / "deuda_consolidada_neta_nominal_1996_2025.csv"
OUT_LETRAS = PROC / "letras_intransferibles_bcra_nominal_anclas.csv"
OUT_CTRL = PROC / "deuda_consolidada_neta_nominal_1996_2025_control_fmi.csv"
BLOQUE = "LETRAS ADQUIRIDAS POR EL BCRA"
TOL_REL = 1e-6


def _fecha_archivo(path: str) -> pd.Timestamp:
    """Fecha de corte desde el nombre 'deuda_publica_DD-MM-AAAA...'."""
    m = re.search(r"(\d{2})-(\d{2})-(\d{4})", pathlib.Path(path).name)
    if not m:
        raise ValueError(f"Nombre sin fecha: {path}")
    return pd.Timestamp(f"{m.group(3)}-{m.group(2)}-{m.group(1)}")


def parse_letras(path: str) -> pd.DataFrame:
    """Instrumentos de Letras Intransferibles del BCRA en una planilla MECON.

    Planillas 2013+: filas posteriores al encabezado ``LETRAS ADQUIRIDAS POR EL BCRA``
    hasta el primer rubro siguiente. Planillas 2007-2010: filas 'LETRA INTRANSFERIBLE'
    de la hoja A.12.3. Montos en miles de USD (original, residual, actualizado).
    """
    x = pd.ExcelFile(path)
    fecha = _fecha_archivo(path)
    rows: List[dict] = []
    for sh in x.sheet_names:
        d = x.parse(sh, header=None)
        blk = d.apply(lambda c: c.astype(str).str.contains(BLOQUE, case=False)).any(axis=1)
        if blk.any():
            start, modo = int(d.index[blk][0]) + 1, "bloque"
        elif sh == "A.12.3":
            start, modo = 0, "viejo"
        else:
            continue
        visto = False
        for i in range(start, len(d)):
            r = d.loc[i].dropna().tolist()
            if not r:
                continue
            es_instr = len(r) >= 7 and isinstance(r[0], datetime.datetime)
            if modo == "bloque":
                if es_instr:
                    visto = True
                elif visto:
                    break
                else:
                    continue
            elif not (es_instr and "INTRANSFERIBLE" in str(r[1]).upper()):
                continue
            rows.append({"fecha_corte": fecha, "hoja": sh, "emision": pd.Timestamp(r[0]), "denominacion": str(r[1]).strip(),
                         "orig": float(r[-3]), "resid": float(r[-2]), "actual": float(r[-1])})
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out = out.sort_values(["emision", "resid"], ascending=[True, False]).reset_index(drop=True)
    out["orden"] = out.groupby("emision").cumcount()
    out["clave"] = out["emision"].dt.strftime("%Y-%m-%d") + "#" + out["orden"].astype(str)
    return out


def load_anchors() -> Tuple[Dict[pd.Timestamp, pd.DataFrame], pd.DataFrame]:
    """Una tabla de instrumentos por fecha de corte y el resumen (stock USD mm) por ancla."""
    anchors: Dict[pd.Timestamp, pd.DataFrame] = {}
    for f in sorted(glob.glob(str(RAW_MECON / "deuda_publica_*"))):
        t = parse_letras(f)
        if not t.empty:
            anchors[t["fecha_corte"].iloc[0]] = t
    res = pd.DataFrame({
        "n_instrumentos": {k: len(v) for k, v in anchors.items()},
        "nominal_residual_usd_mm": {k: v["resid"].sum() / 1e3 for k, v in anchors.items()},
        "nominal_original_usd_mm": {k: v["orig"].sum() / 1e3 for k, v in anchors.items()},
        "nominal_actualizado_usd_mm": {k: v["actual"].sum() / 1e3 for k, v in anchors.items()},
    }).sort_index()
    res.index.name = "fecha_corte"
    return anchors, res


def quarterly_nominal(anchors: Dict[pd.Timestamp, pd.DataFrame], idx: pd.DatetimeIndex) -> pd.DataFrame:
    """Stock nominal residual (USD mm) a fin de cada trimestre de ``idx`` con su metodo."""
    fechas = sorted(anchors)
    stock = pd.Series(np.nan, index=idx)
    metodo = pd.Series("sin_dato", index=idx, dtype=object)
    tot = {f: anchors[f]["resid"].sum() / 1e3 for f in fechas}
    # 1) quirurgico: anclas coinciden con fin de trimestre
    for f in fechas:
        if f in stock.index:
            stock[f], metodo[f] = tot[f], "ancla_oficial"
    # 2) hacia atras desde la primera ancla: solo instrumentos emitidos (todos los de la ancla)
    first = anchors[fechas[0]]
    for t in idx[idx < fechas[0]]:
        emitido = first[first["emision"] <= t]
        if t >= first["emision"].min():
            stock[t], metodo[t] = emitido["resid"].sum() / 1e3, "reconstruccion_emisiones_hacia_atras"
    # 3) entre anclas consecutivas
    for a, b in zip(fechas[:-1], fechas[1:]):
        A, B = anchors[a].set_index("clave"), anchors[b].set_index("clave")
        sin_bajas = set(A.index) <= set(B.index)
        mismo_monto = sin_bajas and bool(
            np.all(np.abs(A["resid"].values - B.loc[A.index, "resid"].values) <= TOL_REL * np.maximum(A["resid"].values, 1.0)))
        for t in idx[(idx > a) & (idx < b)]:
            if sin_bajas and mismo_monto:
                nuevos = B.loc[~B.index.isin(A.index)]
                stock[t] = (A["resid"].sum() + nuevos.loc[nuevos["emision"] <= t, "resid"].sum()) / 1e3
                metodo[t] = "reconstruccion_emisiones"
            else:
                w = (t - a).days / (b - a).days
                stock[t] = (1 - w) * tot[a] + w * tot[b]
                metodo[t] = "interpolacion_lineal"
    return pd.DataFrame({"nominal_letras_usd_mm": stock, "nominal_metodo": metodo})


def main() -> None:
    anchors, res = load_anchors()
    res.round(3).to_csv(OUT_LETRAS)
    base = pd.read_csv(NETA_CSV, index_col=0, parse_dates=True)
    gross = pd.read_csv(GROSS_CSV, index_col=0, parse_dates=True)
    idx = base.index
    df = base.copy()
    df["tc_ars_usd"] = gross["tc_ars_usd"].reindex(idx)
    nom = quarterly_nominal(anchors, idx)
    df = df.join(nom)
    disp = df["nominal_letras_usd_mm"].notna()
    df["flag_nominal_disponible"] = disp.astype(int)
    df["flag_nominal_interpolado"] = (df["nominal_metodo"] == "interpolacion_lineal").astype(int)
    df["nominal_letras_ars_mm"] = df["nominal_letras_usd_mm"] * df["tc_ars_usd"]
    # Sustituye el componente ME del balance por el nominal donde hay dato
    df["bcra_tenencia_tesoro_nominal_ars_mm"] = np.where(
        disp, df["bcra_tenencia_tesoro_ars_mm"] - df["bcra_letras_me_ars_mm"] + df["nominal_letras_ars_mm"],
        df["bcra_tenencia_tesoro_ars_mm"])
    # Variante "piso contable": nunca baja la tenencia por debajo del libro; solo agrega el
    # faltante donde el nominal de las Letras supera al componente ME del balance. Se cubre
    # asi la posibilidad de que el componente ME del balance incluya otras tenencias en USD
    # (ratio libros/nominal > 1 en 2014-2023) que la sustitucion estricta eliminaria.
    df["bcra_tenencia_tesoro_nominal_piso_ars_mm"] = np.where(
        disp, df["bcra_tenencia_tesoro_ars_mm"] + np.maximum(df["nominal_letras_ars_mm"] - df["bcra_letras_me_ars_mm"], 0.0),
        df["bcra_tenencia_tesoro_ars_mm"])
    pib = df["pib_4t_mm"]
    df["tenencia_bcra_tesoro_nominal_piso_pib"] = df["bcra_tenencia_tesoro_nominal_piso_ars_mm"] / pib * 100
    df["deuda_consolidada_neta_nominal_piso_pib"] = (
        df["bruta_federal_pib"] - df["tenencia_bcra_tesoro_nominal_piso_pib"] + df["pasivos_bcra_pib"] - df["dep_tesoro_bcra_pib"])
    df["tenencia_bcra_tesoro_nominal_pib"] = df["bcra_tenencia_tesoro_nominal_ars_mm"] / pib * 100
    df["deuda_consolidada_neta_nominal_pib"] = (
        df["bruta_federal_pib"] - df["tenencia_bcra_tesoro_nominal_pib"] + df["pasivos_bcra_pib"] - df["dep_tesoro_bcra_pib"])
    df["deuda_consolidada_neta_libros_pib"] = df["deuda_consolidada_neta_pib"]
    df["dif_nominal_menos_libros_pp"] = df["deuda_consolidada_neta_nominal_pib"] - df["deuda_consolidada_neta_libros_pib"]
    df["libros_me_usd_mm"] = df["bcra_letras_me_ars_mm"] / df["tc_ars_usd"]
    df["ratio_libros_me_sobre_nominal"] = df["libros_me_usd_mm"] / df["nominal_letras_usd_mm"]
    cols = ["bruta_federal_pib", "tenencia_bcra_tesoro_pib", "tenencia_bcra_tesoro_nominal_pib", "pasivos_bcra_pib",
            "dep_tesoro_bcra_pib", "deuda_consolidada_neta_libros_pib", "deuda_consolidada_neta_nominal_pib",
            "deuda_consolidada_neta_nominal_piso_pib", "tenencia_bcra_tesoro_nominal_piso_pib", "dif_nominal_menos_libros_pp", "flag_nominal_disponible", "flag_nominal_interpolado", "nominal_metodo",
            "nominal_letras_usd_mm", "libros_me_usd_mm", "ratio_libros_me_sobre_nominal", "tc_ars_usd",
            "flag_fgs_faltante", "flag_swap_pboc_faltante", "pib_4t_mm", "bcra_tenencia_tesoro_ars_mm",
            "bcra_letras_me_ars_mm", "bcra_tenencia_tesoro_nominal_ars_mm", "nominal_letras_ars_mm"]
    df[cols].to_csv(OUT_CSV, float_format="%.6f")
    print(f"[OK] {OUT_CSV} | trimestres con nominal: {int(disp.sum())}/{len(df)}")
    print("\nAnclas MECON (USD mm, nominal residual):\n", res.round(1).to_string())
    print("\nMetodo por trimestre:", df["nominal_metodo"].value_counts().to_dict())

    rows: List[dict] = []
    for k, f in v2.FMI.items():
        r = df.loc[pd.Timestamp(k)]
        rows.append({"fecha": k, "bruta_nuestra": r["bruta_federal_pib"], "bruta_fmi": f["bruta_total"],
                     "tenencia_bcra_libros": r["tenencia_bcra_tesoro_pib"],
                     "tenencia_bcra_nominal": r["tenencia_bcra_tesoro_nominal_pib"], "intra_publico_fmi_todo": f["intra_publico_tesoro"],
                     "neta_ex_fgs_libros": r["deuda_consolidada_neta_libros_pib"],
                     "neta_ex_fgs_nominal": r["deuda_consolidada_neta_nominal_pib"],
                     "neta_ex_fgs_nominal_piso": r["deuda_consolidada_neta_nominal_piso_pib"], "neta_fmi": f["neta"],
                     "libros_me_usd_mm": r["libros_me_usd_mm"], "nominal_usd_mm": r["nominal_letras_usd_mm"]})
    ctrl = pd.DataFrame(rows).set_index("fecha").round(2)
    ctrl.to_csv(OUT_CTRL)
    print("\nControl FMI:\n", ctrl.T.to_string())
    y = df[df.index.month == 12][["libros_me_usd_mm", "nominal_letras_usd_mm", "deuda_consolidada_neta_libros_pib",
                                  "deuda_consolidada_neta_nominal_pib", "deuda_consolidada_neta_nominal_piso_pib"]].dropna(subset=["nominal_letras_usd_mm"])
    print("\nCierres de ano (USD mm; % PIB):\n", (y / [1000, 1000, 1, 1, 1]).round(2).rename(
        columns={"libros_me_usd_mm": "libros_bn", "nominal_letras_usd_mm": "nominal_bn"}).to_string())


if __name__ == "__main__":
    main()
