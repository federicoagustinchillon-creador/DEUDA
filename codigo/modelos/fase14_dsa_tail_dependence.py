"""
H6 (optima) -- Robustez del DSA estocastico bajo shocks t marginales
INDEPENDIENTES (sin estructura de copula-t, por tanto sin tail dependence),
preservando exactamente la misma varianza marginal de cada shock que la
version correlacionada de fase6_sostenibilidad_deuda.py. Compara contra
30.4% (referencia, t-copula correlacionada).

Reporta ademas una variante intermedia (copula Gaussiana + marginales t)
que preserva la correlacion lineal pero remueve el exceso de tail
dependence propio de la t-copula, para distinguir el efecto de la
correlacion del efecto de la tail dependence.
"""
import numpy as np
from scipy.stats import t as t_dist, norm
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fase6_sostenibilidad_deuda import (
    SCENARIOS, STD_DEVS, CORR, ALPHA, D_INITIAL, DSA_STUDENT_T_NU,
    build_cov_matrix, simulate_stochastic_dsa
)

years = np.arange(2026, 2036)
n_years = len(years)
nu = DSA_STUDENT_T_NU
cov_matrix = build_cov_matrix()
base_params = SCENARIOS['Referencia']
alpha = ALPHA

# --- 0. Referencia: t-copula correlacionada (replica exacta de fase6) ---
d_paths_ref = simulate_stochastic_dsa(alpha, D_INITIAL, base_params, cov_matrix, years, nu, n_simulations=1000)
p_ref = np.mean(d_paths_ref[:, -1] > 1.0)
print(f"[0] Referencia (t-copula correlacionada, tal como reportado): {p_ref*100:.1f}%")

def simulate_path_from_shocks(shocks_5xN, alpha, d_initial, base_params, years):
    n_years = len(years)
    d = np.zeros(n_years)
    d[0] = d_initial
    pb_s = np.full(n_years, base_params['pb']) + shocks_5xN[:, 0]
    g_s = np.full(n_years, base_params['g']) + shocks_5xN[:, 1]
    rd_s = np.full(n_years, base_params['r_d']) + shocks_5xN[:, 2]
    rf_s = np.full(n_years, base_params['r_f']) + shocks_5xN[:, 3]
    delta_e_s = np.full(n_years, base_params['delta_e']) + shocks_5xN[:, 4]
    for i in range(1, n_years):
        term_d = alpha * (1 + rd_s[i]) / (1 + g_s[i])
        term_f = (1 - alpha) * (1 + rf_s[i]) * (1 + delta_e_s[i]) / (1 + g_s[i])
        M = term_d + term_f
        d[i] = M * d[i-1] - pb_s[i] + 0.0
    return d

# --- 1. Marginales t INDEPENDIENTES (sin correlacion, sin tail dependence) ---
np.random.seed(42)
n_sim = 1000
scale_indep = np.sqrt(np.diag(cov_matrix) * (nu - 2) / nu)  # preserva var. marginal exacta
d_paths_indep = np.zeros((n_sim, n_years))
d_paths_indep[:, 0] = D_INITIAL
for s in range(n_sim):
    shocks = np.zeros((n_years, 5))
    for j in range(5):
        shocks[:, j] = t_dist.rvs(df=nu, size=n_years) * scale_indep[j]
    d_paths_indep[s, :] = simulate_path_from_shocks(shocks, alpha, D_INITIAL, base_params, years)
p_indep = np.mean(d_paths_indep[:, -1] > 1.0)
print(f"[1] Marginales t independientes (sin correlacion, sin tail dependence): {p_indep*100:.1f}%")

# --- 2. Copula Gaussiana + marginales t (preserva correlacion, sin exceso de tail dependence) ---
np.random.seed(42)
L = np.linalg.cholesky(CORR)
d_paths_gausscop = np.zeros((n_sim, n_years))
d_paths_gausscop[:, 0] = D_INITIAL
for s in range(n_sim):
    Z = np.random.normal(size=(n_years, 5)) @ L.T   # correlacion gaussiana
    U = norm.cdf(Z)                                   # a uniformes via copula gaussiana
    U = np.clip(U, 1e-6, 1 - 1e-6)
    T = t_dist.ppf(U, df=nu)                           # a marginales t(nu) correlacionadas via copula gaussiana
    shocks = T * scale_indep[np.newaxis, :]
    d_paths_gausscop[s, :] = simulate_path_from_shocks(shocks, alpha, D_INITIAL, base_params, years)
p_gausscop = np.mean(d_paths_gausscop[:, -1] > 1.0)
print(f"[2] Copula Gaussiana + marginales t (correlacion sin exceso de tail dependence): {p_gausscop*100:.1f}%")

print()
print(f"Mediana 2035 -- ref: {np.median(d_paths_ref[:,-1])*100:.1f}%  indep: {np.median(d_paths_indep[:,-1])*100:.1f}%  gausscop: {np.median(d_paths_gausscop[:,-1])*100:.1f}%")

# Persistencia a CSV para trazabilidad (mismo criterio que el resto de las
# fases: todo resultado intermedio citado en la tesis debe quedar en
# resultados/tablas/, no solo impreso por consola).
import pandas as pd
tabla = pd.DataFrame([
    {"especificacion": "Copula-t correlacionada (reportada, Tabla 7.3)",
     "prob_insolvencia_2035": p_ref * 100, "mediana_2035": np.median(d_paths_ref[:, -1]) * 100},
    {"especificacion": "Copula Gaussiana + marginales t (correlacion sin exceso de tail dependence)",
     "prob_insolvencia_2035": p_gausscop * 100, "mediana_2035": np.median(d_paths_gausscop[:, -1]) * 100},
    {"especificacion": "Marginales t independientes (sin correlacion, sin tail dependence)",
     "prob_insolvencia_2035": p_indep * 100, "mediana_2035": np.median(d_paths_indep[:, -1]) * 100},
])
tabla.to_csv("resultados/tablas/fase14_dsa_tail_dependence.csv", index=False)
print("\nGuardado: resultados/tablas/fase14_dsa_tail_dependence.csv")
