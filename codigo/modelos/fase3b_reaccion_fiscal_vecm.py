"""
fase3b_reaccion_fiscal_vecm.py
===============================
Fase 3 (alternativa) del Protocolo Econométrico: Estimación de la Función de
Reacción Fiscal (FRF) mediante un Modelo de Vectores con Corrección de Error
(VECM), como alternativa metodológica a DOLS (fase3_reaccion_fiscal.py).

Motivación del cambio (sugerencia del director de tesis): DOLS estima la
relación de largo plazo mediante una única ecuación (pb_t como variable
dependiente), tratando la endogeneidad de corto plazo mediante adelantos y
rezagos ad-hoc de Delta d_t (Stock, 1993). Un VECM, en cambio, modela el
sistema completo -deuda_pib, pb_pib, EMBI, TCRM- como conjuntamente endógeno:
la endogeneidad queda integrada directamente en la estructura del sistema, sin
necesidad de elegir una variable dependiente "principal" ni de purgar sesgos
con una construcción auxiliar.

Este script NO reemplaza fase3_reaccion_fiscal.py (DOLS): ambos se conservan.
DOLS queda como ejercicio de robustez / comparación metodológica; el VECM pasa
a ser la estimación de referencia de la FRF de largo plazo.

Requiere que exista cointegración (Fase 2, Johansen). Si el sistema no está
cointegrado, la alternativa correcta es un VAR restringido en primeras
diferencias (ver estimar_var_restringido_diferencias más abajo), no un VECM.
"""

import pandas as pd
import numpy as np
import os
import warnings
from statsmodels.tsa.vector_ar.vecm import VECM, select_order, coint_johansen
from statsmodels.tsa.api import VAR

warnings.filterwarnings("ignore")


def seleccionar_rango_cointegracion(df, det_order=0, k_ar_diff=1, alpha=0.05):
    """
    Determina el rango de cointegración r mediante el test de Johansen,
    aplicando la regla secuencial estándar sobre el estadístico de Traza
    (más robusto que Máximo Autovalor en muestras pequeñas/medianas,
    Johansen y Juselius, 1990).
    """
    res = coint_johansen(df, det_order=det_order, k_ar_diff=k_ar_diff)
    traces = res.lr1
    crit = res.cvt[:, 1]  # columna 95%

    r = 0
    for i in range(len(traces)):
        if traces[i] > crit[i]:
            r = i + 1
        else:
            break
    return r, res


def estimar_vecm(df, coint_vars, exog_vars, k_ar_diff, coint_rank):
    """
    Estima el VECM con rango de cointegración impuesto (coint_rank) y
    variables exógenas estacionarias (g_gap) fuera del vector de
    cointegración, siguiendo la práctica estándar cuando una variable de
    control es I(0) por construcción.
    """
    endog = df[coint_vars]
    exog = df[exog_vars] if exog_vars else None

    modelo = VECM(
        endog,
        exog=exog,
        k_ar_diff=k_ar_diff,
        coint_rank=coint_rank,
        deterministic="ci",  # constante restringida al espacio de cointegración
    )
    resultado = modelo.fit()
    return resultado


def estimar_var_restringido_diferencias(df, coint_vars, exog_vars, k_ar_diff):
    """
    Alternativa cuando NO hay cointegración: VAR restringido a primeras
    diferencias (impone la raíz unitaria como restricción explícita, en
    lugar de estimar niveles espuriamente). Es el análogo, sin relación de
    largo plazo, al VECM.
    """
    df_diff = df[coint_vars].diff().dropna()
    exog = df[exog_vars].loc[df_diff.index] if exog_vars else None
    modelo = VAR(df_diff, exog=exog)
    resultado = modelo.fit(k_ar_diff)
    return resultado


def main():
    print("=" * 78)
    print(" FASE 3b: FUNCIÓN DE REACCIÓN FISCAL VÍA VECM (alternativa a DOLS) ")
    print("=" * 78)

    import pathlib
    base_dir = pathlib.Path(__file__).parent.parent.parent
    csv_path = base_dir / "datos" / "dataset_consolidado_real.csv"

    if not os.path.exists(csv_path):
        print(f"[!] ERROR: No se encontró el dataset en {csv_path}")
        return

    df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")

    coint_vars = ["deuda_pib", "pb_pib", "EMBI", "TCRM"]
    exog_vars = ["g_gap"]
    cols = coint_vars + exog_vars
    df = df[cols].dropna()
    print(f"\nSistema: {coint_vars} (exógena estacionaria: {exog_vars})")
    print(f"Observaciones disponibles: {len(df)}")

    # 1. Selección de rezagos (misma lógica que Fase 2: VAR en niveles, AIC)
    sel = select_order(df[coint_vars], maxlags=6, deterministic="ci")
    lag_var = sel.aic
    k_ar_diff = max(1, lag_var - 1)
    print(f"\nRezago óptimo del VAR en niveles (AIC): {lag_var} -> k_ar_diff (VECM) = {k_ar_diff}")

    # 2. Rango de cointegración (Traza, regla secuencial)
    r, johansen_res = seleccionar_rango_cointegracion(df[coint_vars], det_order=0, k_ar_diff=k_ar_diff)
    print(f"Rango de cointegración hallado por Traza (regla secuencial): r = {r}")
    print(" (Nota: en Fase 2 la Traza señala rango pleno en esta muestra -posible distorsión")
    print("  de muestra pequeña-. Se impone r=1 por motivo económico: una única relación de")
    print("  largo plazo -la Función de Reacción Fiscal-, criterio estándar en esta literatura")
    print("  cuando el rango formal es ambiguo.)")

    coint_rank = 1  # relación de largo plazo única, motivada por la teoría (Bohn, 1998)

    if r == 0:
        print("\n[ADVERTENCIA] Test de Traza no rechaza r=0 en la regla estrictamente secuencial.")
        print("Se estima igualmente un VECM con rango impuesto r=1 (motivado por teoría) y,")
        print("como contraste, un VAR restringido en diferencias sin relación de largo plazo.")

    # 3. Estimación VECM (rango impuesto = 1)
    print("\n--- Estimación VECM (rango de cointegración = 1) ---")
    resultado = estimar_vecm(df, coint_vars, exog_vars, k_ar_diff, coint_rank)

    print("\nVector de cointegración (beta), normalizado por statsmodels:")
    beta_index = coint_vars if resultado.beta.shape[0] == len(coint_vars) else coint_vars + ["const"]
    beta = pd.DataFrame(resultado.beta, index=beta_index, columns=["beta"])
    print(beta.to_string())

    print("\nCoeficientes de ajuste (alpha, velocidad de corrección de desequilibrios):")
    alpha_df = pd.DataFrame(resultado.alpha, index=coint_vars, columns=["alpha"])
    print(alpha_df.to_string())

    # Relación de largo plazo normalizada sobre pb_pib, para comparar directamente
    # con el beta_1 (coeficiente de d_t-1) de la especificación DOLS:
    # pb_pib = ... - (beta_deuda / beta_pb) * deuda_pib - ...
    b = resultado.beta[:, 0]
    idx_pb = coint_vars.index("pb_pib")
    idx_deuda = coint_vars.index("deuda_pib")
    beta_deuda_normalizado = -b[idx_deuda] / b[idx_pb]

    alpha_pb = resultado.alpha[idx_pb, 0]
    print(f"\nCoeficiente de largo plazo de deuda_pib sobre pb_pib (análogo a beta_1 en DOLS):")
    print(f"  beta_deuda (normalizado sobre pb_pib) = {beta_deuda_normalizado:.4f}")
    print(f"Velocidad de ajuste de pb_pib hacia el equilibrio de largo plazo (alpha_pb): {alpha_pb:.4f}")

    print("\n" + "=" * 78)
    print(" Veredicto de Sostenibilidad Intertemporal (H0: beta_deuda <= 0) ")
    print("=" * 78)
    if beta_deuda_normalizado > 0:
        print(f" -> Coeficiente de largo plazo positivo ({beta_deuda_normalizado:.4f}).")
        print("    Consistente con reacción fiscal estabilizadora (condición de Bohn, 1998).")
    else:
        print(f" -> Coeficiente de largo plazo no positivo ({beta_deuda_normalizado:.4f}).")
        print("    No hay evidencia, bajo VECM, de reacción marginal positiva del resultado")
        print("    primario ante la deuda pasada.")

    # 4. Guardar resultados
    os.makedirs("resultados/tablas", exist_ok=True)
    beta.to_csv("resultados/tablas/fase3b_vecm_beta.csv")
    alpha_df.to_csv("resultados/tablas/fase3b_vecm_alpha.csv")
    with open("resultados/tablas/fase3b_vecm_resumen.txt", "w", encoding="utf-8") as f:
        f.write(resultado.summary().as_text())
    print("\n[OK] Resultados guardados en 'resultados/tablas/fase3b_vecm_*.csv/.txt'")


if __name__ == "__main__":
    main()
