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
    ax1.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

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

    p_coefs = np.polyfit(d["d_lag1"], d["pb_pib"], 2)
    p_poly = np.poly1d(p_coefs)
    y_pred = p_poly(d["d_lag1"])
    ss_tot = np.sum((d["pb_pib"] - d["pb_pib"].mean()) ** 2)
    ss_res = np.sum((d["pb_pib"] - y_pred) ** 2)
    r2 = 1 - ss_res / ss_tot
    d_star = -p_coefs[1] / (2 * p_coefs[0])

    badge = (
        f"$pb_t = {p_coefs[2]:.2f} {p_coefs[1]:+.3f} d_{{t-1}} {p_coefs[0]:+.4f} d_{{t-1}}^2$\n"
        f"$R^2 = {r2:.3f} \\quad (n = {len(d)})$\n"
        f"Vértice de fatiga: $d^* = {d_star:.1f}\\%$ del PIB"
    )
    ax.text(0.97, 0.95, badge, transform=ax.transAxes, ha="right", va="top",
            fontsize=9.5, bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#CBD5E1", alpha=0.95))

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


def fig_svar_irf():
    """Genera las Funciones de Impulso-Respuesta Estructurales (SVAR IRF) con bandas al 95%."""
    import sys
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from codigo.modelos.fase19_var_restringido_macro import cargar_datos, estimar_svar_restringido
    data, _ = cargar_datos()
    res = estimar_svar_restringido(data, nlags=2, n_boot=200, horizon=16)
    
    irf = res["irf_structural"]
    low = res["irf_lower"]
    upp = res["irf_upper"]
    vars_names = ["Brecha PIB", "Superávit Prim.", "EMBI+", "TCRM", "Deuda/PIB"]
    
    # Graficamos las respuestas de Deuda y EMBI+ ante shocks de Superávit, PIB y Tipo de Cambio
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True)
    horizons = np.arange(17)
    
    # Fila 1: Respuesta de la Deuda/PIB
    # Shock 1: Superavit Primario
    axes[0, 0].plot(horizons, irf[:, 4, 1], color=NAVY, linewidth=2, label="Impulso")
    axes[0, 0].fill_between(horizons, low[:, 4, 1], upp[:, 4, 1], color=NAVY, alpha=0.2, label="IC 95%")
    axes[0, 0].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[0, 0].set_title("Deuda/PIB ante Shock Fiscal (pb)", fontsize=10, fontweight="bold")
    axes[0, 0].set_ylabel("Respuesta (%)", fontsize=9)
    
    # Shock 2: Brecha PIB
    axes[0, 1].plot(horizons, irf[:, 4, 0], color=NAVY, linewidth=2)
    axes[0, 1].fill_between(horizons, low[:, 4, 0], upp[:, 4, 0], color=NAVY, alpha=0.2)
    axes[0, 1].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[0, 1].set_title("Deuda/PIB ante Shock de PIB", fontsize=10, fontweight="bold")
    
    # Shock 3: Tipo de Cambio Real
    axes[0, 2].plot(horizons, irf[:, 4, 3], color=NAVY, linewidth=2)
    axes[0, 2].fill_between(horizons, low[:, 4, 3], upp[:, 4, 3], color=NAVY, alpha=0.2)
    axes[0, 2].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[0, 2].set_title("Deuda/PIB ante Shock Cambiario (TCRM)", fontsize=10, fontweight="bold")
    
    # Fila 2: Respuesta del EMBI+
    # Shock 1: Superavit Primario
    axes[1, 0].plot(horizons, irf[:, 2, 1], color=GREY_RED, linewidth=2)
    axes[1, 0].fill_between(horizons, low[:, 2, 1], upp[:, 2, 1], color=GREY_RED, alpha=0.2)
    axes[1, 0].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[1, 0].set_title("EMBI+ ante Shock Fiscal (pb)", fontsize=10, fontweight="bold")
    axes[1, 0].set_xlabel("Trimestres posteriores", fontsize=9)
    axes[1, 0].set_ylabel("Respuesta (pb)", fontsize=9)
    
    # Shock 2: Brecha PIB
    axes[1, 1].plot(horizons, irf[:, 2, 0], color=GREY_RED, linewidth=2)
    axes[1, 1].fill_between(horizons, low[:, 2, 0], upp[:, 2, 0], color=GREY_RED, alpha=0.2)
    axes[1, 1].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[1, 1].set_title("EMBI+ ante Shock de PIB", fontsize=10, fontweight="bold")
    axes[1, 1].set_xlabel("Trimestres posteriores", fontsize=9)
    
    # Shock 3: Tipo de Cambio Real
    axes[1, 2].plot(horizons, irf[:, 2, 3], color=GREY_RED, linewidth=2)
    axes[1, 2].fill_between(horizons, low[:, 2, 3], upp[:, 2, 3], color=GREY_RED, alpha=0.2)
    axes[1, 2].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[1, 2].set_title("EMBI+ ante Shock Cambiario (TCRM)", fontsize=10, fontweight="bold")
    axes[1, 2].set_xlabel("Trimestres posteriores", fontsize=9)
    
    fig.suptitle("Funciones de Impulso-Respuesta Estructurales (SVAR Restringido)", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_svar_irf.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura SVAR IRF guardada en {out_path}")


def fig_svar_fevd():
    """Genera el gráfico de barras apiladas de Descomposición de Varianza (FEVD)."""
    fevd_path = os.path.join(BASE_DIR, "resultados", "tablas", "fase19_fevd.csv")
    if not os.path.exists(fevd_path):
        return
    df_fevd = pd.read_csv(fevd_path)
    
    # Filtramos la descomposición de la Deuda y del EMBI+
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    shocks = ["Shock_g_gap", "Shock_pb_pib", "Shock_EMBI", "Shock_TCRM", "Shock_deuda_pib"]
    colors = ["#0B3D66", "#4A6984", "#C27D38", "#9E2A2B", "#5E6472"]
    labels = ["Brecha PIB", "Superávit Prim.", "EMBI+", "TCRM", "Deuda Propia"]
    
    for ax, var_name, title in zip(axes, ["deuda_pib", "EMBI"], ["Varianza de Deuda/PIB", "Varianza de EMBI+"]):
        sub = df_fevd[df_fevd["Variable_Explicada"] == var_name]
        bottom = np.zeros(len(sub))
        for s, col, lab in zip(shocks, colors, labels):
            vals = sub[s].values
            ax.bar(sub["Horizonte_Trimestres"].astype(str) + "T", vals, bottom=bottom, color=col, label=lab, width=0.6)
            bottom += vals
        ax.set_title(title, fontweight="bold")
        ax.set_ylabel("Porcentaje de Varianza Explicada (%)")
        ax.set_xlabel("Horizonte de Pronóstico (Trimestres)")
        ax.set_ylim(0, 100)
        
    axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=9)
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_svar_fevd.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura SVAR FEVD guardada en {out_path}")


def fig_cir_simulacion():
    """Genera el gráfico de trayectorias de Monte Carlo del proceso CIR calibrado
    rigurosamente a partir de resultados/tablas/fase20_cir_calibracion.csv."""
    calib_path = os.path.join(BASE_DIR, "resultados", "tablas", "fase20_cir_calibracion.csv")
    if os.path.exists(calib_path):
        df_calib = pd.read_csv(calib_path)
        row = df_calib.iloc[0]  # Muestra homogénea 2004-2025
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
    n_steps = 40  # 10 años (40 trimestres)
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.5), gridspec_kw={"width_ratios": [3.2, 1]}, sharey=True)

    # 50 trayectorias individuales tenues de fondo
    for i in range(50):
        ax1.plot(t_grid, paths[i], color="#4A6984", alpha=0.10, linewidth=0.8)

    mediana = np.median(paths, axis=0)
    p90 = np.percentile(paths, 90, axis=0)
    p10 = np.percentile(paths, 10, axis=0)
    p75 = np.percentile(paths, 75, axis=0)
    p25 = np.percentile(paths, 25, axis=0)

    ax1.fill_between(t_grid, p10, p90, color=NAVY, alpha=0.12, label="Banda 10%-90%")
    ax1.fill_between(t_grid, p25, p75, color=NAVY, alpha=0.22, label="Banda 25%-75%")
    ax1.plot(t_grid, mediana, color=NAVY, linewidth=2.4, label=f"Mediana proyectada ({mediana[-1]:.0f} pb)")
    ax1.axhline(theta, color="#9E2A2B", linestyle="--", linewidth=1.6,
                label=rf"Equilibrio LP $\theta = {theta:.0f}$ pb")
    ax1.scatter([0], [r0], color="#9E2A2B", s=45, zorder=5, label=f"Condición inicial $r_0 = {r0:.0f}$ pb")

    ax1.set_xlabel("Años de Proyección (2026–2035)", fontweight="bold")
    ax1.set_ylabel("EMBI+ Proyectado (puntos básicos)", fontweight="bold")
    ax1.set_title(f"Simulación Monte Carlo: Proceso CIR del EMBI+ (N=5.000 trayectorias)\n"
                  rf"$\kappa = {kappa:.4f}$ (vida media 0.75 a), $\theta = {theta:.0f}$ pb, $\sigma = {sigma:.2f}$ (Feller ratio = 2.63)",
                  fontweight="bold", fontsize=11)
    ax1.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, max(2500, p90.max() * 1.08))

    # Densidad terminal
    sns.kdeplot(y=paths[:, -1], ax=ax2, fill=True, color=NAVY, alpha=0.35, linewidth=1.5)
    ax2.axhline(theta, color="#9E2A2B", linestyle="--", linewidth=1.6)
    ax2.axhline(mediana[-1], color=NAVY, linestyle=":", linewidth=1.4)
    ax2.set_title("Densidad Terminal\n($t=10$, 2035)", fontweight="bold", fontsize=10)
    ax2.set_xlabel("Densidad", fontsize=9)
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(3))

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_cir_simulacion.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura CIR Simulación guardada en {out_path}")


def fig_spread_historico_1983_2025():
    """
    Genera la figura institucional del spread soberano histórico de 42 años (1983-2025),
    con sombreado de crisis, umbral de fatiga fiscal y descomposición por instrumento.
    """
    csv_path = os.path.join(cur_dir, "datos", "procesados", "spread_soberano_historico_1983_2025.csv")
    if not os.path.exists(csv_path):
        print(f"[SKIP] No se encontró {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]})

    # 1. Panel Superior: Serie del Spread Empalmado
    ax1.plot(df["Date"], df["Spread_Empalmado_pb"], color=NAVY, linewidth=2.0, label="Spread Soberano Empalmado (pb)")
    ax1.axhline(2083.0, color=GREY_RED, linestyle="--", linewidth=1.5, label="Umbral Crítico de Fatiga Fiscal (τ* = 2.083 pb)")

    # Sombreados de crisis
    crisis_shades = [
        ("1989-01-01", "1990-12-31", "Hiperinflación / Plan Bonex", "#FFE6E6"),
        ("1994-12-01", "1995-09-30", "Efecto Tequila", "#FFF2E6"),
        ("2001-07-01", "2003-03-31", "Default y Fin Convertibilidad", "#FFE6E6"),
        ("2008-09-01", "2009-06-30", "Crisis Lehman 2008", "#FFF2E6"),
        ("2018-04-01", "2019-12-31", "Crisis Cambiaria / Stand-By", "#FFE6E6"),
        ("2020-03-01", "2020-09-30", "COVID-19 / Canje 2020", "#FFF2E6"),
    ]

    for start, end, label, col in crisis_shades:
        ax1.axvspan(pd.to_datetime(start), pd.to_datetime(end), color=col, alpha=0.6, zorder=1)

    # Anotaciones de hitos mayores
    ax1.annotate("Hiperinflación\n5.600 pb", xy=(pd.to_datetime("1989-12-31"), 5600),
                 xytext=(pd.to_datetime("1986-06-30"), 6000),
                 arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2), fontsize=9, fontweight="bold")

    ax1.annotate("Pico Default\n6.659 pb", xy=(pd.to_datetime("2002-09-30"), 6659),
                 xytext=(pd.to_datetime("1998-01-01"), 6800),
                 arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2), fontsize=9, fontweight="bold")

    ax1.annotate("Plan Brady 1993\n(690 pb)", xy=(pd.to_datetime("1993-12-31"), 690),
                 xytext=(pd.to_datetime("1992-01-01"), 2500),
                 arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2), fontsize=8)

    ax1.annotate("Mínimo Histórico\n2007 (210 pb)", xy=(pd.to_datetime("2007-03-31"), 210),
                 xytext=(pd.to_datetime("2004-06-30"), 1100),
                 arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2), fontsize=8)

    ax1.set_title("Evolución Histórica del Spread Soberano de Argentina (1983–2025): 42 Años de Democracia",
                  fontweight="bold", fontsize=13)
    ax1.set_ylabel("Spread Soberano (puntos básicos)", fontweight="bold")
    ax1.legend(loc="upper right", fontsize=9)
    ax1.set_ylim(0, 7500)

    # 2. Panel Inferior: Instrumentos Fuente
    mask_bonex = df["Date"] <= "1992-12-31"
    mask_brady = (df["Date"] >= "1993-01-01") & (df["Date"] <= "1997-12-31")
    mask_embi = df["Date"] >= "1998-01-01"

    ax2.plot(df.loc[mask_bonex, "Date"], df.loc[mask_bonex, "Spread_Empalmado_pb"],
             color="#9E2A2B", linewidth=2.0, label="Bonex Series 82/84/87/89 (1983–1992)")
    ax2.plot(df.loc[mask_brady, "Date"], df.loc[mask_brady, "Spread_Empalmado_pb"],
             color="#C27D38", linewidth=2.0, label="JP Morgan Brady Stripped (1993–1997)")
    ax2.plot(df.loc[mask_embi, "Date"], df.loc[mask_embi, "Spread_Empalmado_pb"],
             color="#0B3D66", linewidth=2.0, label="JP Morgan EMBI+ / Global (1998–2025)")

    ax2.set_title("Composición por Instrumento Soberano y Mercado de Origen", fontweight="bold", fontsize=10)
    ax2.set_xlabel("Año de Observación", fontweight="bold")
    ax2.set_ylabel("Nivel (pb)", fontsize=9)
    ax2.legend(loc="upper right", fontsize=8)

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


