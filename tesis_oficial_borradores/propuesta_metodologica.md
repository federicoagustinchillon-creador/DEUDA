% Qué se hizo con la propuesta metodológica

# Para qué es este documento

Resume qué pasó con cada punto de la propuesta metodológica en la versión del modelo del 12 de octubre de 2026, por qué se tomó cada decisión y qué tienen que validar Pablo y el equipo. La tesis completa está en Tesis.pdf y en Tesis_borrador.docx; acá va solo lo que toca a la propuesta.

# La retroalimentación entre la deuda y el sistema

La propuesta planteaba que la deuda funcione como una "esponja contable" dentro del SVAR: que el riesgo país, el crecimiento y el tipo de cambio muevan la deuda, y que la deuda a su vez mueva al riesgo país y al resultado primario.

Había tres caminos posibles:

1. **Fácil:** dejar la deuda afuera del VAR y calcularla al final con la identidad. No hay retroalimentación.
2. **Intermedio, el que se usó:** la deuda rezagada entra en las cuatro ecuaciones del sistema y se acumula con la identidad contable. La retroalimentación va en los dos sentidos: los *shocks* del sistema cambian la deuda, y la deuda cambia el riesgo país, el superávit, el crecimiento y el tipo de cambio de los períodos siguientes. En la simulación la deuda que entra en las ecuaciones se actualiza al cierre de cada año, porque la identidad del FMI es anual.
3. **Difícil:** estimar una quinta ecuación para la deuda e identificar también su *shock* contemporáneo.

Se eligió el segundo porque es el que recomienda la literatura para este problema (Favero y Giavazzi, 2007). Una ecuación estimada para la deuda agrega un error que la identidad no tiene y rompe la contabilidad: la deuda simulada dejaría de cerrar con el déficit, los intereses y la devaluación. En un trimestre la deuda casi no reacciona a sí misma por fuera de esos componentes, así que su *shock* propio no tendría interpretación económica. En el *bootstrap*, la deuda histórica se regenera en cada réplica, para que su incertidumbre también entre en los intervalos.

**Qué dio con el modelo nuevo (deuda federal bruta):**

- **Reacción fiscal.** El coeficiente de impacto de la deuda rezagada sobre el resultado primario trimestral es 0,0495 [0,0099; 0,0799]; el multiplicador de largo plazo, que descuenta los rezagos propios del resultado primario, es 0,167 [0,057; 0,296]. Los dos tienen intervalo y los dos excluyen el cero.
- **Riesgo país.** Un punto más de deuda sube el EMBI+ 15,5 puntos básicos, con un intervalo de 90% de [-4,2; 29,7] que incluye el cero.
- **Sin retroalimentación.** La probabilidad de no estabilización en 2031 casi no cambia (31,4% contra 32,8%), pero el abanico se abre (55,5 puntos de ancho en 2031 contra 48,3), porque sin la reacción fiscal nada frena la deuda.

# Cada propuesta y qué se hizo

| Propuesta | Qué se hizo | Dónde está |
|---|---|---|
| ADF y KPSS; Zivot-Andrews y Bai-Perron para quiebres | Hecho, con datos desde 1999. Los quiebres de Bai-Perron sobre la deuda federal bruta (2001T4, 2006T2, 2018T1) entran como variables binarias; la variante sin ellas se informa | Capítulo 4 y Apéndice A.2 |
| Rezagos por AIC y BIC con residuos sin autocorrelación | Cumplido. Regla: el criterio de Schwarz (BIC) entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados, el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1 rezago, con residuos autocorrelacionados (Portmanteau p = 0,000); se usan 2, sin autocorrelación (p = 0,296), que es también el orden de Hannan-Quinn. El AIC sin restricción elige 5. Todos los órdenes se comparan sobre la misma muestra, 2000T3-2025T4 | Capítulo 4 y Apéndice A.3 |
| Variables binarias por quiebres | Hecho | Capítulo 4 |
| Deuda como variable del sistema (retroalimentación) | Camino intermedio explicado arriba | Capítulos 4 y 6 |
| Contraste con y sin retroalimentación | Hecho | Capítulo 6 y Apéndice A.8 |
| Cholesky con orden crecimiento, TCRM, EMBI+, resultado primario | Como robustez, con el resultado primario primero y último. La probabilidad de no estabilización es exactamente la misma que con la identificación principal (32,8% en 2031), como corresponde: los *shocks* estructurales reconstruyen los mismos residuos. Cambia el reparto de la varianza: la diferencia entre los *shocks* no fiscales y el fiscal es 63,9 [31,4; 75,3] y 95,8 [92,0; 100,0] puntos, contra 82,6 en la principal. La identificación principal es la de Blanchard y Perotti (2002), la que aprobó el director | Capítulo 4 y Apéndice A.8 |
| Opción B: tasa en dólares desde el EMBI+ y tasa en pesos aparte | Es la especificación principal; el canal del riesgo país sobre la tasa en pesos va como robustez | Capítulo 4 y Apéndice A.8 |
| *Shock* de la FED con la tasa sombra | Hecho (Wu y Xia, 2016). En 2022T1, cuando la serie pasa de la tasa sombra a la efectiva, la variación se calcula con la tasa efectiva en los dos trimestres, para no confundir el cambio de serie con un cambio de política | Capítulo 5 |
| *Shocks* de la FED de alta frecuencia | Línea futura | Capítulo 8 |
| Términos de intercambio | Línea futura | Capítulo 8 |
| Probabilidad de que la deuda supere 100% del PIB | Reemplazada por la métrica del FMI, porque el umbral de 100% no tiene fuente que lo justifique | Capítulo 4 |
| Módulo de balanza de pagos | Fuera del alcance; línea futura | Capítulo 8 |
| Restricciones de signo y Blanchard-Quah | No se usan: suponer que el tipo de cambio real es neutral en el largo plazo es difícil de sostener para Argentina | Guía de defensa |
| X-13 para desestacionalizar | Variables binarias estacionales | Capítulo 4 |

# Resultados con el modelo nuevo

Especificación principal: deuda federal bruta, con el punto de partida, el escenario base y la métrica del FMI (2026). Intervalos de 90% de Hall.

| Hipótesis | Resultado | Estado |
|---|---|---|
| H1a | La contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del fiscal en 82,6 puntos [65,8; 92,4]. Reparto: externo 46,6%, cambiario y de riesgo 32,3%, actividad 12,4%, fiscal 8,7%. Complemento descriptivo: con el resultado primario en su máximo de 1999-2025 (3,58% del PIB, 2004) todos los años, la probabilidad de no estabilización en 2031 es 25,5%; para llevarla al 1% del FMI haría falta sumar 7,75 puntos al resultado primario del escenario en todos los años | Respaldada con su criterio original, en las 19 especificaciones (menor límite inferior: 31,4) |
| H1b | No estabilización de 32,8% [26,8; 37,9] en 2031, contra 1% del FMI, y de 31,3% [27,0; 35,3] en 2035, contra menos de 3%. Con Bonferroni, los límites inferiores son 26,3 y 26,4 | Respaldada en las 19 especificaciones (menor límite inferior: 20,3, deuda consolidada). Con el procedimiento de *shocks* del FMI sobre la historia argentina se obtiene 16,6% en 2031: tampoco se reproduce el 1% |
| H2 | Senda de la FED de 2022-2025: +11,3 puntos de probabilidad en 2035 [4,4; 17,9] y +12,6 puntos de deuda [1,2; 21,8]. Nivel 0,50 puntos más alto: +1,5 [0,5; 2,6] y +1,5 [0,1; 2,5] | Respaldada en su efecto sobre la probabilidad; no en su mecanismo. Con Bonferroni, el efecto sobre la deuda esperada incluye el cero. Solo 3 de 84 intervalos de respuesta excluyen el cero, todos del TCRM. El 75% del efecto sobre la deuda es el costo directo de la deuda en dólares |
| Extensión consolidada | No estabilización de 26,8% [20,3; 31,0] en 2031 y 24,1% [20,4; 29,6] en 2035 | Mismas conclusiones para H1a y H1b; el efecto de la senda de la FED sobre la deuda esperada incluye el cero |

# Lo que tienen que validar Pablo y el equipo

**1. Perímetro de la especificación principal (D1).** La principal pasa a ser la deuda bruta del gobierno federal, que es el perímetro del análisis de sostenibilidad del FMI, con su punto de partida (80,3% del PIB a fines de 2025). Es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, punto de partida, escenario y métrica: el escenario del FMI está construido para esa deuda. La deuda consolidada con el BCRA queda como extensión, con el *stock* consolidado del FMI (52,1% del PIB) como punto de partida. Su construcción sigue siendo un aporte, porque permite estimar la dinámica de ese perímetro y compararla con la federal.

**2. Muestra desde 1999 (D2).** Los datos empiezan en 1999T1, porque desde entonces el EMBI+ se toma de la serie diaria que publica Ámbito Financiero. Los valores de 1996-1998 eran diferenciales de bonos Brady y valores transcriptos sin cuadro ni página de origen, y el TCRM de 1996 estaba retropolado. La muestra efectiva es 2000T3-2025T4 (102 trimestres).

**3. Definición del resultado primario (D4).** Para la deuda federal, con rentas de la propiedad, que es la definición del FMI para el gobierno federal: las utilidades que el BCRA transfiere al Tesoro son ingreso del Tesoro. Para la deuda consolidada, sin rentas, porque en ese perímetro esas utilidades son un flujo interno. La otra definición se informa como robustez.

**4. Título (D13).** "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos". El título anterior hablaba de solvencia intertemporal y de deuda consolidada, que ya no son el objeto central.

**5. H1a con su criterio original.** H1a se contrasta con el criterio que figuraba antes de estimar: la descomposición de la varianza de la deuda en 2035, con un intervalo de 90% que excluye el cero. El cambio de criterio de la versión anterior se eliminó y ya no hace falta. La suficiencia del superávit queda como análisis descriptivo, sin criterio de contraste.
