# Guía de defensa: qué hicimos, por qué y qué nos pueden discutir

Documento interno del grupo. No forma parte de la tesis. Resume cada paso del trabajo empírico con su justificación, lo que corrigió la revisión adversarial del 11/10/2026 y las críticas que todavía puede hacer un jurado, con la respuesta.

## Parte 1. Qué hicimos, paso a paso

### Paso 1. Pregunta e hipótesis

- **Origen.** La pregunta, los objetivos y las hipótesis salen de la Introducción corregida del 7/10/2026, con los comentarios de Pablo del 15/9 incorporados.
- **H1a**: los determinantes condicionan la sostenibilidad y el superávit, por sí solo, no basta para estabilizar la deuda.
- **H1b:** nuestra probabilidad de no estabilización es mayor que la del FMI en 2031 y en 2035.
- **H2:** un endurecimiento de la FED eleva la deuda y la probabilidad de no estabilización.
- **Cifras de comparación:** son las del análisis de sostenibilidad más reciente del FMI (2026, Artículo IV y segunda revisión): 1% a mediano plazo y menos de 3% en su abanico de diez años. El 1% es la estimación puntual del FMI para Argentina, no un umbral de riesgo bajo que defina el FMI. El umbral de 100% del PIB que había antes no tenía fuente y se sacó.

### Paso 2. Datos

Las series se construyen con scripts reproducibles. Hay dos excepciones a las fuentes primarias: el EMBI+ es un índice de J.P. Morgan que no se publica en forma libre y se toma de compilaciones secundarias, y su tramo 1996-1998 se empalma con *spreads* de bonos Brady cargados a mano.

| Serie | Fuente | Construcción | Por qué así |
|---|---|---|---|
| Deuda consolidada neta | MECON y BCRA | Deuda bruta del Tesoro + pasivos remunerados del BCRA − deuda del Tesoro en poder del BCRA (Letras a valor nominal) − depósitos del Tesoro | Es la consolidación del FMI (2021, anexo II) |
| Denominador | INDEC | PIB nominal de los últimos cuatro trimestres | No mezcla un stock con un flujo trimestral |
| Resultado primario | MECON, esquema ahorro-inversión-financiamiento | Flujo trimestral anualizado | La suma móvil crea autocorrelación artificial |
| PIB real | INDEC | Base 1993 empalmada a base 2004 (k = 1,751) | La base 2004 empieza en 2004 |
| EMBI+ | J.P. Morgan; *stripped spread* Brady antes de 1999 | Promedio trimestral | El EMBI+ empieza en 1999 |
| TCRM | BCRA | Promedio trimestral | Es el índice que usa el FMI |
| Tasa de la FED | FRED y tasa sombra de Wu y Xia (2016) | Sombra en el límite cero | En el límite cero la tasa efectiva no refleja la política |

**Controles contra el FMI.** La deuda neta da 119,0%, 61,1% y 61,0% del PIB en 2023, 2024 y 2025, contra 111,1%, 53,6% y 52,1% del FMI (2026). La diferencia (de 7,5 a 8,9 puntos) es compatible con las tenencias del FGS, que el FMI descuenta y nosotros no. Las LEFI de 2024-2025 están incluidas en la deuda del Tesoro (informe del MECON al 31/12/2024, hoja A.1.7).

### Paso 3. El modelo: un SVARX

- **Variables:** cuatro endógenas (resultado primario, crecimiento, EMBI+, TCRM); exógenas: variación de la tasa de la FED con dos rezagos, VIX, binarias estacionales y binarias de los quiebres de Bai y Perron (2001T4, 2006T2, 2018T1). La deuda rezagada entra en todas las ecuaciones.
- **Por qué un VAR:** las cuatro variables se determinan juntas; es la arquitectura del abanico estocástico del FMI (Celasun et al., 2006).
- **Por qué la FED es exógena:** Argentina es una economía pequeña y abierta (Cushman y Zha, 1997; Canova, 2005).
- **Por qué en niveles:** las estimaciones son consistentes sin imponer cointegración (Sims et al., 1990); la inferencia se hace con *bootstrap* porque la distribución de algunos estimadores no es la estándar.
- **Propiedades de las series** (lo pedía la propuesta metodológica): ADF, KPSS, Zivot-Andrews, Bai-Perron y Johansen, en el Apéndice A.1.
- **Rezagos:** el mayor orden estable que no supera al del AIC: tres (el AIC llega a su mínimo en seis, pero desde cuatro el VAR es inestable). Ivanov y Kilian (2005) recomiendan el AIC para respuestas al impulso con datos trimestrales. Entre los órdenes estables, el AIC elige dos; con dos rezagos la no estabilización es de 27,4% en 2031 y 27,9% en 2035, y está informada en la Tabla 6.6.
- **Muestra:** 1998T2-2025T4 (111 trimestres) para todas las especificaciones.

### Paso 4. Identificación de los *shocks*

- **Fiscal:** se descuenta la respuesta automática al ciclo con una elasticidad de 0,25 (Blanchard y Perotti, 2002; Girouard y André, 2005).
- **Actividad:** puede responder al *shock* fiscal en el trimestre.
- **Bloque cambiario y de riesgo:** el EMBI+ y el TCRM sin orden entre sí; solo se interpreta el efecto conjunto (Christiano et al., 1999). El resultado primario y el crecimiento no responden en el trimestre a ese bloque.
- **Robusteces:** Cholesky con el resultado primario primero y último, y elasticidades de 0 y 0,5.
- **Dato clave:** la identificación no cambia la probabilidad de no estabilización (H1b), porque los *shocks* reconstruyen los mismos residuos. Sirve para separar la varianza por bloque y definir el *shock* fiscal. Las diferencias de 0,5 a 0,8 puntos entre las filas de identificación de la Tabla 6.6 vienen de las extracciones de Monte Carlo.

### Paso 5. Retroalimentación entre la deuda y las variables

Es la "arquitectura B" de la propuesta metodológica: la deuda rezagada entra en las cuatro ecuaciones y, en la simulación, vuelve como desvío acumulado respecto de la senda base. La deuda se asocia con más superávit (coeficiente de impacto de 0,051 sobre el resultado primario trimestral; multiplicador de largo plazo de alrededor de 0,19 por MCO, sin intervalo) y más crecimiento; con el EMBI+ la estimación es de 22 puntos básicos por punto de deuda, pero el intervalo incluye el cero. Sin retroalimentación (arquitectura A), las probabilidades casi no cambian.

### Paso 6. Inferencia

*Bootstrap* salvaje de diseño recursivo (Gonçalves y Kilian, 2004). En cada réplica se regenera también la deuda, con un VAR auxiliar que la incluye. Los coeficientes de rezago se corrigen por el sesgo de muestra pequeña (Kilian, 1998). El autovalor máximo es 0,964 por MCO y 0,9998 en la estimación central corregida (corrección multiplicada por δ = 0,9). Las réplicas usan un δ menor, de modo que los intervalos percentiles no quedan centrados y la estimación central queda cerca del límite superior. Semilla fija.

### Paso 7. Simulación

1. **Escenario base del FMI (2026, cuadro 6):** crecimiento, deflactor, tasa efectiva, resultado primario, ajuste stock-flujo e inflación relativa. Se verifica que la identidad reproduzca la senda de deuda del FMI (desvío máximo de 0,1 puntos).
2. **Desvíos:** el SVARX se simula trimestre a trimestre con *shocks* históricos remuestreados.
3. **Identidad:** separa moneda local (42%) y extranjera (58%); la tasa en dólares se reprecia 28% por año.
4. **Métrica del FMI:** la deuda no se estabiliza en T si el superávit del escenario base es menor que el que la estabilizaría. Se mide en 2031 y 2035.
5. **Estimación central:** parámetros corregidos y 20.000 trayectorias (error de Monte Carlo de 0,3 puntos). **Intervalos:** 200 réplicas con 1.000 trayectorias.
6. **Escenarios de la FED:** la tasa entra como variación trimestral, así que el desvío de nivel es la suma acumulada y persiste. Un desvío estándar es un nivel 0,50 puntos más alto de 2026 a 2035. La senda 2022-2025 sube el nivel 5,25 puntos, lo baja 1,43 en 2026-2029 y lo deja 3,82 puntos por encima del base hasta 2035.

### Paso 8. Contrastes

| Hipótesis | Medida | Criterio |
|---|---|---|
| H1a | Superávit necesario en 2031, desplazando el resultado primario de todos los años, para llevar la probabilidad de 2031 al 1% que estima el FMI; descomposición de la varianza como complemento (era el criterio original) | No basta si el necesario supera el máximo histórico del SPN (3,6% en 2004) |
| H1b | Probabilidad de no estabilización en 2031 y 2035 | Límite inferior de 90% mayor que 1% y 3%; se informa también Bonferroni |
| H2 | Diferencia de probabilidad y de deuda con la FED | Intervalo de 90% que excluye el cero |

### Paso 9. Resultados

- **H1b, respaldada.** No estabilización de 25,2% en 2031 [19,0; 27,7] y 22,3% en 2035 [15,6; 24,9]. Se cumple en las 17 especificaciones alternativas y con *shocks* a la manera del FMI (23,7%), pero ese procedimiento no reproduce el 1% del FMI, así que la comparabilidad no está establecida.
- **H1a, respaldada por suficiencia.** Hace falta subir el resultado primario de todos los años unos 4,75 puntos: 6,15% del PIB en 2026 y 7,05% en 2031, casi el doble del máximo histórico (3,6%). Con el criterio original, la descomposición de la varianza (cambiario y de riesgo 59%, fiscal 32%), no se cumple.
- **H2, respaldada solo en parte.** La senda de 2022-2025 suma 13 puntos de probabilidad en 2035 [1,0; 24,8] y el nivel 0,50 puntos más alto suma 1,5 [0,1; 3,1]. El efecto sobre la deuda esperada no excluye el cero, no se sostiene con Bonferroni y solo 5 de 84 bandas de respuesta excluyen el cero (el azar daría unas ocho). El 60% del efecto es el costo directo de la deuda en dólares, que entra en la identidad por construcción.

## Parte 2. Qué encontró la revisión adversarial y cómo se corrigió

| Problema encontrado | Corrección |
|---|---|
| La identidad omitía la inflación relativa del escenario del FMI, que es la valuación de la deuda en dólares. Con eso, la senda base caía el doble que la del FMI | Se incorporó, y ahora un control exige reproducir la senda del FMI antes de simular |
| La retroalimentación usaba la sorpresa del año en lugar del desvío acumulado de la deuda | Corregido: desvío respecto de la senda base |
| Se informaban medias del *bootstrap* en lugar de la estimación puntual, y el *bootstrap* subestimaba la persistencia | Estimación central con corrección de sesgo de Kilian (1998) y 20.000 trayectorias |
| El *bootstrap* no regeneraba la deuda | VAR auxiliar con la deuda como quinta variable |
| El horizonte de mediano plazo del FMI es 2031, no 2030 | Se mide en 2031 |
| El escenario de la FED dejaba la tasa 5,25 puntos más alta durante diez años | Ahora repite las variaciones de 2022-2025: el nivel sube 5,25 puntos, baja 1,43 y queda 3,82 puntos por encima del base hasta 2035 |
| El criterio de H1a (varianza) no medía si el superávit "alcanza", y además no se cumplía | Contraste de suficiencia como criterio principal, adoptado después de la primera estimación y declarado en 4.7 |
| Afirmaciones de robustez que no se cumplían (H1a con deuda bruta, H1b con el escenario de 2025) | Corregidas; la tesis informa dónde se sostiene cada resultado y dónde no |
| Errores de texto: un error algebraico en 3.2, atribuciones equivocadas (Eichengreen, Everaert), un marcador sin borrar, rutas de código en el texto, nombre de un autor en una tabla, referencias sin citar y citas sin referencia | Corregidos |

## Parte 3. Críticas que puede hacer el jurado y respuesta honesta

1. **"Cambiaron los criterios después de ver los resultados."** Es cierto. En octubre de 2026, después de la primera estimación, el criterio de H1a pasó de la descomposición de la varianza, que no se cumple ([-4,8; 91,2] incluye el cero), al de suficiencia; los tamaños de los *shocks* de la FED también se fijaron entonces. La tesis lo declara en la sección 4.7 e informa los dos criterios.
2. **"H1b compara cosas que no son comparables."** La comparabilidad con el FMI no está establecida. Con *shocks* a la manera del FMI nuestros datos dan 23,7% en 2031 y un abanico de 114 puntos, contra 1% y 71,5 del FMI, así que no reproducimos su número ni con su procedimiento. Los perímetros también difieren: 61,0% del PIB de deuda consolidada neta contra 80,3% de deuda federal bruta. No sabemos de dónde viene la diferencia.
3. **"La estimación central es casi una raíz unitaria."** Es cierto: el autovalor máximo pasa de 0,964 por MCO a 0,9998 con la corrección de sesgo. Eso vuelve muy persistentes los *shocks* y eleva las probabilidades. Las réplicas usan una corrección menor, así que los intervalos no quedan centrados y la estimación central está cerca del límite superior. Está declarado en 4.5 y 6.1.
4. **"La regla de rezagos es ad hoc."** La regla elige el mayor orden estable que no supera al del AIC (tres). Entre los órdenes estables, el AIC elige dos. Con dos rezagos las probabilidades son algo mayores (27,4% y 27,9%) y están informadas.
5. **"Hay autocorrelación residual y remuestrean como si no la hubiera."** Es cierto (Portmanteau, p = 0,036). Los *shocks* se remuestrean como independientes entre trimestres; está declarado como limitación y no se corrigió.
6. **"El resultado primario incluye las utilidades del BCRA."** Es cierto; la fuente no permite separarlas. Sin rentas de la propiedad, la probabilidad es de 23,4% en 2031 y 19,6% en 2035, y el máximo histórico del superávit baja a 3,29%.
7. **"El escenario del FMI es para la deuda federal bruta y ustedes lo aplican a la consolidada neta."** Es cierto, y no tiene una solución completa. Con el ajuste stock-flujo en cero la probabilidad es de 22,0% en 2031, y partiendo de la deuda del FMI (52,1%), de 22,8%.
8. **"No restaron el FGS aunque hay datos de tenencias desde 2004."** Es cierto. Hay datos anuales de la deuda en manos de organismos del sector público desde 2004, que no se usaron porque no cubren 1996-2003 ni separan al FGS. Es una decisión discutible; la única sensibilidad hecha es partir de la deuda del FMI, que sí lo descuenta.
9. **"El EMBI+ de 1996-1998 no es el EMBI+."** Es cierto: son *spreads* de bonos Brady cargados a mano y empalmados en 1999 con una corrección proporcional. Son 12 de los 120 trimestres. No hay una robustez específica que los excluya.
10. **"La identificación no aporta nada a la probabilidad."** Es cierto: la probabilidad de no estabilización no depende de la identificación. La identificación sirve para separar la varianza por bloque y definir el *shock* fiscal, y esa descomposición no es robusta.
11. **"H2 es débil."** Es cierto y así se dice: el efecto sobre la probabilidad cumple el criterio al 90%, el efecto sobre la deuda esperada no, nada resiste Bonferroni, y la mayor parte del efecto es el costo directo de la deuda en dólares, que el modelo incorpora por construcción.
12. **"La elasticidad de 0,25 es de la OCDE."** Solo afecta la descomposición de la varianza, no la probabilidad ni la suficiencia.
13. **Endogeneidad del riesgo país** (no está en el texto por decisión de Pablo): en series de tiempo todo es endógeno salvo los *shocks* de mayor frecuencia que el sistema; por eso el VIX y la tasa de la FED entran como exógenas.

## Parte 4. Pendientes

- **FGS.** Hay que bajar a mano los informes de ANSES; la sensibilidad partiendo de la deuda del FMI ya está hecha.
- **Citas.** Braun y Joy (1968), sin acceso al original; Adler et al. (2016), verificada sobre el documento de trabajo.
- **Revisión.** Que el grupo y Pablo lean el texto completo.

## Parte 5. Números para tener a mano

| Número | Qué es |
|---|---|
| 61,0% del PIB | Deuda consolidada neta a diciembre de 2025 |
| 0,051 [0,010; 0,103] | Reacción fiscal: coeficiente de impacto (largo plazo por MCO, alrededor de 0,19) |
| 25,2% [19,0; 27,7] | No estabilización en 2031 (FMI: 1%) |
| 22,3% [15,6; 24,9] | No estabilización en 2035 (FMI: menos de 3%) |
| 7,05% del PIB | Superávit necesario en 2031 para llegar al 1% del FMI, con 6,15% en 2026 (máximo histórico: 3,6%) |
| 59% / 32% / 9% | Varianza de la deuda en 2035: cambiario y de riesgo / fiscal / actividad (no robusto) |
| +13 pp [1; 25] | Efecto de la senda de la FED 2022-2025 (nivel 3,82 pp más alto desde 2029) sobre la probabilidad en 2035 |
| 0,964 / 0,9998 | Autovalor máximo: MCO / estimación central corregida |
| 17 | Especificaciones alternativas de la Tabla 6.6 (más dos a la manera del FMI y la referencia del FMI) |
| 35,3 contra 71,5 | Ancho del abanico en 2031: nuestro contra el del FMI |
| 3 rezagos, 111 trimestres | Especificación del VAR |
