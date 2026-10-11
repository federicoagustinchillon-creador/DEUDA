# 1. Introducción

## 1.1 Contextualización

La historia macroeconómica de América Latina, y de la República Argentina en particular, está atravesada por un patrón recurrente de dependencia del crédito externo, vulnerabilidad ante la interrupción repentina de los flujos de capital (*sudden stops*)[^1] y crisis de impago soberano (Comín Comín, 2014, p. 699; Reinhart y Rogoff, 2009). En el caso argentino, ese patrón fue relevado por la historiografía económica desde mediados del siglo XX (Díaz Alejandro, 1970; della Paolera y Taylor, 2001; Rapoport, 2020) y volvió a manifestarse en el default de 2001 y en la reestructuración de 2020. Ambos episodios dejaron en evidencia la vulnerabilidad de una economía condicionada por la restricción externa de divisas.

La administración que asumió en diciembre de 2023 recibió un elevado stock de pasivos y un acceso muy limitado al crédito voluntario. El regreso a los mercados fue gradual: la primera colocación en dólares se realizó en diciembre de 2025, con un bono a 2029 bajo legislación local por USD 1.000 millones de valor nominal y un rendimiento de 9,26% anual (Secretaría de Finanzas, 2025). El precio de colocación fue de 91 por cada 100 nominales, de modo que el Tesoro recaudó unos USD 910 millones (Chequeado, 2025). En 2026 el Tesoro siguió financiándose con bonos en dólares bajo ley local y no emitió bajo legislación de Nueva York: en septiembre, el ministro de Economía afirmó que el Gobierno no tenía planes de emitir deuda internacional (Infobae, 2026). A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones, y los vencimientos en divisas previstos para el resto del año alcanzaban USD 5.080 millones, de los cuales el 53,5% correspondía a pagos al Fondo Monetario Internacional (FMI) (Oficina de Presupuesto del Congreso [OPC], 2026).

## 1.2 Planteamiento del problema

Frente a esta coyuntura, surge la necesidad de evaluar si la consecución de un superávit fiscal primario y la voluntad política de pago bastan para asegurar la sostenibilidad de la deuda en el mediano plazo. La alternativa es que los determinantes estructurales de la economía argentina condicionen el resultado fiscal e incrementen la probabilidad de un nuevo default o reestructuración soberana.

La evidencia internacional matiza la premisa de que la consolidación presupuestaria alcanza para disipar el riesgo de impago: en promedio, los ajustes fiscales discrecionales tienen un efecto reducido sobre la ratio de deuda, y solo se asocian con reducciones duraderas cuando se aplican en fases de expansión económica (Ando et al., 2025). La sostenibilidad depende además de otros factores. Uno es la capacidad de la economía de generar las divisas que exige el servicio de una deuda dolarizada (Calvo et al., 2003). Otro es el efecto de valuación del tipo de cambio real sobre los pasivos en moneda extranjera (Levy Yeyati y Sturzenegger, 2023). Se suman la exposición de la deuda a las condiciones financieras externas (Adler y Sosa, 2013) y la menor tolerancia a la deuda de las economías con historia de default (Reinhart et al., 2003). Por último, la incertidumbre macroeconómica reduce el nivel de deuda que un gobierno puede sostener (Mendoza y Oviedo, 2009), y existe un límite político e institucional a los superávits que una sociedad acepta de manera prolongada, conocido como fatiga fiscal (Ghosh et al., 2013).

## 1.3 Preguntas de investigación

La pregunta principal es: ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario de Argentina (1996-2025) condicionan la sostenibilidad de su deuda pública consolidada, que suma la del Sector Público No Financiero (SPNF) y la del Banco Central de la República Argentina (BCRA), en el horizonte 2026-2035, y cuál es la probabilidad de que esa trayectoria resulte insostenible?

Como pregunta específica, se plantea: ¿cómo y en qué magnitud impactaría un endurecimiento de la política monetaria de la Reserva Federal de los Estados Unidos (FED) sobre la dinámica de la deuda pública consolidada argentina y sobre su probabilidad de no estabilizarse durante 2026-2035?

La elección de esta perturbación se fundamenta en que opera simultáneamente sobre varios canales. Encarece el financiamiento externo y eleva el riesgo soberano (Uribe y Yue, 2006). Desencadena una depreciación del tipo de cambio real, con efectos de valuación sobre los pasivos dolarizados (Calvo et al., 2003). Deprime el crecimiento y, con ello, deteriora el diferencial entre la tasa de interés y el crecimiento (Blanchard, 2019; Neumeyer y Perri, 2005; Uribe y Yue, 2006). Por último, condiciona la transmisión de la política monetaria doméstica en las economías emergentes (Renzhi y Beirne, 2024). En Argentina, ese último canal operó durante buena parte del período histórico a través del costo de los pasivos remunerados del BCRA, cuyo stock llegó a 18,4% del PIB en 2023 y cayó a 2,2% en 2024, cuando la esterilización monetaria pasó al Tesoro (FMI, 2025, anexo II, cuadro 2).

## 1.4 Objetivos

El objetivo general es evaluar la dinámica de la deuda pública consolidada argentina (SPNF y BCRA) a partir de sus determinantes macroeconómicos históricos (1996-2025), para proyectar su sostenibilidad en el horizonte 2026-2035 y estimar la probabilidad de que no se estabilice.

Para alcanzarlo, se plantean los siguientes objetivos específicos:

1. Construir una serie trimestral de deuda pública consolidada (SPNF y pasivos remunerados del BCRA) para 1996-2025.
2. Analizar las propiedades estocásticas de las series (raíz unitaria y quiebres estructurales).
3. Estimar un modelo de vectores autorregresivos estructural con variables exógenas (SVARX), en el que la deuda consolidada interactúa con el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario, y en el que la tasa de la FED y la volatilidad financiera global entran como variables exógenas.
4. Medir la contribución de cada canal a la variabilidad de la deuda y la reacción del resultado primario ante el nivel de endeudamiento.
5. Simular, mediante el método de Monte Carlo, la distribución de trayectorias de la deuda consolidada en 2026-2035 bajo un escenario base.
6. Estimar el impacto de un endurecimiento de la política monetaria de la FED sobre esa distribución.

## 1.5 Hipótesis

H1a. Los determinantes macroeconómicos históricos de Argentina (1996-2025), es decir, el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario, condicionan la sostenibilidad de la deuda pública consolidada (SPNF y BCRA), de modo que el superávit primario, por sí solo, no basta para estabilizarla en 2026-2035.

H1b. La probabilidad de que la deuda consolidada no se estabilice, medida a cinco años (2030, el mismo horizonte de la métrica del FMI) y a diez años (2035, el final del horizonte de proyección) y estimada con shocks estructuralmente identificados, es mayor que la que el FMI reporta para la deuda federal bruta en su análisis de 2025, de alrededor de 3% (FMI, 2025, anexo II). Para que la comparación sea válida, el escenario base de la simulación reproduce los supuestos del escenario base del FMI.

H2. Un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda consolidada y su probabilidad de no estabilizarse, a través del riesgo soberano, el tipo de cambio real y el crecimiento. El shock se mide de dos maneras: un desvío estándar de la variación trimestral de la tasa (convención de la literatura de VAR) y una repetición del ciclo de subas de 2022-2023.

## 1.6 Estrategia metodológica

Para contrastar estas hipótesis se estima un SVARX con datos trimestrales de Argentina (1996-2025). La deuda consolidada entra como variable del sistema, de modo que los shocks se transmiten entre las variables en ambos sentidos: la deuda responde al riesgo país, al tipo de cambio y al resultado fiscal, y a la vez los afecta en los trimestres siguientes. La evolución de la deuda respeta la identidad contable de acumulación, que distingue el tramo en moneda local del tramo en moneda extranjera. Los resultados del modelo alimentan simulaciones de Monte Carlo que generan distribuciones de probabilidad sobre la trayectoria de la deuda en 2026-2035, cuyos resultados se resumen en gráficos de abanico (*fan charts*)[^2] y en las métricas que utiliza el FMI para evaluar el riesgo soberano.

## 1.7 Justificación

La Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública exige, desde 2021, que todo nuevo endeudamiento del Estado nacional se someta a un análisis de sostenibilidad. La literatura académica local, sin embargo, no dispone de un protocolo econométrico propio, replicable y contrastado que dé contenido empírico a esa exigencia.

El precedente metodológico directo es Medeiros (2012), quien combinó un modelo VAR con una función de reacción fiscal para simular la trayectoria de la deuda y construir distribuciones de probabilidad en lugar de escenarios únicos. El FMI adoptó luego esa lógica en su Marco de Riesgo Soberano y Sostenibilidad de la Deuda (SRDSF), aplicado a Argentina en sus revisiones del programa (FMI, 2024, 2025). Esta tesis retoma esa arquitectura y la especifica para el caso argentino en dos direcciones. La primera es metodológica: identifica de manera explícita los canales de transmisión entre el resultado fiscal, el riesgo soberano, el tipo de cambio real y la actividad, e incorpora un shock externo de origen identificable, la política monetaria de la FED. La segunda es de cobertura: estima la dinámica histórica de la deuda incluyendo los pasivos remunerados del BCRA, que el propio FMI considera parte de la deuda pública cuando pueden financiar al Tesoro o representan un riesgo fiscal material (FMI, 2021).

## 1.8 Organización del trabajo

El Capítulo 2 revisa los antecedentes y delimita el área de vacancia. El Capítulo 3 presenta el marco teórico. El Capítulo 4 describe la estrategia metodológica y el Capítulo 5, los datos. El Capítulo 6 expone los resultados, incluido el escenario de shock de la FED. El Capítulo 7 los discute y el Capítulo 8 presenta las conclusiones y las limitaciones. [AJUSTAR cuando se cierre el índice.]

[^1]: Interrupción repentina de los flujos de capital.
[^2]: Gráficos que muestran la distribución de trayectorias posibles de una variable mediante bandas de percentiles.

---

## Referencias

Ver `referencias_y_notas.md` (lista única de Introducción y Antecedentes, verificada).

## Nota 1: criterio de H1b

Ver `referencias_y_notas.md`, nota 1 (versión vigente del criterio).

## Nota 2: tamaño del shock de la FED (pendiente)

En la versión anterior puse "+100 puntos básicos" sin justificarlo: fue un error mío y lo saqué.
Hay dos criterios defendibles, a elegir cuando tengamos la serie:

- *Un desvío estándar* de la variación trimestral de la tasa sombra de la FED en la muestra
  1996-2025. Es la convención de la literatura de VAR: el shock tiene el tamaño típico
  observado en los datos.
- *Un episodio histórico real*, por ejemplo el ciclo de subas de 2022-2023, replicado como
  escenario. Tiene la ventaja de ser concreto y fácil de explicar.

Se puede usar el primero para las respuestas al impulso y el segundo para el Monte Carlo.

## Nota 3: el área de vacancia (ver `antecedentes.md`)

Santiago escribió que el marco del FMI "excluye los pasivos remunerados del Banco Central".
**No es correcto.** La revisión del marco (FMI, 2021, anexo II, párr. 5) establece que las
letras de liquidez del banco central se incluyen en la deuda pública cuando pueden financiar al
gobierno, cuando el gobierno responde de hecho por su servicio o cuando representan un riesgo
fiscal material. Además, cita expresamente a Argentina: esas letras sumaban 5% del PIB a fines
de 2018 (nota 8). La vacancia se reescribe en el archivo aparte.
