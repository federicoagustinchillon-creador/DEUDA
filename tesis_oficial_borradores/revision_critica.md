% Revisión crítica de la tesis y del plan de labor: registro y resolución

# Para qué es este documento

Registra la revisión adversarial de la tesis y cómo se resolvió cada punto en la versión del modelo del 12 de octubre de 2026, reestimada el 17 de octubre con la ventana 1996-2025. La sección 5 registra la revisión posterior de un compañero del grupo y la sección 6, un error propio detectado en la lectura final. La revisión la hicieron tres evaluadores con el encargo explícito de buscar motivos para desaprobar: uno sobre econometría y método, otro sobre datos y escenario, y otro sobre criterios académicos y de la cátedra de Metodología. Cada punto se verificó contra el código, los datos y los resultados. Las decisiones que resolvieron cada crítica están numeradas de D1 a D14 en el documento de decisiones finales, y los números salen de la hoja de números y del Apéndice.

Cada crítica tiene uno de dos estados:

- **Resuelto:** se corrigió en el modelo o en el texto; se indica la decisión y el resultado.
- **Limitación declarada:** no tiene solución dentro del alcance de la tesis; se indica dónde se declara.

Lo único que queda abierto es la validación del grupo de D1 y D13 y el recorte a unas 60 páginas, si todavía hace falta (sección 7).

# 1. Problemas de fondo

## 1.1 Los criterios de H1a y de H2 se habían definido después de la primera estimación

**Crítica.** El criterio original de H1a era la descomposición de la varianza. En la versión anterior no se cumplía y se reemplazó por el de suficiencia del superávit el mismo día. Un jurado podía leerlo como acomodar la prueba al resultado.

**Estado: Resuelto (D10 y D12).** H1a vuelve a su criterio original: la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del *shock* fiscal, con un intervalo de 90% que excluye el cero. Resultado: 78,3 puntos [57,3; 87,9], y se cumple en las 20 especificaciones (menor límite inferior: 25,6). La suficiencia del superávit queda como análisis descriptivo, sin criterio de contraste. H2 conserva su criterio, con 2035 como horizonte porque el efecto de una tasa más alta se acumula. Los dos tamaños del *shock* de la FED tienen una justificación externa a los resultados: un desvío estándar y la repetición del episodio de 2022-2025.

## 1.2 La comparación con el FMI (H1b) no estaba validada

**Crítica.** La tesis comparaba una probabilidad calculada sobre la deuda consolidada con el BCRA con la del FMI para la deuda federal bruta, con otro punto de partida. El procedimiento de *shocks* del FMI aplicado a los datos de la tesis no reproducía el 1%. Un evaluador podía sostener que H1b se cumplía casi por construcción y que no era una hipótesis en sentido estricto.

**Estado: Resuelto (D1 y D11), con una limitación declarada.** H1b compara ahora con el mismo perímetro, el mismo punto de partida (80,3% del PIB), el mismo escenario, el mismo horizonte y la misma métrica del FMI. Resultado: 31,8% [25,2; 36,4] en 2031 y 31,0% [26,8; 35,6] en 2035; con Bonferroni, límites inferiores de 24,2 y 26,6. Se cumple en las 20 especificaciones. La hipótesis se presenta con el mismo esquema que las otras (unidad de análisis, variables, relación esperada y criterio de contraste). El argumento de que se cumple por construcción no se sostiene: el abanico del FMI es más ancho que el nuestro (71,5 puntos contra 46,6 en 2031) y aun así da 1%.

**Limitación declarada (Capítulo 7 y Guía de defensa).** Con el procedimiento de *shocks* del FMI aplicado a la historia argentina de la ventana, sobre el mismo perímetro, se obtiene 24,1% en 2031 y un ancho de 148,4: tampoco se reproduce el 1%. La diferencia proviene de la distribución de *shocks* que usa el FMI, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). La tesis no atribuye la brecha a una causa que no puede verificar.

## 1.3 El escenario base del FMI se aplicaba a otra deuda

**Crítica.** El escenario del FMI está construido para la deuda federal bruta y se aplicaba a la deuda consolidada con el BCRA. El ajuste *stock*-flujo se sumaba sin escalar, la métrica de estabilización lo omitía y la proporción en pesos no correspondía al perímetro.

**Estado: Resuelto (D1 y D9).** El escenario se aplica a la deuda para la que fue construido, y la identidad reproduce la senda del FMI con un desvío máximo de 0,12 puntos. El ajuste *stock*-flujo se escala por la deuda en pesos simulada y la inflación relativa por la deuda en moneda extranjera. La métrica incluye el ajuste *stock*-flujo, como la identidad (FMI, 2021, párr. 53). La proporción en pesos es la de cada perímetro: 0,422 en la federal y 0,315 en la consolidada.

**Limitación declarada (Capítulo 7).** La extensión consolidada usa el escenario del FMI con los flujos escalados por la deuda en pesos y en moneda extranjera de ese perímetro, porque el FMI no publica un escenario completo para la deuda consolidada.

## 1.4 El título prometía algo que la tesis no mide

**Crítica.** "Solvencia intertemporal" y "post-2025" prometían algo más amplio que lo que se mide.

**Estado: Resuelto (D13), pendiente de validación del grupo.** Título nuevo: "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos".

## 1.5 El área de vacancia se debilitaba con los propios resultados

**Crítica.** La vacancia se apoyaba en el perímetro consolidado, en la identificación y en el *shock* de la FED, y los resultados anteriores debilitaban los tres. Algunas afirmaciones de ausencia eran exageradas.

**Estado: Resuelto (D1).** La vacancia se formula como "en la literatura revisada no se encontró" y reconoce los trabajos previos. Los tres aportes quedan así: una probabilidad con *shocks* identificados comparable con la del FMI (H1b se cumple con el mismo perímetro); la traducción del *shock* de la FED en un cambio de esa probabilidad (+9,7 puntos en 2035 [4,2; 16,0] con la senda de 2022-2025); y la estimación de la dinámica de la deuda consolidada, que se compara con la federal. La tesis no presenta la identificación como un aporte para la probabilidad, porque no la cambia por construcción.

# 2. Problemas graves de método

## 2.1 La estimación central estaba al borde de una raíz unitaria

**Crítica.** La corrección de sesgo llevaba el autovalor máximo a 0,9998, y las réplicas usaban una corrección menor, con intervalos descentrados.

**Estado: Resuelto (D8).** La estimación central usa los parámetros de MCO, con autovalor máximo 0,896; la mediana de las réplicas es 0,842. Los intervalos son percentiles de Hall (1992), que corrigen el sesgo de la distribución *bootstrap* respecto de la estimación puntual. La corrección de Kilian (1998) queda como robustez: 30,1% en 2031.

## 2.2 La regla de rezagos no tenía respaldo

**Crítica.** "El mayor orden estable que no supera al del AIC" no tenía fuente, y la cita de Ivanov y Kilian (2005) para el AIC era incorrecta para datos trimestrales y esta muestra.

**Estado: Resuelto (D3).** Regla: el criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1 (p = 0,000); se usan 2 (p = 0,056), el mismo orden que elige Hannan-Quinn. Con 1 y 3 rezagos, la probabilidad en 2031 es 31,4% y 30,0%.

## 2.3 Autocorrelación residual con remuestreo independiente

**Crítica.** Los residuos estaban autocorrelacionados, la simulación remuestreaba los *shocks* como independientes y el *bootstrap* salvaje se usaba sin heterocedasticidad condicional que lo justificara.

**Estado: Resuelto (D3, D7 y D8).** Con 2 rezagos los residuos no rechazan la ausencia de autocorrelación (p = 0,056). La simulación remuestrea bloques de ocho trimestres, como los bloques de dos años del abanico del FMI. La inferencia usa un *bootstrap* de bloques móviles de cuatro trimestres (Brüggemann et al., 2016). El *bootstrap* salvaje se abandonó, porque no reproduce la estructura de cuarto orden de las innovaciones.

## 2.4 H2 cumplía su criterio solo en parte y su mecanismo no aparecía

**Crítica.** El efecto sobre la deuda esperada no excluía el cero, no resistía Bonferroni y los canales que nombra la hipótesis no se distinguían.

**Estado: Resuelto en el criterio (D12), con limitaciones declaradas (Capítulos 6 y 7).** En la especificación principal se cumple el criterio en los dos escenarios y en las dos medidas: senda de 2022-2025, +9,7 puntos de probabilidad en 2035 [4,2; 16,0] y +9,0 de deuda [0,3; 16,2]; nivel 0,494 puntos más alto, +1,1 [0,2; 1,9] y +1,0 [0,0; 1,8]. Lo que sigue débil se declara:

- con Bonferroni (95%), solo el efecto de la senda sobre la probabilidad sigue excluyendo el cero ([3,6; 16,8]); el del desvío estándar sobre la probabilidad ([-0,0; 2,0]) y los efectos sobre la deuda esperada ([-0,5; 2,0] y [-4,1; 17,4]) lo incluyen;
- en las robusteces, el efecto de la senda sobre la probabilidad excluye el cero en 18 de 20 especificaciones (no con datos desde 2004 ni con la corrección de Kilian) y sobre la deuda en 9 de 20;
- 2 de 84 intervalos de respuesta excluyen el cero, los dos del TCRM y con signo de apreciación;
- el 96% del efecto de la senda sobre la deuda en 2035 es el costo directo de la deuda en dólares (8,6 de 9,0 puntos).

Veredicto de la tesis: H2 respaldada en el efecto de la senda de 2022-2025 sobre la probabilidad, que es robusto; el efecto sobre la deuda esperada y el del desvío estándar no son robustos, y el mecanismo es el costo directo de la deuda en dólares.

## 2.5 El contraste de suficiencia estaba mal descripto

**Crítica.** El superávit necesario se informaba para un año cuando el desplazamiento era de todos, el máximo histórico incluía rentas sin decirlo y la métrica no era monótona en 2035.

**Estado: Resuelto (D10).** La suficiencia es ahora un complemento descriptivo. Con el resultado primario en su máximo anual de 1996-2025 (3,29% del PIB en 2004, sin rentas, la definición principal) todos los años, la probabilidad en 2031 es 26,1% (24,5% con el máximo con rentas, 3,58%). Para llevarla al 1% haría falta sumar 8,00 puntos en todos los años (9,4% del PIB en 2026 y 10,3% en 2031). En 2035 la relación no es monótona: la probabilidad baja hasta 0,71% (+6,50) y vuelve a subir a 2,91% (+10,00), porque con la deuda cerca de cero la métrica se activa con cualquier *shock*. La tesis lo dice.

## 2.6 La reacción fiscal se interpretaba como si fuera anual

**Crítica.** El coeficiente de impacto es trimestral y el multiplicador de largo plazo no tenía intervalo.

**Estado: Resuelto.** Coeficiente de impacto 0,0576 [0,0220; 0,0822] y multiplicador de largo plazo 0,199 [0,112; 0,328], los dos con intervalo de Hall.

## 2.7 El abanico se angostaba de manera artificial

**Crítica.** El VIX y la FED quedaban fijos en la simulación, y las binarias de quiebre se eligieron con la serie de deuda.

**Estado: Resuelto en lo primero (D6); lo segundo es una limitación declarada (Apéndice A.3 y Capítulo 7).** El VIX y el nivel de la tasa de la FED se simulan con procesos AR(1) (0,703 y 0,970), con sus innovaciones remuestreadas junto con los *shocks* estructurales; el bloque externo explica 44,9% de la varianza de la deuda en 2035. Las fechas de quiebre (2001T4, 2006T2, 2018T1) siguen estimadas sobre la deuda. Sin esas binarias, la probabilidad en 2031 es 30,5% y el ancho del abanico, 55,2.

## 2.8 El resultado primario y la deuda tenían perímetros distintos

**Crítica.** El resultado primario incluía las utilidades del BCRA, que en un perímetro consolidado son un flujo interno.

**Estado: Resuelto (D4).** Una sola definición para los dos perímetros: el resultado primario del Sector Público Nacional sin rentas de la propiedad, que deja afuera las utilidades del BCRA, como el FMI (FMI, 2026, cuadro 1, nota 4). La serie con rentas se informa como robustez. La primera corrección de este punto tenía una justificación falsa para la deuda federal; ver la sección 6.

## 2.9 La identificación no afectaba la probabilidad principal

**Crítica.** Las diferencias entre las filas de identificación venían del sorteo de Monte Carlo.

**Estado: Resuelto (D8).** Todas las especificaciones usan los mismos números aleatorios, y las identificaciones alternativas dan exactamente la misma probabilidad, como corresponde. La identificación sigue siendo necesaria para repartir la varianza por bloque, que es el criterio de H1a, y para definir el *shock* fiscal. Con los dos ordenamientos de Cholesky de robustez el reparto cambia (60,7 y 91,9 puntos de diferencia no fiscal menos fiscal), y el criterio de H1a se cumple en todas las variantes.

# 3. Problemas de datos

## 3.1 Tenencias del FGS

**Crítica.** La deuda consolidada de la tesis no descontaba las tenencias del FGS y quedaba por encima de la del FMI.

**Estado: Limitación declarada (Capítulos 5 y 7).** La especificación principal es la deuda federal bruta, que no se ve afectada. La simulación de la extensión consolidada parte del *stock* del FMI (52,1% del PIB), que sí descuenta el FGS. La serie histórica consolidada con la que se estima la dinámica no lo descuenta. Los informes del FGS tienen que bajarse a mano (ver Seguimiento de tareas).

## 3.2 El EMBI anterior a 1999 estaba escrito a mano

**Crítica.** La base anterior tenía valores del EMBI de 1993-1998 escritos a mano, sin fuente.

**Estado: Resuelto (D2).** Esos valores se eliminaron. Desde diciembre de 1998 el EMBI se toma de la serie diaria que publica Ámbito Financiero, como promedio trimestral. Para 1996T1-1998T3 se usa un empalme con series oficiales: la tasa de préstamos interfinancieros en dólares del BCRA menos la tasa de fondos federales, con la relación EMBI = 550,3 + 1,171 × diferencial estimada en la superposición 1998T4-2001T3 (R² = 0,89). La validación cruzada dejando un trimestre afuera da un error típico de 102 puntos básicos, contra un desvío del EMBI de 240, y el pronóstico fuera de muestra de 2001 acierta el nivel y subestima el salto de la crisis. Con datos desde 1999, solo con el EMBI observado, la probabilidad en 2031 es 32,4% [26,6; 37,0], y H1a y H2 no cambian (Apéndice A.9).

## 3.3 Otras cuestiones de datos

- **TCRM de 1996 sin método documentado.** Resuelto (D2): se encadena hacia atrás con las variaciones del tipo de cambio real efectivo amplio del BIS, invertido; las variaciones trimestrales de los dos índices tienen una correlación de 0,92 en el período común y de 0,98 en 1997-2001.
- **Muestra informada con números distintos en distintos documentos.** Resuelto (D2): ventana 1996-2025 en todos los documentos; las ecuaciones se estiman con 1998T2-2025T4, 111 trimestres (ver también 5.1).
- **Salto de la tasa de la FED en 2022T1.** Resuelto (D5): la variación de ese trimestre se calcula con la tasa efectiva en los dos trimestres. El desvío de la variación trimestral queda en 0,494 puntos.
- **Cuadro de comparación con el FMI con dos ediciones mezcladas.** Resuelto (D1): los *stocks* de partida salen del informe de 2026 (cuadro 2).
- **Valor nominal de las Letras.** Limitación declarada (Capítulo 5): afecta solo la serie consolidada de la extensión, donde una parte de los trimestres se reconstruye o se interpola.
- **Empalme del PIB de 1999-2003.** Limitación declarada (Capítulo 5). El empalme afecta el nivel y no las tasas de crecimiento; la variante con datos desde 2004 da 31,6% en 2031.
- **Tipo de cambio de fin de período de 2024 y 2025.** Limitación menor: solo afecta la serie histórica propia, porque la simulación parte del *stock* del FMI. No se verificó contra la Comunicación A 3500.
- **Fuente del VIX.** Resuelto en la versión anterior.

# 4. Problemas de forma y de criterio académico

- **Hipótesis con esquemas distintos.** Resuelto: unidad, variables, relación esperada y criterio para las tres, en el plan y en la tesis.
- **Matriz de datos del plan.** Resuelto: separa la probabilidad simulada de las variables observadas.
- **Viabilidad del plan.** Resuelto: el EMBI es de J.P. Morgan y se toma de la serie publicada por Ámbito Financiero desde diciembre de 1998, con el empalme para 1996T1-1998T3.
- **Plan de labor desactualizado.** Resuelto: el plan usa el título de D13, el perímetro de D1, la ventana de D2, la regla de rezagos de D3 y los criterios originales, y conserva el formato de la cátedra.
- **Antecedentes como catálogo.** Resuelto (D14): los ejes 2, 3 y 8 se redujeron a lo esencial.
- **Marco teórico.** Resuelto: no cita resultados propios ni repite Antecedentes.
- **Términos en inglés sin cursiva, siglas sin definir y registro coloquial.** Resuelto.
- **Tablas y figuras.** Resuelto: la tabla completa de robustez pasó al Apéndice (A.9) y Resultados conserva una tabla corta (D14).
- **Referencias en formato APA.** Resuelto en lo verificable; se agregan Brüggemann et al. (2016) y Hall (1992).
- **Carátula y resumen.** Resueltos en la versión anterior.
- **Extensión.** Pendiente de verificar con el texto reescrito (sección 6).

# 5. Revisión de un compañero del grupo (octubre de 2026)

Después de la reescritura, un compañero leyó la tesis y los documentos del grupo y encontró cinco inconsistencias. Las cinco se verificaron y se resolvieron en la versión del 17 de octubre de 2026, con el modelo reestimado sobre la ventana 1996-2025.

## 5.1 El período de estudio no era el mismo en todos los documentos

**Crítica.** Unos documentos decían que el estudio empezaba en 1996, otros en 1999 y otros en 2000, y el plan de labor fechaba la estimación en otro período que los capítulos.

**Estado: Resuelto (D2 y D2b).** La ventana del estudio es una sola, 1996-2025, y la proyección es 2026-2035. La única aclaración técnica, en Metodología, Datos y el Apéndice, es que las ecuaciones se estiman con 1998T2-2025T4 (111 trimestres), porque los primeros trimestres de la ventana son condiciones iniciales de los rezagos. Las dos series sin dato directo en toda la ventana se completan con empalmes validados (Apéndice A.2 y Figura A.1). El EMBI de 1996T1-1998T3 sale de la tasa de préstamos interfinancieros en dólares del BCRA menos la tasa de fondos federales, con la relación estimada en la superposición 1998T4-2001T3 (R² = 0,89; error típico de 102 puntos básicos dejando un trimestre afuera; pronóstico fuera de muestra de 2001 que acierta el nivel). El TCRM de 1996 se encadena con el tipo de cambio real efectivo del BIS (correlación de las variaciones trimestrales de 0,92). Con datos desde 1999, sin empalme, la probabilidad de no estabilización en 2031 es 32,4% contra 31,8% con la ventana completa. El control automático `verificar_consistencia.py` falla si algún capítulo o el plan de labor nombra otro período.

## 5.2 El riesgo país tenía varios nombres

**Crítica.** La misma variable aparecía como EMBI, con el nombre del índice anterior de J.P. Morgan (con el signo más) y con el término en inglés para el diferencial, sin cursiva.

**Estado: Resuelto (D2b).** En la primera mención de cada capítulo: "el riesgo país, medido por el diferencial del índice EMBI de J.P. Morgan para Argentina (EMBI)"; después, siempre EMBI. "Riesgo país" queda solo como concepto, y el término en inglés solo puede aparecer en la definición, en cursiva. El control automático detecta los nombres alternativos.

## 5.3 La identificación se nombraba de distintas maneras

**Crítica.** Según el capítulo, la identificación aparecía como de Blanchard y Perotti, como restricciones de impacto o como Cholesky, sin que quedara claro cuál era la principal.

**Estado: Resuelto (D2b).** Toda mención usa el mismo nombre: restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto. La robustez son dos ordenamientos de Cholesky (resultado primario primero y resultado primario último). El control automático marca toda línea que nombre a Cholesky sin decir que es robustez.

## 5.4 Había números de versiones anteriores

**Crítica.** Algunos documentos conservaban cifras de la estimación anterior (por ejemplo, 32,8% de no estabilización en 2031 y 19 especificaciones de robustez).

**Estado: Resuelto.** El modelo se reestimó con la ventana 1996-2025 y todos los números salen de la hoja de números (`codigo/modelos/hoja_de_numeros.py`) y del Apéndice (`codigo/modelos/apendice_tablas.py`). La probabilidad principal en 2031 es 31,8% [25,2; 36,4], H1a da 78,3 puntos [57,3; 87,9] y hay 20 especificaciones. El 32,8% ya no aparece en ningún documento: era una cifra de la estimación anterior. El control automático marca todo número con decimales que no esté en la hoja de números, el Apéndice o las decisiones finales.

## 5.5 Los cambios no se veían en GitHub

**Crítica.** Los *commits* no aparecían en la rama por defecto del repositorio, de modo que el grupo veía una versión vieja.

**Estado: Resuelto.** El trabajo estaba en la rama `var-restringido`. La rama se fusiona con `main`, que es la que muestra GitHub por defecto.

# 6. Error propio detectado en la lectura final

## 6.1 La justificación del resultado primario con rentas era falsa

**Crítica.** Error propio detectado en la lectura final: la justificación del resultado primario con rentas era falsa (el FMI excluye las utilidades del BCRA); se corrigió a una definición única sin rentas; los resultados casi no cambian. La versión anterior usaba para la deuda federal el resultado primario con rentas de la propiedad y lo presentaba como la definición del FMI para el gobierno federal, apoyada en la coincidencia con el resultado primario del FMI en 2024 y 2025. El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4), de modo que esa coincidencia no probaba que la definición fuera la misma.

**Estado: Resuelto (D4).** Una sola definición para toda la tesis: el resultado primario del Sector Público Nacional sin rentas de la propiedad. La fuente pública del MECON no separa las transferencias de utilidades del BCRA del resto de las rentas de la propiedad, y la serie sin rentas es la que las deja afuera. En el perímetro consolidado esas utilidades también son un flujo interno. La serie con rentas queda como robustez. Se eliminaron del texto la idea de que la definición depende del perímetro y las comparaciones con el FMI de 2024 y 2025. Cambio en los resultados de la especificación principal, de la versión con rentas a la versión sin rentas:

| Medida | Con rentas (versión anterior) | Sin rentas (versión actual) |
|---|---|---|
| No estabilización 2031 (%) | 32,0 [25,7; 35,9] | 31,8 [25,2; 36,4] |
| No estabilización 2035 (%) | 31,3 [27,4; 36,2] | 31,0 [26,8; 35,6] |
| H1a, no fiscal menos fiscal (puntos) | 85,0 [70,3; 93,9] | 78,3 [57,3; 87,9] |
| Senda de la FED, probabilidad 2035 (pp) | 11,3 [5,3; 19,0] | 9,7 [4,2; 16,0] |
| Senda de la FED, deuda 2035 (pp del PIB) | 11,7 [2,1; 21,2] | 9,0 [0,3; 16,2] |
| Máximo histórico del resultado primario (% del PIB) y probabilidad 2031 con ese máximo | 3,58 y 24,5% | 3,29 y 26,1% |

Las conclusiones de H1a, H1b y H2 no cambian: H1a y H1b se cumplen en las 20 especificaciones y H2 se respalda en el efecto de la senda sobre la probabilidad. Lo que sí cambia es la robustez del efecto sobre la deuda esperada, que ahora excluye el cero en 9 de 20 especificaciones, y la proporción del costo directo en ese efecto, que pasa a 96% (8,6 de 9,0 puntos). Los números de la columna con rentas figuran solo en este registro.

# 7. Qué queda abierto

1. Validación del grupo de D1 (deuda federal bruta como especificación principal y deuda consolidada con el BCRA como extensión).
2. Validación del grupo de D13 (título).
3. Recorte a unas 60 páginas, si después de la reescritura todavía hace falta.

La ventana 1996-2025 (D2) ya no está abierta: es una decisión del grupo. Las limitaciones declaradas no están pendientes: son límites del alcance de la tesis y se informan en el texto.
