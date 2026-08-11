"""
fase17_calibracion_nu_dsa.py
==============================
Recalibra los grados de libertad (nu) de la distribución t de Student
multivariada del DSA estocástico (fase6_sostenibilidad_deuda.py,
DSA_STUDENT_T_NU) sobre los shocks históricos reales de resultado primario
y tipo de cambio real, ahora que TCRM ya no es la serie de contingencia
(ver actualizar_tcrm_embi_real.py).

El ajuste original (nu=5.1) se estimó por máxima verosimilitud conjunta de
los tres parámetros de la t (loc, scale, nu) sobre el TCRM de contingencia.
Repetir ese mismo ajuste (scipy.stats.t.fit) sobre el TCRM real da nu=1.54
para el shock de resultado primario y nu=2.61 para el de tipo de cambio
real -por debajo de 2, varianza teóricamente infinita-, arrastrado por un
puñado de trimestres genuinamente extremos (devaluación de 2016, crisis de
2018, ajuste fiscal y cambiario de 2023-2024) que no son errores de datos,
pero sí generan un patrón de inestabilidad conocido del MLE conjunto sin
restringir en muestras chicas: la superficie de verosimilitud es casi plana
para nu bajo, y un par de observaciones extremas aisladas pueden arrastrar
la estimación hacia una solución de esquina que "explica" esos puntos vía
cola infinita en lugar de reflejar la forma de la distribución en su
conjunto.

Se adopta en su lugar el estimador por método de momentos (ajuste por
curtosis en exceso), más robusto frente a esa patología porque no depende
de la verosimilitud conjunta de los tres parámetros: para una t de Student,
la curtosis en exceso poblacional es 6/(nu-4) (nu>4), de donde
nu = 4 + 6/curtosis_exceso_muestral. Es el mismo estadístico (curtosis en
exceso) que ya cita el Capítulo 7 de la tesis como evidencia de colas
pesadas, aplicado ahora como estimador y no solo como diagnóstico.
"""

import pandas as pd
import numpy as np
import os
import pathlib
from scipy.stats import t as t_dist

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS = BASE_DIR / "datos"
RESULTADOS = BASE_DIR / "resultados" / "tablas"


def nu_mle_conjunto(serie):
    """MLE conjunto (loc, scale, nu) vía scipy.stats.t.fit -método original-."""
    nu, loc, scale = t_dist.fit(serie)
    return nu


def nu_metodo_momentos(serie):
    """nu = 4 + 6/curtosis_exceso, válido para curtosis_exceso > 0 (nu>4)."""
    k = serie.kurtosis()
    if k <= 0:
        return np.inf
    return 4 + 6 / k


def main():
    print("=" * 78)
    print(" FASE 17: RECALIBRACIÓN DE NU (COLAS GORDAS, DSA ESTOCÁSTICO)")
    print("=" * 78)

    df = pd.read_csv(DATOS / "dataset_consolidado_real.csv", parse_dates=["Date"], index_col="Date")
    pb_shock = df["pb_pib"].diff().dropna()
    delta_e_shock = (df["TCRM"].pct_change() * 100).dropna()

    filas = []
    for nombre, serie in [("resultado_primario (dpb)", pb_shock), ("tipo_cambio_real (TCRM, %var)", delta_e_shock)]:
        k = serie.kurtosis()
        nu_mle = nu_mle_conjunto(serie)
        nu_mm = nu_metodo_momentos(serie)
        print(f"\n{nombre}: n={len(serie)}  curtosis_exceso={k:.2f}")
        print(f"  nu (MLE conjunto, loc/scale/nu)  = {nu_mle:.2f}")
        print(f"  nu (método de momentos, curtosis) = {nu_mm:.2f}")
        filas.append({
            "Variable": nombre,
            "n": len(serie),
            "Curtosis_exceso": round(k, 2),
            "nu_MLE_conjunto": round(nu_mle, 2),
            "nu_metodo_momentos": round(nu_mm, 2),
        })

    tabla = pd.DataFrame(filas)
    nu_final = round(tabla["nu_metodo_momentos"].mean(), 1)

    print("\n" + "=" * 78)
    print(f" NU FINAL ADOPTADO (promedio, método de momentos): {nu_final}")
    print(" (Compartido entre las tres variables del DSA -pb, g, delta_e-, ")
    print("  mismo criterio de conservadurismo que la calibración original, ")
    print("  que también promediaba y compartía un nu único entre las tres.)")
    print("=" * 78)

    os.makedirs(RESULTADOS, exist_ok=True)
    tabla.to_csv(RESULTADOS / "fase17_calibracion_nu_dsa.csv", index=False)
    with open(RESULTADOS / "fase17_nu_final.txt", "w", encoding="utf-8") as f:
        f.write(str(nu_final))
    print(f"\n[OK] Resultados guardados en 'resultados/tablas/fase17_calibracion_nu_dsa.csv' y 'fase17_nu_final.txt'")


if __name__ == "__main__":
    main()
