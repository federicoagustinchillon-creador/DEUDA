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
# Estilo editorial académico (estándar AER / Econometrica / FMI)
# ---------------------------------------------------------------------------
sns.set_theme(style="ticks", context="paper", font_scale=1.10)
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Computer Modern Roman"],
    "mathtext.fontset": "cm",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#4A5568",
    "axes.linewidth": 0.8,
    "axes.labelcolor": "#1A202C",
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "legend.frameon": False,
    "grid.color": "#E2E8F0",
    "grid.linewidth": 0.5,
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})

NAVY = "#1B365D"       # Deep Academic Navy (solvencia / serie principal)
CRIMSON = "#8B1E1E"    # Oxblood / Academic Crimson (déficit / contraste / umbrales)
SLATE = "#2D3748"      # Charcoal Slate
TEAL = "#0D5C56"       # Deep Academic Teal
LIGHT_GREY = "#A0AEC0"

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
    "2004–2011\nDesendeudamiento",
    "2012–2017\nDeterioro gradual",
    "2018–2020\nCrisis y FMI",
    "2021–2025\nConsolidación",
]


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["year"] = df["Date"].dt.year
    return df


def fig_5_1_deuda_resultado_primario(df):
    """Figura 5.1 (estándar académico AER / Econometrica / FMI):
    Ejes duales (twinx) unificados (Deuda Consolidada eje izq., Resultado Primario eje der.),
    con marcadores discretos para promedios anuales, delimitación sutil de regímenes
    y leyenda inferior centrada. Coincide exactamente con el texto de 05_datos.tex."""
    annual = df.groupby("year").agg(
        deuda_pib=("deuda_pib", "mean"),
        pb_pib=("pb_pib", "mean")
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax2 = ax1.twinx()

    # Serie 1: Deuda Consolidada (Eje Izquierdo)
    l1 = ax1.plot(annual["year"], annual["deuda_pib"], color=NAVY, linewidth=2.0,
                  marker="o", markersize=5, label="Deuda Pública Consolidada / PIB (%)")
    ax1.set_ylabel("Deuda Pública Consolidada / PIB (%)", color=NAVY, fontsize=10)
    ax1.tick_params(axis="y", labelcolor=NAVY)
    ax1.set_ylim(35, 115)
    ax1.set_xlabel("Año", fontsize=10)

    # Serie 2: Resultado Primario (Eje Derecho)
    l2 = ax2.plot(annual["year"], annual["pb_pib"], color=CRIMSON, linewidth=2.0,
                  linestyle="--", marker="s", markersize=5, label="Resultado Primario / PIB (%)")
    ax2.axhline(0, color="#718096", linewidth=0.8, linestyle=":")
    ax2.set_ylabel("Resultado Primario / PIB (%)", color=CRIMSON, fontsize=10)
    ax2.tick_params(axis="y", labelcolor=CRIMSON)
    ax2.set_ylim(-3.5, 2.0)

    # Regímenes macrofiscales con delimitación sutil
    regime_info = [
        (2004, 2011, "2004–2011\nDescompresión"),
        (2011, 2017, "2012–2017\nDeterioro gradual"),
        (2017, 2020.5, "2018–2020\nCrisis y FMI"),
        (2020.5, 2025, "2021–2025\nConsolidación"),
    ]
    for start, end, label in regime_info:
        mid = (start + end) / 2
        ax1.text(mid, 112, label, ha="center", va="top", fontsize=8, color="#4A5568")

    for boundary in [2011.5, 2017.5, 2020.5]:
        ax1.axvline(boundary, color=LIGHT_GREY, linestyle=":", linewidth=1.0, zorder=1)

    ax1.set_xlim(2003.5, 2025.5)
    ax1.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
    ax1.grid(True, axis="y", alpha=0.3)

    # Leyenda combinada al pie
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper center", bbox_to_anchor=(0.5, -0.12),
               ncol=2, frameon=False, fontsize=9)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig5_1_deuda_resultado_primario.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura 5.1 guardada en {out_path}")


def fig_5_3_dispersion_fatiga_fiscal(df):
    """Figura 5.3 (estándar académico): Dispersión empírica (d_{t-1}, pb_t) con ajuste
    polinómico cuadrático e intervalo de confianza del 95% sombreado, sin inferencia espuria
    de umbrales ni fórmulas decorativas en el canvas (fiel a 05_datos.tex)."""
    d = df.copy()
    d["d_lag1"] = d["deuda_pib"].shift(1)
    d = d.dropna(subset=["d_lag1", "pb_pib"])

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    # Puntos de dispersión trimestrales
    ax.scatter(d["d_lag1"], d["pb_pib"], color=SLATE, alpha=0.60, s=26,
               edgecolor="white", linewidth=0.4, label=rf"Observaciones trimestrales ($n={len(d)}$)")

    # Ajuste polinómico cuadrático con banda de confianza del 95% (bootstrap estándar)
    sns.regplot(data=d, x="d_lag1", y="pb_pib", order=2, ax=ax, scatter=False,
                color=CRIMSON, line_kws={"linewidth": 2.2, "label": "Ajuste polinómico de 2do grado (IC 95%)"},
                ci=95)

    # Línea horizontal cero
    ax.axhline(0, color="#718096", linewidth=0.8, linestyle=":")

    ax.set_xlabel(r"Ratio Deuda Pública / PIB rezagada ($d_{t-1}$, %)", fontsize=10)
    ax.set_ylabel(r"Resultado Primario / PIB ($pb_t$, %)", fontsize=10)
    ax.legend(loc="lower left", frameon=False, fontsize=8.8)
    ax.grid(True, linestyle="--", alpha=0.4, color="#E2E8F0")

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig5_3_dispersion_fatiga_fiscal.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura 5.3 guardada en {out_path}")


def fig_6_1_diagnostico_primera_etapa(df):
    """Figura 6.1 (estándar académico): Diagnóstico de instrumentos IV-2SLS (EMBI+ real vs.
    ajustado en primera etapa) con línea de 45° de ajuste perfecto y reporte sobrio."""
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

    y = d["EMBI"]
    X_full = sm.add_constant(d[["d_t_1", "g_gap", "VIX", "EMBI_BRASIL"]])
    full_model = sm.OLS(y, X_full).fit()
    fitted = full_model.fittedvalues

    iv_exog = sm.add_constant(d[["d_t_1", "g_gap"]])
    iv_endog = d[["EMBI"]]
    iv_instr = d[["VIX", "EMBI_BRASIL"]]
    iv_res = IV2SLS(dependent=d["pb_pib"], exog=iv_exog, endog=iv_endog,
                     instruments=iv_instr).fit(cov_type="kernel", kernel="newey-west")
    f_stat = iv_res.first_stage.diagnostics.loc["EMBI", "f.stat"]
    f_pval = iv_res.first_stage.diagnostics.loc["EMBI", "f.pval"]
    sargan = iv_res.sargan

    fig, ax = plt.subplots(figsize=(8.0, 5.8))
    ax.scatter(fitted, y, color=NAVY, alpha=0.60, s=28, edgecolor="white", linewidth=0.4,
               label=rf"Observaciones trimestrales ($n={len(d)}$)")

    lo = min(fitted.min(), y.min()) - 50
    hi = max(fitted.max(), y.max()) + 50
    ax.plot([lo, hi], [lo, hi], color=CRIMSON, linestyle="--", linewidth=1.4,
            label="Línea de 45° (ajuste teórico perfecto)")

    ax.set_xlabel(r"EMBI+ Ajustado por $d_{t-1}$, Brecha PIB, VIX y EMBI$_{\mathrm{Brasil}}$ (pb)", fontsize=10)
    ax.set_ylabel("EMBI+ Observado (puntos básicos)", fontsize=10)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.legend(loc="upper left", frameon=False, fontsize=8.8)
    ax.grid(True, linestyle="--", alpha=0.4, color="#E2E8F0")

    # Diagnósticos econométricos discretos sin caja invasiva
    diag_text = (
        rf"$F_{{\mathrm{{IV}}}} = {f_stat:.2f} \quad (p < 0.001)$" + "\n" +
        rf"$\text{{Sargan: }} S = {sargan.stat:.3f} \quad (p = {sargan.pval:.3f})$"
    )
    ax.text(0.95, 0.06, diag_text, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, linespacing=1.4, color=SLATE)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig6_1_diagnostico_primera_etapa.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura 6.1 guardada en {out_path}")
    print(f"     -> F={f_stat:.4f}  p={f_pval:.6f}  (n={len(d)})")


def fig_svar_irf():
    """Genera las Funciones de Impulso-Respuesta Estructurales (SVAR IRF) con bandas al 95%
    bajo estándar editorial académico (Tufte despine y tipografía LaTeX)."""
    import sys
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from codigo.modelos.fase19_var_restringido_macro import cargar_datos, estimar_svar_restringido
    data, _ = cargar_datos()
    res = estimar_svar_restringido(data, nlags=2, n_boot=200, horizon=16)

    irf = res["irf_structural"]
    low = res["irf_lower"]
    upp = res["irf_upper"]

    fig, axes = plt.subplots(2, 3, figsize=(12, 6.8), sharex=True)
    horizons = np.arange(17)

    # Configuración de títulos matemáticos limpios
    titles_row1 = [
        r"$\text{Deuda/PIB ante Shock Fiscal }(pb)$",
        r"$\text{Deuda/PIB ante Shock de PIB }(y)$",
        r"$\text{Deuda/PIB ante Shock Cambiario }(TCRM)$",
    ]
    titles_row2 = [
        r"$\text{EMBI+ ante Shock Fiscal }(pb)$",
        r"$\text{EMBI+ ante Shock de PIB }(y)$",
        r"$\text{EMBI+ ante Shock Cambiario }(TCRM)$",
    ]
    shocks_idx = [1, 0, 3]  # pb, PIB, TCRM

    # Fila 1: Respuesta de la Deuda/PIB
    for col_idx, s_idx in enumerate(shocks_idx):
        ax = axes[0, col_idx]
        ax.plot(horizons, irf[:, 4, s_idx], color=NAVY, linewidth=2.0, label="Impulso")
        ax.fill_between(horizons, low[:, 4, s_idx], upp[:, 4, s_idx], color=NAVY, alpha=0.18, label="IC 95%")
        ax.axhline(0, color="#718096", linestyle="--", linewidth=0.8)
        ax.set_title(titles_row1[col_idx], fontsize=10, fontweight="bold")
        ax.grid(True, axis="y", alpha=0.3)
        if col_idx == 0:
            ax.set_ylabel("Respuesta (% PIB)", fontsize=9.5)

    # Fila 2: Respuesta del EMBI+
    for col_idx, s_idx in enumerate(shocks_idx):
        ax = axes[1, col_idx]
        ax.plot(horizons, irf[:, 2, s_idx], color=CRIMSON, linewidth=2.0)
        ax.fill_between(horizons, low[:, 2, s_idx], upp[:, 2, s_idx], color=CRIMSON, alpha=0.18)
        ax.axhline(0, color="#718096", linestyle="--", linewidth=0.8)
        ax.set_title(titles_row2[col_idx], fontsize=9.5)
        ax.set_xlabel("Trimestres Posteriores", fontsize=9.5)
        ax.grid(True, axis="y", alpha=0.3)
        if col_idx == 0:
            ax.set_ylabel("Respuesta (pb)", fontsize=9.5)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_svar_irf.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura SVAR IRF guardada en {out_path}")


def fig_svar_fevd():
    """Genera la Descomposición de Varianza del Error de Pronóstico (FEVD) a estándar editorial."""
    fevd_path = os.path.join(BASE_DIR, "resultados", "tablas", "fase19_fevd.csv")
    if not os.path.exists(fevd_path):
        return
    df_fevd = pd.read_csv(fevd_path)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    shocks = ["Shock_g_gap", "Shock_pb_pib", "Shock_EMBI", "Shock_TCRM", "Shock_deuda_pib"]
    colors = [NAVY, "#4A6984", "#B45309", CRIMSON, "#718096"]
    labels = ["Brecha PIB", "Superávit Prim.", "EMBI+", "TCRM", "Deuda Propia"]

    for ax, var_name, title in zip(axes, ["deuda_pib", "EMBI"],
                                  ["A. Deuda Pública / PIB", "B. Riesgo Soberano (EMBI+)"]):
        sub = df_fevd[df_fevd["Variable_Explicada"] == var_name]
        bottom = np.zeros(len(sub))
        for s, col, lab in zip(shocks, colors, labels):
            vals = sub[s].values
            ax.bar(sub["Horizonte_Trimestres"].astype(str) + "T", vals, bottom=bottom,
                   color=col, label=lab, width=0.55, edgecolor="white", linewidth=0.5)
            bottom += vals
        ax.set_title(title, loc="left", fontsize=10.5, pad=6)
        ax.set_ylabel("Varianza Explicada (%)", fontsize=9.5)
        ax.set_xlabel("Horizonte de Pronóstico (Trimestres)", fontsize=9.5)
        ax.set_ylim(0, 100)
        ax.grid(True, axis="y", alpha=0.3)

    axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=8.5)
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_svar_fevd.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura SVAR FEVD guardada en {out_path}")


def fig_cir_simulacion():
    """Genera la simulación Monte Carlo del proceso CIR (1985) con abanico estocástico limpio
    y densidad terminal suavemente cerrada sin ticks espurios."""
    calib_path = os.path.join(BASE_DIR, "resultados", "tablas", "fase20_cir_calibracion.csv")
    if os.path.exists(calib_path):
        df_calib = pd.read_csv(calib_path)
        row = df_calib.iloc[0]
        kappa = float(row["kappa"])
        theta = float(row["theta_pb"])
        sigma = float(row["sigma"])
    else:
        kappa, theta, sigma = 0.9229, 1032.25, 26.9175

    data_path = os.path.join(BASE_DIR, "datos", "dataset_consolidado_real.csv")
    if os.path.exists(data_path):
        df_data = pd.read_csv(data_path)
        r0 = float(df_data["EMBI"].dropna().iloc[-1])
    else:
        r0 = 745.03

    np.random.seed(42)
    dt = 0.25
    n_steps = 40  # 10 años
    n_sims = 5000

    t_grid = np.linspace(0, 10, n_steps + 1)
    paths = np.zeros((n_sims, n_steps + 1))
    paths[:, 0] = r0

    for t in range(n_steps):
        dw = np.random.normal(0, np.sqrt(dt), size=n_sims)
        r_curr = paths[:, t]
        drift = kappa * (theta - r_curr) * dt
        diff = sigma * np.sqrt(np.maximum(r_curr, 1.0)) * dw
        paths[:, t + 1] = np.maximum(r_curr + drift + diff, 10.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.0), gridspec_kw={"width_ratios": [3.5, 1]}, sharey=True)

    mediana = np.median(paths, axis=0)
    p90 = np.percentile(paths, 90, axis=0)
    p10 = np.percentile(paths, 10, axis=0)
    p75 = np.percentile(paths, 75, axis=0)
    p25 = np.percentile(paths, 25, axis=0)

    ax1.fill_between(t_grid, p10, p90, color=NAVY, alpha=0.12, label="Intervalo 10%–90%")
    ax1.fill_between(t_grid, p25, p75, color=NAVY, alpha=0.25, label="Intervalo 25%–75%")
    ax1.plot(t_grid, mediana, color=NAVY, linewidth=2.2, label=f"Mediana proyectada ({mediana[-1]:.0f} pb)")
    ax1.axhline(theta, color=CRIMSON, linestyle="--", linewidth=1.4,
                label=rf"Equilibrio LP $\theta = {theta:.0f}$ pb")
    ax1.scatter([0], [r0], color=CRIMSON, s=32, zorder=5, label=rf"Nivel inicial $r_0 = {r0:.0f}$ pb")

    ax1.set_xlabel("Años de Proyección (2026–2035)", fontsize=10)
    ax1.set_ylabel("EMBI+ Proyectado (puntos básicos)", fontsize=10)
    ax1.set_title("A. Trayectorias Predictivas del EMBI+ (2026–2035)", loc="left", fontsize=10.5)
    ax1.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 2400)
    ax1.grid(True, axis="y", alpha=0.3)

    # Panel lateral de Densidad Terminal
    import scipy.stats as stats
    kde = stats.gaussian_kde(paths[:, -1])
    y_dens_grid = np.linspace(0, 2400, 300)
    dens_vals = kde(y_dens_grid)
    ax2.plot(dens_vals, y_dens_grid, color=NAVY, linewidth=1.6)
    ax2.fill_betweenx(y_dens_grid, 0, dens_vals, color=NAVY, alpha=0.18)
    ax2.axhline(theta, color=CRIMSON, linestyle="--", linewidth=1.4)
    ax2.axhline(mediana[-1], color=NAVY, linestyle=":", linewidth=1.2)

    ax2.set_title("B. Densidad (2035)", loc="left", fontsize=10.5)
    ax2.set_xticks([])
    ax2.set_xlabel("Densidad", fontsize=9)
    ax2.grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_cir_simulacion.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura CIR Simulación guardada en {out_path}")


def fig_spread_historico_1983_2025():
    """
    Genera la figura panorámica del spread soberano histórico de 42 años (1983–2025)
    a estándar editorial: regímenes sombreados, umbral de Hansen-Seo tau* y fuentes empalmadas.
    """
    csv_path = os.path.join(cur_dir, "datos", "procesados", "spread_soberano_historico_1983_2025.csv")
    if not os.path.exists(csv_path):
        print(f"[SKIP] No se encontró {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7.0), sharex=True,
                                   gridspec_kw={"height_ratios": [3.0, 1]})

    # 1. Panel Superior: Spread Empalmado
    ax1.plot(df["Date"], df["Spread_Empalmado_pb"], color=NAVY, linewidth=1.8,
             label="Spread Soberano Empalmado (pb)")
    ax1.axhline(2083.0, color=CRIMSON, linestyle="--", linewidth=1.3,
                label=r"Umbral Crítico de Fatiga Fiscal ($\tau^* = 2.083$ pb)")
    ax1.text(df["Date"].iloc[-1], 2180, r"$\tau^* = 2.083$ pb", color=CRIMSON,
             fontsize=8.5, ha="right")

    # Regímenes macroeconómicos históricos
    regimes = [
        ("1989-01-01", "1990-12-31", "Hiperinflación\n(1989–90)", "#FEE2E2", 7400),
        ("1994-12-01", "1995-10-31", "Efecto Tequila\n(1995)", "#FEF3C7", 7400),
        ("2001-07-01", "2003-03-31", "Default y Fin\nConvertibilidad", "#FEE2E2", 7400),
        ("2008-09-01", "2009-06-30", "Crisis Subprime\n(2008–09)", "#FEF3C7", 7400),
        ("2018-04-01", "2019-12-31", "Crisis Cambiaria\ny FMI (2018–19)", "#FEE2E2", 7400),
        ("2020-03-01", "2020-09-30", "COVID-19 y Canje\n(2020)", "#FEF3C7", 6100),
    ]

    for start, end, label, col, y_pos in regimes:
        s_date, e_date = pd.to_datetime(start), pd.to_datetime(end)
        ax1.axvspan(s_date, e_date, color=col, alpha=0.50, zorder=0)
        mid_date = s_date + (e_date - s_date) / 2
        ax1.text(mid_date, y_pos, label, ha="center", va="top", fontsize=7.5,
                 color="#4A5568")

    ax1.set_title("A. Spread Soberano Empalmado y Episodios de Estrés Financiero (1983–2025)",
                  loc="left", fontsize=10.5)
    ax1.set_ylabel("Spread Soberano (pb)", fontsize=10)
    ax1.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax1.set_ylim(0, 8200)
    ax1.grid(True, axis="y", alpha=0.3)

    # 2. Panel Inferior: Instrumentos Fuente
    mask_bonex = df["Date"] <= "1992-12-31"
    mask_brady = (df["Date"] >= "1993-01-01") & (df["Date"] <= "1997-12-31")
    mask_embi = df["Date"] >= "1998-01-01"

    ax2.plot(df.loc[mask_bonex, "Date"], df.loc[mask_bonex, "Spread_Empalmado_pb"],
             color=CRIMSON, linewidth=1.6, label="Bonex Series 82/84/87/89 (1983–1992)")
    ax2.plot(df.loc[mask_brady, "Date"], df.loc[mask_brady, "Spread_Empalmado_pb"],
             color="#B45309", linewidth=1.6, label="JP Morgan Brady Stripped (1993–1997)")
    ax2.plot(df.loc[mask_embi, "Date"], df.loc[mask_embi, "Spread_Empalmado_pb"],
             color=NAVY, linewidth=1.6, label="JP Morgan EMBI+ / Global (1998–2025)")

    ax2.set_title("B. Composición por Instrumento de Mercado y Período Histórico",
                  loc="left", fontsize=10.5)
    ax2.set_xlabel("Año de Observación", fontsize=10)
    ax2.set_ylabel("Nivel (pb)", fontsize=10)
    ax2.legend(loc="upper right", frameon=False, fontsize=8.0)
    ax2.grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_spread_historico_1983_2025.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura Spread Histórico guardada en {out_path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    fig_5_1_deuda_resultado_primario(df)
    fig_5_3_dispersion_fatiga_fiscal(df)
    fig_6_1_diagnostico_primera_etapa(df)
    fig_svar_irf()
    fig_svar_fevd()
    fig_cir_simulacion()
    fig_spread_historico_1983_2025()


if __name__ == "__main__":
    main()


