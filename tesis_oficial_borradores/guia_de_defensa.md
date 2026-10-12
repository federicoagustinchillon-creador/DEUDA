# Guía de defensa: qué hicimos, por qué y qué nos pueden discutir

Documento interno del grupo. No forma parte de la tesis. Resume cada paso del trabajo empírico con su justificación, para poder responder con precisión en la defensa, y lista las críticas que puede hacer un jurado, con la respuesta que tenemos y lo que se podría mejorar.

## Parte 1. Qué hicimos, paso a paso

### Paso 1. Pregunta e hipótesis

- **Qué:** la pregunta, los objetivos y las tres hipótesis salen de la Introducción corregida de Santiago (7/10/2026), con los comentarios de Pablo del 15/9 incorporados: citas para cada afirmación, sin frases de tono periodístico, sin rayas, términos en inglés en cursiva con nota al pie.
- **H1a** es el texto de Santiago: los determinantes condicionan la sostenibilidad y el superávit, por sí solo, no basta.
- **H1b** compara nuestra probabilidad de no estabilización con la del FMI: 1% a mediano plazo y menos de 3% a diez años.
- **H2** mide el efecto de un endurecimiento de la FED.
- **Por qué los umbrales del FMI:** son el diagnóstico oficial vigente, del análisis de sostenibilidad más reciente (FMI, 2026, Artículo IV y segunda revisión, mayo de 2026): probabilidad de estabilización de alrededor de 99% a mediano plazo y superior a 97% en el abanico de diez años. El umbral de 100% del PIB que había antes no tenía fuente y se sacó. Hasta octubre de 2026 se usaba el informe de abril de 2025 (3%), que quedó como robustez.

### Paso 2. Datos

Todas las series se construyeron desde fuentes primarias con scripts que se pueden volver a correr (`codigo/ingesta_datos/`). No hay cifras tipeadas a mano.

| Serie | Fuente | Cómo se construyó | Por qué así |
|---|---|---|---|
| Deuda consolidada neta (principal) | MECON (deuda federal) y BCRA (balance) | Deuda bruta del Tesoro, más pasivos remunerados del BCRA, menos la deuda del Tesoro en poder del BCRA (Letras Intransferibles a valor nominal), menos depósitos del Tesoro en el BCRA | Es la consolidación que propone el FMI (2021, anexo II): se netean los créditos del banco central al gobierno y se suman sus pasivos |
| Denominador | INDEC | PIB nominal de los últimos cuatro trimestres | Evita mezclar un stock con un flujo trimestral anualizado, que infla el cociente en trimestres de alta inflación |
| Resultado primario | MECON, esquema ahorro-inversión-financiamiento (dataset 379) | Flujo trimestral anualizado sobre el PIB de cuatro trimestres | La suma móvil de cuatro trimestres induce autocorrelación artificial en el VAR |
| PIB real | INDEC base 1993 empalmada a base 2004 | Coeficiente de enlace k = 1,751 (media de 2004) | La base 2004 empieza en 2004 |
| EMBI+ | JP Morgan, con *stripped spread* Brady antes de 1998 | Empalme con corrección proporcional en el punto de unión | El EMBI+ oficial empieza en 1998 |
| TCRM | BCRA (índice multilateral) | Promedio trimestral | Es el que usa el FMI para el efecto de valuación |
| Tasa de la FED | FRED: tasa de fondos federales y tasa sombra de Wu y Xia (2016) | Tasa sombra en los años de tasa cero | En el límite cero la tasa de fondos federales no refleja la política |
| VIX | CBOE | Promedio trimestral | Volatilidad financiera global |

**Controles contra el FMI.** La deuda neta da 119,0% del PIB en 2023, 61,1% en 2024 y 61,0% en 2025, contra 111,1%, 53,6% y 52,1% del FMI (2026, cuadro 2). La diferencia, de 8 a 9 puntos y estable, viene sobre todo de los títulos en cartera del FGS, que el FMI descuenta y nosotros todavía no (Capítulo 5).

### Paso 3. El modelo: un SVARX

- **Qué es:** un vector autorregresivo estructural con variables exógenas, trimestral. Las endógenas son el resultado primario, el crecimiento, el EMBI+ y el TCRM. Las exógenas son la variación de la tasa de la FED (contemporánea y dos rezagos), el VIX, binarias estacionales y binarias de los quiebres de Bai y Perron (2001T4, 2006T2, 2018T1). La deuda rezagada entra en todas las ecuaciones.
- **Por qué un VAR:** las cuatro variables se determinan juntas. Es la arquitectura que el propio FMI usa para el abanico estocástico (Celasun, Debrun y Ostry, 2006): un VAR para los determinantes y la identidad de la deuda para acumularlos.
- **Por qué la FED es exógena:** Argentina es una economía pequeña y abierta. Su economía no mueve la tasa de Estados Unidos (Cushman y Zha, 1997; Canova, 2005).
- **Por qué en niveles:** las estimaciones siguen siendo consistentes aunque haya raíces unitarias, sin imponer relaciones de cointegración que no tienen respaldo (Sims, Stock y Watson, 1990).
- **Rezagos:** se elige el orden que minimiza el AIC, sujeto a que el modelo sea estable. El AIC llega a su mínimo en 6, pero desde 4 rezagos el modelo es inestable (raíz de 1,02), así que se usan 3 (raíz de 0,96). El criterio de Hannan-Quinn elige 2 y el de Schwarz, 1, así que 3 queda dentro del rango que sugieren los tres criterios.
- **Muestra:** todas las especificaciones se estiman sobre los mismos trimestres, 1998T2-2025T4 (111). Los trimestres de 1996-1998 se usan como valores iniciales de los rezagos, así que los criterios de información se comparan sobre el mismo período (Lütkepohl, 2005).

### Paso 4. Identificación de los shocks

- **Shock fiscal:** se le descuenta al resultado primario su respuesta automática al ciclo, con una elasticidad de 0,25 (Blanchard y Perotti, 2002; Girouard y André, 2005). Lo que queda es el shock fiscal discrecional.
- **Shock de actividad:** la parte del crecimiento que no explica el shock fiscal.
- **Bloque cambiario y de riesgo:** el EMBI+ y el TCRM se tratan como un bloque, sin ordenarlos entre sí. No hay razón teórica para decir cuál reacciona primero. Solo se interpreta el efecto conjunto del bloque, que no depende de cómo se ordene adentro (Christiano, Eichenbaum y Evans, 1999).
- **Por qué no Cholesky como principal:** obliga a elegir un orden entre el EMBI+ y el TCRM sin fundamento. Esa justificación ya la aprobó Pablo. Cholesky se corrió como robustez (ver Parte 2).

### Paso 5. Retroalimentación entre la deuda y las variables

Es la "arquitectura B" que propuso Santiago: la deuda no se proyecta aparte, sino que realimenta al sistema. La deuda rezagada entra en las cuatro ecuaciones (Favero y Giavazzi, 2007), y en la simulación la deuda se acumula con la identidad y vuelve a entrar en el trimestre siguiente.

- **Qué da:** un punto más de deuda sube el EMBI+ 22 puntos básicos al trimestre siguiente, con un intervalo de 90% de [11; 41], y sube el superávit primario 0,05 puntos (la reacción de Bohn).
- **Cuánto pesa:** sin retroalimentación (la "arquitectura A"), la probabilidad a 2030 queda igual (11,5%) y el abanico se ensancha un poco. Los dos efectos se compensan.

### Paso 6. Intervalos de confianza

Se usa un *bootstrap* salvaje de diseño recursivo (Gonçalves y Kilian, 2004), con 1.000 réplicas para el VAR y 300 para la simulación, y semilla fija. Es válido aunque los residuos no sean normales (no lo son) y aunque tengan heterocedasticidad.

### Paso 7. Simulación de la deuda (Monte Carlo)

1. **Escenario base:** el del FMI (2026, cuadro 6). En promedio para 2026-2035 tiene crecimiento real de 3,3%, deflactor de 10,8% (30,2% en 2026, 7,5% desde 2029), tasa efectiva de 4,4% y superávit primario de 2,1% del PIB. Se usa el del FMI para que la comparación con su probabilidad sea directa.
2. **Desvíos:** el SVARX se simula trimestre a trimestre en desvíos respecto del escenario base, con shocks estructurales históricos remuestreados. Así se conservan las colas gordas y la correlación entre variables.
3. **Identidad de la deuda, con separación de monedas:** el tipo de cambio real revalúa el 58% de la deuda que está en moneda extranjera. La tasa en dólares (FED más EMBI+) se reprecia de a poco, a medida que vence la deuda: cada año se refinancia el 28%, que es el cociente entre las necesidades de financiamiento promedio y la deuda promedio de los seis primeros años del escenario del FMI.
4. **Punto de partida:** deuda neta de 61,0% del PIB en diciembre de 2025.
5. **Tamaño:** 300 réplicas de parámetros por 400 trayectorias cada una, 120.000 en total.

### Paso 8. Cómo se contrasta cada hipótesis

| Hipótesis | Qué se mide | Criterio | Por qué |
|---|---|---|---|
| H1a | Cuánto de la varianza de la deuda en 2035 explica cada bloque de shocks | Lo no fiscal supera a lo fiscal, con un intervalo de 90% de la diferencia que excluye el cero | Traduce "el superávit por sí solo no basta" en un número que se puede contrastar |
| H1b | Probabilidad de que el superávit del escenario base no alcance para estabilizar la deuda (definición del FMI, 2021, anexo VI, nota 9) | El límite inferior del intervalo de 90% supera la cifra del FMI para el mismo horizonte: 1% a cinco años y 3% a diez (contraste unilateral al 5%) | Es la misma métrica y son las mismas cifras del FMI |
| H2 | Diferencia en esa probabilidad y en la deuda entre el escenario con suba de la FED y el base | El intervalo de 90% de la diferencia excluye el cero | Mide el efecto de un shock externo identificado |

**Tamaño del shock de la FED:** un desvío estándar de la variación trimestral (0,50 puntos), que es la convención en estos modelos, y una repetición del ciclo de 2022-2023 (5,25 puntos en ocho trimestres), el episodio real más reciente.

### Paso 9. Resultados y robusteces

| Especificación | No estabilización 2030 | No estabilización 2035 | H1a (no fiscal menos fiscal) |
|---|---|---|---|
| Principal (escenario FMI 2026) | 11,5% [7,7; 15,2] | 6,6% [3,3; 10,5] | 58 [13; 92] |
| Deuda neta a valor libros | 12,7% | 7,4% | 59 [17; 91] |
| Deuda bruta | 12,3% | 7,8% | 53 [-7; 94] |
| Canal de tasas en pesos | 12,2% | 8,8% | 64 [17; 94] |
| Sin retroalimentación | 11,5% | 6,1% | 58 [12; 92] |
| Escenario del FMI de 2025 | 11,8% | 6,0% | 61 [18; 93] |
| Cholesky en el orden de Santiago | 11,6% | 6,6% | 78 [35; 96] |
| Cholesky con el fiscal primero | 11,5% | 6,6% | 33 [-48; 87] |
| Shocks a la manera del FMI | 23,0% | 15,2% | no aplica |

- **H1b** se sostiene a cinco y a diez años en todas las especificaciones con el escenario de 2026.
- **H2** se sostiene para el ciclo 2022-2023 en todas, y no para el shock de medio punto.
- **H1a** se sostiene en todas menos en dos: la deuda bruta (intervalo de [-7; 94]) y Cholesky con el fiscal primero.

## Parte 2. Lo que nos pueden discutir

Ordenado de más a menos peligroso.

### 2.1 Críticas de fondo

**1. "H1a depende de cómo identificaron el shock fiscal."**
- **Es cierto en parte.** Con Cholesky ordenando el fiscal primero, que es el orden más favorable a lo fiscal, el intervalo de la diferencia incluye el cero. La mayoría de las réplicas (77%) igual da lo no fiscal por encima. Con la deuda bruta pasa algo parecido: 92% de las réplicas da lo no fiscal por encima, pero el intervalo también incluye el cero.
- **Respuesta:** la identificación principal se basa en una elasticidad estimada, no en un orden arbitrario. Con el orden propuesto por Santiago el resultado es todavía más fuerte, y el bloque cambiario y de riesgo explica cerca de 60% en todas las identificaciones. Lo que cambia es cuánto se lleva el fiscal frente a la actividad.
- **Cómo quedó:** está en Robustez (6.6) y en Limitaciones (7.5): H1a depende de identificar el shock fiscal por su respuesta al ciclo.

**2. "¿Por qué ese escenario del FMI y no otro?"**
- **Respuesta:** es el análisis de sostenibilidad más reciente del FMI (mayo de 2026). Hasta octubre de 2026 se usaba el de abril de 2025, y con ese escenario los resultados son casi los mismos (11,8% a cinco años), así que la conclusión no depende de cuál se use.
- **Cuidado:** el escenario y el umbral tienen que salir del mismo informe. Por eso con el escenario de 2026 se compara contra 1%, y con el de 2025, contra 3%.

**3. "Comparan su deuda consolidada neta con la deuda federal bruta del FMI."**
- **Es cierto.** Por eso se reporta también la bruta, y el resultado de H1b no cambia (12,3%).
- **Además:** con el procedimiento del FMI aplicado a nuestros datos sale 23,0%, no 1%. La diferencia con el FMI no es solo de perímetro. Su 3% no se puede reproducir porque el FMI no publica sus datos de entrada.

**4. "La tasa efectiva y el ajuste stock-flujo del escenario son de la deuda federal bruta, no de la consolidada neta."**
- **Es cierto.** Es una aproximación. El ajuste stock-flujo del FMI (4,2 y 4,7 puntos en 2026 y 2027, por la indexación de bonos y los intereses capitalizados) se suma igual a nuestra deuda.
- **Mejora:** correr una variante con el ajuste stock-flujo en cero para mostrar que no cambia la conclusión.

**5. "Los coeficientes son los mismos en convertibilidad, default, alta inflación y desinflación."**
- **Es cierto:** las binarias de quiebre solo mueven el nivel, no las pendientes.
- **Respuesta:** con 111 trimestres no hay grados de libertad para estimar cuatro modelos distintos. Los quiebres sí capturan los cambios de nivel.
- **Mejora:** estimar desde 2004 como robustez (pierde el default pero gana homogeneidad).

**6. "El EMBI+ de 2002-2005 no es un costo de financiamiento: el país estaba en default."**
- **Es cierto.** El quiebre de 2001T4 y el de 2006T2 absorben el nivel, pero las fluctuaciones de ese período igual entran en la estimación.
- **Mejora:** la misma robustez desde 2004, o una binaria por el período de default.

**7. "La variación de la tasa de la FED no es un shock: es en parte anticipada."**
- **Es cierto.** Santiago ya proponía usar shocks identificados por la literatura (de alta frecuencia o narrativos).
- **Respuesta:** la tasa es exógena para Argentina aunque sea anticipada en Estados Unidos.
- **Mejora:** reemplazarla por una serie de shocks monetarios de alta frecuencia publicada. Quedó en las líneas futuras.

**8. "Las respuestas a la FED no son significativas, pero H2 sí."**
- **Es cierto, y está explicado.** El efecto significativo de H2 viene en tres quintos (61%) del costo directo de refinanciar la deuda en dólares, no de los canales indirectos.

**9. "La probabilidad de no estabilización no es la probabilidad de default."**
- **Correcto, y así se dice.** Es la probabilidad de que el superávit del escenario base no alcance para que la deuda deje de subir (FMI, 2021, recuadro 2: no estabilización y deuda insostenible son conceptos distintos).

### 2.2 Críticas de datos

**10. "La deuda neta no descuenta el FGS."**
- **Es cierto.** Es la principal diferencia con el FMI, de 8 a 10 puntos del PIB.
- **Mejora:** bajar a mano los PDF de ANSES y restarlo. Está en el plan.

**11. "Faltan las LEFI entre julio de 2024 y julio de 2025."**
- **Puede ser:** si la deuda del Tesoro que usamos no las incluye, faltan unos 2 puntos del PIB en esos trimestres.
- **Mejora:** verificarlo en los informes de Finanzas y corregir.

**12. "Las Letras Intransferibles a valor nominal o a valor libros."**
- **Se reportan las dos.** Los resultados casi no cambian (11,5% contra 12,7%).

**13. "El crecimiento no está desestacionalizado."**
- **Respuesta:** las binarias estacionales absorben la estacionalidad (Lütkepohl, 2005). Desestacionalizar con X-13 antes de un VAR también tiene objeciones conocidas.

### 2.3 Críticas de método

**14. "Hay autocorrelación en los residuos (Portmanteau p = 0,036)."**
- **Es cierto y está declarado.** Los órdenes que la eliminarían son inestables. Se priorizó la estabilidad porque sin ella no se puede simular.

**15. "La descomposición de la varianza por bloques ignora las interacciones."**
- **Es cierto:** se simula cada bloque por separado y se normaliza.
- **Mejora:** reportar también la suma sin normalizar, para mostrar cuánto se pierde.

**16. "La velocidad de refinanciación (28% por año) está calibrada, no estimada."**
- **Es cierto.** Sale de las necesidades de financiamiento del FMI.
- **Mejora:** probar 10% y 30% como sensibilidad.

**17. "La métrica usa el superávit del escenario base y no el simulado."**
- **Es la definición del FMI.** La variante con el superávit simulado da más alto (14,6% a 2030), así que la elección es conservadora.

**18. "No hay fatiga fiscal (respuesta no lineal del superávit)."**
- **Es cierto.** El marco teórico la presenta como complemento (Ghosh et al., 2013), y la regla lineal es la que usa el FMI.

### 2.4 Lo que el grupo propuso y quedó afuera, con el motivo

- **Módulo de balanza de pagos** (exportaciones, importaciones, inversión extranjera directa, fuga, renovación de vencimientos): es otra tesis y no estaba especificado. Quedó como línea futura.
- **Restricciones de signo y Blanchard-Quah:** tres esquemas de identificación excede una tesis de grado, y la neutralidad de largo plazo del TCRM es difícil de sostener para Argentina.
- **Umbral de deuda de 100% del PIB:** sin fuente que lo justifique.
- **Términos de intercambio como variable exógena:** quedó como línea futura.
- **Panel Argentina-Chile:** quedó como línea futura, por decisión del 17/9.

## Parte 3. Qué mejorar, por prioridad

1. **Hecho:** la robustez de H1a a la identificación y al perímetro está escrita en Robustez y en Limitaciones (crítica 1).
2. **Restar el FGS** (crítica 10) y verificar las LEFI (crítica 11). Puede cambiar el punto de partida y conviene que esté antes de la entrega.
3. **Hecho:** el escenario base pasó al análisis del FMI de mayo de 2026, y el de abril de 2025 quedó como robustez.
4. **Robusteces baratas:** estimar desde 2004, ajuste stock-flujo en cero y velocidad de refinanciación de 10% y 30% (críticas 4, 5 y 16).
5. **Revisar la extensión:** el capítulo de Datos es el más largo y se puede achicar llevando el detalle de construcción al apéndice.

## Parte 4. Decisiones del director que hay que respetar

- **No nombrar la elección de un solo período de estimación** como "ventana única": es implícita (18/9).
- **No incluir en el texto la discusión sobre si el riesgo país es endógeno.** Si preguntan, la respuesta oral es que en series de tiempo todo es endógeno salvo los shocks de mayor frecuencia que el sistema, y por eso el VIX y la tasa de la FED entran como exógenas (reunión del 17/9).
- **Tesis corta**, sin resumen en inglés.

## Parte 5. Números para tener a mano

| Número | Qué es |
|---|---|
| 61,0% del PIB | Deuda consolidada neta a diciembre de 2025 (punto de partida) |
| 0,051 [0,020; 0,082] | Reacción fiscal de Bohn |
| 22 pb [11; 41] | Suba del EMBI+ por cada punto de deuda |
| 60% / 19% / 21% | Varianza de la deuda en 2035: cambiario y de riesgo / actividad / fiscal |
| 11,5% [7,7; 15,2] | No estabilización a cinco años (FMI: 1%) |
| 6,6% [3,3; 10,5] | No estabilización a diez años (FMI: menos de 3%) |
| +7,8 pp del PIB, +9,5 pp de probabilidad | Efecto de un ciclo de la FED como el de 2022-2023 en 2035 |
| 18,6 contra 71,5 | Ancho del abanico a cinco años: nuestro contra el del FMI |
| 3 rezagos, 111 trimestres, 1998T2-2025T4 | Especificación del VAR |
