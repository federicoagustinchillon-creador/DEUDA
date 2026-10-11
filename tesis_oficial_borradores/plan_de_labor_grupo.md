# Plan de labor de la tesis

Documento de trabajo del grupo. Versión del 10 de octubre de 2026.

## 1. Para qué sirve este documento

Ordena qué está hecho, qué se decidió y qué falta, paso a paso, para que todos trabajemos sobre
la misma base. Cada decisión tiene su justificación. Cada número viene de un archivo del
repositorio o de una fuente citada. Lo que todavía no está verificado aparece marcado como
pendiente.

## 2. De dónde partimos

**Lo que ya existe en el repositorio:**

- Una base trimestral 1996-2025 (120 trimestres) con deuda/PIB, resultado primario/PIB, PIB
  real, tipo de cambio real multilateral (TCRM), EMBI+ y VIX.
- Un modelo SVAR restringido estimado sobre esa base. Su descomposición de varianza a 20
  trimestres atribuye la variabilidad de la deuda/PIB así: 54,2% a la inercia propia de la
  deuda, 25,8% a los canales cambiario y de riesgo soberano y 20,0% a los canales fiscal y de
  actividad.
- Un VECM que no encuentra reacción del resultado primario ante la deuda (p = 0,996).
- Una simulación de Monte Carlo de 1.000 trayectorias para 2026-2035, que ya separa la deuda en
  pesos de la deuda en dólares.
- Una tesis en LaTeX de 81 páginas, que hay que reorganizar según las decisiones de este
  documento.

**Lo que aportó Santiago (archivos del 26 de septiembre y del 7 de octubre de 2026):**

- Una Introducción con pregunta, objetivos e hipótesis nuevos.
- El shock de la tasa de la FED como pregunta específica.
- El perímetro consolidado SPNF y BCRA.
- Notas de metodología.

## 3. Decisiones tomadas

| N.° | Decisión | Justificación |
|---|---|---|
| 1 | La Introducción de Santiago del 7/10 es la base, completada con la Justificación y los objetivos específicos del texto LaTeX. | Es la versión más reciente y ya fue revisada. |
| 2 | Todo el trabajo empírico (modelo y simulación) se hace sobre la deuda consolidada SPNF y BCRA. | Es el perímetro que plantea la pregunta de investigación, y el FMI considera deuda pública a los pasivos del banco central cuando pueden financiar al Tesoro o implican riesgo fiscal (FMI, 2021, anexo II). |
| 3 | El modelo es un SVARX: la deuda consolidada es una variable más del sistema, con la tasa de la FED y la volatilidad global como variables exógenas. | Permite efectos conjuntos: la deuda responde a los shocks y a su vez los afecta. Es lo que hace falta para medir cómo un shock de la FED vuelve sobre la deuda a través del riesgo país y del tipo de cambio. |
| 4 | La identificación principal es el SVAR restringido por teoría que ya existe. El ordenamiento de Cholesky queda solo como prueba de robustez. | No hay razón teórica para ordenar el EMBI+ y el TCRM entre sí, y esa justificación ya fue aprobada por el director. |
| 5 | H1b se contrasta con la probabilidad de que la deuda no se estabilice, con corte en 50%. | Es la métrica del FMI (FMI, 2021, párr. 53). El 50% equivale a afirmar que la trayectoria mediana no se estabiliza. El corte calibrado del FMI no se puede replicar con un solo país. Se reporta también la probabilidad completa, para que el resultado no dependa del corte. |
| 6 | El criterio "deuda mayor a 100% del PIB" sale de las hipótesis. | No tiene fuente que lo justifique. |
| 7 | El área de vacancia se reformula. | La afirmación "el marco del FMI excluye al BCRA" es incorrecta (FMI, 2021, anexo II). La vacancia pasa a ser la combinación de tres aspectos que nadie cubrió juntos para Argentina: identificación estructural, un shock externo identificado y la estimación sobre el perímetro consolidado. |
| 8 | El canal cuasifiscal del shock de la FED se redacta en pasado. | Los pasivos remunerados del BCRA se redujeron a niveles mínimos desde 2024. |
| 9 | El módulo de balanza de pagos (exportaciones, importaciones, inversión extranjera directa, fuga de capitales, renovación de vencimientos, necesidades de financiamiento) queda fuera y pasa a investigación futura. | No está especificado, y su tamaño es el de otra tesis. |
| 10 | Todo umbral, corte o tamaño de shock tiene que tener una justificación escrita, propia o citada. | Criterio del grupo. |

## 4. Etapas

Estado: **hecho**, **en curso** o **pendiente**.

### Etapa 1. Introducción (en curso)

- Hecho: borrador corregido (`introduccion_v3`). Corrige citas mal usadas (Reinhart et al.,
  2003; Mendoza y Oviedo, 2007), actualiza la coyuntura con datos de la OPC de julio de 2026,
  reescribe la pregunta, los objetivos y las hipótesis, y suma la Justificación con la Ley
  27.612.
- Pendiente: definir el tamaño del shock de la FED (ver punto 6) y verificar los datos marcados.

### Etapa 2. Antecedentes y área de vacancia (en curso)

- Hecho: borrador de la vacancia (`area_vacancia_v1`).
- Pendiente:
  - bajar a mano el informe del FMI sobre Argentina de 2025 (Informe de País N.° 25/95, anexo I)
    para confirmar si incluye la deuda del BCRA;
  - releer Levy Yeyati y Sturzenegger (2023) y Klemm et al. (2014) para confirmar cómo se los
    describe;
  - fusionar los antecedentes de Santiago con los del texto LaTeX, sin duplicar autores.

### Etapa 3. Datos (pendiente; es el siguiente paso técnico)

1. Construir la deuda consolidada 1996-2025:
   - bajar de la API del BCRA los pases (serie 1261) y las LEBAC (serie 1258) para 1996-2003;
     las LEBAC empiezan en 2002, así que antes de ese año valen cero;
   - empalmar el PIB nominal base 1993 con el base 2004;
   - verificar que la deuda del SPNF y los pasivos del BCRA estén expresados sobre el mismo PIB
     antes de sumarlos.
2. Recalcular la proporción de deuda en pesos para el perímetro consolidado. Hoy el código usa
   46,3% para el SPNF solo.
3. Bajar la tasa de la FED y la tasa sombra de Wu y Xia (que cubre los años de tasa cero) desde
   FRED, y pasarlas a frecuencia trimestral.
4. Validación: gráfico y valores de control de cada serie, revisados por el grupo antes de
   seguir.

### Etapa 4. Metodología (pendiente)

- Reescribir el capítulo con el SVARX y la identificación.
- Definir el tamaño del shock de la FED con criterio justificado: un desvío estándar de la
  serie, un episodio histórico como el de 2022-2023, o ambos.
- Justificar el corte de H1b, siguiendo lo ya escrito en la Introducción.
- Agregar diagnósticos de residuos: autocorrelación, heterocedasticidad, normalidad y
  estabilidad.

### Etapa 5. Estimación (pendiente)

- Pruebas de raíz unitaria y de quiebres sobre la serie consolidada.
- SVARX con dummies en los quiebres que detecte el test de Bai-Perron.
- Respuestas al impulso ante un shock de la FED.
- Descomposición de varianza (H1a).

### Etapa 6. Simulación (pendiente)

- Monte Carlo en el escenario base y con el shock de la FED.
- Métricas del FMI: probabilidad de no estabilización y ancho del abanico entre los
  percentiles 5 y 95, medidos a cinco años y a 2035.
- Contraste de H1b y H2.

### Etapa 7. Resultados, discusión y conclusiones (pendiente)

- Si algún resultado contradice lo que hoy dice la tesis, se frena y se discute en el grupo
  antes de escribirlo.

### Etapa 8. Entrega (pendiente)

- Pasar todo al formato final, revisar las referencias y compilar.

## 5. Pendientes de verificación

| Qué | Dónde se usa |
|---|---|
| Si hubo emisión de deuda bajo ley de Nueva York en 2026 | Introducción, contexto |
| Fuente oficial de la colocación de diciembre de 2025 (USD 1.000 millones al 9,26%) | Introducción, contexto |
| Nivel de los pasivos remunerados del BCRA a fines de 2025 | Introducción y vacancia |
| Número de artículo de Ando et al. (2025) en el JEDC | Referencias |
| Volumen y páginas de Mendoza y Oviedo (2007) | Referencias |
| Número del Informe de País del FMI de 2024 | Referencias |
| Sección exacta del clasificador de Bayes en Hastie, Tibshirani y Friedman (2009) | Justificación del corte de H1b |
| Si el análisis del FMI de 2025 incluye la deuda del BCRA | Vacancia |

## 6. Decisiones abiertas

1. **Tamaño del shock de la FED.** Hay dos criterios defendibles: un desvío estándar de la
   serie o un episodio histórico. Se decide cuando esté la serie.
2. **Horizonte de las métricas.** A cinco años, como el FMI, a 2035, o ambos. La propuesta es
   reportar los dos.

## Referencias de este documento

- Fondo Monetario Internacional. (2021). *Review of the debt sustainability framework for
  market access countries* (IMF Policy Paper).
- Fondo Monetario Internacional y Mecanismo Europeo de Estabilidad. (2023). *The stochastic
  debt fanchart in the IMF's Sovereign Risk and Debt Sustainability Framework for MACs*
  (presentación, 30 de noviembre de 2023).
- Oficina de Presupuesto del Congreso. (2026). *Operaciones de deuda pública, julio 2026*.
