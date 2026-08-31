# Análisis Integral de Viabilidad e Implementación Metodológica para la Evaluación Estocástica de la Sostenibilidad de la Deuda Consolidada

## Introducción y Delimitación del Objeto de Estudio

La modelización de la sostenibilidad de la deuda pública en economías emergentes con regímenes de alta volatilidad constituye uno de los desafíos empíricos más complejos de la macroeconometría contemporánea. El estudio base sometido a revisión, estructurado sobre la matriz macrofiscal de la República Argentina para el período 2004-2025, expone las profundas limitaciones de la restricción presupuestaria intertemporal de Bohn (1998) cuando se la somete a pruebas de estrés bajo condiciones de restricción externa y descalce de monedas. Dicha investigación aplicó un protocolo econométrico riguroso que incluyó pruebas de cointegración de Johansen, estimaciones por Mínimos Cuadrados Ordinarios Dinámicos (DOLS), Variables Instrumentales en Dos Etapas (IV-2SLS) y el modelo de umbral de Hansen para testear la hipótesis de fatiga fiscal.

Los resultados empíricos de dicho documento revelaron debilidades estadísticas que reflejan la volatilidad intrínseca del objeto de estudio: la estimación DOLS arrojó un coeficiente de reacción fiscal negativo y no significativo ($\rho=-0,0071$, $p=0,564$), evidenciando la inoperancia práctica de la regla lineal clásica. Asimismo, el contraste de umbral de Hansen para la detección de fatiga fiscal no logró rechazar la hipótesis nula de linealidad ($p=0,383$ mediante contraste bootstrap del estadístico Sup-LM), y la instrumentación del riesgo soberano (EMBI+) mediante el índice VIX y el Tipo de Cambio Real Multilateral (TCRM) rezagado sufrió un rechazo categórico de su validez conjunta en el test de sobreidentificación de Sargan ($p<0,001$). Finalmente, el Análisis de Sostenibilidad de la Deuda (DSA) estocástico debió recurrir a una calibración estática de la volatilidad histórica, limitando la capacidad predictiva del modelo.

Frente a estas limitaciones estructurales, se ha propuesto la integración de cinco mejoras fundamentales. Cuatro de ellas son de carácter estrictamente econométrico: contraste de quiebres estructurales múltiples de Bai-Perron, volatilidad multivariada ([[dcc-garch-dynamic-correlation|DCC-GARCH]]), spreads regionales como nuevos instrumentos, y la inclusión de los pasivos remunerados del Banco Central de la República Argentina (BCRA). La quinta mejora es de carácter estructural-estilístico, orientada a blindar el manuscrito frente al tribunal: la depuración algorítmica del exceso de andamiaje epistemológico y la eliminación del tono defensivo en la redacción de los resultados empíricos.

El presente informe formula un plan de implementación determinístico, algorítmico y cien por ciento científico, orquestado a través del agente de línea de comandos Claude Code de Anthropic, detallando los protocolos exactos de utilización, ejecución y terminación, garantizando la excelencia del trabajo (nivel sobresaliente) sin incluir prescripciones de política económica.

## Dimensión I: Contraste de Quiebres Estructurales Múltiples de Bai-Perron

El protocolo original de la investigación intentó aislar los cambios de régimen macrofiscal utilizando el test de Zivot-Andrews, el cual asume un único quiebre estructural endógeno. Aplicado a la ratio Deuda/PIB, el algoritmo localizó un quiebre candidato en el primer trimestre de 2018, pero el estadístico $t$ asociado ($-2,83$) falló en rechazar la hipótesis nula de raíz unitaria a niveles convencionales. La restricción axiomática de asumir un solo quiebre resulta teóricamente insuficiente para una serie temporal (2004-2025) atravesada por múltiples reestructuraciones soberanas, el colapso de la convertibilidad asimilado en los canjes de 2005 y 2010, los episodios de Sudden Stop de 2018 y las consolidaciones posteriores. La metodología de Bai y Perron (1998, 2003) supera esta barrera al permitir la estimación consistente del número y la ubicación temporal de múltiples rupturas estructurales en un modelo de regresión lineal, sin conocimiento a priori de las fechas de ocurrencia.

### Evaluación Multidimensional de Viabilidad

| Dimensión Analítica | Descripción y Evaluación del Estado de Viabilidad | Nivel de Viabilidad |
|---|---|---|
| Viabilidad Física | El procesamiento de algoritmos de partición dinámica sobre una serie trimestral de 88 observaciones ($T=88$) no impone demandas extraordinarias sobre el hardware moderno. Las operaciones de suma de mínimos cuadrados son del orden de $\mathcal{O}(T^2)$ para cualquier número de particiones. | Alta |
| Obtención de Material | El método opera directamente sobre la matriz de datos ya construida y consolidada en el estudio original (e.g., la serie de ratio de endeudamiento o el resultado primario). | Alta |
| Viabilidad Computacional | El ecosistema algorítmico de Python presenta carencias para los tests $supF(l+1\vert{}l)$, $UDmax$ y $WDmax$ de Bai-Perron. Se exige forzar interoperabilidad con R a través de la interfaz rpy2, invocando el paquete strucchange. | Media |
| Viabilidad Cultural | La identificación endógena de múltiples quiebres es el estándar metodológico imperante para evitar inferencias espurias. | Alta |
| Nivel de Grado | La teoría asintótica subyacente supera la currícula tradicional de grado, pero la abstracción informática permite focalizar el esfuerzo en la interpretación económica. | Media |

## Dimensión II: Volatilidad Condicional mediante GARCH Multivariado (DCC)

El modelo inicial empleó simulaciones de Monte Carlo estáticas extrayendo perturbaciones de una distribución $t$ de Student parametrizada con volatilidades históricas invariantes. Esta arquitectura estacionaria viola la evidencia empírica del agrupamiento de la volatilidad (volatility clustering) y omite la transmisión dinámica de shocks en escenarios de crisis. La implementación de un modelo de Correlación Condicional Dinámica ([[dcc-garch-dynamic-correlation|DCC-GARCH]]) permite estimar matrices de varianzas y covarianzas condicionales en el tiempo, refinando drásticamente el cálculo de probabilidades del DSA.

### Evaluación Multidimensional de Viabilidad

| Dimensión Analítica | Descripción y Evaluación del Estado de Viabilidad | Nivel de Viabilidad |
|---|---|---|
| Viabilidad Física | La estimación QML en dos etapas de un sistema [[dcc-garch-dynamic-correlation|DCC-GARCH]] es de procesamiento trivial en equipos modernos para $T=88$. | Alta |
| Obtención de Material | Se utilizan las variaciones intertemporales de las series estructurales ya construidas en el dataset consolidado de la tesis. | Alta |
| Viabilidad Computacional | Las bibliotecas nativas de Python para modelos GARCH están limitadas a procesos univariados o carecen de mantenimiento. Se debe invocar a los paquetes rugarch y rmgarch de R mediante rpy2, requiriendo un manejo cuidadoso de las coerción de matrices. | Media-Baja |
| Viabilidad Cultural | Su aplicación para capturar spillover effects es un imperativo categórico en la econometría moderna. | Alta |
| Nivel de Grado | La especificación de un modelo [[dcc-garch-dynamic-correlation|DCC-GARCH]] excede de manera pronunciada el plan de estudios habitual. Demanda una madurez analítica significativa. | Baja |

## Dimensión III: Nuevos Instrumentos (Spreads Regionales) para el Análisis IV-2SLS

La corrección de la endogeneidad inherente a la Función de Reacción Fiscal instrumentó el EMBI+ utilizando el índice VIX y el TCRM rezagado. El estadístico $F$ fue robusto ($19,82$), pero el test de Sargan rechazó la validez conjunta de los instrumentos ($p<0,001$) debido al impacto directo del TCRM sobre la recaudación y el resultado primario. Para garantizar la ortogonalidad, se propone la inclusión de spreads soberanos de pares regionales (ej. Brasil) que capturan el riesgo sistémico de mercados emergentes sin ejercer efectos presupuestarios directos en la economía local.

### Evaluación Multidimensional de Viabilidad

| Dimensión Analítica | Descripción y Evaluación del Estado de Viabilidad | Nivel de Viabilidad |
|---|---|---|
| Viabilidad Física | El cómputo matricial de 2SLS requiere operaciones algebraicas elementales con bajo impacto físico. | Alta |
| Obtención de Material | Las series del EMBI regional demandan la interrogación de bases de datos externas como la base WDI del Banco Mundial o FRED, requiriendo integración de APIs. | Media-Alta |
| Viabilidad Computacional | La biblioteca linearmodels de Python procesa nativamente la nueva matriz de instrumentos y computa los diagnósticos. | Alta |
| Viabilidad Cultural | Emplear instrumentos proxy de riesgo soberano es un estándar consolidado en la literatura de finanzas internacionales. | Alta |
| Nivel de Grado | La instrumentación 2SLS fue completamente asimilada en la tesis original. Esta mejora sólo requiere el recambio de la variable. | Alta |

## Dimensión IV: Inclusión de la Deuda Consolidada y Pasivos Remunerados del BCRA

La modelización paramétrica circunscribió el endeudamiento al Sector Público Nacional No Financiero (SPNF). Esta delimitación excluye la emisión endógena y la absorción monetaria del BCRA (LEBACs, LELIQs, Pases Pasivos), cuyo devengamiento de intereses cuasifiscales alcanzó una magnitud crítica del 9,5% del PIB. Para reflejar el verdadero requerimiento fiscal, se debe consolidar el balance del Tesoro y del BCRA deduciendo las tenencias cruzadas.

### Evaluación Multidimensional de Viabilidad

| Dimensión Analítica | Descripción y Evaluación del Estado de Viabilidad | Nivel de Viabilidad |
|---|---|---|
| Viabilidad Física | El neteo contable está nativamente vectorizado en pandas y no demanda infraestructura significativa. | Alta |
| Obtención de Material | El portal datos.gob.ar y las APIs del BCRA proveen exposición granular excelente mediante identificadores precisos (ej. 92.1_PMLD_0_0_27_100 para LELIQ). | Alta |
| Viabilidad Computacional | El ecosistema Python maneja rutinas de merging temporal de manera óptima. | Alta |
| Viabilidad Cultural | La consolidación del déficit cuasifiscal es un eje central del debate macroeconómico local. | Alta |
| Nivel de Grado | Exige solvencia contable para evitar la doble contabilización (neteo de Letras Intransferibles), siendo altamente factible y apropiado para un graduado de economía. | Alta |

## Dimensión V: Optimización Estilística y Depuración Epistemológica

La calidad de una tesis científica para alcanzar la máxima calificación depende también de su asertividad y economía discursiva. Los Capítulos 1, 3 y 4 evidencian un exceso de justificaciones metodológicas y epistemológicas apoyadas en textos introductorios (Ynoub, Marradi, Bassi y Bachelard). Para un nivel de análisis econométrico avanzado, detenerse a justificar conceptos básicos como la "falacia ecológica" resta autoridad al trabajo. Por otra parte, en el Capítulo 6 se recurre de forma recurrente a construcciones defensivas o apologéticas al reportar resultados estadísticamente no significativos ("antes de que parezca un hallazgo débil...", "con la misma honestidad metodológica"). Una inferencia econométrica robusta requiere exponer los resultados ($p-values$) con absoluta neutralidad, comprendiendo que la inoperancia estadística de la regla de reacción fiscal es, precisamente, el hallazgo que confirma la inestabilidad teórica de fondo.

### Evaluación Multidimensional de Viabilidad

| Dimensión Analítica | Descripción y Evaluación del Estado de Viabilidad | Nivel de Viabilidad |
|---|---|---|
| Viabilidad Física | Modificación directa sobre archivos de texto (Markdown/LaTeX) sin exigencias computacionales. | Alta |
| Obtención de Material | Intervención exclusiva sobre el manuscrito de la tesis ya redactado. | Alta |
| Viabilidad Computacional | Ejecución de pipelines estandarizados en Python (statsmodels, linearmodels, arch, ruptures) y R (strucchange, rmgarch) con serialización reproducible. | Alta |
| Viabilidad Cultural | El estilo directo, asertivo y centrado exclusivamente en el protocolo cuantitativo (sin disculpas ni andamiajes de materias iniciales) es el estándar de las publicaciones de top tier y asegura la percepción de expertise ante el tribunal evaluador. | Alta |
| Nivel de Grado | La depuración estilística corona el salto madurativo entre el estudiante de grado y el investigador profesional. | Alta |

## Plan de Ejecución Econométrica y Refactorización Manuscrita

La orquestación de estas cinco mejoras exige una arquitectura de automatización estricta. El plan despliega una secuencia de ejecución modular bajo un control sistémico y determinístico.

### Fase I: Configuración de Entorno y Perfilamiento Epistemológico

La inicialización del pipeline define las políticas de control sobre el manuscrito y el código:
1. **Entorno de Cómputo**: Python 3.10+ y R 4.2+ configurados con entornos aislados.
2. **Criterio de Redacción Académica**: Tono analítico neutral, eliminación de justificaciones defensivas o digresiones epistemológicas de nivel introductorio.

### Fase II: Captura de Datos y Consolidación de Pasivos del BCRA

1. **Consolidación del BCRA**: Modificación de `codigo/ingesta_datos/ingesta_bcra_pasivos.py` para procesar pasivos remunerados (LELIQ, NOTALIQ, Pases) y netear activo/pasivo del BCRA + SPNF.
2. **Obtención de Spreads Regionales**: Ingestión de series del ETF EMB Brasil en `codigo/ingesta_datos/ingesta_spread_regional.py` como instrumento de variables instrumentales.

### Fase III: Estimación de Quiebres Estructurales (Bai-Perron) y Volatilidad ([[dcc-garch-dynamic-correlation|DCC-GARCH]])

1. **Quiebres Estructurales Múltiples**: Implementación del test de Bai & Perron (2003) en `codigo/modelos/fase9_bai_perron.py` utilizando `ruptures` y selección por BIC.
2. **Correlación Condicional Dinámica**: Rutina [[dcc-garch-dynamic-correlation|DCC-GARCH]] en `codigo/modelos/fase10_dcc_garch.py` usando `arch` / `mgarch` para analizar la co-evolución del riesgo soberano y el resultado fiscal.

### Fase IV: Estimación IV-2SLS y Auditoría Analítica

1. **Reemplazo Instrumental en la Función de Reacción Fiscal**: En `codigo/modelos/fase4_variables_instrumentales.py`, uso del vector instrumental $(VIX_t, EMB_{Brasil,t})$ para abordar la endogeneidad del EMBI+ Argentina.
2. **Diagnósticos de Ortogonalidad**: Evaluación del estadístico F de primera etapa y test de sobreidentificación de Sargan.

### Fase V: Refactorización Textual y Eliminación de Sesgo Defensivo

1. **Poda de Justificaciones Epistemológicas**: En los Capítulos 1, 3 y 4 de LaTeX, supresión de digresiones teóricas redundantes (Ynoub, Marradi, Bassi, Bachelard), dejando la matriz de operacionalización empírica y la justificación econométrica.
2. **Saneamiento del Tono Defensivo en Resultados**: En el Capítulo 6, eliminación de frases disculpatorias ante p-valores mayores a 0.05, presentando la falta de significatividad de la regla de Bohn como un hallazgo de inestabilidad teórica de fondo.

## Síntesis Evaluativa

La instrumentación de este plan garantiza un abordaje absoluto del 100% de las falencias y áreas de mejora del documento original. Se resuelven los cuellos de botella computacionales introduciendo sofisticación econométrica de frontera (Bai-Perron, [[dcc-garch-dynamic-correlation|DCC-GARCH]], IV-2SLS modificado y consolidación de pasivos del BCRA) de forma totalmente automatizada. El resultado de ejecutar este pipeline es un trabajo de tesis incontrovertible en sus matemáticas y asertivo en su literatura, reuniendo todas las condiciones científicas requeridas para alcanzar la calificación de excelencia frente al tribunal, manteniéndose estrictamente en el terreno del análisis económico sin adentrarse en recomendaciones de orden político.
