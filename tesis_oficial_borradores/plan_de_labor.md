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

**1.4. Denominación del proyecto:** La solvencia intertemporal de la deuda consolidada argentina post-2025: proyecciones a partir de sus determinantes macroeconómicos (1996-2025).

**1.5. Palabras clave:** deuda pública consolidada; sostenibilidad de la deuda; vectores autorregresivos estructurales; simulación de Monte Carlo; política monetaria de Estados Unidos.

**1.6. Resumen técnico.** Argentina registró un superávit primario en 2024 y 2025 y volvió a colocar deuda en dólares en diciembre de 2025, después de dos décadas marcadas por el *default*[^en-default] de 2001 y la reestructuración de 2020. Este proyecto se pregunta si ese superávit alcanza para que la deuda pública se estabilice o si el crecimiento, el tipo de cambio real y el riesgo país la condicionan más que el esfuerzo fiscal. La deuda se mide en forma consolidada: la del Tesoro nacional más los pasivos remunerados del Banco Central de la República Argentina (BCRA). Se estimará un modelo de vectores autorregresivos estructural con variables exógenas (SVARX) con datos trimestrales de 1996 a 2025. Sus variables serán el crecimiento, el resultado primario, el riesgo país y el tipo de cambio real; la tasa de la Reserva Federal de los Estados Unidos (FED) y la volatilidad financiera global entrarán como exógenas. Los *shocks*[^en-shock] identificados del modelo alimentarán una simulación de Monte Carlo de la deuda entre 2026 y 2035 sobre el escenario base del Fondo Monetario Internacional (FMI). El resultado será la probabilidad de que la deuda no se estabilice, medida con el mismo criterio que usa el FMI, y el cambio de esa probabilidad ante un endurecimiento de la política monetaria de la FED. El estudio es cuantitativo, explicativo y longitudinal, y trabaja solo con datos secundarios de fuentes oficiales. Se espera aportar una medida del riesgo de la deuda que identifique de dónde viene la incertidumbre y que pueda compararse directamente con la del FMI.

# 2. Descripción del proyecto

## 2.1. Tema

La sostenibilidad de la deuda pública consolidada argentina (Tesoro nacional y BCRA) y sus determinantes macroeconómicos, 1996-2035.

## 2.2. Estado actual del conocimiento

La literatura sobre la deuda argentina puede ordenarse en ocho ejes, que el capítulo de Antecedentes de la tesis desarrolla. Los que delimitan el problema son cuatro.

El primero discute las limitaciones de los enfoques contables. Rodríguez (2023) muestra que la ratio deuda/PIB no alcanza para evaluar la solvencia si no se consideran las tasas de interés y el ciclo económico. Sanches (2019) descompone la dinámica de la ratio en sus componentes. Ninguno de estos trabajos estima cómo se transmiten los *shocks* entre el resultado fiscal, el riesgo país, el tipo de cambio y la actividad.

El segundo eje estudia los límites del ajuste. Ghosh et al. (2013) encuentran que el superávit primario responde cada vez menos a la deuda cuando esta es alta, lo que llaman fatiga fiscal. Ando et al. (2025) muestran que los ajustes fiscales discrecionales reducen poco la ratio de deuda y solo lo hacen de forma duradera en fases de expansión.

El tercer eje es la simulación estocástica de la deuda. Celasun et al. (2006) proponen en el FMI combinar un VAR sobre los determinantes de la deuda con una función de reacción fiscal y la identidad de acumulación, para obtener distribuciones de trayectorias en lugar de un único escenario. Medeiros (2012) aplica la misma arquitectura en la Comisión Europea, y el FMI la incorporó a su Marco de Riesgo Soberano y Sostenibilidad de la Deuda (FMI, 2021), con el que evalúa a la Argentina en las revisiones del programa (FMI, 2025, 2026). Ese marco genera los *shocks* a partir de la historia de los determinantes, sin identificar su origen.

El cuarto eje trata la exposición externa. Calvo et al. (2003) explican cómo una interrupción repentina de capitales encarece la deuda en dólares a través de la depreciación real. Uribe y Yue (2006) estiman que las tasas internacionales elevan las primas de riesgo de los países emergentes, y Levy Yeyati y Sturzenegger (2023) estudian el efecto de valuación del tipo de cambio sobre el patrimonio neto del sector público argentino.

**Área de vacancia.** La revisión deja tres aspectos sin cubrir de manera conjunta para el caso argentino. No hay una estimación con *shocks* identificados: los trabajos que los identifican lo hacen sobre paneles de países, y los que estudian la deuda argentina no los identifican. El efecto de la política monetaria de Estados Unidos no se tradujo en un cambio en la probabilidad de que la deuda argentina no se estabilice. Y aunque el FMI (2021) admite incluir los pasivos del banco central en la deuda pública, en su análisis de la Argentina usa la deuda bruta del gobierno federal; la deuda consolidada con el BCRA aparece solo como un cuadro de stocks[^en-stock] (FMI, 2025, anexo II). Ningún trabajo estima cómo evolucionó esa deuda consolidada junto con sus determinantes.

## 2.3. Planteamiento del problema

**Contextualización.** La historia argentina muestra un ciclo repetido de endeudamiento externo, interrupción de los flujos de capital y cesación de pagos (Reinhart y Rogoff, 2009; Rapoport, 2020). La administración que asumió en diciembre de 2023 recibió un stock elevado de pasivos y un acceso muy limitado al crédito voluntario. El Tesoro volvió a colocar un bono en dólares en diciembre de 2025, bajo ley local y a una tasa de 9,26% anual (Secretaría de Finanzas, 2025). A fines de julio de 2026, la deuda en moneda extranjera de la Administración Central sumaba USD 248.458 millones (Oficina de Presupuesto del Congreso [OPC], 2026). Entre 2002 y 2024, además, el BCRA absorbió liquidez con pasivos remunerados que llegaron a 18,4% del PIB en 2023 (FMI, 2025, anexo II), de modo que una parte del endeudamiento público no aparece en la deuda del Tesoro.

**Problema.** Resta determinar si el superávit primario alcanza para estabilizar la deuda en el mediano plazo o si los determinantes estructurales de la economía argentina la condicionan más que el resultado fiscal.

**Preguntas de investigación.**

- Pregunta general: ¿en qué medida el crecimiento, el tipo de cambio real, el riesgo país y el resultado primario de Argentina (1996-2025) condicionan la sostenibilidad de la deuda consolidada en 2026-2035, y cuál es la probabilidad de que la deuda no se estabilice bajo el escenario base?
- Pregunta específica: ¿cómo y en qué magnitud impactaría un endurecimiento de la política monetaria de la FED sobre la dinámica de la deuda consolidada y sobre su probabilidad de no estabilizarse en 2026-2035?

**Objetivo general.** Evaluar la dinámica de la deuda pública consolidada argentina a partir de sus determinantes macroeconómicos históricos (1996-2025), para proyectar su sostenibilidad en 2026-2035 y estimar la probabilidad de que no se estabilice.

**Objetivos específicos.**

1. Construir una serie trimestral de deuda pública consolidada (Tesoro nacional y pasivos remunerados del BCRA) para 1996-2025.
2. Analizar las propiedades estadísticas de las series: raíz unitaria, quiebres estructurales y cointegración.
3. Estimar un SVARX en el que el crecimiento, el resultado primario, el riesgo país y el tipo de cambio real interactúan con la deuda rezagada, con la tasa de la FED y la volatilidad global como variables exógenas.
4. Medir la reacción del resultado primario ante el nivel de deuda y la contribución de los *shocks* fiscal, de actividad y cambiario y de riesgo a la variabilidad de la deuda.
5. Simular la distribución de trayectorias de la deuda en 2026-2035 bajo el escenario base del FMI y calcular la probabilidad de que no se estabilice.
6. Estimar el efecto de un endurecimiento de la política monetaria de la FED sobre esa distribución.

**Justificación.** La Ley 27.612 (2021) exige una ley especial para emitir deuda en moneda extranjera bajo legislación extranjera por encima del máximo del presupuesto y una ley que apruebe cada programa con el FMI. Esas decisiones requieren evaluaciones de sostenibilidad, y la evaluación probabilística de referencia es la del FMI. El proyecto aporta una segunda medida, comparable con la del FMI porque usa su escenario y su métrica, pero con *shocks* identificados y sobre el perímetro consolidado. En lo metodológico, deja un procedimiento replicable que puede actualizarse con cada nuevo informe del FMI.

**Viabilidad.** El proyecto no requiere trabajo de campo ni financiamiento. Todos los datos son públicos y gratuitos: Ministerio de Economía (MECON), BCRA, Instituto Nacional de Estadística y Censos (INDEC), FMI, Reserva Federal y la Bolsa de Opciones de Chicago (CBOE). La estimación y la simulación se programan en Python con bibliotecas de uso libre. El único dato de acceso incierto son las tenencias de títulos públicos del Fondo de Garantía de Sustentabilidad (FGS) de la ANSES; si no se consiguen completas, se informa una variante que parte de la deuda consolidada neta del FMI, que ya las descuenta.

## 2.4. Marco teórico

El marco va de la teoría general a la teoría sustantiva en cuatro niveles.

**Restricción externa.** El punto de partida es el enfoque de la restricción externa: en una economía que necesita divisas para crecer y para pagar su deuda, el endeudamiento en moneda extranjera la expone a la disponibilidad de dólares (Díaz Alejandro, 1970; Calvo et al., 2003). Ese enfoque explica por qué en Argentina el tipo de cambio real y el riesgo país pesan sobre la deuda tanto como el resultado fiscal.

**Solvencia y sostenibilidad.** El gobierno es solvente si el valor presente de sus superávits primarios futuros cubre la deuda actual. Bohn (1998) muestra que una condición suficiente es que el superávit primario responda positivamente al nivel de deuda. Esa respuesta, sin embargo, no garantiza que la deuda se estabilice en un nivel determinado: si la diferencia entre la tasa de interés y el crecimiento es alta, el superávit necesario puede superar lo que la economía genera. El FMI (2021) define la deuda como sostenible cuando el gobierno puede cumplir sus obligaciones sin un ajuste poco realista, y evalúa la estabilización con la identidad de acumulación de la deuda.

**Identidad de la deuda con composición por monedas.** La ratio deuda/PIB cambia por el diferencial entre la tasa de interés y el crecimiento, por el resultado primario y, cuando parte de la deuda está en moneda extranjera, por la depreciación real. Esta identidad conecta las variables del modelo con la deuda y separa el efecto del esfuerzo fiscal del efecto de valuación.

**Deuda consolidada.** Cuando el banco central financia al Tesoro o absorbe la liquidez con pasivos remunerados, la restricción presupuestaria relevante es la del sector público consolidado. El FMI (2021) incluye esos pasivos en la deuda pública cuando pueden financiar al gobierno o representan un riesgo fiscal material.

**Transmisión de la política monetaria de Estados Unidos.** Una suba de la tasa de la FED eleva la prima de riesgo de los emergentes (Uribe y Yue, 2006), deprecia su tipo de cambio real y reduce su crecimiento (Neumeyer y Perri, 2005). Cada canal entra en la identidad de la deuda por un término distinto.

**Sostenibilidad en sentido probabilístico.** Como los determinantes son inciertos, la sostenibilidad se expresa como la probabilidad de que la deuda no se estabilice, construida con simulaciones (Celasun et al., 2006; FMI, 2021). La fatiga fiscal (Ghosh et al., 2013) completa el marco: fija un límite a cuánto superávit puede exigirse de manera realista.

## 2.5. Hipótesis

**H1a.** El crecimiento, el tipo de cambio real, el riesgo país y el resultado primario condicionan la sostenibilidad de la deuda consolidada, de modo que el superávit primario, por sí solo, no basta para estabilizarla en 2026-2035. Unidad: la economía argentina. Variables: superávit primario necesario y probabilidad de no estabilización. Relación: el superávit que reduciría esa probabilidad al nivel del FMI supera el máximo alcanzado en 1996-2025.

**H1b.** La probabilidad de que la deuda consolidada no se estabilice es mayor que la que informa el FMI para la deuda federal bruta: alrededor de 1% a mediano plazo (2031) y menos de 3% a diez años (2035) (FMI, 2026).

**H2.** Un endurecimiento de la política monetaria de la FED eleva la trayectoria esperada de la deuda consolidada y su probabilidad de no estabilizarse, a través del riesgo país, el tipo de cambio real y el crecimiento.

## 2.6. Estrategia metodológica

**Tipo de estudio.** Cuantitativo, explicativo y longitudinal. Es explicativo porque busca medir cómo los determinantes macroeconómicos afectan la deuda. Es retrospectivo en la estimación (1996-2025) y prospectivo en la simulación (2026-2035).

**Unidad de análisis, población y muestra.** La unidad de análisis es el trimestre de la economía argentina. La población son todos los trimestres con datos de deuda pública. La muestra es no probabilística e intencional: 1996-2025, porque desde 1996 existen series trimestrales homogéneas de todas las variables y porque el período incluye regímenes cambiarios y fiscales distintos (convertibilidad, *default*, desendeudamiento, reendeudamiento y programa con el FMI). La muestra efectiva de estimación es 1998T2-2025T4 (111 trimestres), porque los primeros trimestres se reservan para los rezagos.

**Técnicas de obtención y evaluación de datos secundarios.** Todos los datos son secundarios. La evaluación de cada serie revisará cuatro aspectos: la institución que la produce, la definición y cobertura, los cambios metodológicos (por ejemplo, el cambio de base del PIB en 2004) y la coherencia con otra fuente. La serie de deuda consolidada se construirá sumando la deuda bruta de la Administración Central y los pasivos remunerados del BCRA, y restando la deuda del Tesoro en poder del BCRA y los depósitos del Tesoro en el banco central. Se contrastará con el cuadro de deuda consolidada del FMI (2025, anexo II) en los años en que ambos se superponen.

**Variables, dimensiones e indicadores.**

**Tabla 1. Variables, indicadores y fuentes**

| Variable | Dimensión | Indicador | Fuente | Rol |
|---|---|---|---|---|
| Sostenibilidad de la deuda | Estabilización | Probabilidad de que la deuda no se estabilice en 2031 y 2035 | Elaboración propia con el criterio del FMI (2021) | Dependiente |
| Deuda pública consolidada | Solvencia | Deuda del Tesoro y del BCRA neta de tenencias cruzadas, % del PIB | MECON y BCRA | Entra rezagada y se acumula con la identidad |
| Política fiscal | Esfuerzo fiscal | Resultado primario del Sector Público Nacional, % del PIB | MECON | Endógena |
| Actividad | Crecimiento | Variación trimestral del PIB real | INDEC | Endógena |
| Riesgo soberano | Costo del financiamiento | EMBI+ Argentina (puntos básicos) | J.P. Morgan | Endógena |
| Precios relativos | Efecto de valuación | Tipo de cambio real multilateral | BCRA | Endógena |
| Política monetaria de Estados Unidos | *Shock* externo | Tasa de fondos federales; tasa sombra en el límite cero (Wu y Xia, 2016) | Reserva Federal | Exógena |
| Condiciones financieras globales | Aversión al riesgo | VIX | CBOE | Exógena |
| Escenario base | Proyección oficial | Crecimiento, deflactor, tasa efectiva, resultado primario y ajuste stock-flujo, 2026-2035 | FMI (2026), cuadro 6 | Supuesto de la simulación |

Fuente: elaboración propia.

**Procedimiento y pruebas.** El trabajo empírico seguirá seis pasos.

1. *Propiedades de las series.* Pruebas de raíz unitaria de Dickey y Fuller aumentada (ADF) y de Kwiatkowski, Phillips, Schmidt y Shin (KPSS); prueba de Zivot y Andrews, que admite un quiebre; quiebres múltiples de Bai y Perron (2003) sobre la serie de deuda, que entrarán como variables binarias; prueba de cointegración de Johansen.
2. *Especificación.* Selección de rezagos con los criterios de Akaike, Hannan-Quinn y Schwarz, sujeta a que el modelo sea estable (todos los autovalores de la matriz compañera con módulo menor que uno). Diagnóstico de residuos: autocorrelación (Portmanteau), normalidad (Jarque-Bera) y heterocedasticidad.
3. *Identificación.* Restricciones de impacto según Blanchard y Perotti (2002): el resultado primario no responde dentro del trimestre a los *shocks* cambiarios y de riesgo, y su respuesta automática al ciclo se fija con una elasticidad de 0,25. Como robustez, dos ordenamientos de Cholesky.
4. *Inferencia.* Intervalos de confianza por *bootstrap*[^en-bootstrap] salvaje (Gonçalves y Kilian, 2004), válidos con heterocedasticidad, y corrección del sesgo de muestra chica de Kilian (1998).
5. *Simulación.* Monte Carlo de 2026 a 2035 sobre el escenario base del FMI (2026), con los *shocks* estructurales remuestreados de la historia. Antes de simular se verificará que la identidad reproduzca la senda de deuda del FMI.
6. *Contraste de hipótesis y robustez.* H1a: superávit primario necesario para que la probabilidad baje al 1% del FMI, comparado con el máximo histórico; como complemento, la descomposición de la varianza de la deuda por bloque de *shocks*. H1b: el límite inferior del intervalo de 90% debe superar la probabilidad del FMI. H2: el intervalo de 90% de la diferencia entre el escenario de la FED y el base debe excluir el cero. Robustez: otras series de deuda, otra identificación, otros rezagos, otra muestra y el procedimiento de *shocks* del propio FMI.

# 3. Transferencia y beneficiarios

**Organismos públicos.** El Congreso de la Nación, que por la Ley 27.612 aprueba el endeudamiento en moneda extranjera bajo ley extranjera y los programas con el FMI, y su Oficina de Presupuesto, que analiza la deuda pública. El Ministerio de Economía y el BCRA, como usuarios de una evaluación de la deuda consolidada distinta de la del FMI.

**Ámbito académico.** Estudiantes y cátedras de Macroeconomía, Finanzas Públicas y Econometría de la FCE, que dispondrán de una aplicación completa de un SVARX a la deuda argentina, con datos y código reproducibles.

**Analistas y sociedad.** Analistas de riesgo soberano y periodistas económicos, que podrán contrastar la probabilidad de no estabilización con la del FMI y saber qué *shocks* la explican.

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
| Construcción de la deuda consolidada y evaluación de las fuentes | | | X | X | X | | | | | | | |
| Pruebas de raíz unitaria, quiebres y cointegración | | | | | X | | | | | | | |
| Especificación, identificación y estimación del SVARX | | | | | X | X | | | | | | |
| Escenario base del FMI y simulación de Monte Carlo | | | | | | X | X | | | | | |
| Contraste de hipótesis y pruebas de robustez | | | | | | | X | X | | | | |
| Redacción de resultados, discusión y conclusiones | | | | | | | | X | X | | | |
| Revisión del director y correcciones | | | | | | | | | X | X | X | |
| Entrega y preparación de la defensa | | | | | | | | | | | X | X |

Fuente: elaboración propia.

# 5. Referencias bibliográficas

Ando, S., Mishra, P., Patel, N., Peralta-Alva, A., y Presbitero, A. F. (2025). Fiscal consolidation and public debt. *Journal of Economic Dynamics and Control*, *170*, artículo 104998. https://doi.org/10.1016/j.jedc.2024.104998

Bai, J., y Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics*, *18*(1), 1-22. https://doi.org/10.1002/jae.659

Blanchard, O., y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. *Quarterly Journal of Economics*, *117*(4), 1329-1368. https://doi.org/10.1162/003355302320935043

Bohn, H. (1998). The behavior of U.S. public debt and deficits. *Quarterly Journal of Economics*, *113*(3), 949-963. https://doi.org/10.1162/003355398555793

Calvo, G. A., Izquierdo, A., y Talvi, E. (2003). *Sudden stops, the real exchange rate, and fiscal sustainability: Argentina's lessons* (NBER Working Paper No. 9828). National Bureau of Economic Research. https://doi.org/10.3386/w9828

Celasun, O., Debrun, X., y Ostry, J. D. (2006). *Primary surplus behavior and risks to fiscal sustainability in emerging market countries: A "fan-chart" approach* (IMF Working Paper No. 06/67). Fondo Monetario Internacional. https://doi.org/10.5089/9781451863277.001

Díaz Alejandro, C. F. (1970). *Essays on the economic history of the Argentine Republic*. Yale University Press.

Fondo Monetario Internacional. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper). Aprobado por el Directorio el 14 de enero de 2021.

Fondo Monetario Internacional. (2025). *Argentina: Request for an extended arrangement under the Extended Fund Facility* (IMF Country Report No. 25/95). Anexo II: Application of the Sovereign Risk and Debt Sustainability Framework.

Fondo Monetario Internacional. (2026). *Argentina: 2026 Article IV consultation, second review under the extended arrangement under the Extended Fund Facility* (IMF Country Report No. 26/105). Anexo: Sovereign Risk and Debt Sustainability Assessment.

Ghosh, A. R., Kim, J. I., Mendoza, E. G., Ostry, J. D., y Qureshi, M. S. (2013). Fiscal fatigue, fiscal space and debt sustainability in advanced economies. *The Economic Journal*, *123*(566), F4-F30. https://doi.org/10.1111/ecoj.12010

Gonçalves, S., y Kilian, L. (2004). Bootstrapping autoregressions with conditional heteroskedasticity of unknown form. *Journal of Econometrics*, *123*(1), 89-120. https://doi.org/10.1016/j.jeconom.2003.10.030

Kilian, L. (1998). Small-sample confidence intervals for impulse response functions. *Review of Economics and Statistics*, *80*(2), 218-230. https://doi.org/10.1162/003465398557465

Levy Yeyati, E., y Sturzenegger, F. (2023). A balance-sheet approach to fiscal sustainability. *Fiscal Studies*, *44*(1), 61-84. https://doi.org/10.1111/1475-5890.12319

Ley 27.612 de Fortalecimiento de la Sostenibilidad de la Deuda Pública. (2021, 3 de marzo). Boletín Oficial de la República Argentina. https://www.argentina.gob.ar/normativa/nacional/norma-347532/texto

Medeiros, J. (2012). *Stochastic debt simulation using VAR models and a panel fiscal reaction function: Results for a selected number of countries* (European Economy Economic Papers No. 459). Comisión Europea.

Neumeyer, P. A., y Perri, F. (2005). Business cycles in emerging economies: The role of interest rates. *Journal of Monetary Economics*, *52*(2), 345-380. https://doi.org/10.1016/j.jmoneco.2004.04.011

Oficina de Presupuesto del Congreso. (2026). *Operaciones de deuda pública, julio 2026*.

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
