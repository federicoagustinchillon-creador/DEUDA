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
    if "deuda_consolidada_pib" not in df.columns:
        if "pasivos_bcra_pib" in df.columns:
            df["deuda_consolidada_pib"] = df["deuda_pib"] + df["pasivos_bcra_pib"]
        else:
            bcra_path = BASE_DIR / "datos" / "procesados" / "bcra_pasivos_trimestral.csv"
            if bcra_path.exists():
                bcra = pd.read_csv(bcra_path, parse_dates=["fecha"], index_col="fecha")
                df["pasivos_bcra_pib"] = bcra["pasivos_bcra_pib"]
                df["deuda_consolidada_pib"] = df["deuda_pib"] + df["pasivos_bcra_pib"].fillna(0)

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

    # ------------------------------------------------------------------
    # CONFIGURACIÓN TIPOGRÁFICA Y EDITORIAL ACADÉMICA (AER / FMI)
    # ------------------------------------------------------------------
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif', 'cmr10'],
        'mathtext.fontset': 'cm',
        'axes.edgecolor': '#475569',
        'axes.linewidth': 0.8,
        'grid.color': '#E2E8F0',
        'grid.linewidth': 0.5,
        'grid.alpha': 0.7,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.unicode_minus': False
    })

    # --- Gráfico en Dos Paneles Sincronizados (SPNF vs Consolidada) ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 7.8), sharex=True, gridspec_kw={'hspace': 0.24})
    NAVY = "#1B365D"
    CRIMSON = "#8B1E1E"

    # Panel A: Deuda SPNF
    ax1.plot(df.index, df["deuda_pib"], color=NAVY, linewidth=2.0, label="Deuda SPNF / PIB")
    for seg in result_spnf["medias_segmento"].itertuples():
        ax1.hlines(seg.media, seg.inicio, seg.fin, color=NAVY, linewidth=2.6, alpha=0.65)
        mid_date = seg.inicio + (seg.fin - seg.inicio) / 2
        ax1.text(mid_date, seg.media + 2.2, rf"$\bar{{d}} = {seg.media:.1f}\%$",
                 color=NAVY, fontsize=8.5, fontweight='bold', ha='center', va='bottom',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

    for d in result_spnf["fechas_quiebre"]:
        ts = pd.Timestamp(d)
        q_label = f"{ts.year}-T{ts.quarter}"
        ax1.axvline(d, color="#64748B", linestyle="--", alpha=0.75, linewidth=1.1)
        ax1.text(d, 114, f"Quiebre:\n{q_label}", color="#334155", fontsize=8,
                 ha="center", va="top", fontweight="bold",
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='#CBD5E1', alpha=0.9))

    ax1.set_title("A. Deuda Pública del SPNF / PIB — Cronología de Quiebres Óptimos por BIC ($m^* = 3$)",
                  fontweight="bold", fontsize=10.5, pad=8, color="#0F172A", loc="left")
    ax1.set_ylabel("% del PIB", fontweight="bold", fontsize=9.5)
    ax1.set_ylim(20, 126)
    ax1.legend(fontsize=8.5, loc="lower left", frameon=False)
    ax1.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0", axis="y")

    # Panel B: Deuda Consolidada
    ax2.plot(df.index, df["deuda_consolidada_pib"], color=CRIMSON, linewidth=2.0,
             label="Deuda Consolidada SPNF + Pasivos BCRA / PIB")
    for seg in result_cons["medias_segmento"].itertuples():
        ax2.hlines(seg.media, seg.inicio, seg.fin, color=CRIMSON, linewidth=2.6, alpha=0.65)
        mid_date = seg.inicio + (seg.fin - seg.inicio) / 2
        ax2.text(mid_date, seg.media + 2.2, rf"$\bar{{d}} = {seg.media:.1f}\%$",
                 color=CRIMSON, fontsize=8.5, fontweight='bold', ha='center', va='bottom',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

    for d in result_cons["fechas_quiebre"]:
        ts = pd.Timestamp(d)
        q_label = f"{ts.year}-T{ts.quarter}"
        ax2.axvline(d, color="#64748B", linestyle="--", alpha=0.75, linewidth=1.1)
        ax2.text(d, 126, f"Quiebre:\n{q_label}", color="#334155", fontsize=8,
                 ha="center", va="top", fontweight="bold",
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='#CBD5E1', alpha=0.9))

    ax2.set_title("B. Deuda Pública Consolidada (SPNF + Pasivos BCRA) / PIB — Quiebres Óptimos por BIC ($m^* = 2$)",
                  fontweight="bold", fontsize=10.5, pad=8, color="#0F172A", loc="left")
    ax2.set_xlabel("Trimestre", fontweight="bold", fontsize=10)
    ax2.set_ylabel("% del PIB", fontweight="bold", fontsize=9.5)
    ax2.set_ylim(20, 138)
    ax2.legend(fontsize=8.5, loc="lower left", frameon=False)
    ax2.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0", axis="y")

    fig.suptitle("Detección de Quiebres Estructurales Múltiples de Bai-Perron (2004–2025)",
                 fontweight="bold", fontsize=12, y=0.98)

    # Nota metodológica elegante al pie
    fig.text(0.08, 0.012,
             "Nota: Algoritmo de programación dinámica de Bai y Perron (2003) con recorte h=13 (15% muestral). "
             "Las líneas punteadas verticales indican las fechas estimadas de quiebre;\n"
             "las barras horizontales identifican la media del ratio de deuda correspondiente a cada segmento macrofiscal estable.",
             fontsize=8, color="#475569", style="italic")

    fig.tight_layout(rect=[0, 0.04, 1, 0.95])
    out_path = LATEX_DIR / "figura_9_1_bai_perron.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"\n[OK] Gráfico: {out_path}")
    print("\n[OK] Fase 9 completa.")


if __name__ == "__main__":
    main()
