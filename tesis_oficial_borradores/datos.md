# 5. Datos

Las series son trimestrales. Las dos series de deuda se construyen para 1996T1-2025T4; el sistema usa datos desde 1999T1, y la muestra efectiva de estimación es 2000T3-2025T4 (102 trimestres), porque los primeros trimestres se reservan como condiciones iniciales para que todos los órdenes de rezago se comparen sobre la misma muestra (sección 4.5). Las fuentes, secundarias, son el Ministerio de Economía de la Nación (MECON), el BCRA, el Instituto Nacional de Estadística y Censos (INDEC), la Reserva Federal y J.P. Morgan. Los estadísticos descriptivos están en el Apéndice (A.1).

## 5.1 Series y fuentes

**Tabla 5.1. Series del modelo: rol, fuente y construcción**

| Variable | Rol en el modelo | Fuente | Construcción |
|---|---|---|---|
| Deuda federal bruta (% del PIB) | Especificación principal | MECON, Informe de Deuda Pública (Administración Central) | Sección 5.2 |
| Deuda consolidada con el BCRA (% del PIB) | Extensión | MECON (deuda de la Administración Central) y BCRA (balance y estadísticas monetarias) | Sección 5.2 |
| Resultado primario (% del PIB) | Endógena | MECON, esquema ahorro-inversión-financiamiento del Sector Público Nacional, base caja | Suma mensual por trimestre, anualizada; con o sin rentas de la propiedad según el perímetro (sección 5.3) |
| Crecimiento real | Endógena | INDEC, PIB a precios constantes | Variación logarítmica trimestral; 1999-2003 en base 1993 empalmada a base 2004 |
| EMBI+ (puntos básicos) | Endógena | J.P. Morgan, EMBI+ Argentina, serie diaria publicada por Ámbito Financiero | Promedio trimestral |
| Tipo de cambio real multilateral | Endógena | BCRA | Promedio trimestral del índice |
| Tasa de política de la FED | Exógena | Tasa de fondos federales, obtenida de FRED (Board of Governors of the Federal Reserve System, s. f.); tasa sombra de Wu y Xia (2016) (Federal Reserve Bank of Atlanta, s. f.) | Promedio trimestral; tasa sombra en el límite cero; empalme en 2022T1 (sección 5.4) |
| VIX | Exógena | Índice VIX de la *Chicago Board Options Exchange* (CBOE), descargado de Yahoo Finance | Promedio trimestral |

Fuente: elaboración propia.

Todos los cocientes usan como denominador el PIB nominal de los últimos cuatro trimestres, que evita la estacionalidad del PIB de un solo trimestre y, en diciembre, coincide con el PIB del año, comparable con las cifras anuales del FMI.

## 5.2 Deuda federal bruta y deuda consolidada con el BCRA

La deuda federal bruta, de la especificación principal, es la deuda de la Administración Central que publica el MECON (Ministerio de Economía de la Nación, 2025), en pesos al tipo de cambio de fin de trimestre. Incluye la deuda en poder del BCRA, del Fondo de Garantía de Sustentabilidad (FGS) de la Administración Nacional de la Seguridad Social (ANSES) y de otros organismos públicos, igual que la del FMI (2026, anexo II, cuadro 2, línea 1). A fines de 2025 la serie propia da 77,7% del PIB y la del FMI, 80,3%. La diferencia son conceptos que el MECON no incluye (intereses capitalizados hasta el vencimiento, deuda con acreedores que no entraron a los canjes y reclamos por los cupones atados al PIB) y la medición del PIB. La dinámica se estima con la serie propia y la simulación parte del *stock* del FMI, de modo que esa diferencia no entra en la proyección. La Figura 5.1 muestra las dos series de deuda.

La deuda consolidada con el BCRA, de la extensión, sigue la consolidación del FMI (2021, anexo II):

D = B − T + L − DEP

donde B es la deuda federal bruta; T, la deuda del Tesoro en poder del BCRA (adelantos transitorios, títulos en pesos y Letras Intransferibles); L, los pasivos remunerados del BCRA (LEBAC y NOBAC, LELIQ y NOTALIQ, posición neta de pases y letras en moneda extranjera), y DEP, los depósitos del Tesoro en el BCRA. Las Letras Intransferibles se valúan al valor nominal que publica el MECON, el mismo criterio de la deuda bruta, y no al valor contable del balance del BCRA (Banco Central de la República Argentina, s. f.); antes de 2006, cuando no existían, rige el valor contable.

![Figura 5.1. Deuda federal bruta y deuda consolidada con el BCRA, 1996-2025 (% del PIB de los últimos cuatro trimestres). Los puntos son las cifras del FMI a diciembre de 2023, 2024 y 2025: deuda federal bruta, 154,6, 84,7 y 80,3; deuda del sector público consolidado con el BCRA, 111,1, 53,6 y 52,1. Fuente: elaboración propia con datos del MECON, el BCRA y el INDEC, y FMI (2026, anexo II, cuadro 2).](../tesis/figuras/fig5_1_deuda_1996_2025.png)

## 5.3 Resultado primario y crecimiento

El resultado primario trimestral es la suma de los tres meses de la serie del MECON, y su definición depende del perímetro de la deuda. Con la deuda federal bruta se usa el resultado con rentas de la propiedad, que es la definición del FMI para el gobierno federal: las utilidades que el BCRA transfiere al Tesoro son un ingreso del Tesoro. Con esa definición, la serie propia da 1,78% del PIB en 2024 y 1,38% en 2025, frente a 1,8% y 1,4% del FMI (2026). Con la deuda consolidada con el BCRA se usa el resultado sin rentas de la propiedad, porque en ese perímetro las utilidades del BCRA son un flujo interno; la fuente no permite separarlas del resto de las rentas, de modo que se excluye algo más. En cada perímetro, la otra definición se informa como robustez (Apéndice, A.8). El máximo anual de 1999-2025 con la definición del FMI es 3,58% del PIB, en 2004; sin rentas de la propiedad, 3,29%.

El PIB real es la serie del INDEC en base 2004, empalmada con la de base 1993 para 1999-2003; el empalme afecta el nivel y no las tasas de crecimiento que entran al modelo. Se usa la serie original porque la desestacionalizada empieza en 2004, y la estacionalidad la absorben las variables binarias.

## 5.4 Variables financieras y externas

El EMBI+ es el índice de J.P. Morgan para Argentina, promedio trimestral de la serie diaria que publica Ámbito Financiero, disponible desde diciembre de 1998. De ahí el inicio en 1999T1: antes solo había diferenciales de los bonos Brady[^en-brady] y valores transcriptos sin cuadro ni página de origen, y el tipo de cambio real de 1996 estaba retropolado; empezar en 1999 deja todas las series con una fuente publicada y verificable. El VIX es la volatilidad implícita del índice S&P 500.

La tasa de la FED es la de fondos federales, salvo en los trimestres en el límite cero (2009-2015 y 2020-2021), donde la tasa efectiva deja de reflejar la orientación de la política y se usa la tasa sombra de Wu y Xia (2016). En el modelo entra su variación trimestral. En 2022T1, cuando la serie pasa de la tasa sombra a la efectiva, la variación se calcula con la tasa efectiva en ambos trimestres, para no confundir el cambio de serie con un cambio de política. Su desvío estándar en la muestra, 0,504 puntos, es el tamaño del primer escenario de la FED (sección 4.6). Las Figuras 5.2 y 5.3 muestran las variables endógenas y las exógenas.

![Figura 5.2. Variables endógenas del SVARX, 1999-2025. El crecimiento es la variación trimestral del PIB real sin desestacionalizar. Las líneas punteadas marcan los quiebres de Bai y Perron. Fuente: elaboración propia con datos del INDEC, el MECON, el BCRA y J.P. Morgan (sección 5.4).](../tesis/figuras/fig5_2_variables_endogenas.png)

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

Fuente: elaboración propia con datos del MECON, el BCRA y el INDEC, y FMI (2026, anexo II, cuadro 2, líneas 1, 3, 4 y 5). En el cuadro del FMI, la deuda consolidada es la deuda federal en manos de tenedores ajenos al sector público más los pasivos del BCRA, sin restar los depósitos del Tesoro.

La deuda federal bruta propia queda entre 1,1 y 2,6 puntos por debajo de la del FMI (sección 5.2). La consolidada queda 17,1 puntos por encima en 2023, 7,5 en 2024 y 8,9 en 2025, sobre todo porque el FMI resta también la deuda del Tesoro en poder del FGS. Los pasivos del BCRA propios son menores, entre otras razones, porque no incluyen el *swap*[^en-swap] con el Banco Popular de China, que no tiene serie pública (0,9% del PIB en 2024 y en 2025 según el FMI).

## 5.6 Limitaciones de los datos

La principal limitación es el FGS. La serie consolidada no descuenta la deuda del Tesoro en su poder porque no hay una serie pública que separe esas tenencias para todo el período: la Secretaría de Finanzas las publica agrupadas con las de otras agencias del sector público, incluido el BCRA. La simulación de la extensión parte de la deuda consolidada del FMI, 52,1% del PIB en 2025, que sí las descuenta, de modo que la brecha afecta la dinámica estimada y no el punto de partida. La especificación principal no se ve afectada, porque la deuda federal bruta incluye las tenencias del sector público, igual que la del FMI.

El resultado primario cubre el Sector Público Nacional, más amplio que el gobierno federal del FMI, y tiene dos cambios de metodología (2007 y 2015) sin superposición.

[^en-swap]: *Swap*: acuerdo de intercambio de monedas entre bancos centrales.
[^en-brady]: *Brady*: bonos emitidos por países en desarrollo en la década de 1990 para canjear préstamos bancarios en cesación de pagos, según el plan que lleva el nombre del secretario del Tesoro de Estados Unidos Nicholas Brady.
