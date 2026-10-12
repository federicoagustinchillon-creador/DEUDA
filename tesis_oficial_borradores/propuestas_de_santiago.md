% Qué se hizo con la metodología propuesta por Santiago

# Para qué es este documento

Resume qué pasó con cada propuesta de la metodología de Santiago, por qué se tomó cada decisión y qué tienen que validar Santiago y Pablo antes de seguir. La tesis completa está en Tesis.pdf y en Tesis_borrador.docx; acá va solo lo que toca lo que él ya había armado.

# La retroalimentación entre la deuda y el sistema

Santiago propuso que la deuda funcione como una "esponja contable" dentro del SVAR: que el riesgo país, el crecimiento y el tipo de cambio muevan la deuda, y que la deuda a su vez mueva al riesgo país y al resultado primario.

Había tres caminos posibles:

1. **Fácil:** dejar la deuda afuera del VAR y calcularla al final con la identidad. No hay retroalimentación.
2. **Intermedio, el que se usó:** la deuda rezagada entra en las cuatro ecuaciones del sistema y se acumula trimestre a trimestre con la identidad contable. La retroalimentación va en los dos sentidos: los *shocks* del sistema cambian la deuda, y la deuda del período anterior cambia el riesgo país, el superávit, el crecimiento y el tipo de cambio del período siguiente.
3. **Difícil:** estimar una quinta ecuación para la deuda e identificar también su *shock* contemporáneo.

Se eligió el segundo porque es el que recomienda la literatura para este problema (Favero y Giavazzi, 2007). Una ecuación estimada para la deuda agrega un error que la identidad no tiene y rompe la contabilidad: la deuda simulada dejaría de cerrar con el déficit, los intereses y la devaluación. Además, en un trimestre la deuda casi no reacciona a sí misma por fuera de esos componentes, así que el *shock* propio de la deuda no tiene interpretación económica.

El camino difícil sí se usa en una parte: en el *bootstrap*, cada réplica regenera la deuda histórica con un VAR auxiliar de cinco variables, para que la incertidumbre de la deuda también entre en los intervalos.

**Qué dio:** un punto más de deuda sube el EMBI+ 22 puntos básicos en el trimestre siguiente, pero el intervalo de 90% incluye el cero. La deuda sí tiene un efecto claro sobre el superávit (la reacción fiscal de Bohn, 0,051). Si se apaga la retroalimentación, la probabilidad de no estabilización casi no cambia (25,6% contra 25,2% en 2031), porque el riesgo país más alto y el superávit más alto se compensan. El abanico, en cambio, se abre mucho más (46,7 puntos de ancho contra 35,3), porque sin la reacción fiscal nada frena la deuda.

# Cada propuesta y qué se hizo

| Propuesta de Santiago | Qué se hizo | Dónde está |
|---|---|---|
| ADF y KPSS; Zivot-Andrews y Bai-Perron para quiebres | Hecho; los quiebres de Bai-Perron (2001T4, 2006T2, 2018T1) entran como variables binarias | 4.2, 6.1 y Apéndice A.2 |
| Rezagos por AIC y BIC con residuos sin autocorrelación | El mayor rezago estable que no supere al del AIC (3). No se logró eliminar toda la autocorrelación; se informa como limitación | 4.5, A.3, A.4 y 7.6 |
| Variables binarias por quiebres | Hecho | 4.2 |
| Deuda como variable del sistema (retroalimentación) | Camino intermedio explicado arriba | 4.2 y 6.1 |
| Contraste con y sin retroalimentación | Hecho | Tabla 6.6 |
| Cholesky con orden crecimiento, TCRM, EMBI+, resultado primario | Como robustez, con el resultado primario primero y último. La identificación principal es Blanchard y Perotti, la que aprobó Pablo | 4.4 y Tabla 6.6 |
| Opción B: tasa en dólares desde el EMBI+ y tasa en pesos aparte | Es la especificación principal; el canal del riesgo país sobre la tasa en pesos va como robustez | 4.6 y Tabla 6.6 |
| *Shock* de la FED con la tasa sombra | Hecho (Wu y Xia, 2016) | 5.4 |
| *Shocks* de la FED de alta frecuencia | Línea futura | 8 |
| Términos de intercambio (Lanteri, 2019) | Línea futura | 8 |
| Probabilidad de que la deuda supere 100% del PIB | Reemplazada por la métrica del FMI, porque el umbral de 100% no tiene fuente que lo justifique | 4.7 |
| Módulo de balanza de pagos | Fuera del alcance; línea futura | 8 |
| Restricciones de signo y Blanchard-Quah | No se usan: suponer que el tipo de cambio real es neutral en el largo plazo es difícil de sostener para Argentina | Guía de defensa |
| X-13 para desestacionalizar | Variables binarias estacionales | 4.2 |

# Lo que tienen que validar Santiago y Pablo

**1. El criterio de H1a cambió.** La hipótesis de Santiago dice que el superávit por sí solo no alcanza. Antes se contrastaba con la descomposición de la varianza: si los *shocks* no fiscales explican más varianza de la deuda que los fiscales. Con las correcciones de la simulación, esa diferencia (35,9 puntos) tiene un intervalo que incluye el cero y cambia de signo en algunas variantes, así que no sirve como prueba principal.

El criterio nuevo pregunta directamente lo que dice la hipótesis: cuánto superávit haría falta para que la probabilidad de no estabilización baje al 1% que usa el FMI. Hace falta 7,0% del PIB, el doble del máximo de las últimas tres décadas (3,6% en 2004). Con el máximo histórico la probabilidad sigue en torno a 15%. La descomposición de la varianza queda informada como complemento.

**2. Los resultados cambiaron respecto de las versiones anteriores.** Una revisión completa encontró errores en la simulación: faltaba la inflación relativa del escenario del FMI, la retroalimentación usaba la sorpresa del año y no el desvío acumulado, y el *bootstrap* informaba promedios de réplicas sesgadas. Todo está corregido y explicado en la Guía de defensa. Los números que valen son estos:

| Hipótesis | Resultado | Estado |
|---|---|---|
| H1a | Hace falta 7,0% del PIB de superávit; el máximo histórico es 3,6% | Respaldada |
| H1b | 25,2% en 2031 [19,0; 27,7] contra 1% del FMI; 22,3% en 2035 [15,6; 24,9] contra menos de 3% | Respaldada en las 18 variantes |
| H2 | La senda de la FED de 2022-2025 suma 13,0 puntos de probabilidad en 2035 [1,0; 24,8] | Respaldada de forma débil: no resiste la corrección por pruebas múltiples |

**3. Pendientes del grupo.** Acordar qué se recorta para bajar de 69 a unas 60 páginas. Bajar a mano los informes del FGS de la ANSES, que bloquea la descarga automática (los enlaces están en el Plan de labor). Revisar si el título debería cambiar: "solvencia intertemporal" y "post-2025" prometen algo más amplio que lo que se mide, que es la probabilidad de que la deuda no se estabilice entre 2026 y 2035.
