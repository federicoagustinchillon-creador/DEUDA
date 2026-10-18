# 5. Datos

Las series son trimestrales y cubren 1996-2025. Los primeros trimestres de la ventana se usan como condiciones iniciales de los rezagos (la variación de la tasa de la FED entra con dos rezagos y los órdenes de hasta seis rezagos se comparan sobre una muestra común; Lütkepohl, 2005, sec. 4.3), de modo que las ecuaciones se estiman con los trimestres 1998T2-2025T4 (111 observaciones; sección 4.5). Las fuentes, secundarias, son el Ministerio de Economía de la Nación (MECON), el BCRA, el Instituto Nacional de Estadística y Censos (INDEC), la Reserva Federal, J.P. Morgan y el Banco de Pagos Internacionales. Dos series no tienen dato publicado en toda la ventana, el EMBI antes de diciembre de 1998 y el TCRM en 1996, y se completan con empalmes validados (sección 5.4). Los estadísticos descriptivos están en el Apéndice, sección A.1.

## 5.1 Series y fuentes

**Tabla 5.1. Series del modelo: rol, fuente y construcción**

| Variable | Rol en el modelo | Fuente | Construcción |
|---|---|---|---|
| Deuda federal bruta (% del PIB) | Especificación principal | MECON, Informe de Deuda Pública (Administración Central) | Sección 5.2 |
| Deuda consolidada con el BCRA (% del PIB) | Extensión, estimada desde 2002 | MECON (deuda de la Administración Central) y BCRA (balance y estadísticas monetarias) | Sección 5.2; no descuenta las tenencias del FGS (sección 5.6) |
| Resultado primario (% del PIB) | Endógena | MECON, esquema ahorro-inversión-financiamiento del Sector Público Nacional, base caja | Suma mensual por trimestre, anualizada; sin rentas de la propiedad (sección 5.3) |
| Crecimiento real | Endógena | INDEC, PIB a precios constantes | Variación logarítmica trimestral; 1996-2003 en base 1993 empalmada a base 2004 |
| Riesgo país: diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), en puntos básicos | Endógena | J.P. Morgan, serie diaria publicada por Ámbito Financiero desde el 11 de diciembre de 1998 | Promedio trimestral; 1996T1-1998T3 empalmado con la tasa de préstamos interfinancieros en dólares del BCRA menos la tasa de fondos federales (sección 5.4) |
| Tipo de cambio real multilateral (TCRM) | Endógena | BCRA, desde enero de 1997 | Promedio trimestral del índice; 1996 encadenado con el tipo de cambio real efectivo amplio del BIS (sección 5.4) |
| Tasa de política monetaria de la Reserva Federal (FED) | Exógena | Tasa de fondos federales, obtenida de FRED (Board of Governors of the Federal Reserve System, s. f.); tasa sombra de Wu y Xia (2016) (Federal Reserve Bank of Atlanta, s. f.) | Promedio trimestral; tasa sombra en el límite cero; cambios de serie en 2009T1, 2016T1, 2020T2 y 2022T1 (sección 5.4) |
| VIX | Exógena | Índice VIX de la *Chicago Board Options Exchange* (CBOE), descargado de Yahoo Finance | Promedio trimestral |

Fuente: elaboración propia.

Todos los cocientes usan como denominador el PIB nominal de los últimos cuatro trimestres, que evita la estacionalidad del PIB de un solo trimestre y, en diciembre, coincide con el PIB del año, comparable con las cifras anuales del FMI.

## 5.2 Deuda federal bruta y deuda consolidada con el BCRA

La deuda federal bruta, de la especificación principal, es la deuda de la Administración Central que publica el MECON (Ministerio de Economía de la Nación, 2025), en pesos al tipo de cambio de fin de trimestre. Incluye la deuda en poder del BCRA, del Fondo de Garantía de Sustentabilidad (FGS) de la Administración Nacional de la Seguridad Social (ANSES) y de otros organismos públicos, igual que la del FMI (2026, anexo II, cuadro 2, línea 1). A fines de 2025 la serie propia da 77,7% del PIB y la del FMI, 80,3%. La diferencia son conceptos que el MECON no incluye (intereses capitalizados hasta el vencimiento, deuda con acreedores que no entraron a los canjes y reclamos por los cupones atados al PIB) y la medición del PIB. La dinámica se estima con la serie propia y la simulación parte del *stock* del FMI, de modo que esa diferencia no entra en la proyección. La Figura 5.1 muestra las dos series de deuda.

La deuda consolidada con el BCRA, de la extensión, sigue la consolidación del FMI (2021, anexo II). Se construye para 1996-2025, pero la extensión se estima desde 2002: hasta 2001 el BCRA operó con la autonomía formal de la Carta Orgánica de 1992 y bajo la Convertibilidad, sin financiar al Tesoro, y el criterio del FMI para consolidar al banco central con el gobierno es precisamente que lo financie o realice actividades cuasifiscales (sección 2.9). Antes de 2002 la consolidación no tiene fundamento en ese criterio. Por eso la extensión usa una muestra más corta que la especificación principal (sección 7.6). Aunque la serie se llama deuda consolidada con el BCRA, solo consolida al Tesoro con el BCRA y no descuenta la deuda del Tesoro en poder del FGS, de modo que no equivale a la deuda consolidada del FMI (sección 5.6):

D = B − T + L − DEP

donde B es la deuda federal bruta; T, la deuda del Tesoro en poder del BCRA (adelantos transitorios, títulos en pesos y Letras Intransferibles); L, los pasivos remunerados del BCRA (LEBAC y NOBAC, LELIQ y NOTALIQ, posición neta de pases y letras en moneda extranjera), y DEP, los depósitos del Tesoro en el BCRA. Las Letras Intransferibles se valúan al valor nominal que publica el MECON, el mismo criterio de la deuda bruta, y no al valor contable del balance del BCRA (Banco Central de la República Argentina, s. f.); antes de 2006, cuando no existían, rige el valor contable.

![Figura 5.1. Deuda federal bruta y deuda consolidada con el BCRA en 1996-2025 (% del PIB de los últimos cuatro trimestres). Los puntos son las cifras del FMI a diciembre de 2023, 2024 y 2025 (Tabla 5.2). Fuente: elaboración propia con datos del MECON, el BCRA y el INDEC; FMI (2026, anexo II, cuadro 2).](../tesis/figuras/fig5_1_deuda_1996_2025.png)

## 5.3 Resultado primario y crecimiento

El resultado primario trimestral es la suma de los tres meses de la serie del MECON, y la tesis usa una sola definición en las dos especificaciones: el resultado primario del Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA al Tesoro (FMI, 2026, cuadro 1, nota 4), y la fuente pública no separa esas transferencias del resto de las rentas de la propiedad. La serie sin rentas es la que las excluye, a costa de dejar afuera también otras rentas menores. En el perímetro consolidado esas utilidades son, además, un flujo interno entre el BCRA y el Tesoro. La serie con rentas de la propiedad se informa como robustez (Apéndice, sección A.10). El máximo anual de 1996-2025 es 3,29% del PIB, en 2004; con rentas de la propiedad, 3,58%, en el mismo año.

El PIB real es la serie del INDEC en base 2004, empalmada con la de base 1993 para 1996-2003; el empalme afecta el nivel y no las tasas de crecimiento que entran al modelo. Se usa la serie original porque la desestacionalizada empieza en 2004, y la estacionalidad la absorben las variables binarias.

## 5.4 Variables financieras y externas

El EMBI mide la diferencia de rendimiento (*spread*) entre los bonos soberanos argentinos en dólares y los bonos del Tesoro de Estados Unidos, en puntos básicos. Es el promedio trimestral de la serie diaria de J.P. Morgan que publica Ámbito Financiero desde el 11 de diciembre de 1998. El TCRM es el índice del BCRA, publicado desde enero de 1997, promediado por trimestre. El VIX es la volatilidad implícita del índice S&P 500.

El EMBI de 1996T1-1998T3 y el TCRM de 1996 se completan con dos empalmes, cuya validación está en el Apéndice, sección A.2 (Figura A.1).

**EMBI de 1996T1-1998T3.** Para los trimestres anteriores a la serie diaria se usa el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA, serie oficial mensual desde octubre de 1994, y la tasa de fondos federales. Durante la convertibilidad, lo que costaba el dólar en el sistema financiero argentino por encima de la tasa de Estados Unidos reflejaba el riesgo argentino. La relación se estima en la superposición de las dos series, 1998T4-2001T3 (12 trimestres), que termina antes del corralito de diciembre de 2001 porque este interrumpió el mercado interbancario en dólares: EMBI = 550,3 + 1,171 × diferencial, con un R² de 0,89 y una correlación de 0,944. En la validación cruzada que deja un trimestre afuera, el error típico es de 102 puntos básicos, frente a un desvío del EMBI de 240. Estimada solo con 1998T4-2000T4, la relación pronostica para los tres primeros trimestres de 2001 valores de 744, 801 y 1.033 puntos básicos, contra 750, 973 y 1.469 observados: acierta el nivel y subestima el salto de la crisis. Si el empalme tiene un sesgo, atenúa la volatilidad de 1996-1998 y vuelve conservadoras las probabilidades.

**TCRM de 1996.** El índice del BCRA se encadena hacia atrás con las variaciones del tipo de cambio real efectivo amplio de Argentina que publica el Banco de Pagos Internacionales (Bank for International Settlements [BIS], s. f.), invertido porque ese índice sube cuando el peso se aprecia. Las variaciones trimestrales de los dos índices tienen una correlación de 0,92 entre 1997 y 2025 y de 0,98 en 1997-2001. Con dos rezagos, los valores de 1996 intervienen solo como condiciones iniciales.

**Los resultados no dependen de los empalmes.** Con datos desde 1999, que solo usan el EMBI observado, la probabilidad de no estabilización de la deuda federal bruta en 2031 es de 29,5% [22,5; 36,7], contra 27,7% [20,6; 34,7] con la ventana completa, y las conclusiones sobre H1a y sobre el efecto de la FED en la probabilidad no cambian (Apéndice, sección A.10).

La tasa de la FED es la de fondos federales, salvo en los trimestres en el límite cero (2009-2015 y 2020-2021), donde la tasa efectiva deja de reflejar la orientación de la política y se usa la tasa sombra de Wu y Xia (2016). En el modelo entra su variación trimestral. La serie cambia de tramo cuatro veces: entra al límite cero en 2009T1 y 2020T2 y sale de él en 2016T1 y 2022T1. En cada una de esas transiciones la variación se calcula con la tasa efectiva en ambos trimestres, para no confundir el cambio de serie con un cambio de política; sin esa corrección, la variación de 2009T1 saldría de la diferencia entre una tasa sombra y una efectiva. Dentro de cada tramo se usa la propia serie. Su desvío estándar en la muestra, 0,501 puntos, es el tamaño del primer escenario de la FED (sección 4.6). Las Figuras 5.2 y 5.3 muestran las variables endógenas y las exógenas.

![Figura 5.2. Variables endógenas del SVARX en 1996-2025. El crecimiento es la variación trimestral del PIB real sin desestacionalizar. El EMBI de 1996T1-1998T3 y el TCRM de 1996 provienen de los empalmes de la sección 5.4. Las líneas punteadas marcan los quiebres de Bai y Perron. Fuente: elaboración propia con datos del INDEC, el MECON, el BCRA y J.P. Morgan (sección 5.4).](../tesis/figuras/fig5_2_variables_endogenas.png)

![Figura 5.3. Variables exógenas del SVARX. Arriba, tasa de política de la Reserva Federal: tasa de fondos federales y, en el límite cero, tasa sombra de Wu y Xia (2016). Abajo, VIX. Promedios trimestrales. Fuente: elaboración propia con datos de Board of Governors of the Federal Reserve System (s. f.), Federal Reserve Bank of Atlanta (s. f.) y CBOE, descargados de Yahoo Finance.](../tesis/figuras/fig5_3_fed_y_vix.png)

## 5.5 Contraste con el FMI

**Tabla 5.2. Deuda pública: esta tesis y FMI (% del PIB, diciembre)**

| Concepto | 2023, tesis | 2023, FMI | 2024, tesis | 2024, FMI | 2025, tesis | 2025, FMI |
|---|---|---|---|---|---|---|
| Deuda federal bruta | 153,5 | 154,6 | 82,1 | 84,7 | 77,7 | 80,3 |
| Deuda del Tesoro en poder del sector público | 39,4 (solo BCRA) | 62,1 (BCRA y FGS) | 20,4 (solo BCRA) | 33,7 (BCRA y FGS) | 17,2 (solo BCRA) | 31,4 (BCRA y FGS) |
| Pasivos del BCRA | 14,6 | 19,2 | 1,6 | 2,6 | 1,3 | 3,3 |
| Depósitos del Tesoro en el BCRA | 0,5 | no se restan | 2,1 | no se restan | 0,8 | no se restan |
| Deuda consolidada con el BCRA | 128,2 | 111,1 | 61,1 | 53,6 | 61,0 | 52,1 |

Fuente: elaboración propia con datos del MECON, el BCRA y el INDEC; FMI (2026, anexo II, cuadro 2, líneas 1, 3, 4 y 5). En el cuadro del FMI, la deuda consolidada es la deuda federal en manos de tenedores ajenos al sector público más los pasivos del BCRA, sin restar los depósitos del Tesoro.

La deuda federal bruta propia queda entre 1,1 y 2,6 puntos por debajo de la del FMI (sección 5.2). La consolidada queda 17,1 puntos por encima en 2023, 7,5 en 2024 y 8,9 en 2025, sobre todo porque el FMI resta también la deuda del Tesoro en poder del FGS. Los pasivos del BCRA propios son menores, entre otras razones, porque no incluyen el *swap*[^en-swap] con el Banco Popular de China, que no tiene serie pública (0,9% del PIB en 2024 y en 2025 según el FMI).

## 5.6 Limitaciones de los datos

La principal limitación es el FGS. La serie consolidada no descuenta la deuda del Tesoro en su poder porque no hay una serie pública que separe esas tenencias para todo el período: la Secretaría de Finanzas las publica agrupadas con las de otras agencias del sector público, incluido el BCRA. La simulación de la extensión parte de la deuda consolidada del FMI, 52,1% del PIB en 2025, que sí las descuenta, de modo que la brecha afecta la dinámica estimada y no el punto de partida. La especificación principal no se ve afectada, porque la deuda federal bruta incluye las tenencias del sector público, igual que la del FMI.

El resultado primario cubre el Sector Público Nacional, más amplio que el gobierno federal del FMI, y tiene dos cambios de metodología (2007 y 2015) sin superposición.

La muestra de estimación empieza en 1998T2, de modo que incluye seis años de la Convertibilidad y su crisis, y para esos años varias series no son observaciones directas. La deuda federal bruta trimestral del MECON empieza en 1998T1; los seis trimestres que no son de diciembre en 1996-1997 se interpolan linealmente en dólares, y solo intervienen en la detección de quiebres, no en la estimación. El PIB real de 1996-2003 proviene de la base 1993 del INDEC, empalmada a la base 2004 con un coeficiente de enlace (k = 1,751): el nivel anterior a 2004 depende de ese año de enlace, pero las tasas de crecimiento, que son lo que entra al modelo, no. El EMBI de 1996T1-1998T3 y el TCRM de 1996 se reconstruyen con variables puente (sección 5.4), y la estimación con datos desde 1999, sin ellos, se informa en la Tabla 6.6. El resultado primario es mensual y no se interpola.

[^en-swap]: *Swap*: acuerdo de intercambio de monedas entre bancos centrales.
