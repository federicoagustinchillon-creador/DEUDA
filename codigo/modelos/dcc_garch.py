"""
dcc_garch.py
============
Implementación propia, en Python puro (NumPy/SciPy), del modelo de
Correlación Condicional Dinámica de Engle (2002) -DCC-GARCH-, estimado por
Cuasi-Máxima Verosimilitud (QML) en dos etapas:

  Etapa 1 (univariada): se ajusta un GARCH(1,1) a cada serie individual
  (paquete `arch`, ya utilizado en el proyecto) y se extraen los residuos
  estandarizados z_t = u_t / sigma_t.

  Etapa 2 (correlación dinámica): sobre la matriz de residuos estandarizados
  Z (T x N), se estima por QML el proceso de correlación dinámica:
      Q_t = (1 - a - b) * Qbar + a * z_{t-1} z_{t-1}' + b * Q_{t-1}
      R_t = diag(Q_t)^{-1/2} Q_t diag(Q_t)^{-1/2}
  con Qbar la matriz de correlación incondicional de Z, y (a, b) los
  parámetros de persistencia/reactividad de la correlación, sujetos a
  a >= 0, b >= 0, a + b < 1.

No existe en el ecosistema de Python un equivalente directo y mantenido de
`rmgarch::dccfit()` de R (que a su vez requiere R/rpy2, no disponibles en
este entorno). Esta es una implementación directa de Engle (2002), no una
aproximación: la log-verosimilitud concentrada de la etapa de correlación
es exactamente la de la especificación DCC(1,1) estándar.

Referencia: Engle, R. (2002). "Dynamic Conditional Correlation: A Simple
Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity
Models". Journal of Business & Economic Statistics, 20(3), 339-350.
"""

import numpy as np
from scipy.optimize import minimize
from arch import arch_model


def fit_univariate_garch(series: np.ndarray):
    """Ajusta un GARCH(1,1) univariado (media cero, t de Student) a una
    serie en puntos porcentuales (ya escalada por 100 para estabilidad
    numérica, convención estándar del paquete `arch`)."""
    am = arch_model(series, mean="Zero", vol="GARCH", p=1, q=1, dist="t")
    res = am.fit(disp="off")
    z = res.resid / res.conditional_volatility
    return res, z


def _dcc_neg_loglik(params, Z):
    a, b = params
    T, N = Z.shape
    Qbar = np.corrcoef(Z.T)
    Q_t = Qbar.copy()
    nll = 0.0
    for t in range(T):
        d = np.sqrt(np.diag(Q_t))
        R_t = Q_t / np.outer(d, d)
        try:
            R_inv = np.linalg.inv(R_t)
            sign, logdet = np.linalg.slogdet(R_t)
        except np.linalg.LinAlgError:
            return 1e10
        if sign <= 0:
            return 1e10
        z_t = Z[t, :]
        nll += 0.5 * (logdet + z_t @ R_inv @ z_t.T - z_t @ z_t.T)
        Q_t = (1 - a - b) * Qbar + a * np.outer(z_t, z_t) + b * Q_t
    return nll


def fit_dcc(Z: np.ndarray, a0: float = 0.03, b0: float = 0.90):
    """Estima (a, b) del DCC(1,1) por QML sobre la matriz de residuos
    estandarizados Z (T x N)."""
    cons = ({"type": "ineq", "fun": lambda p: 0.999 - p[0] - p[1]},
             {"type": "ineq", "fun": lambda p: p[0]},
             {"type": "ineq", "fun": lambda p: p[1]})
    res = minimize(_dcc_neg_loglik, x0=[a0, b0], args=(Z,), method="SLSQP",
                    bounds=[(1e-6, 0.5), (1e-6, 0.998)], constraints=cons,
                    options={"maxiter": 300, "ftol": 1e-10})
    a, b = res.x
    return a, b, res


def dcc_correlation_path(Z: np.ndarray, a: float, b: float):
    """Reconstruye la trayectoria completa R_1,...,R_T dado (a, b)."""
    T, N = Z.shape
    Qbar = np.corrcoef(Z.T)
    Q_t = Qbar.copy()
    R_path = np.zeros((T, N, N))
    for t in range(T):
        d = np.sqrt(np.diag(Q_t))
        R_t = Q_t / np.outer(d, d)
        R_path[t] = R_t
        z_t = Z[t, :]
        Q_t = (1 - a - b) * Qbar + a * np.outer(z_t, z_t) + b * Q_t
    return R_path
