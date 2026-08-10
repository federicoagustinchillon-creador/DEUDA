"""
empalme_historico_pre2004.py
=============================
Construye deuda_pib y pb_pib trimestrales para 1996T1-2003T4, para extender
el panel de 88 a ~120 observaciones (pedido del director: VAR/VECM requiere
una ventana temporal mayor, incluso con quiebres estructurales extremos).

Motivo del empalme: las fuentes API de datos.gob.ar para pb_pib y deuda_pib
no tienen datos anteriores a 2004 (IDs de serie discontinuados, ver nota en
ingesta_mecon_indec.py). La fuente oficial más completa para el período
faltante -el Compendio Fiscal 1993-2006 del Ministerio de Economía- es de
frecuencia ANUAL, no trimestral.

Procedimiento (dos pasos, documentados por separado):

1. Coeficiente de enlace (retropolación): las series del Compendio Fiscal no
   miden exactamente lo mismo que pb_pib/deuda_pib en el dataset actual
   (distinto perímetro institucional y, en el caso de deuda_pib, distinta
   valuación -dólares vs. base actual-). En vez de asumir que son la misma
   serie, se calcula un coeficiente de enlace en el año de solapamiento más
   cercano al punto de empalme (2004), y se aplica ese coeficiente a los
   valores anuales del Compendio antes de desagregar. Esto no elimina la
   diferencia de perímetro; la traslada a un único parámetro documentado en
   vez de dejarla implícita.

   ADVERTENCIA pb_pib: el coeficiente de enlace para pb_pib es MENOS estable
   que el de deuda_pib (el ratio compendio/dataset-actual pasa de 1.12 en
   2004 a ~2.07 en 2006 -no es una relación de escala constante-), lo que
   sugiere una diferencia de perímetro más profunda que una simple diferencia
   de valuación. Se usa igualmente el coeficiente del año de empalme (2004,
   el más cercano al punto de unión), documentado como la aproximación menos
   confiable de este script. Este límite queda declarado explícitamente en
   el dataset resultante (columna es_interpolado) y debe mencionarse como
   limitación en el capítulo de datos.

2. Desagregación temporal de Denton (Denton, 1971; sin serie indicadora
   auxiliar): dado que no hay una serie trimestral relacionada confiable
   para todo 1996-2003, se usa la variante de Denton sin indicador, que
   minimiza la suma de las diferencias trimestre a trimestre al cuadrado
   sujeto a que el promedio de los 4 trimestres de cada año coincida con el
   valor anual (ya reescalado por el coeficiente de enlace). Es el
   procedimiento estándar para pasar de anual a trimestral cuando no se
   dispone de una serie de alta frecuencia relacionada.

Fuente de los valores anuales: Compendio Fiscal 1993-2006, Ministerio de
Economía y Producción, Secretaría de Hacienda, Oficina Nacional de
Presupuesto (https://www.economia.gob.ar/onp/documentos/ejectexto/compendio/compendio93-06.pdf).
  - deuda_pib: Cap. IV.1 "Deuda Total del Sector Público Nacional por
    Instrumento", fila "En % PIB en dólares", 1992-2006.
  - pb_pib: Cap. I.1.3 "Cuenta Ahorro-Inversión-Financiamiento, Sector
    Público Nacional, en porcentaje del PIB", fila "IX Resultado Primario",
    1994-2006.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, LinearConstraint

# ---------------------------------------------------------------------------
# 1. Valores anuales transcriptos del Compendio Fiscal 1993-2006
# ---------------------------------------------------------------------------

DEUDA_PIB_ANUAL_COMPENDIO = {
    1992: 30.37, 1993: 30.07, 1994: 31.78, 1995: 34.38, 1996: 36.39,
    1997: 35.42, 1998: 38.18, 1999: 43.51, 2000: 45.65, 2001: 53.67,
    2002: 166.39, 2003: 138.75, 2004: 127.30, 2005: 73.85, 2006: 63.97,
}

PB_PIB_ANUAL_COMPENDIO = {
    1994: 0.41, 1995: -0.11, 1996: -1.15, 1997: 0.49, 1998: 0.49,
    1999: -0.10, 2000: 1.28, 2001: 0.06, 2002: 2.35, 2003: 3.11,
    2004: 4.01, 2005: 2.76, 2006: 3.20,
}

# Coeficiente de enlace: dataset-actual / compendio, en el año de empalme (2004)
LINK_DEUDA_PIB = 110.25 / 127.30   # ~0.866
LINK_PB_PIB = 4.5 / 4.01           # ~1.122


# ---------------------------------------------------------------------------
# 2. Desagregación de Denton (proporcional, sin indicador)
# ---------------------------------------------------------------------------

def denton_sin_indicador(valores_anuales, anios, anclas_futuras=None):
    """
    Distribuye una serie de valores anuales (promedios, no sumas -por eso
    'sin indicador' con restricción de promedio, no de suma) en trimestres,
    minimizando la variación trimestre a trimestre bajo la restricción de
    que el promedio de los 4 trimestres de cada año reproduzca el valor
    anual dado. Denton (1971), variante aditiva sin serie indicadora.

    anclas_futuras: trimestres reales ya conocidos inmediatamente
    posteriores al último año de valores_anuales (p. ej. 2004T1-2006T4,
    que sí son datos genuinos, no interpolados). Se incluyen en el término
    de suavidad (para que los últimos trimestres estimados empalmen sin
    salto artificial contra el primer dato real) pero NO se optimizan ni
    se les exige ninguna restricción de promedio anual: actúan como puntos
    fijos que anclan el extremo de la serie estimada.
    """
    n_anios = len(anios)
    n_trim = n_anios * 4
    anclas = np.asarray(anclas_futuras) if anclas_futuras is not None else np.array([])
    n_ancla = len(anclas)

    x0 = np.repeat(valores_anuales, 4)

    def objetivo(x):
        x_full = np.concatenate([x, anclas])
        d = np.diff(x_full)
        return np.sum(d ** 2)

    def objetivo_grad(x):
        x_full = np.concatenate([x, anclas])
        d = np.diff(x_full)
        g_full = np.zeros_like(x_full)
        g_full[:-1] -= 2 * d
        g_full[1:] += 2 * d
        return g_full[:n_trim]  # gradiente solo respecto de los trimestres libres

    A = np.zeros((n_anios, n_trim))
    for i in range(n_anios):
        A[i, 4 * i:4 * i + 4] = 0.25
    restriccion = LinearConstraint(A, valores_anuales, valores_anuales)

    res = minimize(
        objetivo, x0, jac=objetivo_grad, method="SLSQP",
        constraints=[restriccion], options={"maxiter": 500, "ftol": 1e-12},
    )
    if not res.success:
        raise RuntimeError(f"Denton no convergió: {res.message}")
    return res.x


def construir_serie_trimestral(dict_anual, link, anio_inicio, anio_fin, anclas_futuras=None):
    anios = list(range(anio_inicio, anio_fin + 1))
    valores = np.array([dict_anual[a] * link for a in anios])
    trimestral = denton_sin_indicador(valores, anios, anclas_futuras=anclas_futuras)

    fechas = pd.date_range(f"{anio_inicio}-01-01", periods=len(trimestral), freq="QE")
    return pd.Series(trimestral, index=fechas)


def main():
    # Trimestres reales 2004T1-2006T4 (genuinos, ya presentes en
    # dataset_consolidado_real.csv), usados como anclas para que la
    # desagregación de 2003 no termine en un salto artificial contra el
    # primer dato real de 2004.
    df_real = pd.read_csv(
        "datos/dataset_consolidado_real.csv", parse_dates=["Date"], index_col="Date"
    )
    anclas_deuda = df_real.loc["2004-01-01":"2006-12-31", "deuda_pib"].to_numpy()
    anclas_pb = df_real.loc["2004-01-01":"2006-12-31", "pb_pib"].to_numpy()

    # Se corre Denton sobre una ventana algo más amplia que la que se
    # conserva (buffer 1992/1994-1995), para reducir el sesgo de borde del
    # ajuste; solo se conservan los trimestres 1996T1-2003T4 en el resultado
    # final, que es lo que efectivamente hace falta para llegar a ~120 obs.
    deuda_trim = construir_serie_trimestral(
        DEUDA_PIB_ANUAL_COMPENDIO, LINK_DEUDA_PIB, 1992, 2003,
        anclas_futuras=anclas_deuda,
    )
    pb_trim = construir_serie_trimestral(
        PB_PIB_ANUAL_COMPENDIO, LINK_PB_PIB, 1994, 2003,
        anclas_futuras=anclas_pb,
    )

    deuda_trim = deuda_trim.loc["1996-01-01":"2003-12-31"]
    pb_trim = pb_trim.loc["1996-01-01":"2003-12-31"]

    df = pd.DataFrame({"deuda_pib": deuda_trim, "pb_pib": pb_trim})
    df["es_interpolado"] = 1  # mismo criterio que pib_nominal_es_extrapolado

    print("Verificación: promedio anual reconstruido vs. valor anual empalmado")
    for anio in range(1996, 2004):
        prom_deuda = df.loc[f"{anio}", "deuda_pib"].mean()
        obj_deuda = DEUDA_PIB_ANUAL_COMPENDIO[anio] * LINK_DEUDA_PIB
        prom_pb = df.loc[f"{anio}", "pb_pib"].mean()
        obj_pb = PB_PIB_ANUAL_COMPENDIO[anio] * LINK_PB_PIB
        print(f"  {anio}: deuda_pib {prom_deuda:.4f} (obj {obj_deuda:.4f}) | "
              f"pb_pib {prom_pb:.4f} (obj {obj_pb:.4f})")

    print("\nPrimeras y últimas filas:")
    print(df.head(4).to_string())
    print(df.tail(4).to_string())

    out_path = "datos/empalme_pre2004_deuda_pb.csv"
    df.to_csv(out_path, index_label="Date")
    print(f"\n[OK] Guardado en {out_path} ({len(df)} filas, 1996T1-2003T4)")


if __name__ == "__main__":
    main()
