"""
bai_perron.py
=============
Implementación formal, desde cero, del procedimiento de quiebres estructurales
múltiples de Bai y Perron (1998, 2003) para un modelo de cambio puro en el
nivel de la media de la serie, aplicable a cualquier serie univariada.

No existe en el ecosistema de Python un equivalente directo de
`strucchange::breakpoints()` de R (que a su vez requiere R/rpy2, no
disponibles en este entorno). Este módulo reproduce el núcleo del algoritmo
de Bai-Perron -programación dinámica sobre la suma de cuadrados residuales
(SSR) de todas las particiones factibles- en Python puro/NumPy:

  1. Para una serie y_1,...,y_T, se computa vía sumas prefijas la SSR de
     ajustar una media constante a cualquier segmento contiguo [i,j] en
     tiempo O(1) por consulta.
  2. Programación dinámica exacta (Bai & Perron, 2003, sec. 3.1): para cada
     número de quiebres m=0,...,M, se halla la partición global que minimiza
     la SSR total, respetando el recorte (trimming) de tamaño mínimo de
     segmento h = ceil(trimming * T).
  3. Selección del número de quiebres mediante el criterio BIC (Yao, 1988),
     una de las dos reglas de selección explícitamente recomendadas por
     Bai y Perron (2003, sec. 4) cuando no se dispone de las tablas de
     valores críticos no estándar del contraste secuencial sup F(l+1|l)
     (esas tablas —Bai & Perron, 1998, Tabla II— están calibradas por
     simulación para un conjunto discreto de niveles de significancia y
     números de regresores, y no se ofrecen como función cerrada evaluable
     en software estadístico estándar; por eso se opta aquí por el criterio
     de información, que sí es reproducible exactamente en Python).

Referencia: Bai, J. y Perron, P. (2003). "Computation and Analysis of
Multiple Structural Change Models". Journal of Applied Econometrics, 18(1).
"""

import numpy as np
import pandas as pd


def _ssr_table(y: np.ndarray):
    """Prefijos de y y de y^2 para computar SSR(i,j) de un ajuste de media
    constante en el segmento [i,j] (0-indexado, ambos extremos inclusive)
    en tiempo O(1)."""
    T = len(y)
    cs_y = np.concatenate([[0.0], np.cumsum(y)])
    cs_y2 = np.concatenate([[0.0], np.cumsum(y ** 2)])

    def ssr(i, j):
        n = j - i + 1
        s = cs_y[j + 1] - cs_y[i]
        s2 = cs_y2[j + 1] - cs_y2[i]
        return s2 - (s ** 2) / n

    return ssr


def _optimal_partition(y: np.ndarray, m: int, h: int):
    """Partición óptima exacta de y en m+1 segmentos (m quiebres), con
    tamaño mínimo de segmento h, minimizando la SSR total.

    Devuelve (ssr_total, lista_de_indices_de_quiebre) donde cada índice de
    quiebre bkp_k es el último índice (0-indexado) del segmento k-ésimo.
    """
    T = len(y)
    ssr = _ssr_table(y)

    if m == 0:
        return ssr(0, T - 1), []

    # dp[k][t] = SSR mínima usando k quiebres en el prefijo y[0..t]
    # (es decir, k+1 segmentos cubriendo [0, t]).
    # prev[k][t] = índice del quiebre anterior que logra ese mínimo.
    NEG = np.inf
    dp = np.full((m + 1, T), NEG)
    prev = np.full((m + 1, T), -1, dtype=int)

    for t in range(h - 1, T):
        dp[0, t] = ssr(0, t)

    for k in range(1, m + 1):
        min_t = (k + 1) * h - 1
        for t in range(min_t, T):
            best_val = NEG
            best_prev = -1
            # el quiebre anterior s marca el final del segmento k-1 y el
            # nuevo segmento es (s+1, t); requiere tamaño >= h
            for s in range(k * h - 1, t - h + 1):
                if dp[k - 1, s] == NEG:
                    continue
                val = dp[k - 1, s] + ssr(s + 1, t)
                if val < best_val:
                    best_val = val
                    best_prev = s
            dp[k, t] = best_val
            prev[k, t] = best_prev

    ssr_total = dp[m, T - 1]
    bkps = []
    k, t = m, T - 1
    while k > 0:
        s = prev[k, t]
        bkps.append(s)
        t = s
        k -= 1
    bkps.reverse()
    return ssr_total, bkps


def bai_perron_breaks(series: pd.Series, max_breaks: int = 5, trimming: float = 0.15):
    """Estima quiebres estructurales múltiples en la media de `series`
    (Bai-Perron, cambio puro en la media) para m=0..max_breaks quiebres,
    selecciona m* por BIC (Yao, 1988) y devuelve un diccionario con:

      - 'bic_por_m'      : DataFrame con SSR y BIC para cada m.
      - 'm_optimo'       : número de quiebres seleccionado.
      - 'fechas_quiebre' : fechas (índice de `series`) de los quiebres óptimos.
      - 'medias_segmento': media estimada de cada segmento bajo m*.
    """
    y = series.dropna()
    idx = y.index
    y = y.values
    T = len(y)
    h = max(2, int(np.ceil(trimming * T)))

    rows = []
    particiones = {}
    for m in range(0, max_breaks + 1):
        if (m + 1) * h > T:
            break
        ssr_total, bkps = _optimal_partition(y, m, h)
        n_params = (m + 1) + m  # m+1 medias + m fechas de quiebre estimadas
        bic = T * np.log(ssr_total / T) + n_params * np.log(T)
        rows.append({"m": m, "ssr": ssr_total, "n_parametros": n_params, "bic": bic})
        particiones[m] = bkps

    bic_df = pd.DataFrame(rows)
    m_optimo = int(bic_df.loc[bic_df["bic"].idxmin(), "m"])
    bkps_optimo = particiones[m_optimo]

    fechas_quiebre = [idx[b] for b in bkps_optimo]

    bounds = [-1] + bkps_optimo + [T - 1]
    medias_segmento = []
    for i in range(len(bounds) - 1):
        seg = y[bounds[i] + 1: bounds[i + 1] + 1]
        medias_segmento.append({
            "segmento": i + 1,
            "inicio": idx[bounds[i] + 1],
            "fin": idx[bounds[i + 1]],
            "n_obs": len(seg),
            "media": seg.mean(),
            "std": seg.std(ddof=1) if len(seg) > 1 else np.nan,
        })

    return {
        "bic_por_m": bic_df,
        "m_optimo": m_optimo,
        "fechas_quiebre": fechas_quiebre,
        "medias_segmento": pd.DataFrame(medias_segmento),
        "trimming_h": h,
    }
