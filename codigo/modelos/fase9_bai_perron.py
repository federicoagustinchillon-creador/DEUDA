"""
fase9_bai_perron.py
====================
Mejora Dimensión I: contraste de quiebres estructurales múltiples de
Bai-Perron (1998, 2003) sobre la ratio Deuda/PIB, en reemplazo/complemento
del test de Zivot-Andrews de quiebre único (Fase 1), que había localizado un
candidato en 2018T1 sin poder rechazar la raíz unitaria (t=-2.83).

Implementación propia en `codigo/modelos/bai_perron.py` (programación dinámica
exacta + selección del número de quiebres por BIC), dado que no hay
interfaz de R/rpy2 disponible para invocar `strucchange::breakpoints()`.

Se aplica tanto a `deuda_pib` (serie original, SPNF) como a
`deuda_consolidada_pib` (serie de la Mejora Dimensión IV, SPNF + pasivos
remunerados del BCRA), para verificar si la consolidación cuasi-fiscal altera
la cronología de quiebres detectada.

Salidas:
  - resultados/tablas/fase9_bai_perron_bic.csv
  - resultados/tablas/fase9_bai_perron_quiebres.csv
  - tesis/figuras/figura_9_1_bai_perron.png
"""

import os
import pathlib
import pandas as pd
import matplotlib.pyplot as plt

from bai_perron import bai_perron_breaks

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
CSV_PATH = BASE_DIR / "datos" / "dataset_consolidado_real.csv"
LATEX_DIR = BASE_DIR / "tesis" / "figuras"
TABLES_DIR = BASE_DIR / "resultados" / "tablas"
os.makedirs(TABLES_DIR, exist_ok=True)


def analyze_series(df, col, label, max_breaks=5, trimming=0.15):
    print(f"\n[Bai-Perron] Serie: {label} ({col})")
    result = bai_perron_breaks(df[col], max_breaks=max_breaks, trimming=trimming)
    print(f" -> Recorte h = {result['trimming_h']} observaciones por segmento (trimming={trimming:.0%})")
    print(result["bic_por_m"].round(2).to_string(index=False))
    print(f" -> Número de quiebres seleccionado por BIC: m* = {result['m_optimo']}")
    for d in result["fechas_quiebre"]:
        print(f"    - Quiebre en {pd.Timestamp(d).strftime('%Y-%m')}")
    segmentos_fmt = result["medias_segmento"].copy()
    segmentos_fmt["inicio"] = segmentos_fmt["inicio"].dt.strftime("%Y-%m")
    segmentos_fmt["fin"] = segmentos_fmt["fin"].dt.strftime("%Y-%m")
    print(segmentos_fmt.round(2).to_string(index=False))
    return result


def main():
    print("=" * 75)
    print(" FASE 9: Quiebres Estructurales Múltiples de Bai-Perron")
    print("=" * 75)

    df = pd.read_csv(CSV_PATH, parse_dates=["Date"], index_col="Date")

    result_spnf = analyze_series(df, "deuda_pib", "Deuda SPNF / PIB (original)")
    result_cons = analyze_series(df, "deuda_consolidada_pib",
                                  "Deuda Consolidada SPNF + BCRA / PIB (Mejora Dim. IV)")

    bic_rows = []
    for label, res in [("deuda_pib", result_spnf), ("deuda_consolidada_pib", result_cons)]:
        d = res["bic_por_m"].copy()
        d["serie"] = label
        bic_rows.append(d)
    pd.concat(bic_rows, ignore_index=True).to_csv(TABLES_DIR / "fase9_bai_perron_bic.csv", index=False)

    break_rows = []
    for label, res in [("deuda_pib", result_spnf), ("deuda_consolidada_pib", result_cons)]:
        for d in res["fechas_quiebre"]:
            break_rows.append({"serie": label, "fecha_quiebre": pd.Timestamp(d).strftime("%Y-%m-%d")})
    pd.DataFrame(break_rows).to_csv(TABLES_DIR / "fase9_bai_perron_quiebres.csv", index=False)

    result_spnf["medias_segmento"].assign(serie="deuda_pib").to_csv(
        TABLES_DIR / "fase9_bai_perron_segmentos_deuda_pib.csv", index=False)
    result_cons["medias_segmento"].assign(serie="deuda_consolidada_pib").to_csv(
        TABLES_DIR / "fase9_bai_perron_segmentos_deuda_consolidada.csv", index=False)

    # --- Gráfico ---
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(df.index, df["deuda_pib"], color="#0B3C5D", linewidth=1.6, label="Deuda SPNF / PIB")
    ax.plot(df.index, df["deuda_consolidada_pib"], color="#B33951", linewidth=1.6,
            linestyle="--", label="Deuda Consolidada SPNF + BCRA / PIB")

    for seg in result_spnf["medias_segmento"].itertuples():
        ax.hlines(seg.media, seg.inicio, seg.fin, color="#0B3C5D", linewidth=3, alpha=0.35)
    for d in result_spnf["fechas_quiebre"]:
        ax.axvline(d, color="#0B3C5D", linestyle=":", alpha=0.6)
        ax.text(d, ax.get_ylim()[1] * 0.97, pd.Timestamp(d).strftime("%Y-%m"),
                rotation=90, fontsize=8, color="#0B3C5D", va="top", ha="right")

    for d in result_cons["fechas_quiebre"]:
        ax.axvline(d, color="#B33951", linestyle=":", alpha=0.4)

    ax.set_title("Quiebres Estructurales Múltiples de Bai-Perron (selección por BIC)")
    ax.set_xlabel("Trimestre")
    ax.set_ylabel("% del PIB")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_path = LATEX_DIR / "figura_9_1_bai_perron.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"\n[OK] Gráfico: {out_path}")
    print("\n[OK] Fase 9 completa.")


if __name__ == "__main__":
    main()
