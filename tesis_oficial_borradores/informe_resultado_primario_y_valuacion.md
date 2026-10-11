# Informe: resultado primario desde fuente primaria, PIB real pre-2004 y valuación nominal de la deuda neta

Fecha de construcción: 2026-10-11. Todos los números provienen de los CSV generados por los scripts listados al final; ningún valor está tipeado en el código (las cifras del FMI se leen del PDF local por regex).

## 1. Resultado primario del SPN, 1996T1-2025T4

### 1.1 Fuente

Secretaría de Hacienda, Ministerio de Economía, Subsecretaría de Programación Macroeconómica, "Esquema Ahorro-Inversión-Financiamiento. Sector Público Nacional. Base Caja" (datos.gob.ar, API de series, dataset 379). Frecuencia **mensual desde 1993**, en tres tramos metodológicos (millones de ARS corrientes):

| Tramo | Con rentas ("Superávit primario") | Sin rentas | Rentas de la propiedad |
|---|---|---|---|
| Metodología 1993-2006 | 379.7_SUPERAVIT_006__28_65 | 379.7_RESULTADO_006__36_94 | 379.7_ING_CORR_R006__42_86 |
| Metodología 2007-2014 | 379.8_SUPERAVIT_014__28_7 | 379.8_RESULTADO_014__36_23 | 379.8_ING_CORR_R014__42_59 |
| Metodología 2017 (2015-) | 379.9_SUPERAVIT_017__23_94 | 379.9_RESULTADO_017__31_73 | 379.9_ING_CORR_R017_I_0_M_37_10 |

Crudos guardados en `datos/crudos/resultado_primario/`. Como hay datos mensuales desde 1993, **ya no hace falta la desagregación de Denton 1996-2003**: todo el período es dato primario trimestralizado por suma de meses (se exige que estén los 3 meses; no hay trimestres faltantes).

Verificaciones: (i) con rentas − sin rentas = rentas de la propiedad, exacto en 1993-2014; en el tramo 2017 la diferencia máxima mensual es de 3 393 millones de ARS (≈0,0004% del PIB, atribuible a que ese tramo publica rentas "netas"). (ii) La serie publicada "sin rentas" del tramo 1993-2006 tiene 62 meses vacíos; en esos meses se deriva por identidad (con − rentas) y queda marcado en el código. (iii) El control cruzado contra IMIG (452.3_RESULTADO_RIO_0_M_18_54, 2016+) da diferencia 0,000: IMIG y AIF son la misma compilación, de modo que **no es un control independiente**.

### 1.2 Medida de flujo (decisión)

Denominador: PIB nominal de los últimos 4 trimestres (`pib_4t_mm`, igual a la suma de los 4 flujos trimestrales de INDEC).

- **Serie principal `pb_pib`** = 100 × suma móvil de 4 trimestres del resultado primario / `pib_4t_mm`. Razones: (a) el resultado primario del SPN es fuertemente estacional (aguinaldo, Ganancias en T2); (b) es el numerador homólogo del denominador 4T de la razón deuda/PIB, con lo cual es consistente con la identidad de acumulación de deuda; (c) coincide con la definición anual del FMI en los T4. Costo: es una media móvil MA(3) de flujos trimestrales y genera autocorrelación inducida (autocorr. de orden 1 = 0,965).
- **Alternativa `pb_pib_trim`** = 100 × 4 × PB del trimestre / `pib_4t_mm` (sin superposición, autocorr. de orden 1 = 0,649, pero con estacionalidad, autocorr. de orden 4 = 0,629). Se entrega como robustez para el SVARX; si se usa en el VAR conviene incluir dummies estacionales.

### 1.3 Rentas del BCRA

Las "rentas de la propiedad" de la fuente agregan **todas** las rentas del SPN (utilidades del BCRA, rentas del FGS-ANSES, intereses cobrados por organismos). **La API pública no desglosa la transferencia de utilidades del BCRA**, de modo que no puedo ofrecer la serie "excluyendo solo BCRA". Se entregan: `pb_pib` (con todas las rentas, definición de titular de MECON) y `pb_pib_sin_rentas` (excluye todas las rentas; cota conservadora, excluye más que el FMI). El FMI (CR 25/95, Tabla 3b, nota 9) informa transferencias BCRA de 0,9% del PIB en 2023 y 0,0% en 2024; con eso se arma el contraste "con rentas menos transferencia BCRA del FMI" (no es una serie, es un control de dos puntos).

Rentas totales (con − sin) en % PIB: 0,3 a 0,7 en 1996-2008, 1,3 a 2,6 en 2009-2014 (pico 2,64 en 2014), 0,3 a 1,3 en 2015-2025.

### 1.4 Comparación contra la serie anterior y el FMI

Serie anterior = diccionario `PB_PIB_TRIM` (2004-2025) y Denton anual (1996-2003).

| Período | Correlación nueva-vieja | Error absoluto medio | Máx. |dif| |
|---|---|---|---|
| 1996-2003 | 0,33 | 1,16 pp | 3,13 pp |
| 2004-2025 | 0,89 | 1,29 pp | 3,72 pp |

Control FMI, cierres de diciembre (% PIB):

| Año | Nueva con rentas | Nueva sin rentas | Nueva con rentas − transf. BCRA (FMI) | Serie anterior | FMI, gobierno federal |
|---|---|---|---|---|---|
| 2023 | -2,66 | -3,67 | -3,56 | -2,90 | -2,8 |
| 2024 | 1,78 | 1,01 | 1,78 | 1,40 | 1,8 |

Lectura: la serie nueva con rentas replica casi exacto el número del FMI en 2023 (-2,66 vs -2,8) y 2024 (1,78 vs 1,8). Cuidado con la interpretación: el FMI excluye las transferencias del BCRA y cubre solo el gobierno federal, mientras que esta serie es SPN con todas las rentas; la coincidencia puede ser parcialmente casual (en 2023 restando las transferencias BCRA del FMI daría -3,56). Hay que explicar en la tesis que el aggregate no es el del FMI.

Valores de cierre anual `pb_pib` (con rentas, % PIB): 1996 -0,31; 1999 1,12; 2001 0,50; 2003 2,13; 2004 3,58; 2007 2,87; 2010 1,51; 2013 -0,67; 2015 -3,77; 2017 -3,79; 2019 -0,44; 2020 -6,43; 2022 -2,00; 2023 -2,66; 2024 1,78; 2025 1,38.

### 1.5 Puntos abiertos

1. Dos empalmes metodológicos (2006/2007 y 2014/2015) sin período de solapamiento en la API; se reportan las filas de empalme (2006T4 3,24 y 2007T1 3,12; 2014T4 -0,84 y 2015T1 -1,63) y no se detecta salto anómalo, pero no hay prueba formal. Columna `metodologia` en el CSV para dummy de quiebre.
2. En 1993-2006 las privatizaciones no figuran en el primario; en 2007-2014 se usa la serie "con privatizaciones" (28_7) y no la "sin privatizaciones" (48_10, que termina en 2013-11); la diferencia es chica pero no medida aquí.
3. Perímetro: SPN consolidado (Administración Nacional, organismos descentralizados, instituciones de seguridad social, fondos fiduciarios y empresas), no "gobierno federal" del FMI.
4. Desglose BCRA de las rentas: no disponible en API; habría que ir al Cuadro AIF de Hacienda o al balance del BCRA (utilidades transferidas).

## 2. PIB real 1996-2003

Fuente: INDEC, "Oferta y Demanda Globales", datos.gob.ar: 2.2_OGP_1993_T_17 (millones de $ de 1993, 1993T1-2013T3) y 4.2_OGP_2004_T_17 (millones de $ de 2004). Empalme por coeficiente de enlace k = media de 2004T1-T4 de Y04/Y93 = 1,75099 (mismo criterio que el PIB nominal). `PIB_real` del dataset es proporcional a 4.2_OGP_2004_T_17 (constante c = 2,0614e-4, dispersión nula), por lo que la serie nueva queda en la misma unidad. Salida: `datos/procesados/pib_real_empalme_indec_1996_2003.csv`. Los coeficientes Y04/Y93 varían entre 1,46 y 1,85 en el solapamiento 2004-2013 (distintas ponderaciones de precios), por lo que el nivel pre-2004 depende de elegir 2004 como año de enlace; las tasas de crecimiento pre-2004 no dependen de esa elección.

Discrepancia contra la versión anterior (tasas anuales tipeadas + Denton):

- Nivel trimestral: máxima 9,79% (2002T1), media 3,50%. Se debe a que la versión anterior es suavizada y sin estacionalidad, mientras que la nueva conserva la estacionalidad de INDEC.
- Promedios anuales: diferencia entre -0,59% y -0,88% en todos los años (nivel inicial distinto).
- Crecimiento anual (nuevo vs anterior, %): 1997 8,11/8,1; 1998 3,85/3,8; 1999 -3,39/-3,4; 2000 -0,79/-0,5; 2001 -4,41/-4,5; 2002 -10,89/-10,9; 2003 8,84/8,8. Las tasas tipeadas eran correctas salvo 2000 (-0,5 vs -0,79, diferencia 0,29 pp).
- Salto de empalme 2003T4→2004T1: nuevo -2,10% (efecto estacional T4→T1), anterior +0,5% por construcción de Denton.

Consecuencia: si el output gap y el VAR usan `PIB_real`, el filtro HP del tramo pre-2004 queda con componente estacional; se debe desestacionalizar o usar crecimiento interanual. No se sustituyó `dataset_consolidado_real.csv` (regla de no sobrescribir).

## 3. Deuda consolidada neta con letras intransferibles a valor nominal

### 3.1 Datos

Fuente: Ministerio de Economía, Secretaría de Finanzas, "Estado de la Deuda Pública", planillas `datos/crudos/mecon_deuda/` (hoja A.1.9, A.1.10 o A.1.11 según año; bloque "LETRAS ADQUIRIDAS POR EL BCRA", en miles de USD; 2007-2010: filas "LETRA INTRANSFERIBLE" de A.12.3). El script suma instrumento por instrumento y reproduce los totales del bloque (2024: 69 286 millones de USD; 2013: 42 907). Valor nominal original = residual = actualizado en todas las planillas. Resumen por ancla en `datos/procesados/letras_intransferibles_bcra_nominal_anclas.csv`.

Cobertura: planillas de cierre de año 2007, 2008, 2009, 2013-2025 y marzo de 2010; **no hay planillas 2010-12, 2011-12 ni 2012-12**. Las letras empiezan el 2006-01-03 (primera emisión), de modo que ≤ 2005T4 no hay dato nominal y se conserva el valor contable.

Trimestres no cubiertos por una ancla: `reconstruccion_emisiones` (32 trimestres; las letras son bullet, si todo instrumento de la ancla anterior sigue igual en la siguiente, el stock se arma con la fecha de emisión publicada), `interpolacion_lineal` (24 trimestres; hubo canjes o cambios de monto), `reconstruccion_emisiones_hacia_atras` (7; 2006T1-2007T3), `ancla_oficial` (17), `sin_dato` (40; hasta 2005T4). La columna `nominal_metodo` y `flag_nominal_interpolado` lo registran. La interpolación es una aproximación explícita, no un dato.

### 3.2 Construcción y alerta de valuación

T^BCRA_nom = T^BCRA_libros − L^ME_libros + N × TC, con N el stock nominal en USD y TC el del dataset de deuda. Se calculan dos variantes:

- `deuda_consolidada_neta_nominal_pib` (sustitución estricta del componente ME del balance por el nominal).
- `deuda_consolidada_neta_nominal_piso_pib` (nunca baja la tenencia por debajo del libro: solo suma el faltante donde N × TC supera el componente ME del balance).

Hallazgo: el componente ME del balance (BCRA, balbcrhis.xls) **no es igual a las letras**. En USD: libros vs nominal fue 9,9 vs 9,5 (2006), 46,0 vs 42,9 (2013), 64,4 vs 48,4 (2015), 66,9 vs 48,7 (2017), 42,3 vs 48,7 (2018), 89,2 vs 67,2 (2023), 28,6 vs 69,3 (2024), 32,3 vs 52,5 (2025). Hasta 2017 y 2019-2023 el libro es mayor que el nominal (probablemente intereses devengados y otras tenencias en ME que la sustitución estricta elimina, no pude identificar el contenido exacto de la columna ME); desde 2018 y en 2024-2025 el libro es menor (el BCRA valúa las letras por debajo del nominal). **Los 28,6 de libros vs 69,3 nominal en 2024 se confirman.** La sustitución estricta empeora 2023 (128,2 vs 119,0) porque el libro de 2023 supera al nominal; por eso se agrega la variante piso. Recomendación: usar la variante `piso` para la tesis hasta aclarar el contenido de la columna ME (o abrir las notas a los estados contables del BCRA).

### 3.3 Resultados y control FMI (% PIB 4T)

| Concepto | 2023 | 2024 |
|---|---|---|
| Deuda bruta federal (nuestra) | 153,53 | 82,09 |
| Deuda bruta (FMI) | 155,4 | 85,3 |
| Tenencia BCRA, libros | 48,57 | 13,24 |
| Tenencia BCRA, nominal estricta | 39,38 | 20,44 |
| Intra-público total, FMI (incluye FGS y otros) | 62,5 | 33,9 |
| Neta ex FGS, libros | 119,03 | 68,31 |
| Neta ex FGS, nominal estricta | 128,21 | 61,11 |
| Neta ex FGS, nominal piso | 119,03 | 61,11 |
| Neta FMI | 110,8 | 51,5 |

2024: la valuación nominal baja 7,2 pp (68,3 → 61,1) y cierra parte de la brecha con el FMI (queda 9,6 pp). 2023: sin mejora (la brecha de 8,2 pp con el FMI no se cierra con esta corrección). La brecha restante se explica por el FGS (sin fuente primaria accesible, `flag_fgs_faltante = 1`), otras tenencias intra-públicas, la bruta del FMI mayor que la nuestra (2024: 85,3 vs 82,1) y el swap PBoC. Cierres de año de la neta (libros / nominal estricta / piso): 2015 34,2 / 37,7 / 34,2; 2018 71,2 / 69,5 / 69,5; 2020 89,5 / 91,2 / 89,5; 2023 119,0 / 128,2 / 119,0; 2024 68,3 / 61,1 / 61,1; 2025 64,5 / 61,0 / 61,0.

### 3.4 Puntos abiertos

1. Contenido exacto de la columna ME del balance del BCRA (explica el ratio libros/nominal ≠ 1).
2. Planillas 2010-12, 2011-12, 2012-12 y trimestrales (para evitar interpolar); se pueden pedir a Secretaría de Finanzas.
3. 24 trimestres son interpolación lineal (marcados).
4. FGS-ANSES sigue faltando; la serie sigue siendo "neta excepto FGS".
5. TC de cierre de trimestre del dataset de deuda: si difiere del TC usado por el BCRA en su balance, el ratio libros/nominal tiene ruido de conversión.

## 4. Archivos

- Scripts: `codigo/ingesta_datos/construir_resultado_primario_1996_2025.py`, `codigo/ingesta_datos/construir_pib_real_empalme_indec_1996_2003.py`, `codigo/ingesta_datos/construir_deuda_consolidada_neta_nominal_1996_2025.py`.
- Datos: `datos/procesados/resultado_primario_1996_2025.csv`, `datos/procesados/resultado_primario_1996_2025_control.csv`, `datos/procesados/pib_real_empalme_indec_1996_2003.csv`, `datos/procesados/deuda_consolidada_neta_nominal_1996_2025.csv`, `datos/procesados/deuda_consolidada_neta_nominal_1996_2025_control_fmi.csv`, `datos/procesados/letras_intransferibles_bcra_nominal_anclas.csv`.
- Crudos nuevos: `datos/crudos/resultado_primario/*.csv`.
- No se hicieron tests pytest ni se ejecutó `tools/pre_commit_guard.py`; no se hizo commit. No se tocaron los datasets existentes.
