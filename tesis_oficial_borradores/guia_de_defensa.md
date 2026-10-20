# Guía de defensa: qué hicimos, por qué y qué nos pueden discutir

Documento interno del grupo. No forma parte de la tesis. Resume cada paso del trabajo empírico con su justificación, según la versión final (19/10/2026): ventana 1996-2025 con empalmes validados, binarias presidenciales, cuatro transiciones de la tasa de la FED corregidas, 1.000 réplicas y deuda consolidada desde 2002. Incluye las críticas que se resolvieron y las que todavía puede hacer un jurado, con la respuesta. Todos los números salen de la hoja de números (`_hoja_de_numeros.md`) y del Apéndice.

**Lo más importante, antes que nada: la métrica.** La probabilidad de no estabilización se informa con dos métricas, y los veredictos cambian según cuál se use. Con la **métrica anual** (la que usamos siempre: cada año, ¿el resultado primario previsto alcanza para que la deuda no suba ese año?) da 27,7% en 2031 y H1b se cumple. Con la **definición operativa del FMI** (promedia los *shocks* de la trayectoria y deja afuera el tipo de cambio real y el ajuste *stock*-flujo; FMI, 2022, recuadro 3), que es la que produce el 1% del FMI, da 3,1% [0,0; 6,3] y H1b no se cumple. **Decidimos (D16, 20/10) que la definición del FMI decide el contraste**, porque H1b compara con cifras que salen de ella; la métrica anual queda como complemento. Resultado: **H1a y H1b no quedan respaldadas; H2, parcialmente**. El mensaje para defender: medido como lo mide el FMI, el riesgo es del mismo orden que el que informa el organismo; lo que su métrica deja afuera por construcción es la valuación anual de la deuda en dólares (57,8% de la deuda), y al incorporarla la probabilidad sube a 27,7%. Una hipótesis no respaldada es un resultado válido: no hay que presentarlo como un fracaso. Hay que saber explicar esto mejor que cualquier otra cosa: es lo primero que va a preguntar un jurado que conozca el marco del FMI.

**Cómo usar esta guía.** La Parte 1 es la exposición: el orden en que conviene contar el trabajo. La Parte 3 es el ensayo de preguntas: conviene que cada uno de los tres pueda responder cualquiera de ellas sin leer. La Parte 4 tiene los números que hay que saber de memoria.

## Parte 1. Qué hicimos, paso a paso

### Paso 1. Pregunta e hipótesis

- **Pregunta.** ¿En qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario condicionan la sostenibilidad de la deuda pública argentina en 2026-2035, y cuál es la probabilidad de que no se estabilice bajo el escenario base? Pregunta específica: ¿qué pasa si la FED endurece su política?
- **H1a:** el superávit primario, por sí solo, no basta para estabilizar la deuda. Se contrasta con dos condiciones, y se acepta si se cumplen las dos: (i) la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del *shock* fiscal, con un intervalo de 90% de la diferencia que excluye el cero; (ii) con el resultado primario de todos los años desplazado en la misma magnitud hasta que el de 2031 llega a su máximo histórico, la probabilidad de no estabilización en 2031 sigue por encima del 1% del FMI. La condición (ii) se evalúa con cada métrica; la (i) no depende de la métrica. Como las participaciones suman 100, la (i) equivale a que el bloque fiscal explique menos de la mitad de la varianza.
- **H1b:** nuestra probabilidad de no estabilización de la deuda federal bruta es mayor que la del FMI para esa misma deuda, en 2031 y en 2035. Criterio: el límite inferior del intervalo de 90% supera 1% y 3%; se informa Bonferroni por los dos horizontes (95%). Se evalúa con la métrica anual y con la definición operativa del FMI.
- **H2:** un endurecimiento de la FED eleva la deuda esperada y la probabilidad de no estabilización en 2035. Criterio: el intervalo de 90% de la diferencia con el escenario base excluye el cero en las dos medidas. Si se cumple en una medida o en un escenario y no en los otros, H2 se declara parcialmente respaldada. La hipótesis se refiere al efecto total; los canales se examinan aparte.
- **Cifras de comparación:** las del análisis de sostenibilidad más reciente del FMI (2026, Artículo IV y segunda revisión): 1% a mediano plazo (2031) y menos de 3% en el abanico de diez años (2035). El 1% es la estimación del FMI para Argentina, no un umbral de riesgo.

### Paso 2. Datos y perímetro

- **Perímetro principal (D1):** deuda federal bruta, el perímetro del FMI. La simulación parte del *stock* del FMI a fines de 2025, 80,3% del PIB (cuadro 2, línea 1). Nuestra serie, construida con datos del MECON, da 77,7%; la diferencia son los intereses capitalizados, la deuda no presentada al canje, los reclamos por los cupones atados al PIB y la medición del PIB.
- **Extensión:** deuda consolidada con el BCRA, 52,1% del PIB a fines de 2025 en la definición del FMI, con 68,5% en moneda extranjera. Se estima desde 2002, porque antes el BCRA operaba con la autonomía de la Carta Orgánica de 1992 y la Convertibilidad, con límites estrictos a la asistencia al Tesoro, y el criterio del FMI para consolidar es que el banco financie al gobierno o haga actividades cuasifiscales. Nuestra serie no descuenta la deuda en poder del FGS; por eso el nombre exacto es "deuda del Tesoro neta de la que está en poder del BCRA, más los pasivos remunerados del BCRA", y la llamamos deuda consolidada con el BCRA por brevedad.
- **Ventana (D2):** 1996-2025 para todo el estudio y 2026-2035 para la proyección. Las ecuaciones se estiman con 1998T2-2025T4, 111 trimestres, porque la deuda federal trimestral del MECON empieza en 1998T1 y entra rezagada; los trimestres anteriores son condiciones iniciales de los demás rezagos, y todos los órdenes hasta seis se comparan sobre los mismos trimestres (Lütkepohl, 2005, sec. 4.3). Ojo: por eso el TCRM empalmado de 1996 no entra en la estimación, y el EMBI empalmado solo pesa en 1997T4-1998T3.
- **Resultado primario (D4):** una sola definición, Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las utilidades que el BCRA transfiere al Tesoro (FMI, 2026, cuadro 1, nota 4), y el MECON no las publica separadas del resto de las rentas: la serie sin rentas es la única pública que las deja afuera. La serie con rentas es robustez.
- **PIB real:** INDEC base 1993 empalmada a base 2004 para 1996-2003 con un coeficiente de enlace (k = 1,751); el empalme cambia el nivel, no las tasas de crecimiento. Serie original, sin desestacionalizar, con binarias estacionales.

**Empalmes y por qué son correctos.** El EMBI tiene serie diaria pública desde el 11 de diciembre de 1998, y el TCRM del BCRA empieza en enero de 1997. Para cubrir la ventana se hicieron dos empalmes, con código propio (`codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py`) y validación en el Apéndice A.2 y la Figura A.1.

- **EMBI 1996T1-1998T3.** Se usa el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA y la tasa de fondos federales. Con la Convertibilidad, lo que pagaba un banco en la Argentina por un dólar prestado, por encima de la tasa de Estados Unidos, medía el riesgo argentino. La relación se estima en la superposición 1998T4-2001T3, doce trimestres que terminan antes del corralito: EMBI = 550,3 + 1,171 × diferencial, R² = 0,89, correlación 0,944.
- **Validación del EMBI.** Dejando un trimestre afuera por vez, el error típico es de 102 puntos básicos, contra un desvío del EMBI de 240. Estimando solo con 1998T4-2000T4 y pronosticando 2001, el empalme da 744, 801 y 1.033 contra 750, 973 y 1.469 observados: acierta el nivel y subestima el salto de la crisis. Si sesga, atenúa la volatilidad y las probabilidades quedan del lado conservador.
- **TCRM 1996.** Se encadena con las variaciones del tipo de cambio real efectivo amplio del BIS (invertido). Las variaciones trimestrales de los dos índices tienen una correlación de 0,92 en todo el período común y de 0,98 en 1997-2001. Como la estimación empieza en 1998T2, el TCRM de 1996 no entra en el SVARX; solo lo usa la variante a la manera del FMI, para la depreciación real de 1997.
- **Variante sin empalme.** Con datos desde 1999, solo con el EMBI observado, la probabilidad de no estabilización en 2031 es 29,5% [22,5; 36,7], contra 27,7% [20,6; 34,7] con la ventana completa. H1a (95,7 puntos) y el efecto de la senda de la FED sobre la probabilidad (18,0 puntos) no cambian.
- **Lo que había antes.** La base anterior tenía valores del EMBI de 1993-1998 escritos a mano, sin fuente. Se eliminaron y no se usan.

**Tasa de la FED (D5).** Tasa de fondos federales, con la tasa sombra de Wu y Xia (2016) en el límite cero. La serie cambia de tramo cuatro veces: entra al límite cero en 2009T1 y 2020T2 y sale en 2016T1 y 2022T1. En esas cuatro transiciones la variación se calcula con la tasa efectiva en los dos trimestres. Sin esa corrección, la variación de 2009T1 salía positiva (+0,24) cuando la FED estaba bajando la tasa: era la diferencia entre dos series, no un cambio de política. Desvío estándar de la variación trimestral: 0,501 puntos.

**Controles.** La identidad reproduce la senda de deuda del FMI con un desvío máximo de 0,12 puntos.

### Paso 3. El modelo: un SVARX

- **Variables:** cuatro endógenas (resultado primario, crecimiento, EMBI, TCRM). Exógenas: variación de la tasa de la FED (rezagos 0 a 2), VIX, binarias estacionales, binarias de quiebre (2006T2 y 2018T1) y siete binarias por mandato presidencial. La deuda rezagada entra en todas las ecuaciones.
- **Por qué un VAR:** las cuatro variables se determinan juntas; es la arquitectura del abanico estocástico de Celasun et al. (2006), que el FMI incorporó a su marco de 2021.
- **Por qué la FED y el VIX son exógenos:** Argentina es una economía pequeña y abierta (Cushman y Zha, 1997; Canova, 2005).
- **Por qué en niveles:** las estimaciones son consistentes sin imponer cointegración (Sims et al., 1990), y Bohn (2007) muestra que la ausencia de cointegración no prueba insostenibilidad. Las pruebas de raíz unitaria son ambiguas para la deuda, el EMBI y el TCRM, y Johansen no rechaza rango cero (traza 42,7 contra 47,9). La inferencia se hace con *bootstrap*.
- **Binarias presidenciales.** Una por mandato, con Menem como referencia: De la Rúa, Duhalde, N. Kirchner, C. Fernández de Kirchner, Macri, A. Fernández y Milei. Cada trimestre se asigna al presidente en funciones al cierre, salvo 2001T4, que terminó con presidentes interinos y se asigna a Duhalde. Las pruebas de Wald las rechazan conjuntamente en las ecuaciones del resultado primario (p = 0,014), del EMBI (p < 0,001) y del TCRM (p = 0,005), no en la del crecimiento (p = 0,127); la razón de verosimilitud del sistema, con la corrección de Sims (1980), da p < 0,001. El quiebre de 2001T4 coincide con el inicio del gobierno de Duhalde, así que lo reemplazan las binarias.
- **Rezagos (D3).** Regla: criterio de Schwarz entre los órdenes estables (Ivanov y Kilian, 2005, para datos trimestrales con menos de 120 observaciones); si sus residuos están autocorrelacionados, el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1, con autocorrelación (p < 0,001). Con las binarias y la FED corregida, ningún orden estable pasa el Portmanteau al 5%, así que se aplica la regla de reserva: el orden estable, no menor que el de Schwarz, con el mayor p-valor, que es 2 (p = 0,031), el mismo que elige Hannan-Quinn. Autovalor máximo 0,776. La autocorrelación residual leve se declara como limitación, y se informan 1 y 3 rezagos como robustez.

### Paso 4. Identificación de los *shocks*

- **Nombre (D2b):** restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto. Siempre con estas palabras.
- **Fiscal:** se descuenta la respuesta automática al ciclo con una elasticidad de 0,25 (Blanchard y Perotti, 2002; Girouard y André, 2005).
- **Actividad:** puede responder al *shock* fiscal en el trimestre.
- **Bloque cambiario y de riesgo:** el EMBI y el TCRM sin orden entre sí; solo se interpreta el efecto conjunto. El resultado primario y el crecimiento no responden en el trimestre a ese bloque.
- **Robusteces:** dos ordenamientos de Cholesky (resultado primario primero y resultado primario último), con sus matrices de impacto en el Apéndice A.7, y elasticidades de 0 y 0,5.
- **Dato clave:** la identificación no cambia la estimación central de la probabilidad (27,7% en 2031 con la métrica anual y 3,1% con la definición del FMI, con cualquier identificación), porque los *shocks* estructurales reconstruyen los mismos residuos. Los intervalos cambian levemente, porque en cada réplica la matriz S se reestima. La identificación hace falta para repartir la varianza por bloque, que es la condición (i) de H1a.

### Paso 5. Retroalimentación entre la deuda y las variables

La deuda rezagada entra en las cuatro ecuaciones y se acumula con la identidad (Favero y Giavazzi, 2007). En la simulación se actualiza al cierre de cada año, porque la identidad del FMI es anual.

- **Reacción fiscal:** coeficiente de impacto 0,0466 [0,0231; 0,0835] y multiplicador de largo plazo 0,079 [0,062; 0,147], del orden del 0,05 de Bohn (1998). Con 0,079 la regla estabiliza la deuda solo si (r − g)/(1 + g) queda por debajo de unos ocho puntos, y en los años de estrés la depreciación real lleva el diferencial muy por encima.
- **Deuda y EMBI:** unos 35 puntos básicos por punto de deuda, [13,9; 47,6]. Ojo: sin las binarias presidenciales el intervalo incluye el cero (15,3 [-5,3; 30,4]). Se presenta como un resultado sujeto a la especificación.
- **Sin retroalimentación**, la probabilidad en 2031 casi no cambia con la métrica anual (27,2%); con la definición del FMI baja de 3,1% a 1,3%.

### Paso 6. Inferencia

- **Estimación central (D8):** parámetros de MCO y 20.000 trayectorias; error de Monte Carlo de 0,32 puntos.
- **Intervalos de 90%:** *bootstrap* de bloques móviles de cuatro trimestres sobre los residuos, recursivo, con la deuda regenerada (Brüggemann et al., 2016), y percentiles de Hall (1992). 1.000 réplicas con 1.000 trayectorias cada una: con 200, cada cola del intervalo de 95% de Bonferroni quedaba definida por unas cinco observaciones. Para las participaciones de la varianza, que están acotadas, los intervalos son percentiles simples.
- **Por qué no el *bootstrap* salvaje:** no reproduce la estructura de cuarto orden de las innovaciones (Brüggemann et al., 2016). Los bloques preservan la heterocedasticidad condicional, que aparece en la ecuación del TCRM (ARCH p < 0,001).
- **Números aleatorios comunes:** todas las especificaciones usan los mismos.
- **Corrección de sesgo de Kilian (1998):** robustez, 29,1% en 2031.

### Paso 7. Simulación

1. **Escenario base del FMI (2026, cuadro 6):** crecimiento, deflactor, tasa efectiva, resultado primario, ajuste *stock*-flujo e inflación relativa.
2. **Desvíos:** el SVARX se simula 40 trimestres en desvíos respecto del escenario, con los *shocks* estructurales remuestreados por fecha en bloques de ocho trimestres (D7), como los bloques de dos años del FMI. Las binarias no intervienen en la proyección.
3. **Variables externas (D6):** el VIX y el nivel de la tasa de la FED siguen procesos AR(1) (0,703 y 0,972); sus innovaciones se remuestrean junto con los *shocks*. La varianza tiene un cuarto bloque, externo.
4. **Identidad (D9):** separa moneda local (proporción en pesos 0,422, fija como en el FMI) y extranjera; la tasa en dólares se reprecia con λ = 0,282 por año.
5. **Métricas (D9 y D16):** (a) anual: la deuda no se estabiliza en T si el resultado primario del escenario es menor que pb* = d(T−1)(M(T) − 1) + sf(T) + ri(T), es decir, si con ese resultado la deuda sube en T (FMI, 2021, párr. 53, aplicado año por año); (b) definición operativa del FMI (FMI, 2022, recuadro 3): el mismo cálculo sin tipo de cambio real ni ajuste *stock*-flujo, con los impulsores del escenario en T más el *shock* promedio de 2026 a T. La lectura literal del recuadro, que promedia también el escenario, da todavía menos (0,0% y 0,9%).
6. **Escenarios de la FED:** (i) nivel 0,501 puntos más alto en forma permanente desde 2026T1; (ii) repetición de la senda de 2022-2025 en 2026-2029: sube 5,25 puntos, baja 1,43 y desde 2030 queda 3,82 por encima del base.
7. **Descomposición de la varianza:** para cada bloque se simula la deuda de 2035 solo con sus *shocks* y se calcula la varianza; la participación es esa varianza sobre la suma de las de los cuatro bloques. El bloque externo se abre en VIX, FED y FED solo con su efecto directo. Las aperturas no suman.

### Paso 8. Resultados

- **H1b: no respaldada (se decide con la definición del FMI).** Métrica anual, como complemento: 27,7% [20,6; 34,7] en 2031 y 29,0% [25,0; 36,1] en 2035, contra 1% y menos de 3% del FMI; con Bonferroni, límites inferiores de 19,0 y 24,1; se cumple en las 21 especificaciones (menor límite inferior: 16,2 en 2031, con tres rezagos; 18,0 en 2035, sin ajuste *stock*-flujo y con el escenario de 2025). Definición operativa del FMI: 3,1% [0,0; 6,3] en 2031 y 5,1% [0,0; 10,2] en 2035; la estimación central supera la del FMI pero el intervalo la incluye; el límite inferior supera la cifra del FMI solo en 2 de 21 (consolidada y canal de tasas en pesos). **Veredicto: no respaldada.** Con la anual la supera, pero eso mide el riesgo de valuación anual, no prueba que el FMI subestime. Medidas alternativas: con el resultado primario simulado, 29,7%; probabilidad de que la deuda de 2031 supere a la de 2029, 20,0% [17,3; 26,7].
- **H1a: no respaldada; se cumple (i) y no (ii).** (i) No fiscal menos fiscal: 96,8 puntos [90,8; 99,8]. Reparto de la varianza en 2035: externo 59,4%, cambiario y de riesgo 28,3%, actividad 10,7%, fiscal 1,6%. Sin binarias presidenciales: 77,9 [67,3; 99,4]. Se cumple en las 20 especificaciones en que se informa (en la consolidada no se informa). (ii) Suficiencia, métrica anual: con un desplazamiento uniforme que lleva el resultado primario de 2031 a su máximo de 1996-2025 (3,29% en 2004; el de 2026 queda en 2,39%), la probabilidad en 2031 es 23,0% (21,6% con el máximo con rentas, 3,58%); para llevarla al 1% hay que sumar 7,25 puntos todos los años (8,65% del PIB en 2026 y 9,55% en 2031). Con la definición del FMI, en el máximo histórico baja a 0,9%: **no se cumple**; alcanza con sumar 1,00 punto.
- **H2, parcialmente respaldada con las dos métricas.** Senda de 2022-2025: +18,4 puntos de probabilidad en 2035 [6,3; 29,1], que resiste Bonferroni [4,1; 30,8] y 20 de 21 especificaciones; con la definición del FMI, +17,1 [0,6; 32,6], que no resiste Bonferroni. +19,3 de deuda [-0,3; 31,3], que no excluye el cero (la deuda no depende de la métrica). Nivel 0,501 más alto: +1,9 de probabilidad [0,3; 3,2] y +2,0 de deuda [0,4; 3,2], pequeños y sin resistir Bonferroni. El 77% del efecto de la senda sobre la deuda (14,8 de 19,3 puntos) es el costo directo de la deuda en dólares. Sin binarias presidenciales, el efecto de la senda es la mitad: +9,7 puntos de probabilidad.
- **Extensión consolidada, exploratoria.** 31,1% [27,6; 41,5] en 2031 y 35,0% [32,3; 49,8] en 2035; la senda de la FED suma 19,2 puntos. No se informan la varianza ni la deuda media porque 368 de las 1.000 réplicas tienen trayectorias explosivas.

## Parte 2. Qué cambió y por qué

### Revisión de octubre de 2026 (decisiones D1 a D15)

| Problema de la versión anterior | Decisión | Resultado |
|---|---|---|
| La comparación con el FMI mezclaba perímetros | D1: deuda federal bruta como principal, con punto de partida y escenario del FMI | H1b compara la misma deuda |
| EMBI de 1993-1998 escrito a mano y TCRM de 1996 sin método | D2: ventana 1996-2025 con empalmes documentados y validados | Con datos desde 1999, 29,5% en 2031 contra 27,7% |
| Período y nombres distintos entre documentos | D2b: reglas de consistencia y control automático | Un solo período y un solo nombre para cada variable |
| Regla de rezagos sin respaldo y cita de Ivanov y Kilian mal usada | D3: Schwarz más adecuación de residuos, con regla de reserva | 2 rezagos; autocorrelación leve declarada |
| Resultado primario con utilidades del BCRA, justificado con una definición falsa del FMI | D4: una sola definición, sin rentas | Con rentas, 28,5% en 2031 |
| Saltos de la FED por cambio de serie | D5: las cuatro transiciones con la tasa efectiva | Desvío 0,501 sin cambios de serie |
| VIX y FED fijos en la simulación | D6: procesos AR(1) | Bloque externo en la varianza |
| Remuestreo independiente con residuos autocorrelacionados | D7: bloques de ocho trimestres | Conserva la autocorrelación remanente |
| Intervalos descentrados | D8: MCO, bloques y Hall; 1.000 réplicas | Colas del 95% bien definidas |
| Criterio de H1a cambiado después de estimar | D10: criterio original de varianza más la condición de suficiencia | H1a con dos condiciones explícitas |
| H1b sin perímetro común | D11 | Se cumple en las 21 especificaciones |
| H2 sin horizonte fundado | D12: 2035 | Parcialmente respaldada, con regla escrita |
| Las binarias presidenciales cambian la magnitud de H2 | D15: se mantienen en la principal; la variante sin ellas se informa | Efecto de la senda: 18,4 con binarias, 9,7 sin ellas |
| La tesis decía usar "la misma métrica" que el FMI y no era así | D16: la definición operativa del FMI decide el contraste; la métrica anual queda como complemento | H1b y H1a (ii) no respaldadas |

### Cambios del equipo del 15/10 (lista de cambios A1 a E)

Ventana extendida a 1996 (A1) con empalmes (A2); fechas unificadas (A3); deuda consolidada desde 2002 (A4); binarias presidenciales (A5); matrices de Cholesky en el Apéndice (A6); hipótesis alineadas con sus criterios (B1 a B3); coeficiente fiscal, identificación, intervalos, descomposición, réplicas, quiebres y tasa sombra explicados (C1 a C8); inconsistencias numéricas y de redacción (D1 a D6); forma y referencias (E).

## Parte 3. Preguntas probables del jurado y respuesta

### Sobre la comparación con el FMI

1. **"¿Cómo puede dar 27,7% si el FMI dice 1%?"** Porque el 27,7% usa otra métrica. Con la definición operativa del FMI, la nuestra da 3,1% [0,0; 6,3]: del mismo orden que el 1% y estadísticamente indistinguible. El 27,7% es la métrica anual: pregunta si la deuda sube un año determinado, incluida la valuación de la deuda en dólares; la del FMI promedia los *shocks* de toda la trayectoria y deja afuera el tipo de cambio real. Lo decimos en la tesis y damos los dos resultados con el mismo peso. Dato extra: con el procedimiento de *shocks* del propio FMI sobre la historia argentina y su misma definición, da 29,1%, así que la historia argentina no da 1%; el SVARX da poco con la definición del FMI porque sus *shocks* son sorpresas, más chicas que los desvíos respecto de una media histórica.
1b. **"¿Entonces cuál métrica es la correcta?"** La comparación estricta con el FMI es su definición operativa. La anual tiene un argumento propio: con 57,8% de la deuda en moneda extranjera, una depreciación real de un año cambia mucho la deuda, y promediar la trayectoria lo esconde. Por eso la del FMI decide el contraste, porque es con la que se calculan las cifras con que comparamos, y la anual queda como complemento: muestra cuánto del riesgo viene de la valuación anual de la deuda en dólares.
2. **"Comparan un intervalo con una cifra puntual."** Sí, y lo decimos (sección 7.1). La cifra del FMI no tiene intervalo público e incluye juicio del equipo técnico. Por eso H1b contrasta si el valor del FMI queda fuera del rango que sostienen los datos con su propio escenario, no si el FMI está equivocado.
3. **"Su métrica anual se activa con un solo mal año."** Es cierto: dice que la deuda no se estabiliza en T si sube ese año, aunque la tendencia de varios años siga siendo descendente. Por eso informamos también la definición del FMI (3,1%) y una medida intermedia, que exige que la deuda suba en dos años: la probabilidad de que la deuda de 2031 supere a la de 2029 es 20,0% [17,3; 26,7]. Y la mediana simulada baja de 80,3% a 52,9% en 2031: no decimos que la deuda vaya a explotar.
4. **"Su abanico es más angosto que el del FMI y la probabilidad es mayor. ¿No es contradictorio?"** No. El ancho mide la dispersión acumulada (40,5 puntos contra 71,5); la métrica anual mira la volatilidad de un año. Con más de la mitad de la deuda en moneda extranjera, basta un año de depreciación real para que la deuda suba ese año. Con la definición del FMI, que promedia la trayectoria, la probabilidad es chica (3,1%), coherente con un abanico más angosto.

### Sobre los datos

5. **"El EMBI de 1996-1998 es inventado."** Sale de un empalme con series oficiales, validado: R² de 0,89, error típico de 102 puntos básicos dejando un trimestre afuera, y un pronóstico fuera de muestra de 2001 que acierta el nivel. Y los resultados no dependen de él: con datos desde 1999, 29,5% contra 27,7%.
6. **"¿Por qué la consolidada da más que la federal, si tiene menos deuda en dólares?"** Primero, una precisión: tiene menos deuda en dólares en puntos del PIB, pero una proporción mayor (68,5% contra 57,8% de la federal). Porque las dos estimaciones usan muestras distintas (la consolidada desde 2002) y órdenes de rezagos distintos, y en la consolidada 368 de 1.000 réplicas tienen trayectorias explosivas. Por eso la presentamos como exploratoria: solo respalda el orden de magnitud.
7. **"No descuentan el FGS."** En la serie histórica consolidada, no, porque no hay una serie pública que separe esas tenencias para todo el período. La simulación de la extensión parte del *stock* del FMI, que sí lo descuenta. La especificación principal no se ve afectada.
8. **"¿Por qué sin rentas de la propiedad?"** Porque el FMI excluye las utilidades del BCRA y el MECON no las separa. Lo detectamos nosotros: la versión anterior usaba la serie con rentas con una justificación incorrecta. Con rentas, 28,5% en 2031: casi no cambia.

### Sobre el modelo

9. **"Hay autocorrelación en los residuos."** Leve, con p = 0,031 en el Portmanteau con dos rezagos, y ningún orden estable la elimina en esta muestra. Por eso la remuestreamos en bloques (ocho trimestres en la simulación, cuatro en el *bootstrap*), que conservan la autocorrelación remanente, e informamos uno y tres rezagos: 29,4% y 25,9% en 2031.
10. **"Siete binarias presidenciales en cuatro ecuaciones con 111 trimestres es mucho."** Consumen grados de libertad, y lo declaramos. Pero las pruebas de Wald y de razón de verosimilitud rechazan que no importen (p < 0,001 en el sistema). Su peso es real: sin ellas, el efecto de la senda de la FED se reduce a la mitad (9,7 puntos) y la participación fiscal sube. H1a y H1b no cambian. No intervienen en la proyección porque la simulación es en desvíos.
11. **"La binaria de Milei tiene nueve trimestres."** Sí: su coeficiente es de nivel y está estimado con pocas observaciones. No afecta la proyección, porque las binarias no entran en los desvíos.
12. **"La elasticidad de 0,25 es de la OCDE."** Solo afecta el reparto de la varianza, no la probabilidad. Las unidades son compatibles en el trimestre del impacto, y con 0 y 0,5 la diferencia no fiscal menos fiscal es 85,6 y 99,4, siempre excluyendo el cero.
13. **"El resultado primario podría responder en el trimestre al tipo de cambio (derechos de exportación)."** Puede, aunque el efecto debería ser chico porque la recaudación llega con rezago. Por eso el ordenamiento de Cholesky con el resultado primario último, que lo permite, tiene el mismo peso: da 99,4 puntos en H1a y la misma probabilidad.
14. **"Los quiebres de Bai y Perron sobre una serie tan persistente pueden ser espurios."** Pueden; los aceptamos porque la deuda tuvo cambios de nivel discretos y de origen conocido, y sin ellos la probabilidad en 2031 es 27,1%.
15. **"La identificación no cambia la probabilidad: ¿para qué sirve?"** Para repartir la varianza por bloque, que es la condición (i) de H1a, y para definir el *shock* fiscal. Que la probabilidad no cambie es una propiedad: los *shocks* estructurales reconstruyen los mismos residuos.

### Sobre los resultados

16. **"La participación fiscal de 1,6% es inverosímil."** No mide la importancia de la política fiscal, sino cuánta incertidumbre viene de sorpresas del resultado primario respecto del escenario. Además, parte de esa variación la absorben las binarias presidenciales: sin ellas la diferencia es 77,9 puntos. Lo robusto es el orden de magnitud.
17. **"El VIX solo explica 113%: ¿cómo puede pasar 100%?"** Porque las aperturas del bloque externo usan como base la suma de las varianzas de los cuatro bloques y no son aditivas: los *shocks* se remuestrean por fecha, los picos del VIX coinciden con los recortes de la FED de 2008 y 2020, y la deuda que generan uno y otro por separado se mueve en sentidos opuestos, así que juntos explican menos que el VIX solo. Lo que importa es que el costo directo de la FED es una parte menor (7,6%).
18. **"¿H2 se cumple o no?"** Parcialmente, con las dos métricas y con la regla escrita en la Tabla 4.4: el efecto de la senda sobre la probabilidad se cumple (18,4 con la anual, 17,1 con la del FMI), resiste Bonferroni con la anual y 20 de 21 especificaciones, aunque su magnitud depende de las binarias y de λ (de 11,1 a 23,0); el efecto sobre la deuda esperada no excluye el cero por un margen mínimo; y el 77% del efecto sobre la deuda es el costo directo de la deuda en dólares, que la identidad incorpora. Los canales domésticos se verifican solo en parte, con el EMBI de cuatro a seis trimestres después.
19. **"Con 84 respuestas al impulso, 11 significativas es azar."** Casi: el azar daría unas ocho con intervalos de 90%. Por eso no nos apoyamos en ninguna respuesta aislada. El patrón del EMBI (sube cuatro a seis trimestres después) es coherente con la teoría, pero no lo presentamos como prueba.
20. **"Si el superávit no alcanza, ¿qué proponen?"** La tesis no simula cambios en la composición por moneda ni en los plazos de la deuda, así que no evalúa alternativas. Con la métrica anual, llevar la probabilidad al 1% exigiría un superávit cercano al 9% del PIB todos los años, sin precedentes; con la definición del FMI alcanza con el máximo histórico. Lo que no depende de la métrica es que la mayor parte de la incertidumbre viene de *shocks* externos y cambiarios.

### Debilidades que conviene reconocer antes de que las pregunten

- La tesis dijo durante meses que el riesgo era mucho mayor que el del FMI, y con la métrica del FMI no lo es. Si preguntan por qué cambió: detectamos que estábamos comparando con otra métrica, la corregimos y dejamos que el resultado sea el que es. Conviene plantearlo nosotros antes que el jurado.
- Una sola serie trimestral de treinta años: los efectos de la FED y de la retroalimentación tienen intervalos amplios.
- Autocorrelación residual leve (p = 0,031).
- El escenario del FMI se toma como dado; con el de 2025 la probabilidad en 2031 es 25,7%.
- Composición por monedas fija, como en el FMI: si la depreciación eleva la proporción en dólares, el riesgo está subestimado.
- La magnitud de H2 depende de las binarias presidenciales.
- El *shock* de la FED es la variación observada de la tasa, no un *shock* identificado con datos de alta frecuencia (línea futura).
- Endogeneidad del riesgo país (no está en el texto por decisión del director): en series de tiempo todo es endógeno salvo los *shocks* de mayor frecuencia que el sistema; por eso el VIX y la tasa de la FED entran como exógenas.

## Parte 4. Números clave

| Número | Qué es |
|---|---|
| 80,3% del PIB | Deuda federal bruta del FMI a fines de 2025, punto de partida (serie propia: 77,7%) |
| 52,1% del PIB | Deuda consolidada con el BCRA del FMI a fines de 2025 (extensión) |
| 1996-2025; 2026-2035 | Ventana del estudio y proyección |
| 1998T2-2025T4, 111 trimestres | Muestra de estimación |
| R² = 0,89; 102 pb | Empalme del EMBI: ajuste en la superposición y error típico dejando un trimestre afuera |
| 2 rezagos; p = 0,031 | Orden elegido y Portmanteau |
| 0,776 | Autovalor máximo del VAR principal |
| 0,0466 y 0,079 | Reacción fiscal de impacto y de largo plazo |
| 27,7% [20,6; 34,7] | No estabilización en 2031, métrica anual (FMI: 1%) |
| 29,0% [25,0; 36,1] | No estabilización en 2035, métrica anual (FMI: menos de 3%) |
| 3,1% [0,0; 6,3] y 5,1% [0,0; 10,2] | No estabilización en 2031 y 2035, definición operativa del FMI |
| 0,9% | H1a (ii) con la definición del FMI: probabilidad en 2031 con el máximo histórico |
| 29,1% | *Shocks* a la manera del FMI con su definición, 2031 |
| 57,8% | Deuda federal bruta en moneda extranjera |
| 19,0 y 24,1 | Límites inferiores con Bonferroni, 2031 y 2035 |
| 20,0% | Probabilidad de que la deuda de 2031 supere a la de 2029 |
| 96,8 [90,8; 99,8] | H1a (i): no fiscal menos fiscal; 77,9 sin binarias presidenciales |
| 59,4 / 28,3 / 10,7 / 1,6 | Varianza de 2035: externo / cambiario y de riesgo / actividad / fiscal (%) |
| 3,29% | Máximo del resultado primario sin rentas 1996-2025 (2004) |
| 23,0% | H1a (ii), métrica anual: probabilidad en 2031 con el resultado primario de 2031 en ese máximo |
| +7,25 puntos | Desplazamiento necesario para llevar la probabilidad de 2031 al 1% |
| +18,4 [6,3; 29,1] | Senda de la FED: efecto sobre la probabilidad en 2035 (pp) |
| +19,3 [-0,3; 31,3] | Senda de la FED: efecto sobre la deuda en 2035 (pp del PIB) |
| 14,8 de 19,3 (77%) | Costo directo de la deuda en dólares en el efecto de la senda |
| 9,7 | Efecto de la senda sobre la probabilidad sin binarias presidenciales |
| 0,501 | Desvío estándar de la variación trimestral de la tasa de la FED |
| 24,1% | No estabilización en 2031 con *shocks* a la manera del FMI, métrica anual |
| 40,5 contra 71,5 | Ancho del abanico en 2031: nuestro contra el del FMI |
| 31,1% | Extensión consolidada, 2031 (exploratoria) |
| 21 | Especificaciones del SVARX |
| 1.000 | Réplicas del *bootstrap* |
