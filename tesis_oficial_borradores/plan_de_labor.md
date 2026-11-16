---
title: "Plan de labor"
subtitle: "Tesis final de grado. Facultad de Ciencias Económicas, Universidad Nacional de Cuyo"
---

Páez, Santiago. Legajo 34110

Chillón, Federico. Legajo 34394

Carricondo, Emiliano. Legajo 33396

Director: Pablo Mahnic

Noviembre de 2026

Título: Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos.

Palabras clave: deuda pública; sostenibilidad de la deuda; vectores autorregresivos estructurales; simulación de Monte Carlo; política monetaria de Estados Unidos.

# 1. Introducción y motivación del estudio

La historia económica argentina repite un ciclo conocido de endeudamiento externo, interrupción de los flujos de capital y cesación de pagos (Rapoport, 2020; Reinhart y Rogoff, 2009). El *default* de 2001 y la reestructuración de 2020 dejaron a la vista hasta qué punto la economía depende de la disponibilidad de divisas. La administración que asumió en diciembre de 2023 heredó un *stock* elevado de pasivos y un acceso muy limitado al crédito voluntario. A partir de 2024 el Tesoro pasó a registrar superávit primario y en diciembre de 2025 volvió a colocar un bono en dólares, bajo ley local y a una tasa de 9,26% anual (Secretaría de Finanzas, 2025). A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones (Oficina de Presupuesto del Congreso [OPC], 2026). A esa deuda hay que sumarle la que durante buena parte del período quedó en el balance del Banco Central de la República Argentina (BCRA), que absorbió liquidez con pasivos remunerados hasta llegar a 19,2% del producto interno bruto (PIB) en 2023 (Fondo Monetario Internacional [FMI], 2026, anexo II, cuadro 2).

El programa vigente con el FMI pone al superávit primario en el centro de la sostenibilidad de la deuda. El problema que motiva el estudio es si ese superávit alcanza para estabilizar la deuda en el mediano plazo o si el crecimiento, el tipo de cambio real y el riesgo país pesan más que el resultado fiscal. Con más de la mitad de la deuda federal bruta en moneda extranjera, una depreciación real puede mover el cociente de deuda más que varios años de ajuste fiscal.

La pregunta que nos planteamos en esta investigación es ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario condicionan la sostenibilidad de la deuda pública argentina en 2026-2035, y cuál es la probabilidad de que la deuda no se estabilice bajo el escenario base del FMI? De ella se desprende una pregunta específica: ¿cómo y en qué magnitud afectaría un endurecimiento de la política monetaria de la Reserva Federal de los Estados Unidos (FED) a la dinámica de la deuda y a esa probabilidad?

La respuesta interesa también por una razón institucional. La Ley 27.612 (2021) exige autorización del Congreso, mediante una ley, para el endeudamiento en moneda extranjera bajo legislación extranjera, y que los programas de financiamiento con el FMI también pasen por el Congreso. Esas decisiones se apoyan en evaluaciones de sostenibilidad, y la de referencia es la del propio FMI, que estima para Argentina una probabilidad de no estabilización de alrededor de 1% a mediano plazo y menor a 3% a diez años (FMI, 2026). Este proyecto busca aportar una segunda medición, construida con *shocks* identificados y sobre el mismo perímetro, punto de partida y escenario que usa el organismo, de modo que ambas puedan compararse.

El objetivo general es evaluar la dinámica de la deuda pública argentina a partir de sus determinantes macroeconómicos históricos (1996-2025), para proyectar su sostenibilidad en 2026-2035 y estimar la probabilidad de que no se estabilice. Los objetivos específicos son dos. El primero es estimar la probabilidad de que la deuda federal bruta no se estabilice en 2026-2035 bajo el escenario base del FMI y compararla con la que informa el organismo. El segundo es estimar cómo cambian la trayectoria de la deuda y esa probabilidad ante un endurecimiento de la política monetaria de la FED.

El trabajo parte de tres hipótesis. La primera (H1a) sostiene que el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario condicionan la sostenibilidad de la deuda, de manera que el superávit primario por sí solo no basta para estabilizarla en 2026-2035. La segunda (H1b) plantea que la probabilidad de que la deuda federal bruta no se estabilice es mayor que la que informa el FMI para esa misma deuda, que es de alrededor de 1% a mediano plazo (2031) y menor a 3% a diez años (2035) (FMI, 2026). La razón para esperarlo es metodológica: el propio FMI advierte que sus abanicos de probabilidad subestiman la incertidumbre, porque suponen que el nivel de deuda no retroalimenta a sus determinantes y dejan afuera las trayectorias en las que una deuda más alta eleva el riesgo país (FMI, 2021, anexo VI, párr. 6). El modelo de este proyecto incluye esa retroalimentación. La tercera (H2) afirma que un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda y su probabilidad de no estabilizarse. La forma en que se contrasta cada una se explica en la sección 3.

# 2. Antecedentes del tema

La revisión empieza por la teoría sobre qué determina la sostenibilidad de la deuda, sigue con las herramientas con que se la midió y sus límites, y termina con los resultados empíricos que ya se conocen. De ahí salen las variables del modelo y lo que todavía no se estudió.

## 2.1. Antecedentes teóricos

El punto de partida es el enfoque de la restricción externa. El crecimiento resulta de la acumulación de capital físico y humano y de la incorporación de tecnología, y en la Argentina buena parte de los bienes de capital y de los insumos que requiere esa acumulación se importa, de modo que para crecer hacen falta divisas (Díaz Alejandro, 1970). Con esas mismas divisas se paga la deuda en moneda extranjera, y por eso el endeudamiento externo deja a la economía expuesta a la disponibilidad de dólares (Calvo et al., 2003). Esta idea explica por qué, en el caso argentino, el tipo de cambio real y el riesgo país pueden pesar sobre la deuda tanto como el resultado fiscal.

Sobre esa base se apoya la discusión de la solvencia. Un gobierno es solvente si el valor presente de sus superávits primarios futuros alcanza para cubrir la deuda actual, y Bohn (1998) muestra que una condición suficiente es que el superávit responda positivamente al nivel de deuda. Que el gobierno reaccione, sin embargo, no asegura que la deuda se estabilice en un plazo relevante. Cuando la tasa de interés supera con holgura al crecimiento, el superávit necesario puede exceder lo que la economía es capaz de generar, y la fatiga fiscal que describen Ghosh et al. (2013) pone un techo a cuánto ajuste puede sostenerse en el tiempo.

Para seguir esa dinámica año a año se usa la identidad de acumulación de la deuda. El cociente entre la deuda y el PIB cambia por el diferencial entre la tasa de interés y el crecimiento, por el resultado primario y por el ajuste entre *stocks* y flujos, y cuando una parte de la deuda está en moneda extranjera también cambia con la depreciación real. La identidad permite así separar lo que aporta el esfuerzo fiscal de lo que aporta el efecto de valuación. También obliga a definir el perímetro. Cuando el banco central financia al Tesoro o absorbe liquidez con pasivos remunerados, la restricción que importa es la del sector público consolidado, y por eso el FMI (2021) incluye esos pasivos en la deuda pública cuando pueden financiar al gobierno o representan un riesgo fiscal material.

Los determinantes que entran en la identidad, a su vez, reciben el impacto de las condiciones externas. Una suba de la tasa de la FED eleva la prima de riesgo de los países emergentes (Uribe y Yue, 2006), deprecia su tipo de cambio real y reduce su crecimiento (Neumeyer y Perri, 2005). Cada uno de esos canales llega a la deuda por un término distinto de la identidad, y a ellos se agrega el encarecimiento directo de la deuda en dólares.

Como ninguno de estos determinantes se conoce de antemano, la sostenibilidad se expresa como la probabilidad de que la deuda no se estabilice, calculada con simulaciones (Celasun et al., 2006; FMI, 2021). El FMI considera que la deuda no se estabiliza cuando el resultado primario previsto es menor que el que la mantendría constante, y su guía lleva esa definición a la práctica promediando las variables a lo largo de la trayectoria simulada, sin variación del tipo de cambio real ni ajuste *stock*-flujo (FMI, 2022, recuadro 3).

## 2.2. Antecedentes metodológicos

Los enfoques contables proyectan una sola trayectoria de la deuda. Rodríguez (2023) muestra que el cociente deuda/PIB, mirado de forma aislada, no alcanza para evaluar la solvencia si no se consideran las tasas de interés y el ciclo, y Sanches (2019) descompone su dinámica en componentes. Ninguno de los dos estima cómo se transmiten los *shocks* entre el resultado fiscal, el riesgo país, el tipo de cambio y la actividad, ni asigna una probabilidad a la trayectoria.

Esa limitación es la que intentaron resolver los modelos de simulación estocástica. Celasun et al. (2006), en un documento de trabajo del FMI, proponen combinar un modelo de vectores autorregresivos (VAR) sobre los determinantes de la deuda con una función de reacción fiscal y la identidad de acumulación, de manera de obtener una distribución de trayectorias en lugar de un único escenario. Medeiros (2012) aplica la misma arquitectura en un trabajo para la Comisión Europea, y el FMI la incorporó a su Marco de Riesgo Soberano y Sostenibilidad de la Deuda (FMI, 2021, 2022), que es el que utiliza para evaluar a la Argentina (FMI, 2025, 2026). El marco del FMI tiene, de todos modos, un límite importante para la pregunta de este proyecto: genera los *shocks* a partir de la historia de los determinantes en forma reducida, sin identificar su origen, y por lo tanto no permite saber si el riesgo proviene de la política fiscal, del tipo de cambio o del contexto externo.

Para resolver esa limitación e identificar el origen de los *shocks* hace falta un VAR estructural (SVAR), que descompone los residuos del modelo en *shocks* con interpretación económica a partir de restricciones. Blanchard y Perotti (2002) identifican el *shock* fiscal con restricciones de impacto, bajo el argumento de que los rezagos de decisión impiden que la política fiscal discrecional responda a la actividad dentro del mismo trimestre, mientras que la respuesta automática del resultado primario al ciclo se fija con una elasticidad estimada fuera del modelo. La descomposición de Cholesky es un caso particular de esta lógica, en el que las variables se ordenan de forma recursiva, y como sus resultados dependen del orden elegido se la utilizará solo como prueba de robustez. Favero y Giavazzi (2007) agregan una advertencia que también se toma en cuenta: un VAR fiscal que omite la retroalimentación de la deuda está mal especificado, porque el nivel de deuda condiciona tanto la política fiscal como las tasas.

Existen otras dos formas de identificación que se descartan. Uhlig (2005) propone identificar los *shocks* exigiendo únicamente el signo de algunas respuestas, lo que tiene la ventaja de imponer supuestos más débiles. El costo es que el procedimiento identifica un conjunto de modelos y no uno solo (Fry y Pagan, 2011), con lo cual la descomposición de la varianza que necesita este proyecto quedaría indeterminada. También obligaría a fijar de antemano el signo de respuestas que justamente se quieren medir, como la del riesgo país ante un *shock* fiscal. Las restricciones de largo plazo de Blanchard y Quah (1989) tampoco resultan adecuadas, porque exigen suponer que el tipo de cambio real es neutral en el largo plazo, algo difícil de sostener para la Argentina.

## 2.3. Resultados ya conocidos

La evidencia empírica disponible sugiere que el superávit, por sí solo, tiene un alcance limitado. Ando et al. (2025) encuentran que los ajustes fiscales discrecionales reducen poco el cociente de deuda y que solo lo hacen de forma duradera cuando se aplican en fases de expansión, y Ghosh et al. (2013) muestran que la respuesta del superávit a la deuda se debilita a medida que la deuda crece. En economías con deuda dolarizada suele pesar más el tipo de cambio. Calvo et al. (2003) explican cómo una interrupción repentina de capitales encarece la deuda en dólares a través de la depreciación real y ubican a la Argentina en el peor extremo de los casos comparados, tanto por su grado de apertura como por su descalce de monedas. Levy Yeyati y Sturzenegger (2023) matizan este diagnóstico al mostrar que el patrimonio neto del sector público argentino es menos sensible a la devaluación que el cociente de deuda.

La literatura regional también encuentra efectos del contexto externo. Adler y Sosa (2013) encuentran que el índice de volatilidad VIX es la variable global con efectos más robustos sobre la sostenibilidad de la deuda en América Latina. Uribe y Yue (2006) y Neumeyer y Perri (2005) muestran que los *shocks* de la tasa de Estados Unidos operan sobre todo a través del riesgo soberano. Frente a esta evidencia, que muestra cuánto pesan el tipo de cambio y las condiciones externas, la evaluación vigente del FMI es favorable: estima para la deuda federal bruta argentina una probabilidad de no estabilización de alrededor de 1% a mediano plazo y menor a 3% a diez años, y califica la deuda como sostenible aunque no con alta probabilidad (FMI, 2026).

## 2.4. Variables a incluir

De la revisión anterior surgen las variables del modelo. Los cuatro determinantes que aparecen en la identidad del FMI son el crecimiento real, el resultado primario, el costo del financiamiento, que se mide con el riesgo país, y el tipo de cambio real. A ellos se suman dos variables externas, la tasa de la FED, por los canales que describen Uribe y Yue (2006) y Neumeyer y Perri (2005), y el VIX, por los resultados de Adler y Sosa (2013). La deuda entra rezagada en el sistema, como proponen Favero y Giavazzi (2007).

## 2.5. Aporte de esta investigación

En la literatura revisada no se encontró ningún trabajo que reúna, para el caso argentino, tres elementos que este proyecto combina. El primero es una probabilidad de no estabilización calculada con *shocks* identificados y sobre el mismo perímetro, el mismo escenario y la definición operativa del FMI, ya que los estudios que identifican *shocks* trabajan con paneles de países y los que estudian la deuda argentina no los identifican. El segundo es la traducción del efecto de la política monetaria de Estados Unidos en un cambio de esa probabilidad. El tercero es la dinámica de la deuda consolidada con el BCRA, que el FMI (2021) admite incluir en la deuda pública pero que, en su análisis de la Argentina, presenta solo como un cuadro de *stocks* (FMI, 2026, anexo II). A esto se suma una medida complementaria a la del FMI, una métrica anual de no estabilización que conserva la valuación de la deuda en moneda extranjera de cada año, aspecto que la definición del organismo deja afuera por construcción.

# 3. Metodología

## 3.1. Datos

El estudio es cuantitativo, explicativo y longitudinal, retrospectivo en la estimación (1996-2025) y prospectivo en la simulación (2026-2035). La unidad de análisis es la economía argentina, observada como serie temporal trimestral. La ventana 1996T1-2025T4 se eligió porque abarca regímenes cambiarios y fiscales muy distintos, desde la convertibilidad y el *default* hasta el desendeudamiento, el reendeudamiento y el programa actual con el FMI. Las ecuaciones se estimarán con los trimestres 1998T2-2025T4 (111 observaciones), porque la serie trimestral de deuda federal del MECON empieza en 1998T1 y la deuda entra rezagada; los trimestres anteriores funcionan como condiciones iniciales de los demás rezagos. La Tabla 1 resume las variables, sus indicadores y sus fuentes.

Tabla 1. Variables, indicadores y fuentes

| Variable | Indicador | Fuente | Rol |
|---|---|---|---|
| Deuda federal bruta | Deuda bruta de la Administración Central, % del PIB | Ministerio de Economía (MECON); *stock* inicial del FMI (2026) | Entra rezagada en las cuatro ecuaciones del SVARX y se acumula con la identidad contable (especificación principal) |
| Deuda consolidada con el BCRA | Deuda del Tesoro y del BCRA neta de tenencias cruzadas, % del PIB | MECON y BCRA; *stock* inicial del FMI (2026) | Ídem (extensión, estimada desde 2002) |
| Resultado primario | Resultado del Sector Público Nacional sin rentas de la propiedad, % del PIB | MECON | Endógena |
| Crecimiento | Variación trimestral del PIB real | Instituto Nacional de Estadística y Censos (INDEC) | Endógena |
| Riesgo país | Diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), en puntos básicos | J.P. Morgan, serie diaria publicada por Ámbito Financiero; empalme para 1996T1-1998T3 | Endógena |
| Tipo de cambio real | Tipo de cambio real multilateral (TCRM) | BCRA; empalme para 1996 con el Banco de Pagos Internacionales (BIS) | Endógena |
| Política monetaria de Estados Unidos | Tasa de fondos federales; tasa sombra en el límite cero (Wu y Xia, 2016) | Reserva Federal | Exógena |
| Condiciones financieras globales | VIX | Bolsa de Opciones de Chicago (CBOE) | Exógena |
| Mandato presidencial | Una variable binaria por mandato | Elaboración propia | Control determinista |
| Escenario base | Crecimiento, deflactor, tasa efectiva, resultado primario, ajuste *stock*-flujo e inflación relativa, 2026-2035 | FMI (2026), cuadro 6 | Supuesto de la simulación |

Fuente: elaboración propia.

Todos los datos son secundarios. Cada serie se evaluará según la institución que la produce, su definición y cobertura, sus cambios metodológicos, como el cambio de base del PIB en 2004 o los tramos del resultado primario de 2007 y 2015, y su coherencia con otra fuente. La deuda federal bruta se contrastará con la que publica el FMI, y la simulación partirá del *stock* del organismo a fines de 2025, equivalente a 80,3% del PIB. La deuda consolidada se obtendrá sumando a la deuda bruta los pasivos remunerados del BCRA y restando la deuda del Tesoro en poder del banco central y los depósitos del Tesoro en él. Esta serie se estimará desde 2002, porque hasta entonces el BCRA operaba con la autonomía de la Carta Orgánica de 1992 y bajo la convertibilidad, de modo que la consolidación no tiene fundamento en el criterio del FMI. En cuanto al resultado primario, se tomará la serie sin rentas de la propiedad, ya que el FMI excluye las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4) y la fuente pública no permite separarlas del resto de esas rentas.

Dos series no tienen dato publicado para toda la ventana y deberán completarse. La serie diaria del EMBI comienza en diciembre de 1998. Para 1996T1-1998T3 se usará el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA y la tasa de fondos federales, con una relación que se estimará en la superposición 1998T4-2001T3 y se validará con un pronóstico fuera de muestra. El TCRM del BCRA comienza en enero de 1997, y el año 1996 se reconstruirá encadenándolo con las variaciones del tipo de cambio real efectivo del BIS. Algo similar ocurre con la tasa de la FED, que alterna entre la tasa efectiva y la tasa sombra; en las cuatro transiciones entre ambas (2009T1, 2016T1, 2020T2 y 2022T1) la variación se calculará de modo que el cambio de serie no se confunda con un cambio de política. Para comprobar que los resultados no dependen de estas reconstrucciones, todo el análisis se repetirá con datos desde 1999.

## 3.2. Análisis iniciales

El análisis comienza por las propiedades estadísticas de las series. Se aplicarán las pruebas de raíz unitaria de Dickey y Fuller (1979) aumentada (ADF) y de Kwiatkowski et al. (1992), conocida como KPSS, la prueba de Zivot y Andrews (1992), que admite un quiebre, y el procedimiento de Bai y Perron (2003) para detectar quiebres múltiples, que luego entrarán al modelo como variables binarias. Con esos resultados se definirá cómo entra cada serie al modelo. El crecimiento es la variación trimestral del PIB real, y el resultado primario, el EMBI y el TCRM entrarán en niveles. Un VAR en niveles se estima de forma consistente aunque alguna serie tenga raíz unitaria (Sims et al., 1990); como en ese caso algunos estimadores no tienen distribución estándar, la inferencia se hará por *bootstrap*. Antes de estimar se comprobará con la prueba de Johansen (1991) que las series no estén cointegradas, porque de estarlo correspondería un modelo de corrección de errores y no un VAR.

## 3.3. Estimación y simulación

El SVARX tendrá cuatro variables endógenas (resultado primario, crecimiento, EMBI y TCRM) y, como variables exógenas, la variación de la tasa de la FED con dos rezagos, el VIX y variables binarias estacionales, de quiebre y por mandato presidencial, cuya significancia conjunta se evaluará con pruebas de Wald y de razón de verosimilitud. Las binarias por mandato marcan el período de cada gobierno, cuyas fechas fija el calendario electoral salvo en los cambios de gobierno de la crisis de 2001-2003. La política económica en sí, que responde a la economía, queda recogida en el resultado primario, que es endógeno. Estas binarias controlan los cambios de régimen entre administraciones, no intervienen en la simulación, que se hace en desvíos respecto del escenario base, y todos los resultados se informarán también sin ellas. La deuda entrará rezagada en las cuatro ecuaciones y se irá acumulando con la identidad contable. El número de rezagos se elegirá con el criterio de Schwarz entre los órdenes que den un sistema estable, como recomiendan Ivanov y Kilian (2005) para datos trimestrales con menos de 120 observaciones. Si los residuos de ese orden muestran autocorrelación según la prueba Portmanteau con 12 rezagos al 5%, se tomará el menor orden mayor que la elimine (Lütkepohl, 2005). Si ninguno la elimina, se usará el orden del criterio de Hannan-Quinn, la autocorrelación que quede se informará como una limitación y los resultados se presentarán también con uno y con tres rezagos.

La identificación de los *shocks* seguirá a Blanchard y Perotti (2002) para el bloque fiscal y de actividad, mientras que el EMBI y el TCRM formarán un bloque cambiario y de riesgo identificado en conjunto. Como prueba de robustez se usarán dos ordenamientos de Cholesky, con el resultado primario primero y último, y elasticidades cíclicas de 0 y 0,5. Los intervalos de confianza de 90% se obtendrán por *bootstrap* de bloques móviles de cuatro trimestres, con diseño recursivo (Brüggemann et al., 2016), 1.000 réplicas y percentiles de Hall (1992); para las participaciones y varianzas, que son magnitudes acotadas, se usarán percentiles simples. Con el modelo estimado se medirán la reacción del resultado primario ante el nivel de deuda y la contribución de cada *shock* a la varianza de la deuda.

El modelo estimado alimentará una simulación de Monte Carlo de la deuda entre 2026 y 2035 sobre el escenario base del FMI (2026), desde su *stock* inicial. Los *shocks* estructurales se remuestrearán de la historia en bloques de ocho trimestres, en línea con los bloques de dos años que usa el FMI (2021, anexo VI), y el VIX y la tasa de la FED seguirán procesos autorregresivos de primer orden. La no estabilización se medirá con la definición operativa del FMI (FMI, 2022, recuadro 3) y, como complemento, con la métrica anual.

Las hipótesis se contrastarán con criterios fijados de antemano. H1a se considerará respaldada si se cumplen dos condiciones. La primera es que la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supere a la del *shock* fiscal, con un intervalo de 90% de la diferencia que excluya el cero. La segunda es que, al desplazar en la misma magnitud el resultado primario de todos los años hasta que el de 2031 alcance su máximo de 1996-2025, la probabilidad de no estabilización en 2031, medida con la definición del FMI, siga por encima del 1%. H1b se respaldará si el límite inferior del intervalo de 90% supera la cifra del FMI tanto en 2031 (1%) como en 2035 (3%), según la definición operativa del organismo, y se informará también la corrección de Bonferroni. Para H2 se compararán con el escenario base dos escenarios de la FED, uno con un nivel de la tasa un desvío estándar más alto en forma permanente desde 2026T1 y otro que repite la senda de 2022-2025. La hipótesis se respaldará si el intervalo de 90% de la diferencia excluye el cero en 2035, tanto en la probabilidad como en la deuda esperada, y se considerará parcialmente respaldada si eso ocurre en una sola medida o en un solo escenario.

La robustez de los resultados se evaluará con un conjunto de variantes. Se repetirá el ejercicio con la deuda consolidada, sin las binarias presidenciales, con el resultado primario con rentas, con el canal de tasas en pesos y sin retroalimentación de la deuda. También se probarán uno y tres rezagos, las identificaciones alternativas ya mencionadas, la exclusión de los *shocks* del período de cesación de pagos, muestras desde 1999 y desde 2004, la eliminación de los quiebres, un ajuste *stock*-flujo nulo, dos velocidades de refinanciación, el escenario del FMI de 2025 y la corrección de sesgo de Kilian (1998). Y se aplicará a la historia argentina el procedimiento de *shocks* del propio FMI.

Para saber si el superávit alcanza o si otros determinantes pesan más hay que separar el *shock* fiscal de los cambiarios, de riesgo y externos. El SVAR permite hacerlo; el marco del FMI, que genera los *shocks* en forma reducida, no. Como la deuda se acumula con la identidad contable y no con una ecuación estimada, la simulación distingue también el tramo en pesos del tramo en moneda extranjera y capta el efecto de valuación de la depreciación real. Con más de la mitad de la deuda en dólares, ese efecto puede mover el cociente más que el ajuste fiscal.

El diseño también hace posible la comparación con la evaluación oficial. Al usar el perímetro, el punto de partida, el escenario y la definición operativa del FMI, la diferencia con su cifra proviene sobre todo de la manera de generar los *shocks*. La tasa de la FED entra al modelo como variable exógena, lo que permite medir su efecto como un multiplicador dinámico sin depender de cómo se identifiquen los *shocks* internos, del modo en que Canova (2005) trata los *shocks* de Estados Unidos sobre América Latina.

El proyecto puede hacerse con la información disponible. Con 111 trimestres, un sistema de cuatro variables y dos rezagos puede estimarse, y el *bootstrap* por bloques evita suponer normalidad en series atravesadas por crisis y cambios de régimen. Como los datos son públicos y la estimación se programa en Python con bibliotecas de uso libre, el ejercicio puede replicarse y actualizarse con cada nuevo informe del FMI.

# Referencias bibliográficas

Adler, G., y Sosa, S. (2013). *External conditions and debt sustainability in Latin America* (IMF Working Paper No. 13/27). Fondo Monetario Internacional.

Ando, S., Mishra, P., Patel, N., Peralta-Alva, A., y Presbitero, A. F. (2025). Fiscal consolidation and public debt. *Journal of Economic Dynamics and Control*, *170*, artículo 104998. https://doi.org/10.1016/j.jedc.2024.104998

Bai, J., y Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics*, *18*(1), 1-22. https://doi.org/10.1002/jae.659

Blanchard, O. J., y Quah, D. (1989). The dynamic effects of aggregate demand and supply disturbances. *American Economic Review*, *79*(4), 655-673.

Blanchard, O., y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. *Quarterly Journal of Economics*, *117*(4), 1329-1368. https://doi.org/10.1162/003355302320935043

Bohn, H. (1998). The behavior of U.S. public debt and deficits. *Quarterly Journal of Economics*, *113*(3), 949-963. https://doi.org/10.1162/003355398555793

Brüggemann, R., Jentsch, C., y Trenkler, C. (2016). Inference in VARs with conditional heteroskedasticity of unknown form. *Journal of Econometrics*, *191*(1), 69-85. https://doi.org/10.1016/j.jeconom.2015.10.004

Calvo, G. A., Izquierdo, A., y Talvi, E. (2003). *Sudden stops, the real exchange rate, and fiscal sustainability: Argentina's lessons* (NBER Working Paper No. 9828). National Bureau of Economic Research. https://doi.org/10.3386/w9828

Canova, F. (2005). The transmission of US shocks to Latin America. *Journal of Applied Econometrics*, *20*(2), 229-251. https://doi.org/10.1002/jae.837

Celasun, O., Debrun, X., y Ostry, J. D. (2006). *Primary surplus behavior and risks to fiscal sustainability in emerging market countries: A "fan-chart" approach* (IMF Working Paper No. 06/67). Fondo Monetario Internacional. https://doi.org/10.5089/9781451863277.001

Díaz Alejandro, C. F. (1970). *Essays on the economic history of the Argentine Republic*. Yale University Press.

Dickey, D. A., y Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association*, *74*(366), 427-431. https://doi.org/10.2307/2286348

Favero, C., y Giavazzi, F. (2007). *Debt and the effects of fiscal policy* (NBER Working Paper No. 12822). National Bureau of Economic Research. https://doi.org/10.3386/w12822

Fondo Monetario Internacional [FMI]. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper No. 2021/003). https://doi.org/10.5089/9781513568324.007

Fondo Monetario Internacional [FMI]. (2022). *Staff guidance note on the Sovereign Risk and Debt Sustainability Framework for market access countries* (IMF Policy Paper No. 2022/039). https://doi.org/10.5089/9798400216862.007

Fondo Monetario Internacional [FMI]. (2025). *Argentina: Request for an extended arrangement under the Extended Fund Facility* (IMF Country Report No. 25/95). https://doi.org/10.5089/9798229009188.002

Fondo Monetario Internacional [FMI]. (2026). *Argentina: 2026 Article IV consultation, second review under the extended arrangement under the Extended Fund Facility, requests for a waiver of nonobservance of a performance criterion, modification of performance criteria, and financing assurances review* (IMF Country Report No. 26/105). https://doi.org/10.5089/9798229046831.002

Fry, R., y Pagan, A. (2011). Sign restrictions in structural vector autoregressions: A critical review. *Journal of Economic Literature*, *49*(4), 938-960. https://doi.org/10.1257/jel.49.4.938

Ghosh, A. R., Kim, J. I., Mendoza, E. G., Ostry, J. D., y Qureshi, M. S. (2013). Fiscal fatigue, fiscal space and debt sustainability in advanced economies. *The Economic Journal*, *123*(566), F4-F30. https://doi.org/10.1111/ecoj.12010

Hall, P. (1992). *The bootstrap and Edgeworth expansion*. Springer. https://doi.org/10.1007/978-1-4612-4384-7

Ivanov, V., y Kilian, L. (2005). A practitioner's guide to lag order selection for VAR impulse response analysis. *Studies in Nonlinear Dynamics and Econometrics*, *9*(1), artículo 2. https://doi.org/10.2202/1558-3708.1219

Johansen, S. (1991). Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models. *Econometrica*, *59*(6), 1551-1580. https://doi.org/10.2307/2938278

Kilian, L. (1998). Small-sample confidence intervals for impulse response functions. *Review of Economics and Statistics*, *80*(2), 218-230. https://doi.org/10.1162/003465398557465

Kwiatkowski, D., Phillips, P. C. B., Schmidt, P., y Shin, Y. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root: How sure are we that economic time series have a unit root? *Journal of Econometrics*, *54*(1-3), 159-178. https://doi.org/10.1016/0304-4076(92)90104-Y

Levy Yeyati, E., y Sturzenegger, F. (2023). A balance-sheet approach to fiscal sustainability. *Fiscal Studies*, *44*(1), 61-84. https://doi.org/10.1111/1475-5890.12319

Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública. (2021, 3 de marzo). Boletín Oficial de la República Argentina.

Lütkepohl, H. (2005). *New introduction to multiple time series analysis*. Springer.

Medeiros, J. (2012). *Stochastic debt simulation using VAR models and a panel fiscal reaction function: Results for a selected number of countries* (European Economy Economic Papers No. 459). Comisión Europea. https://doi.org/10.2765/26084

Neumeyer, P. A., y Perri, F. (2005). Business cycles in emerging economies: The role of interest rates. *Journal of Monetary Economics*, *52*(2), 345-380. https://doi.org/10.1016/j.jmoneco.2004.04.011

Oficina de Presupuesto del Congreso [OPC]. (2026). *Operaciones de deuda pública, julio 2026*.

Rapoport, M. (2020). *Historia económica, política y social de la Argentina (1880-2003)*. Crítica.

Reinhart, C. M., y Rogoff, K. S. (2009). *This time is different: Eight centuries of financial folly*. Princeton University Press.

Rodríguez, A. (2023). Financiamiento y sostenibilidad de la deuda pública: El caso de la economía argentina (2001-2022). *Ciencias Económicas*, *2*(20), e0032. https://doi.org/10.14409/rce.2023.20.e0032

Sanches, P. (2019). *Análisis de la sostenibilidad de la deuda soberana argentina. 2019-2023* [Tesis de maestría]. Universidad Torcuato Di Tella.

Secretaría de Finanzas. (2025, 10 de diciembre). *Resultado de licitación del Bono del Tesoro Nacional en dólares estadounidenses 6,50% con vencimiento 30 de noviembre de 2029* [Comunicado]. Ministerio de Economía de la Nación. https://www.argentina.gob.ar/noticias/resultado-de-licitacion-del-bono-del-tesoro-nacional-en-dolares-estadounidenses-650-con

Sims, C. A., Stock, J. H., y Watson, M. W. (1990). Inference in linear time series models with some unit roots. *Econometrica*, *58*(1), 113-144. https://doi.org/10.2307/2938337

Uhlig, H. (2005). What are the effects of monetary policy on output? Results from an agnostic identification procedure. *Journal of Monetary Economics*, *52*(2), 381-419. https://doi.org/10.1016/j.jmoneco.2004.05.007

Uribe, M., y Yue, V. Z. (2006). Country spreads and emerging countries: Who drives whom? *Journal of International Economics*, *69*(1), 6-36. https://doi.org/10.1016/j.jinteco.2005.04.003

Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking*, *48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300

Zivot, E., y Andrews, D. W. K. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. *Journal of Business and Economic Statistics*, *10*(3), 251-270. https://doi.org/10.1080/07350015.1992.10509904
