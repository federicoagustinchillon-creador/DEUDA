# 7. Discusión

## 7.1 Qué cambia respecto del diagnóstico del FMI

El FMI (2026) concluye que la deuda argentina es sostenible pero no con alta probabilidad, y estima en alrededor de 99% la probabilidad de que se estabilice en el mediano plazo. Esta tesis llega a un diagnóstico más exigente con el mismo escenario base. Con shocks identificados y el perímetro consolidado, la probabilidad de no estabilización a cinco años es de 11,5%, con un intervalo de 90% de 7,7% a 15,2%. Como el escenario base es el mismo, la diferencia no viene de supuestos más pesimistas sobre crecimiento, superávit o tasas. Viene de la forma de representar la incertidumbre alrededor de esos supuestos, que es la vacancia que plantea la sección 2.9.

A diez años la diferencia se achica: 6,6%, con un límite inferior de 3,3%, apenas por encima del 3% que el FMI da como cota para ese horizonte. No es una contradicción. La métrica del FMI pregunta si el ajuste del escenario base alcanza para poner la deuda en una senda descendente (FMI, 2021, anexo VI, nota 9). En el escenario del FMI la deuda baja rápido, de modo que hacia 2035 quedan pocas trayectorias en las que el superávit previsto resulte insuficiente. El riesgo se concentra en los primeros años, que son también los que el FMI mira para su calificación de riesgo a mediano plazo.

## 7.2 Por qué el abanico es más angosto y, aun así, la probabilidad es mayor

El ancho del abanico de esta tesis en 2030 es de 18,6 puntos del PIB, contra 71,5 del FMI. A primera vista, un abanico cuatro veces más angosto debería dar una probabilidad de no estabilización menor, no mayor. La variante con shocks a la manera del FMI (sección 6.6) permite separar las causas, porque usa los mismos datos, la misma identidad y la misma métrica, y cambia solo la forma de generar los shocks.

**El ancho depende de cómo se generan los shocks, no del perímetro.** Con el procedimiento del FMI aplicado a la deuda neta, el ancho es de 82,8 puntos, del mismo orden que el del FMI. Con el SVARX, la deuda bruta da 19,3 puntos, casi lo mismo que la neta. El perímetro mueve el ancho en uno o dos puntos y la forma de los shocks lo multiplica por cuatro.

La Figura 7.1 compara los dos abanicos. Las medianas son casi iguales, porque las fija el escenario base; lo que cambia es la dispersión.

![Figura 7.1. Abanicos con shocks del SVARX y con shocks a la manera del FMI. Deuda consolidada neta simulada, percentiles 5 y 95 y mediana (% del PIB). Los shocks a la manera del FMI son bloques de dos años de desvíos históricos, 1997-2025.](../tesis/figuras/fig7_1_abanico_svarx_vs_fmi.png)

**Qué ensancha el abanico del procedimiento del FMI.** El ejercicio de la Tabla 7.1 repite esa variante quitando el año 2002 o fijando cada impulsor en su media histórica.

**Tabla 7.1. Diagnóstico de la variante con shocks a la manera del FMI (deuda neta)**

| Variante | No estabilización 2030 | No estabilización 2035 | Ancho del abanico 2030 |
|---|---|---|---|
| Todos los años, 1997-2025 | 23,0% | 15,2% | 82,8 |
| Sin el año 2002 | 22,4% | 15,2% | 62,9 |
| Depreciación real en su media | 20,1% | 13,1% | 61,9 |
| Tasa real efectiva en su media | 10,4% | 7,3% | 54,6 |
| Crecimiento en su media | 22,2% | 12,6% | 70,7 |
| Resultado primario en su media | 22,6% | 14,6% | 84,1 |

Fuente: `codigo/modelos/fase25b_diagnostico_abanico_fmi.py`.

Un solo año, 2002, aporta un cuarto del ancho: la depreciación real de ese año (145%) aparece, con probabilidad uno en catorce, en cada bloque de dos años sorteado. La probabilidad de no estabilización, en cambio, depende sobre todo de la tasa real efectiva. Esa tasa pasó de valores positivos durante la convertibilidad (entre 6% y 9% en 1997-2001) a valores muy negativos con la inflación posterior (-56% en 2023 y -66% en 2024). El procedimiento del FMI mide los shocks como desvíos respecto de una única media para todo el período, de -17%. Así, un año como 1999 cuenta como un shock de 26 puntos de tasa real, y puede aparecer en 2030 junto con cualquier otro año de la muestra, aunque correspondan a regímenes monetarios distintos. Es una manifestación del problema que el propio FMI y el ESM (2023) señalan como desafío de su método: que la historia usada para generar el abanico sea representativa del futuro.

![Figura 7.2. Impulsores anuales de la deuda que usa la variante a la manera del FMI, 1997-2025. La tasa real efectiva pasa de valores positivos en la convertibilidad a valores muy negativos con la inflación posterior.](../tesis/figuras/fig7_2_impulsores_historicos.png)

**Qué hace distinto el SVARX.** El SVARX trata los cambios de régimen con las variables binarias de los quiebres estructurales (2001, 2006 y 2018) y separa lo que la dinámica del sistema permite anticipar de lo que es sorpresa. Solo remuestrea las sorpresas, que son menores que los desvíos respecto de una media de largo plazo. Además, la tasa en dólares se reprecia de a poco, a medida que vence la deuda. El resultado es un abanico más angosto, pero con una forma que importa: los shocks cambiarios y de riesgo son persistentes y están correlacionados entre sí, y por eso, cuando ocurren, empujan la deuda hacia arriba durante varios años seguidos. Con esa persistencia, una dispersión menor alcanza para que en 11,5% de las trayectorias el superávit del escenario base no frene la suba de la deuda en 2030.

**Lo que no se puede reproducir.** Con nuestros datos, el procedimiento del FMI da 23,0% de no estabilización, no 1%. El FMI no publica la muestra histórica ni los datos de los impulsores que usa para Argentina, así que esta diferencia no se puede descomponer con la información disponible. Las dos estimaciones de esta tesis (11,5% con el SVARX y 23,0% con el procedimiento del FMI) superan el 1%, de modo que la conclusión sobre H1b a cinco años no depende de esa elección.

## 7.3 El papel del superávit primario

La reacción fiscal estimada es positiva y significativa (0,051): en 1998-2025, el resultado primario respondió a la deuda, en línea con la condición de Bohn (1998). Pero el bloque fiscal explica alrededor de un quinto de la varianza de la deuda en 2035, y el cambiario y de riesgo, tres quintos. Esto respalda la idea central de H1a. El superávit es necesario, y el escenario base del FMI se apoya en él, pero no alcanza para controlar la trayectoria, porque la mayor parte del riesgo viene del tipo de cambio real y de la prima de riesgo. El resultado coincide con el diagnóstico de la restricción externa del Capítulo 3: con más de la mitad de la deuda en moneda extranjera, una depreciación real cambia el cociente de deuda aunque las cuentas fiscales estén en orden (Calvo et al., 2003).

## 7.4 El shock de la FED

El efecto de la FED depende del tamaño del shock. Una suba de medio punto no tiene un efecto distinguible. Un ciclo como el de 2022-2023 eleva la deuda en 8 puntos del PIB hacia 2035. Tres quintos de ese efecto vienen del canal más directo, el mayor costo de refinanciar la deuda en dólares, y el resto de la respuesta del riesgo país, el tipo de cambio real y el crecimiento. Las respuestas al impulso de esas variables no son significativas por separado. Esto no quiere decir que los canales indirectos no existan. Uribe y Yue (2006) y Canova (2005) los documentan con paneles y muestras más largas. Quiere decir que una sola serie argentina de 111 trimestres no alcanza para medirlos con precisión. La conclusión sobre H2 descansa, por lo tanto, sobre todo en el canal de costo.

## 7.5 Limitaciones

- **Escenario base.** Todos los resultados están condicionados al escenario del FMI, que supone una tasa real efectiva negativa durante toda la década. Si la desinflación avanza más rápido de lo que supone el FMI, el efecto licuación se reduce y las probabilidades de este capítulo serían cotas inferiores.
- **Tasas en pesos.** La especificación principal no hace depender la tasa de la deuda en pesos del riesgo país. Cuando se agrega ese canal, las probabilidades suben (8,8% a diez años, frente a 6,6%). Por eso, la especificación principal es conservadora.
- **Robustez de H1a al perímetro.** Con la deuda bruta, la diferencia entre los shocks no fiscales y el fiscal sigue siendo positiva (52,6 puntos), pero su intervalo de 90% incluye el cero. H1a se sostiene con las dos medidas de deuda neta, que son las que corresponden a la consolidación con el BCRA.
- **Activos del FGS.** La deuda neta no descuenta los títulos públicos en poder del Fondo de Garantía de Sustentabilidad, porque no hay una serie trimestral pública para todo el período (Capítulo 5). Por eso la deuda neta de esta tesis queda por encima de la consolidada que informa el FMI.
- **Autocorrelación residual.** La prueba de Portmanteau rechaza la ausencia de autocorrelación al 5% (p = 0,036). Los órdenes que la eliminarían son inestables, de modo que se mantuvo el orden estable y se informa la limitación.
- **Precisión de los canales externos.** Las respuestas individuales a la FED no son significativas, por lo que la descomposición del efecto de H2 por canales se informa como estimación puntual.
