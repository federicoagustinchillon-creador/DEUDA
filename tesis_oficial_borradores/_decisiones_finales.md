# Decisiones finales de la revisión (12 de octubre de 2026). Documento interno

Base de toda la reescritura. Los números salen exclusivamente de `_hoja_de_numeros.md` (generada por `codigo/modelos/hoja_de_numeros.py`) y del Apéndice (`apendice.md`, generado por `codigo/modelos/apendice_tablas.py`). Ningún número puede salir de otro lado ni de versiones anteriores del texto.

## D1. Perímetro de la especificación principal: deuda federal bruta (perímetro del FMI)

- Principal: deuda bruta del gobierno federal (Administración Central), el perímetro del análisis de sostenibilidad del FMI (2026, anexo II). Punto de partida: el stock del FMI a fines de 2025, 80,3% del PIB (cuadro 2, línea 1, que incluye intereses capitalizados, deuda no presentada al canje y reclamos por los cupones PBI). La serie propia, construida con datos del MECON, da 77,7% a fines de 2025; la diferencia son esos conceptos y la medición del PIB.
- Por qué: es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, el mismo punto de partida, el mismo escenario y la misma métrica. El escenario del FMI (tasa efectiva, ajuste stock-flujo, inflación relativa, necesidades de financiamiento) está construido para esa deuda.
- Extensión: deuda del sector público consolidado con el BCRA en la definición del FMI (cuadro 2, línea 5: deuda federal fuera del sector público más pasivos del BCRA), 52,1% del PIB a fines de 2025, con 68,5% en moneda extranjera (proporción en pesos 0,315). La dinámica se estima con la serie propia de deuda consolidada (Tesoro más BCRA, Letras a valor nominal). El ajuste stock-flujo y la inflación relativa del FMI se escalan por la deuda en pesos y en moneda extranjera de ese perímetro.
- El título de la tesis cambia en consecuencia (D13). La construcción de la deuda consolidada sigue siendo un objetivo y un aporte: permite estimar la dinámica de ese perímetro y compararla con la federal.

## D2. Ventana única 1996-2025 (decisión del grupo, no se negocia)

- Todo el estudio usa la ventana 1996-2025: datos, series, quiebres, figuras, descriptivos y estimación. La proyección es 2026-2035. En ningún lugar del texto puede aparecer otro período de estudio.
- La única aclaración técnica, y solo en Metodología, Datos y el Apéndice: los primeros trimestres de la ventana se usan como condiciones iniciales de los rezagos (variación de la tasa de la FED con dos rezagos y comparación de órdenes hasta seis rezagos sobre una muestra común; Lütkepohl, 2005, sec. 4.3), de modo que las ecuaciones se estiman con los trimestres 1998T2-2025T4 (111 observaciones). Eso no cambia la ventana: es cómo se estima un VAR con rezagos.
- Dos series no tienen dato directo publicado en toda la ventana y se completan con empalmes documentados y validados (código: codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py; validación: Apéndice y Figura A.1):
  - EMBI 1996T1-1998T3. La serie pública diaria de J.P. Morgan para Argentina empieza el 11 de diciembre de 1998. Para antes se usa el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA (serie oficial, mensual desde octubre de 1994) y la tasa de fondos federales: durante la convertibilidad, ese costo del dólar en el sistema financiero argentino refleja el riesgo argentino. Relación estimada en la superposición 1998T4-2001T3 (12 trimestres; termina antes del corralito, que rompe ese mercado): EMBI = 550,3 + 1,171 × diferencial, R² = 0,89, correlación 0,944. Validación cruzada dejando un trimestre afuera: error típico de 102 puntos básicos, contra un desvío del EMBI de 240. Fuera de muestra (estimando con 1998T4-2000T4 y pronosticando 2001): 744, 801 y 1.033 contra 750, 973 y 1.469 observados: acierta el nivel y subestima el salto de la crisis, de modo que el empalme, si sesga, atenúa la volatilidad de 1996-1998 y vuelve conservadoras las probabilidades.
  - TCRM 1996. El índice del BCRA empieza en enero de 1997. Para 1996 se encadena hacia atrás con las variaciones del tipo de cambio real efectivo amplio del BIS (invertido, porque el BIS sube con la apreciación). Las variaciones trimestrales de ambos índices tienen una correlación de 0,92 en 1997-2025 y de 0,98 en 1997-2001. Con dos rezagos, los valores de 1996 solo intervienen como condiciones iniciales.
  - Prueba de que el resultado no depende del empalme: con datos desde 1999 (solo EMBI observado), la probabilidad de no estabilización es 32,4% [26,6; 37,0] en 2031, contra 31,8% [25,2; 36,4] con la ventana completa; H1a se mantiene (75,5 [51,7; 86,3]) y el efecto de la senda de la FED sobre la probabilidad también (9,6 [2,5; 15,7]) (Apéndice A.9).
- La base anterior tenía para el EMBI de 1993-1998 valores escritos a mano sin fuente; se eliminaron. No deben mencionarse en la tesis (sí en la revisión crítica interna).

## D2b. Reglas de consistencia de todo el texto

- Período: "1996-2025" para el estudio, "2026-2035" para la proyección. Prohibido "1999-2025", "2000-2025", "2000T3" como período (solo se admite "datos desde 1999" para nombrar la variante de robustez sin empalme, y las fechas de inicio de las fuentes en Datos).
- Riesgo país: la variable se llama EMBI. Primera mención en cada capítulo: "el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI)". Después siempre "EMBI" (no "EMBI+", no "spread", no "diferencial soberano" como nombre alternativo; "riesgo país" solo como concepto). La palabra *spread* solo puede aparecer en la definición, en cursiva.
- Identificación: siempre con el mismo nombre: "restricciones de impacto en la línea de Blanchard y Perotti (2002)" para el bloque fiscal y de actividad, con "un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto". Robustez: "dos ordenamientos de Cholesky (resultado primario primero y resultado primario último)". Toda mención de la identificación (Introducción 1.6, Metodología 4.4, Resultados, Discusión, Conclusiones, Plan) debe nombrar exactamente esto.
- Tipo de cambio: "tipo de cambio real multilateral (TCRM)" en la primera mención; después "TCRM".
- Deuda: "deuda federal bruta" (principal) y "deuda consolidada con el BCRA" (extensión). Nunca "deuda consolidada neta" ni "deuda pública" a secas cuando se refiere a una de las dos.
- FED: "tasa de política monetaria de la Reserva Federal (FED)"; la serie es la tasa de fondos federales con la tasa sombra de Wu y Xia (2016) en el límite cero.

## D3. Rezagos

- Regla: el criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si los residuos de ese orden rechazan la ausencia de autocorrelación (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no la rechaza (Lütkepohl, 2005, sec. 4.4).
- Resultado: Schwarz elige 1, cuyos residuos están autocorrelacionados (p = 0,000); se usan 2 (p = 0,056), que es también el orden que elige Hannan-Quinn. Autovalor máximo 0,896.
- La versión anterior citaba a Ivanov y Kilian para justificar el AIC; esa cita era incorrecta para datos trimestrales y esta muestra.

## D4. Resultado primario

- Una sola definición para toda la tesis: resultado primario del Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4), y la fuente pública (MECON) no separa esas transferencias del resto de las rentas de la propiedad; la serie sin rentas es la que las excluye. En el perímetro consolidado, además, esas utilidades son un flujo interno. La serie con rentas se informa como robustez (variante "resultado primario con rentas de la propiedad").
- La versión anterior justificaba la serie con rentas como "la definición del FMI": era falso (el FMI excluye las utilidades del BCRA). Corregido.
- Máximo anual 1996-2025: 3,29% del PIB en 2004 sin rentas (definición principal); con rentas, 3,58%.

## D5. Tasa de la FED

- Tasa de fondos federales con la tasa sombra de Wu y Xia (2016) en el límite cero. En 2022T1, cuando la serie pasa de la tasa sombra a la efectiva, la variación se calcula con la tasa efectiva en ambos trimestres, para no confundir el cambio de serie con un cambio de política. Desvío de la variación trimestral en la muestra: 0,494 puntos.

## D6. Variables externas en la simulación

- El VIX y el nivel de la tasa de la FED se simulan con procesos AR(1) estimados en la muestra (coeficientes 0,703 y 0,970). Sus innovaciones históricas se remuestrean junto con los shocks estructurales, por fecha, de modo que la incertidumbre externa forma parte del abanico. La descomposición de la varianza agrega un cuarto bloque, externo (FED y VIX).

## D7. Remuestreo de shocks

- Bloques de ocho trimestres consecutivos (dos años), como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI). Conserva la autocorrelación remanente y la correlación entre variables.

## D8. Inferencia

- Estimación central con los parámetros de MCO (autovalor máximo 0,896) y 20.000 trayectorias; error de Monte Carlo 0,33 puntos.
- Intervalos de 90%: bootstrap de bloques móviles de cuatro trimestres sobre los residuos, de diseño recursivo, en el que la deuda también se regenera (Brüggemann, Jentsch y Trenkler, 2016), con percentiles de Hall (1992), que corrigen el sesgo de la distribución bootstrap respecto de la estimación puntual. Brüggemann et al. muestran además que el bootstrap salvaje no reproduce la estructura de cuarto orden de las innovaciones de la que dependen las respuestas estructurales; por eso se abandona.
- Todas las especificaciones usan los mismos números aleatorios: las diferencias entre filas no vienen del sorteo. Las identificaciones alternativas dan exactamente la misma probabilidad, como corresponde.
- La corrección de sesgo de Kilian (1998) se informa como robustez.

## D9. Identidad y métrica

- El ajuste stock-flujo del FMI (capitalización de deuda indexada, sobre todo en 2026-2027) se escala por la deuda en pesos simulada respecto de la del FMI; la inflación relativa, por la deuda en moneda extranjera. La métrica de estabilización incluye el ajuste stock-flujo, como la identidad: pb* = d_{T-1}(M_T − 1) + sf_T + ri_T. Es la definición del FMI (2021, párr. 53): el resultado primario que estabiliza la deuda en T.
- El desvío del crecimiento anual es la variación del promedio anual del nivel del PIB, no la suma de las tasas trimestrales.
- La proporción en pesos queda fija en el escenario, el mismo supuesto del FMI (2021, anexo VI, párr. 6).
- La retroalimentación se actualiza al cierre de cada año, porque la identidad del FMI es anual: dentro del año, la deuda que entra en las ecuaciones es la del cierre del año anterior.

## D10. H1a

- Criterio: el original, sin cambios: la contribución de los shocks no fiscales a la varianza de la deuda en 2035 supera a la del shock fiscal, con un intervalo de 90% que excluye el cero. Resultado: 78,3 puntos [57,3; 87,9]; se cumple en las 20 especificaciones (el menor límite inferior es 25,6, con elasticidad cíclica 0).
- Complemento sin criterio de contraste (análisis descriptivo, declarado así): con el resultado primario en su máximo anual de 1996-2025 todos los años, la probabilidad de no estabilización en 2031 es 26,1% (3,29%, sin rentas) o 24,5% (3,58%, con rentas); para llevarla al 1% que informa el FMI haría falta sumar 8,00 puntos al resultado primario del escenario en todos los años (9,4% del PIB en 2026, 10,3% en 2031). En 2035 la relación no es monótona: la probabilidad baja hasta 0,71% (+6,50) y vuelve a subir (2,91% con +10,00), porque con la deuda cerca de cero la métrica se activa con cualquier shock.
- Se elimina la versión anterior que había cambiado el criterio tras ver los resultados: ya no hace falta, y el texto lo dice en el registro de cambios del grupo, no en la tesis.

## D11. H1b

- Comparación con el mismo perímetro, punto de partida, escenario, horizonte y métrica del FMI. Criterio: el límite inferior del intervalo de 90% supera la probabilidad del FMI (1% en 2031; menos de 3% en 2035), con corrección de Bonferroni por los dos horizontes (95%).
- Resultado: 31,8% [25,2; 36,4] en 2031 y 31,0% [26,8; 35,6] en 2035; al 95%: límites inferiores 24,2 y 26,6. Se cumple en las 20 especificaciones (menor límite inferior 19,1, deuda consolidada).
- Con el procedimiento de shocks del FMI aplicado a la historia argentina 1997-2025 (impulsores anuales de la ventana), sobre el mismo perímetro: 24,1% en 2031 y un ancho de 148,4. Tampoco se reproduce el 1%: la diferencia con el FMI proviene de la distribución de shocks que este usa, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). La tesis no atribuye la brecha a una causa que no puede verificar.

## D12. H2

- Criterio sin cambios: el intervalo de 90% de la diferencia entre el escenario de la FED y el base excluye el cero, en la probabilidad y en la deuda esperada, al final del horizonte (2035), porque el efecto de una tasa más alta se acumula. 2031 se informa.
- Escenarios: (i) nivel de la tasa 0,494 puntos más alto en forma permanente desde 2026T1; (ii) repetición de la senda trimestral de 2022-2025 en 2026-2029: sube 5,25 puntos y baja 1,43, y desde 2030 queda 3,82 puntos por encima del escenario base hasta 2035.
- Resultado: (i) probabilidad 2035 +1,1 [0,2; 1,9], deuda 2035 +1,0 [0,0; 1,8]; (ii) probabilidad 2035 +9,7 [4,2; 16,0], deuda 2035 +9,0 [0,3; 16,2]. Se cumple el criterio en la especificación principal en los dos escenarios.
- Salvedades: con Bonferroni (95%) solo el efecto de la senda sobre la probabilidad sigue excluyendo el cero ([3,6; 16,8]); el del desvío estándar sobre la probabilidad ([-0,0; 2,0]) y los efectos sobre la deuda esperada ([-0,5; 2,0] y [-4,1; 17,4]) no. En las robusteces, el efecto de la senda sobre la probabilidad excluye el cero en 18 de 20 especificaciones (no en datos desde 2004 ni con corrección de Kilian); sobre la deuda, en 9 de 20. Los canales que nombra la hipótesis (riesgo soberano, tipo de cambio real, crecimiento) no se distinguen: 2 de 84 intervalos de respuesta excluyen el cero, ambos del TCRM y con signo de apreciación. El 96% del efecto de la senda sobre la deuda en 2035 es el costo directo de la deuda en dólares, que la identidad incorpora (8,6 de 9,0 puntos). Veredicto: H2 respaldada en su efecto sobre la probabilidad en el escenario de la senda de 2022-2025, que es robusto; el efecto sobre la deuda esperada y el del desvío estándar no son robustos, y el mecanismo es el costo directo, no los canales que propone la hipótesis.

## D13. Título

"Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos"

## D14. Extensión

- La tabla completa de robustez pasa al Apéndice (A.9). Resultados conserva una tabla corta.
- Antecedentes: los ejes 2, 3 y 8 se reducen a lo esencial.
