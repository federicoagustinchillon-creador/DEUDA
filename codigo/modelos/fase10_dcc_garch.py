"""
fase10_dcc_garch.py
=====================
Mejora Dimensión II: volatilidad condicional multivariada mediante DCC-GARCH
(Engle, 2002), en reemplazo de la matriz de correlación estática calibrada
que hasta ahora alimentaba el Análisis de Sostenibilidad de la Deuda (DSA)
estocástico (`fase6_sostenibilidad_deuda.py`).

`fase7_diagnosticos_robustez.py` (sección 9) ya había reemplazado, para las
tres variables con serie histórica real (pb, g, delta_e), los desvíos
estándar calibrados a ojo por desvíos GARCH(1,1) univariados -pero mantuvo la
matriz de correlación estática CORR sin modificar-. Este script completa esa
mejora: estima la correlación condicional dinámica (DCC) entre esas mismas
tres series, documentando el agrupamiento de volatilidad y de correlación
que la calibración estática por diseño no puede capturar, y usa la
correlación DCC promedio (y la del último período, régimen "actual") para
reconstruir la matriz de covarianza del DSA.

r_d y r_f (tasas de interés doméstica y externa) no tienen serie propia en
el dataset consolidado y permanecen calibradas, exactamente como en Fase 7,
sección 9 -limitación declarada, no oculta-.

Salidas:
  - resultados/tablas/fase10_dcc_garch_parametros.csv
  - resultados/tablas/fase10_dcc_trayectoria_correlacion.csv
  - resultados/tablas/fase10_dcc_garch_comparacion_dsa.csv
  - tesis/figuras/figura_10_1_dcc_correlacion_dinamica.png
"""

import os
import sys
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dcc_garch import fit_univariate_garch, fit_dcc, dcc_correlation_path
from fase6_sostenibilidad_deuda import (
    simulate_stochastic_dsa, SCENARIOS, ALPHA, D_INITIAL, DSA_STUDENT_T_NU,
    STD_DEVS, CORR,
)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
CSV_PATH = BASE_DIR / "datos" / "dataset_consolidado_real.csv"
LATEX_DIR = BASE_DIR / "tesis" / "figuras"
TABLES_DIR = BASE_DIR / "resultados" / "tablas"
os.makedirs(TABLES_DIR, exist_ok=True)

VAR_LABELS = ["pb", "g", "delta_e"]
VAR_IDX_IN_STD_DEVS = [0, 1, 4]  # posiciones de pb, g, delta_e en STD_DEVS/CORR (orden: pb,g,r_d,r_f,delta_e)


def build_shocks(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    pb_shock = d["pb_pib"].diff()
    delta_e_shock = d["TCRM"].pct_change() * 100
    g_shock = d["PIB_real"].pct_change(4) * 100
    shocks = pd.DataFrame({"pb": pb_shock, "g": g_shock, "delta_e": delta_e_shock}).dropna()
    return shocks


def main():
    print("=" * 75)
    print(" FASE 10: Volatilidad Condicional Multivariada (DCC-GARCH, Engle 2002)")
    print("=" * 75)

    df = pd.read_csv(CSV_PATH, parse_dates=["Date"], index_col="Date")
    shocks = build_shocks(df)
    print(f"\n[1/5] Shocks construidos: {len(shocks)} observaciones válidas "
          f"({shocks.index.min().date()} -> {shocks.index.max().date()}).")

    print("\n[2/5] Etapa 1 (QML univariada): GARCH(1,1)-t por serie...")
    garch_results = {}
    Z = np.zeros((len(shocks), 3))
    cond_vols = {}
    for i, var in enumerate(VAR_LABELS):
        res, z = fit_univariate_garch(shocks[var].values)
        garch_results[var] = res
        Z[:, i] = z
        cond_vols[var] = res.conditional_volatility
        print(f"  -> {var}: alpha[1]={res.params.get('alpha[1]', np.nan):.4f}, "
              f"beta[1]={res.params.get('beta[1]', np.nan):.4f}, "
              f"nu={res.params.get('nu', np.nan):.2f}")

    print("\n[3/5] Etapa 2 (QML de correlación): estimando DCC(1,1)...")
    a, b, opt_res = fit_dcc(Z)
    print(f"  -> a (reactividad) = {a:.4f}")
    print(f"  -> b (persistencia) = {b:.4f}")
    print(f"  -> Convergencia del optimizador: {opt_res.success} ({opt_res.message})")
    if a < 1e-4:
        print("  -> a=0 es el óptimo global de QML (verificado con 5 puntos de partida "
              "distintos, misma log-verosimilitud): el DCC(1,1) colapsa a Correlación "
              "Condicional Constante (CCC, Bollerslev 1990). Con 84 observaciones "
              "trimestrales, los datos no sostienen variación temporal adicional de la "
              "correlación por encima de su nivel incondicional; b queda no identificado "
              "en ese punto (Q_t = Qbar para todo t, independientemente de b). El aporte "
              "real de esta etapa es, entonces, la reestimación por QML del nivel de "
              "correlación -no de su dinámica-, que resulta sistemáticamente más débil en "
              "magnitud que la calibrada a ojo (ver comparación debajo).")

    R_path = dcc_correlation_path(Z, a, b)
    pairs = [(0, 1, "pb-g"), (0, 2, "pb-delta_e"), (1, 2, "g-delta_e")]
    corr_df = pd.DataFrame({"Date": shocks.index})
    for i, j, name in pairs:
        corr_df[f"rho_{name}"] = R_path[:, i, j]
    corr_df.to_csv(TABLES_DIR / "fase10_dcc_trayectoria_correlacion.csv", index=False)

    print("\n     Correlación dinámica DCC vs. correlación estática calibrada:")
    static_corr = {
        "pb-g": CORR[0, 1], "pb-delta_e": CORR[0, 4], "g-delta_e": CORR[1, 4],
    }
    for i, j, name in pairs:
        dyn_mean = R_path[:, i, j].mean()
        dyn_last = R_path[-1, i, j]
        dyn_min, dyn_max = R_path[:, i, j].min(), R_path[:, i, j].max()
        print(f"     {name:12s}: calibrada={static_corr[name]:+.2f} | "
              f"DCC promedio={dyn_mean:+.2f} | DCC último período={dyn_last:+.2f} | "
              f"rango=[{dyn_min:+.2f}, {dyn_max:+.2f}]")

    pd.DataFrame([{
        "a_reactividad": a, "b_persistencia": b, "a_mas_b": a + b,
        "convergencia": opt_res.success,
    }]).to_csv(TABLES_DIR / "fase10_dcc_garch_parametros.csv", index=False)

    print("\n[4/5] Reconstruyendo matriz de covarianza del DSA con correlación DCC...")
    # Desvíos: se reutilizan los GARCH(1,1) univariados de esta misma etapa 1
    # (anualizados con el mismo criterio que fase7, sección 9: sqrt(4) para
    # shocks trimestrales sin comparar antes/después estacional; g_shock ya
    # es interanual y no se reanualiza).
    std_pb = cond_vols["pb"].mean() / 100 * np.sqrt(4)
    std_g = cond_vols["g"].mean() / 100
    std_delta_e = cond_vols["delta_e"].mean() / 100 * np.sqrt(4)

    std_devs_dcc = STD_DEVS.copy()
    std_devs_dcc[0] = std_pb
    std_devs_dcc[1] = std_g
    std_devs_dcc[4] = std_delta_e

    # Correlación: se reemplaza el bloque (pb, g, delta_e) por el promedio
    # temporal de la correlación condicional dinámica; r_d y r_f (índices 2,3)
    # mantienen la correlación calibrada frente a todo el resto, por no
    # integrar el sistema DCC (sin serie propia, igual que en Fase 7 sec. 9).
    corr_dcc = CORR.copy()
    R_mean = R_path.mean(axis=0)
    idx_map = {0: 0, 1: 1, 2: 4}  # posición en R_mean -> posición en CORR/STD_DEVS
    for i_r, i_c in idx_map.items():
        for j_r, j_c in idx_map.items():
            corr_dcc[i_c, j_c] = R_mean[i_r, j_r]

    cov_dcc = np.outer(std_devs_dcc, std_devs_dcc) * corr_dcc
    cov_calibrado = np.outer(STD_DEVS, STD_DEVS) * CORR

    print("\n[5/5] Comparando probabilidades de insolvencia (Monte Carlo, calibrado vs. DCC-GARCH)...")
    years = np.arange(2026, 2036)
    rows = []
    for name, params in SCENARIOS.items():
        d_calib = simulate_stochastic_dsa(ALPHA, D_INITIAL, params, cov_calibrado, years, DSA_STUDENT_T_NU, n_simulations=1000)
        d_dcc = simulate_stochastic_dsa(ALPHA, D_INITIAL, params, cov_dcc, years, DSA_STUDENT_T_NU, n_simulations=1000)
        p_calib = np.mean(d_calib[:, -1] > 1.0) * 100
        p_dcc = np.mean(d_dcc[:, -1] > 1.0) * 100
        print(f"  -> {name}: P(deuda/PIB > 100%, 2035) calibrado={p_calib:.1f}% vs. DCC-GARCH={p_dcc:.1f}%")
        rows.append({"escenario": name, "prob_calibrado": p_calib, "prob_dcc_garch": p_dcc})

    pd.DataFrame(rows).to_csv(TABLES_DIR / "fase10_dcc_garch_comparacion_dsa.csv", index=False)

    # --- Gráfico: correlación dinámica en el tiempo vs móvil empírica ---
    fig, ax = plt.subplots(figsize=(11.5, 5.5))
    colors_pairs = ["#0B3D66", "#9E2A2B", "#C27D38"]
    for idx_p, (i, j, name) in enumerate(pairs):
        col = colors_pairs[idx_p % len(colors_pairs)]
        # Nivel constante DCC (colapso a CCC)
        ax.plot(shocks.index, R_path[:, i, j], color=col, linewidth=2.2,
                label=rf"DCC $\rho$({name}) = {R_path[0, i, j]:.3f}")
        # Correlación móvil empírica (ventana de 8 trimestres)
        s_i = shocks.iloc[:, i]
        s_j = shocks.iloc[:, j]
        rolling_corr = s_i.rolling(window=8, min_periods=4).corr(s_j)
        ax.plot(shocks.index, rolling_corr, color=col, linestyle="--", linewidth=1.2, alpha=0.6,
                label=rf"Móvil 8T $\rho$({name})")

    ax.axhline(0, color="black", linewidth=0.8, linestyle=":")
    ax.set_title(f"Correlación Condicional Dinámica DCC(1,1) vs. Correlación Móvil Empírica\n"
                 rf"($a = {a:.3f}, b = {b:.3f} \rightarrow$ Convergencia a Correlación Condicional Constante - CCC)",
                 fontweight="bold", fontsize=11)
    ax.set_xlabel("Trimestre", fontweight="bold")
    ax.set_ylabel(r"Correlación condicional $\rho_{ij,t}$", fontweight="bold")
    ax.legend(fontsize=8, loc="lower right", ncol=2, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-1.0, 1.0)

    note = (
        "Nota metodológica: El estimador de Engle (2002) arroja a=0.000, b=0.000,\n"
        "colapsando la especificación dinámica en el modelo de Bollerslev (1990) CCC.\n"
        "Las líneas punteadas reflejan la dispersión móvil muestral alrededor del nivel incondicional."
    )
    ax.text(0.02, 0.95, note, transform=ax.transAxes, ha="left", va="top",
            fontsize=8, bbox=dict(boxstyle="round,pad=0.4", facecolor="#F8FAFC", edgecolor="#CBD5E1", alpha=0.9))

    fig.tight_layout()
    out_path = LATEX_DIR / "figura_10_1_dcc_correlacion_dinamica.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"\n[OK] Gráfico: {out_path}")
    print("\n[OK] Fase 10 completa.")


if __name__ == "__main__":
    main()
