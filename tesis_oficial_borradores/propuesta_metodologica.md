% Qué se hizo con la propuesta metodológica

# Para qué es este documento

Resume qué pasó con cada punto de la propuesta metodológica en la versión del modelo reestimada con la ventana 1996-2025 (17 de octubre de 2026), por qué se tomó cada decisión y qué tienen que validar Pablo y el equipo. La tesis completa está en Tesis.pdf y en Tesis_borrador.docx; acá va solo lo que toca a la propuesta.

# La retroalimentación entre la deuda y el sistema

La propuesta planteaba que la deuda funcione como una "esponja contable" dentro del SVAR: que el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), el crecimiento y el tipo de cambio real multilateral (TCRM) muevan la deuda, y que la deuda a su vez mueva al EMBI y al resultado primario.

Había tres caminos posibles:

1. **Fácil:** dejar la deuda afuera del VAR y calcularla al final con la identidad. No hay retroalimentación.
2. **Intermedio, el que se usó:** la deuda rezagada entra en las cuatro ecuaciones del sistema y se acumula con la identidad contable. La retroalimentación va en los dos sentidos: los *shocks* del sistema cambian la deuda, y la deuda cambia el EMBI, el superávit, el crecimiento y el TCRM de los períodos siguientes. En la simulación la deuda que entra en las ecuaciones se actualiza al cierre de cada año, porque la identidad del FMI es anual.
3. **Difícil:** estimar una quinta ecuación para la deuda e identificar también su *shock* contemporáneo.

Se eligió el segundo porque es el que recomienda la literatura para este problema (Favero y Giavazzi, 2007). Una ecuación estimada para la deuda agrega un error que la identidad no tiene y rompe la contabilidad: la deuda simulada dejaría de cerrar con el déficit, los intereses y la devaluación. En un trimestre la deuda casi no reacciona a sí misma por fuera de esos componentes, así que su *shock* propio no tendría interpretación económica. En el *bootstrap*, la deuda histórica se regenera en cada réplica, para que su incertidumbre también entre en los intervalos.

**Qué dio con el modelo nuevo (deuda federal bruta):**

- **Reacción fiscal.** El coeficiente de impacto de la deuda rezagada sobre el resultado primario trimestral es 0,0576 [0,0220; 0,0822]; el multiplicador de largo plazo, que descuenta los rezagos propios del resultado primario, es 0,199 [0,112; 0,328]. Los dos tienen intervalo y los dos excluyen el cero.
- **EMBI.** Un punto más de deuda sube el EMBI unos 15 puntos básicos, con un intervalo de 90% que incluye el cero.
- **Sin retroalimentación.** La probabilidad de no estabilización en 2031 casi no cambia (30,4% contra 31,8%), pero el abanico se abre (54,4 puntos de ancho en 2031 contra 46,6), porque sin la reacción fiscal nada frena la deuda.

# Cada propuesta y qué se hizo

| Propuesta | Qué se hizo | Dónde está |
|---|---|---|
| ADF y KPSS; Zivot-Andrews y Bai-Perron para quiebres | Hecho, con la ventana 1996-2025. Los quiebres de Bai-Perron sobre la deuda federal bruta (2001T4, 2006T2, 2018T1) entran como variables binarias; la variante sin ellas se informa | Capítulo 4 y Apéndice A.3 |
| Rezagos por AIC y BIC con residuos sin autocorrelación | Cumplido. Regla: el criterio de Schwarz (BIC) entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados, el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1 rezago, con residuos autocorrelacionados (Portmanteau p = 0,000); se usan 2, sin autocorrelación (p = 0,056), que es también el orden de Hannan-Quinn. El AIC sin restricción elige 6. Todos los órdenes se comparan sobre la misma muestra, 1998T2-2025T4 (111 trimestres): los primeros trimestres de la ventana son condiciones iniciales de los rezagos | Capítulo 4 y Apéndice A.4 |
| Variables binarias por quiebres | Hecho | Capítulo 4 |
| Deuda como variable del sistema (retroalimentación) | Camino intermedio explicado arriba | Capítulos 4 y 6 |
| Contraste con y sin retroalimentación | Hecho | Capítulo 6 y Apéndice A.9 |
| Cholesky con orden crecimiento, TCRM, EMBI, resultado primario | Como robustez, con dos ordenamientos de Cholesky (resultado primario primero y resultado primario último). La probabilidad de no estabilización es exactamente la misma que con la identificación principal (31,8% en 2031), como corresponde: los *shocks* estructurales reconstruyen los mismos residuos. Cambia el reparto de la varianza: la diferencia entre los *shocks* no fiscales y el fiscal es 60,7 [25,6; 73,4] y 91,9 [84,1; 98,5] puntos, contra 78,3 en la principal. La identificación principal, la que aprobó el director, son restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto | Capítulo 4 y Apéndice A.9 |
| Opción B: tasa en dólares desde el EMBI y tasa en pesos aparte | Es la especificación principal; el canal del EMBI sobre la tasa en pesos va como robustez | Capítulo 4 y Apéndice A.9 |
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
| H1a | La contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del fiscal en 78,3 puntos [57,3; 87,9]. Reparto: externo 44,9%, cambiario y de riesgo 32,3%, actividad 12,0%, fiscal 10,8%. Complemento descriptivo: con el resultado primario en su máximo de 1996-2025 (3,29% del PIB, 2004) todos los años, la probabilidad de no estabilización en 2031 es 26,1%; para llevarla al 1% del FMI haría falta sumar 8,00 puntos al resultado primario del escenario en todos los años | Respaldada con su criterio original, en las 20 especificaciones (menor límite inferior: 25,6) |
| H1b | No estabilización de 31,8% [25,2; 36,4] en 2031, contra 1% del FMI, y de 31,0% [26,8; 35,6] en 2035, contra menos de 3%. Con Bonferroni, los límites inferiores son 24,2 y 26,6 | Respaldada en las 20 especificaciones (menor límite inferior: 19,1, deuda consolidada). Con el procedimiento de *shocks* del FMI sobre la historia argentina se obtiene 24,1% en 2031: tampoco se reproduce el 1% |
| H2 | Senda de la FED de 2022-2025: +9,7 puntos de probabilidad en 2035 [4,2; 16,0] y +9,0 puntos de deuda [0,3; 16,2]. Nivel 0,494 puntos más alto: +1,1 [0,2; 1,9] y +1,0 [0,0; 1,8] | Respaldada en el efecto de la senda sobre la probabilidad, que es robusto: con Bonferroni sigue excluyendo el cero [3,6; 16,8] y lo excluye en 18 de 20 especificaciones. El efecto sobre la deuda esperada y el del nivel más alto no son robustos: con Bonferroni incluyen el cero. El mecanismo no es el que propone la hipótesis: solo 2 de 84 intervalos de respuesta excluyen el cero, los dos del TCRM, y el 96% del efecto sobre la deuda es el costo directo de la deuda en dólares |
| Extensión consolidada | No estabilización de 26,5% [19,1; 30,5] en 2031 y 24,1% [20,0; 30,0] en 2035 | Mismas conclusiones para H1a y H1b; el efecto de la senda de la FED sobre la deuda esperada incluye el cero |

# Lo que tienen que validar Pablo y el equipo

**1. Perímetro de la especificación principal (D1).** La principal pasa a ser la deuda federal bruta, que es el perímetro del análisis de sostenibilidad del FMI, con su punto de partida (80,3% del PIB a fines de 2025). Es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, punto de partida, escenario y métrica: el escenario del FMI está construido para esa deuda. La deuda consolidada con el BCRA queda como extensión, con el *stock* consolidado del FMI (52,1% del PIB) como punto de partida. Su construcción sigue siendo un aporte, porque permite estimar la dinámica de ese perímetro y compararla con la federal.

**2. Ventana única 1996-2025 (D2).** El grupo fijó la ventana 1996-2025 para todo el estudio y 2026-2035 para la proyección. Las ecuaciones se estiman con 1998T2-2025T4 (111 trimestres), porque los primeros trimestres de la ventana son condiciones iniciales de los rezagos. Dos series se completan con empalmes documentados (Apéndice A.2 y Figura A.1). El EMBI de 1996T1-1998T3 sale del diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA y la tasa de fondos federales, con la relación estimada en la superposición 1998T4-2001T3: R² = 0,89, error típico de 102 puntos básicos dejando un trimestre afuera y un pronóstico fuera de muestra de 2001 que acierta el nivel y subestima el salto de la crisis. El TCRM de 1996 se encadena con el tipo de cambio real efectivo del BIS (correlación de las variaciones trimestrales de 0,92). Con datos desde 1999, sin empalme, la probabilidad de no estabilización en 2031 es 32,4% [26,6; 37,0], contra 31,8% con la ventana completa. La base anterior tenía valores del EMBI de 1993-1998 escritos a mano sin fuente; se eliminaron.

**3. Definición del resultado primario (D4).** Una sola definición para toda la tesis: el resultado primario del Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4), y la fuente pública del MECON no separa esas transferencias del resto de las rentas de la propiedad; la serie sin rentas es la que las deja afuera. En el perímetro consolidado esas utilidades también son un flujo interno. La serie con rentas se informa como robustez. La versión anterior usaba la serie con rentas para la deuda federal y la presentaba como la definición del FMI; era un error, detectado en la lectura final y corregido. Los resultados casi no cambian (Apéndice A.9).

**4. Título (D13).** "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos". El título anterior hablaba de solvencia intertemporal y de deuda consolidada, que ya no son el objeto central.

**5. H1a con su criterio original.** H1a se contrasta con el criterio que figuraba antes de estimar: la descomposición de la varianza de la deuda en 2035, con un intervalo de 90% que excluye el cero. El cambio de criterio de la versión anterior se eliminó y ya no hace falta. La suficiencia del superávit queda como análisis descriptivo, sin criterio de contraste.
