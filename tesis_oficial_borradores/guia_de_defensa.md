# Guía de defensa: qué hicimos, por qué y qué nos pueden discutir

Documento interno del grupo. No forma parte de la tesis. Resume cada paso del trabajo empírico con su justificación, según la versión del modelo del 12/10/2026 (decisiones D1 a D14), las críticas que se resolvieron en esa versión y las que todavía puede hacer un jurado, con la respuesta. Todos los números salen de la hoja de números y del Apéndice.

## Parte 1. Qué hicimos, paso a paso

### Paso 1. Pregunta e hipótesis

- **H1a:** los determinantes condicionan la sostenibilidad y el superávit, por sí solo, no basta para estabilizar la deuda. Criterio, el original: la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del *shock* fiscal, con un intervalo de 90% que excluye el cero.
- **H1b:** nuestra probabilidad de no estabilización de la deuda federal bruta es mayor que la del FMI para esa misma deuda en 2031 y en 2035. Criterio: el límite inferior del intervalo de 90% supera 1% y 3%; se informa Bonferroni por los dos horizontes (95%).
- **H2:** un endurecimiento de la FED eleva la deuda esperada y la probabilidad de no estabilización. Criterio: el intervalo de 90% de la diferencia con el escenario base excluye el cero en 2035, en la probabilidad y en la deuda; 2031 se informa.
- **Cifras de comparación:** las del análisis de sostenibilidad más reciente del FMI (2026, Artículo IV y segunda revisión): 1% a mediano plazo (2031) y menos de 3% en su abanico de diez años (2035). El 1% es la estimación puntual del FMI para Argentina, no un umbral de riesgo bajo.

### Paso 2. Datos y perímetro

- **Perímetro principal (D1):** deuda bruta del gobierno federal, el perímetro del FMI. La simulación parte del *stock* del FMI a fines de 2025, 80,3% del PIB (cuadro 2, línea 1). Nuestra serie, construida con datos del MECON, da 77,7%; la diferencia son los intereses capitalizados, la deuda no presentada al canje, los reclamos por los cupones PBI y la medición del PIB.
- **Extensión:** deuda del sector público consolidado con el BCRA en la definición del FMI (cuadro 2, línea 5), 52,1% del PIB a fines de 2025, con 68,5% en moneda extranjera. La dinámica se estima con nuestra serie consolidada (Tesoro más BCRA, Letras a valor nominal).
- **Muestra (D2):** datos desde 1999T1; muestra efectiva común 2000T3-2025T4, 102 trimestres, para que todos los órdenes de rezago hasta seis se comparen sobre los mismos trimestres (Lütkepohl, 2005, sec. 4.3).

| Serie | Fuente | Construcción | Por qué así |
|---|---|---|---|
| Deuda federal bruta | MECON; *stock* inicial del FMI (2026) | Deuda bruta de la Administración Central sobre el PIB de los últimos cuatro trimestres | Es la deuda del análisis del FMI |
| Deuda consolidada | MECON y BCRA | Deuda del Tesoro + pasivos remunerados del BCRA − deuda del Tesoro en poder del BCRA − depósitos del Tesoro | Es la consolidación del FMI (2021, anexo II) |
| Resultado primario (D4) | MECON | Flujo trimestral anualizado; con rentas de la propiedad para la deuda federal, sin rentas para la consolidada | Coherencia con cada perímetro |
| PIB real | INDEC | Base 1993 empalmada a base 2004 | La base 2004 empieza en 2004 |
| EMBI+ | J.P. Morgan, serie diaria publicada por Ámbito Financiero | Promedio trimestral | Fuente publicada y verificable desde diciembre de 1998 |
| TCRM | BCRA | Promedio trimestral | Índice multilateral del BCRA |
| Tasa de la FED (D5) | FRED y tasa sombra de Wu y Xia (2016) | Sombra en el límite cero; en 2022T1 la variación se calcula con la tasa efectiva en los dos trimestres | En el límite cero la tasa efectiva no refleja la política, y el cambio de serie no es un cambio de política |
| VIX | CBOE | Promedio trimestral | Medida estándar de aversión global al riesgo |

**Controles.** El resultado primario federal con rentas coincide con el del FMI: 1,38% del PIB en 2025 contra 1,4%, y 1,78% en 2024 contra 1,8%. La identidad reproduce la senda de deuda del FMI con un desvío máximo de 0,12 puntos.

### Paso 3. El modelo: un SVARX

- **Variables:** cuatro endógenas (resultado primario, crecimiento, EMBI+, TCRM); exógenas: variación de la tasa de la FED (rezagos 0 a 2), VIX, binarias estacionales y binarias de los quiebres de Bai y Perron sobre la deuda (2001T4, 2006T2, 2018T1). La deuda rezagada entra en todas las ecuaciones.
- **Por qué un VAR:** las cuatro variables se determinan juntas; es la arquitectura del abanico estocástico de Celasun et al. (2006).
- **Por qué la FED es exógena:** Argentina es una economía pequeña y abierta (Cushman y Zha, 1997; Canova, 2005).
- **Por qué en niveles:** las estimaciones son consistentes sin imponer cointegración (Sims et al., 1990). Las pruebas de raíz unitaria son ambiguas para la deuda, el EMBI+ y el TCRM, y Johansen no rechaza rango cero (traza 45,0 contra 47,9). La inferencia se hace con *bootstrap*.
- **Rezagos (D3):** criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1, con residuos autocorrelacionados (p = 0,000); se usan 2 (p = 0,296), el mismo orden que elige Hannan-Quinn. Autovalor máximo 0,849.

### Paso 4. Identificación de los *shocks*

- **Fiscal:** se descuenta la respuesta automática al ciclo con una elasticidad de 0,25 (Blanchard y Perotti, 2002; Girouard y André, 2005).
- **Actividad:** puede responder al *shock* fiscal en el trimestre.
- **Bloque cambiario y de riesgo:** el EMBI+ y el TCRM sin orden entre sí; solo se interpreta el efecto conjunto (Christiano et al., 1999). El resultado primario y el crecimiento no responden en el trimestre a ese bloque.
- **Robusteces:** Cholesky con el resultado primario primero y último, y elasticidades de 0 y 0,5.
- **Dato clave:** la identificación no cambia la probabilidad de no estabilización, porque los *shocks* estructurales reconstruyen los mismos residuos. Con números aleatorios comunes, las identificaciones alternativas dan exactamente la misma probabilidad (32,8% en 2031). La identificación hace falta para dos cosas: repartir la varianza de la deuda por bloque, que es el criterio de H1a, y definir el *shock* fiscal.

### Paso 5. Retroalimentación entre la deuda y las variables

La deuda rezagada entra en las cuatro ecuaciones y se acumula con la identidad (Favero y Giavazzi, 2007). En la simulación se actualiza al cierre de cada año, porque la identidad del FMI es anual. La deuda se asocia con más superávit: coeficiente de impacto 0,0495 [0,0099; 0,0799] y multiplicador de largo plazo 0,167 [0,057; 0,296]. Con el EMBI+ la estimación es de 15,5 puntos básicos por punto de deuda, con un intervalo que incluye el cero ([-4,2; 29,7]). Sin retroalimentación, la probabilidad en 2031 casi no cambia (31,4%) y el abanico se abre (55,5 puntos contra 48,3).

### Paso 6. Inferencia

- **Estimación central (D8):** parámetros de MCO (autovalor máximo 0,849) y 20.000 trayectorias; error de Monte Carlo de 0,33 puntos.
- **Intervalos de 90%:** *bootstrap* de bloques móviles de cuatro trimestres sobre los residuos, de diseño recursivo, en el que la deuda también se regenera (Brüggemann et al., 2016), con percentiles de Hall (1992), que corrigen el sesgo de la distribución *bootstrap* respecto de la estimación puntual. 200 réplicas con 1.000 trayectorias cada una. Mediana del autovalor máximo en las réplicas: 0,818.
- **Por qué se abandonó el *bootstrap* salvaje:** Brüggemann et al. (2016) muestran que no reproduce la estructura de cuarto orden de las innovaciones de la que dependen las respuestas estructurales.
- **Números aleatorios comunes:** todas las especificaciones usan los mismos, de modo que las diferencias entre filas no vienen del sorteo.
- **Corrección de sesgo de Kilian (1998):** como robustez (31,3% en 2031).

### Paso 7. Simulación

1. **Escenario base del FMI (2026, cuadro 6):** crecimiento, deflactor, tasa efectiva, resultado primario, ajuste *stock*-flujo e inflación relativa, para la deuda a la que corresponde.
2. **Desvíos:** el SVARX se simula trimestre a trimestre con los *shocks* estructurales remuestreados en bloques de ocho trimestres (D7), como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI).
3. **Variables externas (D6):** el VIX y el nivel de la tasa de la FED siguen procesos AR(1) estimados en la muestra (0,700 y 0,960); sus innovaciones se remuestrean junto con los *shocks* estructurales, por fecha. La varianza tiene un cuarto bloque, externo.
4. **Identidad (D9):** separa moneda local (proporción en pesos 0,422, fija como en el FMI) y extranjera; la tasa en dólares se reprecia con λ = 0,282 por año. El ajuste *stock*-flujo se escala por la deuda en pesos simulada y la inflación relativa por la deuda en moneda extranjera. El desvío del crecimiento anual es la variación del promedio anual del nivel del PIB.
5. **Métrica del FMI:** la deuda no se estabiliza en T si el resultado primario del escenario es menor que pb* = d(T-1)(M(T) − 1) + sf(T) + ri(T), el que la estabilizaría incluido el ajuste *stock*-flujo (FMI, 2021, párr. 53).
6. **Escenarios de la FED:** (i) nivel 0,504 puntos más alto en forma permanente desde 2026T1 (un desvío estándar de la variación trimestral); (ii) repetición de la senda trimestral de 2022-2025 en 2026-2029: sube 5,25 puntos, baja 1,43 y desde 2030 queda 3,82 puntos por encima del base hasta 2035.

### Paso 8. Resultados

- **H1a, respaldada.** No fiscal menos fiscal: 82,6 puntos [65,8; 92,4]. Reparto de la varianza en 2035: externo 46,6%, cambiario y de riesgo 32,3%, actividad 12,4%, fiscal 8,7%. Se cumple en las 19 especificaciones (menor límite inferior: 31,4, Cholesky con el resultado primario primero). Complemento descriptivo: con el resultado primario en su máximo de 1999-2025 (3,58%, 2004) todos los años, la probabilidad en 2031 es 25,5%; para llevarla al 1% haría falta sumar 7,75 puntos (9,2% del PIB en 2026 y 10,0% en 2031).
- **H1b, respaldada.** 32,8% [26,8; 37,9] en 2031 y 31,3% [27,0; 35,3] en 2035; con Bonferroni, límites inferiores de 26,3 y 26,4. Se cumple en las 19 especificaciones (menor límite inferior 20,3, deuda consolidada).
- **H2, respaldada en su efecto sobre la probabilidad, no en su mecanismo.** Senda 2022-2025: +11,3 puntos de probabilidad en 2035 [4,4; 17,9] y +12,6 de deuda [1,2; 21,8]. Nivel 0,504 más alto: +1,5 [0,5; 2,6] y +1,5 [0,1; 2,5].

## Parte 2. Qué cambió en la versión del 12/10/2026

| Problema de la versión anterior | Decisión | Resultado |
|---|---|---|
| La comparación con el FMI mezclaba perímetros | D1: deuda federal bruta como principal, con el punto de partida, el escenario y la métrica del FMI; consolidada como extensión | H1b compara lo mismo con lo mismo |
| EMBI+ de 1996-1998 transcripto y TCRM de 1996 retropolado | D2: datos desde 1999 | Todas las series con fuente publicada |
| Regla de rezagos sin respaldo y cita de Ivanov y Kilian mal usada | D3: Schwarz más adecuación de residuos | 2 rezagos, residuos sin autocorrelación (p = 0,296) |
| Resultado primario con perímetro distinto del de la deuda | D4: definición por perímetro | Coincide con el FMI en 2024 y 2025 |
| Salto de la FED en 2022T1 por cambio de serie | D5: variación con la tasa efectiva en los dos trimestres | El desvío (0,504) no incluye el cambio de serie |
| VIX y FED fijos en la simulación | D6: procesos AR(1) con innovaciones remuestreadas | Bloque externo en la varianza |
| Remuestreo independiente con residuos autocorrelacionados | D7: bloques de ocho trimestres | Conserva la autocorrelación remanente |
| Estimación central casi con raíz unitaria e intervalos descentrados | D8: MCO, *bootstrap* de bloques y percentiles de Hall | Autovalor 0,849; Kilian como robustez |
| Ajuste *stock*-flujo sin escalar y métrica sin él | D9: escalado por moneda y pb* con el ajuste | Identidad y métrica coherentes |
| Criterio de H1a cambiado después de estimar | D10: criterio original | Se cumple en las 19 especificaciones |
| H1b contra el FMI sin perímetro común | D11 | Se cumple en las 19 especificaciones |
| H2 sin horizonte fundado | D12: 2035, porque el efecto se acumula | Se cumple en la principal; mecanismo no distinguible |

## Parte 3. Críticas que puede hacer el jurado y respuesta honesta

### Críticas que la versión actual resuelve

1. **"Cambiaron los criterios después de ver los resultados."** Ya no. H1a se contrasta con su criterio original (D10) y H2 mantiene el suyo (D12). Los dos tamaños del *shock* de la FED tienen una justificación externa a los resultados: un desvío estándar, que es la convención de la literatura de VAR, y la repetición del episodio de 2022-2025.
2. **"H1b compara cosas que no son comparables."** Ahora compara lo mismo: perímetro, punto de partida (80,3%), escenario, horizonte y métrica del FMI (D11). Con el procedimiento de *shocks* del FMI aplicado a la historia argentina sobre el mismo perímetro se obtiene 16,6% en 2031 y un ancho de 151,1, así que tampoco se reproduce el 1%. La diferencia viene de la distribución de *shocks* que usa el FMI, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). No atribuimos la brecha a una causa que no podemos verificar.
3. **"La estimación central es casi una raíz unitaria."** Ya no. La estimación central usa MCO, con autovalor máximo 0,849; la mediana de las réplicas es 0,818. Los percentiles de Hall corrigen el sesgo de la distribución *bootstrap*. La corrección de Kilian (1998) queda como robustez y da 31,3% en 2031.
4. **"La regla de rezagos es ad hoc."** La regla tiene respaldo citado: Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones, y adecuación de residuos (Lütkepohl, 2005, sec. 4.4). La versión anterior citaba a Ivanov y Kilian para el AIC, y esa cita era incorrecta. Con 1 y 3 rezagos la probabilidad en 2031 es 32,4% y 30,3%.
5. **"Hay autocorrelación residual y remuestrean como si no la hubiera."** Con 2 rezagos los residuos no rechazan la ausencia de autocorrelación (p = 0,296). La simulación remuestrea en bloques de ocho trimestres y la inferencia usa bloques móviles de cuatro, que conservan la autocorrelación remanente.
6. **"Usan un *bootstrap* salvaje sin heterocedasticidad condicional."** Se abandonó. Las pruebas ARCH no rechazan (p entre 0,114 y 0,998), y Brüggemann et al. (2016) muestran que el *bootstrap* salvaje no reproduce la estructura de cuarto orden de las innovaciones.
7. **"El resultado primario incluye las utilidades del BCRA."** La definición depende del perímetro (D4). Para la deuda federal se incluyen, porque son ingreso del Tesoro y es la definición del FMI; para la consolidada se excluyen, porque son un flujo interno. Sin rentas, la probabilidad federal es 32,4% en 2031.
8. **"El escenario del FMI es para otra deuda."** Ahora se aplica a la deuda para la que fue construido, y la identidad reproduce la senda del FMI con un desvío máximo de 0,12 puntos.
9. **"El EMBI+ de 1996-1998 no es el EMBI+."** Esos años salieron de la muestra (D2): los datos empiezan en 1999, con el EMBI+ de la serie diaria de Ámbito Financiero.
10. **"La identificación no aporta nada a la probabilidad."** Es así por construcción, y la tesis lo dice: las identificaciones alternativas dan exactamente la misma probabilidad. La identificación sigue siendo necesaria para repartir la varianza por bloque, que es el criterio de H1a, y para definir el *shock* fiscal. Con Cholesky el reparto cambia (63,9 y 95,8 puntos), pero el criterio de H1a se cumple en todas las variantes.
11. **"La elasticidad de 0,25 es de la OCDE."** Solo afecta el reparto de la varianza. Con 0 y 0,5 la diferencia no fiscal menos fiscal es 63,9 y 96,5, y las dos excluyen el cero.
12. **"El abanico se angostaba porque el VIX y la FED quedaban fijos."** Ahora se simulan con sus procesos AR(1), y el bloque externo explica 46,6% de la varianza en 2035.

### Debilidades que siguen y cómo responderlas

1. **El mecanismo de H2 no aparece.** Solo 3 de 84 intervalos de respuesta excluyen el cero, todos del TCRM y con signo de apreciación. El 75% del efecto sobre la deuda en 2035 es el costo directo de la deuda en dólares, que la identidad incorpora (9,4 de 12,6 puntos). H2 se respalda en su efecto sobre la probabilidad, no en sus canales.
2. **El efecto sobre la deuda esperada no es robusto.** Con Bonferroni no excluye el cero (límites inferiores -0,0 y -0,5). En las robusteces, el efecto de la senda sobre la deuda excluye el cero en 12 de 19 especificaciones; sobre la probabilidad, en 18 de 19.
3. **Retroalimentación al cierre del año.** Dentro del año, la deuda que entra en las ecuaciones es la del cierre del año anterior. Es coherente con la identidad anual del FMI, pero pierde la reacción dentro del año.
4. **Composición por monedas fija.** La proporción en pesos no cambia en la simulación, aunque una depreciación la cambiaría. Es el mismo supuesto del FMI (2021, anexo VI, párr. 6).
5. **El escenario del FMI se toma como dado.** No construimos un escenario propio. Con el escenario del FMI de 2025 la probabilidad en 2031 es 30,4%, y con el ajuste *stock*-flujo en cero, 29,8%.
6. **La extensión consolidada usa el escenario del FMI con flujos escalados.** El ajuste *stock*-flujo y la inflación relativa se escalan por la deuda en pesos y en moneda extranjera de ese perímetro, pero el escenario se construyó para la deuda federal.
7. **El FGS no se descuenta en la serie histórica consolidada.** La simulación de la extensión parte del *stock* del FMI, que sí lo descuenta, pero la dinámica se estima con una serie que no lo hace.
8. **Muestra pequeña.** Son 102 trimestres para cuatro ecuaciones con dos rezagos, la deuda, las exógenas y las binarias.
9. **Se rechaza la normalidad** (p = 0,000). La simulación y el *bootstrap* remuestrean los residuos empíricos y no suponen normalidad, pero los errores estándar de MCO del Apéndice son solo referencia.
10. **Fechas de quiebre estimadas sobre la deuda.** Los quiebres de Bai y Perron se estiman con la serie de deuda y entran en todas las ecuaciones. Sin esas binarias la probabilidad en 2031 es 31,2%.
11. **Endogeneidad del riesgo país** (no está en el texto por decisión del director): en series de tiempo todo es endógeno salvo los *shocks* de mayor frecuencia que el sistema; por eso el VIX y la tasa de la FED entran como exógenas.

## Parte 4. Números clave

| Número | Qué es |
|---|---|
| 80,3% del PIB | Deuda federal bruta del FMI a fines de 2025, punto de partida (serie propia: 77,7%) |
| 52,1% del PIB | Deuda consolidada con el BCRA del FMI a fines de 2025 (extensión) |
| 2000T3-2025T4, 102 trimestres | Muestra efectiva |
| 2 rezagos | Schwarz elige 1 (Portmanteau p = 0,000); con 2, p = 0,296 |
| 0,849 | Autovalor máximo del VAR principal |
| 0,0495 [0,0099; 0,0799] | Reacción fiscal de impacto |
| 0,167 [0,057; 0,296] | Reacción fiscal de largo plazo |
| 32,8% [26,8; 37,9] | No estabilización en 2031 (FMI: 1%) |
| 31,3% [27,0; 35,3] | No estabilización en 2035 (FMI: menos de 3%) |
| 26,3 y 26,4 | Límites inferiores con Bonferroni (95%), 2031 y 2035 |
| 82,6 [65,8; 92,4] | H1a: no fiscal menos fiscal, varianza de 2035 |
| 46,6 / 32,3 / 12,4 / 8,7 | Varianza de 2035: externo / cambiario y de riesgo / actividad / fiscal (%) |
| 3,58% del PIB | Máximo anual del resultado primario 1999-2025 (2004); sin rentas, 3,29% |
| 25,5% | Probabilidad en 2031 con el resultado primario en su máximo histórico todos los años |
| +7,75 puntos | Aumento del resultado primario necesario para llevar la probabilidad de 2031 al 1% |
| +11,3 [4,4; 17,9] | Senda de la FED 2022-2025: efecto sobre la probabilidad en 2035 (pp) |
| +12,6 [1,2; 21,8] | Senda de la FED 2022-2025: efecto sobre la deuda en 2035 (pp del PIB) |
| 9,4 de 12,6 | Costo directo de la deuda en dólares en el efecto de la senda (75%) |
| 3 de 84 | Intervalos de respuesta a la FED que excluyen el cero |
| 16,6% | No estabilización en 2031 con *shocks* a la manera del FMI |
| 48,3 contra 71,5 | Ancho del abanico en 2031: nuestro contra el del FMI |
| 26,8% y 24,1% | Extensión consolidada: no estabilización en 2031 y 2035 |
| 19 | Especificaciones de robustez del SVARX (Apéndice A.8) |
