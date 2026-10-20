% Qué se hizo con la propuesta metodológica

# Para qué es este documento

Resume qué pasó con cada punto de la propuesta metodológica en la versión final del modelo (19 de octubre de 2026: ventana 1996-2025, binarias presidenciales, cuatro transiciones de la tasa de la FED corregidas, 1.000 réplicas y deuda consolidada desde 2002), por qué se tomó cada decisión y qué tienen que validar Pablo y el equipo. La tesis completa está en Tesis.pdf y en Tesis_borrador.docx; acá va solo lo que toca a la propuesta.

# La retroalimentación entre la deuda y el sistema

La propuesta planteaba que la deuda funcione como una "esponja contable" dentro del SVAR: que el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI), el crecimiento y el tipo de cambio real multilateral (TCRM) muevan la deuda, y que la deuda a su vez mueva al EMBI y al resultado primario.

Había tres caminos posibles:

1. **Fácil:** dejar la deuda afuera del VAR y calcularla al final con la identidad. No hay retroalimentación.
2. **Intermedio, el que se usó:** la deuda rezagada entra en las cuatro ecuaciones del sistema y se acumula con la identidad contable. La retroalimentación va en los dos sentidos: los *shocks* del sistema cambian la deuda, y la deuda cambia el EMBI, el superávit, el crecimiento y el TCRM de los períodos siguientes. En la simulación la deuda que entra en las ecuaciones se actualiza al cierre de cada año, porque la identidad del FMI es anual.
3. **Difícil:** estimar una quinta ecuación para la deuda e identificar también su *shock* contemporáneo.

Se eligió el segundo porque es el que recomienda la literatura para este problema (Favero y Giavazzi, 2007). Una ecuación estimada para la deuda agrega un error que la identidad no tiene y rompe la contabilidad: la deuda simulada dejaría de cerrar con el déficit, los intereses y la devaluación. En un trimestre la deuda casi no reacciona a sí misma por fuera de esos componentes, así que su *shock* propio no tendría interpretación económica. En el *bootstrap*, la deuda histórica se regenera en cada réplica, para que su incertidumbre también entre en los intervalos.

**Qué dio con el modelo nuevo (deuda federal bruta):**

- **Reacción fiscal.** El coeficiente de impacto de la deuda rezagada sobre el resultado primario trimestral es 0,0466 [0,0231; 0,0835]; el multiplicador de largo plazo, que descuenta los rezagos propios del resultado primario, es 0,079 [0,062; 0,147]. Los dos excluyen el cero.
- **EMBI.** Un punto más de deuda sube el EMBI unos 35 puntos básicos [13,9; 47,6]. Sin las binarias presidenciales el intervalo incluye el cero (15,3 [-5,3; 30,4]), de modo que el resultado depende de controlar por los mandatos.
- **Sin retroalimentación.** La probabilidad de no estabilización en 2031 casi no cambia (27,2% contra 27,7%).

# Cada propuesta y qué se hizo

| Propuesta | Qué se hizo | Dónde está |
|---|---|---|
| ADF y KPSS; Zivot-Andrews y Bai-Perron para quiebres | Hecho, con la ventana 1996-2025. Bai-Perron encuentra quiebres en la deuda federal bruta en 2001T4, 2006T2 y 2018T1; el de 2001T4 coincide con el inicio del gobierno de Duhalde y lo reemplazan las binarias presidenciales, y los otros dos entran como binarias. La variante sin ellas se informa | Capítulo 4 y Apéndice A.3 |
| Rezagos por AIC y BIC con residuos sin autocorrelación | Cumplido. Regla: el criterio de Schwarz (BIC) entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados, el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1 rezago, con residuos autocorrelacionados (Portmanteau p < 0,001). Con las binarias presidenciales y la tasa de la FED corregida, ningún orden estable pasa la prueba al 5%, y se usa el orden estable de mayor p-valor, 2 (p = 0,031), que es también el de Hannan-Quinn; la autocorrelación leve que queda se declara como limitación. El AIC sin restricción elige 6, un orden inestable. Todos los órdenes se comparan sobre la misma muestra, 1998T2-2025T4 (111 trimestres): los primeros trimestres de la ventana son condiciones iniciales de los rezagos | Capítulo 4 y Apéndice A.4 |
| Variables binarias por quiebres | Hecho; además, siete binarias por mandato presidencial (pedido del equipo), con pruebas de Wald y de razón de verosimilitud | Capítulo 4 y Apéndice A.3 |
| Deuda como variable del sistema (retroalimentación) | Camino intermedio explicado arriba | Capítulos 4 y 6 |
| Contraste con y sin retroalimentación | Hecho | Capítulo 6 y Apéndice A.10 |
| Cholesky con orden crecimiento, TCRM, EMBI, resultado primario | Como robustez, con dos ordenamientos de Cholesky (resultado primario primero y resultado primario último). La estimación central de la probabilidad de no estabilización es la misma que con la identificación principal (27,7% en 2031), como corresponde: los *shocks* estructurales reconstruyen los mismos residuos. Cambia el reparto de la varianza: la diferencia entre los *shocks* no fiscales y el fiscal es 85,6 [72,3; 99,5] y 99,4 [93,9; 99,8] puntos, contra 96,8 en la principal. Sus matrices de impacto están en el Apéndice A.7. La identificación principal, la que aprobó el director, son restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto | Capítulo 4 y Apéndice A.10 |
| Opción B: tasa en dólares desde el EMBI y tasa en pesos aparte | Es la especificación principal; el canal del EMBI sobre la tasa en pesos va como robustez | Capítulo 4 y Apéndice A.10 |
| *Shock* de la FED con la tasa sombra | Hecho (Wu y Xia, 2016). En las cuatro transiciones entre la tasa sombra y la efectiva (2009T1, 2016T1, 2020T2 y 2022T1), la variación se calcula con la tasa efectiva en los dos trimestres, para no confundir el cambio de serie con un cambio de política | Capítulo 5 |
| *Shocks* de la FED de alta frecuencia | Línea futura | Capítulo 8 |
| Términos de intercambio | Línea futura | Capítulo 8 |
| Probabilidad de que la deuda supere 100% del PIB | Reemplazada por la métrica del FMI, porque el umbral de 100% no tiene fuente que lo justifique | Capítulo 4 |
| Módulo de balanza de pagos | Fuera del alcance; línea futura | Capítulo 8 |
| Restricciones de signo y Blanchard-Quah | No se usan: suponer que el tipo de cambio real es neutral en el largo plazo es difícil de sostener para Argentina | Guía de defensa |
| X-13 para desestacionalizar | Variables binarias estacionales | Capítulo 4 |

# Resultados con el modelo nuevo

Especificación principal: deuda federal bruta, con el punto de partida y el escenario base del FMI (2026). La no estabilización se mide con la métrica anual de la tesis y con la definición operativa del FMI (D16). Intervalos de 90% de Hall.

| Hipótesis | Resultado | Estado |
|---|---|---|
| H1a | (i) La contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del fiscal en 96,8 puntos [90,8; 99,8] (77,9 [67,3; 99,4] sin binarias presidenciales). Reparto: externo 59,4%, cambiario y de riesgo 28,3%, actividad 10,7%, fiscal 1,6%. (ii) Suficiencia: con un desplazamiento uniforme que lleva el resultado primario de 2031 a su máximo de 1996-2025 (3,29% del PIB, 2004), la probabilidad de no estabilización en 2031 es 23,0%; para llevarla al 1% del FMI haría falta sumar 7,25 puntos al resultado primario del escenario en todos los años. Con la definición del FMI, la probabilidad con el máximo histórico es 0,9% | Con la métrica anual, respaldada en sus dos condiciones; con la definición del FMI, solo la (i). La (i) se cumple en las 20 especificaciones en que se informa (menor límite inferior: 67,3, sin binarias presidenciales) |
| H1b | Métrica anual: 27,7% [20,6; 34,7] en 2031, contra 1% del FMI, y 29,0% [25,0; 36,1] en 2035, contra menos de 3%; con Bonferroni, límites inferiores de 19,0 y 24,1. Definición operativa del FMI: 3,1% [0,0; 6,3] y 5,1% [0,0; 10,2] | Respaldada con la métrica anual en las 21 especificaciones (menor límite inferior: 16,2, tres rezagos). No respaldada con la definición del FMI (solo 2 de 21). Con el procedimiento de *shocks* del FMI sobre la historia argentina: 24,1% en 2031 con la métrica anual y 29,1% con la del FMI |
| H2 | Senda de la FED de 2022-2025: +18,4 puntos de probabilidad en 2035 [6,3; 29,1] y +19,3 puntos de deuda [-0,3; 31,3]. Nivel 0,501 puntos más alto: +1,9 [0,3; 3,2] y +2,0 [0,4; 3,2] | Parcialmente respaldada, con las dos métricas. El efecto de la senda sobre la probabilidad excluye el cero: con Bonferroni [4,1; 30,8] y en 20 de 21 especificaciones con la métrica anual, y +17,1 [0,6; 32,6] con la del FMI; su magnitud depende de las binarias y de λ. El efecto sobre la deuda esperada incluye el cero por un margen mínimo, y el del nivel más alto es pequeño y no resiste Bonferroni. El 77% del efecto sobre la deuda es el costo directo de la deuda en dólares; de los canales domésticos solo aparece el del EMBI. Sin binarias presidenciales el efecto de la senda es la mitad (9,7 puntos) |
| Extensión consolidada | No estabilización de 31,1% [27,6; 41,5] en 2031 y 35,0% [32,3; 49,8] en 2035, estimada desde 2002 | Exploratoria: confirma el orden de magnitud de la probabilidad, pero 368 de 1.000 réplicas tienen trayectorias explosivas y no se informan la varianza ni la deuda media |

# Lo que tienen que validar Pablo y el equipo

**0. Métrica de no estabilización (D16), la decisión más importante.** La tesis decía usar la misma métrica que el FMI y no era así. Ahora informa dos con el mismo peso: la anual de la tesis (27,7% en 2031; H1b se cumple) y la definición operativa del FMI (3,1% [0,0; 6,3]; H1b no se cumple, y la condición (ii) de H1a tampoco). Hay que decidir si quedan las dos con el mismo peso o si una pasa a ser la principal. El detalle y las tres opciones están en `_decisiones_finales.md`, D16.

**1. Perímetro de la especificación principal (D1).** La principal pasa a ser la deuda federal bruta, que es el perímetro del análisis de sostenibilidad del FMI, con su punto de partida (80,3% del PIB a fines de 2025). Es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, punto de partida y escenario: el escenario del FMI está construido para esa deuda. La deuda consolidada con el BCRA queda como extensión, con el *stock* consolidado del FMI (52,1% del PIB) como punto de partida. Su construcción sigue siendo un aporte, porque permite estimar la dinámica de ese perímetro y compararla con la federal.

**2. Ventana única 1996-2025 (D2).** El grupo fijó la ventana 1996-2025 para todo el estudio y 2026-2035 para la proyección. Las ecuaciones se estiman con 1998T2-2025T4 (111 trimestres), porque la deuda federal trimestral del MECON empieza en 1998T1 y entra rezagada. Dos series se completan con empalmes documentados (Apéndice A.2 y Figura A.1). El EMBI de 1996T1-1998T3 sale del diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA y la tasa de fondos federales, con la relación estimada en la superposición 1998T4-2001T3: R² = 0,89, error típico de 102 puntos básicos dejando un trimestre afuera y un pronóstico fuera de muestra de 2001 que acierta el nivel y subestima el salto de la crisis. El TCRM de 1996 se encadena con el tipo de cambio real efectivo del BIS (correlación de las variaciones trimestrales de 0,92). Con datos desde 1999, sin empalme, la probabilidad de no estabilización en 2031 es 29,5% [22,5; 36,7], contra 27,7% con la ventana completa. La base anterior tenía valores del EMBI de 1993-1998 escritos a mano sin fuente; se eliminaron.

**3. Definición del resultado primario (D4).** Una sola definición para toda la tesis: el resultado primario del Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4), y la fuente pública del MECON no separa esas transferencias del resto de las rentas de la propiedad; la serie sin rentas es la que las deja afuera. En el perímetro consolidado esas utilidades también son un flujo interno. La serie con rentas se informa como robustez. La versión anterior usaba la serie con rentas para la deuda federal y la presentaba como la definición del FMI; era un error, detectado en la lectura final y corregido. Los resultados casi no cambian (Apéndice A.10).

**4. Título (D13).** "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos". El título anterior hablaba de solvencia intertemporal y de deuda consolidada, que ya no son el objeto central.

**5. H1a con dos condiciones.** H1a se contrasta con el criterio que figuraba antes de estimar, la descomposición de la varianza de la deuda en 2035 con un intervalo de 90% que excluye el cero, y, por la revisión del equipo del 15/10, con una segunda condición que contrasta lo que la hipótesis afirma: con el resultado primario de 2031 en su máximo histórico, la probabilidad de no estabilización sigue por encima del 1% del FMI. Las dos se cumplen.

**6. Binarias presidenciales en la especificación principal.** El equipo pidió incluirlas; las pruebas de Wald y de razón de verosimilitud rechazan que no importen. Pesan en los resultados: sin ellas, el efecto de la senda de la FED se reduce a la mitad. Pablo debería validar que la principal las incluya y que la variante sin ellas quede como robustez.
