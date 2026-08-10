"""
empalme_pib_real_pre2004.py
=============================
Construye PIB_real trimestral para 1996T1-2003T4, mismo objetivo que
empalme_historico_pre2004.py pero para el índice de volumen del PIB.

A diferencia de deuda_pib/pb_pib, acá no hace falta un coeficiente de enlace
de perímetro: la tasa de crecimiento real del PIB argentino no tiene la
ambigüedad institucional del resultado fiscal (no hay "SPNF vs. Administración
Nacional"), así que se puede reconstruir el nivel anual encadenando hacia
atrás desde el propio dato real de 2004 con tasas de crecimiento anuales
ampliamente publicadas y no controvertidas (INDEC / Banco Mundial):

  1996: +4.0%  1997: +8.1%  1998: +3.8%  1999: -3.4%
  2000: -0.5%  2001: -4.5%  2002: -10.9% 2003: +8.8%  2004: +9.0%

Procedimiento:
  1. Nivel anual 2004 = promedio del índice trimestral real ya presente en
     dataset_consolidado_real.csv (base 2004T1=100).
  2. Encadenar hacia atrás: nivel(a-1) = nivel(a) / (1 + crecimiento(a)).
  3. Desagregación de Denton (misma función que empalme_historico_pre2004.py),
     anclada contra los trimestres reales 2004T1-2006T4 para evitar un salto
     artificial en el empalme.
"""

import numpy as np
import pandas as pd
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from empalme_historico_pre2004 import denton_sin_indicador

CRECIMIENTO_ANUAL = {
    1997: 0.081, 1998: 0.038, 1999: -0.034, 2000: -0.005,
    2001: -0.045, 2002: -0.109, 2003: 0.088, 2004: 0.090,
}


def main():
    _base_dir = pathlib.Path(__file__).parent.parent.parent
    df_real = pd.read_csv(
        _base_dir / "datos" / "dataset_consolidado_real.csv",
        parse_dates=["Date"], index_col="Date",
    )

    nivel_2004 = df_real.loc["2004-01-01":"2004-12-31", "PIB_real"].mean()
    niveles = {2004: nivel_2004}
    for anio in [2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997]:
        niveles[anio - 1] = niveles[anio] / (1 + CRECIMIENTO_ANUAL[anio])

    anios = list(range(1996, 2004))
    valores = np.array([niveles[a] for a in anios])

    print("Niveles anuales de PIB_real reconstruidos (índice, base 2004T1=100):")
    for a in anios:
        print(f"  {a}: {niveles[a]:.3f}")

    anclas = df_real.loc["2004-01-01":"2006-12-31", "PIB_real"].to_numpy()
    trimestral = denton_sin_indicador(valores, anios, anclas_futuras=anclas)

    fechas = pd.date_range("1996-01-01", periods=len(trimestral), freq="QE")
    serie = pd.Series(trimestral, index=fechas, name="PIB_real")

    print(f"\nEmpalme 2003T4 (estimado) = {serie.iloc[-1]:.3f}"
          f" vs. 2004T1 (real) = {df_real.loc['2004-03-31', 'PIB_real']:.3f}"
          f" -> salto de {abs(df_real.loc['2004-03-31', 'PIB_real'] - serie.iloc[-1]):.3f} puntos")

    out = _base_dir / "datos" / "pib_real_empalme_1996_2003.csv"
    df_out = serie.to_frame()
    df_out["es_interpolado"] = 1
    df_out.to_csv(out, index_label="Date")
    print(f"\n[OK] Guardado en {out} ({len(df_out)} filas)")


if __name__ == "__main__":
    main()
