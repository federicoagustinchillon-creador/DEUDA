# Plan de Implementación — Revisión de Pares
## Tesis: Sostenibilidad de la Deuda Pública Consolidada Argentina (2004–2025)

> **Instrucciones para Claude Code**: Este documento es la hoja de ruta definitiva. Todas las decisiones metodológicas ya fueron tomadas. Las instrucciones son ejecutables sin interpretación adicional. No buscar nuevos hallazgos. No modificar conclusiones no señaladas aquí. Preservar íntegramente el aporte científico original.

---

## 1. RESUMEN EJECUTIVO

| # | Hallazgo | Estado | Prioridad | Riesgo metodológico | Complejidad | Beneficio esperado |
|---|---------|--------|-----------|---------------------|-------------|-------------------|
| H1 | Hansen con dependiente I(1) | CONFIRMADO | **CRÍTICA** | Alto — p-value sin distribución asintótica garantizada | Media | Elimina objeción formal de metodólogo |
| H2 | ETF EMB y limitación del Sargan | PARCIALMENTE CONFIRMADO | ALTA | Medio — limitación del J-test documentada en literatura | Baja | Refuerza discusión IV-2SLS |
| H3 | Canales exógenos sin SF_t | CONFIRMADO | ALTA | Alto — asimetría epistemológica entre crítica y conclusión | Media–Alta | Eleva rigor del Abstract y Discusión |
| H4 | R²=0.586 con DW=0.321 | NO CONFIRMADO | **DESCARTADO** | N/A — hallazgo metodológicamente incorrecto | N/A | No implementar |
| H5 | CUSUM vs. subperíodos | PARCIALMENTE CONFIRMADO | MEDIA | Medio — afirmación positiva de estabilidad no autorizada | Baja | Elimina aparente contradicción interna |
| H6 | Tail dependence de t multivariada | CONFIRMADO | ALTA | Alto — 30.4% puede sobreestimar riesgo de cola | Media | Robustez adicional o advertencia explícita |
| H7 | Trasplante de Ghosh a Argentina | CONFIRMADO | MEDIA | Medio — alcance del veredicto H1a sobreextendido | Baja | Reformulación de una línea en Tabla de consistencia |

**Hallazgo descartado**: H4 (R²/DW en DOLS) es metodológicamente incorrecto y **no debe implementarse**. El DW bajo con HAC en DOLS es la práctica estándar de Stock & Watson (1993).

---

## 2. PRINCIPIOS GENERALES

### 2.1 Resultados que NO deben modificarse

- Los coeficientes estimados: $\rho=-0.0071$ ($p=0.564$); $F_{IV}=23.39$; Sargan $p=0.576$; Sup-LM $p=0.383$
- La cifra central del DSA: $P(d_{2035}>100\%)=30.4\%$ (y sus robusteces: 31.9% GARCH, 29.1% DCC)
- El número de observaciones: $n=88$ (DOLS: $n=78$, IV-2SLS: $n=73$)
- Los quiebres Bai-Perron: 2007T2, 2014T3, 2018T1 (SPNF); 2007T2, 2016T4 (consolidada)
- Las tablas estadísticas (Tab. DOLS, IV-2SLS, Hansen, Johansen, DF-GLS, sensibilidad temporal)
- Las figuras: Fan Chart, CUSUM/CUSUMSQ, diagnóstico primera etapa IV-2SLS, DSA determinista

### 2.2 Conclusiones que deben preservarse íntegramente

- La hipótesis H1 (reacción fiscal débil) no fue rechazada: $\rho=-0.0071$, $p=0.564$
- La hipótesis H1a (fatiga fiscal) no fue verificada: Sup-LM $p=0.383$
- La hipótesis H1b (endogeneidad del EMBI+): parcialmente verificada
- La hipótesis H1c (quiebres estructurales): verificada
- La interpretación narrativa de los canales exógenos como "compatible pero no inferida"
- Las proyecciones DSA como escenarios calibrados, no como pronósticos

### 2.3 Modelos obligatorios por diseño (no reemplazar)

- DOLS de Stock & Watson (1993): estimador principal de la FRF
- Hansen (1999, 2000): test de umbral — se AÑADE advertencia sobre supuesto, no se elimina el test
- IV-2SLS con VIX + EMB_Brasil: diseño instrumental validado — se AÑADE discusión de limitación del Sargan
- DSA Monte Carlo con distribución t multivariada ($\nu\approx5.1$): se AÑADE robustez, no se reemplaza

### 2.4 Categorías de cambios

| Categoría | Descripción | Hallazgos |
|-----------|-------------|-----------|
| Corrección técnica | Añade advertencia o limitación sobre un método existente | H1, H2 |
| Mejora de coherencia interna | Reformula afirmación textual sin cambiar resultado | H5, H7 |
| Corrección narrativa | Reequilibra peso de conclusión entre cuerpo y Abstract | H3 |
| Robustez estadística | Añade especificación alternativa | H6 |
| No implementar | Hallazgo rechazado en segunda revisión | H4 |

---

## 3. FASES DE IMPLEMENTACIÓN

### FASE 1 — Correcciones técnicas críticas (H1, H2)

**Objetivo**: Añadir advertencias metodológicas sobre el test de Hansen con variable dependiente I(1) y reconocer la limitación formal del Sargan ante instrumentos con canal compartido.

**Archivos afectados**:
- `c:\Users\fedea\Deuda\latex\capitulos\06_resultados.tex` (Secciones 6.4 y 6.3)

**Cambios esperados**:
- Un párrafo nuevo al final de la Sección 6.4 (Hansen) reconociendo el supuesto de estacionariedad
- Un párrafo ampliado en la Sección 6.3 (IV-2SLS) reconociendo la limitación del Sargan

**Criterios de aceptación**:
- El párrafo nuevo en Sección 6.4 cita explícitamente Hansen (1999, Assumption 1; 2000, p. 577)
- El párrafo nuevo en Sección 6.3 cita explícitamente Bound, Jaeger & Baker (1995)
- Los p-values originales (p=0.383, p=0.576) permanecen sin cambio
- El PDF compila sin errores

**Riesgos**:
- Riesgo bajo: son adiciones, no sustituciones de resultados existentes

---

### FASE 2 — Correcciones de coherencia interna (H5, H7)

**Objetivo**: Reformular la afirmación "establemente débiles" del CUSUM y el veredicto H1a de la Tabla de consistencia.

**Archivos afectados**:
- `c:\Users\fedea\Deuda\latex\capitulos\06_resultados.tex` (párrafo CUSUM, Sección 6.2/6.5)
- `c:\Users\fedea\Deuda\latex\capitulos\08_conclusiones.tex` (Tabla \ref{tab:mapa_consistencia}, fila H1a)

**Cambios esperados**:
- En Sección 6 (párrafo CUSUM, línea 165): reemplazar "establemente débiles" por formulación que reconoce que el no-rechazo CUSUM no equivale a afirmación positiva de estabilidad
- En Tabla `tab:mapa_consistencia` (línea 20 de `08_conclusiones.tex`): reformular veredicto H1a

**Criterios de aceptación**:
- El párrafo reformulado no usa la frase "establemente débiles" sin calificación
- El veredicto H1a incluye la referencia al ámbito de economías avanzadas de Ghosh (2013)
- Ningún coeficiente numérico de la Tabla cambia
- El PDF compila sin errores

**Riesgos**:
- Riesgo bajo: modificaciones textuales menores

---

### FASE 3 — Robustez estadística (H6)

**Objetivo**: Añadir una especificación alternativa de colas independientes en el DSA para testear sensibilidad a la tail dependence de la distribución t multivariada.

**Archivos afectados**:
- `c:\Users\fedea\Deuda\latex\capitulos\07_discusion.tex` (Sección 7.3 Fan Chart / Sección 7.4 robustez GARCH)
- Script Python del DSA: `src/models/fase6_sostenibilidad_deuda.py` o `src/models/fase7_diagnosticos_robustez.py`

**Cambios esperados**:
- OPCIÓN A (recomendada): Re-ejecutar DSA con $t$ marginales independientes (sin cópula-t), reportar nueva probabilidad y comparar con 30.4%
- OPCIÓN B (si no hay acceso al script): Añadir párrafo en la Sección de Limitaciones (Sección 7.5, línea 162) reconociendo la tail dependence de la distribución t con $\nu=5.1$ y cuantificando el coeficiente teórico ($\lambda\approx0.15$)

**Criterios de aceptación**:
- Si OPCIÓN A: nueva tabla o línea en tabla existente con la probabilidad bajo colas independientes, acompañada de texto explicativo
- Si OPCIÓN B: párrafo que cita Demarta & McNeil (2005) y cuantifica $\lambda$ formalmente
- La cifra 30.4% permanece como resultado principal; la nueva especificación aparece como robustez adicional
- El PDF compila sin errores

**Riesgos**:
- Riesgo medio-alto (OPCIÓN A): requiere ejecutar código Python; si el resultado con colas independientes diverge significativamente del 30.4%, puede requerir una redacción más cuidadosa
- Riesgo bajo (OPCIÓN B): es solo texto

---

### FASE 4 — Corrección narrativa del Abstract (H3)

**Objetivo**: Reequilibrar el peso de la conclusión sobre canales exógenos en el Abstract y reforzar el caveat en el Cap. 7 para eliminar la asimetría epistemológica identificada.

**Archivos afectados**:
- `c:\Users\fedea\Deuda\latex\capitulos\00_abstract.tex` (línea 1, párrafo Discusión)
- `c:\Users\fedea\Deuda\latex\capitulos\07_discusion.tex` (Sección 7.2, líneas 23-25)

**Cambios esperados**:
- En el Abstract, reformular el fragmento sobre canales exógenos para que la formulación sea explícitamente hipotética desde el inicio (no solo al final del párrafo)
- En Sección 7.2 del Cap. 7, reforzar el caveat sobre cuantificación del SF_t y añadir nota sobre agenda futura

**Criterios de aceptación**:
- El Abstract no presenta los canales exógenos como conclusión empírica, sino como interpretación compatible
- La Sección 7.2 incluye referencia explícita a que la cuantificación del SF_t excede el alcance de esta tesis y constituye agenda futura
- El Abstract sigue dentro del límite de palabras establecido por la institución
- El PDF compila sin errores

**Riesgos**:
- Riesgo bajo: modificaciones textuales en el Abstract
- Riesgo medio: el Abstract es un archivo de una sola línea (`00_abstract.tex`); editar sin romper el bloque de LaTeX

---

### FASE 5 — Verificación y auditoría final

**Objetivo**: Verificar que todos los cambios son internamente consistentes, que no se rompieron referencias cruzadas, numeración de figuras/tablas ni el flujo de compilación.

**Archivos afectados**: Todos los modificados en Fases 1–4 más el archivo principal `.tex`

**Acciones**:
- Compilar el PDF completo (dos pasadas: `pdflatex` + `biber`/`bibtex` + `pdflatex`)
- Verificar que todas las referencias `\ref{}` y `\cite{}` añadidas están definidas en `referencias.bib`
- Verificar numeración de tablas y figuras
- Comparar Abstract modificado con original para confirmar que las cifras estadísticas son idénticas

---

## 4. PLAN DETALLADO POR HALLAZGO

---

### HALLAZGO H1 — Test de Hansen con variable dependiente I(1)

#### Descripción

El test Sup-LM de Hansen (1999/2000) con bootstrap de 1.000 réplicas se aplicó con `pb_t` como variable dependiente, clasificada como I(1) por DF-GLS (estadístico $-1.85$, crítico $-3.06$ al 5\%; Tabla `tab:dfgls`, archivo `06_resultados.tex`, líneas 11–29). Ambos papers de Hansen (1999, Assumption 1, p. 349; 2000, Assumption A, p. 577) requieren que los datos sean estrictamente estacionarios y ergódicos. Esta condición es incompatible con procesos I(1). El p-value de 0.383 del Sup-LM bootstrap carece de distribución asintótica garantizada en esta configuración.

#### Fundamentación

- Hansen, B.E. (1999). "Threshold effects in non-dynamic panels." *Journal of Econometrics* 93(2):345–368. Assumption 1, p. 349: datos estrictamente estacionarios y β-mixing.
- Hansen, B.E. (2000). "Sample splitting and threshold estimation." *Econometrica* 68(3):575–603. Assumption A, p. 577: "the threshold variable $q_t$ and the regression variables $(y_t, x_t)$ are jointly strictly stationary and ergodic."
- Caner, M. & Hansen, B.E. (2004). "Instrumental variable estimation of a threshold model." *Journal of Business & Economic Statistics* 22(3):304–311. Extensión para procesos cointegrados.

#### Impacto

- **Inferencia**: El p-value de 0.383 del Sup-LM puede no tener la distribución asintótica chi-cuadrado esperada, introduciendo incertidumbre adicional en el rechazo de linealidad.
- **Interpretación**: El resultado negativo del test (no rechazo de linealidad) permanece válido como diagnóstico; la incertidumbre afecta la cuantificación exacta del nivel de significancia.
- **Robustez**: La conclusión sustantiva (no evidencia de umbral) no cambia; la corrección la hace formalmente más sólida.
- **Reproducibilidad**: No afecta los datos ni los scripts; solo el texto.

#### Implementación mínima

Añadir un párrafo al final de la Sección 6.4 (Modelo de Umbral de Hansen) del archivo `06_resultados.tex`, después de la oración que termina "...una limitación de potencia que el Capítulo \ref{ch:discusion} examina a la luz de la volatilidad estructural del riesgo soberano argentino." (línea 247, fin del párrafo del Sup-LM).

**Texto exacto a insertar** (en español, estilo del documento):

```latex
\textit{Nota metodológica sobre el supuesto de estacionariedad del test de umbral.} El contraste Sup-LM y su bootstrap son asintóticamente válidos bajo el supuesto de estacionariedad estricta de todos los regresores, incluida la variable dependiente \citep[Assumption~A, p.~577]{hansen2000}. Sin embargo, el diagnóstico del Capítulo~\ref{ch:resultados} clasifica $pb_t$ como I(1) (Tabla~\ref{tab:dfgls}: estadístico~$-1.85$, crítico~$-3.06$), de modo que dicho supuesto no se cumple en sentido estricto. En presencia de una variable dependiente integrada de orden uno, la distribución asintótica del estadístico Sup-LM queda formalmente comprometida, y el $p$-valor de 0.383 debe interpretarse con la cautela adicional que esta limitación impone. \citet{caner2004} extienden el marco de umbral al caso de procesos cointegrados; su aplicación a esta muestra constituye una línea metodológica para investigación futura. El resultado negativo reportado ---ausencia de evidencia de umbral--- permanece como el diagnóstico sustantivo de esta sección, siendo esta nota una calificación de la precisión formal de su $p$-valor, no una reversión de su signo.
```

#### Implementación óptima

Re-estimar el modelo de umbral con $\Delta pb_t$ (I(0)) como variable dependiente y comparar el Sup-LM resultante con el de la especificación en niveles. Si el resultado negativo persiste, la robustez metodológica se vuelve completa. Requiere ejecutar el script Python del Cap. 6 con la variable dependiente transformada.

#### Ubicación exacta

| Elemento | Archivo | Línea(s) |
|---------|---------|---------|
| Tabla DF-GLS (evidencia de I(1)) | `06_resultados.tex` | 11–29 |
| Sección Hansen (`\section{Modelo de Umbral de Hansen}`) | `06_resultados.tex` | 219–249 |
| **Punto de inserción** del párrafo nuevo | `06_resultados.tex` | **después de línea 247** |
| Tabla Hansen (`tab:hansen`) | `06_resultados.tex` | 226–243 |
| Párrafo del Sup-LM p=0.383 | `06_resultados.tex` | 247 |

#### Dependencias

- Ninguna. Este cambio no depende de ningún otro cambio en el documento.

#### Riesgos

- **Bajo**: es una adición de texto, no una modificación de resultado.
- Verificar que `\citet{caner2004}` está en `referencias.bib`. Si no está, añadir:
```bibtex
@article{caner2004,
  author  = {Caner, Mehmet and Hansen, Bruce E.},
  title   = {Instrumental variable estimation of a threshold model},
  journal = {Journal of Business \& Economic Statistics},
  year    = {2004},
  volume  = {22},
  number  = {3},
  pages   = {304--311}
}
```

#### Validación

- [ ] El párrafo cita `\citet{hansen2000}` con referencia a "Assumption A, p. 577"
- [ ] El párrafo cita `\citet{caner2004}`
- [ ] El número 0.383 aparece en el párrafo (para asegurar referencia cruzada correcta)
- [ ] `pdflatex` compila sin `undefined reference` ni `undefined citation`
- [ ] El número de la sección y tabla no cambió

---

### HALLAZGO H2 — ETF EMB y limitación formal del Sargan ante canal compartido

#### Descripción

El Sargan J-test (p=0.576) no rechaza la validez conjunta de los instrumentos VIX + EMB_Brasil. Sin embargo, cuando todos los instrumentos comparten el mismo canal de violación potencial (apetito de riesgo global), el Sargan tiene potencia nula para detectarlo (Bound, Jaeger & Baker, 1995). La tesis no menciona esta limitación estructural del test. El canal específico de valuación del portafolio de reservas del BCRA (segunda revisión: PARCIALMENTE CONFIRMADO) es cuestionable en magnitud pero la limitación formal del Sargan es válida.

#### Fundamentación

- Bound, J., Jaeger, D.A. & Baker, R.M. (1995). "Problems with instrumental variables estimation when the correlation between the instruments and the endogenous explanatory variable is weak." *Journal of the American Statistical Association* 90(430):443–450.
- Staiger, D. & Stock, J.H. (1997). "Instrumental variables regression with weak instruments." *Econometrica* 65(3):557–586. (Ya citado en la tesis; p. 559 discute las limitaciones del J-test)

#### Impacto

- **Inferencia**: No cambia: los instrumentos son fuertes (F=23.39) y el Sargan no rechaza. La limitación es sobre la información adicional que el Sargan provee.
- **Interpretación**: La validez instrumental sigue siendo la mejor evidencia disponible; se añade matiz sobre la robustez de esa evidencia.
- **Reproducibilidad**: No afecta datos ni scripts.

#### Implementación mínima

Añadir una oración al párrafo sobre el test de Sargan en la Sección 6.3 (IV-2SLS), inmediatamente después de la oración "La sustitución de instrumento resuelve, en consecuencia, el problema de validez identificado en la versión preliminar de este ejercicio..." (línea 202 de `06_resultados.tex`).

**Texto exacto a insertar**:

```latex
Conviene precisar, no obstante, el alcance informativo del test de Sargan en este contexto. Como señalan \citet{bound1995}, el test de sobreidentificación carece de potencia para detectar violaciones de la restricción de exclusión cuando los instrumentos comparten el mismo canal de transmisión potencial hacia la variable dependiente ---en este caso, el apetito de riesgo global que tanto el VIX como el EMBI$_\text{Brasil}$ capturan---. El resultado no significativo del Sargan ($p=0.576$) es condición necesaria pero no suficiente para garantizar la restricción de exclusión: constituye evidencia favorable a la validez de los instrumentos en la medida en que los dos instrumentos difieran en su canal de transmisión (el VIX mide volatilidad implícita de acciones globales; el EMBI$_\text{Brasil}$ mide spreads de renta fija soberana regional), diferencia que el test explota para su identificación, pero sin que ello elimine la posibilidad de un canal compartido no detectado. Esta calificación no revierte el diseño instrumental adoptado ---el único disponible dentro de la muestra y dentro de las restricciones de identificación de la literatura de referencia \citep{blanchard2021}--, sino que delimita el alcance de la evidencia que el Sargan provee.
```

#### Implementación óptima

Añadir el párrafo anterior más un test de sensibilidad: re-estimar la segunda etapa usando solo el VIX como instrumento (diseño exactamente identificado, sin Sargan posible) y comparar el coeficiente del EMBI+ instrumentado con el de la especificación completa. Si el coeficiente es similar, la robustez es genuina. Requiere ejecutar el script IV-2SLS.

#### Ubicación exacta

| Elemento | Archivo | Línea(s) |
|---------|---------|---------|
| Sección IV-2SLS (`\section{Corrección por Endogeneidad}`) | `06_resultados.tex` | 169–217 |
| Tabla IV-2SLS (`tab:iv2sls`) | `06_resultados.tex` | 174–198 |
| Párrafo Sargan (oración "La sustitución de instrumento...") | `06_resultados.tex` | **202** |
| **Punto de inserción** del párrafo nuevo | `06_resultados.tex` | **después de línea 202** |
| Discusión instrumental en Cap. 7 | `07_discusion.tex` | 8 |

#### Dependencias

- Añadir entrada `bound1995` en `referencias.bib` si no existe:
```bibtex
@article{bound1995,
  author  = {Bound, John and Jaeger, David A. and Baker, Regina M.},
  title   = {Problems with instrumental variables estimation when the correlation between the instruments and the endogenous explanatory variable is weak},
  journal = {Journal of the American Statistical Association},
  year    = {1995},
  volume  = {90},
  number  = {430},
  pages   = {443--450}
}
```

#### Riesgos

- **Bajo**: adición de texto que no modifica ninguna estimación.
- Verificar que `\citet{blanchard2021}` ya está citado en la tesis (lo está en Cap. 7, línea 8).

#### Validación

- [ ] El párrafo nuevo cita `\citet{bound1995}`
- [ ] El párrafo nuevo menciona el p-value 0.576 por nombre (o referencia a la tabla)
- [ ] El párrafo nuevo menciona la diferencia VIX (acciones) vs. EMBI_Brasil (renta fija)
- [ ] `pdflatex` compila sin errores

---

### HALLAZGO H3 — Conclusión sobre canales exógenos sin descomposición del SF_t

#### Descripción

La tesis critica a la literatura precedente por "vincular narrativamente" variables sin contraste formal (Tabla de contraste del Estado del Arte, Cap. 2). La conclusión central (Abstract, Sección 7.2, Sección 8.2) atribuye la solvencia argentina a canales exógenos (depreciación real, licuación inflacionaria, quitas) sin cuantificar el SF_t para los episodios críticos (2005, 2018, 2020). El Abstract presenta la atribución con el peso de una conclusión empírica; el cuerpo la declara correctamente como "interpretación compatible." Esta asimetría es la que genera la objeción epistemológica.

La segunda revisión confirma que la descomposición del SF_t es el estándar del DSA del FMI (IMF, 2021, Annex I) cuando se combina un resultado nulo de la FRF con una explicación alternativa.

#### Fundamentación

- IMF (2021). *Review of the Debt Sustainability Framework for Market Access Countries*. Washington: IMF. Annex I (stock-flow adjustments como componente estándar de las tablas DSA).
- Bohn, H. (1998). "The behavior of US public debt and deficits." *Quarterly Journal of Economics* 113(3):949–963. (Marco de la FRF; la descomposición contable es el complemento natural del resultado nulo.)
- Eichengreen, B., Hausmann, R. & Panizza, U. (2007). "Currency mismatches, debt intolerance and original sin." NBER Working Paper 10036. (Marco para interpretar restricción externa en economías bimonetarias.)

#### Impacto

- **Inferencia**: No cambia ningún resultado econométrico.
- **Interpretación**: La conclusión sobre canales exógenos mantiene su contenido; se reformula su presentación para que sea consistente con el caveat del cuerpo.
- **Robustez**: Elimina la objeción de asimetría epistemológica que cualquier revisor experto detectará.

#### Implementación mínima

**Modificación A** — En el Abstract (`00_abstract.tex`, línea 1):

Localizar el fragmento: `"...sino por canales exógenos a él --depreciación real y efecto de valuación, licuación inflacionaria y reestructuraciones con quita--, en línea con lo que anticipa el Paradigma de la Restricción Externa para una economía bimonetaria."`

Reemplazar con: `"...sino por canales exógenos a él ---depreciación real y efecto de valuación, licuación inflacionaria y reestructuraciones con quita---; una interpretación compatible con el resultado nulo y coherente con el Paradigma de la Restricción Externa para una economía bimonetaria, aunque no contrastada directamente por esta tesis y especificada como agenda futura en el Capítulo~\ref{ch:conclusiones}."`

**Modificación B** — En Sección 7.2 del Cap. 7 (`07_discusion.tex`), después del párrafo que termina con "...contrastarla exigiría un diseño distinto..." (línea 25), añadir:

```latex
La cuantificación directa de la contribución de cada canal al Ajuste Stock-Flujo ($SF_t$) ---mediante la descomposición contable de la identidad $d_t = \frac{1+r_t}{1+g_t}d_{t-1} - pb_t + SF_t$ para los episodios de 2005 (reestructuración), 2018 (depreciación) y 2020 (quita y licuación)--- permitiría transformar esta interpretación en evidencia directa y constituye la línea prioritaria de investigación futura identificada en la Sección~\ref{sec:agenda_futura}. Su ausencia en este trabajo no invalida la interpretación propuesta, pero limita su peso probatorio al de una hipótesis teórica sustentada en la consistencia con el resultado nulo y en el patrón descriptivo de la Sección~\ref{sec:restriccion_intertemporal}, no en una cuantificación propia de los canales invocados.
```

#### Implementación óptima

Implementar la descomposición contable del SF_t para los tres episodios críticos (2005, 2018, 2020) en una nueva tabla en la Sección 7.2 o en el Apéndice, usando los datos ya disponibles en el dataset. Esta opción transformaría la interpretación en evidencia directa. Si se implementa, citar IMF (2021) como referencia metodológica.

#### Ubicación exacta

| Elemento | Archivo | Línea(s) |
|---------|---------|---------|
| **Abstract** — Párrafo "Discusión" (texto completo en línea 1) | `00_abstract.tex` | **1** |
| **Fragmento exacto a modificar en Abstract** | `00_abstract.tex` | "...sino por canales exógenos..." hasta "...economía bimonetaria." |
| Sección 7.2 (fatiga fiscal) | `07_discusion.tex` | 14–25 |
| **Punto de inserción** del párrafo SF_t en Cap. 7 | `07_discusion.tex` | **después de línea 25** |
| Sección agenda futura (`\label{sec:agenda_futura}`) | `08_conclusiones.tex` | 57–60 |

#### Dependencias

- H3 Mod. B depende de que la etiqueta `\ref{sec:agenda_futura}` exista en `08_conclusiones.tex` — **ya existe** (línea 58).
- El comando `\ref{sec:restriccion_intertemporal}` debe existir — verificar antes de la inserción.

#### Riesgos

- **Riesgo medio en el Abstract**: el archivo `00_abstract.tex` es un único bloque de texto comprimido en 2 líneas. Editar con extremo cuidado para no romper llaves LaTeX o entornos.
- **Riesgo bajo en Cap. 7**: adición de texto al final de un párrafo existente.
- Verificar que el Abstract resultante no supera el límite de palabras de la institución (si existe).

#### Validación

- [ ] El Abstract no presenta los canales exógenos como conclusión empírica sin calificación
- [ ] El Abstract contiene la palabra "interpretación" o equivalente antes de mencionar los canales
- [ ] La Sección 7.2 contiene referencia explícita a SF_t y agenda futura
- [ ] La referencia `\ref{sec:agenda_futura}` resuelve correctamente
- [ ] `pdflatex` compila sin errores
- [ ] El texto del Abstract resultante mantiene todas las cifras estadísticas originales inalteradas

---

### HALLAZGO H5 — Afirmación de estabilidad paramétrica incompatible con evidencia DOLS de subperíodos

#### Descripción

En la Sección 6.2 (o párrafo CUSUM de la Sección 6), línea 165 de `06_resultados.tex`, la frase "los coeficientes de la Tabla \ref{tab:dols}, aunque débiles y no significativos, parecen ser \textit{establemente} débiles a lo largo de todo el período, y no fuertes en un subperíodo y débiles en otro" es una afirmación positiva de estabilidad que va más allá de lo que el no-rechazo CUSUM puede afirmar. Simultáneamente, la Tabla `tab:sensibilidad_temporal` (Sección 6.5, líneas 256–277) demuestra que el coeficiente es positivo y significativo en ambos subperíodos bajo MCO estático ($\rho$=0.0373 y $\rho$=0.0530), y que el coeficiente nulo de muestra completa DOLS es un artefacto de la augmentación global.

La segunda revisión clasifica esto como PARCIALMENTE CONFIRMADO: la distinción CUSUM-OLS vs. DOLS-subperíodo es técnicamente válida, pero la afirmación textual sobrepasa lo que el no-rechazo CUSUM autoriza.

#### Fundamentación

- Brown, R.L., Durbin, J. & Evans, J.M. (1975). "Techniques for testing the constancy of regression relationships over time." *Journal of the Royal Statistical Society, Series B* 37(2):149–163. (El CUSUM solo testea constancia paramétrica en OLS; un no-rechazo es "ausencia de evidencia de inestabilidad", no "evidencia de estabilidad".)
- Ploberger, W. & Krämer, W. (1992). "The CUSUM test with OLS residuals." *Econometrica* 60(2):271–285. (Documenta la baja potencia del CUSUM ante quiebres moderados en coeficientes de pendiente.)

#### Impacto

- **Interpretación**: La corrección convierte una aparente contradicción interna en una descripción metodológicamente precisa de dos tests con objetos distintos.
- **Coherencia interna**: El párrafo CUSUM y la Sección 6.5 pasan a ser complementarios, no contradictorios.

#### Implementación mínima

Localizar en `06_resultados.tex` la oración exacta de la línea 165:

**Texto actual** (a reemplazar):
```
...los coeficientes de la Tabla \ref{tab:dols}, aunque débiles y no significativos, parecen ser \textit{establemente} débiles a lo largo de todo el período, y no fuertes en un subperíodo y débiles en otro.
```

**Texto de reemplazo**:
```latex
...los coeficientes de la Tabla \ref{tab:dols}, aunque débiles y no significativos en la especificación OLS que el CUSUM evalúa, no cruzan los límites de confianza en ningún punto de la muestra: el no-rechazo del CUSUM implica ausencia de evidencia de inestabilidad en la especificación lineal OLS, no una afirmación positiva de estabilidad del coeficiente estructural $\rho$. La Sección \ref{sec:sensibilidad_temporal} complementa este diagnóstico mostrando que, bajo augmentación dinámica DOLS por subperíodo, la reacción fiscal estimada es positiva y significativa en ambas mitades de la muestra (2004--2014: $\rho=0.0373$, $p=0.0015$; 2015--2025: $\rho=0.0530$, $p=0.0026$), siendo el coeficiente nulo de muestra completa un artefacto de la augmentación global que absorbe correlaciones de corto plazo de distinta naturaleza en cada régimen.
```

#### Ubicación exacta

| Elemento | Archivo | Línea(s) |
|---------|---------|---------|
| Párrafo CUSUM completo | `06_resultados.tex` | 154–167 |
| **Oración exacta a reemplazar** | `06_resultados.tex` | **165 (segunda mitad)** |
| Tabla sensibilidad temporal (`tab:sensibilidad_temporal`) | `06_resultados.tex` | 256–277 |

**Texto exacto de la oración a localizar** (búsqueda literal):
```
parecen ser \textit{establemente} débiles a lo largo de todo el período, y no fuertes en un subperíodo y débiles en otro.
```

#### Dependencias

- La referencia `\ref{sec:sensibilidad_temporal}` debe existir — **ya existe** (línea 251 de `06_resultados.tex`).
- Los coeficientes citados en el reemplazo ($\rho=0.0373$, $\rho=0.0530$) deben coincidir exactamente con la Tabla `tab:sensibilidad_temporal` — **ya coinciden** (líneas 263 y 267).

#### Riesgos

- **Bajo**: modificación textual de una oración.
- Verificar que la sustitución no rompe el flujo de la oración anterior ("En otras palabras:").

#### Validación

- [ ] La oración "establemente débiles" ya no aparece sin calificación en el documento
- [ ] El texto nuevo incluye los valores numéricos $\rho=0.0373$ y $\rho=0.0530$ con sus p-values
- [ ] La referencia `\ref{sec:sensibilidad_temporal}` resuelve correctamente
- [ ] El CUSUM/CUSUMSQ permanece sin modificación en la Figura `fig:cusum`
- [ ] `pdflatex` compila sin errores

---

### HALLAZGO H6 — Distribución t multivariada con tail dependence: robustez adicional al 30.4%

#### Descripción

La distribución $t$ de Student multivariada con $\nu\approx5.1$ impone tail dependence por construcción (Demarta & McNeil, 2005). El coeficiente teórico es $\lambda = 2 \cdot T_{\nu+1}\!\left(-\sqrt{(\nu+1)(1-\rho)/(1+\rho)}\right)$. Para $\nu=5.1$ y $\rho=0.11$ (correlación QML del [[dcc-garch-dynamic-correlation|DCC-GARCH]]), $\lambda\approx0.15$. Esto significa que hay un 15% de probabilidad de shocks simultáneos extremos en todas las variables, incluso con correlación baja. Las tres robusteces reportadas (30.4%, 31.9%, 29.1%) no testeen la sensibilidad a esta estructura de dependencia —todas mantienen la distribución $t$ multivariada.

#### Fundamentación

- Demarta, S. & McNeil, A.J. (2005). "The t copula and related copulas." *International Statistical Review* 73(1):111–129. (Fórmula del coeficiente de tail dependence, pp. 114–116.)
- IMF (2021). *Review of the Debt Sustainability Framework for Market Access Countries*. (Reconoce la necesidad de ir más allá de distribuciones normales, pero no prescribe t multivariada como estándar único.)

#### Impacto

- **Robustez**: La cifra 30.4% puede sobreestimar el riesgo de cola si la tail dependence no es empíricamente representativa de la economía argentina.
- **Transparencia**: La advertencia hace explícita una propiedad matemática del método que actualmente no está mencionada en el texto.

#### Implementación mínima (OPCIÓN B — solo texto)

Añadir un párrafo al final de la Sección de Limitaciones del DSA (`07_discusion.tex`, Sección 7.5, línea 162), después del párrafo final que termina con "...un control solo parcial."

**Texto exacto a insertar**:

```latex
Una cuarta advertencia, de naturaleza técnica, concierne a la estructura de dependencia de los \textit{shocks} en la simulación estocástica. La distribución $t$ de Student multivariada con $\nu\approx5.1$ grados de libertad no solo impone colas gruesas marginales, sino también dependencia en colas (\textit{tail dependence}) entre todas las variables por construcción: el coeficiente de dependencia en colas inferior y superior es $\lambda = 2 \cdot T_{\nu+1}\!\left(-\sqrt{(\nu+1)(1-\rho)/(1+\rho)}\right)$, que para $\nu=5.1$ y la correlación QML estimada ($\rho=0.11$) resulta aproximadamente $\lambda\approx0.15$ \citep{demarta2005}. Esta propiedad implica que, incluso bajo la correlación débil estimada por DCC-GARCH, la distribución genera eventos extremos simultáneos en todas las variables con una frecuencia del orden del 15\%, superior a la que una estructura de dependencia empíricamente estimada podría justificar. Las tres robusteces reportadas en este capítulo (30.4\%, 31.9\%, 29.1\%) no testeen la sensibilidad a esta estructura de dependencia de colas, pues todas mantienen la distribución $t$ multivariada; una especificación alternativa con marginales $t$ independientes (sin \textit{tail dependence}, con idéntica curtosis individual) constituye una extensión metodológica que esta tesis especifica como agenda futura. La cifra central del 30.4\% debe interpretarse, en consecuencia, como un límite superior conservador de la probabilidad de insolvencia bajo la hipótesis de co-ocurrencia de eventos extremos.
```

#### Implementación óptima (OPCIÓN A — con robustez estadística adicional)

Si hay acceso al script `src/models/fase6_sostenibilidad_deuda.py` o `src/models/fase7_diagnosticos_robustez.py`:

1. Agregar una función que simule el DSA con shocks $t$ marginales independientes:
   - Mantener la misma matriz de varianzas (mismos $\sigma$ individuales)
   - Reemplazar la cópula-t por shocks $t$ marginales independientes (sin correlación estructural de colas)
   - Ejecutar 1.000 iteraciones y calcular $P(d_{2035}>100\%)$
2. Reportar el resultado en la Tabla `tab:garch_dsa_comparacion` (línea 135 de `07_discusion.tex`) como una fila adicional: "Colas independientes (t marginal): [P%]"
3. Añadir el párrafo de la OPCIÓN B ajustando la redacción para incluir el resultado numérico obtenido.

#### Ubicación exacta

| Elemento | Archivo | Línea(s) |
|---------|---------|---------|
| Sección Limitaciones DSA (`\section{Limitaciones del Análisis}`) | `07_discusion.tex` | 159–163 |
| **Punto de inserción** del párrafo de tail dependence | `07_discusion.tex` | **después de línea 163** |
| Fan Chart (Figura con 30.4%) | `07_discusion.tex` | 73–80 |
| Tabla probabilidades por escenario | `07_discusion.tex` | 88–103 |
| Tabla robustez GARCH (para OPCIÓN A) | `07_discusion.tex` | 133–148 |

#### Dependencias

- Añadir entrada `demarta2005` en `referencias.bib`:
```bibtex
@article{demarta2005,
  author  = {Demarta, Stefano and McNeil, Alexander J.},
  title   = {The t copula and related copulas},
  journal = {International Statistical Review},
  year    = {2005},
  volume  = {73},
  number  = {1},
  pages   = {111--129}
}
```

#### Riesgos

- **OPCIÓN B**: Riesgo bajo. Solo texto con fórmula LaTeX.
- **OPCIÓN A**: Riesgo medio. Requiere ejecutar código Python. Si el resultado con colas independientes es muy distinto al 30.4% (ej. <20%), debe redactarse con más cuidado.

#### Validación

- [ ] El párrafo nuevo contiene la fórmula de tail dependence en LaTeX
- [ ] El párrafo cita `\citet{demarta2005}`
- [ ] El párrafo menciona explícitamente que las tres robusteces existentes no testean la tail dependence
- [ ] Si OPCIÓN A: la nueva fila de la tabla usa el mismo número de simulaciones (1.000)
- [ ] `pdflatex` compila sin errores

---

### HALLAZGO H7 — Veredicto H1a trasplantado directamente desde el marco Ghosh para economías avanzadas

#### Descripción

El paper original de Ghosh et al. (2013) está explícitamente delimitado a "23 advanced economies." La Tabla `tab:mapa_consistencia` en `08_conclusiones.tex` (línea 20) reporta el veredicto de H1a como "**No verificada**: ningún componente significativo." Esta formulación puede leerse como "no hay fatiga fiscal en Argentina," cuando la evidencia solo demuestra que no se verifican las regularidades de Ghosh en una especificación diseñada para economías con acceso continuo a financiamiento en moneda propia. Para Argentina, el mecanismo relevante opera en el espacio de divisas, no en el espacio del resultado primario vs. deuda total.

#### Fundamentación

- Ghosh, A.R., Kim, J.I., Mendoza, E.G., Ostry, J.D. & Qureshi, M.S. (2013). "Fiscal fatigue, fiscal space and debt sustainability in advanced economies." *The Economic Journal* 123(566):F4–F30. (Título y abstract delimitan explícitamente el ámbito a economías avanzadas.)
- Eichengreen, B., Hausmann, R. & Panizza, U. (2007). "Currency mismatches, debt intolerance and original sin." NBER Working Paper 10036. (Marco para interpretar por qué el espacio relevante para Argentina es el de divisas, no el del SF doméstico.)

#### Impacto

- **Interpretación**: El veredicto "No verificada" es correcto para la especificación de Ghosh; la corrección añade el calificativo que delimita ese veredicto a dicha especificación.
- **Coherencia**: Elimina la lectura más fuerte que el Abstract o la Tabla puedan sugerir a un lector no especializado.

#### Implementación mínima

Localizar en `08_conclusiones.tex` la línea 20:

**Texto actual** (columna Veredicto de la fila H1a):
```latex
\textbf{No verificada}: ningún componente significativo
```

**Texto de reemplazo**:
```latex
\textbf{No verificada} en la especificación de \citet{ghosh2013} para economías avanzadas; el umbral relevante para Argentina operaría en el espacio (superávit en divisas / deuda externa / reservas)
```

También localizar en `07_discusion.tex` la Sección 7.2, línea 19, donde se hace referencia a las regularidades de Ghosh, y añadir al final del párrafo:

```latex
Corresponde precisar, adicionalmente, que el modelo de \citet{ghosh2013} fue calibrado sobre 23 economías avanzadas con acceso continuo a financiamiento en moneda propia; su aplicación a Argentina, donde la restricción \textit{binding} es la disponibilidad de divisas y no la curva de Laffer fiscal interna, somete la hipótesis de fatiga fiscal a una especificación potencialmente inadecuada para el mecanismo teórico relevante. El resultado negativo puede reflejar, en consecuencia, inadecuación del marco más que ausencia del fenómeno \citep{eichengreen2007}.
```

#### Ubicación exacta

| Elemento | Archivo | Línea(s) |
|---------|---------|---------|
| Tabla `tab:mapa_consistencia`, fila H1a | `08_conclusiones.tex` | **20** |
| **Texto a modificar en la tabla** | `08_conclusiones.tex` | `\textbf{No verificada}: ningún componente significativo` |
| Párrafo Ghosh en Sección 7.2 | `07_discusion.tex` | **19** |
| **Punto de inserción** del párrafo adicional | `07_discusion.tex` | **al final del párrafo de línea 19** |

#### Dependencias

- Añadir entrada `eichengreen2007` en `referencias.bib` si no existe:
```bibtex
@techreport{eichengreen2007,
  author      = {Eichengreen, Barry and Hausmann, Ricardo and Panizza, Ugo},
  title       = {Currency Mismatches, Debt Intolerance, and the Original Sin: Why They Are Not the Same and Why It Matters},
  institution = {National Bureau of Economic Research},
  year        = {2007},
  number      = {10036},
  type        = {Working Paper}
}
```

#### Riesgos

- **Bajo**: una modificación en la tabla y un párrafo adicional en Cap. 7.
- Verificar que la columna de la tabla tiene espacio suficiente para el texto ampliado (puede requerir ajustar el `p{2.5cm}` de la última columna a `p{3.5cm}`).

#### Validación

- [ ] La fila H1a de la tabla menciona explícitamente "economías avanzadas" de Ghosh
- [ ] La fila no dice solo "ningún componente significativo" sin calificación
- [ ] La Sección 7.2 cita `\citet{eichengreen2007}` en el nuevo párrafo
- [ ] `pdflatex` compila sin errores con la tabla redimensionada

---

## 5. ORDEN ÓPTIMO DE EJECUCIÓN — DAG DE DEPENDENCIAS

```
                     ┌─────────────────────────────────┐
                     │   INICIO: Backup del repositorio │
                     └─────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
   [A] Verificar referencias.bib  [B] Leer archivos     [C] Compilar PDF base
       Añadir entradas faltantes:      exactos con        (sin modificaciones)
       - caner2004                     líneas para        para obtener hash PDF
       - bound1995                     confirmación       de referencia
       - demarta2005                   de ubicaciones
       - eichengreen2007
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  FASE 1: Correcciones H1 y  │
            │  H2 en 06_resultados.tex    │ ← Sin dependencias previas
            └─────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
   [H1] Añadir párrafo     [H2] Añadir párrafo
        Sección 6.4              Sección 6.3
        (línea 247)              (línea 202)
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  FASE 2: Correcciones H5 y  │  ← Sin dependencias con Fase 1
            │  H7 (coherencia interna)    │     (pueden hacerse en paralelo)
            └─────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
   [H5] Reemplazar oración    [H7-tabla] Modificar
        línea 165 en               fila H1a en
        06_resultados.tex          08_conclusiones.tex
              │                       │
              │                [H7-cap7] Añadir párrafo
              │                     línea 19 de
              │                     07_discusion.tex
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  FASE 3: Robustez H6        │  ← Sin dependencias previas
            │  en 07_discusion.tex        │     (puede hacerse en paralelo)
            └─────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
   [H6-B] Añadir párrafo   [H6-A OPCIONAL] Ejecutar
        tail dependence          script Python y
        al final de Sec. 7.5     reportar resultado
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  FASE 4: Corrección         │  ← EJECUTAR ÚLTIMA:
            │  narrativa H3 (Abstract)    │     es el elemento de mayor
            └─────────────────────────────┘     riesgo de edición
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
   [H3-abstract] Modificar   [H3-cap7] Añadir párrafo
        fragmento en              SF_t en
        00_abstract.tex           07_discusion.tex
              │                   (línea 25)
              └───────────┬───────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  FASE 5: Verificación final  │
            │  Compilación + Auditoría     │
            └─────────────────────────────┘
```

### Cambios que pueden hacerse en paralelo

- H1 (Fase 1) y H5 (Fase 2) son independientes entre sí
- H2 (Fase 1) y H7 (Fase 2) son independientes entre sí
- H6 (Fase 3) es independiente de todas las demás

### Cambios que requieren compilación entre fases

- Compilar después de Fase 1 para verificar que `caner2004` y `bound1995` resuelven correctamente
- Compilar después de Fase 3 para verificar que `demarta2005` resuelve correctamente
- Compilación final obligatoria: dos pasadas `pdflatex` + `biber`/`bibtex` + `pdflatex`

---

## 6. CHECKLIST PARA CLAUDE CODE

### Pre-implementación

- [ ] Crear backup de todos los archivos `.tex` antes de editar
- [ ] Compilar el PDF original (sin cambios) y guardar el hash MD5 como referencia
- [ ] Verificar que `referencias.bib` contiene (o no) las entradas: `caner2004`, `bound1995`, `demarta2005`, `eichengreen2007`
- [ ] Añadir a `referencias.bib` las entradas que falten (ver fichas de cada hallazgo)

### Fase 1 — H1: Hansen con I(1)

- [ ] Abrir `06_resultados.tex`
- [ ] Localizar la línea 247 (párrafo del Sup-LM p=0.383)
- [ ] Confirmar que el texto termina con "...una limitación de potencia que el Capítulo \ref{ch:discusion} examina a la luz de la volatilidad estructural del riesgo soberano argentino."
- [ ] Insertar el párrafo de nota metodológica DESPUÉS de esa oración (dentro del mismo párrafo o como párrafo nuevo)
- [ ] Verificar que `\citet{hansen2000}` y `\citet{caner2004}` compilan sin error

### Fase 1 — H2: ETF EMB y Sargan

- [ ] En `06_resultados.tex`, localizar la línea 202 (párrafo Sargan)
- [ ] Confirmar la oración exacta: "La sustitución de instrumento resuelve, en consecuencia, el problema de validez identificado en la versión preliminar de este ejercicio..."
- [ ] Insertar el párrafo sobre limitación del Sargan DESPUÉS de esa oración
- [ ] Verificar que `\citet{bound1995}` y `\citet{blanchard2021}` compilan sin error
- [ ] Compilar `06_resultados.tex` parcialmente y verificar sin errores

### Fase 2 — H5: CUSUM vs. subperíodos

- [ ] En `06_resultados.tex`, localizar la línea 165
- [ ] Confirmar texto exacto: "parecen ser \textit{establemente} débiles a lo largo de todo el período, y no fuertes en un subperíodo y débiles en otro."
- [ ] Reemplazar ese fragmento (desde "parecen ser" hasta "otro.") con el texto de reemplazo especificado
- [ ] Confirmar que la referencia `\ref{sec:sensibilidad_temporal}` resuelve (existe en línea 251)
- [ ] Confirmar que los valores numéricos $0.0373$ y $0.0530$ coinciden con la Tabla `tab:sensibilidad_temporal`

### Fase 2 — H7: Veredicto H1a en Tabla de consistencia

- [ ] En `08_conclusiones.tex`, localizar la línea 20 (fila H1a de la tabla)
- [ ] Confirmar texto actual: `\textbf{No verificada}: ningún componente significativo`
- [ ] Reemplazar ese texto con el texto especificado en la ficha H7
- [ ] Verificar que el ancho de la columna (`p{2.5cm}`) es suficiente; si no, ajustar a `p{3.5cm}`
- [ ] En `07_discusion.tex`, localizar el párrafo de línea 19 (Ghosh tres regularidades)
- [ ] Añadir el párrafo adicional sobre el ámbito de Ghosh y economías avanzadas
- [ ] Verificar que `\citet{eichengreen2007}` compila sin error

### Fase 3 — H6: Tail dependence de la t multivariada

- [ ] Decidir: OPCIÓN A (con script Python) u OPCIÓN B (solo texto)
- [ ] En `07_discusion.tex`, localizar el final de la Sección de Limitaciones (línea 163)
- [ ] Confirmar que la sección termina con "...un control solo parcial."
- [ ] Insertar el párrafo de tail dependence DESPUÉS de esa oración (como párrafo nuevo)
- [ ] Verificar la fórmula LaTeX de tail dependence: `$\lambda = 2 \cdot T_{\nu+1}\!\left(-\sqrt{(\nu+1)(1-\rho)/(1+\rho)}\right)$`
- [ ] Verificar que `\citet{demarta2005}` compila sin error
- [ ] Si OPCIÓN A: confirmar que el resultado Python está disponible antes de insertar el párrafo

### Fase 4 — H3: Abstract y Sección 7.2

- [ ] Abrir `00_abstract.tex` con extremo cuidado (una sola línea de texto comprimido)
- [ ] Localizar el fragmento exacto: "sino por canales exógenos a él --depreciación real y efecto de valuación, licuación inflacionaria y reestructuraciones con quita--, en línea con lo que anticipa el Paradigma de la Restricción Externa para una economía bimonetaria."
- [ ] Reemplazar con la versión modificada especificada en la ficha H3
- [ ] Verificar que el Abstract resultante mantiene todas las cifras: $\rho=-0.0071$, $p=0.564$, $p=0.383$, $F=23.39$, $p=0.576$, $30.4\%$, $29.1\%$
- [ ] En `07_discusion.tex`, localizar el final del párrafo de línea 25 (termina con "...especifica esos diseños.")
- [ ] Añadir el párrafo sobre SF_t y agenda futura DESPUÉS de esa oración
- [ ] Verificar que `\ref{sec:agenda_futura}` y `\ref{sec:restriccion_intertemporal}` resuelven correctamente

### Fase 5 — Verificación final

- [ ] Compilar PDF completo: `pdflatex main.tex` (o el archivo raíz del proyecto)
- [ ] Ejecutar `biber main` (o `bibtex main`) para actualizar bibliografía
- [ ] Compilar nuevamente: `pdflatex main.tex`
- [ ] Compilar por tercera vez: `pdflatex main.tex` (resolver referencias cruzadas residuales)
- [ ] Verificar que el PDF no contiene `??` en referencias ni citaciones
- [ ] Verificar el Abstract en el PDF: leer las cifras estadísticas y confirmar que coinciden con el original
- [ ] Verificar la Tabla `tab:mapa_consistencia` en el PDF: confirmar fila H1a modificada
- [ ] Verificar la Sección 6.4 en el PDF: confirmar párrafo nuevo al final de Hansen
- [ ] Verificar la Sección 6.3 en el PDF: confirmar párrafo nuevo sobre Sargan
- [ ] Verificar la Sección 6 (párrafo CUSUM) en el PDF: confirmar que "establemente débiles" ya no aparece sin calificación
- [ ] Verificar la Sección 7.2 en el PDF: confirmar párrafo sobre SF_t y agenda futura
- [ ] Verificar la Sección 7.5 en el PDF: confirmar párrafo sobre tail dependence
- [ ] Verificar que el número total de páginas del PDF no cambió más de ±3 páginas
- [ ] Calcular hash MD5 del PDF final y comparar con el original (deben ser distintos)

---

## 7. CRITERIOS DE ACEPTACIÓN

### H1 — ACEPTADO cuando:

1. Existe un párrafo nuevo al final de la Sección 6.4 que contiene las palabras "estacionariedad" y "Assumption" con referencia a Hansen (2000)
2. El párrafo contiene la cita `\citet{caner2004}`
3. El p-value 0.383 permanece en la Tabla `tab:hansen` sin modificación
4. `pdflatex` compila sin `undefined citation` para `caner2004`

### H2 — ACEPTADO cuando:

1. Existe un párrafo nuevo en la Sección 6.3 que contiene las palabras "potencia" y "Sargan"
2. El párrafo cita `\citet{bound1995}`
3. El estadístico Sargan (0.313, p=0.576) permanece en la Tabla `tab:iv2sls` sin modificación
4. `pdflatex` compila sin `undefined citation` para `bound1995`

### H3 — ACEPTADO cuando:

1. En el Abstract, la palabra "interpretación" (o equivalente) aparece antes del fragmento sobre canales exógenos, o el fragmento incluye "especificada como agenda futura"
2. En Sección 7.2, existe un párrafo que menciona "SF_t" y "agenda futura"
3. Todas las cifras estadísticas del Abstract son idénticas a las del original (verificación numérica literal)
4. `pdflatex` compila sin errores

### H5 — ACEPTADO cuando:

1. La frase "establemente débiles a lo largo de todo el período, y no fuertes en un subperíodo y débiles en otro" ya NO aparece literalmente en el PDF
2. El texto de reemplazo incluye los valores $0.0373$ y $0.0530$ con sus p-values
3. La Figura `fig:cusum` permanece sin modificación
4. `pdflatex` compila sin errores

### H6 — ACEPTADO cuando:

1. Existe un párrafo nuevo en la Sección 7.5 que contiene la palabra "tail dependence" y la fórmula $\lambda$
2. El párrafo cita `\citet{demarta2005}`
3. La cifra 30.4% permanece como el resultado principal del DSA (visible en Abstract y Sección 7.3)
4. `pdflatex` compila sin `undefined citation` para `demarta2005`

### H7 — ACEPTADO cuando:

1. La fila H1a de `tab:mapa_consistencia` contiene la referencia a "economías avanzadas" de Ghosh
2. La fila H1a NO dice solo "ningún componente significativo" sin calificación
3. La Sección 7.2 o 7.3 contiene referencia a que el ámbito de Ghosh es economías avanzadas
4. `pdflatex` compila sin errores

---

## 8. PROTOCOLO DE AUDITORÍA FINAL

### 8.1 Consistencia metodológica

| Verificación | Método | Criterio de aprobación |
|-------------|--------|------------------------|
| H1: Párrafo Hansen presente | Buscar texto "estacionariedad" + "Assumption" en Sección 6.4 del PDF | Presente |
| H2: Párrafo Sargan presente | Buscar texto "potencia" + "Bound" en Sección 6.3 del PDF | Presente |
| H3: Abstract equilibrado | Buscar "interpretación" antes del fragmento exógenos | Presente |
| H5: "Establemente débiles" eliminado | `grep "establemente débiles" 06_resultados.tex` | Sin resultado |
| H6: Tail dependence advertida | Buscar "$\lambda$" o "tail dependence" en Sección 7.5 del PDF | Presente |
| H7: Veredicto H1a calificado | Revisar fila H1a de `tab:mapa_consistencia` en PDF | Contiene "avanzadas" |

### 8.2 Consistencia estadística

Verificar que las siguientes cifras aparecen idénticas antes y después de la implementación:

| Estadístico | Valor esperado | Ubicación |
|------------|----------------|-----------|
| $\rho$ DOLS | $-0.0071$ ($p=0.564$) | `tab:dols`, Abstract |
| Sargan J-stat | $0.313$ ($p=0.576$) | `tab:iv2sls`, Abstract |
| Sup-LM p-value | $p=0.383$ | `tab:hansen`, Abstract |
| F primera etapa | $23.39$ | `tab:iv2sls`, Abstract |
| DSA Referencia | $30.4\%$ | `fig:fan_chart_final`, Abstract |
| DSA GARCH parcial | $31.9\%$ | `tab:garch_dsa_comparacion` |
| DSA [[dcc-garch-dynamic-correlation|DCC-GARCH]] | $29.1\%$ | `07_discusion.tex` línea 157 |
| n DOLS | $n=78$ | `tab:dols` |
| n IV-2SLS | $n=73$ | `tab:iv2sls` |

### 8.3 Consistencia bibliográfica

- [ ] Todas las citas nuevas (`caner2004`, `bound1995`, `demarta2005`, `eichengreen2007`) resuelven en el PDF sin `??`
- [ ] La lista de referencias al final del PDF contiene estas cuatro entradas nuevas
- [ ] Las entradas nuevas siguen el formato bibliográfico del resto del documento

### 8.4 Consistencia narrativa

- [ ] El Abstract no presenta contradicciones internas con el cuerpo de la tesis
- [ ] La Sección 7.2 no presenta contradicciones internas con el Abstract modificado
- [ ] El párrafo CUSUM modificado no contradice la Figura `fig:cusum` ni la Sección 6.5
- [ ] La fila H1a modificada no contradice el desarrollo del Cap. 6 sobre Hansen

### 8.5 Referencias cruzadas e integridad estructural

- [ ] Todas las etiquetas `\ref{}` del documento resuelven (no hay `??` en el PDF)
- [ ] La numeración de tablas y figuras no cambió (verificar Tabla 6.5 = `tab:sensibilidad_temporal`, Figura 6.2 = `fig:cusum`)
- [ ] La tabla de contenido refleja correctamente las secciones modificadas
- [ ] El Abstract aparece en la posición correcta del documento

### 8.6 Compilación y reproducibilidad

```powershell
# Secuencia de compilación verificada
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex

# Verificar ausencia de errores LaTeX
# grep "Error" main.log | grep -v "^!" 

# Hash del PDF final
Get-FileHash main.pdf -Algorithm MD5
```

- [ ] La compilación completa finaliza sin errores (`! Fatal error` ausente en `.log`)
- [ ] El número de warnings sobre referencias no definidas es 0
- [ ] El hash MD5 del PDF final difiere del hash MD5 original (hay cambios)
- [ ] El tamaño del PDF final está dentro de ±10% del tamaño original

---

## APÉNDICE — Entradas BibTeX a añadir

```bibtex
@article{caner2004,
  author  = {Caner, Mehmet and Hansen, Bruce E.},
  title   = {Instrumental variable estimation of a threshold model},
  journal = {Journal of Business \& Economic Statistics},
  year    = {2004},
  volume  = {22},
  number  = {3},
  pages   = {304--311},
  doi     = {10.1198/073500104000000366}
}

@article{bound1995,
  author  = {Bound, John and Jaeger, David A. and Baker, Regina M.},
  title   = {Problems with instrumental variables estimation when the
             correlation between the instruments and the endogenous
             explanatory variable is weak},
  journal = {Journal of the American Statistical Association},
  year    = {1995},
  volume  = {90},
  number  = {430},
  pages   = {443--450},
  doi     = {10.1080/01621459.1995.10476536}
}

@article{demarta2005,
  author  = {Demarta, Stefano and McNeil, Alexander J.},
  title   = {The t copula and related copulas},
  journal = {International Statistical Review},
  year    = {2005},
  volume  = {73},
  number  = {1},
  pages   = {111--129},
  doi     = {10.1111/j.1751-5823.2005.tb00254.x}
}

@techreport{eichengreen2007,
  author      = {Eichengreen, Barry and Hausmann, Ricardo and Panizza, Ugo},
  title       = {Currency Mismatches, Debt Intolerance, and the Original Sin:
                 Why They Are Not the Same and Why It Matters},
  institution = {National Bureau of Economic Research},
  year        = {2007},
  number      = {10036},
  type        = {Working Paper},
  note        = {Revisión de 2007 del Working Paper original de 2002}
}
```
