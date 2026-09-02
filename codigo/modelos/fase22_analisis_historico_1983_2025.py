"""
FASE 22: ANALISIS ECONOMETRICO DEL SPREAD SOBERANO HISTORICO (1983-2025)
42 Años de Democracia Continua (n = 169 observaciones trimestrales).

Estimaciones:
1. Quiebres estructurales múltiples de Bai y Perron (2003) sobre el spread empalmado.
2. Calibración por Máxima Verosimilitud exacta del Proceso Cox-Ingersoll-Ross (CIR 1985).
3. Análisis comparativo por régimen presidencial y contraste con el umbral de fatiga fiscal.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import iv
import ruptures as rpt

# Rutas
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATOS_DIR = BASE_DIR / "datos"
PROCESADOS_DIR = DATOS_DIR / "procesados"
RESULTADOS_TABLAS = BASE_DIR / "resultados" / "tablas"

RESULTADOS_TABLAS.mkdir(parents=True, exist_ok=True)


def cargar_datos_historicos() -> pd.DataFrame:
    ruta = PROCESADOS_DIR / "spread_soberano_historico_1983_2025.csv"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecutar primero fase22_construccion_spread_1983_2025.py")
    df = pd.read_csv(ruta)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def estimar_quiebres_bai_perron(df: pd.DataFrame, n_quiebres: int = 5) -> pd.DataFrame:
    """
    Detección de quiebres estructurales múltiples mediante programación dinámica (Bai-Perron / Dynp).
    """
    y = df["Spread_Empalmado_pb"].values
    n = len(y)
    
    # Modelo L2 (cambios en media del spread)
    algo = rpt.Dynp(model="l2", min_size=8, jump=1).fit(y)
    puntos_quiebre = algo.predict(n_bkps=n_quiebres)
    
    # El último punto en ruptures es siempre n (fin de la muestra), lo excluimos
    indices_quiebres = [idx for idx in puntos_quiebre if idx < n]
    
    registros = []
    prev_idx = 0
    for i, idx in enumerate(indices_quiebres + [n]):
        fecha_inicio = df.loc[prev_idx, "Date"].strftime("%Y-%m-%d")
        fecha_fin = df.loc[idx - 1, "Date"].strftime("%Y-%m-%d")
        sub_y = y[prev_idx:idx]
        media_seg = np.mean(sub_y)
        std_seg = np.std(sub_y, ddof=1)
        
        fecha_quiebre_str = df.loc[idx - 1, "Date"].strftime("%Y-%m-%d") if idx < n else "Fin de Muestra"
        hito = df.loc[idx - 1, "Evento_Hito"] if idx < n else "Cierre 2025"
        
        registros.append({
            "Segmento": f"Régimen {i + 1}",
            "Fecha_Inicio": fecha_inicio,
            "Fecha_Fin": fecha_fin,
            "N_Obs": len(sub_y),
            "Media_Spread_pb": round(media_seg, 2),
            "Desvio_Spread_pb": round(std_seg, 2),
            "Fecha_Quiebre": fecha_quiebre_str,
            "Hito_Asociado": hito
        })
        prev_idx = idx
        
    df_quiebres = pd.DataFrame(registros)
    salida_csv = RESULTADOS_TABLAS / "fase22_bai_perron_1983_2025.csv"
    df_quiebres.to_csv(salida_csv, index=False)
    print(f"\n[FASE 22] Quiebres Bai-Perron exportados a: {salida_csv}")
    print(df_quiebres[["Segmento", "Fecha_Inicio", "Fecha_Fin", "Media_Spread_pb", "Hito_Asociado"]])
    return df_quiebres


def cir_log_likelihood(params: np.ndarray, r: np.ndarray, dt: float) -> float:
    """
    Log-verosimilitud negativa exacta del proceso CIR con densidad Chi-cuadrado no central.
    """
    kappa, theta, sigma = params
    if kappa <= 1e-4 or theta <= 1.0 or sigma <= 1e-4:
        return 1e12
        
    # Condición de no negatividad de Feller relajada para penalización suave
    feller_penalty = 0.0
    if 2 * kappa * theta <= sigma**2:
        feller_penalty = 1e4 * (sigma**2 - 2 * kappa * theta)
        
    n = len(r)
    r_t = r[:-1]
    r_tp1 = r[1:]
    
    exp_k = np.exp(-kappa * dt)
    c = 2.0 * kappa / (sigma**2 * (1.0 - exp_k))
    q = 2.0 * kappa * theta / (sigma**2) - 1.0
    
    u = c * r_t * exp_k
    v = c * r_tp1
    
    z = 2.0 * np.sqrt(u * v)
    # Aproximación robusta para iv(q, z)
    # log(iv(q, z)) para z grande
    with np.errstate(over="ignore", invalid="ignore"):
        bessel_val = iv(q, z)
        # Reemplazar ceros o infinitos numéricos
        bessel_val = np.where(bessel_val <= 1e-300, 1e-300, bessel_val)
        log_bessel = np.log(bessel_val)
        
    log_lik = (
        (n - 1) * np.log(c)
        - np.sum(u + v)
        + 0.5 * q * np.sum(np.log(v / u))
        + np.sum(log_bessel)
    )
    
    if np.isnan(log_lik) or np.isinf(log_lik):
        return 1e12
        
    return -log_lik + feller_penalty


def calibrar_cir_historico(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calibra el modelo CIR sobre la muestra completa de 42 años (1983-2025).
    """
    r = df["Spread_Empalmado_pb"].values
    dt = 0.25  # frecuencia trimestral
    
    # Valores iniciales por OLS de AR(1)
    # r_{t+1} - r_t = a + b * r_t
    diff_r = np.diff(r)
    X = np.column_stack([np.ones(len(r) - 1), r[:-1]])
    beta = np.linalg.lstsq(X, diff_r, rcond=None)[0]
    
    kappa_init = max(-beta[1] / dt, 0.05)
    theta_init = max(beta[0] / (kappa_init * dt), 500.0)
    resids = diff_r - X @ beta
    sigma_init = max(np.std(resids) / (np.sqrt(np.mean(r[:-1]) * dt)), 5.0)
    
    init_params = np.array([kappa_init, theta_init, sigma_init])
    bounds = [(0.01, 3.0), (100.0, 4000.0), (1.0, 50.0)]
    
    res = minimize(
        cir_log_likelihood,
        init_params,
        args=(r, dt),
        method="L-BFGS-B",
        bounds=bounds
    )
    
    kappa_hat, theta_hat, sigma_hat = res.x
    feller_stat = 2 * kappa_hat * theta_hat
    feller_crit = sigma_hat**2
    feller_ratio = feller_stat / feller_crit
    cumple_feller = bool(feller_ratio > 1.0)
    half_life = np.log(2.0) / kappa_hat
    
    log_lik_cir = -res.fun
    k_params_cir = 3
    n_obs = len(r)
    aic_cir = 2 * k_params_cir - 2 * log_lik_cir
    
    # AR(1) benchmark
    res_ar1 = np.sum(resids**2)
    log_lik_ar1 = -0.5 * (n_obs - 1) * (np.log(2 * np.pi * res_ar1 / (n_obs - 1)) + 1)
    aic_ar1 = 2 * 2 - 2 * log_lik_ar1
    
    resultados = [{
        "Muestra": "Ultra-Larga (42 Años, 1983-2025)",
        "N_Obs": n_obs,
        "kappa": round(kappa_hat, 4),
        "theta_pb": round(theta_hat, 2),
        "sigma": round(sigma_hat, 4),
        "feller_stat": round(feller_stat, 2),
        "feller_crit": round(feller_crit, 2),
        "feller_ratio": round(feller_ratio, 4),
        "cumple_feller": cumple_feller,
        "half_life_anios": round(half_life, 2),
        "log_lik_cir": round(log_lik_cir, 2),
        "aic_cir": round(aic_cir, 2),
        "aic_ar1": round(aic_ar1, 2),
        "cir_preferido_aic": bool(aic_cir < aic_ar1)
    }]
    
    df_cir = pd.DataFrame(resultados)
    salida_csv = RESULTADOS_TABLAS / "fase22_cir_calibracion_1983_2025.csv"
    df_cir.to_csv(salida_csv, index=False)
    print(f"\n[FASE 22] Calibración CIR 1983-2025 exportada a: {salida_csv}")
    print(df_cir[["Muestra", "kappa", "theta_pb", "sigma", "feller_ratio", "half_life_anios", "cir_preferido_aic"]])
    return df_cir


def estadisticas_por_regimen(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa estadísticas descriptivas por administración presidencial.
    """
    grupos = df.groupby("Regimen_Politico", sort=False)
    res = []
    for reg, grp in grupos:
        s = grp["Spread_Empalmado_pb"]
        res.append({
            "Regimen_Presidencial": reg,
            "Inicio": grp["Date"].min().strftime("%Y-%m"),
            "Fin": grp["Date"].max().strftime("%Y-%m"),
            "Trimestres": len(grp),
            "Media_pb": round(s.mean(), 2),
            "Mediana_pb": round(s.median(), 2),
            "Min_pb": round(s.min(), 2),
            "Max_pb": round(s.max(), 2),
            "Desvio_pb": round(s.std(), 2)
        })
    df_reg = pd.DataFrame(res)
    salida_csv = RESULTADOS_TABLAS / "fase22_spread_por_regimen.csv"
    df_reg.to_csv(salida_csv, index=False)
    print(f"\n[FASE 22] Estadísticas por régimen exportadas a: {salida_csv}")
    print(df_reg[["Regimen_Presidencial", "Trimestres", "Media_pb", "Min_pb", "Max_pb"]])
    return df_reg


def main():
    df = cargar_datos_historicos()
    print(f"[FASE 22] Iniciando análisis econométrico sobre {len(df)} observaciones (1983-2025)...")
    
    # 1. Bai-Perron
    estimar_quiebres_bai_perron(df, n_quiebres=5)
    
    # 2. CIR
    calibrar_cir_historico(df)
    
    # 3. Descriptivos por régimen
    estadisticas_por_regimen(df)
    
    print("\n[FASE 22] Estimación econométrica histórica completada con éxito.")


if __name__ == "__main__":
    main()
