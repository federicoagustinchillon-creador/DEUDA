# Guía de defensa: qué hicimos, por qué y qué nos pueden discutir

Documento interno del grupo. No forma parte de la tesis. Resume cada paso del trabajo empírico con su justificación, lo que corrigió la revisión adversarial del 11/10/2026 y las críticas que todavía puede hacer un jurado, con la respuesta.

## Parte 1. Qué hicimos, paso a paso

### Paso 1. Pregunta e hipótesis

- **Origen.** La pregunta, los objetivos y las hipótesis salen de la Introducción corregida de Santiago (7/10/2026), con los comentarios de Pablo del 15/9 incorporados.
- **H1a** (texto de Santiago): los determinantes condicionan la sostenibilidad y el superávit, por sí solo, no basta para estabilizar la deuda.
- **H1b:** nuestra probabilidad de no estabilización es mayor que la del FMI en 2031 y en 2035.
- **H2:** un endurecimiento de la FED eleva la deuda y la probabilidad de no estabilización.
- **Umbrales:** son los del análisis de sostenibilidad más reciente del FMI (2026, Artículo IV y segunda revisión): 1% a mediano plazo y menos de 3% en su abanico de diez años. El umbral de 100% del PIB que había antes no tenía fuente y se sacó.

### Paso 2. Datos

Todas las series salen de fuentes primarias con scripts reproducibles, sin intervención manual.

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
- **Propiedades de las series** (lo pedía la metodología de Santiago): ADF, KPSS, Zivot-Andrews, Bai-Perron y Johansen, en el Apéndice A.1.
- **Rezagos:** el mayor orden estable que no supera al del AIC: tres. Ivanov y Kilian (2005) recomiendan el AIC para respuestas al impulso con datos trimestrales. Con dos rezagos (el que elige el AIC entre los estables) los resultados se mantienen.
- **Muestra:** 1998T2-2025T4 (111 trimestres) para todas las especificaciones.

### Paso 4. Identificación de los *shocks*

- **Fiscal:** se descuenta la respuesta automática al ciclo con una elasticidad de 0,25 (Blanchard y Perotti, 2002; Girouard y André, 2005).
- **Actividad:** puede responder al *shock* fiscal en el trimestre.
- **Bloque cambiario y de riesgo:** el EMBI+ y el TCRM sin orden entre sí; solo se interpreta el efecto conjunto (Christiano et al., 1999). El resultado primario y el crecimiento no responden en el trimestre a ese bloque.
- **Robusteces:** Cholesky con el resultado primario primero y último, y elasticidades de 0 y 0,5.
- **Dato clave:** la identificación no cambia la probabilidad de no estabilización (H1b), porque los *shocks* reconstruyen los mismos residuos. Solo cambia la descomposición de la varianza.

### Paso 5. Retroalimentación entre la deuda y las variables

Es la "arquitectura B" de Santiago: la deuda rezagada entra en las cuatro ecuaciones y, en la simulación, vuelve como desvío acumulado respecto de la senda base. La deuda se asocia con más superávit (0,051) y más crecimiento; con el EMBI+ la estimación es de 22 puntos básicos por punto de deuda, pero el intervalo incluye el cero. Sin retroalimentación (arquitectura A), las probabilidades casi no cambian.

### Paso 6. Inferencia

*Bootstrap* salvaje de diseño recursivo (Gonçalves y Kilian, 2004). En cada réplica se regenera también la deuda, con un VAR auxiliar que la incluye. Los coeficientes de rezago se corrigen por el sesgo de muestra chica (Kilian, 1998). Semilla fija.

### Paso 7. Simulación

1. **Escenario base del FMI (2026, cuadro 6):** crecimiento, deflactor, tasa efectiva, resultado primario, ajuste stock-flujo e inflación relativa. Se verifica que la identidad reproduzca la senda de deuda del FMI (desvío máximo de 0,1 puntos).
2. **Desvíos:** el SVARX se simula trimestre a trimestre con *shocks* históricos remuestreados.
3. **Identidad:** separa moneda local (42%) y extranjera (58%); la tasa en dólares se reprecia 28% por año.
4. **Métrica del FMI:** la deuda no se estabiliza en T si el superávit del escenario base es menor que el que la estabilizaría. Se mide en 2031 y 2035.
5. **Estimación central:** parámetros corregidos y 20.000 trayectorias (error de Monte Carlo de 0,3 puntos). **Intervalos:** 200 réplicas con 1.000 trayectorias.

### Paso 8. Contrastes

| Hipótesis | Medida | Criterio |
|---|---|---|
| H1a | Superávit necesario en 2031 para llevar la probabilidad al 1% del FMI; descomposición de la varianza como complemento | No basta si el necesario supera el máximo histórico del SPN (3,6% en 2004) |
| H1b | Probabilidad de no estabilización en 2031 y 2035 | Límite inferior de 90% mayor que 1% y 3%; se informa también Bonferroni |
| H2 | Diferencia de probabilidad y de deuda con la FED | Intervalo de 90% que excluye el cero |

### Paso 9. Resultados

- **H1b, respaldada y robusta.** No estabilización de 25,2% en 2031 [19,0; 27,7] y 22,3% en 2035 [15,6; 24,9]. Se cumple en las 18 especificaciones y con el método del FMI (23,7%).
- **H1a, respaldada por suficiencia.** Hace falta un superávit de 7,0% del PIB, el doble del máximo histórico. La descomposición de la varianza (cambiario y de riesgo 59%, fiscal 32%) no es significativa.
- **H2, respaldada de manera débil.** La senda de 2022-2025 suma 13 puntos de probabilidad en 2035 [1,0; 24,8]. No se sostiene con Bonferroni y el efecto sobre la deuda no es significativo. El 60% del efecto es el costo directo de la deuda en dólares.

## Parte 2. Qué encontró la revisión adversarial y cómo se corrigió

| Problema encontrado | Corrección |
|---|---|
| La identidad omitía la inflación relativa del escenario del FMI, que es la valuación de la deuda en dólares. Con eso, la senda base caía el doble que la del FMI | Se incorporó, y ahora un control exige reproducir la senda del FMI antes de simular |
| La retroalimentación usaba la sorpresa del año en lugar del desvío acumulado de la deuda | Corregido: desvío respecto de la senda base |
| Se informaban medias del *bootstrap* en lugar de la estimación puntual, y el *bootstrap* subestimaba la persistencia | Estimación central con corrección de sesgo de Kilian (1998) y 20.000 trayectorias |
| El *bootstrap* no regeneraba la deuda | VAR auxiliar con la deuda como quinta variable |
| El horizonte de mediano plazo del FMI es 2031, no 2030 | Se mide en 2031 |
| El escenario de la FED dejaba la tasa 5,25 puntos más alta durante diez años | Ahora repite la senda real 2022-2025 (sube y después baja) |
| El criterio de H1a (varianza) no medía si el superávit "alcanza" | Contraste de suficiencia como criterio principal |
| Afirmaciones de robustez que no se cumplían (H1a con deuda bruta, H1b con el escenario de 2025) | Corregidas; la tesis informa dónde se sostiene cada resultado y dónde no |
| Errores de texto: un error algebraico en 3.2, atribuciones equivocadas (Eichengreen, Everaert), un marcador sin borrar, rutas de código en el texto, nombre de un autor en una tabla, referencias sin citar y citas sin referencia | Corregidos |

## Parte 3. Lo que todavía nos pueden discutir

1. **"H1a cambió de criterio."** Respuesta: el criterio de varianza no mide si el superávit alcanza; el de suficiencia mide exactamente lo que dice la hipótesis. La varianza se sigue informando y la tesis dice con claridad que no es robusta.
2. **"¿Por qué su probabilidad es 25 veces la del FMI?"** Respuesta: no lo explican el perímetro, el punto de partida ni la identificación; con el método del propio FMI sobre nuestros datos da casi lo mismo (23,7%). La diferencia viene de la historia argentina con la que se generan los *shocks*, que el FMI no publica. La tesis no afirma más que eso.
3. **"El escenario del FMI es para la deuda federal bruta y ustedes lo aplican a la consolidada."** Es cierto; con el ajuste stock-flujo en cero, con la deuda solo del Tesoro o partiendo de la deuda del FMI, las conclusiones no cambian.
4. **"La autocorrelación residual y el remuestreo independiente."** Es cierto (p = 0,036); está declarado como limitación.
5. **"El EMBI+ del período de cesación de pagos."** Sin esos trimestres en el remuestreo, la probabilidad baja a 23,7%; la conclusión no cambia.
6. **"La elasticidad de 0,25 es de la OCDE."** Solo afecta la descomposición de la varianza, no la probabilidad ni la suficiencia.
7. **"H2 es débil."** Es cierto y así se dice: dirección correcta, poca precisión, y el efecto pasa sobre todo por el costo de la deuda en dólares.
8. **"El autovalor corregido es 0,9998, casi una raíz unitaria."** La corrección de Kilian aumenta la persistencia y se la reduce para mantener la estabilidad; con dos rezagos, el modelo es menos persistente y los resultados se mantienen.
9. **Endogeneidad del riesgo país** (no está en el texto por decisión de Pablo): en series de tiempo todo es endógeno salvo los *shocks* de mayor frecuencia que el sistema; por eso el VIX y la tasa de la FED entran como exógenas.

## Parte 4. Pendientes

- **FGS.** Hay que bajar a mano los informes de ANSES; la sensibilidad partiendo de la deuda del FMI ya está hecha.
- **Citas.** Braun y Joy (1968), sin acceso al original; Adler et al. (2016), verificada sobre el documento de trabajo.
- **Revisión.** Que el grupo y Pablo lean el texto completo.

## Parte 5. Números para tener a mano

| Número | Qué es |
|---|---|
| 61,0% del PIB | Deuda consolidada neta a diciembre de 2025 |
| 0,051 [0,010; 0,103] | Reacción fiscal de Bohn |
| 25,2% [19,0; 27,7] | No estabilización en 2031 (FMI: 1%) |
| 22,3% [15,6; 24,9] | No estabilización en 2035 (FMI: menos de 3%) |
| 7,0% del PIB | Superávit necesario para llegar al 1% del FMI (máximo histórico: 3,6%) |
| 59% / 32% / 9% | Varianza de la deuda en 2035: cambiario y de riesgo / fiscal / actividad (no robusto) |
| +13 pp [1; 25] | Efecto de la senda de la FED 2022-2025 sobre la probabilidad en 2035 |
| 35,3 contra 71,5 | Ancho del abanico en 2031: nuestro contra el del FMI |
| 3 rezagos, 111 trimestres | Especificación del VAR |
