# Ingesta de datos

Los insumos del modelo ya están guardados en `datos/procesados/`: para reestimar no hace falta descargar nada. Estos scripts reconstruyen esas series desde las fuentes primarias.

| Script | Qué construye | Sale a |
|---|---|---|
| `construir_dataset_1996_2025.py` | Panel trimestral 1996T1-2025T4 del modelo, a partir de la base ampliada anterior | `datos/dataset_consolidado_1996_2025.csv` |
| `empalme_embi_tcrm_1996_1998.py` | Empalmes del EMBI (1996T1-1998T3) y del TCRM (1996) con su validación | `datos/procesados/empalmes_1996_1998.csv`, `resultados/tablas/empalmes_validacion.csv` |
| `construir_resultado_primario_1996_2025.py` | Resultado primario del Sector Público Nacional, con y sin rentas de la propiedad | `datos/procesados/resultado_primario_1996_2025.csv` |
| `construir_pib_real_empalme_indec_1996_2003.py` | PIB real de 1996-2003 empalmado de la base 1993 a la base 2004 | `datos/procesados/pib_real_empalme_indec_1996_2003.csv` |
| `construir_deuda_consolidada_1996_2025.py`, `construir_deuda_consolidada_neta_1996_2025.py`, `construir_deuda_consolidada_neta_nominal_1996_2025.py` | Deuda federal bruta y deuda consolidada con el BCRA | `datos/procesados/deuda_*_1996_2025.csv` |
| `construir_tenencias_fgs.py` | Tenencias del sector público y del FGS | `datos/procesados/tenencias_fgs_1996_2025.csv` |
| `ingesta_tasa_fed_1996_2025.py` | Tasa de la FED trimestral, con la tasa sombra de Wu y Xia | `datos/procesados/tasa_fed_trimestral_1996_2025.csv` |
| `ingesta_instrumentos_1996_2025.py` | VIX trimestral | `datos/procesados/instrumentos_1996_2025.csv` |
| `extraer_escenario_base_fmi_cr26105.py` | Escenario base del FMI (Informe de País 26/105) | `datos/procesados/escenario_base_fmi_cr26105.csv` |

El resto de los scripts de esta carpeta (`ingesta_bcra*.py`, `ingesta_mecon_indec.py`, `construccion_dataset.py`, `construir_dataset_ampliado.py`, `empalme_historico_pre2004.py`, `empalme_pib_real_pre2004.py` y otros) construyen la base anterior de 2004-2025 y 1999-2025, de la que parte `construir_dataset_1996_2025.py`.
