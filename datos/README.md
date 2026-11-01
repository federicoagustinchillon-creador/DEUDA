# Datos

Tres niveles, en orden de procesamiento: `crudos/` (descargas originales, sin tocar), `procesados/` (series limpias por fuente) y el panel consolidado que usa el modelo.

El panel del modelo es [`dataset_consolidado_1996_2025.csv`](dataset_consolidado_1996_2025.csv): 120 trimestres, 1996T1-2025T4. Las columnas `EMBI_fuente` y `TCRM_fuente` indican el origen de cada trimestre, y `es_interpolado`, `es_empalme_pib`, `es_empalme_embi` y `es_interpolado_tcrm` marcan los valores reconstruidos. Las ecuaciones se estiman con 1998T2-2025T4 porque la deuda trimestral del MECON empieza en 1998T1.

Además del panel, el modelo lee en `procesados/` el resultado primario, la tasa de la FED, el VIX, el PIB real empalmado, las series de deuda federal bruta y consolidada, los empalmes del EMBI y del TCRM y el escenario base del FMI (Informe de País 26/105). Los scripts que las construyen están en [`codigo/ingesta_datos/`](../codigo/ingesta_datos/README.md).

Los paneles `dataset_consolidado_real.csv` (2004-2025) y `dataset_consolidado_real_ext.csv` (1999-2025) son de la etapa anterior y sirven de insumo para construir el panel de 1996-2025. Los CSV de `crudos/no_referenciados/` se descargaron en algún momento y ningún script los usa hoy.

Definiciones, unidades y fuentes de cada variable: [`codebook.md`](codebook.md).
