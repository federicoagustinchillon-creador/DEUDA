"""
fase21_tvecm_hansen_seo.py
===========================
Implementa el Modelo de Vectores con Corrección de Error y Umbral
(Threshold VECM / TVECM) de Hansen y Seo (2002) para evaluar si las velocidades
de ajuste fiscal (alpha) conmutan de régimen según el nivel de estrés del riesgo soberano.

Modelo:
-------
Delta Y_t = (mu_1 + alpha_1 * ect_{t-1} + Gamma_1 * Delta Y_{t-1}) * I(EMBI_{t-1} <= tau) +
            (mu_2 + alpha_2 * ect_{t-1} + Gamma_2 * Delta Y_{t-1}) * I(EMBI_{t-1} > tau) + eps_t

Donde ect_{t-1} = beta' Y_{t-1} es el término de corrección de error.
El algoritmo realiza una búsqueda en grilla sobre el espacio de umbrales tau (soporte 15%-85%).

Exportación:
------------
- Tablas a resultados/tablas/fase21_tvecm_resultados.csv
"""

import os
import pathlib
import warnings
import numpy as np
import pandas as pd
from scipy import linalg
from statsmodels.tsa.vector_ar.vecm import VECM, select_order

warnings.filterwarnings("ignore")

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS_DIR = BASE_DIR / "datos"
TABLAS_DIR = BASE_DIR / "resultados" / "tablas"

os.makedirs(TABLAS_DIR, exist_ok=True)


def cargar_datos():
    ruta = DATOS_DIR / "dataset_consolidado_real.csv"
    df = pd.read_csv(ruta)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    
    # 4 variables del sistema de cointegración
    vars_coint = ["deuda_pib", "pb_pib", "EMBI", "TCRM"]
    data = df[vars_coint].dropna()
    return data, vars_coint


def estimar_tvecm(data, trimming=0.15, n_boot=200):
    Y = data.values
    T, K = Y.shape
    
    # 1. Estimación preliminar de beta por VECM lineal de Johansen
    vecm_lin = VECM(data, k_ar_diff=1, coint_rank=1, deterministic="ci").fit()
    beta = vecm_lin.beta.flatten() # (K+1,) o (K,)
    
    # Término de corrección de error
    # ect_t = Y_t @ beta[:K]
    ect = Y @ beta[:K]
    
    # Matrices en diferencias
    dY = np.diff(Y, axis=0) # (T-1, K)
    dY_lag = dY[:-1]        # (T-2, K)
    dY_curr = dY[1:]        # (T-2, K)
    ect_lag = ect[1:-1]     # (T-2,)
    embi_threshold_var = data["EMBI"].values[1:-1] # (T-2,)
    
    n_effective = len(dY_curr)
    
    # Rejilla de búsqueda de umbrales sobre el soporte intermedio
    embi_sorted = np.sort(embi_threshold_var)
    q_low = int(trimming * n_effective)
    q_high = int((1 - trimming) * n_effective)
    grid_tau = embi_sorted[q_low:q_high:2] # Evaluación cada 2 puntos para eficiencia
    
    # Regresión lineal irrestricta (H0: un solo régimen)
    X_lin = np.column_stack([np.ones(n_effective), ect_lag, dY_lag])
    B_lin, res_lin, _, _ = linalg.lstsq(X_lin, dY_curr)
    u_lin = dY_curr - X_lin @ B_lin
    sigma_lin = (u_lin.T @ u_lin) / n_effective
    det_lin = linalg.det(sigma_lin)
    
    best_loglik = 1e12
    best_tau = None
    best_B1 = None
    best_B2 = None
    best_sigma = None
    
    # Búsqueda en grilla del umbral tau
    for tau in grid_tau:
        mask1 = (embi_threshold_var <= tau)
        mask2 = (embi_threshold_var > tau)
        
        n1 = np.sum(mask1)
        n2 = np.sum(mask2)
        if n1 < q_low or n2 < q_low:
            continue
            
        X1 = X_lin[mask1]
        Y1 = dY_curr[mask1]
        X2 = X_lin[mask2]
        Y2 = dY_curr[mask2]
        
        B1, _, _, _ = linalg.lstsq(X1, Y1)
        B2, _, _, _ = linalg.lstsq(X2, Y2)
        
        u1 = Y1 - X1 @ B1
        u2 = Y2 - X2 @ B2
        
        u_total = np.zeros_like(dY_curr)
        u_total[mask1] = u1
        u_total[mask2] = u2
        
        sigma_t = (u_total.T @ u_total) / n_effective
        det_t = linalg.det(sigma_t)
        
        if det_t > 0 and det_t < best_loglik:
            best_loglik = det_t
            best_tau = tau
            best_B1 = B1
            best_B2 = B2
            best_sigma = sigma_t
            
    # Estadístico Sup-LM
    # LM = T * (det_lin - best_loglik) / det_lin
    sup_lm = float(n_effective * (det_lin - best_loglik) / det_lin)
    
    # Bootstrap no paramétrico para p-value
    lm_boot = np.zeros(n_boot)
    for b in range(n_boot):
        idx_b = np.random.choice(n_effective, size=n_effective, replace=True)
        u_b = u_lin[idx_b]
        dY_b = X_lin @ B_lin + u_b
        
        # Búsqueda de tau sobre datos simulados bajo H0
        best_ll_b = 1e12
        for tau in grid_tau[::3]:
            m1 = (embi_threshold_var <= tau)
            m2 = (embi_threshold_var > tau)
            if np.sum(m1) < q_low or np.sum(m2) < q_low:
                continue
            B1_b, _, _, _ = linalg.lstsq(X_lin[m1], dY_b[m1])
            B2_b, _, _, _ = linalg.lstsq(X_lin[m2], dY_b[m2])
            u_b_tot = np.zeros_like(dY_b)
            u_b_tot[m1] = dY_b[m1] - X_lin[m1] @ B1_b
            u_b_tot[m2] = dY_b[m2] - X_lin[m2] @ B2_b
            dt_b = linalg.det((u_b_tot.T @ u_b_tot) / n_effective)
            if dt_b > 0 and dt_b < best_ll_b:
                best_ll_b = dt_b
        lm_boot[b] = n_effective * (det_lin - best_ll_b) / det_lin
        
    p_val_sup_lm = float(np.mean(lm_boot >= sup_lm))
    
    return {
        "best_tau_pb": round(float(best_tau), 2),
        "sup_lm_stat": round(sup_lm, 3),
        "p_val_sup_lm": round(p_val_sup_lm, 4),
        "alpha_pb_regimen1": round(float(best_B1[1, 1]), 4), # Coeficiente ECT sobre Delta pb en Reg 1
        "alpha_pb_regimen2": round(float(best_B2[1, 1]), 4), # Coeficiente ECT sobre Delta pb en Reg 2
        "n_obs_regimen1": int(np.sum(embi_threshold_var <= best_tau)),
        "n_obs_regimen2": int(np.sum(embi_threshold_var > best_tau)),
        "n_total": n_effective
    }


def main():
    data, vars_coint = cargar_datos()
    res = estimar_tvecm(data, trimming=0.15, n_boot=200)
    
    df_res = pd.DataFrame([res])
    df_res.to_csv(TABLAS_DIR / "fase21_tvecm_resultados.csv", index=False)
    
    print("[FASE 21] Estimacion de Threshold VECM (Hansen & Seo, 2002) completada con exito.")
    print(f"[FASE 21] Umbral Optimo Estimado: {res['best_tau_pb']} pb")
    print(f"[FASE 21] Sup-LM Stat: {res['sup_lm_stat']} (p-val: {res['p_val_sup_lm']})")
    print(f"[FASE 21] alpha_pb Regimen 1: {res['alpha_pb_regimen1']} vs Regimen 2: {res['alpha_pb_regimen2']}")
    print(f"[FASE 21] Tablas exportadas a {TABLAS_DIR}")


if __name__ == "__main__":
    main()
