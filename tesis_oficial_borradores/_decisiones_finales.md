# Decisiones finales de la revisión (12 de octubre de 2026). Documento interno

Base de toda la reescritura. Los números salen exclusivamente de `_hoja_de_numeros.md` (generada por `codigo/modelos/hoja_de_numeros.py`) y del Apéndice (`apendice.md`, generado por `codigo/modelos/apendice_tablas.py`). Ningún número puede salir de otro lado ni de versiones anteriores del texto.

## D1. Perímetro de la especificación principal: deuda federal bruta (perímetro del FMI)

- Principal: deuda bruta del gobierno federal (Administración Central), el perímetro del análisis de sostenibilidad del FMI (2026, anexo II). Punto de partida: el stock del FMI a fines de 2025, 80,3% del PIB (cuadro 2, línea 1, que incluye intereses capitalizados, deuda no presentada al canje y reclamos por los cupones PBI). La serie propia, construida con datos del MECON, da 77,7% a fines de 2025; la diferencia son esos conceptos y la medición del PIB.
- Por qué: es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, el mismo punto de partida, el mismo escenario y la misma métrica. El escenario del FMI (tasa efectiva, ajuste stock-flujo, inflación relativa, necesidades de financiamiento) está construido para esa deuda.
- Extensión: deuda del sector público consolidado con el BCRA en la definición del FMI (cuadro 2, línea 5: deuda federal fuera del sector público más pasivos del BCRA), 52,1% del PIB a fines de 2025, con 68,5% en moneda extranjera (proporción en pesos 0,315). La dinámica se estima con la serie propia de deuda consolidada (Tesoro más BCRA, Letras a valor nominal). El ajuste stock-flujo y la inflación relativa del FMI se escalan por la deuda en pesos y en moneda extranjera de ese perímetro.
- El título de la tesis cambia en consecuencia (D13). La construcción de la deuda consolidada sigue siendo un objetivo y un aporte: permite estimar la dinámica de ese perímetro y compararla con la federal.

## D2. Muestra

- Datos desde 1999T1. El EMBI+ Argentina de J.P. Morgan se toma de la serie diaria que publica Ámbito Financiero, disponible desde diciembre de 1998, como promedio trimestral. Los valores de 1996-1998 eran diferenciales de bonos Brady y de 1998T1-T3 transcriptos sin cuadro ni página de origen, y el TCRM de 1996 estaba retropolado. Empezar en 1999 deja todas las series con una fuente publicada y verificable.
- Muestra efectiva común: 2000T3-2025T4, 102 trimestres. Se reservan los primeros trimestres como condiciones iniciales para que todos los órdenes de rezago (hasta seis) se comparen sobre la misma muestra (Lütkepohl, 2005, sec. 4.3).

## D3. Rezagos

- Regla: el criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si los residuos de ese orden rechazan la ausencia de autocorrelación (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no la rechaza (Lütkepohl, 2005, sec. 4.4).
- Resultado: Schwarz elige 1, cuyos residuos están autocorrelacionados (p = 0,000); se usan 2 (p = 0,296), que es también el orden que elige Hannan-Quinn. Autovalor máximo 0,849.
- La versión anterior citaba a Ivanov y Kilian para justificar el AIC; esa cita era incorrecta para datos trimestrales y esta muestra.

## D4. Resultado primario

- Definición coherente con el perímetro. Federal: con rentas de la propiedad, que es la definición del FMI para el gobierno federal (2025: 1,4% en el FMI y 1,38% en la serie; 2024: 1,8% y 1,78%); las utilidades que el BCRA transfiere al Tesoro son ingreso del Tesoro. Consolidada: sin rentas de la propiedad, porque en ese perímetro las utilidades del BCRA son un flujo interno. La otra definición se informa como robustez.
- Máximo anual 1999-2025 con la definición del FMI: 3,58% del PIB en 2004 (sin rentas: 3,29%).

## D5. Tasa de la FED

- Tasa de fondos federales con la tasa sombra de Wu y Xia (2016) en el límite cero. En 2022T1, cuando la serie pasa de la tasa sombra a la efectiva, la variación se calcula con la tasa efectiva en ambos trimestres, para no confundir el cambio de serie con un cambio de política. Desvío de la variación trimestral en la muestra: 0,504 puntos.

## D6. Variables externas en la simulación

- El VIX y el nivel de la tasa de la FED se simulan con procesos AR(1) estimados en la muestra (coeficientes 0,700 y 0,960). Sus innovaciones históricas se remuestrean junto con los shocks estructurales, por fecha, de modo que la incertidumbre externa forma parte del abanico. La descomposición de la varianza agrega un cuarto bloque, externo (FED y VIX).

## D7. Remuestreo de shocks

- Bloques de ocho trimestres consecutivos (dos años), como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI). Conserva la autocorrelación remanente y la correlación entre variables.

## D8. Inferencia

- Estimación central con los parámetros de MCO (autovalor máximo 0,849) y 20.000 trayectorias; error de Monte Carlo 0,33 puntos.
- Intervalos de 90%: bootstrap de bloques móviles de cuatro trimestres sobre los residuos, de diseño recursivo, en el que la deuda también se regenera (Brüggemann, Jentsch y Trenkler, 2016), con percentiles de Hall (1992), que corrigen el sesgo de la distribución bootstrap respecto de la estimación puntual. Brüggemann et al. muestran además que el bootstrap salvaje no reproduce la estructura de cuarto orden de las innovaciones de la que dependen las respuestas estructurales; por eso se abandona.
- Todas las especificaciones usan los mismos números aleatorios: las diferencias entre filas no vienen del sorteo. Las identificaciones alternativas dan exactamente la misma probabilidad, como corresponde.
- La corrección de sesgo de Kilian (1998) se informa como robustez.

## D9. Identidad y métrica

- El ajuste stock-flujo del FMI (capitalización de deuda indexada, sobre todo en 2026-2027) se escala por la deuda en pesos simulada respecto de la del FMI; la inflación relativa, por la deuda en moneda extranjera. La métrica de estabilización incluye el ajuste stock-flujo, como la identidad: pb* = d_{T-1}(M_T − 1) + sf_T + ri_T. Es la definición del FMI (2021, párr. 53): el resultado primario que estabiliza la deuda en T.
- El desvío del crecimiento anual es la variación del promedio anual del nivel del PIB, no la suma de las tasas trimestrales.
- La proporción en pesos queda fija en el escenario, el mismo supuesto del FMI (2021, anexo VI, párr. 6).
- La retroalimentación se actualiza al cierre de cada año, porque la identidad del FMI es anual: dentro del año, la deuda que entra en las ecuaciones es la del cierre del año anterior.

## D10. H1a

- Criterio: el original, sin cambios: la contribución de los shocks no fiscales a la varianza de la deuda en 2035 supera a la del shock fiscal, con un intervalo de 90% que excluye el cero. Resultado: 82,6 puntos [65,8; 92,4]; se cumple en las 19 especificaciones (el menor límite inferior es 31,4, con Cholesky y el resultado primario primero).
- Complemento sin criterio de contraste (análisis descriptivo, declarado así): con el resultado primario en su máximo anual de 1999-2025 (3,58%) todos los años, la probabilidad de no estabilización en 2031 es 25,5%; para llevarla al 1% que informa el FMI haría falta sumar 7,75 puntos al resultado primario del escenario en todos los años (9,2% del PIB en 2026, 10,0% en 2031). En 2035 la relación no es monótona: la probabilidad baja hasta 1,35% (+6,25) y vuelve a subir (2,05% con +8,00), porque con la deuda cerca de cero la métrica se activa con cualquier shock.
- Se elimina la versión anterior que había cambiado el criterio tras ver los resultados: ya no hace falta, y el texto lo dice en el registro de cambios del grupo, no en la tesis.

## D11. H1b

- Comparación con el mismo perímetro, punto de partida, escenario, horizonte y métrica del FMI. Criterio: el límite inferior del intervalo de 90% supera la probabilidad del FMI (1% en 2031; menos de 3% en 2035), con corrección de Bonferroni por los dos horizontes (95%).
- Resultado: 32,8% [26,8; 37,9] en 2031 y 31,3% [27,0; 35,3] en 2035; al 95%: límites inferiores 26,3 y 26,4. Se cumple en las 19 especificaciones (menor límite inferior 20,3, deuda consolidada).
- Con el procedimiento de shocks del FMI aplicado a la historia argentina 2000-2025, sobre el mismo perímetro: 16,6% en 2031 y un ancho de 151,1. Tampoco se reproduce el 1%: la diferencia con el FMI proviene de la distribución de shocks que este usa, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). La tesis no atribuye la brecha a una causa que no puede verificar.

## D12. H2

- Criterio sin cambios: el intervalo de 90% de la diferencia entre el escenario de la FED y el base excluye el cero, en la probabilidad y en la deuda esperada, al final del horizonte (2035), porque el efecto de una tasa más alta se acumula. 2031 se informa.
- Escenarios: (i) nivel de la tasa 0,504 puntos más alto en forma permanente desde 2026T1; (ii) repetición de la senda trimestral de 2022-2025 en 2026-2029: sube 5,25 puntos y baja 1,43, y desde 2030 queda 3,82 puntos por encima del escenario base hasta 2035.
- Resultado: (i) probabilidad 2035 +1,5 [0,5; 2,6], deuda 2035 +1,5 [0,1; 2,5]; (ii) probabilidad 2035 +11,3 [4,4; 17,9], deuda 2035 +12,6 [1,2; 21,8]. Se cumple el criterio en la especificación principal.
- Salvedades: con Bonferroni (95%) los efectos sobre la probabilidad siguen excluyendo el cero (+0,2 y +1,4 como límites inferiores) y los efectos sobre la deuda esperada no (-0,0 y -0,5). En las robusteces, el efecto de la senda sobre la probabilidad excluye el cero en 18 de 19 especificaciones; sobre la deuda, en 12 de 19. Los canales que nombra la hipótesis (riesgo soberano, tipo de cambio real, crecimiento) no se distinguen: 3 de 84 intervalos de respuesta excluyen el cero, todos del TCRM y con signo de apreciación. El 75% del efecto sobre la deuda en 2035 es el costo directo de la deuda en dólares, que la identidad incorpora (9,4 de 12,6 puntos). Veredicto: H2 respaldada en su efecto sobre la probabilidad; no en su mecanismo.

## D13. Título

"Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos"

## D14. Extensión

- La tabla completa de robustez pasa al Apéndice (A.8). Resultados conserva una tabla corta.
- Antecedentes: los ejes 2, 3 y 8 se reducen a lo esencial.
