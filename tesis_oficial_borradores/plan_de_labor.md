---
title: "Plan de labor"
subtitle: "Tesis final de grado. Facultad de Ciencias Económicas, Universidad Nacional de Cuyo"
---

Páez, Santiago. Legajo 34110

Chillón, Federico. Legajo 34394

Carricondo, Emiliano. Legajo 33396

Director: Pablo Mahnic

Octubre de 2026

**Título:** Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos.

**Palabras clave:** deuda pública; sostenibilidad de la deuda; vectores autorregresivos estructurales; simulación de Monte Carlo; política monetaria de Estados Unidos.

# 1. Introducción: motivación del estudio

**Contexto.** La historia argentina muestra un ciclo repetido de endeudamiento externo, interrupción de los flujos de capital y cesación de pagos (Reinhart y Rogoff, 2009; Rapoport, 2020). El *default*[^en-default] de 2001 y la reestructuración de 2020 dejaron en evidencia una economía condicionada por la disponibilidad de divisas. La administración que asumió en diciembre de 2023 recibió un *stock*[^en-stock] elevado de pasivos y un acceso muy limitado al crédito voluntario. Desde 2024 el Tesoro registra superávit primario, y en diciembre de 2025 volvió a colocar un bono en dólares, bajo ley local y a una tasa de 9,26% anual (Secretaría de Finanzas, 2025). A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones (Oficina de Presupuesto del Congreso [OPC], 2026). Durante buena parte del período, el Banco Central de la República Argentina (BCRA) absorbió liquidez con pasivos remunerados que llegaron a 19,2% del producto interno bruto (PIB) en 2023 (Fondo Monetario Internacional [FMI], 2026, anexo II, cuadro 2), de modo que una parte del endeudamiento público no aparecía en la deuda del Tesoro.

**Problema.** El superávit primario es la condición que el programa vigente con el FMI pone en el centro de la sostenibilidad de la deuda. El problema que motiva el estudio es si ese superávit alcanza para estabilizar la deuda en el mediano plazo o si el crecimiento, el tipo de cambio real y el riesgo país la condicionan más que el resultado fiscal. Con más de la mitad de la deuda federal bruta en moneda extranjera, una depreciación real puede mover el cociente de deuda más que varios años de ajuste fiscal.

**Por qué importa.** La Ley 27.612 (2021) exige una ley especial para emitir deuda en moneda extranjera bajo legislación extranjera por encima del máximo del presupuesto y una ley que apruebe cada programa con el FMI. Esas decisiones requieren evaluaciones de sostenibilidad, y la evaluación probabilística de referencia es la del FMI, que estima para Argentina una probabilidad de no estabilización de alrededor de 1% a mediano plazo y menos de 3% a diez años (FMI, 2026). El proyecto aporta una segunda medida, con *shocks*[^en-shock] identificados y sobre el mismo perímetro, punto de partida y escenario que usa el organismo.

**Preguntas de investigación.**

- Pregunta general: ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario de Argentina condicionan la sostenibilidad de la deuda pública en 2026-2035, y cuál es la probabilidad de que la deuda no se estabilice bajo el escenario base del FMI?
- Pregunta específica: ¿cómo y en qué magnitud impactaría un endurecimiento de la política monetaria de la Reserva Federal de los Estados Unidos (FED) sobre la dinámica de la deuda y sobre su probabilidad de no estabilizarse en 2026-2035?

**Objetivo general.** Evaluar la dinámica de la deuda pública argentina a partir de sus determinantes macroeconómicos históricos (1996-2025), para proyectar su sostenibilidad en 2026-2035 y estimar la probabilidad de que no se estabilice.

**Objetivos específicos.**

1. Construir series trimestrales de la deuda bruta del gobierno federal y de la deuda consolidada con el BCRA entre 1996 y 2025, y contrastarlas con los *stocks* que publica el FMI.
2. Establecer las propiedades estadísticas de las series: raíz unitaria, quiebres estructurales y cointegración.
3. Estimar un modelo de vectores autorregresivos estructural con variables exógenas (SVARX) en el que el crecimiento, el resultado primario, el riesgo país y el tipo de cambio real interactúan con la deuda rezagada, con la tasa de la FED y la volatilidad global como variables exógenas.
4. Medir la reacción del resultado primario ante el nivel de deuda y la contribución de los *shocks* fiscal, de actividad, cambiario y de riesgo y externo a la varianza de la deuda.
5. Simular la distribución de trayectorias de la deuda federal bruta en 2026-2035 bajo el escenario base del FMI, calcular la probabilidad de que no se estabilice y compararla con la del FMI; repetir el ejercicio con la deuda consolidada con el BCRA.
6. Estimar el efecto de un endurecimiento de la política monetaria de la FED sobre esa distribución.

**Hipótesis.**

- **H1a.** El crecimiento, el tipo de cambio real, el riesgo país y el resultado primario condicionan la sostenibilidad de la deuda, de modo que el superávit primario, por sí solo, no basta para estabilizarla en 2026-2035.
- **H1b.** La probabilidad de que la deuda federal bruta no se estabilice es mayor que la que informa el FMI para esa misma deuda: alrededor de 1% a mediano plazo (2031) y menos de 3% a diez años (2035) (FMI, 2026).
- **H2.** Un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda y su probabilidad de no estabilizarse.

Los criterios con que se contrasta cada hipótesis se presentan en la sección 3.

# 2. Antecedentes del tema

Esta sección resume qué se sabe del tema y qué se hizo antes, en tres planos: los antecedentes teóricos, que dicen qué determina la sostenibilidad de la deuda; los metodológicos, que dicen qué herramientas sirven para medirla y cuáles no, y los resultados ya conocidos. Cierra con las variables que esos antecedentes indican incluir y con las ideas nuevas que aporta el proyecto.

## 2.1. Antecedentes teóricos

**Restricción externa.** En una economía que necesita divisas para crecer y para pagar su deuda, el endeudamiento en moneda extranjera la expone a la disponibilidad de dólares (Díaz Alejandro, 1970; Calvo et al., 2003). Por esa vía, el tipo de cambio real y el riesgo país pesan sobre la deuda tanto como el resultado fiscal.

**Solvencia y regla de reacción fiscal.** El gobierno es solvente si el valor presente de sus superávits primarios futuros cubre la deuda actual. Bohn (1998) muestra que una condición suficiente es que el superávit primario responda positivamente al nivel de deuda. Esa respuesta no garantiza que la deuda se estabilice en un horizonte relevante: si el diferencial entre la tasa de interés y el crecimiento es alto, el superávit necesario puede superar lo que la economía genera. La fatiga fiscal (Ghosh et al., 2013) pone un techo a cuánto superávit puede sostenerse.

**Identidad de la deuda y perímetro.** El cociente entre la deuda y el PIB cambia por el diferencial entre la tasa de interés y el crecimiento, por el resultado primario, por el ajuste entre *stocks* y flujos y, cuando parte de la deuda está en moneda extranjera, por la depreciación real. Esta identidad separa el efecto del esfuerzo fiscal del efecto de valuación. Cuando el banco central financia al Tesoro o absorbe liquidez con pasivos remunerados, la restricción relevante es la del sector público consolidado, y el FMI (2021) incluye esos pasivos en la deuda pública cuando pueden financiar al gobierno o representan un riesgo fiscal material.

**Transmisión externa.** Una suba de la tasa de la FED eleva la prima de riesgo de los emergentes (Uribe y Yue, 2006), deprecia su tipo de cambio real y reduce su crecimiento (Neumeyer y Perri, 2005). Cada canal entra en la identidad de la deuda por un término distinto, y a ellos se suma el costo directo de la deuda en dólares.

**Sostenibilidad en sentido probabilístico.** Como los determinantes de la deuda son inciertos, la sostenibilidad se expresa como la probabilidad de que la deuda no se estabilice, construida con simulaciones (Celasun et al., 2006; FMI, 2021). El FMI define la no estabilización como un resultado primario previsto menor que el que estabilizaría la deuda; su guía la vuelve operativa promediando las variables a lo largo de la trayectoria, sin variación del tipo de cambio real ni ajuste *stock*-flujo (FMI, 2022, recuadro 3).

## 2.2. Antecedentes metodológicos

**Metodologías que no alcanzan.** Los enfoques contables proyectan una sola trayectoria de la deuda. Rodríguez (2023) muestra que el cociente deuda/PIB, tomado de forma aislada, no alcanza para evaluar la solvencia si no se consideran las tasas de interés y el ciclo, y Sanches (2019) descompone su dinámica en componentes. Ninguno de los dos estima cómo se transmiten los *shocks* entre el resultado fiscal, el riesgo país, el tipo de cambio y la actividad, ni asigna una probabilidad a la trayectoria.

**Simulación estocástica con vectores autorregresivos.** Celasun et al. (2006) proponen en el FMI combinar un modelo de vectores autorregresivos (VAR) sobre los determinantes de la deuda con una función de reacción fiscal y la identidad de acumulación, para obtener una distribución de trayectorias en lugar de un único escenario. Medeiros (2012) aplica la misma arquitectura en la Comisión Europea, y el FMI la incorporó a su Marco de Riesgo Soberano y Sostenibilidad de la Deuda (FMI, 2021, 2022), con el que evalúa a la Argentina (FMI, 2025, 2026). La limitación de ese marco es que genera los *shocks* a partir de la historia de los determinantes en forma reducida, sin identificar su origen, de modo que no permite atribuir el riesgo a una perturbación concreta.

**VAR estructural.** Un VAR estructural (SVAR) separa los residuos en *shocks* con interpretación económica imponiendo restricciones. Blanchard y Perotti (2002) identifican el *shock* fiscal con restricciones de impacto: los rezagos de decisión hacen que la política fiscal discrecional no responda a la actividad dentro del trimestre, y la respuesta automática del resultado primario al ciclo se fija con una elasticidad externa. La descomposición de Cholesky es el caso particular en que las variables se ordenan de manera recursiva, y su resultado depende del orden elegido; en este proyecto se usará como robustez. Favero y Giavazzi (2007) muestran que un VAR fiscal que omite la retroalimentación de la deuda está mal especificado, porque el nivel de deuda condiciona la política fiscal y las tasas. Para el caso argentino, el SVAR sirve porque permite separar el *shock* fiscal de los cambiarios, de riesgo y externos, que es exactamente lo que la pregunta de investigación necesita medir.

**Restricciones de signo.** Uhlig (2005) propone identificar los *shocks* exigiendo solo el signo de algunas respuestas, sin restricciones de cero. Tiene la ventaja de imponer supuestos más débiles, pero identifica un conjunto de modelos y no uno solo (Fry y Pagan, 2011), de modo que la descomposición de la varianza queda indeterminada, y exige fijar de antemano el signo de respuestas que el proyecto busca medir, como la del riesgo país ante el *shock* fiscal. Por esas dos razones no se usarán. Las restricciones de largo plazo de Blanchard y Quah (1989) tampoco: exigen suponer que el tipo de cambio real es neutral en el largo plazo, un supuesto difícil de sostener para la Argentina.

## 2.3. Resultados ya conocidos

- **El superávit tiene un efecto limitado.** Los ajustes fiscales discrecionales reducen poco el cociente de deuda y solo lo hacen de forma duradera en fases de expansión (Ando et al., 2025). La respuesta del superávit a la deuda se debilita cuando la deuda es alta (Ghosh et al., 2013).
- **La depreciación real domina en las economías dolarizadas.** Una interrupción repentina de capitales encarece la deuda en dólares a través de la depreciación real, y Argentina estaba en el peor extremo de los casos comparados en apertura y descalce de monedas (Calvo et al., 2003). Levy Yeyati y Sturzenegger (2023) muestran que el patrimonio neto del sector público argentino es menos sensible a la devaluación que el cociente de deuda.
- **Las condiciones externas pesan.** En América Latina, el índice de volatilidad VIX es la variable global con efectos más robustos sobre la sostenibilidad de la deuda (Adler y Sosa, 2013), y los *shocks* de la tasa de Estados Unidos operan sobre todo a través del riesgo soberano (Uribe y Yue, 2006; Neumeyer y Perri, 2005).
- **La evaluación vigente del FMI.** Para la deuda federal bruta argentina, el FMI estima una probabilidad de no estabilización de alrededor de 1% a mediano plazo y menos de 3% a diez años, y califica la deuda como sostenible pero no con alta probabilidad (FMI, 2026).

## 2.4. Variables a incluir

Los antecedentes indican cuatro determinantes de la deuda, que son los impulsores de la identidad del FMI: el crecimiento real, el resultado primario, el costo del financiamiento, medido por el riesgo país, y el tipo de cambio real. A ellos se suman dos variables externas: la tasa de la FED, por los canales de Uribe y Yue (2006) y Neumeyer y Perri (2005), y el VIX, por los resultados de Adler y Sosa (2013). La deuda entra rezagada en el sistema, por el argumento de Favero y Giavazzi (2007).

## 2.5. Ideas nuevas: área de vacancia

En la literatura revisada no se encontró un trabajo que cubra de manera conjunta tres aspectos para el caso argentino:

1. Una probabilidad de no estabilización calculada con *shocks* identificados sobre el mismo perímetro, el mismo escenario y la misma definición operativa que usa el FMI. Los trabajos que identifican *shocks* lo hacen sobre paneles de países, y los que estudian la deuda argentina no los identifican.
2. La traducción del efecto de la política monetaria de Estados Unidos en un cambio de esa probabilidad.
3. La dinámica de la deuda consolidada con el BCRA: aunque el FMI (2021) admite incluir los pasivos del banco central en la deuda pública, en su análisis de la Argentina la consolidada aparece solo como un cuadro de *stocks* (FMI, 2026, anexo II).

Se agrega una medida complementaria a la del FMI, una métrica anual de no estabilización que conserva la valuación de la deuda en moneda extranjera de cada año, que la definición del organismo excluye por construcción.

# 3. Metodología

## 3.1. Datos

**Tipo de estudio, unidad de análisis y muestra.** El estudio es cuantitativo, explicativo y longitudinal, retrospectivo en la estimación (1996-2025) y prospectivo en la simulación (2026-2035). La unidad de análisis es la economía argentina, observada como serie temporal trimestral. La ventana 1996T1-2025T4 incluye regímenes cambiarios y fiscales distintos: convertibilidad, *default*, desendeudamiento, reendeudamiento y programa con el FMI. Las ecuaciones se estimarán con 1998T2-2025T4 (111 trimestres), porque los primeros trimestres de la ventana son condiciones iniciales de los rezagos.

**Tabla 1. Variables, indicadores y fuentes**

| Variable | Indicador | Fuente | Rol |
|---|---|---|---|
| Deuda federal bruta | Deuda bruta de la Administración Central, % del PIB | Ministerio de Economía (MECON); *stock* inicial del FMI (2026) | Entra rezagada y se acumula con la identidad (especificación principal) |
| Deuda consolidada con el BCRA | Deuda del Tesoro y del BCRA neta de tenencias cruzadas, % del PIB | MECON y BCRA; *stock* inicial del FMI (2026) | Ídem (extensión, estimada desde 2002) |
| Resultado primario | Resultado del Sector Público Nacional sin rentas de la propiedad, % del PIB | MECON | Endógena |
| Crecimiento | Variación trimestral del PIB real | Instituto Nacional de Estadística y Censos (INDEC) | Endógena |
| Riesgo país | Diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), en puntos básicos | J.P. Morgan, serie diaria publicada por Ámbito Financiero; empalme para 1996T1-1998T3 | Endógena |
| Tipo de cambio real | Tipo de cambio real multilateral (TCRM) | BCRA; empalme para 1996 con el Banco de Pagos Internacionales (BIS) | Endógena |
| Política monetaria de Estados Unidos | Tasa de fondos federales; tasa sombra en el límite cero (Wu y Xia, 2016) | Reserva Federal | Exógena |
| Condiciones financieras globales | VIX | Bolsa de Opciones de Chicago (CBOE) | Exógena |
| Orientación de la política económica | Una variable binaria por mandato presidencial | Elaboración propia | Exógena (control) |
| Escenario base | Crecimiento, deflactor, tasa efectiva, resultado primario, ajuste *stock*-flujo e inflación relativa, 2026-2035 | FMI (2026), cuadro 6 | Supuesto de la simulación |

Fuente: elaboración propia.

**Construcción y evaluación de las series.** Todos los datos son secundarios. Cada serie se evaluará por la institución que la produce, su definición y cobertura, sus cambios metodológicos (el cambio de base del PIB en 2004 y los tramos del resultado primario de 2007 y 2015) y su coherencia con otra fuente. La deuda federal bruta se contrastará con la del FMI, y la simulación partirá del *stock* del organismo a fines de 2025 (80,3% del PIB). La deuda consolidada sumará a la deuda bruta los pasivos remunerados del BCRA y restará la deuda del Tesoro en poder del BCRA y los depósitos del Tesoro en el banco central; se estimará desde 2002, porque antes el BCRA operaba con la autonomía de la Carta Orgánica de 1992 y bajo la convertibilidad, y la consolidación no tiene fundamento en el criterio del FMI. El resultado primario se tomará sin rentas de la propiedad, porque el FMI excluye las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4) y la fuente pública no las separa del resto de esas rentas.

**Empalmes.** La serie diaria del EMBI empieza en diciembre de 1998; para 1996T1-1998T3 se usará el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA y la tasa de fondos federales, con la relación estimada en la superposición 1998T4-2001T3 y validada con el R², una validación cruzada y un pronóstico fuera de muestra. El TCRM del BCRA empieza en enero de 1997; para 1996 se encadenará con las variaciones del tipo de cambio real efectivo del BIS. En la tasa de la FED, las cuatro transiciones entre la tasa sombra y la efectiva (2009T1, 2016T1, 2020T2 y 2022T1) se tratarán para que el cambio de serie no se confunda con un cambio de política. Para comprobar que los resultados no dependen de los empalmes, todo se repetirá con datos desde 1999.

## 3.2. Cómo se analizarán

1. **Propiedades de las series.** Pruebas de raíz unitaria de Dickey y Fuller aumentada (ADF) y de Kwiatkowski, Phillips, Schmidt y Shin (KPSS); prueba de Zivot y Andrews, que admite un quiebre; quiebres múltiples de Bai y Perron (2003), que entrarán como variables binarias, y prueba de cointegración de Johansen.
2. **Especificación.** SVARX con cuatro variables endógenas (resultado primario, crecimiento, EMBI y TCRM) y, como exógenas, la variación de la tasa de la FED con dos rezagos, el VIX y variables binarias estacionales, de quiebre y por mandato presidencial, cuya significancia conjunta se contrastará con pruebas de Wald y de razón de verosimilitud. La deuda entrará rezagada en las cuatro ecuaciones y se acumulará con la identidad contable.
3. **Rezagos.** El criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si los residuos rechazan la ausencia de autocorrelación (Portmanteau con 12 rezagos, al 5%), el menor orden mayor que no la rechace (Lütkepohl, 2005), y si ninguno la pasa, el de mayor p-valor.
4. **Identificación.** Restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto. Como robustez, dos ordenamientos de Cholesky (resultado primario primero y último) y elasticidades cíclicas de 0 y 0,5.
5. **Inferencia.** Intervalos de 90% por *bootstrap*[^en-bootstrap] de bloques móviles de cuatro trimestres, de diseño recursivo (Brüggemann et al., 2016), con 1.000 réplicas y percentiles de Hall (1992); las participaciones y varianzas, que están acotadas, usarán percentiles simples.
6. **Simulación.** Monte Carlo de 2026 a 2035 sobre el escenario base del FMI (2026), desde su *stock* inicial, con los *shocks* estructurales remuestreados en bloques de ocho trimestres, como los bloques de dos años del FMI (FMI, 2021, anexo VI). El VIX y la tasa de la FED seguirán procesos autorregresivos de primer orden. La no estabilización se medirá con la definición operativa del FMI (FMI, 2022, recuadro 3) y, como complemento, con la métrica anual.
7. **Contraste de hipótesis.**
    - H1a se respalda si se cumplen dos condiciones: (i) la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del fiscal, con un intervalo de 90% de la diferencia que excluye el cero, y (ii) con el resultado primario de todos los años desplazado en la misma magnitud hasta que el de 2031 alcanza su máximo de 1996-2025, la probabilidad de no estabilización en 2031, con la definición del FMI, sigue por encima del 1%.
    - H1b se respalda si el límite inferior del intervalo de 90% supera la cifra del FMI en 2031 (1%) y en 2035 (3%), con la definición operativa del FMI; se informará también la corrección de Bonferroni.
    - H2 se respalda si el intervalo de 90% de la diferencia entre cada escenario de la FED y el base excluye el cero en 2035, en la probabilidad y en la deuda esperada; si se cumple en una medida o un escenario y no en los otros, se declara parcialmente respaldada. Los escenarios son un nivel de la tasa un desvío estándar más alto y la repetición de la senda de 2022-2025.
8. **Robustez.** Deuda consolidada; sin binarias presidenciales; resultado primario con rentas; canal de tasas en pesos; sin retroalimentación; uno y tres rezagos; identificaciones alternativas; sin los *shocks* de la cesación de pagos; datos desde 1999 y desde 2004; sin quiebres; ajuste *stock*-flujo en cero; dos velocidades de refinanciación; escenario del FMI de 2025; corrección de sesgo de Kilian (1998), y el procedimiento de *shocks* del propio FMI aplicado a la historia argentina.

## 3.3. Por qué la metodología sirve en este caso

- **Identifica el origen del riesgo.** La pregunta es si el superávit alcanza o si otros determinantes pesan más. Para responderla hay que separar el *shock* fiscal de los cambiarios, de riesgo y externos, y eso es lo que hace un SVAR. El marco del FMI no lo permite, porque genera los *shocks* en forma reducida.
- **Respeta la contabilidad de la deuda.** Al acumular la deuda con la identidad, y no con una ecuación estimada, la simulación separa el tramo en pesos del tramo en moneda extranjera y capta el efecto de valuación de la depreciación real, central en una economía con más de la mitad de la deuda en dólares.
- **Es comparable con la evaluación oficial.** Usa el perímetro, el punto de partida, el escenario y la definición operativa del FMI, de modo que la diferencia con su cifra solo puede provenir de la forma de generar los *shocks*.
- **Incorpora el *shock* externo con nombre propio.** La tasa de la FED entra como variable exógena, lo que permite medir su efecto como un multiplicador dinámico, sin depender de cómo se identifiquen los *shocks* argentinos (Canova, 2005).
- **Es factible con los datos disponibles.** Con 111 trimestres, un sistema de cuatro variables con dos rezagos es estimable, y el *bootstrap* por bloques evita suponer normalidad en una serie con crisis y cambios de régimen.
- **Es replicable.** Los datos son públicos y la estimación se programa en Python con bibliotecas de uso libre, de modo que el ejercicio puede actualizarse con cada nuevo informe del FMI.

# Referencias bibliográficas

Adler, G., y Sosa, S. (2013). *External conditions and debt sustainability in Latin America* (IMF Working Paper No. 13/27). Fondo Monetario Internacional.

Ando, S., Mishra, P., Patel, N., Peralta-Alva, A., y Presbitero, A. F. (2025). Fiscal consolidation and public debt. *Journal of Economic Dynamics and Control*, *170*, artículo 104998. https://doi.org/10.1016/j.jedc.2024.104998

Bai, J., y Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics*, *18*(1), 1-22. https://doi.org/10.1002/jae.659

Blanchard, O. J., y Quah, D. (1989). The dynamic effects of aggregate demand and supply disturbances. *American Economic Review*, *79*(4), 655-673.

Blanchard, O., y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. *Quarterly Journal of Economics*, *117*(4), 1329-1368. https://doi.org/10.1162/003355302320935043

Bohn, H. (1998). The behavior of U.S. public debt and deficits. *Quarterly Journal of Economics*, *113*(3), 949-963. https://doi.org/10.1162/003355398555793

Brüggemann, R., Jentsch, C., y Trenkler, C. (2016). Inference in VARs with conditional heteroskedasticity of unknown form. *Journal of Econometrics*, *191*(1), 69-85. https://doi.org/10.1016/j.jeconom.2015.10.004

Calvo, G. A., Izquierdo, A., y Talvi, E. (2003). *Sudden stops, the real exchange rate, and fiscal sustainability: Argentina's lessons* (NBER Working Paper No. 9828). National Bureau of Economic Research. https://doi.org/10.3386/w9828

Canova, F. (2005). The transmission of US shocks to Latin America. *Journal of Applied Econometrics*, *20*(2), 229-251. https://doi.org/10.1002/jae.837

Celasun, O., Debrun, X., y Ostry, J. D. (2006). *Primary surplus behavior and risks to fiscal sustainability in emerging market countries: A "fan-chart" approach* (IMF Working Paper No. 06/67). Fondo Monetario Internacional. https://doi.org/10.5089/9781451863277.001

Díaz Alejandro, C. F. (1970). *Essays on the economic history of the Argentine Republic*. Yale University Press.

Favero, C., y Giavazzi, F. (2007). *Debt and the effects of fiscal policy* (NBER Working Paper No. 12822). National Bureau of Economic Research. https://doi.org/10.3386/w12822

Fondo Monetario Internacional [FMI]. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper).

Fondo Monetario Internacional [FMI]. (2022). *Staff guidance note on the Sovereign Risk and Debt Sustainability Framework for market access countries* (IMF Policy Paper No. 2022/039). https://www.imf.org/en/Publications/Policy-Papers/Issues/2022/08/08/Staff-Guidance-Note-on-the-Sovereign-Risk-and-Debt-Sustainability-Framework-for-Market-521884

Fondo Monetario Internacional [FMI]. (2025). *Argentina: Request for an extended arrangement under the Extended Fund Facility* (IMF Country Report No. 25/95).

Fondo Monetario Internacional [FMI]. (2026). *Argentina: 2026 Article IV consultation, second review under the extended arrangement under the Extended Fund Facility* (IMF Country Report No. 26/105).

Fry, R., y Pagan, A. (2011). Sign restrictions in structural vector autoregressions: A critical review. *Journal of Economic Literature*, *49*(4), 938-960. https://doi.org/10.1257/jel.49.4.938

Ghosh, A. R., Kim, J. I., Mendoza, E. G., Ostry, J. D., y Qureshi, M. S. (2013). Fiscal fatigue, fiscal space and debt sustainability in advanced economies. *The Economic Journal*, *123*(566), F4-F30. https://doi.org/10.1111/ecoj.12010

Hall, P. (1992). *The bootstrap and Edgeworth expansion*. Springer. https://doi.org/10.1007/978-1-4612-4384-7

Ivanov, V., y Kilian, L. (2005). A practitioner's guide to lag order selection for VAR impulse response analysis. *Studies in Nonlinear Dynamics and Econometrics*, *9*(1), artículo 2. https://doi.org/10.2202/1558-3708.1219

Kilian, L. (1998). Small-sample confidence intervals for impulse response functions. *Review of Economics and Statistics*, *80*(2), 218-230. https://doi.org/10.1162/003465398557465

Levy Yeyati, E., y Sturzenegger, F. (2023). A balance-sheet approach to fiscal sustainability. *Fiscal Studies*, *44*(1), 61-84. https://doi.org/10.1111/1475-5890.12319

Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública. (2021, 3 de marzo). Boletín Oficial de la República Argentina. https://www.argentina.gob.ar/normativa/nacional/norma-347532/texto

Lütkepohl, H. (2005). *New introduction to multiple time series analysis*. Springer.

Medeiros, J. (2012). *Stochastic debt simulation using VAR models and a panel fiscal reaction function: Results for a selected number of countries* (European Economy Economic Papers No. 459). Comisión Europea. https://doi.org/10.2765/26084

Neumeyer, P. A., y Perri, F. (2005). Business cycles in emerging economies: The role of interest rates. *Journal of Monetary Economics*, *52*(2), 345-380. https://doi.org/10.1016/j.jmoneco.2004.04.011

Oficina de Presupuesto del Congreso [OPC]. (2026). *Operaciones de deuda pública, julio 2026*.

Rapoport, M. (2020). *Historia económica, política y social de la Argentina (1880-2003)*. Crítica.

Reinhart, C. M., y Rogoff, K. S. (2009). *This time is different: Eight centuries of financial folly*. Princeton University Press.

Rodríguez, A. (2023). Financiamiento y sostenibilidad de la deuda pública: El caso de la economía argentina (2001-2022). *Ciencias Económicas*, *2*(20), e0032. https://doi.org/10.14409/rce.2023.20.e0032

Sanches, P. (2019). *Análisis de la sostenibilidad de la deuda soberana argentina. 2019-2023* [Tesis de maestría]. Universidad Torcuato Di Tella.

Secretaría de Finanzas, Ministerio de Economía. (2025, 10 de diciembre). *Resultado de licitación del Bono del Tesoro Nacional en dólares estadounidenses 6,50% con vencimiento 30 de noviembre de 2029* [Comunicado]. https://www.argentina.gob.ar/noticias/resultado-de-licitacion-del-bono-del-tesoro-nacional-en-dolares-estadounidenses-650-con

Uhlig, H. (2005). What are the effects of monetary policy on output? Results from an agnostic identification procedure. *Journal of Monetary Economics*, *52*(2), 381-419. https://doi.org/10.1016/j.jmoneco.2004.05.007

Uribe, M., y Yue, V. Z. (2006). Country spreads and emerging countries: Who drives whom? *Journal of International Economics*, *69*(1), 6-36. https://doi.org/10.1016/j.jinteco.2005.04.003

Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking*, *48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300

[^en-default]: *Default*: cesación de pagos de la deuda.
[^en-shock]: *Shock*: perturbación inesperada que afecta a una variable y se transmite a las demás.
[^en-stock]: *Stock*: saldo de una variable en un momento dado, por oposición a un flujo.
[^en-bootstrap]: *Bootstrap*: método de remuestreo que aproxima la distribución de un estimador repitiendo la estimación sobre muestras generadas a partir de los propios datos.
