# 6. Resultados

Todos los resultados de este capítulo salen de la misma muestra efectiva, 1998T2-2025T4 (111 trimestres), y del mismo escenario base, el del FMI (2025, anexo II). La especificación principal usa la deuda consolidada neta con las Letras Intransferibles a valor nominal, que parte de 61,0% del PIB en diciembre de 2025. Las cifras se pueden reproducir con `codigo/modelos/fase24_svarx_1996_2025.py` y `codigo/modelos/fase25_simulacion_dsa_svarx.py`.

## 6.1 El SVARX estimado

**Rezagos y diagnósticos.** Con la regla de la sección 4.5, el modelo usa tres rezagos. La raíz de mayor módulo del polinomio característico es 0,96, de modo que el sistema es estable y tiene representación de medias móviles. La prueba de Portmanteau con 12 rezagos da un p-valor de 0,036: queda algo de autocorrelación en los residuos, que se informa como limitación. Los residuos no son normales (p < 0,001), lo que justifica remuestrear shocks históricos en lugar de suponer normalidad. La prueba ARCH-LM con cuatro rezagos no detecta heterocedasticidad condicional en ninguna ecuación (p-valores entre 0,87 y 0,99). El *bootstrap* salvaje es válido con y sin heterocedasticidad, así que su uso no depende de este resultado.

**Reacción fiscal.** El coeficiente de la deuda rezagada en la ecuación del resultado primario es 0,051 (p = 0,019), con un intervalo de 90% del *bootstrap* de [0,020; 0,082]. Diez puntos más de deuda en relación con el PIB se asocian, en promedio, con medio punto más de superávit primario. El resultado no depende del perímetro de la deuda:

| Serie de deuda | Rezagos | Reacción fiscal | Intervalo de 90% |
|---|---|---|---|
| Consolidada neta, Letras a valor nominal (principal) | 3 | 0,051 | [0,020; 0,082] |
| Consolidada neta, Letras a valor libros | 3 | 0,053 | [0,021; 0,085] |
| Consolidada bruta | 4 | 0,054 | [0,027; 0,079] |

El signo coincide con el que encuentran Celasun et al. (2006) en su panel de economías emergentes. La política fiscal argentina respondió a la deuda en el período, pero con un coeficiente chico. La simulación muestra si esa respuesta alcanza para estabilizarla.

**Respuesta a la tasa de la FED.** Un aumento de un desvío estándar en la tasa de política de la FED (0,50 puntos porcentuales) no produce respuestas significativas de las variables domésticas en ninguno de los horizontes considerados (0, 4, 8 y 20 trimestres). El EMBI+ sube 9 puntos básicos en el trimestre del shock, con un intervalo de 90% de [-83; 103], y 12 puntos básicos a los dos años, con un intervalo de [-14; 42]. El tipo de cambio real y el resultado primario tampoco responden de manera significativa. La única excepción es el crecimiento, que en el trimestre del shock sube medio punto con un intervalo que apenas excluye el cero, [0,00; 1,04]. Ese signo no tiene una explicación económica clara y desaparece desde el cuarto trimestre. Con 111 trimestres y un shock chico, el modelo no puede distinguir los efectos indirectos de la FED del ruido.

## 6.2 El gráfico de abanico

La Tabla 6.1 resume la distribución de la deuda simulada. La mediana baja de 61,0% del PIB en 2025 a 35,9% en 2030 y a 16,7% en 2035. La caída la determina el escenario base del FMI, que combina un superávit primario de alrededor de 2,5% del PIB con una tasa de interés efectiva de alrededor de 4% y un deflactor del PIB que crece cerca de 7,5% por año. Con esos supuestos, la tasa real que paga la deuda es negativa y la licua año tras año.

**Tabla 6.1. Deuda consolidada neta simulada (% del PIB), percentiles**

| Año | p5 | p25 | Mediana | p75 | p95 |
|---|---|---|---|---|---|
| 2026 | 46,0 | 49,7 | 52,8 | 56,9 | 64,5 |
| 2028 | 37,7 | 41,9 | 45,6 | 50,0 | 57,9 |
| 2030 | 25,9 | 31,2 | 35,9 | 40,7 | 49,6 |
| 2032 | 15,0 | 21,1 | 26,9 | 32,7 | 44,2 |
| 2035 | 2,2 | 9,6 | 16,7 | 23,7 | 38,5 |

El ancho del abanico entre los percentiles 5 y 95 es de 19,4 puntos en 2030, con un intervalo de 90% de [15,4; 24,3]. El del FMI para la deuda federal bruta es 74,2 (FMI, 2025, anexo II, cuadro 7). El Capítulo 7 analiza esta diferencia.

## 6.3 Contraste de H1a

H1a sostiene que el superávit primario, por sí solo, no basta para estabilizar la deuda, porque la condicionan también el crecimiento, el tipo de cambio real y el riesgo país. El contraste compara la contribución de cada bloque de shocks a la varianza de la deuda simulada en 2035.

| Bloque de shocks | Participación en la varianza de la deuda en 2035 | Intervalo de 90% |
|---|---|---|
| Fiscal | 19,4% | [3,5; 41,2] |
| Actividad | 21,6% | [3,9; 49,9] |
| Cambiario y de riesgo (EMBI+ y TCRM) | 59,0% | [12,5; 89,5] |
| No fiscal menos fiscal (diferencia) | 61,2 puntos | [17,5; 93,0] |

Los shocks no fiscales explican cerca de cuatro quintos de la incertidumbre sobre la deuda en 2035, y el intervalo de la diferencia con el fiscal excluye el cero. **H1a queda respaldada.** El bloque cambiario y de riesgo es el que más pesa. El resultado es coherente con la reacción fiscal positiva de la sección 6.1: el superávit responde a la deuda, pero la variabilidad de la deuda la dominan el tipo de cambio real y el riesgo país.

## 6.4 Contraste de H1b

| Horizonte | Probabilidad de no estabilización | Intervalo de 90% | Criterio (límite inferior > 3%) |
|---|---|---|---|
| 2030 (cinco años, el horizonte del FMI) | 11,8% | [8,0; 15,8] | Se cumple |
| 2035 (diez años) | 6,0% | [3,0; 9,8] | Límite inferior igual al umbral |

A cinco años, la probabilidad de que la deuda consolidada no se estabilice es de 11,8%, casi cuatro veces el 3% del FMI, y el intervalo de 90% queda entero por encima del umbral. **H1b queda respaldada en el horizonte en que el FMI mide su métrica.** A diez años la probabilidad baja a 6,0%, porque el escenario base sigue reduciendo la deuda y cada vez menos trayectorias terminan con la deuda en aumento. El límite inferior del intervalo coincide con el 3%, así que a diez años el contraste no rechaza que la probabilidad sea igual a la del FMI.

## 6.5 Contraste de H2

| Escenario | Diferencia en la probabilidad de no estabilización en 2035 | Diferencia en la deuda media en 2035 |
|---|---|---|
| Suba de un desvío estándar (0,50 pp) | +0,5 pp [0,0; 1,5] | +0,7 pp del PIB |
| Repetición del ciclo 2022-2023 (+5,25 pp en ocho trimestres) | +7,7 pp [2,5; 16,0] | +7,0 pp del PIB [1,4; 16,0] |

Entre corchetes, los intervalos de 90%.

Con un shock de un desvío estándar, el intervalo de la diferencia en la probabilidad toca el cero, de modo que no hay un efecto distinguible. Con una suba como la de 2022-2023, la probabilidad de no estabilización en 2035 sube 7,7 puntos y la deuda esperada, 7,0 puntos del PIB, y los dos intervalos excluyen el cero. **H2 queda respaldada para un endurecimiento de la magnitud del de 2022-2023, y no para un shock de un desvío estándar.**

Para saber por qué canal pasa el efecto, se repitió el escenario de 2022-2023 anulando la respuesta de las variables domésticas a la FED, de modo que solo actúa el mayor costo de refinanciar la deuda en dólares. Con los parámetros estimados, ese costo directo explica 4,7 de los 7,3 puntos de aumento de la deuda en 2035 (dos tercios). El tercio restante corresponde a la respuesta del riesgo país, el tipo de cambio real y el crecimiento, que en conjunto empujan en la misma dirección aunque, como se vio en la sección 6.1, ninguna de esas respuestas es significativa por separado.

## 6.6 Robustez

**Perímetro de la deuda.** Con la deuda neta a valor libros y con la deuda bruta, los resultados cambian poco. La probabilidad de no estabilización a cinco años es de 13,0% y 12,7%, con límites inferiores de 9,0% y 9,0%. A diez años es de 6,8% y 7,3%, y en los dos casos el límite inferior (3,3% y 4,0%) queda por encima del 3%. La contribución de los shocks no fiscales supera a la del fiscal en las dos variantes, aunque con la deuda bruta el límite inferior de la diferencia queda prácticamente en cero (0,1 puntos). El efecto del ciclo 2022-2023 sobre la probabilidad a diez años es de 8,2 y 7,2 puntos, con intervalos que excluyen el cero.

**Canal de tasas domésticas.** Si el riesgo país también encarece la deuda en pesos (sección 4.6), la probabilidad de no estabilización sube a 12,2% a cinco años y a 7,6% a diez años, con límites inferiores de 8,5% y 3,7%: con este canal, H1b queda respaldada en los dos horizontes. El bloque cambiario y de riesgo pasa a explicar 66,9% de la varianza de la deuda en 2035 y el efecto del ciclo 2022-2023 sube a 9,0 puntos de probabilidad.

**Shocks como los del FMI.** Con el procedimiento del abanico del FMI aplicado a las mismas series (sección 4.6), la probabilidad de no estabilización es de 23,5% a cinco años y de 15,1% a diez años, y el ancho del abanico en 2030 es de 93,3 puntos. Con la deuda bruta, las cifras son 25,2%, 17,4% y 118,4. Las dos formas de generar los shocks llevan a la misma conclusión sobre H1b. La del FMI da probabilidades y anchos mucho mayores.

**Tabla 6.2. Resumen de robustez de H1b**

| Especificación | No estabilización 2030 | No estabilización 2035 | Ancho del abanico 2030 |
|---|---|---|---|
| SVARX, deuda neta (principal) | 11,8% [8,0; 15,8] | 6,0% [3,0; 9,8] | 19,4 |
| SVARX, deuda neta a valor libros | 13,0% [9,0; 17,8] | 6,8% [3,3; 10,8] | 19,9 |
| SVARX, deuda bruta | 12,7% [9,0; 17,0] | 7,3% [4,0; 11,3] | 20,9 |
| SVARX, deuda neta con canal de tasas domésticas | 12,2% [8,5; 16,0] | 7,6% [3,7; 12,0] | 21,3 |
| Shocks a la manera del FMI, deuda neta | 23,5% | 15,1% | 93,3 |
| Shocks a la manera del FMI, deuda bruta | 25,2% | 17,4% | 118,4 |
| FMI (2025), deuda federal bruta | 3,0% | | 74,2 |

Entre corchetes, los intervalos de 90% del *bootstrap* de parámetros. Las filas a la manera del FMI no tienen intervalo porque ese procedimiento no estima parámetros.
