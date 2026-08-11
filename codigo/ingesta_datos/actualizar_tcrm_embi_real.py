"""
actualizar_tcrm_embi_real.py
=============================
Reemplaza las columnas TCRM y EMBI de dataset_consolidado_real.csv (matriz
original, 88 observaciones, 2004T1-2025T4) por las series reales de fuente
primaria construidas para la ventana ampliada (tcrm_real_bcra_1997_2025.csv,
embi_real_ambito_1999_2025.csv), en lugar de los valores de contingencia
usados hasta este punto.

Motivo: la auditoría de trazabilidad de fuentes (ver nota en
ingesta_mecon_indec.py y Sección 4.2.2 de la tesis) encontró que TCRM y
EMBI+ correspondían en su totalidad, en las 88 observaciones originales, a
la fuente de contingencia y no a un llamado API exitoso. Al reemplazarlas
por series reales en la matriz ampliada (construir_dataset_ampliado.py), se
decidió -para no sostener dos versiones incompatibles de estas variables en
la misma tesis- propagar el mismo reemplazo a la matriz original de 88
observaciones y re-ejecutar el protocolo completo que depende de ella
(Fases 1 a 5, 7, 10, 12 y 13).

Este script SOBREESCRIBE dataset_consolidado_real.csv. La versión anterior
queda preservada en el historial de git de la rama (commit "Commit inicial:
tesis y codigo completo" y el checkpoint de la etapa VECM), no en un
archivo .bak adicional.
"""

import pandas as pd
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATOS = BASE_DIR / "datos"


def main():
    path_real = DATOS / "dataset_consolidado_real.csv"
    df = pd.read_csv(path_real, parse_dates=["Date"], index_col="Date")

    tcrm_real = pd.read_csv(
        DATOS / "tcrm_real_bcra_1997_2025.csv", parse_dates=["Date"], index_col="Date"
    )["TCRM"]
    embi_real = pd.read_csv(
        DATOS / "embi_real_ambito_1999_2025.csv", parse_dates=["Date"], index_col="Date"
    )["EMBI"]

    tcrm_antes = df["TCRM"].copy()
    embi_antes = df["EMBI"].copy()

    df["TCRM"] = tcrm_real.reindex(df.index)
    df["EMBI"] = embi_real.reindex(df.index)

    faltantes_tcrm = df["TCRM"].isna().sum()
    faltantes_embi = df["EMBI"].isna().sum()
    if faltantes_tcrm or faltantes_embi:
        raise RuntimeError(
            f"Reindexado incompleto: {faltantes_tcrm} NaN en TCRM, "
            f"{faltantes_embi} NaN en EMBI. Revisar cobertura de las series reales."
        )

    print("TCRM: contingencia -> real")
    print(f"  Media anterior: {tcrm_antes.mean():.3f}  |  Media nueva: {df['TCRM'].mean():.3f}")
    print(f"  Correlación entre ambas series en la ventana 2004-2025: {tcrm_antes.corr(df['TCRM']):.3f}")
    print("\nEMBI: contingencia -> real")
    print(f"  Media anterior: {embi_antes.mean():.1f}  |  Media nueva: {df['EMBI'].mean():.1f}")
    print(f"  Correlación entre ambas series en la ventana 2004-2025: {embi_antes.corr(df['EMBI']):.3f}")

    df.to_csv(path_real, index_label="Date")
    print(f"\n[OK] {path_real} actualizado con TCRM y EMBI de fuente primaria real.")


if __name__ == "__main__":
    main()
