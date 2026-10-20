---
title: "Plan de labor"
subtitle: "Tesis final de grado. Facultad de Ciencias Económicas, Universidad Nacional de Cuyo"
---

Páez, Santiago. Legajo 34110

Chillón, Federico. Legajo 34394

Carricondo, Emiliano. Legajo 33396

Octubre de 2026

# 1. Identificación del proyecto

**1.1. Director:** Pablo Mahnic.

**1.2. Codirector:** no tiene.

**1.3. Ubicación académica:** Facultad de Ciencias Económicas, Universidad Nacional de Cuyo.

**1.4. Denominación del proyecto:** Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos.

**1.5. Palabras clave:** deuda pública; sostenibilidad de la deuda; vectores autorregresivos estructurales; simulación de Monte Carlo; política monetaria de Estados Unidos.

**1.6. Resumen técnico.** Argentina registró superávit primario en 2024 y 2025 y volvió a colocar deuda en dólares en diciembre de 2025, después de dos décadas marcadas por el *default*[^en-default] de 2001 y la reestructuración de 2020. El proyecto se pregunta si ese superávit alcanza para estabilizar la deuda pública o si el crecimiento, el tipo de cambio real y el riesgo país la condicionan más que el esfuerzo fiscal. La deuda principal será la deuda federal bruta, perímetro del análisis de sostenibilidad del Fondo Monetario Internacional (FMI); como extensión, la deuda consolidada con el Banco Central de la República Argentina (BCRA). Se estimará un modelo de vectores autorregresivos estructural con variables exógenas (SVARX) con datos trimestrales de 1996 a 2025. El resultado primario, el crecimiento, el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), y el tipo de cambio real multilateral (TCRM) serán las variables endógenas, y la deuda rezagada entrará en todas las ecuaciones. La tasa de política monetaria de la Reserva Federal (FED) de los Estados Unidos y la volatilidad financiera global serán exógenas. Los *shocks*[^en-shock] del modelo alimentarán una simulación de Monte Carlo de la deuda entre 2026 y 2035 sobre el escenario base del FMI, con su punto de partida y su métrica. Se obtendrá la probabilidad de que la deuda no se estabilice, comparable con la del FMI, la contribución de cada grupo de *shocks* a su varianza y el efecto de un endurecimiento de la política monetaria de la FED. El estudio es cuantitativo, explicativo y longitudinal, y trabaja con datos secundarios.

# 2. Descripción del proyecto

## 2.1. Tema

La sostenibilidad de la deuda pública argentina y sus determinantes macroeconómicos: estimación con datos de 1996-2025 y proyección para 2026-2035.

## 2.2. Estado actual del conocimiento

La tesis organiza la literatura sobre la deuda argentina en ocho ejes, que desarrolla el capítulo de Antecedentes. Este plan resume los cuatro que delimitan el problema.

El primero trata las limitaciones de los enfoques contables. Rodríguez (2023) muestra que la ratio entre la deuda y el producto interno bruto (deuda/PIB) no alcanza para evaluar la solvencia si no se consideran las tasas de interés y el ciclo económico. Sanches (2019) descompone la dinámica de la ratio en sus componentes. Ninguno de estos trabajos estima cómo se transmiten los *shocks* entre el resultado fiscal, el riesgo país, el tipo de cambio y la actividad.

El segundo eje es la discusión sobre la fatiga fiscal. Ghosh et al. (2013) encuentran que el superávit primario responde cada vez menos a la deuda cuando esta es alta, lo que llaman fatiga fiscal. Ando et al. (2025) muestran que los ajustes fiscales discrecionales reducen poco la ratio de deuda y solo lo hacen de forma duradera en fases de expansión.

El tercer eje es la simulación estocástica de deuda y los marcos de riesgo soberano. Celasun et al. (2006) proponen en el FMI combinar un VAR sobre los determinantes de la deuda con una función de reacción fiscal y la identidad de acumulación, para obtener distribuciones de trayectorias en lugar de un único escenario. Medeiros (2012) aplica la misma arquitectura en la Comisión Europea, y el FMI la incorporó a su Marco de Riesgo Soberano y Sostenibilidad de la Deuda (FMI, 2021), con el que evalúa a la Argentina en las revisiones del programa (FMI, 2025, 2026). Ese marco genera los *shocks* a partir de la historia de los determinantes, sin identificar su origen.

El cuarto eje contrapone el balance patrimonial y la ratio deuda/PIB. Calvo et al. (2003) explican cómo una interrupción repentina de capitales encarece la deuda en dólares a través de la depreciación real, y Levy Yeyati y Sturzenegger (2023) estudian el efecto de valuación del tipo de cambio sobre el patrimonio neto del sector público argentino.

**Área de vacancia.** En la literatura revisada no se encontró un trabajo que cubra de manera conjunta tres aspectos para el caso argentino. El primero es una probabilidad de no estabilización calculada con *shocks* identificados sobre el mismo perímetro y el mismo escenario que usa el FMI, y con su definición operativa de la métrica: los trabajos revisados que identifican *shocks* lo hacen sobre paneles de países, y los que estudian la deuda argentina no los identifican. El segundo es la traducción del efecto de la política monetaria de Estados Unidos en un cambio de esa probabilidad. El tercero es la dinámica de la deuda consolidada con el BCRA: aunque el FMI (2021) admite incluir los pasivos del banco central en la deuda pública, en su análisis de la Argentina usa la deuda bruta del gobierno federal, y la consolidada aparece solo como un cuadro de *stocks*[^en-stock] (FMI, 2025, anexo II). No se encontró un trabajo que estime cómo evolucionó esa deuda junto con sus determinantes.

## 2.3. Planteamiento del problema

**Contextualización.** La historia argentina muestra un ciclo repetido de endeudamiento externo, interrupción de los flujos de capital y cesación de pagos (Reinhart y Rogoff, 2009; Rapoport, 2020). La administración que asumió en diciembre de 2023 recibió un *stock* elevado de pasivos y un acceso muy limitado al crédito voluntario. El Tesoro volvió a colocar un bono en dólares en diciembre de 2025, bajo ley local y a una tasa de 9,26% anual (Secretaría de Finanzas, 2025). A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones (Oficina de Presupuesto del Congreso [OPC], 2026). Durante buena parte del período, el BCRA absorbió liquidez con pasivos remunerados que llegaron a 18,4% del PIB en 2023 (FMI, 2025, anexo II), de modo que una parte del endeudamiento público no aparecía en la deuda del Tesoro.

**Problema.** El problema es determinar si el superávit primario alcanza para estabilizar la deuda en el mediano plazo o si los determinantes estructurales de la economía argentina la condicionan más que el resultado fiscal.

**Preguntas de investigación.**

- Pregunta general: ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario de Argentina condicionan la sostenibilidad de la deuda pública en 2026-2035, y cuál es la probabilidad de que la deuda no se estabilice bajo el escenario base del FMI?
- Pregunta específica: ¿cómo y en qué magnitud impactaría un endurecimiento de la política monetaria de la FED sobre la dinámica de la deuda y sobre su probabilidad de no estabilizarse en 2026-2035?

**Objetivo general.** Evaluar la dinámica de la deuda pública argentina a partir de sus determinantes macroeconómicos históricos (1996-2025), para proyectar su sostenibilidad en 2026-2035 y estimar la probabilidad de que no se estabilice.

**Objetivos específicos.**

1. Construir series trimestrales de la deuda bruta del gobierno federal y de la deuda consolidada con el BCRA entre 1996 y 2025, y contrastarlas con los *stocks* que publica el FMI.
2. Establecer las propiedades estadísticas de las series: raíz unitaria, quiebres estructurales y cointegración.
3. Estimar un SVARX en el que el crecimiento, el resultado primario, el EMBI y el TCRM interactúan con la deuda rezagada, con la tasa de la FED y la volatilidad global como variables exógenas.
4. Medir la reacción del resultado primario ante el nivel de deuda y la contribución de los *shocks* fiscal, de actividad, cambiario y de riesgo y externo a la varianza de la deuda.
5. Simular la distribución de trayectorias de la deuda federal bruta en 2026-2035 bajo el escenario base del FMI, calcular la probabilidad de que no se estabilice y compararla con la del FMI; repetir el ejercicio con la deuda consolidada.
6. Estimar el efecto de un endurecimiento de la política monetaria de la FED sobre esa distribución.

**Justificación.** La Ley 27.612 (2021) exige una ley especial para emitir deuda en moneda extranjera bajo legislación extranjera por encima del máximo del presupuesto y una ley que apruebe cada programa con el FMI. Esas decisiones requieren evaluaciones de sostenibilidad, y la evaluación probabilística de referencia es la del FMI. El proyecto aporta una segunda medida con *shocks* identificados que usa el perímetro, el punto de partida, el escenario y la métrica del FMI, de modo que la diferencia entre ambas pueda atribuirse a la forma de generar los *shocks*. La extensión a la deuda consolidada con el BCRA mide la dinámica de un perímetro que el FMI informa solo como *stock*. En lo metodológico, deja un procedimiento replicable que puede actualizarse con cada nuevo informe del FMI.

**Viabilidad.** El proyecto no requiere trabajo de campo ni financiamiento. La mayoría de los datos son de acceso público: Ministerio de Economía (MECON), BCRA, Instituto Nacional de Estadística y Censos (INDEC), FMI, Reserva Federal y la Bolsa de Opciones de Chicago (CBOE), que publica el índice de volatilidad implícita VIX. La excepción es el EMBI, que elabora J.P. Morgan y no se publica en forma libre: se tomará de la serie diaria que publica Ámbito Financiero, disponible desde diciembre de 1998. Los trimestres anteriores de la ventana se completarán con un empalme construido con series oficiales del BCRA y de la Reserva Federal, y el TCRM de 1996 con el índice del Banco de Pagos Internacionales (BIS), como se explica en la estrategia metodológica. La estimación y la simulación se programarán en Python con bibliotecas de uso libre. El dato de acceso más incierto son las tenencias de títulos públicos del Fondo de Garantía de Sustentabilidad (FGS) de la Administración Nacional de la Seguridad Social (ANSES). Si no se consiguen completas, la serie histórica de deuda consolidada no las descontará y se declarará como limitación; la simulación de esa extensión partirá del *stock* consolidado del FMI, que ya las descuenta.

## 2.4. Marco teórico

El marco va de la teoría general a la teoría sustantiva en cuatro niveles.

**Nivel 1. Restricción externa.** El punto de partida es el enfoque de la restricción externa: en una economía que necesita divisas para crecer y para pagar su deuda, el endeudamiento en moneda extranjera la expone a la disponibilidad de dólares (Díaz Alejandro, 1970; Calvo et al., 2003). Ese enfoque explica por qué en Argentina el tipo de cambio real y el riesgo país pesan sobre la deuda tanto como el resultado fiscal.

**Nivel 2. Solvencia y sostenibilidad.** El gobierno es solvente si el valor presente de sus superávits primarios futuros cubre la deuda actual. Bohn (1998) muestra que una condición suficiente es que el superávit primario responda positivamente al nivel de deuda. Esa respuesta no garantiza que la deuda se estabilice en un nivel determinado: si la diferencia entre la tasa de interés y el crecimiento es alta, el superávit necesario puede superar lo que la economía genera. La fatiga fiscal (Ghosh et al., 2013) fija un límite a cuánto superávit puede exigirse de manera realista. El FMI (2021) define la deuda como sostenible cuando el gobierno puede cumplir sus obligaciones sin un ajuste poco realista.

**Nivel 3. Identidad de la deuda y perímetro.** La ratio deuda/PIB cambia por el diferencial entre la tasa de interés y el crecimiento, por el resultado primario, por el ajuste entre *stocks* y flujos y, cuando parte de la deuda está en moneda extranjera, por la depreciación real. Esta identidad conecta las variables del modelo con la deuda y separa el efecto del esfuerzo fiscal del efecto de valuación. El FMI (2021) la usa para definir la estabilización: la deuda no se estabiliza en un año si el resultado primario es menor que el que la mantendría constante. El perímetro define qué deuda y qué resultado primario entran en la identidad. Cuando el banco central financia al Tesoro o absorbe liquidez con pasivos remunerados, la restricción relevante es la del sector público consolidado, y el FMI (2021) incluye esos pasivos en la deuda pública cuando pueden financiar al gobierno o representan un riesgo fiscal material.

**Nivel 4. Transmisión externa y sostenibilidad probabilística.** Una suba de la tasa de la FED eleva la prima de riesgo de los emergentes (Uribe y Yue, 2006), deprecia su tipo de cambio real y reduce su crecimiento (Neumeyer y Perri, 2005). Cada canal entra en la identidad de la deuda por un término distinto. Como los determinantes son inciertos, la sostenibilidad se expresa como la probabilidad de que la deuda no se estabilice, construida con simulaciones (Celasun et al., 2006; FMI, 2021).

## 2.5. Hipótesis

**H1a.** El crecimiento, el tipo de cambio real, el riesgo país y el resultado primario condicionan la sostenibilidad de la deuda, de modo que el superávit primario, por sí solo, no basta para estabilizarla en 2026-2035.

- Unidad de análisis: la economía argentina, observada como serie temporal trimestral.
- Variables: contribución de los *shocks* fiscal, de actividad, cambiario y de riesgo y externo a la varianza de la deuda federal bruta en 2035.
- Relación esperada: la contribución conjunta de los *shocks* no fiscales es mayor que la del *shock* fiscal.
- Criterio de contraste: la hipótesis se respalda si la diferencia entre la contribución de los *shocks* no fiscales y la del *shock* fiscal es positiva y su intervalo de 90% excluye el cero. Como complemento descriptivo, sin criterio de contraste, se calculará la probabilidad de no estabilización con el resultado primario en su máximo anual de 1996-2025 y el aumento del resultado primario que la llevaría a la estimación del FMI.

**H1b.** La probabilidad de que la deuda federal bruta no se estabilice es mayor que la que informa el FMI para esa misma deuda: alrededor de 1% a mediano plazo (2031) y menos de 3% a diez años (2035) (FMI, 2026).

- Unidad de análisis: la economía argentina, observada como serie temporal trimestral.
- Variables: probabilidad de no estabilización de la deuda federal bruta en 2031 y 2035, calculada con el punto de partida y el escenario base del FMI, con una métrica anual y con la definición operativa del FMI, y la probabilidad que informa el FMI para cada horizonte.
- Relación esperada: la primera es mayor que la segunda en los dos horizontes.
- Criterio de contraste: el límite inferior del intervalo de 90% supera la cifra del FMI en cada horizonte (1% y 3%); se informará también el límite con la corrección de Bonferroni por los dos horizontes (95%).

**H2.** Un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda y su probabilidad de no estabilizarse. La hipótesis se refiere al efecto total; los canales por los que opera (riesgo país, tipo de cambio real, crecimiento y costo directo de la deuda en dólares) se examinarán por separado.

- Unidad de análisis: la economía argentina, observada como serie temporal trimestral.
- Variables: tasa de la FED; deuda esperada y probabilidad de no estabilización en 2035; EMBI, TCRM y crecimiento como canales.
- Relación esperada: positiva entre la tasa de la FED y la deuda esperada y entre la tasa de la FED y la probabilidad de no estabilización.
- Criterio de contraste: el intervalo de 90% de la diferencia entre cada escenario de la FED y el base excluye el cero en 2035, para la probabilidad y para la deuda esperada. Se mide al final del horizonte porque el efecto de una tasa más alta se acumula; 2031 se informará. Se informarán también la corrección de Bonferroni y la respuesta de cada canal.

## 2.6. Estrategia metodológica

**Tipo de estudio.** Cuantitativo, explicativo y longitudinal. Es explicativo porque busca medir cómo los determinantes macroeconómicos afectan la deuda. Es retrospectivo en la estimación (1996-2025) y prospectivo en la simulación (2026-2035).

**Unidad de análisis, población y muestra.** La unidad de análisis es la economía argentina, observada como serie temporal trimestral. La población son todos los trimestres con datos de deuda pública. La muestra es no probabilística e intencional: 1996T1-2025T4, porque la ventana incluye regímenes cambiarios y fiscales distintos (convertibilidad, *default*, desendeudamiento, reendeudamiento y programa con el FMI). Las ecuaciones se estimarán con los trimestres 1998T2-2025T4 (111 trimestres): los primeros trimestres de la ventana se usarán como condiciones iniciales de los rezagos, porque la variación de la tasa de la FED entra con dos rezagos y todos los órdenes de rezago considerados, hasta seis, se compararán sobre la misma muestra (Lütkepohl, 2005, sec. 4.3). Esto no cambia la ventana del estudio.

**Técnicas de obtención y evaluación de datos secundarios.** Todos los datos son secundarios. La evaluación de cada serie revisará cuatro aspectos: la institución que la produce, la definición y cobertura, los cambios metodológicos (el cambio de base del PIB en 2004 y los tramos metodológicos del resultado primario de 2007 y 2015) y la coherencia con otra fuente. La deuda federal bruta se tomará de los informes de deuda del MECON y se contrastará con la del FMI; la simulación partirá del *stock* del FMI a fines de 2025 (80,3% del PIB), que incluye conceptos que el MECON no informa, como los intereses capitalizados. La deuda consolidada se construirá sumando la deuda bruta de la Administración Central y los pasivos remunerados del BCRA, y restando la deuda del Tesoro en poder del BCRA y los depósitos del Tesoro en el banco central. Se contrastará con el cuadro de deuda consolidada del FMI (2025, anexo II; 2026) en los años en que ambos se superponen. El resultado primario tendrá una sola definición para todo el estudio: el del Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4), y la fuente pública del MECON no las separa del resto de las rentas de la propiedad, de modo que la serie sin rentas es la que las deja afuera. En el perímetro consolidado esas utilidades también son un flujo interno. La serie con rentas de la propiedad se informará como robustez. En la tasa de la FED, el cambio de la tasa sombra a la tasa efectiva en 2022T1 se tratará de modo que no se confunda con un cambio de política.

**Empalmes.** Dos series no tienen dato directo publicado en toda la ventana y se completarán con empalmes documentados. La serie diaria del EMBI empieza el 11 de diciembre de 1998; para 1996T1-1998T3 se usará el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA, serie oficial mensual desde octubre de 1994, y la tasa de fondos federales. Durante la convertibilidad, ese costo del dólar dentro del sistema financiero argentino refleja el riesgo argentino. La relación entre ambas series se estimará en la superposición 1998T4-2001T3, que termina antes del corralito porque este rompe ese mercado, y se validará de tres maneras: con el R² de la regresión, con una validación cruzada que deja un trimestre afuera por vez y con un pronóstico fuera de muestra de 2001 estimado solo con 1998T4-2000T4. El índice del TCRM del BCRA empieza en enero de 1997; para 1996 se encadenará hacia atrás con las variaciones del tipo de cambio real efectivo amplio del BIS, invertido porque ese índice sube con la apreciación, y se verificará la correlación entre las variaciones trimestrales de los dos índices en el período común. Para comprobar que los resultados no dependen de los empalmes, la estimación y la simulación se repetirán con datos desde 1999, solo con el EMBI observado.

**Variables, dimensiones e indicadores.**

**Tabla 1. Variables, indicadores y fuentes**

| Variable | Dimensión | Indicador | Fuente | Rol |
|---|---|---|---|---|
| Sostenibilidad de la deuda | Estabilización | Probabilidad de que la deuda no se estabilice en 2031 y 2035 | Elaboración propia con el criterio del FMI (2021) | Dependiente |
| Deuda federal bruta | Nivel de endeudamiento | Deuda bruta de la Administración Central, % del PIB | MECON; *stock* inicial del FMI (2026) | Entra rezagada y se acumula con la identidad (principal) |
| Deuda consolidada con el BCRA | Nivel de endeudamiento | Deuda del Tesoro y del BCRA neta de tenencias cruzadas, % del PIB | MECON y BCRA; *stock* inicial del FMI (2026) | Entra rezagada y se acumula con la identidad (extensión) |
| Política fiscal | Esfuerzo fiscal | Resultado primario sin rentas de la propiedad, % del PIB (con rentas, como robustez) | MECON | Endógena |
| Actividad | Crecimiento | Variación trimestral del PIB real | INDEC | Endógena |
| Riesgo soberano | Costo del financiamiento | EMBI (puntos básicos); 1996T1-1998T3 empalmado con la tasa interfinanciera en dólares menos la tasa de fondos federales | J.P. Morgan, serie diaria publicada por Ámbito Financiero; BCRA y Reserva Federal para el empalme | Endógena |
| Precios relativos | Efecto de valuación | TCRM; 1996 encadenado con el tipo de cambio real efectivo amplio | BCRA; BIS para el empalme | Endógena |
| Política monetaria de Estados Unidos | *Shock* externo | Tasa de fondos federales; tasa sombra en el límite cero (Wu y Xia, 2016) | Reserva Federal | Exógena |
| Condiciones financieras globales | Aversión al riesgo | VIX | CBOE | Exógena |
| Escenario base | Proyección oficial | Crecimiento, deflactor, tasa efectiva, resultado primario, ajuste *stock*-flujo e inflación relativa, 2026-2035 | FMI (2026), cuadro 6 | Supuesto de la simulación |

Fuente: elaboración propia.

La primera fila de la tabla es un indicador de síntesis: la probabilidad de no estabilización es un resultado del modelo, no un dato observado. La matriz de datos tiene una fila por trimestre y una columna por cada variable observada (deuda federal bruta, deuda consolidada con el BCRA, resultado primario, crecimiento, EMBI, TCRM, tasa de la FED y VIX).

**Procedimiento y pruebas.** El trabajo empírico seguirá siete pasos.

1. *Propiedades de las series.* Pruebas de raíz unitaria de Dickey y Fuller aumentada (ADF) y de Kwiatkowski, Phillips, Schmidt y Shin (KPSS); prueba de Zivot y Andrews, que admite un quiebre; quiebres múltiples de Bai y Perron (2003) sobre la serie de deuda, que entrarán como variables binarias; prueba de cointegración de Johansen.
2. *Especificación del sistema.* El SVARX tendrá cuatro variables endógenas (resultado primario, crecimiento, EMBI y TCRM) y, como exógenas, la variación de la tasa de la FED con dos rezagos, el VIX, variables binarias estacionales, las de los quiebres y una por mandato presidencial, para controlar los cambios de orientación de la política económica entre administraciones; su significancia conjunta se contrastará con pruebas de Wald y de razón de verosimilitud. La deuda entrará rezagada en las cuatro ecuaciones y se acumulará con la identidad contable, no con una ecuación estimada: así la deuda responde a los *shocks* del sistema y, a la vez, condiciona al resultado primario, al EMBI, al crecimiento y al TCRM en los trimestres siguientes, sin romper la contabilidad (Favero y Giavazzi, 2007). El efecto de esa retroalimentación se medirá comparando con una versión que la apaga. Se usará el crecimiento sin desestacionalizar, porque la serie desestacionalizada del INDEC empieza en 2004; la estacionalidad la absorberán las variables binarias trimestrales (Lütkepohl, 2005), en lugar de un filtro X-13 que agregaría un paso de estimación previo. La tasa de la deuda en dólares se construirá con la tasa efectiva del escenario más el desvío simulado del EMBI y del nivel de la tasa de la FED, que alcanza a la deuda a medida que se refinancia; la tasa de la deuda en pesos seguirá la del escenario, y la variante en la que el EMBI también la encarece se informará como robustez.
3. *Selección de rezagos.* El orden de rezagos será el que elija el criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones. Si los residuos de ese orden rechazan la ausencia de autocorrelación (Portmanteau con 12 rezagos, al 5%), se tomará el menor orden mayor que no la rechace (Lütkepohl, 2005, sec. 4.4); si ningún orden estable la pasa, el de mayor p-valor. Diagnóstico de residuos: autocorrelación, normalidad multivariada y heterocedasticidad condicional.
4. *Identificación.* Restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto: el resultado primario no responde dentro del trimestre a los *shocks* cambiarios y de riesgo, y su respuesta automática al ciclo se fija con una elasticidad de 0,25. Como robustez, dos ordenamientos de Cholesky (resultado primario primero y resultado primario último). La identificación no cambia la estimación central de la probabilidad de no estabilización, porque los *shocks* estructurales reconstruyen los mismos residuos; se necesita para repartir la varianza de la deuda por grupo de *shocks* y para definir el *shock* fiscal, de los que depende H1a.
5. *Inferencia.* Intervalos de 90% por *bootstrap*[^en-bootstrap] de bloques móviles de cuatro trimestres sobre los residuos, de diseño recursivo, en el que la deuda también se regenera (Brüggemann et al., 2016), con los percentiles de Hall (1992). La corrección del sesgo de muestra pequeña de Kilian (1998) se informará como robustez. Todas las especificaciones usarán los mismos números aleatorios, para que las diferencias entre ellas no provengan del sorteo.
6. *Simulación.* Monte Carlo de 2026 a 2035 sobre el escenario base del FMI (2026), desde su *stock* inicial, con los *shocks* estructurales remuestreados de la historia en bloques de ocho trimestres, como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI). El VIX y el nivel de la tasa de la FED se simularán con procesos autorregresivos de primer orden, con sus innovaciones remuestreadas junto con los *shocks* estructurales. El ajuste *stock*-flujo del escenario se escalará por la deuda en pesos simulada y la inflación relativa por la deuda en moneda extranjera; la proporción en pesos quedará fija, el mismo supuesto del FMI (2021, anexo VI). La retroalimentación de la deuda se actualizará al cierre de cada año, porque la identidad del FMI es anual. Antes de simular se verificará que la identidad reproduzca la senda de deuda del FMI.
7. *Contraste de hipótesis y robustez.* H1a: dos condiciones, la descomposición de la varianza de la deuda en 2035 por grupo de *shocks* y la suficiencia del superávit (con el resultado primario de 2031 en su máximo histórico, la probabilidad debe seguir por encima del 1% del FMI). H1b: el límite inferior del intervalo de 90% debe superar la probabilidad del FMI en 2031 y 2035, con cada métrica. H2: el intervalo de 90% de la diferencia entre el escenario de la FED y el base debe excluir el cero en 2035, en la probabilidad y en la deuda esperada (si se cumple en una y no en la otra, parcialmente respaldada), con dos escenarios: un nivel de la tasa más alto en un desvío estándar de su variación trimestral, en forma permanente, y la repetición de la senda de la tasa de 2022-2025. Robustez: deuda consolidada con el BCRA, estimada desde 2002; sin las binarias presidenciales; la otra definición del resultado primario; canal de tasas en pesos; sin retroalimentación; uno y tres rezagos; dos ordenamientos de Cholesky (resultado primario primero y resultado primario último) y elasticidades cíclicas de 0 y 0,5; sin los *shocks* del período de cesación de pagos y canje; datos desde 1999, sin empalmes; datos desde 2004; sin variables de quiebre; ajuste *stock*-flujo en cero; dos velocidades de refinanciación; el escenario del FMI de 2025; corrección de sesgo, y el procedimiento de *shocks* del propio FMI aplicado a la historia argentina.

**Alcances, alternativas descartadas y líneas futuras.** Las restricciones de signo y las de largo plazo de Blanchard y Quah (1989) no se usarán: exigen suponer, entre otras cosas, que el tipo de cambio real es neutral en el largo plazo, un supuesto difícil de sostener para la Argentina. La probabilidad de que la deuda supere el 100% del PIB se reemplazará por la métrica de no estabilización del FMI, porque ese umbral no tiene una fuente que lo justifique y la métrica del FMI permite comparar con su evaluación. Quedarán como líneas futuras, fuera del alcance de una tesis de grado, los *shocks* de política monetaria de la FED identificados con datos de alta frecuencia, los términos de intercambio como determinante externo, un módulo de balanza de pagos y un panel con Chile que compare la dinámica de la deuda en dos economías de la región.

# 3. Transferencia y beneficiarios

**Organismos públicos.** El Congreso de la Nación, que por la Ley 27.612 aprueba el endeudamiento en moneda extranjera bajo ley extranjera y los programas con el FMI, y su Oficina de Presupuesto, que analiza la deuda pública. El Ministerio de Economía y el BCRA, como usuarios de una evaluación probabilística de la deuda que complementa la del FMI con el mismo perímetro y la extiende a la deuda consolidada.

**Ámbito académico.** Estudiantes y cátedras de Macroeconomía, Finanzas Públicas y Econometría de la FCE, que dispondrán de una aplicación completa de un SVARX a la deuda argentina, con datos y código reproducibles.

**Analistas y sociedad.** Analistas de riesgo soberano y periodistas económicos, que podrán contrastar la probabilidad de no estabilización con la del FMI sobre una base comparable.

El conocimiento se transferirá mediante la tesis, su defensa pública y un repositorio con los datos y el código.

# 4. Cronograma de actividades

El mes 1 corresponde a marzo de 2026, cuando el grupo comenzó a trabajar con el director.

**Tabla 2. Cronograma de actividades por mes**

| Actividad | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Revisión bibliográfica y antecedentes | X | X | X | | | | | | | | | |
| Problema, preguntas, objetivos e hipótesis | X | X | | | | | | | | | | |
| Marco teórico | | X | X | X | | | | | | | | |
| Recolección de datos secundarios | | X | X | X | | | | | | | | |
| Construcción de las series de deuda y evaluación de las fuentes | | | X | X | X | | | | | | | |
| Pruebas de raíz unitaria, quiebres y cointegración | | | | | X | | | | | | | |
| Especificación, identificación y estimación del SVARX | | | | | X | X | | | | | | |
| Escenario base del FMI y simulación de Monte Carlo | | | | | | X | X | | | | | |
| Contraste de hipótesis | | | | | | | X | X | | | | |
| Revisión de la especificación y pruebas de robustez | | | | | | | X | X | | | | |
| Redacción de resultados, discusión y conclusiones | | | | | | | | X | X | | | |
| Revisión del director y correcciones | | | | | | | | | X | X | X | |
| Entrega y preparación de la defensa | | | | | | | | | | | X | X |

Fuente: elaboración propia.

# 5. Referencias bibliográficas

Ando, S., Mishra, P., Patel, N., Peralta-Alva, A., y Presbitero, A. F. (2025). Fiscal consolidation and public debt. *Journal of Economic Dynamics and Control*, *170*, artículo 104998. https://doi.org/10.1016/j.jedc.2024.104998

Bai, J., y Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics*, *18*(1), 1-22. https://doi.org/10.1002/jae.659

Blanchard, O. J., y Quah, D. (1989). The dynamic effects of aggregate demand and supply disturbances. *American Economic Review*, *79*(4), 655-673.

Blanchard, O., y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. *Quarterly Journal of Economics*, *117*(4), 1329-1368. https://doi.org/10.1162/003355302320935043

Bohn, H. (1998). The behavior of U.S. public debt and deficits. *Quarterly Journal of Economics*, *113*(3), 949-963. https://doi.org/10.1162/003355398555793

Brüggemann, R., Jentsch, C., y Trenkler, C. (2016). Inference in VARs with conditional heteroskedasticity of unknown form. *Journal of Econometrics*, *191*(1), 69-85. https://doi.org/10.1016/j.jeconom.2015.10.004

Calvo, G. A., Izquierdo, A., y Talvi, E. (2003). *Sudden stops, the real exchange rate, and fiscal sustainability: Argentina's lessons* (NBER Working Paper No. 9828). National Bureau of Economic Research. https://doi.org/10.3386/w9828

Celasun, O., Debrun, X., y Ostry, J. D. (2006). *Primary surplus behavior and risks to fiscal sustainability in emerging market countries: A "fan-chart" approach* (IMF Working Paper No. 06/67). Fondo Monetario Internacional. https://doi.org/10.5089/9781451863277.001

Díaz Alejandro, C. F. (1970). *Essays on the economic history of the Argentine Republic*. Yale University Press.

Favero, C., y Giavazzi, F. (2007). *Debt and the effects of fiscal policy* (NBER Working Paper No. 12822). National Bureau of Economic Research. https://doi.org/10.3386/w12822

Fondo Monetario Internacional [FMI]. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper).

Fondo Monetario Internacional [FMI]. (2025). *Argentina: Request for an extended arrangement under the Extended Fund Facility* (IMF Country Report No. 25/95).

Fondo Monetario Internacional [FMI]. (2026). *Argentina: 2026 Article IV consultation, second review under the extended arrangement under the Extended Fund Facility* (IMF Country Report No. 26/105).

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

Uribe, M., y Yue, V. Z. (2006). Country spreads and emerging countries: Who drives whom? *Journal of International Economics*, *69*(1), 6-36. https://doi.org/10.1016/j.jinteco.2005.04.003

Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking*, *48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300

[^en-default]: *Default*: cesación de pagos de la deuda.
[^en-shock]: *Shock*: perturbación inesperada que afecta a una variable y se transmite a las demás.
[^en-stock]: *Stock*: saldo de una variable en un momento dado, por oposición a un flujo.
[^en-bootstrap]: *Bootstrap*: método de remuestreo que aproxima la distribución de un estimador repitiendo la estimación sobre muestras generadas a partir de los propios datos.
