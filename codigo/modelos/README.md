# Mapa del Análisis Estadístico — Orden de Ejecución

Este archivo es el índice único y ordenado de **todo** el análisis econométrico de la tesis. Cada fila es un script que corre, en este orden, sobre el panel de datos (ver [`datos/README.md`](../../datos/README.md)) y produce una salida verificable en [`resultados/tablas/`](../../resultados/tablas/) que después se cita en un capítulo puntual de la tesis.

Si querés entender "cómo se llegó a tal número de la tesis", este es el punto de partida: buscá la fase, corré el script (o mirá el CSV que ya generó), y andá al capítulo indicado.

> La fuente autoritativa de esta tabla es el Apéndice de la tesis (`tesis/capitulos/09_apendice.tex`, sección "Estructura de la Cadena de Procesamiento de Código", Tabla `tab:pipeline_estructura`). Este README es una copia de lectura rápida — ante cualquier discrepancia, el Apéndice manda.

## Ventana ampliada (1999–2025, n=108) — técnica de referencia actual (rama `revision-var-vecm`)

| Fase | Script | Qué hace | Dónde queda el resultado (capítulo de la tesis) |
|---|---|---|---|
| 2.16 | `fase16_vecm_dataset_ampliado.py` | Empalme histórico 1999–2003, tests de estacionariedad, selección de rezagos del VAR, sensibilidad de Johansen al inicio muestral, estimación VECM final | `resultados/tablas/fase16_*.csv` → Cap. 6, §6.2 (`sec:resultados_vecm`) |
| 2.17 | `../ingesta_datos/actualizar_tcrm_embi_real.py` | Reemplaza series de contingencia (TCRM, EMBI+) por series primarias reales en el panel | actualiza `datos/dataset_consolidado_real.csv` |
| 2.18 | `fase17_calibracion_nu_dsa.py` | Recalibra los grados de libertad $\nu$ de la $t$-Student del DSA por método de momentos, sobre shocks reales | $\nu\approx4.8$ → Cap. 7, §"Aporte Metodológico" |
| 2.19 | `fase18_dummies_presidenciales.py` | Robustez de $\alpha_{pb}$ (velocidad de ajuste del VECM) por administración presidencial, interactuando con el término de corrección de error (`ect`) | `resultados/tablas/fase18_dummies_vecm_ect.csv` → Cap. 6, §6.2.3 (`sec:dummies_presidenciales`) |
| — | `fase3b_reaccion_fiscal_vecm.py` | Verificación complementaria: mismo VECM pero sobre la ventana **original** (2004–2025, n=87) con series reales, para chequear que el hallazgo no depende de la ventana ampliada | `resultados/tablas/fase3b_vecm_*` → Cap. 6, subsección "Verificación Complementaria" |

## Ventana original (2004–2025, n=88) — pipeline base, se conserva como robustez

| Fase | Script | Qué hace | Dónde queda el resultado (capítulo de la tesis) |
|---|---|---|---|
| 2.1 | `fase1_estacionariedad.py` | Raíz unitaria: ADF, KPSS, PP, DF-GLS, Zivot-Andrews | Cap. 6, Tabla `tab:estacionariedad`, Tabla `tab:dfgls` |
| 2.2 | `fase2_cointegracion.py` | Cointegración de Johansen (Traza y Máximo Autovalor) | Cap. 6, §Johansen (`sec:johansen_cap6`) |
| 2.3 | `fase3_reaccion_fiscal.py` | DOLS (Mínimos Cuadrados Ordinarios Dinámicos) + diagnósticos de especificación | Cap. 6, Tabla `tab:dols` |
| 2.4 | `fase4_variables_instrumentales.py` | IV-2SLS (instrumentos: VIX + spread regional Brasil), F de primera etapa, Wu-Hausman, Sargan | Cap. 6, Tabla `tab:iv2sls` |
| 2.5 | `fase5_umbral_hansen.py` | Umbral de Hansen (fatiga fiscal), bootstrap Sup-LM | Cap. 6, Tabla `tab:hansen` |
| 2.6 | `fase6_sostenibilidad_deuda.py` | DSA determinista y Monte Carlo ($t$-Student) | Cap. 6, Tabla `tab:dsa_determinista`, Figura `fig:fan_chart_final` |
| 2.7 | `fase7_diagnosticos_robustez.py` | ACF/PACF, ARCH-LM, CUSUM/CUSUMSQ, Engle-Granger, sensibilidad temporal, causalidad de Granger, filtro de Hamilton, covarianza GARCH(1,1) | Cap. 6, Figuras `fig:acf_pacf`/`fig:cusum`, varias tablas |
| 2.8 | `fase8_deuda_consolidada.py` | Consolida deuda SPNF + pasivos remunerados del BCRA (LELIQ/NOTALIQ/Pases) | Cap. 6, Figura `fig:deuda_consolidada` |
| 2.9 | `bai_perron.py` + `fase9_bai_perron.py` | Quiebres estructurales múltiples (Bai & Perron 2003, DP + BIC) | Cap. 6, Figura `fig:bai_perron` |
| 2.10 | `dcc_garch.py` + `fase10_dcc_garch.py` | [[dcc-garch-dynamic-correlation|DCC-GARCH]]: correlación condicional dinámica entre shocks del DSA | Cap. 6, §[[dcc-garch-dynamic-correlation|DCC-GARCH]] |
| 2.11 | `fase11_dols_subperiodos.py` | DOLS por subperíodo (Kirchnerismo/Macri-AF) frente a MCO estático | Cap. 6, Tabla `tab:sensibilidad_temporal` |
| 2.12 | `fase12_diagnosticos_complementarios.py` | Orden de rezagos del VAR (AIC/BIC/HQ/FPE), sensibilidad del rango de Johansen, VIF, número de condición | Cap. 6, Tablas `tab:rezagos_var`, `tab:vif` |
| 2.13 | `fase13_robustez_hansen_dpb.py` | Robustez del umbral de Hansen usando $\Delta pb_t$ (I(0)) como dependiente | Cap. 6, Tabla `tab:hansen_dpb` |
| 2.14 | `fase14_dsa_tail_dependence.py` | Robustez del DSA a la estructura de dependencia en colas (cópula Gaussiana vs. $t$ independientes) | Cap. 6, Tabla `tab:tail_dependence_robustez` |
| 2.15 | `fase15_sft_decomposicion_ilustrativa.py` | Descomposición ilustrativa del Ajuste Stock-Flujo ($SF_t$), episodios 2005/2018/2020 | Cap. 6, Tabla `tab:sft_ilustrativo` |

## Cómo correr todo de una vez

```bash
python codigo/codigo_completo_deuda.py
```

Ese script concatena y ejecuta en orden las Etapas 1.1 a 3.2 completas (ingesta + todas las fases + gráficos). Para correr solo una fase puntual, ejecutá el `.py` individual — todos leen `datos/dataset_consolidado_real.csv` o `datos/dataset_consolidado_real_ext.csv` y escriben su salida en `resultados/tablas/`.

## Gráficos (Etapa 3)

| Script | Qué genera |
|---|---|
| `../graficos/generacion_graficos_tesis.py` | Figuras 5.1, 5.3, 5.4 y 6.1 de la tesis |
| `../graficos/generacion_cronologia_quiebres.py` | Cronología visual de quiebres estructurales |
