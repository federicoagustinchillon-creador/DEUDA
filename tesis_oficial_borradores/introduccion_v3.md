# 1. Introducción (versión 3, borrador para revisar)

Base: `Introduccion_corregida.docx` de Santiago (última edición 2026-10-07). Se le suman la
Justificación y la lista de objetivos específicos de `tesis/capitulos/01_introduccion.tex`.
Las marcas `[VERIFICAR]` y `[DECIDIR]` son pendientes y se borran antes de pasar a Word.

---

## 1.1 Contextualización

La historia macroeconómica de América Latina, y de la República Argentina en particular, está atravesada por un patrón recurrente de dependencia del crédito externo, vulnerabilidad ante la interrupción repentina de los flujos de capital (*sudden stops*)[^1] y crisis de impago soberano (Comín Comín, 2014, p. 699; Reinhart y Rogoff, 2009). En el caso argentino, ese patrón fue relevado por la historiografía económica desde mediados del siglo XX (Díaz Alejandro, 1970; della Paolera y Taylor, 2001; Rapoport, 2020) y volvió a manifestarse en el default de 2001 y en la reestructuración de 2020. Ambos episodios dejaron en evidencia la vulnerabilidad de una economía condicionada por la restricción externa de divisas.

La administración que asumió en diciembre de 2023 recibió un elevado stock de pasivos y un acceso muy limitado al crédito voluntario. El regreso a los mercados fue gradual: la primera colocación en dólares se realizó en diciembre de 2025, por USD 1.000 millones a una tasa de 9,26% anual y bajo legislación local. [VERIFICAR antes de entregar: si hubo emisión bajo ley de Nueva York en 2026.] A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones, y los vencimientos en divisas previstos para el resto del año alcanzaban USD 5.080 millones, de los cuales el 53,5% correspondía a pagos al Fondo Monetario Internacional (FMI) (Oficina de Presupuesto del Congreso [OPC], 2026).

## 1.2 Planteamiento del problema

Frente a esta coyuntura, surge la necesidad de evaluar si la consecución de un superávit fiscal primario y la voluntad política de pago bastan para asegurar la sostenibilidad de la deuda en el mediano plazo. La alternativa es que los determinantes estructurales de la economía argentina condicionen el resultado fiscal e incrementen la probabilidad de un nuevo default o reestructuración soberana.

La evidencia internacional matiza la premisa de que la consolidación presupuestaria alcanza para disipar el riesgo de impago: en promedio, los ajustes fiscales discrecionales tienen un efecto reducido sobre la ratio de deuda, y solo se asocian con reducciones duraderas cuando se aplican en fases de expansión económica (Ando et al., 2025). La sostenibilidad depende además de otros factores. Uno es la capacidad de la economía de generar las divisas que exige el servicio de una deuda dolarizada (Calvo et al., 2003). Otro es el efecto de valuación del tipo de cambio real sobre los pasivos en moneda extranjera (Levy Yeyati y Sturzenegger, 2023). Se suman la volatilidad de los spreads de riesgo país ante shocks financieros externos (Adler y Sosa, 2014) y la menor tolerancia a la deuda de las economías con historia de default (Reinhart et al., 2003). Por último, la incertidumbre macroeconómica reduce el nivel de deuda que un gobierno puede sostener (Mendoza y Oviedo, 2007), y existe un límite político e institucional a los superávits que una sociedad acepta de manera prolongada, conocido como fatiga fiscal (Ghosh et al., 2013).

## 1.3 Preguntas de investigación

La pregunta principal es: ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario de Argentina (1996-2025) condicionan la sostenibilidad de su deuda pública consolidada, que suma la del Sector Público No Financiero (SPNF) y la del Banco Central de la República Argentina (BCRA), en el horizonte 2026-2035, y cuál es la probabilidad de que esa trayectoria resulte insostenible?

Como pregunta específica, se plantea: ¿cómo y en qué magnitud impactaría un endurecimiento de la política monetaria de la Reserva Federal de los Estados Unidos (FED) sobre la dinámica de la deuda pública consolidada argentina y sobre su probabilidad de no estabilizarse durante 2026-2035?

La elección de esta perturbación se fundamenta en que opera simultáneamente sobre varios canales. Encarece el financiamiento externo y eleva el riesgo soberano (Klemm et al., 2014). Desencadena una depreciación del tipo de cambio real, con efectos de valuación sobre los pasivos dolarizados (Adler y Sosa, 2014; Calvo et al., 2003). Deprime el crecimiento y, con ello, deteriora el diferencial entre la tasa de interés y el crecimiento (Blanchard, 2019; Neumeyer y Perri, 2005; Uribe y Yue, 2006). Por último, condiciona la transmisión de la política monetaria doméstica en las economías emergentes (Renzhi y Beirne, 2024). En Argentina, ese último canal operó durante buena parte del período histórico a través del costo de los pasivos remunerados del BCRA, cuyo stock llegó a representar cerca del 9,5% del PIB en 2022-2023. Desde mediados de 2024, con el traspaso de la esterilización monetaria al Tesoro, ese stock se redujo a niveles mínimos. [VERIFICAR con la serie que se construya en el paso de datos: nivel de los pasivos remunerados del BCRA a fines de 2025.]

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

H1a. La dinámica de la deuda pública consolidada argentina (1996-2025) responde en mayor medida a los canales cambiario y de riesgo soberano que al resultado primario, cuya reacción ante el nivel de deuda no es estadísticamente significativa. En consecuencia, el superávit primario, por sí solo, no basta para estabilizar la deuda en 2026-2035.

H1b. En el escenario base, la probabilidad de que la deuda consolidada no se estabilice hacia el final del horizonte de proyección supera el 50%. La métrica es la que el FMI utiliza en su marco de riesgo soberano (FMI, 2021), y el corte del 50% equivale a afirmar que la trayectoria mediana de la distribución simulada no se estabiliza (la justificación se desarrolla en el Capítulo 4).

H2. Un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda consolidada y su probabilidad de no estabilizarse, a través del riesgo soberano, el tipo de cambio real y el crecimiento. [DECIDIR el tamaño del shock con criterio justificado: ver nota 2 al final del archivo.]

## 1.6 Estrategia metodológica

Para contrastar estas hipótesis se estima un SVARX con datos trimestrales de Argentina (1996-2025). La deuda consolidada entra como variable del sistema, de modo que los shocks se transmiten entre las variables en ambos sentidos: la deuda responde al riesgo país, al tipo de cambio y al resultado fiscal, y a la vez los afecta en los trimestres siguientes. La evolución de la deuda respeta la identidad contable de acumulación, que distingue el tramo en moneda local del tramo en moneda extranjera. Los resultados del modelo alimentan simulaciones de Monte Carlo que generan distribuciones de probabilidad sobre la trayectoria de la deuda en 2026-2035, cuyos resultados se resumen en gráficos de abanico (*fan charts*)[^2] y en las métricas que utiliza el FMI para evaluar el riesgo soberano.

## 1.7 Justificación

La Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública exige, desde 2021, que todo nuevo endeudamiento del Estado nacional se someta a un análisis de sostenibilidad. La literatura académica local, sin embargo, no dispone de un protocolo econométrico propio, replicable y contrastado que dé contenido empírico a esa exigencia.

El precedente metodológico directo es Medeiros (2012), quien combinó un modelo VAR con una función de reacción fiscal para simular la trayectoria de la deuda y construir distribuciones de probabilidad en lugar de escenarios únicos. El FMI adoptó luego esa lógica en su Marco de Riesgo Soberano y Sostenibilidad de la Deuda (SRDSF), aplicado a Argentina en 2024 (FMI, 2024). Esta tesis retoma esa arquitectura y la especifica para el caso argentino en dos direcciones. La primera es metodológica: identifica de manera explícita los canales de transmisión entre el resultado fiscal, el riesgo soberano, el tipo de cambio real y la actividad, e incorpora un shock externo de origen identificable, la política monetaria de la FED. La segunda es de cobertura: estima la dinámica histórica de la deuda incluyendo los pasivos remunerados del BCRA, que el propio FMI considera parte de la deuda pública cuando pueden financiar al Tesoro o representan un riesgo fiscal material (FMI, 2021).

## 1.8 Organización del trabajo

El Capítulo 2 revisa los antecedentes y delimita el área de vacancia. El Capítulo 3 presenta el marco teórico. El Capítulo 4 describe la estrategia metodológica y el Capítulo 5, los datos. El Capítulo 6 expone los resultados, incluido el escenario de shock de la FED. El Capítulo 7 los discute y el Capítulo 8 presenta las conclusiones y las limitaciones. [AJUSTAR cuando se cierre el índice.]

[^1]: Interrupción repentina de los flujos de capital.
[^2]: Gráficos que muestran la distribución de trayectorias posibles de una variable mediante bandas de percentiles.

---

## Referencias citadas en la Introducción

- Adler, G., y Sosa, S. (2014). External conditions and debt sustainability in Latin America. En D. Iakova, L. M. Cubeddu, G. Adler y S. Sosa (Eds.), *Latin America: New challenges to growth and stability*. Fondo Monetario Internacional.
- Ando, S., Mishra, P., Patel, N., Peralta-Alva, A., y Presbitero, A. F. (2025). Fiscal consolidation and public debt. *Journal of Economic Dynamics and Control*, 170. [VERIFICAR número de artículo. Versión previa: CEPR DP 18548, 2023.]
- Blanchard, O. (2019). Public debt and low interest rates. *American Economic Review*, 109(4), 1197-1229.
- Calvo, G. A., Izquierdo, A., y Talvi, E. (2003). *Sudden stops, the real exchange rate, and fiscal sustainability: Argentina's lessons* (NBER Working Paper No. 9828).
- Comín Comín, F. (2014). *Historia económica mundial: De los orígenes a la actualidad*. Alianza Editorial.
- della Paolera, G., y Taylor, A. M. (2001). *Straining at the anchor: The Argentine currency board and the search for macroeconomic stability, 1880-1935*. University of Chicago Press.
- Díaz Alejandro, C. F. (1970). *Essays on the economic history of the Argentine Republic*. Yale University Press.
- Fondo Monetario Internacional. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper, aprobado por el Directorio el 14 de enero de 2021).
- Fondo Monetario Internacional. (2024). *Argentina: Eighth review under the extended arrangement under the Extended Fund Facility* (IMF Country Report No. 24/167). [VERIFICAR número: en `referencias.bib` figura como "Eighth and Ninth Reviews".]
- Ghosh, A. R., Kim, J. I., Mendoza, E. G., Ostry, J. D., y Qureshi, M. S. (2013). Fiscal fatigue, fiscal space and debt sustainability in advanced economies. *The Economic Journal*, 123(566), F4-F30.
- Klemm, A., Meier, A., y Sosa, S. (2014). Spillovers to Latin America from the normalization of U.S. monetary policy. En Iakova et al. (Eds.), *op. cit.*
- Levy Yeyati, E., y Sturzenegger, F. (2023). A balance-sheet approach to fiscal sustainability. *Fiscal Studies*, 44(1), 61-84.
- Medeiros, J. (2012). *Stochastic debt simulation using VAR models and a panel fiscal reaction function* (European Economy Economic Papers 459). Comisión Europea.
- Mendoza, E. G., y Oviedo, P. M. (2007). Public debt, fiscal solvency and macroeconomic uncertainty in Latin America. *Economía*. [COMPLETAR volumen y páginas.]
- Neumeyer, P. A., y Perri, F. (2005). Business cycles in emerging economies: The role of interest rates. *Journal of Monetary Economics*, 52(2), 345-380.
- Oficina de Presupuesto del Congreso. (2026). *Operaciones de deuda pública, julio 2026*. https://opc.gob.ar/operaciones-de-deuda-publica/operaciones-de-deuda-publica-julio-2026/
- Rapoport, M. (2020). *Historia económica, política y social de la Argentina (1880-2003)*. Crítica.
- Reinhart, C. M., y Rogoff, K. S. (2009). *This time is different: Eight centuries of financial folly*. Princeton University Press.
- Reinhart, C. M., Rogoff, K. S., y Savastano, M. A. (2003). Debt intolerance. *Brookings Papers on Economic Activity*, 2003(1), 1-74.
- Renzhi, N., y Beirne, J. (2024). *Global shocks and monetary policy transmission in emerging markets* (ADB Economics Working Paper No. 726). Asian Development Bank.
- Uribe, M., y Yue, V. Z. (2006). Country spreads and emerging countries: Who drives whom? *Journal of International Economics*, 69(1), 6-36.
- Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública (2021). Boletín Oficial de la República Argentina, 3 de marzo de 2021.
- Fuente del dato de la colocación de diciembre de 2025: [VERIFICAR y citar fuente oficial, Secretaría de Finanzas o BCRA, no la nota periodística.]

---


## Nota 1: justificación académica del criterio de H1b

**Qué se mide.** La probabilidad de que la deuda no se estabilice: la proporción de trayectorias
simuladas en las que el resultado primario al final del horizonte es menor que el necesario para
estabilizar la deuda. No es un criterio propio: es la primera de las tres métricas del *fan chart*
del FMI (FMI, 2021, párr. 53), y la no estabilización de la deuda es uno de los tres conceptos
centrales que distingue el marco (FMI, 2021, Recuadro 2).

**Por qué el corte en 50%.** Tres razones, de más fuerte a más débil:

1. *Equivalencia exacta con la mediana.* Si X es la diferencia entre el resultado primario
   proyectado y el que estabiliza la deuda, P(X < 0) > 0,5 si y solo si la mediana de X es
   negativa. Afirmar "la probabilidad de no estabilización supera el 50%" es afirmar que la
   trayectoria central de la distribución simulada no estabiliza la deuda. Es la versión
   probabilística del chequeo determinista que el FMI aplica a su escenario base.
2. *Regla de decisión estándar.* Con costos simétricos de equivocarse en un sentido o en el
   otro, la regla que minimiza el error esperado asigna el caso al estado más probable, lo que
   equivale a un corte de 0,5 (clasificador de Bayes; Hastie, Tibshirani y Friedman, 2009,
   sección 2.4). [VERIFICAR la sección en el libro antes de citar.]
3. *El corte calibrado del FMI no es replicable.* Los cortes del índice compuesto del FMI
   (DFI menor a 1,13, riesgo bajo; mayor a 2,08, riesgo alto) se calibraron sobre un panel de
   crisis de muchos países, para que haya 10% de crisis no anticipadas y 10% de falsas
   alarmas (FMI y ESM, 2023, diapositiva 31). Requieren además un índice de calidad
   institucional y una normalización que no están publicados. Con un solo país no se puede
   calibrar un corte así.

**Cómo se blinda el resultado.** Se reporta la probabilidad completa, no solo si supera el
50%, junto con el ancho del *fan chart* (percentiles 5 a 95), que es la segunda métrica del FMI.
También se muestra a partir de qué corte cambiaría la conclusión. Así, el lector puede aplicar
otro criterio sin rehacer el análisis.

**Qué se cae.** El criterio "deuda mayor a 100% del PIB" que usa hoy el código no tiene
fuente. Sale de las hipótesis: o se le encuentra una justificación citada, o queda solo como
dato descriptivo.

## Nota 2: tamaño del shock de la FED (pendiente)

En la versión anterior puse "+100 puntos básicos" sin justificarlo: fue un error mío y lo saqué.
Hay dos criterios defendibles, a elegir cuando tengamos la serie:

- *Un desvío estándar* de la variación trimestral de la tasa sombra de la FED en la muestra
  1996-2025. Es la convención de la literatura de VAR: el shock tiene el tamaño típico
  observado en los datos.
- *Un episodio histórico real*, por ejemplo el ciclo de subas de 2022-2023, replicado como
  escenario. Tiene la ventaja de ser concreto y fácil de explicar.

Se puede usar el primero para las respuestas al impulso y el segundo para el Monte Carlo.

## Nota 3: el área de vacancia (ver `area_vacancia_v1.md`)

Santiago escribió que el marco del FMI "excluye los pasivos remunerados del Banco Central".
**No es correcto.** La revisión del marco (FMI, 2021, anexo II, párr. 5) establece que las
letras de liquidez del banco central se incluyen en la deuda pública cuando pueden financiar al
gobierno, cuando el gobierno responde de hecho por su servicio o cuando representan un riesgo
fiscal material. Además, cita expresamente a Argentina: esas letras sumaban 5% del PIB a fines
de 2018 (nota 8). La vacancia se reescribe en el archivo aparte.
