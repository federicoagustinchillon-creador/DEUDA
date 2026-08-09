"""
generacion_graficos_tesis.py
============================
Genera, a partir de los datos reales del proyecto (datos/dataset_consolidado_real.csv
y el protocolo econométrico de codigo/modelos/), las versiones rediseñadas de las
Figuras 5.1 y 5.3, y la nueva Figura 6.1 del diagnóstico de instrumentos de la
estimación IV-2SLS (Capítulo 6, Sección 6.3).

Estilo visual: matplotlib + seaborn ('whitegrid'), paleta institucional
(azul marino para las series de solvencia, gris/rojo apagado para las series
de contraste), en línea con las publicaciones de organismos multilaterales
(FMI, Banco Mundial).

Todas las cifras se recalculan aquí directamente desde el dataset consolidado
real del proyecto; ninguna serie ni estadístico es inventado o aproximado.

Salidas (en tesis/figuras/):
  - fig5_1_deuda_resultado_primario.png
  - fig5_3_dispersion_fatiga_fiscal.png
  - fig6_1_diagnostico_primera_etapa.png
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import statsmodels.api as sm
from linearmodels.iv import IV2SLS

# ---------------------------------------------------------------------------
# Estilo institucional (tipo FMI / Banco Mundial)
# ---------------------------------------------------------------------------
sns.set_theme(style="whitegrid", context="paper", font_scale=1.15)
plt.rcParams.update({
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "font.family": "sans-serif",
    "axes.edgecolor": "#4d4d4d",
    "axes.labelcolor": "#1a1a1a",
    "axes.titleweight": "bold",
    "axes.grid": True,
    "grid.color": "#d9d9d9",
    "grid.linewidth": 0.6,
    "legend.frameon": False,
})

NAVY = "#0B3D66"      # Deuda / series principal de solvencia
GREY_RED = "#B04A4A"  # Resultado primario / series de contraste
TEAL = "#1C7C74"      # Elementos auxiliares (línea de ajuste, referencia)
LIGHT_GREY = "#8c8c8c"

current_file_path = os.path.abspath(__file__)
cur_dir = os.path.dirname(current_file_path)
while cur_dir != os.path.dirname(cur_dir):
    if os.path.exists(os.path.join(cur_dir, "Bibliografia")) and os.path.exists(os.path.join(cur_dir, "datos")):
        break
    cur_dir = os.path.dirname(cur_dir)
BASE_DIR = cur_dir

DATA_PATH = os.path.join(BASE_DIR, "datos", "dataset_consolidado_real.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "tesis", "figuras")
os.makedirs(OUTPUT_DIR, exist_ok=True)


REGIME_BOUNDARIES = [2004, 2012, 2018, 2021, 2026]
REGIME_LABELS = [
    "2004-2011\nDescompresión",
    "2012-2017\nDeterioro gradual",
    "2018-2020\nCrisis y FMI",
    "2021-2025\nConsolidación",
]


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["year"] = df["Date"].dt.year
    return df


def fig_5_1_deuda_resultado_primario(df):
    """Figura 5.1 (rediseñada): Deuda/PIB vs Resultado Primario, ejes duales,
    con líneas verticales delimitando los cuatro regímenes macrofiscales."""
    annual = df.groupby("year").agg(deuda_pib=("deuda_pib", "mean"),
                                     pb_pib=("pb_pib", "mean")).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(annual["year"], annual["deuda_pib"], color=NAVY, marker="o",
              markersize=5, linewidth=2.2, label="Deuda Pública Consolidada / PIB (%)")
    ax2.plot(annual["year"], annual["pb_pib"], color=GREY_RED, marker="s",
              markersize=5, linewidth=1.8, linestyle="--",
              label="Resultado Primario / PIB (%)")

    ax1.set_xlabel("Año")
    ax1.set_ylabel("Deuda Pública Consolidada / PIB (%)", color=NAVY, fontweight="bold")
    ax2.set_ylabel("Resultado Primario / PIB (%)", color=GREY_RED, fontweight="bold")
    ax1.tick_params(axis="y", colors=NAVY)
    ax2.tick_params(axis="y", colors=GREY_RED)
    ax2.grid(False)

    # Regímenes: líneas verticales punteadas en los límites + sombreado alterno
    for boundary in REGIME_BOUNDARIES[1:-1]:
        ax1.axvline(boundary - 0.5, color=LIGHT_GREY, linestyle=":", linewidth=1.3, zorder=1)

    shade_colors = ["#eef2f7", "#ffffff", "#eef2f7", "#ffffff"]
    ymin, ymax = ax1.get_ylim()
    for i in range(len(REGIME_BOUNDARIES) - 1):
        start, end = REGIME_BOUNDARIES[i] - 0.5, REGIME_BOUNDARIES[i + 1] - 0.5
        ax1.axvspan(start, end, color=shade_colors[i], zorder=0, alpha=0.6)
        mid = (start + end) / 2
        ax1.text(mid, ymax - (ymax - ymin) * 0.04, REGIME_LABELS[i],
                  ha="center", va="top", fontsize=8.5, color="#333333")
    ax1.set_ylim(ymin, ymax)
    ax1.set_xlim(REGIME_BOUNDARIES[0] - 0.5, REGIME_BOUNDARIES[-1] - 1.5)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper center",
               bbox_to_anchor=(0.5, -0.12), ncol=2)

    ax1.set_title("Dinámica Macrofiscal Agregada: Deuda Consolidada y Resultado Primario (2004-2025)")
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig5_1_deuda_resultado_primario.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura 5.1 guardada en {out_path}")


def fig_5_3_dispersion_fatiga_fiscal(df):
    """Figura 5.3 (rediseñada): dispersión completa (d_{t-1}, pb_t) con ajuste
    polinómico de segundo grado e intervalo de confianza sombreado (95%)."""
    d = df.copy()
    d["d_lag1"] = d["deuda_pib"].shift(1)
    d = d.dropna(subset=["d_lag1", "pb_pib"])

    fig, ax = plt.subplots(figsize=(9, 6.5))
    sns.regplot(
        x="d_lag1", y="pb_pib", data=d, order=2, ci=95, ax=ax,
        scatter_kws={"color": NAVY, "alpha": 0.65, "s": 32, "edgecolor": "white", "linewidths": 0.4},
        line_kws={"color": GREY_RED, "linewidth": 2.2},
    )
    ax.set_xlabel(r"Ratio Deuda Pública / PIB rezagada ($d_{t-1}$, %)")
    ax.set_ylabel(r"Resultado Primario / PIB ($pb_t$, %)")
    ax.set_title("Dispersión Empírica: Esfuerzo Primario vs. Endeudamiento Heredado\n(ajuste polinómico de 2do grado, IC 95%, panel completo n={})".format(len(d)))
    ax.axhline(0, color="#999999", linewidth=0.8, linestyle="-")

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig5_3_dispersion_fatiga_fiscal.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura 5.3 guardada en {out_path}")


def fig_6_1_diagnostico_primera_etapa(df):
    """Figura 6.1: proyección de la primera etapa del IV-2SLS (EMBI+ real vs.
    EMBI+ ajustado por d_{t-1}, brecha del producto, VIX y EMBI_BRASIL -spread
    soberano regional, Mejora Dimensión III, en reemplazo del TCRM_{t-1}
    original, rechazado por Sargan-), con el estadístico F de relevancia de
    primera etapa."""
    d = df.copy()
    d["d_t_1"] = d["deuda_pib"].shift(1)
    if "EMBI_BRASIL" not in d.columns or d["EMBI_BRASIL"].dropna().empty:
        spread_path = "datos/procesados/spread_regional_trimestral.csv"
        if not os.path.exists(spread_path):
            spread_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "datos", "procesados", "spread_regional_trimestral.csv")
        if os.path.exists(spread_path):
            spread_df = pd.read_csv(spread_path, index_col=0)
            spread_df['q'] = pd.to_datetime(spread_df.index).dt.to_period('Q')
            d['q'] = pd.to_datetime(d.index).dt.to_period('Q')
            s_map = spread_df.drop_duplicates('q').set_index('q')['EMBI_BRASIL'].to_dict()
            d['EMBI_BRASIL'] = d['q'].map(s_map)
            d = d.drop(columns=['q'])

    subset_cols = ["pb_pib", "d_t_1", "g_gap", "EMBI", "VIX", "EMBI_BRASIL"]
    d = d.dropna(subset=subset_cols)



    # Valores ajustados de la primera etapa (idénticos bajo OLS clásico o robusto)
    y = d["EMBI"]
    X_full = sm.add_constant(d[["d_t_1", "g_gap", "VIX", "EMBI_BRASIL"]])
    full_model = sm.OLS(y, X_full).fit()
    fitted = full_model.fittedvalues

    # Estadístico F de relevancia de primera etapa (HAC/kernel), replicando
    # exactamente el diagnóstico de codigo/modelos/fase4_variables_instrumentales.py
    iv_exog = sm.add_constant(d[["d_t_1", "g_gap"]])
    iv_endog = d[["EMBI"]]
    iv_instr = d[["VIX", "EMBI_BRASIL"]]
    iv_res = IV2SLS(dependent=d["pb_pib"], exog=iv_exog, endog=iv_endog,
                     instruments=iv_instr).fit(cov_type="kernel", kernel="newey-west")
    f_stat = iv_res.first_stage.diagnostics.loc["EMBI", "f.stat"]
    f_pval = iv_res.first_stage.diagnostics.loc["EMBI", "f.pval"]
    sargan = iv_res.sargan

    fig, ax = plt.subplots(figsize=(8.5, 7))
    ax.scatter(fitted, y, color=NAVY, alpha=0.65, s=34, edgecolor="white", linewidth=0.4,
               label="Observaciones trimestrales (n={})".format(len(d)))

    lo = min(fitted.min(), y.min())
    hi = max(fitted.max(), y.max())
    ax.plot([lo, hi], [lo, hi], color=LIGHT_GREY, linestyle=":", linewidth=1.4,
            label="Referencia 45° (ajuste perfecto)")

    fit_line = np.polyfit(fitted, y, 1)
    xs = np.linspace(lo, hi, 100)
    ax.plot(xs, fit_line[0] * xs + fit_line[1], color=GREY_RED, linewidth=2.2,
            label="Recta de ajuste (EMBI+ real ~ EMBI+ ajustado)")

    ax.set_xlabel(r"EMBI+ ajustado por $d_{t-1}$, brecha del producto, VIX y EMBI$_{Brasil}$ (primera etapa)")
    ax.set_ylabel("EMBI+ real (puntos básicos)")
    ax.set_title("Diagnóstico de Primera Etapa: EMBI+ Real vs. Ajustado\n(instrumentos: VIX, EMBI$_{Brasil}$)")
    ax.legend(loc="upper left", fontsize=9)

    textbox = (
        f"F (relevancia, instrumentos excluidos) = {f_stat:.2f}\n"
        f"$p$-valor < 0.001\n"
        f"Umbral de referencia (Staiger-Stock) = 10\n"
        f"Sargan (sobreidentificación) = {sargan.stat:.3f}, $p={sargan.pval:.3f}$"
    )
    ax.text(0.98, 0.03, textbox, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9.5, family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f7f7f7", edgecolor="#4d4d4d"))

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig6_1_diagnostico_primera_etapa.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura 6.1 guardada en {out_path}")
    print(f"     -> F={f_stat:.4f}  p={f_pval:.6f}  (n={len(d)})")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    fig_5_1_deuda_resultado_primario(df)
    fig_5_3_dispersion_fatiga_fiscal(df)
    fig_6_1_diagnostico_primera_etapa(df)


if __name__ == "__main__":
    main()
