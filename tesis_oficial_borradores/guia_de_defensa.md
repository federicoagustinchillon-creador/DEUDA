# Guía de defensa: qué hicimos, por qué y qué nos pueden discutir

Documento interno del grupo. No forma parte de la tesis. Resume cada paso del trabajo empírico con su justificación, según la versión del modelo reestimada con la ventana 1996-2025 (17/10/2026; decisiones D1 a D14), las críticas que se resolvieron y las que todavía puede hacer un jurado, con la respuesta. Todos los números salen de la hoja de números y del Apéndice.

## Parte 1. Qué hicimos, paso a paso

### Paso 1. Pregunta e hipótesis

- **H1a:** los determinantes condicionan la sostenibilidad y el superávit, por sí solo, no basta para estabilizar la deuda. Criterio, el original: la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del *shock* fiscal, con un intervalo de 90% que excluye el cero.
- **H1b:** nuestra probabilidad de no estabilización de la deuda federal bruta es mayor que la del FMI para esa misma deuda en 2031 y en 2035. Criterio: el límite inferior del intervalo de 90% supera 1% y 3%; se informa Bonferroni por los dos horizontes (95%).
- **H2:** un endurecimiento de la FED eleva la deuda esperada y la probabilidad de no estabilización. Criterio: el intervalo de 90% de la diferencia con el escenario base excluye el cero en 2035, en la probabilidad y en la deuda; 2031 se informa.
- **Cifras de comparación:** las del análisis de sostenibilidad más reciente del FMI (2026, Artículo IV y segunda revisión): 1% a mediano plazo (2031) y menos de 3% en su abanico de diez años (2035). El 1% es la estimación puntual del FMI para Argentina, no un umbral de riesgo bajo.

### Paso 2. Datos y perímetro

- **Perímetro principal (D1):** deuda federal bruta, el perímetro del FMI. La simulación parte del *stock* del FMI a fines de 2025, 80,3% del PIB (cuadro 2, línea 1). Nuestra serie, construida con datos del MECON, da 77,7%; la diferencia son los intereses capitalizados, la deuda no presentada al canje, los reclamos por los cupones PBI y la medición del PIB.
- **Extensión:** deuda consolidada con el BCRA en la definición del FMI (cuadro 2, línea 5), 52,1% del PIB a fines de 2025, con 68,5% en moneda extranjera. La dinámica se estima con nuestra serie consolidada (Tesoro más BCRA, Letras a valor nominal).
- **Ventana (D2):** 1996-2025 para todo el estudio y 2026-2035 para la proyección, por decisión del grupo. Las ecuaciones se estiman con 1998T2-2025T4, 111 trimestres, porque los primeros trimestres de la ventana son condiciones iniciales de los rezagos: la variación de la tasa de la FED entra con dos rezagos y todos los órdenes hasta seis se comparan sobre los mismos trimestres (Lütkepohl, 2005, sec. 4.3). La ventana del estudio sigue siendo 1996-2025.

**Empalmes y por qué son correctos.** El riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), tiene serie diaria pública desde el 11 de diciembre de 1998, y el índice del tipo de cambio real multilateral (TCRM) del BCRA empieza en enero de 1997. Para cubrir la ventana completa se hicieron dos empalmes, con código propio (`codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py`) y validación en el Apéndice A.2 y la Figura A.1.

- **EMBI 1996T1-1998T3.** Se usa el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA (serie oficial, mensual desde octubre de 1994) y la tasa de fondos federales. Con la convertibilidad, lo que pagaba un banco en la Argentina por un dólar prestado, por encima de la tasa de Estados Unidos, medía el riesgo argentino. La relación se estima en la superposición 1998T4-2001T3, doce trimestres que terminan antes del corralito, que rompe ese mercado: EMBI = 550,3 + 1,171 × diferencial, R² = 0,89, correlación 0,944.
- **Validación del EMBI.** Dejando un trimestre afuera por vez, el error típico es de 102 puntos básicos, contra un desvío del EMBI de 240. Estimando solo con 1998T4-2000T4 y pronosticando 2001, el empalme da 744, 801 y 1.033 contra 750, 973 y 1.469 observados: acierta el nivel y subestima el salto de la crisis. Si sesga, atenúa la volatilidad de 1996-1998, y con eso las probabilidades quedan del lado conservador.
- **TCRM 1996.** Se encadena hacia atrás con las variaciones del tipo de cambio real efectivo amplio del BIS, invertido porque ese índice sube con la apreciación. Las variaciones trimestrales de los dos índices tienen una correlación de 0,92 en todo el período común y de 0,98 en 1997-2001. Con dos rezagos, los cuatro trimestres de 1996 solo intervienen como condiciones iniciales.
- **Variante sin empalme.** Con datos desde 1999, solo con el EMBI observado, la probabilidad de no estabilización en 2031 es 32,4% [26,6; 37,0], contra 31,8% [25,2; 36,4] con la ventana completa. H1a (75,5 puntos [51,7; 86,3]) y H2 (senda de la FED, 9,6 puntos [2,5; 15,7]) no cambian (Apéndice A.9).
- **Lo que había antes.** La base anterior tenía valores del EMBI de 1993-1998 escritos a mano, sin fuente. Se eliminaron y no se usan en ninguna parte. Si el jurado pregunta por versiones viejas, la respuesta es esa.

| Serie | Fuente | Construcción | Por qué así |
|---|---|---|---|
| Deuda federal bruta | MECON; *stock* inicial del FMI (2026) | Deuda bruta de la Administración Central sobre el PIB de los últimos cuatro trimestres | Es la deuda del análisis del FMI |
| Deuda consolidada con el BCRA | MECON y BCRA | Deuda del Tesoro + pasivos remunerados del BCRA − deuda del Tesoro en poder del BCRA − depósitos del Tesoro | Es la consolidación del FMI (2021, anexo II) |
| Resultado primario (D4) | MECON | Flujo trimestral anualizado del Sector Público Nacional, sin rentas de la propiedad, una sola definición para los dos perímetros; con rentas, como robustez | El FMI excluye las utilidades del BCRA de su resultado primario (FMI, 2026, cuadro 1, nota 4) y el MECON no las separa del resto de las rentas |
| PIB real | INDEC | Base 1993 empalmada a base 2004 | La base 2004 empieza en 2004 |
| EMBI | J.P. Morgan, serie diaria publicada por Ámbito Financiero; BCRA y Reserva Federal para el empalme | Promedio trimestral; 1996T1-1998T3 con el empalme validado | Serie diaria desde diciembre de 1998; el empalme usa series oficiales |
| TCRM | BCRA; BIS para el empalme | Promedio trimestral; 1996 encadenado con el BIS | El índice del BCRA empieza en enero de 1997 |
| Tasa de la FED (D5) | FRED y tasa sombra de Wu y Xia (2016) | Sombra en el límite cero; en 2022T1 la variación se calcula con la tasa efectiva en los dos trimestres | En el límite cero la tasa efectiva no refleja la política, y el cambio de serie no es un cambio de política |
| VIX | CBOE | Promedio trimestral | Medida estándar de aversión global al riesgo |

**Controles.** La identidad reproduce la senda de deuda del FMI con un desvío máximo de 0,12 puntos.

### Paso 3. El modelo: un SVARX

- **Variables:** cuatro endógenas (resultado primario, crecimiento, EMBI, TCRM); exógenas: variación de la tasa de la FED (rezagos 0 a 2), VIX, binarias estacionales y binarias de los quiebres de Bai y Perron sobre la deuda (2001T4, 2006T2, 2018T1). La deuda rezagada entra en todas las ecuaciones.
- **Por qué un VAR:** las cuatro variables se determinan juntas; es la arquitectura del abanico estocástico de Celasun et al. (2006).
- **Por qué la FED es exógena:** Argentina es una economía pequeña y abierta (Cushman y Zha, 1997; Canova, 2005).
- **Por qué en niveles:** las estimaciones son consistentes sin imponer cointegración (Sims et al., 1990). Las pruebas de raíz unitaria son ambiguas para la deuda, el EMBI y el TCRM, y Johansen no rechaza rango cero (traza 42,7 contra 47,9). La inferencia se hace con *bootstrap*.
- **Rezagos (D3):** criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1, con residuos autocorrelacionados (p = 0,000); se usan 2 (p = 0,056), el mismo orden que elige Hannan-Quinn. Autovalor máximo 0,896.

### Paso 4. Identificación de los *shocks*

- **Nombre (D2b):** restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto. Siempre con estas palabras.
- **Fiscal:** se descuenta la respuesta automática al ciclo con una elasticidad de 0,25 (Blanchard y Perotti, 2002; Girouard y André, 2005).
- **Actividad:** puede responder al *shock* fiscal en el trimestre.
- **Bloque cambiario y de riesgo:** el EMBI y el TCRM sin orden entre sí; solo se interpreta el efecto conjunto (Christiano et al., 1999). El resultado primario y el crecimiento no responden en el trimestre a ese bloque.
- **Robusteces:** dos ordenamientos de Cholesky (resultado primario primero y resultado primario último), y elasticidades de 0 y 0,5.
- **Dato clave:** la identificación no cambia la probabilidad de no estabilización, porque los *shocks* estructurales reconstruyen los mismos residuos. Con números aleatorios comunes, las identificaciones alternativas dan exactamente la misma probabilidad (31,8% en 2031). La identificación hace falta para dos cosas: repartir la varianza de la deuda por bloque, que es el criterio de H1a, y definir el *shock* fiscal.

### Paso 5. Retroalimentación entre la deuda y las variables

La deuda rezagada entra en las cuatro ecuaciones y se acumula con la identidad (Favero y Giavazzi, 2007). En la simulación se actualiza al cierre de cada año, porque la identidad del FMI es anual. La deuda se asocia con más superávit: coeficiente de impacto 0,0576 [0,0220; 0,0822] y multiplicador de largo plazo 0,199 [0,112; 0,328]. Con el EMBI la estimación es de unos 15 puntos básicos por punto de deuda, con un intervalo que incluye el cero. Sin retroalimentación, la probabilidad en 2031 casi no cambia (30,4%) y el abanico se abre (54,4 puntos contra 46,6).

### Paso 6. Inferencia

- **Estimación central (D8):** parámetros de MCO (autovalor máximo 0,896) y 20.000 trayectorias; error de Monte Carlo de 0,33 puntos.
- **Intervalos de 90%:** *bootstrap* de bloques móviles de cuatro trimestres sobre los residuos, de diseño recursivo, en el que la deuda también se regenera (Brüggemann et al., 2016), con percentiles de Hall (1992), que corrigen el sesgo de la distribución *bootstrap* respecto de la estimación puntual. 200 réplicas con 1.000 trayectorias cada una. Mediana del autovalor máximo en las réplicas: 0,842.
- **Por qué se abandonó el *bootstrap* salvaje:** Brüggemann et al. (2016) muestran que no reproduce la estructura de cuarto orden de las innovaciones de la que dependen las respuestas estructurales.
- **Números aleatorios comunes:** todas las especificaciones usan los mismos, de modo que las diferencias entre filas no vienen del sorteo.
- **Corrección de sesgo de Kilian (1998):** como robustez (30,1% en 2031).

### Paso 7. Simulación

1. **Escenario base del FMI (2026, cuadro 6):** crecimiento, deflactor, tasa efectiva, resultado primario, ajuste *stock*-flujo e inflación relativa, para la deuda a la que corresponde.
2. **Desvíos:** el SVARX se simula trimestre a trimestre con los *shocks* estructurales remuestreados en bloques de ocho trimestres (D7), como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI).
3. **Variables externas (D6):** el VIX y el nivel de la tasa de la FED siguen procesos AR(1) estimados en la muestra (0,703 y 0,970); sus innovaciones se remuestrean junto con los *shocks* estructurales, por fecha. La varianza tiene un cuarto bloque, externo.
4. **Identidad (D9):** separa moneda local (proporción en pesos 0,422, fija como en el FMI) y extranjera; la tasa en dólares se reprecia con λ = 0,282 por año. El ajuste *stock*-flujo se escala por la deuda en pesos simulada y la inflación relativa por la deuda en moneda extranjera. El desvío del crecimiento anual es la variación del promedio anual del nivel del PIB.
5. **Métrica del FMI:** la deuda no se estabiliza en T si el resultado primario del escenario es menor que pb* = d(T-1)(M(T) − 1) + sf(T) + ri(T), el que la estabilizaría incluido el ajuste *stock*-flujo (FMI, 2021, párr. 53).
6. **Escenarios de la FED:** (i) nivel 0,494 puntos más alto en forma permanente desde 2026T1 (un desvío estándar de la variación trimestral); (ii) repetición de la senda trimestral de 2022-2025 en 2026-2029: sube 5,25 puntos, baja 1,43 y desde 2030 queda 3,82 puntos por encima del base hasta 2035.

### Paso 8. Resultados

- **H1a, respaldada.** No fiscal menos fiscal: 78,3 puntos [57,3; 87,9]. Reparto de la varianza en 2035: externo 44,9%, cambiario y de riesgo 32,3%, actividad 12,0%, fiscal 10,8%. Se cumple en las 20 especificaciones (menor límite inferior: 25,6, con elasticidad cíclica 0, una de las variantes de robustez). Complemento descriptivo: con el resultado primario en su máximo de 1996-2025 (3,29% sin rentas, 2004) todos los años, la probabilidad en 2031 es 26,1% (24,5% con el máximo con rentas, 3,58%); para llevarla al 1% haría falta sumar 8,00 puntos (9,4% del PIB en 2026 y 10,3% en 2031).
- **H1b, respaldada.** 31,8% [25,2; 36,4] en 2031 y 31,0% [26,8; 35,6] en 2035; con Bonferroni, límites inferiores de 24,2 y 26,6. Se cumple en las 20 especificaciones (menor límite inferior 19,1, deuda consolidada con el BCRA).
- **H2, respaldada en parte.** Senda 2022-2025: +9,7 puntos de probabilidad en 2035 [4,2; 16,0], robusto, y +9,0 de deuda [0,3; 16,2], no robusto. Nivel 0,494 más alto: +1,1 [0,2; 1,9] y +1,0 [0,0; 1,8]; el efecto sobre la probabilidad no resiste Bonferroni ([-0,0; 2,0]). El 96% del efecto de la senda sobre la deuda es el costo directo de la deuda en dólares; los canales que nombra la hipótesis no se distinguen.

## Parte 2. Qué cambió en la revisión de octubre de 2026

| Problema de la versión anterior | Decisión | Resultado |
|---|---|---|
| La comparación con el FMI mezclaba perímetros | D1: deuda federal bruta como principal, con el punto de partida, el escenario y la métrica del FMI; consolidada con el BCRA como extensión | H1b compara lo mismo con lo mismo |
| EMBI de 1993-1998 escrito a mano sin fuente y TCRM de 1996 sin método documentado | D2: ventana única 1996-2025, con empalmes documentados y validados; los valores a mano se eliminaron | Con datos desde 1999, sin empalme, 32,4% en 2031 contra 31,8% |
| Período de estudio y nombres de variables distintos entre documentos | D2b: reglas de consistencia y control automático (`verificar_consistencia.py`) | Un solo período, un solo nombre para el EMBI y para la identificación |
| Regla de rezagos sin respaldo y cita de Ivanov y Kilian mal usada | D3: Schwarz más adecuación de residuos | 2 rezagos, residuos sin autocorrelación (p = 0,056) |
| Resultado primario con utilidades del BCRA, justificado con una definición del FMI que era falsa | D4: una sola definición, sin rentas de la propiedad, que excluye las utilidades del BCRA como el FMI | Con rentas, como robustez; los resultados casi no cambian |
| Salto de la FED en 2022T1 por cambio de serie | D5: variación con la tasa efectiva en los dos trimestres | El desvío (0,494) no incluye el cambio de serie |
| VIX y FED fijos en la simulación | D6: procesos AR(1) con innovaciones remuestreadas | Bloque externo en la varianza |
| Remuestreo independiente con residuos autocorrelacionados | D7: bloques de ocho trimestres | Conserva la autocorrelación remanente |
| Estimación central casi con raíz unitaria e intervalos descentrados | D8: MCO, *bootstrap* de bloques y percentiles de Hall | Autovalor 0,896; Kilian como robustez |
| Ajuste *stock*-flujo sin escalar y métrica sin él | D9: escalado por moneda y pb* con el ajuste | Identidad y métrica coherentes |
| Criterio de H1a cambiado después de estimar | D10: criterio original | Se cumple en las 20 especificaciones |
| H1b contra el FMI sin perímetro común | D11 | Se cumple en las 20 especificaciones |
| H2 sin horizonte fundado | D12: 2035, porque el efecto se acumula | Se cumple en la principal; robusto solo el efecto de la senda sobre la probabilidad; mecanismo no distinguible |

## Parte 3. Críticas que puede hacer el jurado y respuesta honesta

### Críticas que la versión actual resuelve

1. **"Cambiaron los criterios después de ver los resultados."** Ya no. H1a se contrasta con su criterio original (D10) y H2 mantiene el suyo (D12). Los dos tamaños del *shock* de la FED tienen una justificación externa a los resultados: un desvío estándar, que es la convención de la literatura de VAR, y la repetición del episodio de 2022-2025.
2. **"H1b compara cosas que no son comparables."** Ahora compara lo mismo: perímetro, punto de partida (80,3%), escenario, horizonte y métrica del FMI (D11). Con el procedimiento de *shocks* del FMI aplicado a la historia argentina de la ventana, sobre el mismo perímetro, se obtiene 24,1% en 2031 y un ancho de 148,4, así que tampoco se reproduce el 1%. La diferencia viene de la distribución de *shocks* que usa el FMI, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). No atribuimos la brecha a una causa que no podemos verificar.
3. **"La estimación central es casi una raíz unitaria."** Ya no. La estimación central usa MCO, con autovalor máximo 0,896; la mediana de las réplicas es 0,842. Los percentiles de Hall corrigen el sesgo de la distribución *bootstrap*. La corrección de Kilian (1998) queda como robustez y da 30,1% en 2031.
4. **"La regla de rezagos es ad hoc."** La regla tiene respaldo citado: Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones, y adecuación de residuos (Lütkepohl, 2005, sec. 4.4). La versión anterior citaba a Ivanov y Kilian para el AIC, y esa cita era incorrecta. Con 1 y 3 rezagos la probabilidad en 2031 es 31,4% y 30,0%.
5. **"Hay autocorrelación residual y remuestrean como si no la hubiera."** Con 2 rezagos los residuos no rechazan la ausencia de autocorrelación (p = 0,056). La simulación remuestrea en bloques de ocho trimestres y la inferencia usa bloques móviles de cuatro, que conservan la autocorrelación remanente.
6. **"Usan un *bootstrap* salvaje sin heterocedasticidad condicional."** Se abandonó. Las pruebas ARCH no rechazan al 5% (en la principal, p entre 0,108 y 0,996), y Brüggemann et al. (2016) muestran que el *bootstrap* salvaje no reproduce la estructura de cuarto orden de las innovaciones.
7. **"El resultado primario incluye las utilidades del BCRA."** Ya no. La versión anterior usaba para la deuda federal el resultado primario con rentas de la propiedad y lo justificaba como la definición del FMI. Era falso: el FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4). Lo detectamos nosotros en la lectura final. Como el MECON no publica esas transferencias separadas del resto de las rentas de la propiedad, la única serie pública que las deja afuera es la que excluye todas las rentas. Por eso la tesis usa una sola definición, sin rentas, para los dos perímetros (D4); en el consolidado esas utilidades también son un flujo interno. La serie con rentas queda como robustez. El costo de la corrección es mínimo: la probabilidad de 2031 es 31,8% [25,2; 36,4] sin rentas, y las conclusiones de H1a, H1b y H2 no cambian (Apéndice A.9). Si el jurado pregunta por qué no se separan solo las utilidades, la respuesta es que la fuente pública no lo permite y que excluir todas las rentas es el criterio más cercano al del FMI que se puede replicar.
8. **"El escenario del FMI es para otra deuda."** Ahora se aplica a la deuda para la que fue construido, y la identidad reproduce la senda del FMI con un desvío máximo de 0,12 puntos.
9. **"El EMBI de 1996-1998 es inventado."** El EMBI de 1996T1-1998T3 sale de un empalme con series oficiales (la tasa interfinanciera en dólares del BCRA menos la tasa de fondos federales), estimado en la superposición 1998T4-2001T3 con R² = 0,89, error típico de 102 puntos básicos dejando un trimestre afuera y un pronóstico fuera de muestra de 2001 que acierta el nivel. Con datos desde 1999, solo con el EMBI observado, la probabilidad en 2031 es 32,4% contra 31,8%, y H1a y H2 no cambian. Los valores de 1993-1998 escritos a mano de la base anterior se eliminaron.
10. **"La identificación no aporta nada a la probabilidad."** Es así por construcción, y la tesis lo dice: las identificaciones alternativas dan exactamente la misma probabilidad. La identificación sigue siendo necesaria para repartir la varianza por bloque, que es el criterio de H1a, y para definir el *shock* fiscal. Con los dos ordenamientos de Cholesky de robustez el reparto cambia (60,7 y 91,9 puntos), y el criterio de H1a se cumple en todas las variantes.
11. **"La elasticidad de 0,25 es de la OCDE."** Solo afecta el reparto de la varianza. Con 0 y 0,5 la diferencia no fiscal menos fiscal es 60,7 y 94,4, y las dos excluyen el cero.
12. **"El abanico se angostaba porque el VIX y la FED quedaban fijos."** Ahora se simulan con sus procesos AR(1), y el bloque externo explica 44,9% de la varianza en 2035.

### Debilidades que siguen y cómo responderlas

1. **El mecanismo de H2 no aparece.** Solo 2 de 84 intervalos de respuesta excluyen el cero, los dos del TCRM y con signo de apreciación. El 96% del efecto de la senda sobre la deuda en 2035 es el costo directo de la deuda en dólares, que la identidad incorpora (8,6 de 9,0 puntos). H2 se respalda en el efecto de la senda sobre la probabilidad; sus canales no se distinguen.
2. **El efecto sobre la deuda esperada y el del desvío estándar no son robustos.** Con Bonferroni (95%), el efecto sobre la deuda no excluye el cero en ningún escenario ([-0,5; 2,0] y [-4,1; 17,4]), y el del desvío estándar sobre la probabilidad tampoco ([-0,0; 2,0]). Solo el efecto de la senda sobre la probabilidad lo excluye ([3,6; 16,8]). En las robusteces, el efecto de la senda sobre la probabilidad excluye el cero en 18 de 20 especificaciones (no con datos desde 2004 ni con la corrección de Kilian); sobre la deuda, en 9 de 20.
3. **Retroalimentación al cierre del año.** Dentro del año, la deuda que entra en las ecuaciones es la del cierre del año anterior. Es coherente con la identidad anual del FMI, pero pierde la reacción dentro del año.
4. **Composición por monedas fija.** La proporción en pesos no cambia en la simulación, aunque una depreciación la cambiaría. Es el mismo supuesto del FMI (2021, anexo VI, párr. 6).
5. **El escenario del FMI se toma como dado.** No construimos un escenario propio. Con el escenario del FMI de 2025 la probabilidad en 2031 es 29,4%, y con el ajuste *stock*-flujo en cero, 28,9%.
6. **La extensión consolidada usa el escenario del FMI con flujos escalados.** El ajuste *stock*-flujo y la inflación relativa se escalan por la deuda en pesos y en moneda extranjera de ese perímetro, pero el escenario se construyó para la deuda federal.
7. **El FGS no se descuenta en la serie histórica consolidada.** La simulación de la extensión parte del *stock* del FMI, que sí lo descuenta, pero la dinámica se estima con una serie que no lo hace.
8. **Muestra pequeña.** Son 111 trimestres para cuatro ecuaciones con dos rezagos, la deuda, las exógenas y las binarias.
9. **El empalme del EMBI atenúa la crisis.** En el pronóstico fuera de muestra subestima el salto de 2001 (1.033 contra 1.469 en 2001T3). Si sesga, atenúa la volatilidad de 1996-1998 y vuelve conservadoras las probabilidades, y la variante con datos desde 1999 da casi lo mismo.
10. **Se rechaza la normalidad** (p = 0,000). La simulación y el *bootstrap* remuestrean los residuos empíricos y no suponen normalidad, pero los errores estándar de MCO del Apéndice son solo referencia.
11. **Fechas de quiebre estimadas sobre la deuda.** Los quiebres de Bai y Perron se estiman con la serie de deuda y entran en todas las ecuaciones. Sin esas binarias la probabilidad en 2031 es 30,5%.
12. **Endogeneidad del riesgo país** (no está en el texto por decisión del director): en series de tiempo todo es endógeno salvo los *shocks* de mayor frecuencia que el sistema; por eso el VIX y la tasa de la FED entran como exógenas.

## Parte 4. Números clave

| Número | Qué es |
|---|---|
| 80,3% del PIB | Deuda federal bruta del FMI a fines de 2025, punto de partida (serie propia: 77,7%) |
| 52,1% del PIB | Deuda consolidada con el BCRA del FMI a fines de 2025 (extensión) |
| 1996-2025 | Ventana del estudio; proyección 2026-2035 |
| 1998T2-2025T4, 111 trimestres | Trimestres con que se estiman las ecuaciones (los anteriores son condiciones iniciales) |
| R² = 0,89; 102 pb | Empalme del EMBI: ajuste en la superposición y error típico dejando un trimestre afuera |
| 32,4% contra 31,8% | No estabilización en 2031 con datos desde 1999 (sin empalme) y con la ventana completa |
| 2 rezagos | Schwarz elige 1 (Portmanteau p = 0,000); con 2, p = 0,056 |
| 0,896 | Autovalor máximo del VAR principal |
| 0,0576 [0,0220; 0,0822] | Reacción fiscal de impacto |
| 0,199 [0,112; 0,328] | Reacción fiscal de largo plazo |
| 31,8% [25,2; 36,4] | No estabilización en 2031 (FMI: 1%) |
| 31,0% [26,8; 35,6] | No estabilización en 2035 (FMI: menos de 3%) |
| 24,2 y 26,6 | Límites inferiores con Bonferroni (95%), 2031 y 2035 |
| 78,3 [57,3; 87,9] | H1a: no fiscal menos fiscal, varianza de 2035 |
| 44,9 / 32,3 / 12,0 / 10,8 | Varianza de 2035: externo / cambiario y de riesgo / actividad / fiscal (%) |
| 3,29% del PIB | Máximo anual del resultado primario sin rentas 1996-2025 (2004), definición principal; con rentas, 3,58% |
| 26,1% | Probabilidad en 2031 con el resultado primario en su máximo histórico (3,29%) todos los años |
| +8,00 puntos | Aumento del resultado primario necesario para llevar la probabilidad de 2031 al 1% |
| +9,7 [4,2; 16,0] | Senda de la FED 2022-2025: efecto sobre la probabilidad en 2035 (pp), robusto |
| +9,0 [0,3; 16,2] | Senda de la FED 2022-2025: efecto sobre la deuda en 2035 (pp del PIB), no robusto |
| +1,1 [0,2; 1,9] | Nivel de la FED 0,494 más alto: efecto sobre la probabilidad en 2035 (pp), no resiste Bonferroni |
| 8,6 de 9,0 | Costo directo de la deuda en dólares en el efecto de la senda (96%) |
| 2 de 84 | Intervalos de respuesta a la FED que excluyen el cero |
| 24,1% | No estabilización en 2031 con *shocks* a la manera del FMI |
| 46,6 contra 71,5 | Ancho del abanico en 2031: nuestro contra el del FMI |
| 26,5% y 24,1% | Extensión consolidada: no estabilización en 2031 y 2035 |
| 20 | Especificaciones de robustez del SVARX (Apéndice A.9) |
