% Revisión crítica de la tesis y del plan de labor: registro y resolución

# Para qué es este documento

Registra la revisión adversarial de la tesis y cómo se resolvió cada punto en la versión del modelo del 12 de octubre de 2026. La revisión la hicieron tres evaluadores con el encargo explícito de buscar motivos para desaprobar: uno sobre econometría y método, otro sobre datos y escenario, y otro sobre criterios académicos y de la cátedra de Metodología. Cada punto se verificó contra el código, los datos y los resultados. Las decisiones que resolvieron cada crítica están numeradas de D1 a D14 en el documento de decisiones finales, y los números salen de la hoja de números y del Apéndice.

Cada crítica tiene uno de dos estados:

- **Resuelto:** se corrigió en el modelo o en el texto; se indica la decisión y el resultado.
- **Limitación declarada:** no tiene solución dentro del alcance de la tesis; se indica dónde se declara.

Lo único que queda abierto es la validación del grupo de D1, D2 y D13 y el recorte a unas 60 páginas, si todavía hace falta (sección 5).

# 1. Problemas de fondo

## 1.1 Los criterios de H1a y de H2 se habían definido después de la primera estimación

**Crítica.** El criterio original de H1a era la descomposición de la varianza. En la versión anterior no se cumplía y se reemplazó por el de suficiencia del superávit el mismo día. Un jurado podía leerlo como acomodar la prueba al resultado.

**Estado: Resuelto (D10 y D12).** H1a vuelve a su criterio original: la contribución de los *shocks* no fiscales a la varianza de la deuda en 2035 supera a la del *shock* fiscal, con un intervalo de 90% que excluye el cero. Resultado: 82,6 puntos [65,8; 92,4], y se cumple en las 19 especificaciones (menor límite inferior: 31,4). La suficiencia del superávit queda como análisis descriptivo, sin criterio de contraste. H2 conserva su criterio, con 2035 como horizonte porque el efecto de una tasa más alta se acumula. Los dos tamaños del *shock* de la FED tienen una justificación externa a los resultados: un desvío estándar y la repetición del episodio de 2022-2025.

## 1.2 La comparación con el FMI (H1b) no estaba validada

**Crítica.** La tesis comparaba una probabilidad calculada sobre la deuda consolidada neta con la del FMI para la deuda federal bruta, con otro punto de partida. El procedimiento de *shocks* del FMI aplicado a los datos de la tesis no reproducía el 1%. Un evaluador podía sostener que H1b se cumplía casi por construcción y que no era una hipótesis en sentido estricto.

**Estado: Resuelto (D1 y D11), con una limitación declarada.** H1b compara ahora con el mismo perímetro, el mismo punto de partida (80,3% del PIB), el mismo escenario, el mismo horizonte y la misma métrica del FMI. Resultado: 32,8% [26,8; 37,9] en 2031 y 31,3% [27,0; 35,3] en 2035; con Bonferroni, límites inferiores de 26,3 y 26,4. Se cumple en las 19 especificaciones. La hipótesis se presenta con el mismo esquema que las otras (unidad de análisis, variables, relación esperada y criterio de contraste). El argumento de que se cumple por construcción no se sostiene: el abanico del FMI es más ancho que el nuestro (71,5 puntos contra 48,3 en 2031) y aun así da 1%.

**Limitación declarada (Capítulo 7 y Guía de defensa).** Con el procedimiento de *shocks* del FMI aplicado a la historia argentina 2000-2025, sobre el mismo perímetro, se obtiene 16,6% en 2031 y un ancho de 151,1: tampoco se reproduce el 1%. La diferencia proviene de la distribución de *shocks* que usa el FMI, que no publica. El propio FMI reconoce que sus abanicos subestiman la incertidumbre porque no incluyen retroalimentación y fijan la composición por monedas (FMI, 2021, anexo VI, párr. 6). La tesis no atribuye la brecha a una causa que no puede verificar.

## 1.3 El escenario base del FMI se aplicaba a otra deuda

**Crítica.** El escenario del FMI está construido para la deuda federal bruta y se aplicaba a la consolidada neta. El ajuste *stock*-flujo se sumaba sin escalar, la métrica de estabilización lo omitía y la proporción en pesos no correspondía al perímetro.

**Estado: Resuelto (D1 y D9).** El escenario se aplica a la deuda para la que fue construido, y la identidad reproduce la senda del FMI con un desvío máximo de 0,12 puntos. El ajuste *stock*-flujo se escala por la deuda en pesos simulada y la inflación relativa por la deuda en moneda extranjera. La métrica incluye el ajuste *stock*-flujo, como la identidad (FMI, 2021, párr. 53). La proporción en pesos es la de cada perímetro: 0,422 en la federal y 0,315 en la consolidada.

**Limitación declarada (Capítulo 7).** La extensión consolidada usa el escenario del FMI con los flujos escalados por la deuda en pesos y en moneda extranjera de ese perímetro, porque el FMI no publica un escenario completo para la deuda consolidada.

## 1.4 El título prometía algo que la tesis no mide

**Crítica.** "Solvencia intertemporal" y "post-2025" prometían algo más amplio que lo que se mide.

**Estado: Resuelto (D13), pendiente de validación del grupo.** Título nuevo: "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos".

## 1.5 El área de vacancia se debilitaba con los propios resultados

**Crítica.** La vacancia se apoyaba en el perímetro consolidado, en la identificación y en el *shock* de la FED, y los resultados anteriores debilitaban los tres. Algunas afirmaciones de ausencia eran exageradas.

**Estado: Resuelto (D1).** La vacancia se formula como "en la literatura revisada no se encontró" y reconoce los trabajos previos. Los tres aportes quedan así: una probabilidad con *shocks* identificados comparable con la del FMI (H1b se cumple con el mismo perímetro); la traducción del *shock* de la FED en un cambio de esa probabilidad (+11,3 puntos en 2035 [4,4; 17,9] con la senda de 2022-2025); y la estimación de la dinámica de la deuda consolidada, que se compara con la federal. La tesis no presenta la identificación como un aporte para la probabilidad, porque no la cambia por construcción.

# 2. Problemas graves de método

## 2.1 La estimación central estaba al borde de una raíz unitaria

**Crítica.** La corrección de sesgo llevaba el autovalor máximo a 0,9998, y las réplicas usaban una corrección menor, con intervalos descentrados.

**Estado: Resuelto (D8).** La estimación central usa los parámetros de MCO, con autovalor máximo 0,849; la mediana de las réplicas es 0,818. Los intervalos son percentiles de Hall (1992), que corrigen el sesgo de la distribución *bootstrap* respecto de la estimación puntual. La corrección de Kilian (1998) queda como robustez: 31,3% en 2031.

## 2.2 La regla de rezagos no tenía respaldo

**Crítica.** "El mayor orden estable que no supera al del AIC" no tenía fuente, y la cita de Ivanov y Kilian (2005) para el AIC era incorrecta para datos trimestrales y esta muestra.

**Estado: Resuelto (D3).** Regla: el criterio de Schwarz entre los órdenes estables, que Ivanov y Kilian (2005) recomiendan para datos trimestrales con menos de 120 observaciones; si sus residuos están autocorrelacionados (Portmanteau, 12 rezagos, 5%), el menor orden mayor que no lo esté (Lütkepohl, 2005, sec. 4.4). Schwarz elige 1 (p = 0,000); se usan 2 (p = 0,296), el mismo orden que elige Hannan-Quinn. Con 1 y 3 rezagos, la probabilidad en 2031 es 32,4% y 30,3%.

## 2.3 Autocorrelación residual con remuestreo independiente

**Crítica.** Los residuos estaban autocorrelacionados, la simulación remuestreaba los *shocks* como independientes y el *bootstrap* salvaje se usaba sin heterocedasticidad condicional que lo justificara.

**Estado: Resuelto (D3, D7 y D8).** Con 2 rezagos los residuos no rechazan la ausencia de autocorrelación (p = 0,296). La simulación remuestrea bloques de ocho trimestres, como los bloques de dos años del abanico del FMI. La inferencia usa un *bootstrap* de bloques móviles de cuatro trimestres (Brüggemann et al., 2016). El *bootstrap* salvaje se abandonó, porque no reproduce la estructura de cuarto orden de las innovaciones.

## 2.4 H2 cumplía su criterio solo en parte y su mecanismo no aparecía

**Crítica.** El efecto sobre la deuda esperada no excluía el cero, no resistía Bonferroni y los canales que nombra la hipótesis no se distinguían.

**Estado: Resuelto en el criterio (D12); el mecanismo es una limitación declarada (Capítulos 6 y 7).** En la especificación principal se cumple el criterio en los dos escenarios y en las dos medidas: senda de 2022-2025, +11,3 puntos de probabilidad en 2035 [4,4; 17,9] y +12,6 de deuda [1,2; 21,8]; nivel 0,504 puntos más alto, +1,5 [0,5; 2,6] y +1,5 [0,1; 2,5]. Lo que sigue débil se declara:

- con Bonferroni, el efecto sobre la deuda esperada incluye el cero (límites inferiores de -0,0 y -0,5);
- en las robusteces, el efecto de la senda sobre la probabilidad excluye el cero en 18 de 19 especificaciones y sobre la deuda en 12 de 19;
- 3 de 84 intervalos de respuesta excluyen el cero, todos del TCRM y con signo de apreciación;
- el 75% del efecto sobre la deuda en 2035 es el costo directo de la deuda en dólares (9,4 de 12,6 puntos).

Veredicto de la tesis: H2 respaldada en su efecto sobre la probabilidad, no en su mecanismo.

## 2.5 El contraste de suficiencia estaba mal descripto

**Crítica.** El superávit necesario se informaba para un año cuando el desplazamiento era de todos, el máximo histórico incluía rentas sin decirlo y la métrica no era monótona en 2035.

**Estado: Resuelto (D10).** La suficiencia es ahora un complemento descriptivo. Con el resultado primario en su máximo anual de 1999-2025 (3,58% del PIB en 2004; 3,29% sin rentas) todos los años, la probabilidad en 2031 es 25,5%. Para llevarla al 1% haría falta sumar 7,75 puntos en todos los años (9,2% del PIB en 2026 y 10,0% en 2031). En 2035 la relación no es monótona: la probabilidad baja hasta 1,35% (+6,25) y vuelve a subir a 2,05% (+8,00), porque con la deuda cerca de cero la métrica se activa con cualquier *shock*. La tesis lo dice.

## 2.6 La reacción fiscal se interpretaba como si fuera anual

**Crítica.** El coeficiente de impacto es trimestral y el multiplicador de largo plazo no tenía intervalo.

**Estado: Resuelto.** Coeficiente de impacto 0,0495 [0,0099; 0,0799] y multiplicador de largo plazo 0,167 [0,057; 0,296], los dos con intervalo de Hall.

## 2.7 El abanico se angostaba de manera artificial

**Crítica.** El VIX y la FED quedaban fijos en la simulación, y las binarias de quiebre se eligieron con la serie de deuda.

**Estado: Resuelto en lo primero (D6); lo segundo es una limitación declarada (Apéndice A.2 y Capítulo 7).** El VIX y el nivel de la tasa de la FED se simulan con procesos AR(1) (0,700 y 0,960), con sus innovaciones remuestreadas junto con los *shocks* estructurales; el bloque externo explica 46,6% de la varianza de la deuda en 2035. Las fechas de quiebre (2001T4, 2006T2, 2018T1) siguen estimadas sobre la deuda. Sin esas binarias, la probabilidad en 2031 es 31,2% y el ancho del abanico, 54,8.

## 2.8 El resultado primario y la deuda tenían perímetros distintos

**Crítica.** El resultado primario incluía las utilidades del BCRA, que en un perímetro consolidado son un flujo interno.

**Estado: Resuelto (D4).** Federal: con rentas de la propiedad, la definición del FMI para el gobierno federal (2025: 1,38% contra 1,4% del FMI; 2024: 1,78% contra 1,8%). Consolidada: sin rentas. La otra definición se informa como robustez (32,4% en 2031 para la federal sin rentas).

## 2.9 La identificación no afectaba la probabilidad principal

**Crítica.** Las diferencias entre las filas de identificación venían del sorteo de Monte Carlo.

**Estado: Resuelto (D8).** Todas las especificaciones usan los mismos números aleatorios, y las identificaciones alternativas dan exactamente la misma probabilidad, como corresponde. La identificación sigue siendo necesaria para repartir la varianza por bloque, que es el criterio de H1a, y para definir el *shock* fiscal. Con Cholesky el reparto cambia (63,9 y 95,8 puntos de diferencia no fiscal menos fiscal), y el criterio de H1a se cumple en todas las variantes.

# 3. Problemas de datos

## 3.1 Tenencias del FGS

**Crítica.** La deuda consolidada de la tesis no descontaba las tenencias del FGS y quedaba por encima de la del FMI.

**Estado: Limitación declarada (Capítulos 5 y 7).** La especificación principal es la deuda federal bruta, que no se ve afectada. La simulación de la extensión consolidada parte del *stock* del FMI (52,1% del PIB), que sí descuenta el FGS. La serie histórica consolidada con la que se estima la dinámica no lo descuenta. Los informes del FGS tienen que bajarse a mano (ver Seguimiento de tareas).

## 3.2 El EMBI+ de 1996-1998 estaba transcripto a mano

**Estado: Resuelto (D2).** Los datos empiezan en 1999T1. El EMBI+ se toma de la serie diaria que publica Ámbito Financiero, disponible desde diciembre de 1998, como promedio trimestral.

## 3.3 Otras cuestiones de datos

- **TCRM de 1996 retropolado.** Resuelto (D2): queda fuera de la muestra.
- **Muestra informada con números distintos en distintos documentos.** Resuelto (D2): 2000T3-2025T4, 102 trimestres, en todos los documentos.
- **Salto de la tasa de la FED en 2022T1.** Resuelto (D5): la variación de ese trimestre se calcula con la tasa efectiva en los dos trimestres. El desvío de la variación trimestral queda en 0,504 puntos.
- **Cuadro de comparación con el FMI con dos ediciones mezcladas.** Resuelto (D1): los *stocks* de partida salen del informe de 2026 (cuadro 2).
- **Valor nominal de las Letras.** Limitación declarada (Capítulo 5): afecta solo la serie consolidada de la extensión, donde una parte de los trimestres se reconstruye o se interpola.
- **Empalme del PIB de 1999-2003.** Limitación declarada (Capítulo 5). El empalme afecta el nivel y no las tasas de crecimiento; la variante con datos desde 2004 da 31,9% en 2031.
- **Tipo de cambio de fin de período de 2024 y 2025.** Limitación menor: solo afecta la serie histórica propia, porque la simulación parte del *stock* del FMI. No se verificó contra la Comunicación A 3500.
- **Fuente del VIX.** Resuelto en la versión anterior.

# 4. Problemas de forma y de criterio académico

- **Hipótesis con esquemas distintos.** Resuelto: unidad, variables, relación esperada y criterio para las tres, en el plan y en la tesis.
- **Matriz de datos del plan.** Resuelto: separa la probabilidad simulada de las variables observadas.
- **Viabilidad del plan.** Resuelto: el EMBI+ es de J.P. Morgan y se toma de la serie publicada por Ámbito Financiero desde 1999.
- **Plan de labor desactualizado.** Resuelto: el plan usa el título de D13, el perímetro de D1, la muestra de D2, la regla de rezagos de D3 y los criterios originales, y conserva el formato de la cátedra.
- **Antecedentes como catálogo.** Resuelto (D14): los ejes 2, 3 y 8 se redujeron a lo esencial.
- **Marco teórico.** Resuelto: no cita resultados propios ni repite Antecedentes.
- **Términos en inglés sin cursiva, siglas sin definir y registro coloquial.** Resuelto.
- **Tablas y figuras.** Resuelto: la tabla completa de robustez pasó al Apéndice (A.8) y Resultados conserva una tabla corta (D14).
- **Referencias en formato APA.** Resuelto en lo verificable; se agregan Brüggemann et al. (2016) y Hall (1992).
- **Carátula y resumen.** Resueltos en la versión anterior.
- **Extensión.** Pendiente de verificar con el texto reescrito (sección 5).

# 5. Qué queda abierto

1. Validación del grupo de D1 (deuda federal bruta como especificación principal y consolidada como extensión).
2. Validación del grupo de D2 (datos desde 1999).
3. Validación del grupo de D13 (título).
4. Recorte a unas 60 páginas, si después de la reescritura todavía hace falta.

Las limitaciones declaradas no están pendientes: son límites del alcance de la tesis y se informan en el texto.
