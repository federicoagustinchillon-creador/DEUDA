# Codebook

Datos de la tesis "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035". Ventana de estimación 1998T2-2025T4 (111 trimestres); series desde 1996T1 para los rezagos y los empalmes. Las fuentes y el tratamiento de cada serie están en el Capítulo 5 y en el Apéndice A.2.

## Panel `dataset_consolidado_1996_2025.csv`

| Variable | Descripción | Unidad | Fuente |
|---|---|---|---|
| Date | Fin de trimestre | Fecha | |
| PIB_real | PIB a precios constantes de 2004, desde 2004T1 | Índice de volumen | INDEC (datos.gob.ar, serie 143.3_NO_PR_2004_A_21) |
| TCRM | Tipo de cambio real multilateral | Índice, diciembre de 2001 = 1 | BCRA (serie 116.4_TCRM_0_0_29), promedio trimestral; 1996 encadenado con el tipo de cambio real efectivo amplio del BIS |
| EMBI | Diferencial soberano del índice EMBI de J.P. Morgan para Argentina | Puntos básicos | J.P. Morgan, serie diaria publicada por Ámbito Financiero desde el 11 de diciembre de 1998, promedio trimestral; 1996T1-1998T3 reconstruido con la tasa interbancaria en dólares del BCRA |
| EMBI_fuente, TCRM_fuente | Origen de cada trimestre de EMBI y TCRM | Texto | |
| es_interpolado | Trimestre de deuda federal bruta interpolado linealmente en dólares (no son de diciembre de 1996-1997; el MECON publica la serie trimestral desde 1998T1). Solo interviene en la detección de quiebres | 0/1 (6 trimestres) | |
| es_empalme_pib | PIB real 1996-2003 empalmado de la base 1993 del INDEC | 0/1 (32 trimestres) | |
| es_empalme_embi | EMBI de 1996T1-1998T3 reconstruido | 0/1 (11 trimestres) | |
| es_interpolado_tcrm | TCRM de 1996 reconstruido | 0/1 (4 trimestres) | |

El modelo toma del panel el EMBI, el TCRM y el PIB real posterior a 2003; el PIB real de 1996-2003 lo toma de `procesados/pib_real_empalme_indec_1996_2003.csv`.

## Series en `procesados/` que lee el modelo

| Archivo | Columna usada | Descripción | Unidad | Fuente |
|---|---|---|---|---|
| `resultado_primario_1996_2025.csv` | `pb_pib_trim_sin_rentas` | Resultado primario del Sector Público Nacional sin rentas de la propiedad, base caja, flujo trimestral anualizado sobre el PIB nominal de cuatro trimestres. Positivo = superávit | % del PIB | MECON, Administración Central e instituciones (datos.gob.ar, conjunto 379) |
| `deuda_consolidada_neta_nominal_1996_2025.csv` | `bruta_federal_pib` | Deuda bruta del gobierno federal, principal | % del PIB | Secretaría de Finanzas (MECON) |
| `deuda_consolidada_neta_nominal_1996_2025.csv` | `deuda_consolidada_neta_nominal_pib` | Deuda consolidada con el BCRA, extensión (Letras Intransferibles a valor nominal) | % del PIB | MECON y BCRA |
| `tasa_fed_trimestral_1996_2025.csv` | `tasa_politica_fed` | Tasa de fondos federales, promedio trimestral; en el límite cero, tasa sombra de Wu y Xia (2016). `fuente_flag` indica cuál se usa en cada trimestre | % anual | FRED y Banco de la Reserva Federal de Atlanta |
| `instrumentos_1996_2025.csv` | `VIX` | Índice de volatilidad de CBOE, promedio trimestral | Puntos | Yahoo Finance (^VIX) |
| `empalmes_1996_1998.csv` | `EMBI`, `TCRM` | EMBI y TCRM reconstruidos de 1996-1998 con su fuente | | Apéndice A.2 |
| `escenario_base_fmi_cr26105.csv` | | Escenario base del FMI, Informe de País 26/105 (mayo de 2026), cuadros 6 y 7 | | FMI |

## Notas

1. Resultado primario: positivo es superávit y negativo, déficit.
2. La tesis usa una sola definición del resultado primario, sin rentas de la propiedad. La serie con rentas (`pb_pib_trim`) se usa solo como robustez.
3. Los datos crudos están en `crudos/` y no se modifican. Los CSV de `crudos/no_referenciados/` no los usa ningún script.
