# Números reales de la reestimación 1996-2025 (n=120, 30 años)

Fuente: `codigo/modelos/fase23_reestimacion_1996_2025.py`, salidas en
`resultados/tablas/fase23_*.csv`. Verificado con corrida de robustez sin
aproximación (`fase23b_*`, ventana real 1997-2025, n=116, sin los 4
trimestres de TCRM extrapolado): los resultados no cambian de forma
sustantiva, confirmado que la reversión de la FEVD no es un artefacto de
la aproximación.

**Esta ventana (1996-2025, n=120) reemplaza a la ventana ampliada anterior
(1999-2025, n=108) como técnica de referencia para VECM, SVAR restringido
y TVECM. La ventana original (2004-2025, n=88) sigue sosteniendo DOLS,
IV-2SLS, Hansen en niveles y Bai-Perron, sin cambios.**

## 1. Ventana y datos
- `datos/dataset_consolidado_1996_2025.csv`, 1996T1-2025T4, n=120.
- 32 trimestres empalmados (deuda/pb/PIB, 1996-2003, ya documentado).
- 4 trimestres de TCRM extrapolados por tendencia (1996, columna `es_interpolado_tcrm`), única excepción al criterio de no extrapolar.
- El resto de las series (deuda, pb, PIB, EMBI+) provienen de fuente primaria o del empalme ya documentado, sin cambios de método.

## 2. Estacionariedad (ADF/KPSS) — sin cambios sustantivos respecto de la ventana anterior, mismo orden de integración por variable.

## 3. Johansen (rango de cointegración)
- k_ar_diff seleccionado por BIC = 1 (AIC=5, FPE=5, HQIC=2, sin unanimidad, igual que antes).
- Traza: [45.18, 25.21, 10.10, 3.07]. Crítico 95%: [47.85, 29.80, 15.49, 3.84].
- **r=0: NO rechaza la ausencia de cointegración** (45.18 < 47.85).
- Verificación 1997-2025 (n=116, sin aproximación): Traza=[45.46, 24.74, 10.14, 3.25], mismo resultado, r=0.
- Se impone r=1 por motivo teórico (igual criterio que ya usaba la tesis), documentando que la ambigüedad es ahora más marcada que en la ventana 1999-2025 (que sí rechazaba r=0 en un caso, no en otro; acá no rechaza en ninguno de los dos puntos de inicio probados).

## 4. VECM final (k_ar_diff=1, coint_rank=1)
Beta (vector de cointegración, normalizado sobre deuda_pib=1):
- deuda_pib: 1.0
- pb_pib: 5.9653 (p=0.022, significativo)
- EMBI: -0.0150 (p<0.001, significativo)
- TCRM: 2.0466 (p=0.840, NO significativo)
- const: -45.3547 (p=0.007)

Alpha (velocidad de ajuste):
- deuda_pib: -0.0736 (p=0.004, significativo, signo correcto — corrige 7.4%/trimestre de la brecha)
- pb_pib: -0.000017 (p=0.996, NO significativo — sin reacción fiscal, igual lectura que antes)
- EMBI: 6.3560 (p=0.025, significativo — el riesgo soberano es el que ajusta)
- TCRM: -0.0003 (p=0.677, NO significativo)

Lectura: MISMA historia cualitativa que la ventana 1999-2025 (pb no reacciona, EMBI+ absorbe el ajuste, deuda corrige hacia el equilibrio). Los valores puntuales cambian pero no el signo ni la significatividad de ningún alpha. Esto SÍ se puede escribir como confirmación robusta.

## 5. SVAR restringido (matriz de impacto S, orden g_gap/pb_pib/EMBI/TCRM/deuda_pib)
```
             Shock_g_gap  Shock_pb_pib  Shock_EMBI  Shock_TCRM  Shock_deuda_pib
g_gap           4.6021       0.0000      0.0000      0.0000       0.0000
pb_pib          1.1505       1.2634      0.0000      0.0000       0.0000
EMBI         -150.4775    -181.0409    484.3715      0.0000       0.0000
TCRM            0.0200       0.0341      0.0040      0.1203       0.0000
deuda_pib       -2.6559      -2.8430      1.0438      1.7344       3.8114
```

## 6. FEVD de deuda_pib a 20 trimestres — CAMBIO CUALITATIVO IMPORTANTE
| Shock | Ventana vieja (2004-2025, n=88) | Ventana nueva (1996-2025, n=120) |
|---|---|---|
| g_gap (actividad) | 28.56% | 7.28% |
| pb_pib (fiscal) | 47.53% | 12.70% |
| EMBI (riesgo soberano) | 4.22% | 11.36% |
| TCRM (cambiario) | 7.26% | 14.44% |
| deuda_pib (inercia propia) | 12.43% | 54.21% |

**Se invierte la conclusión que tenía la tesis** ("la deuda se mueve por shocks fiscales y de actividad, no por el canal cambiario"): con 30 años, el canal cambiario+riesgo (25.8%) supera al fiscal+actividad (20.0%), y lo que más pesa por lejos es la inercia propia de la deuda (54.2% — antes 12.4%). Verificado en `fase23b` (ventana 1997-2025 sin aproximación): 53.15% inercia propia, 27.5% cambiario+riesgo, 19.4% fiscal+actividad — mismo patrón, no es artefacto de la extrapolación del TCRM de 1996.

Interpretación a incorporar en el texto (Resultados/Discusión): con una ventana que incorpora la salida de la hiperinflación, el Tequila 1995 y la Convertibilidad completa además de su colapso, el sistema muestra mucha menos capacidad de auto-corrección de la deuda vía los canales fiscal/real, y mucho más peso de la inercia propia y del canal cambiario-riesgo. Es coherente con el hallazgo de Johansen (§3): menos evidencia de cointegración estable es consistente con más inercia propia dominando la dinámica.

## 7. TVECM (Hansen-Seo)
- tau* = 2104.22 pb (antes: 2081 pb en la ventana 2004-2025 — prácticamente el mismo umbral)
- Sup-LM = 59.779, p-valor bootstrap = 0.632 (antes: p=0.625 — sigue sin ser significativo, mismo resultado cualitativo)
- alpha_pb régimen 1 (normal): +0.0011 (antes +0.006)
- alpha_pb régimen 2 (estrés): -0.0074 (antes -0.008)
- n régimen 1 = 96, régimen 2 = 22 (n_total=118, se pierden 2 obs por rezagos)

Lectura: el patrón de reversión de signo (normal positivo, estrés negativo) se REPLICA con valores muy similares. El umbral estimado (~2100 pb) es notablemente estable entre ventanas. Sigue sin alcanzar significatividad formal (Sup-LM).

## 8. DSA estocástico (Monte Carlo, covarianza SVAR-fundada, Etapa 6 simplificada)
- P(d_2035 > 100% PIB) = **26.1%** (con el S matrix de esta ventana; el número anterior con el SVAR de 2004-2025 había dado 24.8%; el numero CIR/DCC-GARCH viejo, con la matriz calibrada a mano, era 31.2%/32.5%/29.8%).
- Mediana 2035 (determinista, escenario Referencia): 82.84% PIB.
- Percentiles estocásticos guardados en `resultados/tablas/fase6_dsa_percentiles_estocastico.csv` (ya sobreescrito con la corrida nueva).

## 9. Archivos ya actualizados como canónicos (sobreescritos)
- `resultados/tablas/fase19_svar_matriz_impacto_S.csv` ← ahora es el de la ventana 1996-2025 (antes era 2004-2025).
- `resultados/tablas/fase19_fevd.csv` ← ídem.
- `resultados/tablas/fase6_dsa_percentiles_estocastico.csv`, `fase6_dsa_probabilidad.csv` ← recalculados con la covarianza nueva.
- Los archivos `fase23_*` y `fase23b_*` quedan como evidencia/trazabilidad de esta reestimación, no se borran.
- Los archivos `fase20_cir_*` (CIR) y `fase10_dcc_garch*` / resultados de DCC-GARCH en 06/07 NO se tocan: quedan como especificación alternativa, pendiente de mostrarle al profesor.

## 9b. Ya escrito en 04_metodologia.tex, 05_datos.tex, 06_resultados.tex, 00_abstract.tex (NO tocar de nuevo)
Estos cuatro archivos YA fueron actualizados con todos los números de este dossier: ventana, tablas de sensibilidad de Johansen (rezagos y punto de inicio, incluida la nueva fila 1996T1-1998T1), tabla beta/alpha del VECM, tabla FEVD del SVAR (con el párrafo de la reversión), tabla del TVECM, tabla de descriptivos y de estacionariedad de la ventana ampliada (incluido el hallazgo de que deuda/PIB ahora lee más cerca de I(0) que de I(1) con ADF y KPSS), la nueva sección de DSA con covarianza del SVAR (26.1%) y el CIR/DCC-GARCH re-etiquetado como "especificación alternativa, pendiente de revisión del director". NO reabrir estos archivos para lo mismo, solo referenciarlos.

## 9c. Datos adicionales para 07/08/09 (sensibilidad de rezagos VECM, ventana 1996-2025)
Tabla de sensibilidad a rezagos (ya en 06_resultados.tex, tabla tab:vecm_sensibilidad_lags), para referencia:
| k_ar_diff | beta_deuda (norm. s/pb) | alpha_pb | p-valor |
|---|---|---|---|
| 1 (BIC) | 0.1677 | -0.00002 | 0.996 |
| 2 | 0.0614 | -0.0047 | 0.022* |
| 3 | 0.0949 | -0.0034 | 0.288 |
| 4 | 0.0870 | -0.0019 | 0.460 |
| 5 (AIC,FPE) | 0.1025 | +0.0019 | 0.558 |

A diferencia de la ventana de 108 obs (donde el signo de beta_deuda era inestable, cambiaba de signo entre especificaciones), acá el signo es estable (siempre positivo) en las cinco especificaciones. El único alpha_pb significativo (k=2, p=0.022) tiene signo negativo, económicamente perverso (implica que pb se aleja del equilibrio), y no lo acompaña ninguna otra especificación — mismo patrón de "hallazgo aislado" que ya usaba el texto viejo, pero ahora con esta apoyatura numérica distinta (antes era el que casi llegaba a significativo con signo positivo, ahora es el que sí llega pero con signo negativo).

## 10. Qué NO cambia
- DOLS (ventana original 88 obs): sin cambios, sigue siendo rho=-0.0071, p=0.564.
- IV-2SLS: sin cambios.
- Hansen en niveles (ventana original): sin cambios.
- Hansen en Δpb (ventana original): sin cambios, sigue siendo el resultado significativo p<0.001.
- Bai-Perron (ventana original): sin cambios.
- CIR/DCC-GARCH (especificación vieja de Etapa 6): sin cambios, quedan documentados aparte.
