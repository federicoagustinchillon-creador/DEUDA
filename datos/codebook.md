# Codebook — Dataset Consolidado Tesis

## Identificación
- **Título:** Datos para "La solvencia intertemporal de la deuda pública consolidada argentina post-2025"
- **Autores:** Santiago Páez, Federico Chillón, Emiliano Carricondo
- **Institución:** Universidad Nacional de Cuyo — FCE
- **Fecha:** 2026
- **Dos ventanas muestrales** (ver detalle de por qué hay dos archivos en [`README.md`](README.md)):
  - `dataset_consolidado_real.csv`: Q1 2004 — Q4 2025 (88 observaciones trimestrales), ventana original.
  - `dataset_consolidado_real_ext.csv`: Q1 1999 — Q4 2025 (108 observaciones trimestrales), ventana ampliada por empalme histórico — **referencia actual (VECM)**.

## Variables núcleo (presentes en ambos archivos)

| Variable | Descripción | Fuente Primaria | Fuente Fallback | Unidad | Transformación |
|---|---|---|---|---|---|
| Date | Trimestre de observación | N/A | — | Fecha | — |
| VIX | Índice de Volatilidad CBOE | Yahoo Finance (^VIX) | — | Puntos | Promedio trimestral |
| EMBI | EMBI+ Argentina (Riesgo País) | Ámbito Financiero API / datos.gob.ar | JP Morgan / BCRA / CEPAL cross-check | Puntos básicos | Promedio trimestral |
| CER | Coeficiente de Estabilización de Referencia | BCRA / datos.gob.ar ID: 94.2_CD_D_0_0_10 | BCRA Informe Monetario | Var. % trimestral | Acumulado trimestral |
| TCRM | Tipo de Cambio Real Multilateral | datos.gob.ar ID: 116.4_TCRM_0_0_29 | BCRA Informe Monetario | Índice dic-2001=1 | Promedio trimestral |
| PIB_real | PIB a precios constantes (base 2004) | INDEC / datos.gob.ar ID: 143.3_NO_PR_2004_A_21 | INDEC DNCN | Índice de volumen | Promedio trimestral |
| pb_pib | Resultado primario SPN / PIB | MECON / datos.gob.ar ID: 11.3_RDP_0_0_32 | MECON Cuadro Fiscal | % del PIB | Anual -> trimestral pro-rata |
| deuda_pib | Deuda pública neta / PIB | MECON Informe de Deuda / datos.gob.ar | FMI WEO Apr 2024 ARG | % del PIB | Fin de trimestre |
| g_gap | Brecha del producto (output gap) | Derivado de PIB_real | — | % del PIB potencial | Filtro HP (λ=1600) |

## Variables adicionales

Solo en `dataset_consolidado_real.csv` (usadas por scripts puntuales — IV-2SLS y consolidación de deuda BCRA):

| Variable | Descripción | Usada por |
|---|---|---|
| EMBI_BRASIL | Spread soberano ETF EMB Brasil, instrumento de IV-2SLS | `codigo/modelos/fase4_variables_instrumentales.py` |
| pasivos_bcra_ars | Pasivos remunerados del BCRA (LELIQ/NOTALIQ/Pases), en pesos corrientes | `codigo/modelos/fase8_deuda_consolidada.py` |
| pib_nominal_trim | PIB nominal trimestral | Consolidación de deuda (denominador) |
| pib_nominal_es_extrapolado | Marca si el trimestre de PIB nominal fue extrapolado por no estar aún publicado | Control de calidad de `fase8` |
| pasivos_bcra_pib | Pasivos remunerados del BCRA / PIB (%) | `codigo/modelos/fase8_deuda_consolidada.py` |

Solo en `dataset_consolidado_real_ext.csv` (empalme histórico):

| Variable | Descripción |
|---|---|
| es_interpolado | Booleano: `True` si la observación (tramo 1999–2003) proviene del empalme histórico en vez de la serie original directa |

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
