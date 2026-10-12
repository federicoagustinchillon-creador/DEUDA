# 4. Metodología

Este capítulo presenta la estrategia empírica: un modelo de vectores autorregresivos estructural con variables exógenas (SVARX), combinado con la identidad de acumulación de la deuda y una simulación de Monte Carlo. Cada decisión de especificación se fundamenta en el marco del FMI, en la literatura o en las propiedades de los datos.

## 4.1 Arquitectura general

El modelo sigue la arquitectura que el FMI desarrolló para economías emergentes. Celasun et al. (2006) proponen tres piezas:

1. Un **VAR trimestral** sobre los determinantes de la dinámica de la deuda: crecimiento, tasas de interés y tipo de cambio. El VAR describe cómo se mueven juntos, estima las varianzas y covarianzas de sus *shocks* y genera proyecciones consistentes entre sí.
2. Un bloque de **comportamiento fiscal**, en su caso una función de reacción fiscal.
3. La **identidad de acumulación de la deuda**, que separa el tramo en moneda local del tramo en moneda extranjera. Por ella pasan las proyecciones del VAR, anualizadas, para calcular la deuda de manera recursiva y construir los gráficos de abanico.

El marco vigente del FMI (2021, párr. 52) mantiene la idea central: el gráfico de abanico se arma aplicando al escenario base *shocks* tomados de la historia de los determinantes de la deuda. El modelo de esta tesis conserva esas tres piezas y agrega dos elementos que justifica la vacancia: los *shocks* se identifican estructuralmente y la tasa de la FED entra como un *shock* externo con nombre propio.

## 4.2 Variables del sistema

**Tabla 4.1. Variables del SVARX**

| Variable | Rol | Fundamento |
|---|---|---|
| Crecimiento real del PIB | Endógena | Determinante de la identidad de la deuda (Celasun et al., 2006; FMI, 2021). Se usa el crecimiento y no la brecha del producto porque es lo que entra en la identidad. Se toma la serie original y no la desestacionalizada del INDEC, que empieza en 2004; la estacionalidad la absorben variables binarias trimestrales (Lütkepohl, 2005). |
| Resultado primario (% del PIB) | Endógena | Determinante de la identidad. Su ecuación incluye la deuda rezagada; ese coeficiente es la reacción fiscal de Bohn (1998). |
| EMBI+ | Endógena | Riesgo soberano: forma parte de la tasa en dólares (tasa de Estados Unidos más la prima de riesgo). |
| Tipo de cambio real multilateral (TCRM) | Endógena | Efecto de valuación sobre la deuda en moneda extranjera (Calvo et al., 2003). Se usa el multilateral porque es el índice con el que el FMI mide la contribución del tipo de cambio real a la dinámica de la deuda (FMI, 2026, cuadro 6, nota 1). |
| Deuda consolidada neta (% del PIB) | Predeterminada: entra rezagada en las ecuaciones y evoluciona por la identidad | Retroalimentación de la deuda sobre el sistema (Favero y Giavazzi, 2007). |
| Variación de la tasa de la FED | Exógena | *Shock* externo de H2. |
| VIX | Exógena | Condiciones financieras globales; es la única variable global con efectos robustos en Adler y Sosa (2013). |
| Variables binarias de quiebre | Exógenas | Quiebres de Bai y Perron (2003) estimados sobre la propia serie de deuda. |

Fuente: elaboración propia.

**Por qué la deuda entra rezagada y se acumula con la identidad.** Favero y Giavazzi (2007) muestran que un VAR fiscal que omite la retroalimentación de la deuda está mal especificado: la restricción presupuestaria hace que el nivel de deuda condicione la política fiscal y las tasas. Su solución es incluir la deuda rezagada en las ecuaciones y hacerla evolucionar con la identidad, no con una ecuación estimada. Eso capta los efectos conjuntos que plantea la pregunta de investigación y mantiene la acumulación contablemente exacta.

## 4.3 Variables exógenas

Argentina es una economía pequeña y abierta: sus variables no afectan la tasa de la FED ni el VIX. En los VAR de economías pequeñas y abiertas, el supuesto estándar es que las variables externas forman un bloque exógeno (Cushman y Zha, 1997). Así se modela la transmisión de los *shocks* de Estados Unidos a América Latina (Canova, 2005) y la relación entre tasas internacionales y primas de riesgo en emergentes (Uribe y Yue, 2006). Una consecuencia es que el efecto de la FED (H2) no depende de cómo se ordenen las variables argentinas entre sí: se calcula como un multiplicador dinámico de la variable exógena.

La serie es la tasa de fondos federales. En los trimestres en que esa tasa estuvo en el piso de cero se usa la tasa sombra de Wu y Xia (2016), que mide la orientación de la política monetaria cuando la tasa efectiva no puede bajar más.

**Tabla 4.2. Canales por los que opera el *shock* de la FED**

| Canal | Variable del modelo | Cómo afecta a la deuda en la identidad |
|---|---|---|
| Prima de riesgo soberano (Uribe y Yue, 2006) | EMBI+ | Eleva la tasa en dólares. |
| Depreciación real y efecto de valuación (Calvo et al., 2003) | TCRM | Aumenta en pesos el valor de la deuda en moneda extranjera. |
| Menor crecimiento y diferencial entre tasa y crecimiento (Neumeyer y Perri, 2005) | Crecimiento real | Achica el denominador y empeora el diferencial. |
| Respuesta fiscal | Resultado primario | Cambia el flujo que reduce o aumenta la deuda. |
| Costo de la deuda en dólares | Tasa de la FED (exógena) | Entra directamente en la tasa en dólares. |

Fuente: elaboración propia.

El canal cuasifiscal, que es el mayor costo de los pasivos remunerados del BCRA, operó en el período de estimación a través de la deuda consolidada. No se proyecta como un canal separado porque esos pasivos son mínimos desde 2024 (FMI, 2025, anexo II).

## 4.4 Identificación de los *shocks* domésticos

Los residuos del VAR, u, se relacionan con cuatro *shocks* estructurales, ε, mediante u = S ε. La matriz S impone las siguientes restricciones en el trimestre del impacto (Tabla 4.3):

- **Fiscal.** Se le descuenta al resultado primario su respuesta automática al ciclo, con una elasticidad de 0,25 respecto del crecimiento (Blanchard y Perotti, 2002; Girouard y André, 2005). Lo que queda es el *shock* fiscal discrecional. La política discrecional tarda más de un trimestre en reaccionar a la actividad (Blanchard y Perotti, 2002).
- **Actividad.** El crecimiento puede responder al *shock* fiscal dentro del trimestre; su propio *shock* es la parte del residuo que el *shock* fiscal no explica.
- **Bloque cambiario y de riesgo.** El EMBI+ y el TCRM responden en el trimestre a los *shocks* fiscal y de actividad, pero el resultado primario y el crecimiento no responden en el mismo trimestre a los *shocks* de ese bloque. Es el supuesto de rezagos de decisión y de información de Blanchard y Perotti (2002) aplicado a la política fiscal, y el de rigidez del producto en el trimestre que usan los VAR monetarios (Christiano et al., 1999). Dentro del bloque no se impone ningún orden con interpretación económica: se usa una ortonormalización arbitraria y solo se informa la contribución conjunta, que no depende de ella (Christiano et al., 1999).

**Tabla 4.3. Restricciones de impacto (S)**

| Variable | *Shock* fiscal | *Shock* de actividad | Bloque cambiario y de riesgo |
|---|---|---|---|
| Resultado primario | libre | 0,25 × respuesta del crecimiento | 0 |
| Crecimiento | libre | libre | 0 |
| EMBI+ | libre | libre | libre |
| TCRM | libre | libre | libre |

Fuente: elaboración propia sobre la base de Blanchard y Perotti (2002).

La elasticidad de 0,25 proviene de estimaciones para países de la OCDE (Girouard y André, 2005); para acotar su efecto, la simulación se repite con elasticidades de 0 y 0,5. La identificación también supone que el resultado primario no responda en el trimestre al tipo de cambio, cuando en Argentina los derechos de exportación dependen de él. Para evaluarlo se usan dos ordenamientos de Cholesky como robustez: uno que pone primero al resultado primario y otro que lo pone último.

## 4.5 Niveles, rezagos e inferencia

- **Variables en niveles.** El VAR se estima en niveles aunque algunas variables tengan raíz unitaria. Sims et al. (1990) muestran que las estimaciones siguen siendo consistentes sin imponer relaciones de cointegración, aunque la distribución de algunos estimadores no es la estándar; por eso la inferencia se hace con *bootstrap* y no con los errores de mínimos cuadrados. Las pruebas de raíz unitaria (ADF y KPSS) no permiten clasificar con claridad la mayoría de las series, y la prueba de Johansen (1991) sobre las variables en niveles no rechaza la ausencia de cointegración (Apéndice, sección A.2). Esa prueba no incluye los quiebres, que sesgan los valores críticos (Johansen et al., 2000), de modo que su resultado se toma como indicativo.
- **Muestra de estimación.** Todas las series cubren 1996-2025, y todas las especificaciones se estiman sobre la misma muestra efectiva, 1998T2-2025T4 (111 trimestres). Los primeros trimestres se usan como condiciones iniciales de los rezagos (la variación de la tasa de la FED con dos rezagos y hasta seis rezagos del VAR). Reservar el mismo número de observaciones para cualquier orden permite comparar los criterios de información entre órdenes (Lütkepohl, 2005, sec. 4.3).
- **Rezagos.** Se toma el mayor orden estable que no supera al que elige el criterio de información de Akaike (AIC). Un VAR es estable si todos los autovalores de su matriz compañera tienen módulo menor que uno, que es lo mismo que pedir que las raíces del polinomio característico queden fuera del círculo unitario; la estabilidad es la condición para que existan las respuestas al impulso y la simulación de largo plazo (Lütkepohl, 2005, cap. 2). Con datos trimestrales, Ivanov y Kilian (2005) recomiendan el AIC para el análisis de respuestas al impulso, porque usar menos rezagos de los necesarios distorsiona más las respuestas que usar de más. El AIC alcanza su mínimo en seis rezagos, el máximo considerado, pero los órdenes desde cuatro son inestables (autovalor máximo de 1,02 a 1,03). Se usan tres rezagos (autovalor máximo de 0,96). Entre los órdenes estables, el AIC, el criterio de Hannan-Quinn y el de Schwarz eligen dos, dos y uno; por eso la simulación se repite con dos rezagos (Capítulo 6). La prueba de Portmanteau multivariada (Hosking, 1980) rechaza la ausencia de autocorrelación residual al 5% (p = 0,036). Como el remuestreo de *shocks* supone independencia entre trimestres, se trata como una limitación de la simulación.
- **Intervalos de confianza.** Los residuos rechazan la normalidad (Jarque y Bera, 1987), y la volatilidad de las variables cambia entre subperíodos. Los intervalos se calculan con un *bootstrap* salvaje de diseño recursivo, válido con heterocedasticidad condicional de forma desconocida (Gonçalves y Kilian, 2004). En cada réplica se regenera también la deuda, con un VAR auxiliar que la incluye como quinta variable, de modo que la retroalimentación entre la deuda y el sistema esté presente en los datos simulados. Los coeficientes de rezago se corrigen por el sesgo de muestra pequeña con el procedimiento de Kilian (1998): una primera etapa de 100 réplicas mide el sesgo, y la estimación y cada réplica de la segunda etapa se corrigen por él, con una corrección reducida cuando la completa volvería inestable al VAR. La semilla es fija para que los resultados se puedan reproducir.
- **Persistencia de la estimación central.** El autovalor de mayor módulo del VAR estimado por mínimos cuadrados es 0,964. La estimación central usa los coeficientes corregidos por sesgo, con la corrección multiplicada por un factor δ = 0,9 para mantener la estabilidad, y su autovalor máximo es 0,9998, prácticamente una raíz unitaria. Con esa dinámica los *shocks* son muy persistentes, lo que eleva las probabilidades de no estabilización. Las réplicas del *bootstrap* generan los datos con un proceso cuyo factor δ es menor, de modo que los intervalos percentiles no quedan centrados en la estimación central, que se ubica cerca de su límite superior.

## 4.6 Simulación de Monte Carlo

**Escenario base.** Los senderos son los del análisis de sostenibilidad más reciente del FMI (2026, cuadro 6), publicado en mayo de 2026: crecimiento real g, deflactor del PIB π, tasa de interés efectiva i, resultado primario pb, ajuste stock-flujo sf e inflación relativa ri, que es la contribución de la depreciación nominal del escenario a la deuda en moneda extranjera. Antes de simular se verifica que la identidad, aplicada al stock de deuda del FMI, reproduzca su senda; el desvío máximo es de 0,1 puntos del PIB. Como robustez se usa el escenario de abril de 2025 (FMI, 2025, anexo II).

**Identidad de la deuda.** Para cada año t de 2026 a 2035:

d_t = d_{t-1} M_t − pb_t + sf_t + ri_t d_{t-1} / d^FMI_{t-1}

M_t = (1 + i_t + (1 − a) x_t)(1 + (1 − a) e_t) / ((1 + π_t)(1 + g_t))

donde a = 0,42 es la proporción de la deuda en pesos (diciembre de 2025), e_t es el desvío de la depreciación real que simula el SVARX y x_t es el desvío de la tasa en dólares (EMBI+ y FED). La inflación relativa del FMI se escala por el cociente entre la deuda simulada y la del FMI, porque es proporcional al stock en moneda extranjera. La tasa en dólares se reprecia gradualmente: cada año se refinancia la fracción λ = 18,0/63,6 ≈ 0,28, cociente entre las necesidades brutas de financiamiento promedio y la deuda promedio de los seis primeros años del escenario del FMI. Como esa fracción incluye la refinanciación de letras en pesos de corto plazo, se informa la sensibilidad a λ = 0,15 y 0,40.

**Algoritmo.**

1. El SVARX se simula trimestre a trimestre, en desvíos respecto del escenario base, durante 40 trimestres. Como la simulación es en desvíos, la constante, las variables binarias estacionales y las de quiebre no intervienen.
2. Los *shocks* estructurales se remuestrean de los 111 trimestres históricos, con reposición y como vectores, para conservar las colas gordas y la correlación entre variables (FMI, 2021, párr. 52).
3. Al final de cada año, los desvíos trimestrales se anualizan (suma para el crecimiento, promedio para el resultado primario y el EMBI+, variación de fin de año para el TCRM) y entran en la identidad.
4. La deuda simulada vuelve al sistema como desvío acumulado respecto de la senda base, multiplicada por los coeficientes de la deuda rezagada.

**Métrica de no estabilización.** Es la del FMI (2021, párr. 53 y anexo VI, nota 9): la deuda no se estabiliza en el año T si el resultado primario del escenario base es menor que el que la estabilizaría en esa trayectoria,

pb*_T = d_{T-1} (M_T − 1) + ri_T d_{T-1} / d^FMI_{T-1}.

Se mide en 2031, que es el último año del abanico de mediano plazo del informe del FMI (t + 5 desde 2026), y en 2035, el último año de su abanico de diez años.

**Estimación e intervalos.** La estimación central usa los parámetros corregidos por sesgo y 20.000 trayectorias; se informa su error de Monte Carlo. Los intervalos de 90% salen de 200 réplicas de parámetros con 1.000 trayectorias cada una.

**Tamaño del *shock* de la FED.** La tasa de la FED entra al modelo como variación trimestral, de modo que el desvío del nivel de la tasa respecto del escenario base es la suma acumulada de esas variaciones y persiste mientras no se revierta. Se usan dos escenarios. El primero es una suba de un desvío estándar de la variación trimestral de la tasa (0,50 puntos), la convención para medir respuestas en estos modelos: el nivel de la tasa queda 0,50 puntos por encima del base de 2026 a 2035. El segundo repite las variaciones trimestrales efectivas de la tasa de fondos federales de 2022 a 2025 (de 0,08% a 5,33% hasta fines de 2023 y a 3,90% en 2025): en 2026-2029 el nivel sube 5,25 puntos y luego baja 1,43, y desde entonces queda 3,82 puntos por encima del base hasta 2035.

**Variantes.**

- **Canal de tasas domésticas.** El mismo desvío del EMBI+ también reprecia la deuda en pesos, con la misma velocidad λ. El fundamento es la tasa de interés del país de Neumeyer y Perri (2005) y Uribe y Yue (2006): el costo del crédito para el soberano es la tasa internacional más la prima de riesgo, cualquiera sea la moneda. No se agrega una tasa en pesos como variable del VAR porque no hay una serie homogénea para 1996-2025.
- ***Shocks* como los del FMI.** Para saber cuánto del resultado depende de la forma de generar los *shocks*, se repite la simulación con el procedimiento del abanico del FMI (FMI, 2021, anexo VI; FMI y Mecanismo Europeo de Estabilidad, 2023). Se calculan los desvíos respecto de la media histórica de los cuatro impulsores anuales de la deuda (tasa real efectiva, crecimiento real, depreciación real y resultado primario, 1997-2025) y se los remuestrea como vectores en bloques de dos años consecutivos. La identidad, el punto de partida y la métrica son los mismos.
- **Otras.** Sin la retroalimentación de la deuda; deuda neta a valor libros, deuda bruta y deuda solo del Tesoro; sin los *shocks* del período de cesación de pagos y canje (2001T4-2005T3); ajuste stock-flujo en cero; resultado primario sin rentas de la propiedad (que incluyen las utilidades del BCRA, internas al perímetro consolidado); muestra desde 2004; punto de partida igual a la deuda consolidada neta del FMI (52,1% del PIB), que descuenta el FGS.

**Por qué la especificación principal es el SVARX.** El procedimiento del FMI genera *shocks* en forma reducida: no distingue un *shock* fiscal de uno cambiario ni aísla la tasa de la FED, de modo que no permite descomponer la incertidumbre por origen ni contrastar H2. La identificación sirve para separar la varianza de la deuda por bloque de *shocks* y para definir el *shock* fiscal. La probabilidad de no estabilización no depende de ella: los *shocks* estructurales reconstruyen los mismos residuos históricos, cualquiera sea la matriz S.

## 4.7 Contraste de las hipótesis

**Tabla 4.4. Medidas y criterios de contraste**

| Hipótesis | Medida | Criterio |
|---|---|---|
| H1a | (i) Resultado primario necesario en 2031 para que la probabilidad de no estabilización en 2031 baje a la estimación puntual del FMI para Argentina (1%), desplazando en la misma magnitud el resultado primario de todos los años 2026-2035 del escenario base, y (ii) contribución de cada bloque de *shocks* a la varianza de la deuda simulada en 2035 | El superávit primario "por sí solo no basta" si el necesario supera el máximo del Sector Público Nacional en 1996-2025: 3,6% del PIB en la suma de los cuatro trimestres a diciembre de 2004, con rentas de la propiedad (el máximo de la suma móvil de cuatro trimestres es 3,93%, en 2004T3, y sin rentas de la propiedad es 3,29%). La descomposición de la varianza se informa como complemento. |
| H1b | Probabilidad de que la deuda no se estabilice, con el escenario base del FMI, en 2031 y en 2035 | El límite inferior del intervalo de 90% supera la probabilidad del FMI para el mismo horizonte (contraste unilateral al 5%): 1,0% a mediano plazo y menos de 3% en el abanico de diez años (FMI, 2026). |
| H2 | Diferencia en esa probabilidad y en la deuda esperada entre cada escenario de la FED y el base | El intervalo de 90% de la diferencia excluye el cero. |

Fuente: elaboración propia.

El criterio (i) de H1a mide directamente lo que afirma la hipótesis: si con un superávit de la magnitud que la Argentina alcanzó en su mejor año la probabilidad de no estabilización sigue por encima de la que el FMI estima para el país, el superávit, por sí solo, no basta. El 1% es la estimación puntual del FMI para Argentina (FMI, 2026), no un umbral de riesgo bajo definido por el FMI. Como H1b se contrasta en dos horizontes y H2 en dos escenarios, se informa también si las conclusiones se sostienen con la corrección de Bonferroni, que usa los límites de 2,5%.

**Revisión de los criterios.** Los criterios de la Tabla 4.4 se revisaron después de la primera estimación, en octubre de 2026. El criterio original de H1a era la descomposición de la varianza: la hipótesis se consideraba respaldada si el intervalo de 90% de la diferencia entre la contribución de los *shocks* no fiscales y la del fiscal excluía el cero. Ese intervalo, [-4,8; 91,2], no cumple el criterio. Se adoptó el criterio de suficiencia porque mide directamente lo que afirma la hipótesis, y el Capítulo 6 informa los dos. Los tamaños de los *shocks* de la FED también se definieron en octubre de 2026.
