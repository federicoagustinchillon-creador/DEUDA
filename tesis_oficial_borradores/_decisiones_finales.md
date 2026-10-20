# Decisiones finales de la revisión (12 de octubre de 2026, actualizadas el 19 de octubre). Documento interno

Base de toda la reescritura. Los números salen exclusivamente de `_hoja_de_numeros.md` (generada por `codigo/modelos/hoja_de_numeros.py`) y del Apéndice (`apendice.md`, generado por `codigo/modelos/apendice_tablas.py`). Ningún número puede salir de otro lado ni de versiones anteriores del texto.

## D1. Perímetro de la especificación principal: deuda federal bruta (perímetro del FMI)

- Principal: deuda bruta del gobierno federal (Administración Central), el perímetro del análisis de sostenibilidad del FMI (2026, anexo II). Punto de partida: el stock del FMI a fines de 2025, 80,3% del PIB (cuadro 2, línea 1, que incluye intereses capitalizados, deuda no presentada al canje y reclamos por los cupones PBI). La serie propia, construida con datos del MECON, da 77,7% a fines de 2025; la diferencia son esos conceptos y la medición del PIB.
- Por qué: es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, el mismo punto de partida y el mismo escenario. La métrica no era la misma (D16). El escenario del FMI (tasa efectiva, ajuste stock-flujo, inflación relativa, necesidades de financiamiento) está construido para esa deuda.
- Extensión: deuda del sector público consolidado con el BCRA en la definición del FMI (cuadro 2, línea 5: deuda federal fuera del sector público más pasivos del BCRA), 52,1% del PIB a fines de 2025, con 68,5% en moneda extranjera (proporción en pesos 0,315). La dinámica se estima con la serie propia de deuda consolidada (Tesoro más BCRA, Letras a valor nominal). El ajuste stock-flujo y la inflación relativa del FMI se escalan por la deuda en pesos y en moneda extranjera de ese perímetro.
- El título de la tesis cambia en consecuencia (D13). La construcción de la deuda consolidada sigue siendo un objetivo y un aporte: permite estimar la dinámica de ese perímetro y compararla con la federal.

## D2. Ventana única 1996-2025 (decisión del grupo, no se negocia)

- Todo el estudio usa la ventana 1996-2025: datos, series, quiebres, figuras, descriptivos y estimación. La proyección es 2026-2035. En ningún lugar del texto puede aparecer otro período de estudio.
- La única aclaración técnica, y solo en Metodología, Datos y el Apéndice: las ecuaciones se estiman con los trimestres 1998T2-2025T4 (111 observaciones), porque la deuda federal bruta trimestral del MECON empieza en 1998T1 y entra rezagada; los trimestres anteriores son condiciones iniciales de los demás rezagos, y los órdenes hasta seis se comparan sobre esa muestra común (Lütkepohl, 2005, sec. 4.3).
- Dos series no tienen dato directo publicado en toda la ventana y se completan con empalmes documentados y validados (código: codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py; validación: Apéndice y Figura A.1):
  - EMBI 1996T1-1998T3. La serie pública diaria de J.P. Morgan para Argentina empieza el 11 de diciembre de 1998. Para antes se usa el diferencial entre la tasa de préstamos interfinancieros en dólares del BCRA (serie oficial, mensual desde octubre de 1994) y la tasa de fondos federales: durante la convertibilidad, ese costo del dólar en el sistema financiero argentino refleja el riesgo argentino. Relación estimada en la superposición 1998T4-2001T3 (12 trimestres; termina antes del corralito, que rompe ese mercado): EMBI = 550,3 + 1,171 × diferencial, R² = 0,89, correlación 0,944. Validación cruzada dejando un trimestre afuera: error típico de 102 puntos básicos, contra un desvío del EMBI de 240. Fuera de muestra (estimando con 1998T4-2000T4 y pronosticando 2001): 744, 801 y 1.033 contra 750, 973 y 1.469 observados: acierta el nivel y subestima el salto de la crisis, de modo que el empalme, si sesga, atenúa la volatilidad de 1996-1998 y vuelve conservadoras las probabilidades.
  - TCRM 1996. El índice del BCRA empieza en enero de 1997. Para 1996 se encadena hacia atrás con las variaciones del tipo de cambio real efectivo amplio del BIS (invertido, porque el BIS sube con la apreciación). Las variaciones trimestrales de ambos índices tienen una correlación de 0,92 en 1997-2025 y de 0,98 en 1997-2001. Como la estimación empieza en 1998T2, los valores de 1996 no entran en el SVARX; solo los usa la variante a la manera del FMI, para la depreciación real de 1997. El EMBI empalmado solo pesa en 1997T4-1998T3.
  - Prueba de que el resultado no depende del empalme: con datos desde 1999 (solo EMBI observado), la probabilidad de no estabilización es 29,5% [22,5; 36,7] en 2031, contra 27,7% [20,6; 34,7] con la ventana completa; H1a se mantiene (95,7 [88,9; 99,8]) y el efecto de la senda de la FED sobre la probabilidad también (18,0 [5,6; 28,3]) (Apéndice A.10).
- La base anterior tenía para el EMBI de 1993-1998 valores escritos a mano sin fuente; se eliminaron. No deben mencionarse en la tesis (sí en la revisión crítica interna).

## D2b. Reglas de consistencia de todo el texto

- Período: "1996-2025" para el estudio, "2026-2035" para la proyección. Prohibido "1999-2025", "2000-2025", "2000T3" como período (solo se admite "datos desde 1999" para nombrar la variante de robustez sin empalme, y las fechas de inicio de las fuentes en Datos).
- Riesgo país: la variable se llama EMBI. Primera mención en cada capítulo: "el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI)". Después siempre "EMBI" (no "EMBI+", no "spread", no "diferencial soberano" como nombre alternativo; "riesgo país" solo como concepto). La palabra *spread* solo puede aparecer en la definición, en cursiva.
- Identificación: siempre con el mismo nombre: "restricciones de impacto en la línea de Blanchard y Perotti (2002)" para el bloque fiscal y de actividad, con "un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto". Robustez: "dos ordenamientos de Cholesky (resultado primario primero y resultado primario último)". Toda mención de la identificación (Introducción 1.6, Metodología 4.4, Resultados, Discusión, Conclusiones, Plan) debe nombrar exactamente esto.
- Tipo de cambio: "tipo de cambio real multilateral (TCRM)" en la primera mención; después "TCRM".
- Deuda: "deuda federal bruta" (principal) y "deuda consolidada con el BCRA" (extensión). Nunca "deuda consolidada neta" ni "deuda pública" a secas cuando se refiere a una de las dos.
- FED: "tasa de política monetaria de la Reserva Federal (FED)"; la serie es la tasa de fondos federales con la tasa sombra de Wu y Xia (2016) en el límite cero.

## D3. Rezagos

- Regla: el criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si los residuos de ese orden rechazan la ausencia de autocorrelación (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no la rechaza (Lütkepohl, 2005, sec. 4.4). Regla de reserva: si ningún orden estable pasa la prueba, el orden estable no menor que el de Schwarz con el mayor p-valor.
- Resultado (versión del 19/10, con binarias presidenciales y la tasa de la FED corregida): Schwarz elige 1, cuyos residuos están autocorrelacionados (p < 0,001); ningún orden estable pasa la prueba al 5%, y se usan 2 (p = 0,031), que es también el orden que elige Hannan-Quinn. Autovalor máximo 0,776. La autocorrelación leve se declara como limitación.
- La versión anterior citaba a Ivanov y Kilian para justificar el AIC; esa cita era incorrecta para datos trimestrales y esta muestra.

## D4. Resultado primario

- Una sola definición para toda la tesis: resultado primario del Sector Público Nacional sin rentas de la propiedad. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4), y la fuente pública (MECON) no separa esas transferencias del resto de las rentas de la propiedad; la serie sin rentas es la que las excluye. En el perímetro consolidado, además, esas utilidades son un flujo interno. La serie con rentas se informa como robustez (variante "resultado primario con rentas de la propiedad").
- La versión anterior justificaba la serie con rentas como "la definición del FMI": era falso (el FMI excluye las utilidades del BCRA). Corregido.
- Máximo anual 1996-2025: 3,29% del PIB en 2004 sin rentas (definición principal); con rentas, 3,58%.

## D5. Tasa de la FED

- Tasa de fondos federales con la tasa sombra de Wu y Xia (2016) en el límite cero. En las cuatro transiciones entre las dos series (2009T1, 2016T1, 2020T2 y 2022T1), la variación se calcula con la tasa efectiva en ambos trimestres, para no confundir el cambio de serie con un cambio de política. Desvío de la variación trimestral en la muestra: 0,501 puntos.

## D6. Variables externas en la simulación

- El VIX y el nivel de la tasa de la FED se simulan con procesos AR(1) estimados en la muestra (coeficientes 0,703 y 0,972). Sus innovaciones históricas se remuestrean junto con los shocks estructurales, por fecha, de modo que la incertidumbre externa forma parte del abanico. La descomposición de la varianza agrega un cuarto bloque, externo (FED y VIX).

## D7. Remuestreo de shocks

- Bloques de ocho trimestres consecutivos (dos años), como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI). Conserva la autocorrelación remanente y la correlación entre variables.

## D8. Inferencia

- Estimación central con los parámetros de MCO (autovalor máximo 0,776) y 20.000 trayectorias; error de Monte Carlo 0,32 puntos. Intervalos con 1.000 réplicas.
- Intervalos de 90%: bootstrap de bloques móviles de cuatro trimestres sobre los residuos, de diseño recursivo, en el que la deuda también se regenera (Brüggemann, Jentsch y Trenkler, 2016), con percentiles de Hall (1992), que corrigen el sesgo de la distribución bootstrap respecto de la estimación puntual. Brüggemann et al. muestran además que el bootstrap salvaje no reproduce la estructura de cuarto orden de las innovaciones de la que dependen las respuestas estructurales; por eso se abandona.
- Todas las especificaciones usan los mismos números aleatorios: las diferencias entre filas no vienen del sorteo. Las identificaciones alternativas dan la misma estimación central de la probabilidad, como corresponde; los intervalos difieren levemente porque en cada réplica la matriz S se reestima.
- La corrección de sesgo de Kilian (1998) se informa como robustez.

## D9. Identidad y métrica

- El ajuste stock-flujo del FMI (capitalización de deuda indexada, sobre todo en 2026-2027) se escala por la deuda en pesos simulada respecto de la del FMI; la inflación relativa, por la deuda en moneda extranjera. La métrica anual incluye el ajuste stock-flujo, como la identidad: pb* = d_{T-1}(M_T − 1) + sf_T + ri_T; aplica año por año la definición del FMI (2021, párr. 53). No es la definición operativa del FMI, que se informa al lado (D16).
- El desvío del crecimiento anual es la variación del promedio anual del nivel del PIB, no la suma de las tasas trimestrales.
- La proporción en pesos queda fija en el escenario, el mismo supuesto del FMI (2021, anexo VI, párr. 6).
- La retroalimentación se actualiza al cierre de cada año, porque la identidad del FMI es anual: dentro del año, la deuda que entra en las ecuaciones es la del cierre del año anterior.

## D10. H1a

- Criterio original: la contribución de los shocks no fiscales a la varianza de la deuda en 2035 supera a la del shock fiscal, con un intervalo de 90% que excluye el cero. Por la revisión del equipo del 15/10 (punto B1) se agrega una segunda condición, que contrasta lo que la hipótesis afirma: con el resultado primario de todos los años desplazado en la misma magnitud hasta que el de 2031 alcanza su máximo anual de 1996-2025, la probabilidad de no estabilización en 2031 sigue por encima del 1% del FMI. H1a se acepta si se cumplen las dos.
- Resultado: (i) 96,8 puntos [90,8; 99,8]; se cumple en las 20 especificaciones en que se informa (menor límite inferior 67,3, sin binarias presidenciales, con 77,9). Como las participaciones suman 100, equivale a que el bloque fiscal explique menos de la mitad. (ii) Con la métrica anual, 23,0% con el máximo sin rentas (3,29%) y 21,6% con el máximo con rentas (3,58%); para llevar la probabilidad al 1% hay que sumar 7,25 puntos al resultado primario del escenario en todos los años (8,65% del PIB en 2026, 9,55% en 2031). En 2035 la relación no es monótona: la probabilidad baja hasta 0,12% (+6,25) y vuelve a subir (1,99% con +10,00). Con la definición operativa del FMI, (ii) no se cumple: 0,9% con el máximo histórico (D16).

## D11. H1b

- Comparación con el mismo perímetro, punto de partida, escenario y horizonte del FMI, con dos métricas (D16). Criterio: el límite inferior del intervalo de 90% supera la probabilidad del FMI (1% en 2031; menos de 3% en 2035), con corrección de Bonferroni por los dos horizontes (95%).
- Resultado con la métrica anual: 27,7% [20,6; 34,7] en 2031 y 29,0% [25,0; 36,1] en 2035; al 95%: límites inferiores 19,0 y 24,1. Se cumple en las 21 especificaciones (menor límite inferior 16,2, tres rezagos). Con la definición operativa del FMI: 3,1% [0,0; 6,3] y 5,1% [0,0; 10,2]; no se cumple (D16).
- Con el procedimiento de shocks del FMI aplicado a la historia argentina 1997-2025 (impulsores anuales de la ventana), sobre el mismo perímetro: 24,1% en 2031 con la métrica anual (29,1% con la definición operativa) y un ancho de 148,4. Tampoco se reproduce el 1%: la diferencia con el FMI proviene de la distribución de shocks que este usa, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). La tesis no atribuye la brecha a una causa que no puede verificar.

## D12. H2

- Criterio: el intervalo de 90% de la diferencia entre el escenario de la FED y el base excluye el cero, en la probabilidad y en la deuda esperada, en 2035, porque el efecto de una tasa más alta se acumula; 2031 se informa. Si se cumple en una medida o en un escenario y no en los otros, H2 se declara parcialmente respaldada. La hipótesis se refiere al efecto total; los canales se examinan aparte.
- Escenarios: (i) nivel de la tasa 0,501 puntos más alto en forma permanente desde 2026T1; (ii) repetición de la senda trimestral de 2022-2025 en 2026-2029: sube 5,25 puntos y baja 1,43, y desde 2030 queda 3,82 puntos por encima del escenario base hasta 2035.
- Resultado: (i) probabilidad 2035 +1,9 [0,3; 3,2], deuda 2035 +2,0 [0,4; 3,2]; (ii) probabilidad 2035 +18,4 [6,3; 29,1], deuda 2035 +19,3 [-0,3; 31,3].
- Salvedades: con Bonferroni (95%) solo el efecto de la senda sobre la probabilidad sigue excluyendo el cero ([4,1; 30,8]). En las robusteces, el efecto de la senda sobre la probabilidad excluye el cero en 20 de 21 especificaciones (no con datos desde 2004); sobre la deuda, lo excluye en 11, lo incluye en 7, el límite inferior es 0,00 en una y no se informa en dos. Con la definición operativa del FMI, la senda eleva la probabilidad de 2035 en 17,1 [0,6; 32,6]. El 77% del efecto de la senda sobre la deuda en 2035 es el costo directo de la deuda en dólares (14,8 de 19,3 puntos). De 84 intervalos de respuesta a la FED, 11 excluyen el cero, entre ellos tres del EMBI de cuatro a seis trimestres después. Sin binarias presidenciales el efecto de la senda es de 9,7 puntos de probabilidad. Veredicto: H2 parcialmente respaldada.

## D13. Título

"Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos"

## D14. Extensión

- La tabla completa de robustez pasa al Apéndice (A.10). Resultados conserva una tabla corta.
- Antecedentes: los ejes 2, 3 y 8 se reducen a lo esencial.

## D15. Binarias presidenciales y deuda consolidada desde 2002

- Siete binarias por mandato presidencial en la especificación principal, con Menem como referencia (2001T4 se asigna a Duhalde); la variante sin ellas se informa como robustez. Pedido del equipo (A5). Las pruebas de Wald y de razón de verosimilitud rechazan que no importen (p < 0,001 en el sistema).
- Consecuencia que hay que validar: sin ellas el efecto de la senda de la FED es la mitad (9,7 puntos de probabilidad contra 18,4) y la diferencia no fiscal menos fiscal baja de 96,8 a 77,9. H1a y H1b no cambian.
- La deuda consolidada se estima desde 2002 (A4), porque antes la consolidación no tiene fundamento en el criterio del FMI.

## D16. Métrica de no estabilización (19/10; decidida el 20/10)

- Problema detectado en la revisión independiente del 19/10: la tesis decía usar "la misma métrica" que el FMI, y no era así. La métrica de la tesis compara cada año el resultado primario previsto con el que estabiliza la deuda ese año, con la valuación de la deuda en moneda extranjera y el ajuste stock-flujo: equivale a que la deuda suba en ese año. La definición operativa del FMI (FMI, 2022, recuadro 3) promedia las variables a lo largo de la trayectoria y deja afuera el tipo de cambio real y el ajuste stock-flujo. Es la que produce el 1% y el menos de 3% con que se compara H1b.
- Qué se hizo: el código calcula las dos (más la lectura literal del recuadro 3, que promedia también el escenario base) con las 1.000 réplicas, y todo el texto se reescribió para informarlas con el mismo peso, sin elegir una como única.
- Resultados con la definición operativa del FMI: 3,1% [0,0; 6,3] en 2031 y 5,1% [0,0; 10,2] en 2035; con Bonferroni, límites inferiores negativos. El límite inferior supera la cifra del FMI solo en 2 de 21 especificaciones (consolidada, 11,0 [2,7; 20,2]; canal de tasas en pesos, 9,0 [2,7; 17,0]). Lectura literal: 0,0% y 0,9%. Con *shocks* a la manera del FMI y su definición: 29,1% y 19,1%. Suficiencia: con el máximo histórico, 0,9%; alcanza un desplazamiento de 1,00 punto. Senda de la FED: +17,1 [0,6; 32,6] en 2035, Bonferroni [-3,6; 33,6].
- Veredictos: H1b respaldada con la métrica anual y no respaldada con la definición del FMI. H1a: la condición (i) no depende de la métrica y se cumple; la (ii) se cumple con la anual y no con la del FMI. H2 parcialmente respaldada con las dos.
- **Opciones que se evaluaron:** (a) dejar las dos con el mismo peso, como está ahora; (b) definición del FMI como principal: H1b y H1a (ii) pasan a no respaldadas, y la conclusión es que, con la métrica del FMI, la dinámica histórica estimada da una probabilidad del mismo orden que la del organismo; (c) métrica anual como principal: hay que justificar por qué es mejor que la del FMI (riesgo cambiario año por año con 57,8% de la deuda en moneda extranjera) y presentar la del FMI como robustez que no se cumple. La opción (a) es la más honesta con lo que hay; la (b) es la más fácil de defender ante un jurado que conozca el marco del FMI. Cualquiera de las tres exige ajustar el resumen, 6.4, 7.1 y las conclusiones; el resto del texto ya informa las dos.
- **Decisión (20/10, Santiago): opción (b).** La definición operativa del FMI decide H1b y la condición (ii) de H1a, porque las cifras de comparación salen de ella y H1b pide comparar magnitudes equivalentes (verificado contra FMI, 2022, recuadro 3: variables promediadas en la trayectoria, sin variación del tipo de cambio real ni ajuste stock-flujo). Veredictos: H1a no respaldada (se cumple (i), no (ii)); H1b no respaldada; H2 parcialmente respaldada. La métrica anual queda como complemento: mide el riesgo de valuación anual de la deuda en moneda extranjera que la definición del FMI excluye. Se ajustaron resumen, introducción, metodología (4.6 y Tabla 4.4), resultados (6.3, 6.4 y Tabla 6.6, con una columna de la definición del FMI), discusión (7.1 y 7.3) y conclusiones.
