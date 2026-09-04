"""
fase6_sostenibilidad_deuda.py
=============================
Fase 6 del Protocolo Econométrico: Análisis de Sostenibilidad de la Deuda (DSA).

Implementa:
  - DSA Determinista (3 escenarios: Optimista, Referencia, Estrés).
  - DSA Estocástico (Monte Carlo con 1000 iteraciones) generando gráficos de abanico
    (Alineado con estándares del FMI, resolviendo HC-04).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import multivariate_t

# Configuraciones para gráficos más limpios
import seaborn as sns
sns.set_theme(style="whitegrid")

# Grados de libertad de la t de Student multivariante, estimados por método
# de momentos (nu = 4 + 6/curtosis_exceso) sobre los shocks históricos reales
# de resultado primario (curtosis en exceso=25.3 -> nu=4.24) y tipo de cambio
# real (curtosis en exceso=4.5 -> nu=5.32) -las dos series con evidencia
# robusta de colas gordas-, promediados y compartidos con el shock de
# crecimiento del PIB real (que no exhibe la misma propiedad, curtosis en
# exceso=-0.27, aproximadamente gaussiano), por el mismo criterio de
# conservadurismo del ajuste original. Se prefiere el método de momentos al
# MLE conjunto de los tres parámetros (loc, scale, nu): sobre la serie real
# de TCRM, el MLE conjunto da nu=1.54 (resultado primario) y nu=2.61 (tipo
# de cambio real) -por debajo de 2, varianza teóricamente infinita-, una
# solución de esquina arrastrada por un puñado de trimestres genuinamente
# extremos (devaluación de 2016, crisis de 2018, ajuste de 2023-2024), no un
# error de datos, pero sí un patrón de inestabilidad conocido del MLE
# conjunto sin restringir en muestras chicas con observaciones extremas
# aisladas. Ver codigo/modelos/fase17_calibracion_nu_dsa.py para el
# procedimiento completo y ambos estimadores.
DSA_STUDENT_T_NU = 4.8

# Parámetros estructurales y de escenario, expuestos a nivel de módulo para que
# scripts complementarios (p.ej. fase7_diagnosticos_robustez.py) los reutilicen por
# import en lugar de duplicarlos, evitando que ambos archivos diverjan si se
# recalibra el DSA.
ALPHA = 0.463  # Proporción de deuda en pesos (ROS)
D_INITIAL = 0.740

SCENARIOS = {
    'Optimista':  {'pb': 0.025, 'g': 0.045,  'r_d': 0.040, 'r_f': 0.055, 'delta_e': -0.020},
    'Referencia': {'pb': 0.015, 'g': 0.035,  'r_d': 0.060, 'r_f': 0.075, 'delta_e': 0.000},
    'Estrés':     {'pb': 0.005, 'g': -0.015, 'r_d': 0.120, 'r_f': 0.150, 'delta_e': 0.250},
}

# Matriz de covarianza empírica (simplificada para volatilidad argentina).
# Orden: [pb, g, r_d, r_f, delta_e]. Volatilidades (std): pb=1.5%, g=4%, r_d=5%,
# r_f=2%, delta_e=15%. Correlaciones calibradas (e.g. g cae cuando delta_e sube).
STD_DEVS = np.array([0.015, 0.040, 0.050, 0.020, 0.150])
CORR = np.array([
    [ 1.0,  0.4, -0.2, -0.1, -0.3],  # pb
    [ 0.4,  1.0, -0.4, -0.2, -0.5],  # g
    [-0.2, -0.4,  1.0,  0.5,  0.6],  # r_d
    [-0.1, -0.2,  0.5,  1.0,  0.4],  # r_f
    [-0.3, -0.5,  0.6,  0.4,  1.0],  # delta_e
])


def build_cov_matrix():
    return np.outer(STD_DEVS, STD_DEVS) * CORR

def simulate_dsa_path(alpha, d_initial, pb, g, r_d, r_f, delta_e, sf, years):
    """
    Simula una trayectoria determinista de la deuda.
    """
    d = np.zeros(len(years))
    d[0] = d_initial
    
    for i in range(1, len(years)):
        term_d = alpha * (1 + r_d[i]) / (1 + g[i])
        term_f = (1 - alpha) * (1 + r_f[i]) * (1 + delta_e[i]) / (1 + g[i])
        M = term_d + term_f
        d[i] = M * d[i-1] - pb[i] + sf[i]
        
    return d

def simulate_stochastic_dsa(alpha, d_initial, base_params, cov_matrix, years, nu=DSA_STUDENT_T_NU, n_simulations=1000):
    """
    Simula trayectorias estocásticas usando Monte Carlo.
    base_params: medias de [pb, g, r_d, r_f, delta_e]
    cov_matrix: matriz de covarianza de los shocks
    nu: grados de libertad de la t de Student multivariante de los shocks
    """
    np.random.seed(42)
    n_years = len(years)

    # Matriz para almacenar las 1000 trayectorias
    d_paths = np.zeros((n_simulations, n_years))
    d_paths[:, 0] = d_initial

    # Matriz de escala de la t multivariada: se reescala el calibrado cov_matrix
    # (Var[X] = shape * nu/(nu-2) para una t multivariada) de modo que la
    # varianza efectiva de los shocks preserve exactamente la calibración
    # histórica original, añadiendo únicamente el exceso de curtosis (colas
    # gordas) que dicha calibración gaussiana no capturaba.
    scale_matrix = cov_matrix * (nu - 2) / nu

    for s in range(n_simulations):
        # Generar shocks multivariados para todos los años (t de Student,
        # nu=5.1, en lugar de perturbaciones gaussianas puras)
        shocks = multivariate_t.rvs(loc=np.zeros(5), shape=scale_matrix, df=nu, size=n_years)

        pb_s = np.full(n_years, base_params['pb']) + shocks[:, 0]
        g_s = np.full(n_years, base_params['g']) + shocks[:, 1]
        rd_s = np.full(n_years, base_params['r_d']) + shocks[:, 2]
        rf_s = np.full(n_years, base_params['r_f']) + shocks[:, 3]
        delta_e_s = np.full(n_years, base_params['delta_e']) + shocks[:, 4]
        sf_s = np.zeros(n_years) # Stock-flow residual asumido cero en MC base
        
        for i in range(1, n_years):
            term_d = alpha * (1 + rd_s[i]) / (1 + g_s[i])
            term_f = (1 - alpha) * (1 + rf_s[i]) * (1 + delta_e_s[i]) / (1 + g_s[i])
            M = term_d + term_f
            d_paths[s, i] = M * d_paths[s, i-1] - pb_s[i] + sf_s[i]
            
    return d_paths

def main():
    print("=" * 75)
    print(" FASE 6: Proyecciones DSA (Deterministas y Estocásticas) ")
    print("=" * 75)
    
    years = np.arange(2026, 2036)
    n_years = len(years)

    # Parámetro estructural
    alpha = ALPHA

    # ------------------------------------------------------------------
    # 1. DSA DETERMINISTA
    # ------------------------------------------------------------------
    print("\n[1/2] Ejecutando DSA Determinista (3 Escenarios)...")

    def expand(val): return np.full(n_years, val)

    sf_by_scenario = {'Optimista': 0.0, 'Referencia': 0.0, 'Estrés': 0.050}

    # Escenario Optimista (D_inicial ajustado a 74% según ROS)
    p = SCENARIOS['Optimista']
    d_opt = simulate_dsa_path(alpha, D_INITIAL, expand(p['pb']), expand(p['g']), expand(p['r_d']), expand(p['r_f']), expand(p['delta_e']), expand(sf_by_scenario['Optimista']), years)

    # Escenario Referencia
    p = SCENARIOS['Referencia']
    d_ref = simulate_dsa_path(alpha, D_INITIAL, expand(p['pb']), expand(p['g']), expand(p['r_d']), expand(p['r_f']), expand(p['delta_e']), expand(sf_by_scenario['Referencia']), years)

    # Escenario Estrés
    p = SCENARIOS['Estrés']
    d_est = simulate_dsa_path(alpha, D_INITIAL, expand(p['pb']), expand(p['g']), expand(p['r_d']), expand(p['r_f']), expand(p['delta_e']), expand(sf_by_scenario['Estrés']), years)

    df_det = pd.DataFrame({
        'Año': years,
        'Optimista': d_opt,
        'Referencia': d_ref,
        'Estrés': d_est
    })
    
    print(df_det.to_string(index=False))

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(base_dir, 'tesis', 'figuras')
    os.makedirs(output_dir, exist_ok=True)

    tables_dir = os.path.join(base_dir, 'resultados', 'tablas')
    os.makedirs(tables_dir, exist_ok=True)
    df_det.to_csv(os.path.join(tables_dir, 'fase6_dsa_determinista.csv'), index=False)
    
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

    # ------------------------------------------------------------------
    # 1. DSA DETERMINISTA (DOS PANELES: ZOOM VIABLE Y DINÁMICA GLOBAL)
    # ------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), gridspec_kw={'width_ratios': [1, 1]})

    col_opt = "#1E6B38"  # Verde bosque académico
    col_ref = "#1B365D"  # Deep Navy institucional
    col_est = "#8B1E1E"  # Carmesí académico

    # Panel 1: Escenarios de Viabilidad Institucional (Optimista vs Referencia)
    ax1.plot(years, d_opt * 100, label=r'Optimista ($pb=2.5\%$, $g=4.5\%$)',
             color=col_opt, linewidth=2.2)
    ax1.plot(years, d_ref * 100, label=r'Referencia ($pb=1.5\%$, $g=3.5\%$)',
             color=col_ref, linewidth=2.2)
    ax1.axhline(100, color='#64748B', linestyle='--', linewidth=1.2, alpha=0.85, label='Frontera Crítica (100% PIB)')

    # Anotaciones terminales directas (sin recuadros flotantes)
    ax1.scatter([years[-1]], [d_opt[-1] * 100], color=col_opt, s=35, zorder=5)
    ax1.text(years[-1] + 0.15, d_opt[-1] * 100, f"{d_opt[-1]*100:.1f}%",
             fontweight='bold', color=col_opt, fontsize=9.5, va='center')
    ax1.scatter([years[-1]], [d_ref[-1] * 100], color=col_ref, s=35, zorder=5)
    ax1.text(years[-1] + 0.15, d_ref[-1] * 100, f"{d_ref[-1]*100:.1f}%",
             fontweight='bold', color=col_ref, fontsize=9.5, va='center')

    ax1.set_title('A. Trayectorias Viables (Zoom 40%–100% PIB)', fontweight='bold', fontsize=11, pad=10)
    ax1.set_xlabel('Año de Proyección', fontsize=10)
    ax1.set_ylabel('Deuda Pública Consolidada Neta (% PIB)', fontsize=10)
    ax1.set_xlim(years[0] - 0.2, years[-1] + 1.2)
    ax1.set_ylim(40, 108)
    ax1.legend(loc='upper left', frameon=False, fontsize=8.8)
    ax1.grid(True, linestyle='--', alpha=0.6, axis='y')

    # Panel 2: Dinámica Global Comparada (con Shock de Estrés Severo)
    ax2.plot(years, d_opt * 100, color=col_opt, linewidth=1.6, linestyle=':', label='Optimista (47.1% en 2035)')
    ax2.plot(years, d_ref * 100, color=col_ref, linewidth=1.8, linestyle='--', label='Referencia (82.8% en 2035)')
    ax2.plot(years, d_est * 100, color=col_est, linewidth=2.4, label='Estrés severo (992.1% en 2035)')
    ax2.axhline(100, color='#64748B', linestyle='--', linewidth=1.2, alpha=0.85, label='Frontera Crítica (100%)')

    # Rótulo directo de estrés sin flechas infantiles ni cajas monoespaciadas
    ax2.scatter([years[-1]], [d_est[-1] * 100], color=col_est, s=40, zorder=5)
    ax2.text(years[-1] - 0.2, d_est[-1] * 100 * 0.93,
             f"{d_est[-1]*100:.1f}% (2035)\nDivergencia explosiva",
             color=col_est, fontsize=9, fontweight='bold', ha='right', va='top')

    ax2.set_title('B. Dinámica Global con Estrés Cambiario y Contracción', fontweight='bold', fontsize=11, pad=10)
    ax2.set_xlabel('Año de Proyección', fontsize=10)
    ax2.set_ylabel('% del PIB', fontsize=10)
    ax2.legend(loc='upper left', frameon=False, fontsize=8.8)
    ax2.grid(True, linestyle='--', alpha=0.6, axis='y')

    fig.suptitle('Análisis de Sostenibilidad de la Deuda (DSA) Determinista (2026–2035)', fontweight='bold', fontsize=12, y=0.98)
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dsa_determinista.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # ------------------------------------------------------------------
    # 2. DSA ESTOCÁSTICO (GRÁFICO DE ABANICO + DENSIDAD TERMINAL)
    # ------------------------------------------------------------------
    print("\n[2/2] Ejecutando DSA Estocástico (Monte Carlo - 1000 simulaciones)...")

    # Parámetros base (usamos los de Referencia)
    base_params = SCENARIOS['Referencia']
    cov_matrix = build_cov_matrix()

    d_paths = simulate_stochastic_dsa(alpha, D_INITIAL, base_params, cov_matrix, years, DSA_STUDENT_T_NU, n_simulations=1000)

    # Calcular percentiles
    p10 = np.percentile(d_paths, 10, axis=0) * 100
    p25 = np.percentile(d_paths, 25, axis=0) * 100
    p50 = np.percentile(d_paths, 50, axis=0) * 100
    p75 = np.percentile(d_paths, 75, axis=0) * 100
    p90 = np.percentile(d_paths, 90, axis=0) * 100

    prob_crisis_final = np.mean(d_paths[:, -1] > 1.0) * 100

    # Gráfico de abanico acoplado a la derecha con densidad terminal en 2035 (Estándar FMI MAC-DSA)
    import scipy.stats as stats
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={'width_ratios': [3.5, 1]}, sharey=True)

    NAVY = "#1B365D"
    CRIMSON = "#8B1E1E"

    # Rellenar áreas de abanico con degradé académico
    ax1.fill_between(years, p10, p90, color=NAVY, alpha=0.14, label='Intervalo 10%–90%')
    ax1.fill_between(years, p25, p75, color=NAVY, alpha=0.28, label='Intervalo 25%–75%')

    # Mediana y frontera
    ax1.plot(years, p50, color=NAVY, linewidth=2.4, label=f'Mediana Base ({p50[-1]:.1f}% en 2035)')
    ax1.axhline(100, color=CRIMSON, linestyle='--', linewidth=1.6, label='Frontera Crítica (100% PIB)')

    # Marcador final de mediana
    ax1.scatter([years[-1]], [p50[-1]], color=NAVY, s=35, zorder=5)

    ax1.set_title('DSA Estocástico: Distribución Predictiva del Ratio Deuda/PIB (2026–2035)', fontweight='bold', fontsize=12, pad=10)
    ax1.set_xlabel('Año de Proyección', fontsize=10)
    ax1.set_ylabel('Deuda Pública Consolidada Neta (% PIB)', fontsize=10)
    ax1.legend(loc='upper left', frameon=False, fontsize=9.2)
    ax1.grid(True, linestyle='--', alpha=0.5, color='#E2E8F0', axis='y')
    ax1.set_xlim(years[0], years[-1])
    ax1.set_ylim(20, 180)

    # Panel de Densidad Terminal en 2035 (ax2)
    d_terminal = d_paths[:, -1] * 100
    kde = stats.gaussian_kde(d_terminal)
    y_grid = np.linspace(20, 180, 400)
    density = kde(y_grid)

    ax2.plot(density, y_grid, color=NAVY, linewidth=1.8)
    ax2.fill_betweenx(y_grid, 0, density, color=NAVY, alpha=0.15)

    # Sombrear la cola crítica (d > 100%)
    mask_tail = y_grid >= 100
    ax2.fill_betweenx(y_grid[mask_tail], 0, density[mask_tail], color=CRIMSON, alpha=0.40)
    ax2.axhline(100, color=CRIMSON, linestyle='--', linewidth=1.6)
    ax2.axhline(p50[-1], color=NAVY, linestyle=':', linewidth=1.2)

    # Notación de probabilidad limpia sin caja rosa estilo notificación
    badge_tail = rf"$\mathbb{{P}}(d_{{2035}} > 100\%) = {prob_crisis_final:.1f}\%$"
    ax2.text(0.5, 0.94, badge_tail, transform=ax2.transAxes, ha='center', va='top',
             fontsize=9.5, fontweight='bold', color=CRIMSON)

    ax2.set_title('Densidad Terminal\n(Año 2035)', fontweight='bold', fontsize=10, pad=8)
    ax2.set_xticks([])  # Eliminar ticks decimales confusos en el eje horizontal
    ax2.set_xlabel('Densidad', fontsize=9)
    ax2.spines['left'].set_visible(False)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#E2E8F0', axis='y')

    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dsa_grafico_abanico.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Reportar probabilidad de quiebre
    prob_crisis_final = np.mean(d_paths[:, -1] > 1.0) * 100
    print(f"\n -> Probabilidad de superar la frontera crítica (100% PIB) en {years[-1]}: {prob_crisis_final:.1f}%")

    df_percentiles = pd.DataFrame({'Año': years, 'p10': p10, 'p25': p25, 'p50': p50, 'p75': p75, 'p90': p90})
    df_percentiles.to_csv(os.path.join(tables_dir, 'fase6_dsa_percentiles_estocastico.csv'), index=False)
    with open(os.path.join(tables_dir, 'fase6_dsa_probabilidad.csv'), 'w') as f:
        f.write('year,prob_exceeds_100pct\n')
        f.write(f'{years[-1]},{prob_crisis_final:.4f}\n')

    print(f"\n[OK] Gráficos guardados en:\n - {os.path.join(output_dir, 'dsa_determinista.png')}\n - {os.path.join(output_dir, 'dsa_grafico_abanico.png')}")

if __name__ == '__main__':
    main()
