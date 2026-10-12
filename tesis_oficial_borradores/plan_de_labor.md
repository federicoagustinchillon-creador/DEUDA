# Plan de labor de la tesis

Documento de trabajo del grupo. Última actualización: 11 de octubre de 2026.

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


## 2b. Inventario técnico: qué tenemos y qué se hace con cada cosa

Hay mucho hecho. La mayor parte se reutiliza; lo que falta son cuatro piezas.

### Datos

| Qué hay | Archivo | Qué se hace |
|---|---|---|
| Base 1996-2025 (120 trimestres): deuda/PIB del SPNF, resultado primario/PIB, PIB real, brecha del producto, TCRM, EMBI+, VIX | `datos/dataset_consolidado_1996_2025.csv` | Se reutiliza. Hay que sumarle la deuda consolidada y la tasa de la FED. |
| Empalmes pre-2004 (deuda, resultado primario y PIB real, por el método de Denton) y TCRM de 1996 extrapolado | `codigo/ingesta_datos/empalme_*.py`, `construir_dataset_1996_2025.py` | Se reutiliza. |
| Pasivos remunerados del BCRA, 2004-2025, de la API del BCRA (LEBAC/NOBAC, Leliq/Notaliq, pases) | `codigo/ingesta_datos/ingesta_bcra_pasivos.py`, `datos/procesados/bcra_pasivos_trimestral.csv` | Se adapta: hay que llevarla a 1996 y revisar el denominador (ver abajo). |
| VIX y volatilidad del Bovespa, 1996-2025 | `ingesta_instrumentos_1996_2025.py` | El VIX se reutiliza como variable exógena. |
| Spread soberano histórico 1983-2025 | `fase22_*` | Queda fuera, como ya se había decidido. |

**Problema detectado con los pasivos del BCRA.** Nuestra serie da 9,5% del PIB en 2022-2023.
El FMI da 18,4% en 2023 (16,2% solo en pesos) sobre el PIB promedio del año, y 11,0% sobre el PIB
anualizado del cuarto trimestre (FMI, 2025, anexo II). La diferencia viene del denominador, que
pesa mucho con inflación alta. Hay que elegir uno, justificarlo y usar el mismo para la deuda del
SPNF y para la del BCRA.

### Modelos

| Qué hay | Archivo | Qué se hace |
|---|---|---|
| Pruebas de raíz unitaria (ADF, KPSS, DF-GLS) y de quiebre único (Zivot-Andrews) | `fase1_estacionariedad.py` | Se reutiliza y se corre sobre la deuda consolidada. |
| Quiebres múltiples de Bai-Perron, con implementación propia | `fase9_bai_perron.py`, `bai_perron.py` | Se reutiliza. Los quiebres pasan a ser dummies del SVARX. |
| Johansen y VECM (versión anterior) | `fase2`, `fase3b`, `fase16` | Reemplazados por la ecuación fiscal del SVARX (`fase24`), estimada sobre la deuda consolidada con datos reales. Su reacción fiscal da 0,019 (p = 0,005), significativa, a diferencia del VECM anterior. |
| SVAR restringido: brecha del producto, resultado primario, EMBI+, TCRM y deuda, con elasticidad cíclica de 0,25 citada y *bootstrap* de 1.000 réplicas | `fase19_var_restringido_macro.py`, `fase23_reestimacion_1996_2025.py` | Es el núcleo. Se extiende a SVARX: el VAR de statsmodels ya admite variables exógenas, y la identificación se aplica igual sobre los residuos. |
| Selección de rezagos, multicolinealidad y diagnósticos de residuos | `fase12`, `fase7` | Se reutiliza para validar el SVARX. |
| Grados de libertad de la t de Student, estimados por momentos (nu = 4,8) | `fase17_calibracion_nu_dsa.py` | Se reutiliza. |
| Umbral de Hansen y TVECM | `fase5`, `fase13`, `fase21` | Queda como resultado complementario de H1a. |
| Simulación (DSA) | `fase6_sostenibilidad_deuda.py` | **Se rehace en buena parte** (ver abajo). Se reutilizan la identidad con separación de monedas, la t de Student y los gráficos. |
| DOLS, variables instrumentales, CIR, DCC-GARCH, dependencia de colas, histórico 1983-2025 | `fase3`, `fase4`, `fase10`, `fase11`, `fase14`, `fase20`, `fase22` | Quedan fuera, como ya se había decidido. |

**Por qué hay que rehacer la simulación.** Revisada con el criterio de que todo número tiene que
estar justificado, tiene cuatro problemas:

1. Los desvíos de los shocks (1,5%, 4%, 5%, 2% y 15%) están "calibrados a mano", según el propio
   código.
2. Los parámetros del escenario base (resultado primario 1,5%, crecimiento 3,5%, tasa en pesos 6%,
   tasa en dólares 7,5%) no tienen fuente.
3. Los shocks son independientes año a año: el SVAR solo aporta las correlaciones, no su
   dinámica. Así no hay efectos conjuntos, que es lo que pide la pregunta.
4. Usa el criterio de 100% del PIB, que salió de las hipótesis.

La versión nueva simula directamente desde el SVARX estimado (remuestreo de residuos, con sus
rezagos), acumula la deuda con la identidad y calcula las métricas del FMI. Para el escenario base
hay que adoptar un sendero con fuente, por ejemplo el del propio FMI (2025), lo que además permite
comparar con su resultado.

### Las cuatro piezas que faltaban (hechas)

1. Deuda consolidada 1996-2025 con un denominador coherente: bruta, neta a valor libros y neta con las Letras Intransferibles a valor nominal (la principal).
2. Tasa de la FED y tasa sombra de Wu y Xia, trimestrales.
3. SVARX nuevo (`fase24_svarx_1996_2025.py`).
4. Simulación desde el SVARX con la métrica del FMI (`fase25_simulacion_dsa_svarx.py`), más la variante con shocks a la manera del FMI y su diagnóstico (`fase25b_diagnostico_abanico_fmi.py`).

## 3. Decisiones tomadas

| N.° | Decisión | Justificación |
|---|---|---|
| 1 | La Introducción de Santiago del 7/10 es la base, completada con la Justificación y los objetivos específicos del texto LaTeX. | Es la versión más reciente y ya fue revisada. |
| 2 | Todo el trabajo empírico (modelo y simulación) se hace sobre la deuda consolidada SPNF y BCRA. | Es el perímetro que plantea la pregunta de investigación, y el FMI considera deuda pública a los pasivos del banco central cuando pueden financiar al Tesoro o implican riesgo fiscal (FMI, 2021, anexo II). |
| 3 | El modelo es un SVARX: la deuda consolidada es una variable más del sistema, con la tasa de la FED y la volatilidad global como variables exógenas. | Permite efectos conjuntos: la deuda responde a los shocks y a su vez los afecta. Es lo que hace falta para medir cómo un shock de la FED vuelve sobre la deuda a través del riesgo país y del tipo de cambio. |
| 4 | La identificación principal es el SVAR restringido por teoría que ya existe. El ordenamiento de Cholesky queda solo como prueba de robustez. | No hay razón teórica para ordenar el EMBI+ y el TCRM entre sí, y esa justificación ya fue aprobada por el director. |
| 5 | H1b contrasta si nuestra probabilidad de no estabilización supera la del FMI, con el escenario base del FMI. Desde el 11/10/2026 se usa el análisis más reciente (FMI, 2026: 1,0% a mediano plazo y menos de 3% a diez años); el de abril de 2025 (3%) queda como robustez. | Es la métrica del FMI (FMI, 2021, párr. 53) y el umbral es su propio diagnóstico. El escenario y el umbral se toman siempre del mismo informe. Se contrasta con el intervalo de 90% del *bootstrap* (unilateral al 5%). |
| 6 | El criterio "deuda mayor a 100% del PIB" sale de las hipótesis. | No tiene fuente que lo justifique. |
| 7 | El área de vacancia se reformula. | El marco del FMI sí admite incluir los pasivos del banco central (FMI, 2021, anexo II), pero en su análisis de Argentina corre las herramientas sobre la deuda federal bruta y muestra la consolidada solo como cuadro (FMI, 2025, anexo II, cuadro 2). La vacancia pasa a ser la combinación de tres aspectos: identificación estructural, un shock externo identificado y la estimación sobre el perímetro consolidado. |
| 8 | El canal cuasifiscal del shock de la FED se redacta en pasado. | Los pasivos remunerados del BCRA se redujeron a niveles mínimos desde 2024. |
| 9 | El módulo de balanza de pagos (exportaciones, importaciones, inversión extranjera directa, fuga de capitales, renovación de vencimientos, necesidades de financiamiento) queda fuera y pasa a investigación futura. | No está especificado, y su tamaño es el de otra tesis. |
| 10 | Todo umbral, corte o tamaño de shock tiene que tener una justificación escrita, propia o citada. | Criterio del grupo. |
| 11 | Una sola muestra de estimación: todas las especificaciones se estiman sobre la misma muestra efectiva, 1998T2-2025T4, y los primeros trimestres de 1996-1998 se usan como condiciones iniciales de los rezagos. | Los criterios de información solo se pueden comparar entre órdenes sobre un mismo período (Lütkepohl, 2005, sec. 4.3), y así la deuda neta, la neta en libros y la bruta se estiman sobre los mismos trimestres. |
| 12 | H1b se contrasta a cinco años (2030) y a diez años (2035). | Son los dos horizontes del FMI (2026): el abanico de mediano plazo y el de diez años, que termina en 2035. |
| 13 | El shock de la FED se mide de dos maneras: un desvío estándar (0,50 puntos) y el ciclo de 2022-2023 (5,25 puntos). | Convención de la literatura de VAR y episodio histórico reciente. |
| 14 | La especificación principal es el SVARX; los shocks a la manera del FMI se informan como comparación. La elección se fijó antes de ver los resultados. | Solo los shocks identificados permiten contrastar H1a (bloques de shocks) y H2 (shock externo). |
| 15 | El canal de tasas en pesos se informa como variante: el riesgo país también reprecia la deuda en pesos. | Tasa de interés del país (Neumeyer y Perri, 2005; Uribe y Yue, 2006). No hay una tasa en pesos homogénea para 1996-2025 que permita sumarla al VAR. |

## 4. Etapas

Estado: **hecho**, **en curso** o **pendiente**.

### Etapa 1. Introducción (hecha; en revisión del grupo)

- Borrador corregido, con la H1a de Santiago, H1b a cinco y diez años y el tamaño del shock de la FED definido.

### Etapa 2. Antecedentes y área de vacancia (hecha; en revisión del grupo)

- Ocho ejes y la vacancia en tres partes, con el perímetro del FMI verificado en su informe de 2025.

### Etapa 3. Datos (hecha)

- Series construidas desde fuentes primarias (MECON, BCRA, INDEC, FRED) y controladas contra el FMI (Capítulo 5).

### Etapa 4. Metodología (hecha)

- SVARX, identificación, muestra de estimación común, rezagos con regla AIC más estabilidad, canales de la FED, variantes y criterios de contraste (Capítulo 4).

### Etapa 5. Estimación (hecha)

- Reacción fiscal 0,051 [0,020; 0,082]; respuestas a la FED no significativas por separado; diagnósticos informados (Capítulo 6).

### Etapa 6. Simulación (hecha)

- Escenario base y dos escenarios de la FED, robustez por perímetro, canal de tasas en pesos y shocks a la manera del FMI.

### Etapa 7. Resultados, discusión y conclusiones (borrador listo para revisión del grupo)

- Resultados corregidos tras la revisión adversarial del 11/10 (inflación relativa del FMI en la identidad, retroalimentación sobre el desvío acumulado, corrección de sesgo de Kilian, deuda regenerada en el bootstrap, horizonte 2031, senda real de la FED 2022-2025). H1b respaldada y robusta: 25,2% en 2031 [19,0; 27,7] contra 1%, y 22,3% en 2035 contra menos de 3%, en las 18 especificaciones. H1a respaldada por suficiencia: hace falta un superávit de 7,0% del PIB, el doble del máximo histórico (3,6%); la descomposición de la varianza no es robusta. H2 respaldada de manera débil: +13 puntos de probabilidad en 2035 [1; 25], que no se sostienen con Bonferroni.

### Etapa 8. Entrega (pendiente)

- Revisión del grupo y del director, y pasaje al formato final.

## 5. Qué falta: tareas, verificaciones y decisiones (actualizado el 11/10/2026)

### 5.1 Datos que hay que bajar o confirmar

| Qué | Por qué importa | Cómo se resuelve | Estado |
|---|---|---|---|
| Títulos públicos en cartera del FGS (ANSES), 2008-2025 | La deuda neta no descuenta la deuda del Tesoro en manos del FGS. Por eso queda unos 8 a 10 puntos del PIB por encima de la consolidada del FMI (119,0 contra 110,8 en 2023; 61,1 contra 51,5 en 2024). Según una nota de prensa no verificada, la cartera de títulos del FGS rondaba los USD 44.000 millones en octubre de 2024 (cerca de 7,7% del PIB): del orden de la brecha. | ANSES bloquea la descarga automática (protección anti-bots); hay que bajar los PDF a mano desde el navegador y guardarlos en `datos/crudos/fgs/`. Archivos: Informe Estadístico Mensual de enero de 2026 (https://www.anses.gob.ar/sites/default/files/archivo/2026-03/IEM-FGS-2026-01.pdf), Anuario 2024 (https://www.anses.gob.ar/sites/default/files/inline-files/Anuario%202024.pdf), Consejo del FGS de diciembre de 2025 (https://www.anses.gob.ar/sites/default/files/archivo/2026-02/Consejo%20FGS-Diciembre-2025.pdf) y, para años anteriores, los anuarios e informes de la página del FGS (https://www.anses.gob.ar/fgs-fondo-de-garantia-de-sustentabilidad). De cada uno se toma la fila "Títulos Públicos Nacionales" al cierre de cada año o trimestre. El script `codigo/ingesta_datos/construir_tenencias_fgs.py` ya está listo para leerlos. | Pendiente: bajar a mano |
| Deuda en manos de Agencias del Sector Público (Secretaría de Finanzas) | Sirve como dato descriptivo de la deuda intra-sector público. No se usa para restar, porque incluye otras entidades y duplicaría parte de lo que ya se consolida. | Ya está en `datos/procesados/tenencias_fgs_1996_2025.csv` (trimestral 2021-2025; anual en % del PIB 2004-2025), con los PDF de Finanzas en `datos/crudos/fgs/`. | Hecho |
| LEFI entre julio de 2024 y julio de 2025 | Si no estaban en la deuda del Tesoro, faltaban en la consolidada. | Verificado en el Informe de Deuda del MECON al 31/12/2024 (hoja A.1.7): la LeFi/$/TNAPM/17-07-2025 figura en el stock de títulos y letras del Tesoro en moneda nacional, por 23,0 billones de pesos. Está en la deuda bruta, y la parte en poder del BCRA se resta como tenencia del BCRA. No falta nada. | Resuelto |

### 5.2 Verificaciones de citas

| Qué | Estado |
|---|---|
| Braun y Joy (1968), restricción externa | No hay copia abierta (Oxford y JSTOR). Si alguien tiene acceso por la facultad, se verifica contra el original; si no, se cita a través de la fuente secundaria (Katz y Kosacoff, CEPAL) indicándolo. |
| Adler, Djigbenou y Sosa (2016) | Se verificó sobre el documento de trabajo del FMI (WP/14/60), no sobre la versión de la revista. Conviene leer la versión publicada si el tribunal lo exige. |
| Las otras siete citas del marco teórico | Verificadas contra el texto completo, con página (ver `verificacion_citas_marco.md`). |

### 5.3 Decisiones abiertas para el grupo

1. **Criterio de H1a (decidido el 11/10, para revisar con el grupo).** La descomposición de la varianza no mide si el superávit alcanza, y con las correcciones no es significativa ni robusta. El criterio principal pasa a ser el contraste de suficiencia: el superávit que haría falta para llevar la probabilidad de no estabilización al 1% del FMI, comparado con el máximo histórico del Sector Público Nacional. La varianza se sigue informando. Conviene que Santiago y Pablo lo validen, porque es un cambio de criterio.
2. **Deuda neta con o sin FGS.** Cuando esté la serie del FGS, hay que definir si la deuda neta sin el FGS pasa a ser la especificación principal, porque es la más parecida a la del FMI, o si queda como robustez. En los dos casos hay que reestimar y volver a simular.

3. **Propuestas del grupo ya incorporadas el 11/10.** Por un lado, la retroalimentación entre la deuda y las variables (arquitectura B de Santiago): un punto más de deuda sube el EMBI+ 22 puntos básicos [11; 41], y está en la sección 6.1. Por otro, el contraste sin retroalimentación (arquitectura A), en la sección 6.6. Se repuso además en las líneas futuras el panel Argentina-Chile (decisión del 17/9), y se sumaron los shocks de la FED de alta frecuencia y los términos de intercambio que proponía Santiago.

4. **Escenario base del FMI actualizado (11/10/2026).** El FMI publicó dos análisis de sostenibilidad posteriores al de abril de 2025: la primera revisión (Informe 25/219, agosto de 2025) y el Artículo IV con la segunda revisión (Informe 26/105, mayo de 2026). Se pasó al de mayo de 2026, extraído del PDF con `codigo/ingesta_datos/extraer_escenario_base_fmi_cr26105.py`. La tesis, los gráficos y la guía de defensa ya usan esas cifras.

### 5.4 Otras tareas

- Revisión del texto completo por el grupo y por Pablo.
- Confirmado: no se pide resumen en inglés y la extensión tiene que ser corta. Candidato a recortar: el capítulo de Datos, llevando el detalle de construcción al apéndice.
- Hecho: se borraron de `tesis/figuras/` las figuras de los modelos viejos que ya no usaba ningún capítulo (quedan en el historial de git).

## Referencias de este documento

- Fondo Monetario Internacional. (2021). *Review of the debt sustainability framework for
  market access countries* (IMF Policy Paper).
- Fondo Monetario Internacional y Mecanismo Europeo de Estabilidad. (2023). *The stochastic
  debt fanchart in the IMF's Sovereign Risk and Debt Sustainability Framework for MACs*
  (presentación, 30 de noviembre de 2023).
- Fondo Monetario Internacional. (2025). *Argentina: Request for an extended arrangement under
  the Extended Fund Facility* (IMF Country Report No. 25/95).
- Oficina de Presupuesto del Congreso. (2026). *Operaciones de deuda pública, julio 2026*.
