# Especificación del modelo: SVARX con identidad de la deuda (versión 1)

Documento para el grupo. Fundamenta, decisión por decisión, la forma del modelo empírico. Cada
decisión se apoya en el marco del FMI, en la literatura o en nuestros propios datos.

## 1. Arquitectura general: la del FMI

El modelo sigue la arquitectura que el propio FMI desarrolló para economías emergentes y aplicó a
Argentina. Celasun, Debrun y Ostry (2006) proponen tres piezas:

1. Un **VAR trimestral sin restricciones** sobre los determinantes de la dinámica de la deuda:
   crecimiento, tasas de interés y tipo de cambio. El VAR describe cómo se mueven juntos, estima
   las varianzas y covarianzas de sus shocks y genera proyecciones consistentes entre sí.
2. Un bloque de **comportamiento fiscal**, en su caso una función de reacción fiscal.
3. La **identidad de acumulación de la deuda**, que separa el tramo en moneda local del tramo
   en moneda extranjera. Por ella pasan las proyecciones del VAR, anualizadas, para calcular la
   deuda de manera recursiva y construir los gráficos de abanico.

El marco vigente del FMI (2021, párr. 52) mantiene la idea central: el gráfico de abanico se
arma aplicando al escenario base shocks tomados de la historia de los determinantes de la deuda.

Nuestro modelo conserva esas tres piezas. Agrega dos cosas que la vacancia justifica: los
shocks se identifican estructuralmente y la tasa de la FED entra como un shock externo con
nombre propio.

## 2. Variables del sistema

| Variable | Rol | Fundamento |
|---|---|---|
| Crecimiento real del PIB | Endógena | Determinante de la identidad de la deuda (Celasun et al., 2006; FMI, 2021). Se usa el crecimiento, no la brecha del producto, porque es lo que entra en la identidad. |
| Resultado primario (% del PIB) | Endógena | Determinante de la identidad. Su ecuación incluye la deuda rezagada, y ese coeficiente es la reacción fiscal de Bohn (1998) que contrasta H1a. |
| EMBI+ | Endógena | Riesgo soberano: forma parte de la tasa en dólares (tasa de Estados Unidos más spread). |
| Tipo de cambio real multilateral | Endógena | Efecto de valuación sobre la deuda en moneda extranjera (Calvo et al., 2003). |
| Deuda consolidada neta (% del PIB) | Entra rezagada en las ecuaciones; evoluciona por la identidad | Retroalimentación de la deuda sobre el sistema (Favero y Giavazzi, 2007). |
| Variación de la tasa de la FED | Exógena | Shock externo de H2. |
| VIX | Exógena | Condiciones financieras globales; es la única variable global con efectos robustos en Adler y Sosa (2013). |
| Dummies de quiebre | Exógenas | Quiebres de Bai-Perron estimados sobre la propia serie de deuda (Bai y Perron, 2003). |

**Por qué la deuda entra rezagada y se acumula con la identidad.** Favero y Giavazzi (2007)
muestran que un VAR fiscal que omite la retroalimentación de la deuda está mal especificado:
la restricción presupuestaria hace que el nivel de deuda condicione la política fiscal y las
tasas. Su solución es incluir la deuda rezagada en las ecuaciones y hacerla evolucionar con la
identidad, no con una ecuación estimada. Eso da los "efectos conjuntos" que pide la pregunta de
investigación y mantiene la acumulación contablemente exacta. Corrige además al `fase19` actual,
donde la deuda era una regresión libre.

## 3. Por qué la FED y el VIX entran como exógenas

Argentina es una economía pequeña y abierta: sus variables no afectan la tasa de la FED ni el
VIX. En los VAR de economías pequeñas y abiertas, el supuesto estándar es que las variables
externas forman un bloque exógeno (Cushman y Zha, 1997). Así se modela la transmisión de los
shocks de Estados Unidos a América Latina (Canova, 2005) y la relación entre tasas
internacionales y spreads en emergentes (Uribe y Yue, 2006).

Una consecuencia importante es que **el efecto de la FED (H2) no depende de cómo se ordenen las
variables argentinas entre sí**. Se calcula como un multiplicador dinámico de la variable
exógena.

La serie es la tasa de fondos federales. En los trimestres en que esa tasa estuvo en el piso de
cero se usa la tasa sombra de Wu y Xia (2016), que mide la orientación de la política monetaria
cuando la tasa efectiva no puede bajar más (ver `informe_tasa_fed_v1.md`).

## 4. Identificación de los shocks argentinos

| Shock | Supuesto | Fundamento |
|---|---|---|
| Fiscal | El componente cíclico del resultado primario se descuenta con una elasticidad de 0,25, y el resto es el shock fiscal discrecional. | Blanchard y Perotti (2002). La política discrecional tarda más de un trimestre en reaccionar, y la elasticidad se toma de estimaciones externas (Girouard y André, 2005). |
| Actividad | El producto puede responder al shock fiscal dentro del trimestre. | Blanchard y Perotti (2002). |
| Riesgo soberano y tipo de cambio | Se identifican como **bloque**, sin ordenarlos entre sí. Se reporta solo su contribución conjunta. | Christiano, Eichenbaum y Evans (1999): con una identificación recursiva por bloques, lo que se identifica no depende del orden dentro de cada bloque. No hay razón teórica para ordenar el EMBI+ y el tipo de cambio, y H1a solo necesita el bloque "cambiario y de riesgo" en conjunto. |

**Esto corrige al `fase19` actual.** El capítulo dice que el EMBI+ y el tipo de cambio quedan
sin ordenar, pero el código los ordenaba. Ahora el código hace lo que dice el texto.

## 5. Niveles, rezagos e inferencia

- **Variables en niveles.** El VAR se estima en niveles aunque algunas variables tengan raíz
  unitaria. Sims, Stock y Watson (1990) muestran que las estimaciones siguen siendo consistentes
  sin imponer relaciones de cointegración. Para 1996-2025, la prueba de Johansen no rechaza la
  ausencia de cointegración, así que imponer un rango concreto sería un supuesto sin respaldo.
- **Rezagos.** Se toma el menor número de rezagos que indican los criterios de información y con
  el que los residuos quedan libres de autocorrelación (Lütkepohl, 2005; Ivanov y Kilian, 2005).
  En la prueba preliminar, el criterio BIC elegía un solo rezago y la autocorrelación quedaba,
  así que esta regla corrige esa elección.
- **Intervalos de confianza.** Los residuos preliminares rechazan la normalidad y muestran
  volatilidad cambiante en el tiempo (heterocedasticidad condicional) en dos ecuaciones. Por eso
  los intervalos se calculan con un *bootstrap* robusto a esa heterocedasticidad (Gonçalves y
  Kilian, 2004), con semilla fija para que sean reproducibles.

## 6. Shocks de la simulación

- **De dónde salen.** Se remuestrean los residuos estimados, que conservan las colas gordas que
  la normal no captura. Es la versión econométrica del principio del FMI de usar shocks
  históricos (FMI, 2021, párr. 52).
- **Incertidumbre de parámetros.** Cada trayectoria usa parámetros de una réplica del
  *bootstrap*. Eso da el intervalo de confianza con el que se contrasta H1b.
- **Escenario base.** Los senderos son los del FMI (2025): crecimiento, resultado primario, tasa
  efectiva y ajuste stock-flujo. Así la comparación con su 3% de no estabilización es directa.
- **Tamaño del shock de la FED.** Un desvío estándar de la variación trimestral, 0,50 puntos
  porcentuales, que es la convención para medir respuestas en estos modelos. Como escenario
  histórico se agrega el ciclo de subas de 2022-2023, de 5,25 puntos.
- **Tasa en dólares.** Es la tasa de la FED más el EMBI+ simulado.

## 7. Qué se contrasta con qué

| Hipótesis | Medida | Criterio |
|---|---|---|
| H1a | Coeficiente de la deuda rezagada en la ecuación del resultado primario, y contribución de cada bloque de shocks a la varianza de la deuda simulada | La reacción no es significativa al 5%, y el bloque cambiario y de riesgo aporta más que el fiscal. |
| H1b | Probabilidad de que la deuda no se estabilice, con el escenario base del FMI | El límite inferior del intervalo de 90% supera el 3% del FMI (contraste unilateral al 5%). |
| H2 | Diferencia en esa probabilidad y en la deuda esperada entre el escenario con shock de la FED y el escenario base | El intervalo de 90% de la diferencia excluye el cero. |

## Referencias

- Bai, J., y Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics*, 18(1), 1-22.
- Blanchard, O., y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. *Quarterly Journal of Economics*, 117(4), 1329-1368.
- Bohn, H. (1998). The behavior of U.S. public debt and deficits. *Quarterly Journal of Economics*, 113(3), 949-963.
- Calvo, G. A., Izquierdo, A., y Talvi, E. (2003). *Sudden stops, the real exchange rate, and fiscal sustainability: Argentina's lessons* (NBER Working Paper No. 9828).
- Canova, F. (2005). The transmission of US shocks to Latin America. *Journal of Applied Econometrics*, 20(2), 229-251.
- Celasun, O., Debrun, X., y Ostry, J. D. (2006). *Primary surplus behavior and risks to fiscal sustainability in emerging market countries: A "fan-chart" approach* (IMF Working Paper WP/06/67).
- Christiano, L. J., Eichenbaum, M., y Evans, C. L. (1999). Monetary policy shocks: What have we learned and to what end? En J. B. Taylor y M. Woodford (Eds.), *Handbook of Macroeconomics* (Vol. 1A, pp. 65-148). Elsevier.
- Cushman, D. O., y Zha, T. (1997). Identifying monetary policy in a small open economy under flexible exchange rates. *Journal of Monetary Economics*, 39(3), 433-448.
- Favero, C., y Giavazzi, F. (2007). *Debt and the effects of fiscal policy* (NBER Working Paper No. 12822).
- Fondo Monetario Internacional. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper).
- Fondo Monetario Internacional. (2025). *Argentina: Request for an extended arrangement under the Extended Fund Facility* (IMF Country Report No. 25/95).
- Girouard, N., y André, C. (2005). *Measuring cyclically-adjusted budget balances for OECD countries* (OECD Economics Department Working Papers No. 434).
- Gonçalves, S., y Kilian, L. (2004). Bootstrapping autoregressions with conditional heteroskedasticity of unknown form. *Journal of Econometrics*, 123(1), 89-120.
- Ivanov, V., y Kilian, L. (2005). A practitioner's guide to lag order selection for VAR impulse response analysis. *Studies in Nonlinear Dynamics and Econometrics*, 9(1).
- Lütkepohl, H. (2005). *New introduction to multiple time series analysis*. Springer.
- Sims, C. A., Stock, J. H., y Watson, M. W. (1990). Inference in linear time series models with some unit roots. *Econometrica*, 58(1), 113-144.
- Uribe, M., y Yue, V. Z. (2006). Country spreads and emerging countries: Who drives whom? *Journal of International Economics*, 69(1), 6-36.
- Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking*, 48(2-3), 253-291.
