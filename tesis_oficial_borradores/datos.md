# 5. Datos

Este capítulo documenta cada serie del modelo: qué mide, de dónde sale, qué transformaciones se le aplicaron y por qué. La muestra es trimestral, 1996T1-2025T4 (120 observaciones). Todas las cifras que aparecen aquí se recalcularon desde los archivos del repositorio citados en cada sección. Cuando una serie tiene una limitación, se declara junto con la dirección probable de su sesgo.

## 5.1 Resumen de las series

| Variable del modelo | Rol (Capítulo 4) | Archivo | Fuente primaria | Cobertura real |
|---|---|---|---|---|
| Deuda consolidada neta (% PIB) | Rezagada en las ecuaciones | `datos/procesados/deuda_consolidada_neta_1996_2025.csv` | MECON y BCRA | 1996T1-2025T4, sin FGS |
| Deuda federal bruta (% PIB) | Componente y serie de robustez | `datos/procesados/deuda_consolidada_1996_2025.csv`, `..._neta_...csv` | MECON, Informe de Deuda 31/12/2025 | 1996T1-2025T4 (6 trimestres interpolados) |
| Pasivos remunerados del BCRA | Componente | `deuda_consolidada_neta_1996_2025.csv` | API BCRA v4.0 | 1996T1-2025T4 (sin swap del PBoC) |
| Deuda del Tesoro en poder del BCRA | Componente | `deuda_consolidada_neta_1996_2025.csv` | BCRA, Balance histórico | 1996T1-2025T4 |
| Depósitos del Tesoro en el BCRA | Componente | `deuda_consolidada_neta_1996_2025.csv` | API BCRA v4.0, id 1264 | 1996T1-2025T4 |
| Resultado primario (% PIB) | Endógena | `datos/dataset_consolidado_1996_2025.csv` | MECON | 1996-2003 empalmado; 2004-2025 ver 5.7 |
| PIB real y crecimiento | Endógena | `datos/dataset_consolidado_1996_2025.csv` | INDEC | 1996-2003 empalmado; 2004-2025 directo |
| EMBI+ | Endógena | `datos/dataset_consolidado_1996_2025.csv` | JP Morgan vía Ámbito; spread Brady | 1996T1-2025T4 |
| TCRM | Endógena | `datos/dataset_consolidado_1996_2025.csv` | BCRA, `ITCRMSerie.xlsx` | 1997T1-2025T4; 1996 retropolado |
| Tasa de la Fed (con tasa sombra) | Exógena | `datos/procesados/tasa_fed_trimestral_1996_2025.csv` | FRED y Atlanta Fed | 1996T1-2025T4 |
| VIX | Exógena | `datos/procesados/instrumentos_1996_2025.csv` | Yahoo Finance, ^VIX | 1996T1-2025T4 |
| PIB nominal de cuatro trimestres | Denominador | `deuda_consolidada_1996_2025.csv` (`pib_4t_mm`) | INDEC | 1996T1-2025T4 (32 trimestres empalmados) |

Un cambio metodológico respecto de versiones anteriores: la deuda ya no sale de un diccionario escrito a mano. Se calcula como cociente entre stocks en pesos tomados de los informes de deuda del MECON y el PIB nominal. Esa construcción es trazable a archivos y reproducible con los scripts del repositorio.

## 5.2 Denominador: PIB nominal de los últimos cuatro trimestres

Un stock de fin de período es una variable de fin de período y el PIB es un flujo anual. Dividir el stock por el PIB de un solo trimestre anualizado mezcla estacionalidad y, con inflación alta, infla el denominador. El denominador elegido es la suma de los últimos cuatro flujos trimestrales del PIB nominal (`pib_4t_mm`, millones de pesos corrientes). En el cuarto trimestre coincide con la convención del FMI, que divide por el PIB del año (FMI, 2025, Annex II, Table 2, nota 1).

- **Fuente.** INDEC, PIB a precios de comprador corrientes. Para 2004T1-2025T4, serie 4.4_OGP_2004_T_17 de datos.gob.ar (88 trimestres). Para 1996T1-2003T4, serie 2.4_OGP_1993_T_17 (base 1993), empalmada con un coeficiente de enlace de 1,0837. Ese coeficiente es la razón entre las medias de 2004 en base 2004 y en base 1993 (32 trimestres, marcados `base1993_empalmada` en `pib_origen`).
- **Límite.** La razón entre bases no es constante a lo largo de 2004 (varía entre 1,07 y 1,12 por trimestre) y se aleja más en años posteriores. El nivel del PIB nominal anterior a 2004 tiene, por lo tanto, una incertidumbre que se traslada a todos los ratios de ese tramo.
- **Costo conocido.** Con inflación de tres dígitos (2023-2024), el PIB de cuatro trimestres rezaga al PIB corriente de fin de período. El ratio se sobreestima en la aceleración y se subestima en la desinflación. El diagnóstico previo, con el PIB del cuarto trimestre anualizado, daba 9,05 % para los pasivos del BCRA en 2023 contra 13,3 % con el denominador adoptado, y el FMI informa 18,4 % para un concepto más amplio. Se declara en la columna `denominador_tipo`.

## 5.3 Deuda consolidada neta y sus componentes

### 5.3.1 Definición

Se sigue la definición de consolidación con el banco central del FMI (2021, Annex II, nota 2, p. 72 del archivo local; también nota 23, p. 28). Consolidar implica restar los créditos del banco central contra el gobierno y sumar los pasivos de deuda del banco central, sin moneda ni depósitos de residentes. En símbolos:

D_neta = B − T_BCRA − T_FGS + L_BCRA − DEP, todo dividido por el PIB de cuatro trimestres.

Aquí B es la deuda bruta federal, T_BCRA la deuda del Tesoro en poder del BCRA, T_FGS la deuda del Tesoro en poder del FGS-ANSES, L_BCRA los pasivos remunerados del BCRA y DEP los depósitos del Tesoro en el BCRA. En la serie estimada, T_FGS no está disponible (sección 5.9).

### 5.3.2 Deuda federal bruta (B)

- **Fuente.** MECON, Secretaría de Finanzas, *Informe de Deuda Pública al 31/12/2025*, hoja A.4.5 (deuda bruta de la Administración Central en miles de millones de dólares, trimestral desde 1998T1). Se multiplica por el tipo de cambio de fin de trimestre de la hoja A.2.4. Control del tipo de cambio: 808,45 al 31/12/2023, igual al cociente USD/ARS de la hoja A.1.1 del informe de 2023. Archivos en `datos/crudos/mecon_deuda/`.
- **Convertibilidad.** Para 1996T1-2001T4 (24 trimestres) el tipo de cambio es 1, por la paridad legal de la Ley 23.928 (`tc_origen = paridad_legal_ley_23928`). Los otros 96 trimestres usan la hoja A.2.4.
- **Interpolación.** En 1996-1997 el informe solo trae el cierre de diciembre. Los seis trimestres no diciembre se interpolan linealmente en dólares (`spnf_origen = interpolado_lineal_usd`, bandera `flag_bruta_interpolada`). Los otros 114 son datos trimestrales del informe. Se interpola porque la alternativa, eliminar seis trimestres, deja agujeros en un VAR de frecuencia trimestral.
- **Perímetro.** Es la deuda bruta de la Administración Central. Excluye la deuda elegible pendiente de reestructuración e incluye tenencias del BCRA, del FGS y de otros organismos públicos.
- **Corrección de una fecha.** La hoja A.2.4 trae una fila con fecha 2022-03-31 duplicada, que corresponde a 2002-03-31 (intercalada con un CER de 1,0481). El script la reasigna solo si detecta la duplicación.

### 5.3.3 Pasivos remunerados del BCRA (L_BCRA)

- **Moneda local.** API del BCRA, Estadísticas Monetarias v4.0 (`https://api.bcra.gob.ar/estadisticas/v4.0/monetarias`): id 1258 (LEBAC y NOBAC), id 1260 (LELIQ y NOTALIQ), id 1261 (posición neta de pases). La API no devuelve datos de 1258 antes de 2002-03 ni de 1260 antes de 2018-01. En esos tramos el valor es cero y queda una bandera (`lebac_nobac_sin_serie`, `leliq_notaliq_sin_serie`). El cero refleja que el instrumento no existía en la fecha de inicio de la serie, no un dato imputado.
- **Pases en neto.** El id 1261 es pases pasivos menos pases activos y puede ser negativo. Ocurre en 15 trimestres (2001T2-2004T1 y 2024T3-2025T1, bandera `flag_pases_neto_negativo`). En esos trimestres el BCRA fue acreedor neto y el total reduce la deuda. El FMI informa 0,0 para 2024. Es un desvío declarado.
- **Moneda extranjera.** Id 1259 (LEBAC, LEDIV y BOPREAL en moneda extranjera, valuados en pesos). En 2023-12 y 2024-12 coincide con el id 158 (USD) por el tipo de cambio. Antes de 2002-03 el instrumento no existe y se imputa cero con bandera (24 trimestres, `flag_letras_fx_sin_serie`).
- **Swap con el Banco Popular de China (PBoC).** No existe una serie pública en la API ni en `series.xlsm` de la que se pueda leer el saldo activado. Queda omitido desde 2020 (bandera `flag_swap_pboc_faltante`, 24 trimestres). Su omisión subestima L_BCRA y, por lo tanto, subestima la deuda neta (sesgo en dirección contraria al del FGS).

### 5.3.4 Deuda del Tesoro en poder del BCRA (T_BCRA)

- **Fuente.** BCRA, *Balance del Banco Central* histórico (`https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/balbcrhis.xls`), hoja B.C.R.A., columna "Sector oficial, Total". Incluye adelantos transitorios y títulos públicos en pesos, y Letras Intransferibles y títulos en moneda extranjera. Se toma el cierre de trimestre del dato mensual. Se verifica que el total sea igual a la suma de sus dos partes en todos los trimestres.
- **Valuación.** Es valor contable del BCRA. Esto es relevante desde diciembre de 2019 (ajuste de las Letras Intransferibles) y desde mayo de 2024 (costo amortizado), según documenta el script de construcción. El FMI usa el stock de deuda del Tesoro. La sección 5.9 cuantifica el efecto en 2024.

### 5.3.5 Depósitos del Tesoro en el BCRA (DEP)

API del BCRA v4.0, id 1264, "Depósitos del gobierno en el BCRA". Es coherente con la columna "Sector oficial, Depósitos" del Balance (1.002.754 millones de pesos en 2023-12). Cobertura completa, sin interpolaciones. Se incluyen los depósitos en moneda extranjera a la valuación del BCRA.

### 5.3.6 Identidad verificada

Con los datos del CSV, `bruta − tenencia BCRA + pasivos BCRA − depósitos = deuda neta` se cumple al cuarto decimal en 2023 (119,03) y en 2024 (68,31). La identidad que el FMI usa en el Cuadro 2 (línea 6 = 2 + 4 − 5) también se cumple con sus cifras: 92,9 + 18,4 − 0,5 = 110,8 y 51,4 + 2,2 − 2,1 = 51,5.

## 5.4 Resultado primario

- **Definición.** Resultado primario del sector público nacional como porcentaje del PIB; positivo es superávit. Cada trimestre repite el nivel anual del ratio (la suma de los cuatro trimestres de un año es cuatro veces el ratio), de modo que el promedio anual de la serie es el ratio anual.
- **1996-2003.** *Compendio Fiscal 1993-2006* (MECON, Secretaría de Hacienda, Oficina Nacional de Presupuesto), capítulo I.1.3, fila "Resultado primario" (anual). Se multiplica por un coeficiente de enlace calculado en 2004 y se desagrega a trimestres con el método de Denton sin indicador (Denton, 1971), que minimiza las diferencias cuadráticas entre trimestres con el promedio anual fijo. Se justifica el enlace porque el Compendio y la serie posterior no miden el mismo perímetro, y se prefiere trasladar esa diferencia a un parámetro explícito antes que ignorarla. Se justifica Denton porque no existe un indicador trimestral confiable para todo 1996-2003.
- **Limitación declarada.** El coeficiente de enlace es inestable (la razón Compendio sobre serie vigente pasa de 1,12 en 2004 a 2,07 en 2006), lo que apunta a una diferencia de perímetro más profunda que la valuación. Es la aproximación menos confiable del empalme. Las 32 observaciones están marcadas con `es_interpolado = 1`.
- **2004-2025.** Los valores provienen de una tabla escrita en el código de ingesta (`PB_PIB_TRIM` en `ingesta_mecon_indec.py`), con un decimal, rotulada como "MECON, Sector Público Consolidado". El identificador de datos.gob.ar previsto (11.3_RDP_0_0_32) devuelve error HTTP 400. A diferencia de la deuda, **esta serie no fue reconstruida desde archivos primarios** y es la limitación más relevante de trazabilidad que persiste. La sección 5.8 la contrasta con el FMI. Se recomienda sustituirla por las series fiscales trimestrales del MECON antes de la defensa.

## 5.5 PIB real y crecimiento

- **Fuente 2004T1-2025T4.** INDEC, cuentas nacionales, PIB a precios constantes de 2004, serie 143.3_NO_PR_2004_A_21 de datos.gob.ar (índice de volumen). Según la auditoría del script de ingesta, se obtiene en vivo, sin pasar por el diccionario de contingencia.
- **Fuente 1996T1-2003T4.** No hay serie trimestral de base compatible. Se parte del nivel anual de 2004 (media del índice trimestral) y se encadena hacia atrás con las tasas anuales de crecimiento 1997-2004 (+8,1 %, +3,8 %, −3,4 %, −0,5 %, −4,5 %, −10,9 %, +8,8 %, +9,0 %), tomadas de INDEC y del Banco Mundial según el script `empalme_pib_real_pre2004.py`. La desagregación trimestral usa el mismo Denton anclado en 2004T1-2006T4 para evitar un salto en la unión. A diferencia del resultado primario, aquí no se usa coeficiente de enlace, porque la tasa de crecimiento real no tiene ambigüedad de perímetro. Las tasas están escritas en el script y no se contrastaron aquí contra la publicación primaria de INDEC.
- **Transformación.** El crecimiento que entra en el sistema es `crec = 100 × Δln(PIB real)`, trimestral. Es lo que aparece en la identidad de la deuda (Capítulo 4, sección 4.2). El crecimiento pierde la primera observación, así que tiene 119 datos.
- **Efecto del Denton.** La desagregación suaviza el perfil intra-anual de 1996-2003. La variación trimestral de ese tramo refleja el filtro y no un dato observado. Es una limitación declarada.

## 5.6 Variables financieras

### 5.6.1 EMBI+ (riesgo soberano)

- **Definición.** Diferencial de rendimiento de los bonos soberanos argentinos en dólares sobre los bonos del Tesoro de Estados Unidos, en puntos básicos, promedio trimestral.
- **1999T1-2025T4.** Serie diaria de riesgo país de Ámbito Financiero (`https://mercados.ambito.com//riesgopais/historico/...`), que reproduce el EMBI+ y el EMBI Global de J.P. Morgan. Archivo `datos/embi_real_ambito_1999_2025.csv`. Se promedia por trimestre.
- **1996T1-1998T4.** Se empalma el *stripped spread* de los bonos Brady (1994-1997) con el EMBI+ oficial desde 1998. En el punto de unión se aplica una corrección proporcional de sesgo, k = 540,0/620,0 = 0,8710 (media de 1998T1 del EMBI+ sobre media de 1997T4 del spread Brady), para evitar una discontinuidad espuria de nivel. Es una corrección multiplicativa y preserva la estructura de varianza condicional. El empalme está en `fase22_construccion_spread_1983_2025.py` y la serie resultante en `datos/procesados/spread_soberano_historico_1983_2025.csv` (columna `Spread_Empalmado_pb`). Desde 1999T1 es idéntica punto a punto a la serie de Ámbito.
- **Limitación.** El spread Brady no es exactamente el EMBI+ (distinto universo de instrumentos). El factor k ajusta el nivel pero no el comportamiento de corto plazo. Son 12 de 120 trimestres.

### 5.6.2 Tipo de cambio real multilateral (TCRM)

- **Fuente.** BCRA, Índice de Tipo de Cambio Real Multilateral (`datos/crudos/ITCRMSerie.xlsx`, hoja de promedios mensuales, base 17-12-2015 = 100).
- **Transformación.** Se divide el índice mensual por su valor de diciembre de 2001 (69,213) y se promedia por trimestre. La serie queda con diciembre de 2001 = 1. Recalculado desde el archivo crudo, el resultado coincide con `tcrm_real_bcra_1997_2025.csv` con una diferencia máxima de 4,4 × 10⁻¹⁶. Esa base se elige porque deja el índice en torno de 1 y no altera su dinámica.
- **Cobertura.** El BCRA publica el índice desde enero de 1997. Los cuatro trimestres de 1996 (3,3 % de la muestra) se retropolan con una regresión de ln(TCRM) sobre una tendencia lineal en 1997T1-1999T4 (12 observaciones), proyectada hacia atrás, y se marcan con `es_interpolado_tcrm = 1`. Es la única variable del sistema en que una proyección reemplaza a una fuente primaria. La alternativa, perder un año de muestra, se considera peor que una aproximación declarada. Los resultados centrales se verifican reestimando desde 1997 (Capítulo 6).

### 5.6.3 Tasa de política de la Fed, con tasa sombra de Wu y Xia

- **Fuentes.** FEDFUNDS (tasa efectiva de fondos federales, mensual), FRED (`https://fred.stlouisfed.org/series/FEDFUNDS`). Tasa sombra de Wu y Xia (2016), mensual, Federal Reserve Bank of Atlanta (`https://www.atlantafed.org/cqer/research/wu-xia-shadow-federal-funds-rate`). Copias en `datos/crudos/tasa_fed/`; script `ingesta_tasa_fed_1996_2025.py`; salida `tasa_fed_trimestral_1996_2025.csv`.
- **Construcción.** Cada serie mensual se promedia por trimestre. La variable `tasa_politica_fed` toma la tasa sombra cuando el promedio trimestral de FEDFUNDS es menor que 0,25 % y están los tres meses de la sombra. En los demás casos usa FEDFUNDS. El umbral 0,25 % es el techo del rango objetivo en el piso cero. Resultado: `fedfunds` en 84 trimestres, `shadow_wu_xia` en 35 (2009T1-2015T4 y 2020T2-2021T4) y `fedfunds_zlb_sin_shadow` en uno.
- **Por qué la sombra.** En el piso cero la tasa efectiva deja de reflejar la orientación de la política y su variación subestima las medidas no convencionales. La sombra recupera esa orientación.
- **Empalme en 2022T1.** La hoja de Wu y Xia termina en febrero de 2022. 2022T1 está en el piso cero (FEDFUNDS = 0,12 %) pero solo tiene dos meses de sombra, así que se usa FEDFUNDS y se marca. El salto entre 2021T4 (−1,57 %, sombra) y 2022T1 (0,12 %) es de unos 1,7 puntos y es un artefacto de la definición. Entra una vez en la primera diferencia. Los trimestres 2022T2-2025T4 usan FEDFUNDS.
- **Uso.** En el modelo entra como variación trimestral (ΔFed), con una media de −0,012 pp y un desvío estándar de 0,505 pp (119 variaciones). Ese desvío es el tamaño del shock del Capítulo 4. El ciclo 2022-2023 acumula 6,90 pp con la sombra de base y 5,25 pp medido solo con FEDFUNDS.

### 5.6.4 VIX

Índice de volatilidad implícita del CBOE (^VIX), cierre diario de Yahoo Finance descargado con `yfinance` (`ingesta_instrumentos_1996_2025.py`), promedio trimestral. Tiene cobertura real desde 1996, sin faltantes (120 observaciones). Entra como exógena en nivel (Adler y Sosa, 2013, citados en el Capítulo 4).

## 5.7 Variables que figuran en la base pero no entran en el sistema

El CER (existe desde 2002), la brecha del producto (filtro Hodrick-Prescott, λ = 1600) y los instrumentos de las pruebas de variables instrumentales no forman parte del SVARX principal. Se documentan en `datos/codebook.md`.

## 5.8 Comparación con cifras oficiales e independientes

Esta sección calcula, desde los CSV del repositorio, cada cifra propia y la compara con el FMI (2025), *Country Report* No. 25/95, Annex II, Table 2 (p. 68 del PDF; datos en `datos/procesados/escenario_base_fmi_cr2595.csv`). El FMI publica ese cuadro solo para 2023-2026.

### 5.8.1 Tabla de control, deuda (% del PIB, cierre de diciembre)

| Concepto | 2023 propio | 2023 FMI | Dif. | 2024 propio | 2024 FMI | Dif. |
|---|---|---|---|---|---|---|
| 1. Deuda federal bruta | 153,5 | 155,4 | −1,9 | 82,1 | 85,3 | −3,2 |
| 3. Deuda del Tesoro en poder del sector público | 48,6 (solo BCRA) | 62,5 (BCRA y FGS) | −13,9 | 13,2 (solo BCRA) | 33,9 (BCRA y FGS) | −20,7 |
| 4. Pasivos del BCRA, total | 14,6 | 18,4 | −3,8 | 1,6 | 2,2 | −0,6 |
|   en moneda local | 13,3 | 16,2 | −2,9 | −0,06 | 0,0 | −0,1 |
|   en moneda extranjera (sin swap) | 1,3 | 2,1 | −0,8 | 1,6 | 2,1 | −0,5 |
| 5. Depósitos del Tesoro en el BCRA | 0,52 | 0,5 | 0,0 | 2,10 | 2,1 | 0,0 |
| 6. Deuda neta consolidada | **119,0** | **110,8** | **+8,2** | **68,3** | **51,5** | **+16,8** |

Fuentes: columnas propias en `deuda_consolidada_neta_1996_2025.csv` (diciembre de cada año); columnas FMI en `escenario_base_fmi_cr2595.csv` (variables `a2_*`). El control está además en `deuda_consolidada_neta_1996_2025_control_fmi.csv`. En dólares, el FMI publica 367,9 y 478,7 mil millones para la deuda bruta federal y 262,2 y 289,0 para la deuda neta consolidada (2023 y 2024).

**Lectura.** La deuda bruta, los depósitos y los pasivos en moneda local replican al FMI dentro de 3 puntos, y los depósitos coinciden. La diferencia en la bruta se debe a que el FMI agrega intereses capitalizados, *holdouts* y reclamos por el cupón PIB (nota 1 del cuadro), que no figuran en los informes del MECON, y a la versión de PIB de su informe. La diferencia de los pasivos del BCRA en 2023 es compatible con la omisión del swap con el PBoC y de otros instrumentos, aunque no se pudo verificar por falta de una serie. La brecha de la deuda neta no se explica por esas partidas: se concentra en la línea 3.

### 5.8.2 Descomposición de la diferencia en la deuda neta

Como la deuda neta es B − T + L − DEP, la diferencia propio menos FMI es la suma de las diferencias de cada línea.

| Componente | 2023 (pp) | 2024 (pp) |
|---|---|---|
| Deuda bruta | −1,9 | −3,2 |
| Menos tenencias intra-públicas (diferencia de signo cambiado) | +13,9 | +20,7 |
| Pasivos del BCRA | −3,8 | −0,6 |
| Menos depósitos del Tesoro | 0,0 | 0,0 |
| **Diferencia en la deuda neta** | **+8,2** | **+16,8** |

El 100 % del exceso de nuestra deuda neta sobre la del FMI proviene del neteo incompleto de las tenencias intra-públicas.

### 5.8.3 Otras comparaciones

| Concepto | Propio | Contraste | Fuente del contraste |
|---|---|---|---|
| Crecimiento real del PIB 2023 (media anual del índice) | −1,9 % | −1,6 % | FMI (2025), Cuadro 1 |
| Crecimiento real del PIB 2024 | −1,4 % | −1,7 % | FMI (2025), Cuadro 1 |
| Resultado primario 2023 (promedio anual) | −2,05 % PIB | −2,8 % PIB | FMI (2025), gobierno federal |
| Resultado primario 2024 | +1,58 % PIB | +1,8 % PIB | FMI (2025), gobierno federal |
| Cociente USD/ARS al 31/12/2023 | 808,45 | 808,45 | MECON, hoja A.1.1 (informe 2023) |
| Pasivos del BCRA 2023, con PIB anualizado del cuarto trimestre | 9,05 % | 13,3 % con el denominador adoptado | `deuda_consolidada_1996_2025_control_fmi.csv` |

Las diferencias de crecimiento (0,3 puntos) son compatibles con revisiones de INDEC posteriores al informe del FMI. El resultado primario del FMI corresponde al gobierno federal, y el propio al sector público nacional con la serie descripta en 5.4, de modo que la comparación solo sirve como orden de magnitud. En ambos años los signos coinciden y la diferencia es de 0,2 a 0,75 puntos. No se pudo contrastar contra los informes mensuales del MECON porque la serie de 2004-2025 no tiene archivo de origen.

### 5.8.4 Control del T_BCRA contra el stock nominal del MECON

El Informe de Deuda del MECON publica, en la hoja A.1.9, el valor nominal de las Letras adquiridas por el BCRA (en miles de dólares).

| Concepto | 31/12/2023 | 31/12/2024 |
|---|---|---|
| Letras Intransferibles, nominal MECON (miles de millones de USD) | 67,2 | 69,3 |
| Tenencia del BCRA en moneda extranjera, valor contable, propia (miles de millones de USD) | 89,2 | 28,6 |
| Diferencia: nominal menos contable (puntos del PIB) | −9,2 (contable mayor) | +7,2 |

En 2023 la columna contable de moneda extranjera incluye otros títulos en dólares, por lo que supera al nominal de las Letras. En 2024, en cambio, el nominal de las Letras (69,3 mil millones de USD) supera en 40,7 mil millones de USD (7,2 puntos del PIB) a toda la tenencia del BCRA en moneda extranjera que registra el Balance. Eso confirma que el valor contable subestima la tenencia en 2024 por al menos esa magnitud (ver 5.9.3).

## 5.9 La diferencia con el FGS-ANSES y otras limitaciones de la deuda neta

### 5.9.1 Dos conceptos distintos

La consolidación con el banco central (FMI, 2021) y la exclusión de las tenencias intra-públicas son operaciones distintas.

- **Consolidación con el banco central.** Se netean los créditos del BCRA contra el Tesoro y se suman los pasivos de deuda del BCRA. Cambia el perímetro hacia el sector público ampliado con el banco central. Es lo que implementa la serie de esta tesis.
- **Exclusión de tenencias intra-públicas.** Se resta de la deuda del Tesoro la parte cuyo acreedor es otra entidad pública (el FGS-ANSES, organismos de la seguridad social, bancos públicos). Es un concepto de deuda consolidada del sector público en sentido amplio. El FMI (2025, Annex II, Table 2) lo aplica en la línea 3, "Deuda del Tesoro intra-sector público (BCRA y FGS)".

Con el FMI (2021) en la mano, nuestra serie netea el BCRA pero **no netea las tenencias del FGS-ANSES ni las de otros tenedores públicos**. No se trata de una omisión por criterio, sino de falta de datos.

### 5.9.2 Por qué no se pudo incluir

La serie de tenencias del FGS se publica en el Informe Estadístico Mensual y en los Anuarios del FGS de ANSES. El sitio de ANSES bloquea las descargas automatizadas con una protección anti-bot (HTTP 403). Los archivos guardados como `datos/crudos/deuda_consolidada_neta/fgs_anuario2024.pdf` y `p.html` son páginas HTML de bloqueo de 880 bytes, no el documento. Ninguna cifra del FGS está en el CSV (`tenencia_fgs_tesoro_pib` es vacía en las 120 filas, `flag_fgs_faltante = 1`). El MECON no ofrece una apertura trimestral por tenedor sectorial (la hoja A.4.5 clasifica por residencia), y el FMI da las tenencias solo para 2023-2026. Aproximar con una cifra no verificada violaría la regla de no fabricar datos.

### 5.9.3 Magnitud y dirección del sesgo

- **Brecha 2023 y 2024.** El FMI resta 62,5 puntos del PIB en 2023 y 33,9 en 2024 por tenencias del BCRA y del FGS. Nosotros restamos 48,6 y 13,2 (solo BCRA). La diferencia es 13,9 y 20,7 puntos, y se traslada uno a uno a la deuda neta: nuestra serie está por encima de la del FMI en 8,2 y 16,8 puntos (tabla 5.8.2), una vez compensadas las diferencias menores de bruta y pasivos.
- **Qué parte es valuación.** Según 5.8.4, en 2024 al menos 7,2 puntos de la brecha de 20,7 se deben a que el BCRA registra las Letras Intransferibles a costo amortizado (desde el 7 de mayo de 2024, Res. 128/24, según el script) en vez de a valor nominal, que es el que usa el FMI. El resto (13,5 puntos en 2024 y la totalidad de los 13,9 de 2023) es un residuo que incluye al FGS, a otros tenedores públicos y a diferencias de cobertura. **No se puede asignar entre ellos con los datos disponibles.**
- **Desde cuándo.** El FGS se crea por el Decreto 897/2007, dictado el 12 de julio de 2007 y publicado el 13 de julio de 2007 en el Boletín Oficial (Poder Ejecutivo Nacional, 2007, según la base normativa de la AFIP). Su importancia creció tras la incorporación de los fondos de las AFJP en 2008 (Decreto 2103/2008). Por eso, **desde 2007T3 nuestra serie neta es una cota superior de la neta del FMI**. Antes de esa fecha el FGS no existe como tenedor, y los 46 trimestres de 1996T1 a 2007T2 tienen todos los componentes (bandera `comparable_fmi = 1`). Para ese tramo, sin embargo, no hay cifra del FMI con la que contrastar.
- **Otras fuentes de brecha y su signo.**

| Fuente | Efecto sobre nuestra deuda neta |
|---|---|
| FGS-ANSES y otros tenedores públicos sin netear | Sobreestima |
| Letras Intransferibles a valor contable en vez de nominal (desde 2019 y sobre todo desde 2024) | Sobreestima |
| Swap con el PBoC activado omitido (desde 2020) | Subestima |
| Pases en neto, con trimestres negativos (2024T3-2025T1) | Subestima |
| Bruta del MECON excluye intereses capitalizados, *holdouts* y cupón PIB | Subestima |

El balance de las fuentes es una sobreestimación en 2023 y 2024 y probablemente en todo 2007-2025, de entre 8 y 17 puntos del PIB en esos dos años de control.

### 5.9.4 Cómo se trata en el análisis

La serie se presenta como **deuda neta consolidada con el BCRA, sin neteo del FGS**, y no como "la deuda neta del FMI". En el modelo entra rezagada y cumple una función de retroalimentación, de modo que la corrección de nivel no cambia la dinámica si la brecha es aproximadamente estable. Esa condición no se cumple entre 2023 y 2024, años en que la brecha pasa de 14 a 21 puntos. El sistema se estima con la deuda bruta como serie de contraste (`deuda_consolidada_1996_2025.csv`), que es homogénea y verificable en todo el período, de modo que la conclusión pueda evaluarse con ambas medidas. El cierre de la brecha exige tres insumos: las series de tenencias del FGS en ANSES (descarga manual), el stock nominal de Letras Intransferibles y adelantos por tenedor (MECON) y el saldo del swap activado (estados contables del BCRA).

## 5.10 Estadísticos descriptivos

Muestra 1996T1-2025T4. El crecimiento y la variación de la Fed pierden una observación por la primera diferencia. Las variables en niveles del sistema de estimación son las filas 1, 6 a 9 y 11.

| Variable | Media | Desv. est. | Mínimo | Máximo | n |
|---|---|---|---|---|---|
| Deuda consolidada neta (% PIB) | 56,55 | 27,15 | 26,13 | 136,60 | 120 |
| Deuda federal bruta (% PIB) | 64,37 | 31,45 | 31,86 | 154,59 | 120 |
| Tenencia del BCRA de deuda del Tesoro (% PIB) | 12,40 | 7,77 | 1,82 | 48,57 | 120 |
| Pasivos remunerados del BCRA (% PIB) | 5,22 | 3,53 | −2,29 | 14,58 | 120 |
| Depósitos del Tesoro en el BCRA (% PIB) | 0,64 | 0,77 | 0,01 | 3,74 | 120 |
| Resultado primario (% PIB) | −0,27 | 1,73 | −3,80 | 4,08 | 120 |
| Crecimiento real del PIB (pp trimestral, 100·Δln) | 0,43 | 6,47 | −12,23 | 18,21 | 119 |
| EMBI+ (pb) | 1483,95 | 1573,84 | 210,22 | 6658,98 | 120 |
| TCRM (dic. 2001 = 1) | 1,63 | 0,45 | 0,98 | 2,76 | 120 |
| Tasa de política de la Fed (%) | 2,08 | 2,67 | −2,92 | 6,52 | 120 |
| Variación de la tasa de la Fed (pp) | −0,01 | 0,50 | −1,43 | 1,69 | 119 |
| FEDFUNDS (%) | 2,44 | 2,20 | 0,06 | 6,52 | 120 |
| VIX (puntos) | 20,15 | 7,11 | 10,31 | 58,60 | 120 |

Fuente: cálculo propio sobre los CSV citados en 5.1. La desviación estándar es muestral (ddof = 1). El crecimiento del PIB tiene un desvío alto porque el tramo 1996-2003 contiene variaciones trimestrales de la crisis de 2001-2002, y no por ruido de medición. El máximo de la deuda neta ocurre en 2002T3 y el mínimo en 2013T3. El máximo del EMBI+ ocurre en 2002T3 y el mínimo en 2007T1.

## 5.11 Resumen de limitaciones de datos

1. **Deuda neta sin FGS.** Cota superior de la neta del FMI desde 2007T3 (secciones 5.8 y 5.9).
2. **Resultado primario 2004-2025.** Serie de un decimal que no se reconstruyó desde archivos. Su contraste con el FMI es solo de orden de magnitud.
3. **Empalme 1996-2003** de resultado primario, PIB real y PIB nominal. Incertidumbre de nivel por el coeficiente de enlace.
4. **Seis trimestres de deuda bruta interpolados** (1996-1997) y **cuatro de TCRM retropolados** (1996).
5. **Swap con el PBoC** y **pases en neto** en los pasivos del BCRA.
6. **Valuación contable** de la deuda en poder del BCRA.
7. **Denominador** con rezago en períodos de inflación alta.

## Referencias del capítulo

Denton, F. T. (1971). Adjustment of monthly or quarterly series to annual totals: An approach based on quadratic minimization. *Journal of the American Statistical Association, 66*(333), 99-102.

Federal Reserve Bank of Atlanta. (s. f.). *Wu-Xia shadow federal funds rate* [Conjunto de datos]. https://www.atlantafed.org/cqer/research/wu-xia-shadow-federal-funds-rate

Fondo Monetario Internacional. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper). Fondo Monetario Internacional. (Archivo local: `Bibliografia/descargas_verificacion/imf2021_dsf_mac_review.pdf`; Annex II, nota 2, p. 72.)

Fondo Monetario Internacional. (2025). *Argentina: Request for an extended arrangement under the Extended Fund Facility* (IMF Country Report No. 25/95). Fondo Monetario Internacional. (Archivo local: `Bibliografia/descargas_verificacion/1argea2025002-print-pdf.pdf`; Annex II, Table 2, p. 68.)

Banco Central de la República Argentina. (s. f.). *Balance del Banco Central, serie histórica* [Conjunto de datos]. https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/balbcrhis.xls

Banco Central de la República Argentina. (s. f.). *API de Estadísticas Monetarias v4.0* [Conjunto de datos]. https://api.bcra.gob.ar/estadisticas/v4.0/monetarias

Board of Governors of the Federal Reserve System (US). (s. f.). *Federal funds effective rate* [FEDFUNDS; conjunto de datos]. Federal Reserve Bank of St. Louis, FRED. https://fred.stlouisfed.org/series/FEDFUNDS

Ministerio de Economía de la Nación, Secretaría de Finanzas. (2025). *Informe de deuda pública al 31/12/2025* [Conjunto de datos]. (Archivos de los cierres 2007 a 2025 en `datos/crudos/mecon_deuda/`.)

Ministerio de Economía y Producción, Secretaría de Hacienda, Oficina Nacional de Presupuesto. (2006). *Compendio fiscal 1993-2006*. https://www.economia.gob.ar/onp/documentos/ejectexto/compendio/compendio93-06.pdf

Poder Ejecutivo Nacional. (2007). *Decreto 897/2007: Fondo de Garantía de Sustentabilidad del Régimen Previsional Público de Reparto* (Boletín Oficial, 13 de julio de 2007). Base normativa de la AFIP. https://biblioteca.afip.gob.ar/dcp/DEC_C_000897_2007_07_12

Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking, 48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300
