"""
construccion_dataset.py
================
Proceso maestro de construcción del dataset consolidado.
Ejecuta los tres scripts de ingestión y combina las salidas
en un único dataset_consolidado_real.csv con documentación de calidad.

Variables en el dataset final:
  - Date           : fin de trimestre (YYYY-MM-DD)
  - VIX            : Índice de Volatilidad (promedio trimestral, puntos)
  - EMBI           : EMBI+ Argentina (promedio trimestral, puntos básicos)
  - CER            : Var. % trimestral del CER
  - TCRM           : Tipo de Cambio Real Multilateral (índice dic-2001=1)
  - PIB_real       : Índice de Volumen del PIB (base 2004 Q1 = 100)
  - pb_pib         : Resultado primario SPN / PIB (%)
  - deuda_pib      : Deuda pública neta / PIB (%)
  - g_gap          : Brecha del producto — output gap (%)

Ejecutar desde el directorio raíz del proyecto (c:/Users/fedea/Deuda):
  python codigo/ingesta_datos/construccion_dataset.py
"""

import sys
import os
import pandas as pd
import numpy as np

# Agregar el directorio del script al path (para importar los otros modulos de ingesta)
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import ingesta_datos_financieros as fin
import ingesta_bcra as bcra
import ingesta_mecon_indec as mecon


def run_all_ingestion() -> pd.DataFrame:
    """Ejecuta los tres módulos de ingestión y combina los resultados."""
    print("=" * 65)
    print(" BUILD DATASET — Tesis: Solvencia Intertemporal Argentina")
    print("=" * 65)

    # 1. Datos financieros (VIX, EMBI)
    print("\n>>> MÓDULO 1: Datos Financieros (VIX + EMBI+)")
    fin.main()

    # 2. Datos BCRA (CER, TCRM)
    print("\n>>> MÓDULO 2: Datos BCRA (CER + TCRM)")
    bcra.main()

    # 3. Datos MECON/INDEC (PIB, resultado primario, deuda)
    print("\n>>> MÓDULO 3: Datos MECON / INDEC")
    mecon.main()

    # 4. Spread soberano regional (EMB / EMBI_BRASIL - Instrumento IV)
    print("\n>>> MÓDULO 4: Spread Soberano Regional (ETF EMB)")
    try:
        import ingesta_spread_regional as spread
        spread.main()
    except Exception as e:
        print(f"[!] Aviso ingesta spread regional: {e}")

    # 5. Pasivos remunerados del BCRA
    print("\n>>> MÓDULO 5: Pasivos Remunerados del BCRA")
    try:
        import ingesta_bcra_pasivos as pasivos
        pasivos.main()
    except Exception as e:
        print(f"[!] Aviso ingesta pasivos BCRA: {e}")

    # --- Cargar archivos procesados ---
    finance = pd.read_csv("datos/procesados/financiero_trimestral.csv", index_col=0)
    bcra_df = pd.read_csv("datos/procesados/bcra_trimestral.csv", index_col=0)
    macro   = pd.read_csv("datos/procesados/macro_trimestral.csv", index_col=0)

    # Convertir índices a PeriodIndex trimestral (Q)
    finance.index = pd.to_datetime(finance.index).to_period("Q")
    bcra_df.index = pd.to_datetime(bcra_df.index).to_period("Q")
    macro.index   = pd.to_datetime(macro.index).to_period("Q")

    # Combinar datasets principales
    df = finance.copy()
    for other in [bcra_df, macro]:
        cols_to_use = [c for c in other.columns if c not in df.columns]
        if cols_to_use:
            df = pd.merge(df, other[cols_to_use], left_index=True, right_index=True, how="outer")

    # Fusionar spread regional (EMB / EMBI_BRASIL) si existe
    if os.path.exists("datos/procesados/spread_regional_trimestral.csv"):
        spread_df = pd.read_csv("datos/procesados/spread_regional_trimestral.csv", index_col=0)
        spread_df.index = pd.to_datetime(spread_df.index).to_period("Q")
        if "EMBI_BRASIL" in spread_df.columns:
            if "EMBI_BRASIL" in df.columns:
                df = df.drop(columns=["EMBI_BRASIL"])
            df = pd.merge(df, spread_df[["EMBI_BRASIL"]], left_index=True, right_index=True, how="left")

    # Fusionar pasivos BCRA si existe
    if os.path.exists("datos/procesados/bcra_pasivos_trimestral.csv"):
        pasivos_df = pd.read_csv("datos/procesados/bcra_pasivos_trimestral.csv", index_col=0)
        pasivos_df.index = pd.to_datetime(pasivos_df.index).to_period("Q")
        cols_to_merge = [c for c in pasivos_df.columns if c not in df.columns]
        if cols_to_merge:
            df = pd.merge(df, pasivos_df[cols_to_merge], left_index=True, right_index=True, how="left")

    df = df.sort_index()
    df = df.loc["2004Q1":"2025Q4"]
    # Convertir el índice final a fecha de fin de trimestre (YYYY-MM-DD)
    df.index = df.index.to_timestamp("Q")
    df.index.name = "Date"

    return df




def quality_report(df: pd.DataFrame) -> None:
    """Imprime un informe de calidad del dataset."""
    print("\n" + "=" * 65)
    print(" INFORME DE CALIDAD DEL DATASET")
    print("=" * 65)
    print(f"\n  Período: {df.index.min().date()} -> {df.index.max().date()}")
    print(f"  Observaciones totales: {len(df)}")
    print(f"  Variables: {list(df.columns)}")
    print(f"\n  Cobertura por variable:")
    for col in df.columns:
        valid = df[col].notna().sum()
        pct = valid / len(df) * 100
        status = "[OK]" if pct >= 80 else "[!]" if pct >= 50 else "[X]"
        print(f"    {status} {col:20s}: {valid:3d}/{len(df)} ({pct:.1f}%)")
    print(f"\n  Estadísticas descriptivas:")
    print(df.describe().round(2).to_string())


def save_codebook(df: pd.DataFrame, path: str) -> None:
    """Genera el codebook de datos (AEA Data Policy)."""
    codebook = """# Codebook — Dataset Consolidado Tesis

## Identificación
- **Título:** Datos para "La solvencia intertemporal de la deuda consolidada argentina post-2025"
- **Autor:** Federico [Apellido]
- **Institución:** Universidad Nacional de Cuyo — FCE
- **Fecha:** 2026
- **Período:** Q1 2004 — Q4 2025 (88 observaciones trimestrales)

## Variables

| Variable | Descripción | Fuente Primaria | Fuente Fallback | Unidad | Transformación |
|---|---|---|---|---|---|
| VIX | Índice de Volatilidad CBOE | Yahoo Finance (^VIX) | — | Puntos | Promedio trimestral |
| EMBI | EMBI+ Argentina (Riesgo País) | Ámbito Financiero API / datos.gob.ar | JP Morgan / BCRA / CEPAL cross-check | Puntos básicos | Promedio trimestral |
| CER | Coeficiente de Estabilización de Referencia | BCRA / datos.gob.ar ID: 94.2_CD_D_0_0_10 | BCRA Informe Monetario | Var. % trimestral | Acumulado trimestral |
| TCRM | Tipo de Cambio Real Multilateral | datos.gob.ar ID: 116.4_TCRM_0_0_29 | BCRA Informe Monetario | Índice dic-2001=1 | Promedio trimestral |
| PIB_real | PIB a precios constantes (base 2004) | INDEC / datos.gob.ar ID: 143.3_NO_PR_2004_A_21 | INDEC DNCN | Índice de volumen | Promedio trimestral |
| pb_pib | Resultado primario SPN / PIB | MECON / datos.gob.ar ID: 11.3_RDP_0_0_32 | MECON Cuadro Fiscal | % del PIB | Anual -> trimestral pro-rata |
| deuda_pib | Deuda pública neta / PIB | MECON Informe de Deuda / datos.gob.ar | FMI WEO Apr 2024 ARG | % del PIB | Fin de trimestre |
| g_gap | Brecha del producto (output gap) | Derivado de PIB_real | — | % del PIB potencial | Filtro HP (λ=1600) |

## Notas Metodológicas
1. **Signo pb_pib:** Positivo = superávit primario; negativo = déficit primario.
2. **Deuda consolidada:** Incluye deuda intra-sector público (FGS-ANSES); la corrección neta reduce el ratio bruto en ~15-20 pp según el año.
3. **EMBI+ fuente de fallback:** Los valores del fallback son promedios trimestrales construidos desde series publicadas por BCRA ("Informe Monetario Mensual"), CEPAL STAT y FMI IFS (Argentina, riesgo soberano). Todos los valores fueron cruzados entre mínimo dos fuentes.
4. **Output gap:** Se aplica filtro HP con λ=1600 (estándar para datos trimestrales). El sesgo de endpoint es reconocido; como análisis de sensibilidad considerar el filtro de Hamilton (2018).
5. **Período 2023-2025:** Los datos del período Milei incorporan la corrección cambiaria de dic-2023 y el programa de estabilización. Los valores de EMBI+ reflejan la compresión de spreads a partir de la consolidación fiscal.

## Citas de Fuentes Primarias
- BCRA (2024). *Informe Monetario Mensual*. Buenos Aires: Banco Central de la República Argentina.
- INDEC (2024). *Cuentas Nacionales: PIB por enfoque del gasto*. Buenos Aires: Instituto Nacional de Estadística y Censos.
- MECON (2024). *Informe de Deuda Pública*. Buenos Aires: Ministerio de Economía de la Nación.
- FMI (2024). *World Economic Outlook Database*, April 2024. Washington D.C.: International Monetary Fund.
- datos.gob.ar (2024). *API de Series de Tiempo*. Buenos Aires: Gobierno de la República Argentina. https://apis.datos.gob.ar/series/
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(codebook)
    print(f"\n[OK] Codebook guardado en: {path}")


def main():
    # Asegurarse de estar en el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    os.chdir(project_root)
    print(f"Directorio de trabajo: {os.getcwd()}")

    df = run_all_ingestion()

    # Guardar dataset consolidado
    os.makedirs("datos", exist_ok=True)
    output_path = "datos/dataset_consolidado_real.csv"
    df.to_csv(output_path)
    print(f"\n[OK] Dataset consolidado guardado en: {output_path}")

    # Informe de calidad
    quality_report(df)

    # Codebook
    save_codebook(df, "datos/codebook.md")

    # Validación final
    required = ["VIX", "EMBI", "CER", "TCRM", "PIB_real", "pb_pib", "deuda_pib", "g_gap"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"\n[!] ADVERTENCIA: Columnas faltantes: {missing}")
    else:
        coverage_ok = all(df[c].notna().mean() >= 0.80 for c in required)
        if coverage_ok:
            print("\n[OK] VALIDACION EXITOSA: Todas las variables tienen >=80% de cobertura.")
            print("  El dataset está listo para la Fase 1 (tests de raíz unitaria).")
        else:
            for c in required:
                pct = df[c].notna().mean()
                if pct < 0.80:
                    print(f"\n[!] Cobertura insuficiente: {c} = {pct:.1%}")


if __name__ == "__main__":
    main()
