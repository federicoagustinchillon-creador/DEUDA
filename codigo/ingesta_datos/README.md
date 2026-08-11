# Ingesta de Datos — Orden de Ejecución

Scripts que descargan y arman las series primarias. Se corren antes que cualquier fase de `codigo/modelos/`.

## Descarga por fuente (paso 1)

| Script | Qué descarga | Sale a |
|---|---|---|
| `ingesta_bcra.py` | Series monetarias/cambiarias del BCRA (API v4.0) | `datos/procesados/bcra_trimestral.csv` |
| `ingesta_bcra_pasivos.py` | Pasivos remunerados del BCRA (LELIQ, NOTALIQ, Pases) | `datos/procesados/bcra_pasivos_trimestral.csv` |
| `ingesta_mecon_indec.py` | PIB, resultado primario, deuda (MECON/INDEC vía `datos.gob.ar`) | `datos/procesados/macro_trimestral.csv` |
| `ingesta_datos_financieros.py` | VIX, EMBI+ (Yahoo Finance, Ámbito Financiero) | `datos/procesados/financiero_trimestral.csv` |
| `ingesta_spread_regional.py` | Spread soberano ETF EMB Brasil (instrumento IV-2SLS) | `datos/procesados/spread_regional_trimestral.csv` |

## Empalme histórico para la ventana ampliada (paso 2, opcional — solo si se reconstruye `_ext.csv`)

| Script | Qué hace |
|---|---|
| `empalme_historico_pre2004.py` | Empalma deuda/PIB y resultado primario 1999–2003 → `datos/empalme_pre2004_deuda_pb.csv` |
| `empalme_pib_real_pre2004.py` | Empalma PIB real 1996–2003 → `datos/pib_real_empalme_1996_2003.csv` |

## Fusión en panel final (paso 3)

| Script | Qué hace | Sale a |
|---|---|---|
| `construccion_dataset.py` | Orquesta paso 1, fusiona y valida → panel ventana original | `datos/dataset_consolidado_real.csv` (n=88) |
| `construir_dataset_ampliado.py` | Fusiona paso 1 + paso 2 → panel ventana ampliada | `datos/dataset_consolidado_real_ext.csv` (n=108) |
| `actualizar_tcrm_embi_real.py` | Reemplaza series de contingencia por series primarias reales una vez descargadas | actualiza `datos/dataset_consolidado_real.csv` |

Detalle de columnas y fuentes: ver [`datos/README.md`](../../datos/README.md) y [`datos/codebook.md`](../../datos/codebook.md).
