# Datos — Guía de la Carpeta

Tres niveles, en orden de procesamiento: **crudos → procesados → consolidado**.

## 1. `crudos/` — descargas originales, sin tocar

- `ITCRMSerie.xlsx`: serie oficial del Tipo de Cambio Real Multilateral (BCRA), tal como se descarga.
- `descargas_drive/`: informes y papers de contexto usados como fuente secundaria (p. ej. auditoría AGN de la deuda con el FMI). No son datos tabulares, son documentos de respaldo.
- `no_referenciados/`: dos CSV de EMBI (`embicsv.csv`, `embi_real_ambito_1998_2026.csv`) que se descargaron en algún momento pero **ningún script del pipeline los usa hoy** — se conservan por si hacen falta, pero no son insumo activo. La serie de EMBI+ realmente usada es `embi_real_ambito_1999_2025.csv` (un nivel más arriba).

## 2. `procesados/` — series intermedias ya limpias, por fuente

Salida de `codigo/ingesta_datos/`, todavía no fusionadas en el panel final:
`bcra_trimestral.csv`, `bcra_pasivos_trimestral.csv`, `financiero_trimestral.csv`, `macro_trimestral.csv`, `spread_regional_trimestral.csv`.

## 3. Panel consolidado — el dataset que usan los modelos

Hay **dos** versiones, para dos ventanas muestrales distintas. No son la misma tabla con distinto nombre — cubren períodos diferentes:

| Archivo | Ventana | n | Uso |
|---|---|---|---|
| **`dataset_consolidado_real_ext.csv`** | 1999T1–2025T4 (ampliada por empalme histórico) | 108 | **Técnica de referencia actual** (VECM, rama `revision-var-vecm`) |
| `dataset_consolidado_real.csv` | 2004T1–2025T4 (ventana original) | 88 | DOLS y robustez sobre la ventana original |

Insumos del empalme histórico (usados solo por `codigo/modelos/fase16_vecm_dataset_ampliado.py` para construir la versión `_ext`):
- `empalme_pre2004_deuda_pb.csv` — deuda/PIB y resultado primario 1999–2003.
- `pib_real_empalme_1996_2003.csv` — PIB real 1996–2003.
- `tcrm_real_bcra_1997_2025.csv` — TCRM real, serie larga.

**Columnas** (ambos archivos comparten el núcleo): `Date`, `deuda_pib`, `pb_pib`, `PIB_real`, `TCRM`, `EMBI`, `VIX`, `CER`, `g_gap`. El archivo `dataset_consolidado_real.csv` además trae columnas de trabajo intermedias (`EMBI_BRASIL`, `pasivos_bcra_ars`, `pib_nominal_trim`, `pib_nominal_es_extrapolado`, `pasivos_bcra_pib`) usadas por scripts puntuales (IV-2SLS, deuda consolidada). El archivo `_ext.csv` agrega `es_interpolado` (marca qué observaciones del tramo 1999–2003 vienen de empalme vs. serie original).

Definiciones exactas de cada variable, unidad y fuente primaria: **[`codebook.md`](codebook.md)**.

## ¿Y el análisis que usa estos datos?

Ver **[`codigo/modelos/README.md`](../codigo/modelos/README.md)** — ahí está la tabla completa de qué script lee cuál de estos dos archivos y qué produce.
