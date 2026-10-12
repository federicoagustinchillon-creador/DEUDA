% Revisión crítica de la tesis y del plan de labor

# Para qué es este documento

Reúne todo lo que el director o el jurado podrían objetar, ordenado por gravedad. La revisión la hicieron tres evaluadores con el encargo explícito de buscar motivos para desaprobar: uno sobre econometría y método, otro sobre datos y escenario, y otro sobre criterios académicos y de la cátedra de Metodología. Cada punto se verificó contra el código, los datos y los resultados.

Cada crítica tiene uno de tres estados:

- **Corregido:** se arregló en el texto en esta versión.
- **Requiere recálculo:** el arreglo cambia números y hay que volver a correr el modelo.
- **Decisión del equipo:** el arreglo depende de una elección que tienen que hacer Pablo y el equipo; acá se explican las opciones.

# 1. Problemas de fondo

## 1.1 Los criterios de H1a y de H2 se definieron después de la primera estimación

**Crítica.** El criterio original de H1a era la descomposición de la varianza: los *shocks* no fiscales debían explicar más varianza de la deuda que los fiscales, con un intervalo de 90% que excluyera el cero. El resultado, 35,9 puntos con intervalo [-4,8; 91,2], no lo cumple. El criterio se cambió por el de suficiencia del superávit en octubre de 2026, el mismo día en que el anterior dejó de cumplirse. El tamaño del *shock* de la FED también se definió en octubre. Un jurado puede leerlo como acomodar la prueba al resultado.

**Estado.** Corregido en el texto en cuanto a transparencia: la sección 4.7 declara el cambio, cuándo se hizo y por qué, e informa los dos criterios. **Decisión del equipo:** cuál es el criterio principal de H1a. Hay dos opciones honestas:

- Mantener la suficiencia como principal, declarando el cambio. Su argumento es que mide lo que dice la hipótesis.
- Volver al criterio original y aceptar que H1a no se sostiene con él, dejando la suficiencia como análisis complementario.

## 1.2 La comparación con el FMI (H1b) no está validada

**Crítica.** La tesis compara su probabilidad de no estabilización (25,2% en 2031) con el 1% del FMI. Pero son cosas distintas:

- **Perímetro:** deuda consolidada neta que parte de 61,0% del PIB, contra deuda federal bruta que parte de 80,3%.
- **Generación de los *shocks*:** el SVARX frente al procedimiento del FMI.
- **Datos:** el FMI usa información que no publica.

El dato más fuerte en contra es que el procedimiento del FMI aplicado a los datos de la tesis da 23,7% y un abanico de 114 puntos, no 1% y 71,5. La tesis no reproduce el número del FMI ni con el método del FMI. La métrica, por otra parte, evalúa un solo año: con una caída planeada de unos 3,4 puntos por año, cualquier modelo con volatilidad anual parecida da 20 a 25%. Un evaluador puede sostener que H1b se cumple casi por construcción.

H1b tampoco es una hipótesis en sentido estricto: no relaciona variables, compara una estimación propia con la de otro organismo.

**Estado.** Corregido en el texto: se sacaron las afirmaciones de que la diferencia "no depende del método" o "proviene de los datos", y la conclusión de que el FMI es "más optimista" quedó condicionada. **Requiere recálculo:** reproducir el 1% del FMI con su perímetro (deuda federal bruta), su punto de partida y sus impulsores. **Decisión del equipo:** si H1b se mantiene como hipótesis, se reformula como objetivo descriptivo o se agrega una pregunta específica sobre la comparación con el FMI.

## 1.3 El escenario base del FMI se aplica a otra deuda

**Crítica.** El cuadro 6 del FMI se armó para la deuda federal bruta: su tasa de interés, su ajuste stock-flujo, su inflación relativa y su velocidad de refinanciación son los de esa deuda. La tesis los aplica a la deuda consolidada neta de 61,0%, de modo que la senda base no es la del FMI ni la de ningún perímetro definido. El FMI publica su propia proyección de la deuda consolidada neta (de alrededor de 52% a poco menos de 30% en cinco años, nota 15 del informe), y la tesis no la usa. Hay además errores de escala: el ajuste stock-flujo se suma sin escalar mientras la inflación relativa sí se escala, la métrica de estabilización omite el ajuste stock-flujo que la identidad incluye, y la proporción en pesos (0,42) se calculó sobre la deuda bruta y no sobre la neta (el FMI da 0,31 para la consolidada).

**Estado.** **Decisión del equipo** y **requiere recálculo**. Opciones:

- Usar como especificación principal la deuda federal bruta, que es la única comparable con el FMI. La variante ya existe y da 27,3% en 2031.
- Reconstruir un escenario base para la deuda consolidada neta a partir del cuadro 2 y la nota 15 del FMI.

En cualquiera de las dos hay que corregir las escalas del ajuste stock-flujo y de la proporción en pesos.

## 1.4 El título promete algo que la tesis no mide

**Crítica.** "Solvencia intertemporal" es, en el marco de Bohn que usa la propia tesis, la condición que se cumple si el superávit reacciona a la deuda, y la tesis estima que reacciona (0,051, intervalo [0,010; 0,103]). Lo que mide la tesis es otra cosa: la probabilidad de que la deuda no se estabilice entre 2026 y 2035. "Post-2025" es coloquial, y el título no menciona ni la probabilidad ni la FED.

**Estado.** **Decisión del equipo.** Propuesta: "Probabilidad de no estabilización de la deuda pública consolidada argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos (1996-2025)".

## 1.5 El área de vacancia se debilita con los propios resultados

**Crítica.** La vacancia se apoya en tres aportes, y los resultados debilitan los tres:

- **Perímetro consolidado:** "el perímetro no cambia los resultados".
- **Identificación de los *shocks*:** no influye en la probabilidad principal.
- ***Shock* de la FED:** impreciso.

Algunas afirmaciones de ausencia eran exageradas: Celasun et al. (2006) incluyen a la Argentina, Levy Yeyati y Sturzenegger (2023) estiman un VAR argentino y Canova (2005) identifica *shocks* de Estados Unidos para la región.

**Estado.** Corregido en el texto: se reconocen esos trabajos y la vacancia se formula como "en la literatura revisada no se encontró". **Decisión del equipo:** reescribir la justificación en torno a lo que la tesis efectivamente aporta: la medición del nivel de la deuda consolidada y la probabilidad estimada con datos argentinos y la métrica del FMI.

# 2. Problemas graves de método

## 2.1 La estimación central está al borde de una raíz unitaria

**Crítica.** Sin corregir, el modelo es estable (autovalor máximo 0,964). La corrección del sesgo lo lleva a 0,9998: los *shocks* se vuelven casi permanentes y eso eleva las probabilidades. Las réplicas del *bootstrap* usan una corrección menor, así que los intervalos quedan descentrados y la estimación central queda pegada al techo: 25,2% con intervalo [19,0; 27,7]. En la muestra desde 2004 queda incluso por encima.

**Estado.** Corregido en el texto: el 0,9998 y el descentrado se informan en 4.5 y 6.1, además del apéndice. **Requiere recálculo:**

- usar la misma corrección en la estimación central y en las réplicas;
- calcular intervalos de Hall o corregidos por sesgo;
- informar la estimación sin corrección como variante.

## 2.2 La regla de rezagos no tiene respaldo

**Crítica.** "El mayor orden estable que no supera al del AIC" no tiene fuente. Entre los órdenes estables, los tres criterios de información (AIC, Hannan-Quinn y Schwarz) eligen dos rezagos o menos, no tres. El AIC toca el borde de la grilla (seis rezagos). Con dos rezagos la probabilidad de 2035 sube a 27,9% y la descomposición de la varianza sí excluye el cero.

**Estado.** **Decisión del equipo:** dos rezagos como especificación principal, o una justificación citada de la regla. Los resultados con dos rezagos ya están en la Tabla 6.6.

## 2.3 Autocorrelación residual con remuestreo independiente

**Crítica.** La prueba de Portmanteau rechaza la ausencia de autocorrelación en todos los órdenes estables. Aun así, la simulación remuestrea los *shocks* como si fueran independientes y el *bootstrap* salvaje supone diferencias de martingala. La heterocedasticidad condicional que justificaría el *bootstrap* salvaje no aparece en las pruebas ARCH (p entre 0,87 y 0,99), y conviene revisar esa implementación.

**Estado.** Declarado como limitación. **Requiere recálculo:** *bootstrap* por bloques en la simulación y en la inferencia.

## 2.4 H2 cumple su criterio solo en parte y su mecanismo no aparece

**Crítica.** El criterio de la Tabla 4.4 pide que el intervalo excluya el cero en la probabilidad y en la deuda esperada:

- se cumple para la probabilidad (+13,0 puntos, intervalo [1,0; 24,8]);
- no se cumple para la deuda ([-1,4; 20,4]);
- no resiste la corrección por contrastes múltiples.

Los canales que nombra la hipótesis no aparecen: de 84 bandas de respuesta al impulso, solo 5 excluyen el cero, menos de las que darían el azar. La mayor parte del efecto (60%) es el costo directo de la deuda en dólares, que el modelo incorpora por construcción. El escenario "senda 2022-2025" no vuelve a la base: deja la tasa 3,82 puntos más alta hasta 2035, y el de un desvío estándar es una suba permanente de 0,50 puntos.

**Estado.** Corregido en el texto: H2 queda como "respaldada solo en parte", con esas salvedades, y los escenarios se describen como cambios permanentes de nivel.

## 2.5 El contraste de suficiencia estaba mal descripto

**Crítica.**

- **Qué se informaba:** "7,0% en 2031", pero el desplazamiento se aplica a todos los años. En realidad es un superávit de 6,15% en 2026 que sube a 7,05% en 2031.
- **El umbral:** el 1% es la estimación puntual del FMI para la Argentina, no un umbral de "riesgo bajo".
- **El máximo histórico:** de 3,6% incluye las rentas de la propiedad; sin ellas es 3,29%.
- **La métrica no es monótona:** en 2035, más superávit puede subir la probabilidad (de 1,15% a 1,93%), porque con deuda cercana a cero cualquier *shock* pequeño la dispara.

**Estado.** Corregido en el texto.

## 2.6 La reacción fiscal se interpretaba como si fuera anual

**Crítica.** El 0,051 es el efecto de impacto de la deuda rezagada sobre el resultado primario trimestral, en un VAR con tres rezagos del propio resultado primario. La respuesta de largo plazo es aproximadamente 0,19 (estimación puntual). Se comparaba con valores anuales de Bohn y con el diferencial anual entre tasa y crecimiento.

**Estado.** Corregido en el texto: se informa el multiplicador de largo plazo y se sacaron las conversiones a términos anuales. Corregida también la cita a Bohn (2007), que debía ser Bohn (1998, 2005). **Requiere recálculo:** el intervalo del multiplicador de largo plazo.

## 2.7 El abanico se angosta de manera artificial

**Crítica.** Dos cosas angostan el abanico:

- En la simulación base, el VIX y la FED quedan en su valor de escenario, así que la varianza que explican no vuelve a la simulación.
- Las variables binarias de quiebre se eligieron con la serie de deuda y absorben los saltos de crisis en el EMBI+, el tipo de cambio y el crecimiento.

Eso debilita la comparación del ancho del abanico (35,3 contra 71,5 del FMI).

**Estado.** **Requiere recálculo:** simular el VIX con su propio proceso y agregar una variante sin las variables binarias.

## 2.8 El resultado primario y la deuda tienen perímetros distintos

**Crítica.** El resultado primario incluye las rentas de la propiedad, que contienen las utilidades del BCRA: en un perímetro consolidado es un flujo interno. Con la serie sin rentas, el ancho del abanico baja a 22,9, la descomposición cambia de signo y el efecto de la FED deja de excluir el cero.

**Estado.** Declarado en el texto. **Decisión del equipo:** si la serie principal debe ser la que no incluye rentas.

## 2.9 La identificación no afecta la probabilidad principal

**Crítica.** La probabilidad de no estabilización no depende de la matriz de identificación, porque los *shocks* estructurales reconstruyen los mismos residuos. La identificación sirve solo para la descomposición por bloques, que no es robusta. Las pequeñas diferencias entre las filas de identificación de la Tabla 6.6 (0,5 a 0,8 puntos) vienen del sorteo de Monte Carlo, no de la identificación.

**Estado.** Corregido en el texto: no se presenta la identificación como aporte para la probabilidad. **Requiere recálculo:** números aleatorios comunes entre especificaciones, para que esas diferencias desaparezcan.

# 3. Problemas de datos

## 3.1 Las tenencias del FGS sí estaban disponibles

**Crítica.** La tesis decía que no se podían descontar las tenencias de deuda del Tesoro en manos de organismos públicos por falta de datos. Pero el repositorio tiene la serie de tenencias de agencias del sector público (Secretaría de Finanzas), anual desde 2004 y trimestral desde 2021. Por eso la deuda de la tesis queda 7,5 a 9,6 puntos del PIB por encima de la consolidada del FMI.

**Estado.** Corregido en el texto: se describe qué datos existen. **Requiere recálculo:** construir la variante neta de esas tenencias para 2004-2025 y agregarla a la Tabla 6.6. Antes hay que verificar si la categoría "Agencias del Sector Público" de la Secretaría de Finanzas incluye al BCRA: en 2023 suma 70,1% del PIB, lo que sugiere que sí, y en ese caso habría que restar solo la parte que no es del BCRA para no descontarla dos veces.

## 3.2 El EMBI+ de 1996-1998 está transcripto a mano

**Crítica.** Los diferenciales de los bonos Brady de 1993-1998 están escritos en el código y no se leen de un archivo fuente. El capítulo de Datos decía "sin intervención manual", y el trimestre 1998T2-T3 entra en la muestra de estimación.

**Estado.** Corregido en el texto: se declara el procedimiento. El empalme con bonos Brady afecta a 8 trimestres (1996-1997), que quedan fuera de la muestra de estimación; los valores de 1998T1-T3 también están transcriptos, y 1998T2 y 1998T3 sí entran en la muestra. El código atribuye los valores a J.P. Morgan, Neumeyer y Perri (2005) y Uribe y Yue (2006), sin cuadro ni página. **Pendiente:** documentar la fuente exacta o empezar la estimación en 1999.

## 3.3 Otras cuestiones de datos

- **Valor nominal de las Letras.** De los 80 trimestres con dato nominal, 17 son observados, 39 reconstruidos y 24 interpolados; en los otros 40 se usa valor contable. Corregido en el texto. **Decisión del equipo:** la variante "piso" combina criterios según el año y conviene revisarla.
- **Cuadro de comparación con el FMI.** Mezcla dos ediciones del informe del FMI (2025 y 2026). **Requiere recálculo** con el informe de 2026, que además publica el *swap* con China.
- **Salto de la tasa de la FED en 2022T1.** Es el paso de la tasa sombra a la tasa efectiva, y define el desvío de 0,50 que se usa como *shock*. **Requiere recálculo:** variable binaria o empalme.
- **Empalme del PIB nominal de 1996-2003.** No tiene análisis de sensibilidad. **Requiere recálculo.**
- **Tipo de cambio de fin de período de 2024 y 2025.** Puede ser un promedio y no un cierre. **Pendiente de verificar** contra la Comunicación A 3500.
- **Muestra.** El informe de construcción de datos decía 117 trimestres y el capítulo de Datos, 111. Corregido.
- **Fuente del VIX.** Se aclaró que se descarga de Yahoo Finance. Corregido.
- **Tipo de cambio real de 1996.** Está extrapolado con una tendencia, sin variaciones propias, y no se declaraba como debilidad. Esos trimestres quedan fuera de la muestra de estimación, pero conviene decirlo en el capítulo de Datos. **Pendiente.**

# 4. Problemas de forma y de criterio académico

- **Hipótesis con esquemas distintos.** Las tres hipótesis tenían esquemas distintos en el plan y en la tesis. Corregido: unidad, variables, relación y criterio para las tres.
- **Matriz de datos del plan.** Mezclaba la probabilidad simulada con las variables observadas. Corregido.
- **Viabilidad del plan.** Afirmaba que todas las series eran homogéneas, públicas y gratuitas. Corregido: el EMBI+ es de J.P. Morgan y el tramo 1996-1998 es un empalme.
- **Antecedentes como catálogo.** Tres ejes (reestructuración, tensión material, costo del *default*) no volvían a usarse. Corregido: cada uno se vincula con el problema o se acortó.
- **Marco teórico.** Citaba resultados propios y repetía un párrafo de Antecedentes. Corregido.
- **Términos en inglés sin cursiva, siglas sin definir y registro coloquial.** Por ejemplo, "muestra chica" y "de a poco". Corregido.
- **Tablas y figuras.** Había tablas y figuras sin fuente, una tabla sin número, figuras numeradas fuera de orden y el conteo "18 especificaciones" equivocado. Corregido.
- **Referencias en formato APA.** Faltaban siglas de autor institucional, había fragmentos que no son APA y años inconsistentes. Corregido en lo verificable.
- **Carátula.** No nombraba al director. Corregido.
- **Resumen.** Tenía 335 palabras. Corregido.
- **Extensión.** 69 páginas contra unas 60. **Decisión del equipo:** qué se recorta. Candidatos: acortar los ejes 2, 3 y 8 de Antecedentes y pasar la Tabla 7.1 al Apéndice.

# 5. Qué tiene que decidir el equipo con Pablo

1. Criterio principal de H1a (punto 1.1).
2. Si H1b se mantiene como hipótesis y contra qué número se compara (punto 1.2).
3. Perímetro y escenario base de la especificación principal (punto 1.3).
4. Título (punto 1.4).
5. Rezagos: dos o tres (punto 2.2).
6. Resultado primario con o sin rentas de la propiedad (punto 2.8).
7. Qué se recorta para llegar a unas 60 páginas.

Con esas decisiones tomadas, los recálculos de los puntos 1.2, 1.3, 2.1, 2.3, 2.7, 2.9 y 3.1 se hacen en una sola corrida y se actualizan todos los números de la tesis.
