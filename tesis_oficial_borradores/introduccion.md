# 1. Introducción

## 1.1 Contextualización

La historia macroeconómica de América Latina, y de la República Argentina en particular, está atravesada por un patrón recurrente de dependencia del crédito externo, vulnerabilidad ante la interrupción repentina de los flujos de capital (*sudden stops*)[^1] y crisis de impago soberano (Comín Comín, 2014, p. 699; Reinhart y Rogoff, 2009). En el caso argentino, ese patrón fue relevado por la historiografía económica (Díaz Alejandro, 1970; della Paolera y Taylor, 2001; Rapoport, 2020) y volvió a manifestarse en el default[^en-default] de 2001 y en la reestructuración de 2020. Ambos episodios dejaron en evidencia la vulnerabilidad de una economía condicionada por la restricción externa de divisas.

La administración que asumió en diciembre de 2023 recibió un elevado stock[^en-stock] de pasivos y un acceso muy limitado al crédito voluntario. El regreso a los mercados fue gradual: la primera colocación en dólares se realizó en diciembre de 2025, con un bono a 2029 bajo legislación local por USD 1.000 millones de valor nominal y un rendimiento de 9,26% anual. El precio de corte fue de USD 910 por cada USD 1.000 nominales, de modo que el Tesoro recaudó USD 910 millones (Secretaría de Finanzas, 2025). En 2026 el Tesoro siguió financiándose con bonos en dólares bajo ley local y no emitió bajo legislación de Nueva York: en septiembre, en un encuentro con inversores en Nueva York, el ministro de Economía afirmó que el Gobierno no tenía planes de emitir deuda internacional (Infobae, 2026). A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones, y los vencimientos en divisas previstos para el resto del año alcanzaban USD 5.080 millones, de los cuales el 53,5% correspondía a pagos al Fondo Monetario Internacional (FMI) (Oficina de Presupuesto del Congreso [OPC], 2026).

## 1.2 Planteamiento del problema

El problema que aborda esta tesis es si un superávit fiscal primario alcanza para asegurar la sostenibilidad de la deuda en el mediano plazo. La alternativa es que los determinantes estructurales de la economía argentina condicionen el resultado fiscal de modo que, aun con superávit, la deuda no se estabilice.

La evidencia internacional matiza la premisa de que la consolidación presupuestaria alcanza para disipar el riesgo de impago: en promedio, los ajustes fiscales discrecionales tienen un efecto reducido sobre la ratio de deuda, y solo se asocian con reducciones duraderas cuando se aplican en fases de expansión económica (Ando et al., 2025). La sostenibilidad depende también de otros factores. Uno es la capacidad de la economía de generar las divisas que exige el servicio de una deuda dolarizada (Calvo et al., 2003). Otro es el efecto de valuación del tipo de cambio real sobre los pasivos en moneda extranjera (Levy Yeyati y Sturzenegger, 2023). Se suman la exposición de la deuda a las condiciones financieras externas (Adler y Sosa, 2013) y la menor tolerancia a la deuda de las economías con historia de default (Reinhart et al., 2003). La incertidumbre macroeconómica reduce, por otra parte, el nivel de deuda que un gobierno puede sostener (Mendoza y Oviedo, 2009), y existe un límite político e institucional a los superávits que una sociedad acepta de manera prolongada, conocido como fatiga fiscal (Ghosh et al., 2013).

## 1.3 Preguntas de investigación

La deuda pública que se estudia es la deuda bruta del gobierno federal (Administración Central), el perímetro sobre el que el FMI evalúa la sostenibilidad de la deuda argentina. Como extensión se estudia la deuda del sector público consolidado con el Banco Central de la República Argentina (BCRA). La pregunta principal tiene dos partes. La primera es: ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario de Argentina en 1996-2025 condicionan la sostenibilidad de la deuda pública en el horizonte 2026-2035? La segunda es: ¿cuál es la probabilidad de que la deuda no se estabilice bajo el escenario base?

Como pregunta específica, se plantea: ¿cómo y en qué magnitud impactaría un endurecimiento de la política monetaria de la Reserva Federal de los Estados Unidos (FED) sobre la dinámica de la deuda pública argentina y sobre su probabilidad de no estabilizarse durante 2026-2035?

La elección de esta perturbación se fundamenta en que opera simultáneamente sobre varios canales. Encarece el financiamiento externo y eleva el riesgo soberano (Uribe y Yue, 2006). Desencadena una depreciación del tipo de cambio real, con efectos de valuación sobre los pasivos dolarizados (Calvo et al., 2003). Deprime el crecimiento y, con ello, deteriora el diferencial entre la tasa de interés y el crecimiento (Neumeyer y Perri, 2005; Uribe y Yue, 2006). También condiciona la transmisión de la política monetaria doméstica en las economías emergentes (Renzhi y Beirne, 2024). En Argentina, ese último canal operó durante buena parte del período histórico a través del costo de los pasivos del BCRA, que sumaban 19,2% del producto interno bruto (PIB) a fines de 2023 y 3,3% a fines de 2025, después de que la esterilización monetaria pasara al Tesoro (FMI, 2026, anexo II, cuadro 2, línea 4; sección 5.5).

## 1.4 Objetivos

El objetivo general es evaluar la dinámica de la deuda pública argentina a partir de sus determinantes macroeconómicos históricos en 1996-2025, para proyectarla en el horizonte 2026-2035 y estimar la probabilidad de que no se estabilice.

Para alcanzarlo, se plantean los siguientes objetivos específicos:

1. Construir series trimestrales de la deuda federal bruta y de la deuda consolidada con el BCRA para 1996-2025. La segunda es la deuda del Tesoro nacional que no está en poder del BCRA, más los pasivos remunerados del BCRA, menos los depósitos del Tesoro en el BCRA. La deuda consolidada con el BCRA se estima desde 2002, el año desde el cual la autonomía del BCRA se redujo y la consolidación tiene fundamento en el criterio del FMI (sección 2.9).
2. Analizar las propiedades estocásticas de las series (raíz unitaria y quiebres estructurales).
3. Estimar un modelo de vectores autorregresivos estructural con variables exógenas (SVARX), en el que la deuda pública interactúa con el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario, y en el que la tasa de política monetaria de la FED y la volatilidad financiera global entran como variables exógenas.
4. Medir la contribución de los bloques de *shocks*[^en-shock] fiscal, de actividad, cambiario y de riesgo, y externo a la variabilidad de la deuda, y la reacción del resultado primario ante el nivel de endeudamiento.
5. Simular, mediante el método de Monte Carlo, la distribución de trayectorias de la deuda federal bruta en 2026-2035 bajo el escenario base del FMI, y repetir la simulación con la deuda consolidada con el BCRA.
6. Estimar el impacto de un endurecimiento de la política monetaria de la FED sobre esa distribución.

## 1.5 Hipótesis

H1a. Los determinantes macroeconómicos históricos de Argentina en 1996-2025 (el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario) condicionan la sostenibilidad de la deuda pública (la federal bruta en la especificación principal y la consolidada con el BCRA como extensión), de modo que el superávit primario, por sí solo, no basta para estabilizarla en 2026-2035.

H1b. La probabilidad de que la deuda pública no se estabilice, medida en 2031 (el último año del abanico de mediano plazo del FMI) y en 2035 (el final del horizonte de proyección y de su abanico de diez años), es mayor que la que el FMI reporta en su análisis más reciente: alrededor de 1% a mediano plazo y menos de 3% a diez años (FMI, 2026). Para que la comparación sea válida, se hace sobre el perímetro que usa el FMI, la deuda federal bruta, con el mismo punto de partida y el mismo escenario base. La no estabilización se mide de dos maneras: con una métrica anual, que compara cada año el resultado primario previsto con el que estabilizaría la deuda ese año, y con la definición operativa del FMI, que promedia los *shocks* a lo largo de la trayectoria (sección 4.6).

H2. Un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda pública (la federal bruta en la especificación principal y la consolidada con el BCRA como extensión) y su probabilidad de no estabilizarse. La hipótesis se refiere al efecto total; los canales por los que opera (riesgo soberano, tipo de cambio real, crecimiento y costo directo de la deuda en dólares) se describen en la sección 4.3 y se examinan por separado en el Capítulo 6, sin ser parte del contraste. En la extensión con la deuda consolidada, que es exploratoria, se contrastan solo la probabilidad de no estabilización y el efecto de la FED sobre ella (sección 6.6). El *shock* se mide de dos maneras: un nivel de la tasa más alto en forma permanente, en un desvío estándar de su variación trimestral (convención de la literatura de vectores autorregresivos, VAR), y una repetición de la senda efectiva de la tasa en 2022-2025.

## 1.6 Estrategia metodológica

Para contrastar estas hipótesis se estima un SVARX con datos trimestrales de Argentina de 1996-2025. Las variables endógenas son el resultado primario, el crecimiento, el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), y el tipo de cambio real multilateral (TCRM). La tasa de política monetaria de la FED y el índice de volatilidad VIX entran como exógenas, junto con variables binarias estacionales, de quiebre y por mandato presidencial. Los *shocks* se identifican con restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto; como robustez se usan dos ordenamientos de Cholesky (resultado primario primero y resultado primario último). La deuda federal bruta entra rezagada en todas las ecuaciones del sistema y se acumula con la identidad contable, de modo que el diseño permite la retroalimentación en ambos sentidos: la deuda puede responder al EMBI, al TCRM y al resultado primario, y a la vez afectarlos en los trimestres siguientes. Qué canales de retroalimentación resultan distinguibles de cero se establece en el Capítulo 6. La identidad de acumulación distingue el tramo en moneda local del tramo en moneda extranjera e incorpora el ajuste stock-flujo del escenario del FMI. El modelo estimado alimenta simulaciones de Monte Carlo alrededor del escenario base del FMI, con su mismo punto de partida, que generan distribuciones de probabilidad sobre la trayectoria de la deuda en 2026-2035. Los resultados se resumen en gráficos de abanico (*fan charts*)[^2] y en la probabilidad de no estabilización, medida con una métrica anual y con la definición operativa del FMI. El mismo ejercicio se repite con la deuda consolidada con el BCRA, estimada desde 2002.

## 1.7 Justificación

La Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública, sancionada en 2021, dio al Congreso un papel mayor en las decisiones de endeudamiento. Exige una ley especial para emitir títulos en moneda extranjera bajo legislación y jurisdicción extranjeras por encima del máximo que fije la Ley de Presupuesto (art. 1) y una ley que apruebe de manera expresa cada programa con el FMI y sus ampliaciones (art. 2). Para esas decisiones hacen falta evaluaciones de la sostenibilidad de la deuda, y en la literatura revisada (sección 2.9) no se encontró una estimación para Argentina con *shocks* identificados cuyo resultado se compare con la probabilidad de no estabilización del FMI, sobre el perímetro y el escenario del propio FMI.

El precedente metodológico es la arquitectura de Celasun et al. (2006), desarrollada en el FMI y extendida por Medeiros (2012) en la Comisión Europea: un modelo VAR combinado con una función de reacción fiscal, que simula la trayectoria de la deuda y construye distribuciones de probabilidad en lugar de escenarios únicos. El FMI la incorporó a su marco de 2021, el Marco de Riesgo Soberano y Sostenibilidad de la Deuda (SRDSF; FMI, 2021, 2022), que aplicó a Argentina en sus revisiones del programa (FMI, 2024, 2025, 2026). Esta tesis retoma esa arquitectura y la especifica para el caso argentino en dos direcciones. La primera es metodológica: identifica de manera explícita los canales de transmisión entre el resultado fiscal, el riesgo soberano, el tipo de cambio real y la actividad, e incorpora un *shock* externo de origen identificable, la política monetaria de la FED. Como la simulación usa el perímetro, el punto de partida y el escenario del FMI, y también la definición operativa de su métrica, su resultado se compara de manera directa con la probabilidad que el organismo informa para Argentina. La segunda es de cobertura: estima también la dinámica de la deuda consolidada con el BCRA, cuyos pasivos el propio FMI considera parte de la deuda pública cuando pueden financiar al Tesoro o representan un riesgo fiscal material (FMI, 2021).

## 1.8 Organización del trabajo

El Capítulo 2 revisa los antecedentes y delimita el área de vacancia. El Capítulo 3 presenta el marco teórico. El Capítulo 4 describe la estrategia metodológica y el Capítulo 5, los datos. El Capítulo 6 expone los resultados, incluidos los escenarios de *shock* de la FED. El Capítulo 7 los discute y presenta, en la sección 7.6, las limitaciones. El Capítulo 8 reúne las conclusiones. El Apéndice estadístico completa las pruebas y estimaciones.

[^1]: Interrupción abrupta de la entrada neta de capitales, que obliga a un ajuste rápido de la cuenta corriente (Calvo et al., 2003).
[^2]: Gráficos que muestran la distribución de trayectorias posibles de una variable mediante bandas de percentiles.

---

[^en-default]: *Default*: cesación de pagos de la deuda.
[^en-stock]: *Stock*: saldo de una variable en un momento dado, por oposición a un flujo.
[^en-shock]: *Shock*: perturbación inesperada que afecta a una variable del sistema y se transmite a las demás.

## Referencias

Ver `referencias_y_notas.md` (lista única de Introducción y Antecedentes, verificada).

## Nota 1: criterio de H1b

Ver `referencias_y_notas.md`, nota 1 (versión vigente del criterio).

## Nota 2: tamaño del shock de la FED (decidido)

Los "+100 puntos básicos" de una versión anterior no estaban justificados y se sacaron. Se usan
los dos criterios (ver `referencias_y_notas.md`, nota 2): un nivel de la tasa más alto en forma
permanente, en un desvío estándar de su variación trimestral en la muestra (0,501 puntos), y la
repetición de la senda trimestral de 2022-2025 en 2026-2029.

## Nota 3: el área de vacancia (ver `antecedentes.md`)

La versión anterior decía que el marco del FMI "excluye los pasivos remunerados del Banco Central".
**No es correcto.** La revisión del marco (FMI, 2021, anexo II, párr. 5) establece que las
letras de liquidez del banco central se incluyen en la deuda pública cuando pueden financiar al
gobierno, cuando el gobierno responde de hecho por su servicio o cuando representan un riesgo
fiscal material, y cita expresamente a Argentina: esas letras sumaban 5% del PIB a fines
de 2018 (nota 8). La vacancia se reescribe en el archivo aparte.
