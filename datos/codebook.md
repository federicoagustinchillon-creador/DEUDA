# Codebook — Dataset Consolidado Tesis

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
