# Datos

Tres niveles, en orden de procesamiento: `crudos/` (descargas originales, sin tocar), `procesados/` (series limpias por fuente) y el panel consolidado que usa el modelo.

El panel [`dataset_consolidado_1996_2025.csv`](dataset_consolidado_1996_2025.csv) tiene 120 trimestres, 1996T1-2025T4, y reúne las series que no tienen archivo propio en `procesados/`: el EMBI, el TCRM y el PIB real. Las columnas `EMBI_fuente` y `TCRM_fuente` indican el origen de cada trimestre, y `es_interpolado`, `es_empalme_pib`, `es_empalme_embi` y `es_interpolado_tcrm` marcan los valores reconstruidos. El modelo toma del panel el EMBI, el TCRM y el PIB real posterior a 2003; el PIB real de 1996-2003 sale del empalme del INDEC en `procesados/`.

El resto de las series las lee el modelo de `procesados/`: el resultado primario, la tasa de la FED, el VIX, las series de deuda federal bruta y consolidada, los empalmes del EMBI y del TCRM y el escenario base del FMI (Informe de País 26/105). Las ecuaciones se estiman con 1998T2-2025T4 porque la deuda trimestral del MECON empieza en 1998T1. Los scripts que construyen cada archivo están en [`codigo/ingesta_datos/`](../codigo/ingesta_datos/README.md).

Los paneles `dataset_consolidado_real.csv` (2004-2025) y `dataset_consolidado_real_ext.csv` (1999-2025) son de la etapa anterior y sirven de insumo para construir el panel de 1996-2025. Los CSV de `crudos/no_referenciados/` se descargaron en algún momento y ningún script los usa hoy.

Definiciones, unidades y fuentes de cada variable: [`codebook.md`](codebook.md).
