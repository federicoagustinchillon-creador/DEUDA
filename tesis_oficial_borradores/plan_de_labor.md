# Plan de labor, tesis oficial (director Pablo)

Este archivo es un documento de trabajo interno, para ir tachando fases entre nosotros. No es parte
de la tesis y no se entrega ni se pega en ningún capítulo. Si la carrera exige un "Plan de Trabajo"
formal dentro del proyecto de tesis que se presenta para aprobación, eso es un documento distinto,
con su propio formato institucional, que se escribe aparte cuando haga falta.

Esta tesis es distinta del desarrollo cuantitativo que ya existe en `tesis/`, `codigo/` y
`resultados/` (SVAR, VECM, CIR, TVECM, DSA sobre 2004-2025 y la extensión 1983-2025). La Fase 2
resuelve cómo se relacionan ambos.

## Fase 0, hecho (2026-09-15)
- [x] `Introducción.docx` y `antecedentes.docx` pasados a Markdown.
- [x] Extraídos los más de 30 comentarios de Pablo del PDF anotado (no estaban visibles como texto
      plano, solo como anotaciones PDF; había que leer `/Annots` de cada página).
- [x] Confirmado que `Introducción.docx` era idéntico a la versión que Pablo comentó, sin ninguna
      corrección aplicada.

## Fase 1, hecho (2026-09-15)
- [x] Corregidos los 6 comentarios de la página 1 (sin guiones largos como inciso, sin "narrativa
      oficial", sin el conector "Frente a este dilema", cortada la oración final que pidió sacar,
      dos huecos de cita marcados en vez de resueltos con una cita inventada).
- [x] Purgados los 10 pares de guion largo del resto del documento (páginas 2 y 3, sección
      Antecedentes).
- [x] Puestos en cursiva con nota al pie los términos en inglés (*sudden stop*, *fan charts*,
      *push*, *early warning systems*) en su primera aparición.
- [x] Sacada la aclaración "(2020, por ejemplo)" que pidió sacar Pablo.
- [x] Validado sin cambios el fragmento que Pablo marcó como "buen detalle para tener en cuenta".

Texto final: `introduccion_antecedentes_v2_corregido.md`, con una tabla de trazabilidad al final que
mapea cada comentario de Pablo con el cambio hecho. Falta: pasarlo a `Introducción.docx` (Word,
Calibri, sin nada que huela a IA en el formato) y decidir las dos citas marcadas `[CITA: ...]`
antes de darlo por cerrado; no se puso ninguna cita sin verificar primero que el paper sostenga lo
que se le está haciendo decir.

## Fase 2, alcance metodológico: RESUELTO (2026-09-15)
Confirmado por el usuario: es una tesis de grado, no de doctorado. Nivel de grado sí, nivel de
doctorado no.

- El desarrollo cuantitativo que ya existe en `tesis/`, `codigo/` y `resultados/` (SVAR restringido,
  VECM, TVECM de Hansen-Seo, calibración CIR por máxima verosimilitud exacta, DCC-GARCH, Bai-Perron,
  DSA estocástico con varias especificaciones de robustez), apilado completo, es más propio de una
  tesis de maestría o doctorado que de una de grado. No se inserta tal cual.
- La metodología del cuerpo de esta tesis se arma alrededor de una estrategia empírica central, bien
  ejecutada, del mismo tipo que ya usan los antecedentes centrales de la sección de Antecedentes: FRF
  a la Bohn (superávit primario en función de la deuda rezagada y la brecha del producto, como
  Medeiros 2012 y Everaert-Jansen 2018) estimada por DOLS o por un VECM simple de dos o tres
  variables, más un DSA determinista y una simulación Monte Carlo simple, sin necesidad de GARCH ni
  cópulas. Es el mismo nivel de instrumental que ya revisa la sección de Antecedentes, así que no
  hace falta justificar un salto de complejidad frente al propio texto.
- El SVAR, el TVECM, el CIR y el DCC-GARCH quedan disponibles como código y resultados ya corridos
  (`resultados/tablas/`) por si hace falta un anexo de robustez puntual más adelante, pero no como
  columna vertebral del capítulo de resultados.

Con esto resuelto, falta redactar el párrafo de cierre de Antecedentes que pide Pablo: por qué esta
metodología y por qué estas variables. Con la FRF a la Bohn como eje, las tres razones que da Pablo
como ejemplo encajan directamente: no se ha probado con la especificación de descalce cambiario que
plantea esta tesis (razón 1), el contexto post-2024 cambió respecto de los antecedentes revisados
(razón 2), y falta en los antecedentes una variable de riesgo soberano tratada como endógena en el
caso argentino específicamente (razón 3, en diálogo con Levy Yeyati y Sturzenegger y con Rodríguez
2023, ambos ya en Antecedentes).

## Fase 3, fuente de datos para vencimientos en moneda extranjera
Usar el informe mensual de la Oficina de Presupuesto del Congreso (OPC), *Operaciones de Deuda
Pública*, como fuente puntual para la cifra que se cita en la Introducción. No existe una fuente
única y homogénea para una serie histórica larga de vencimientos por moneda, y no vale la pena
reconstruirla: alcanza con el stock "% deuda en moneda extranjera", que ya está en la matriz de
datos de la tesis individual, como proxy de descalce cambiario a través del tiempo.

## Fase 2b, corrección de la Fase 2: RESUELTO (2026-09-15)
La Fase 2 original estaba mal apoyada: asumía que `tesis/`, `codigo/` y `resultados/` eran un
desarrollo aparte, no la tesis oficial. Al revisar `tesis/capitulos/04_metodologia.tex` apareció
que ya está escrito y compilado en `tesis/fuente/Tesis.pdf` (92 páginas antes de esta fase): VECM,
SVAR restringido con la identidad de acumulación de deuda del FMI como restricción estructural
($d_t = \frac{1+r_t}{1+g_t}d_{t-1} - pb_t + sft_t$), TVECM de Hansen-Seo, DOLS, IV-2SLS, umbral de
Hansen, Bai-Perron y CIR+DCC-GARCH para el DSA estocástico. Es la tesis oficial, no un desarrollo
paralelo.

Confirmado por el usuario: SVAR restringido y TVECM se quedan. El resto se recorta solo si no deja
una arista faltante. Cada pieza del protocolo está atada a una de las tres hipótesis derivadas de
`01_introduccion.tex` o a un objetivo específico:
- $H_{1a}$ (fatiga fiscal) se contrasta con el umbral de Hansen: no se puede cortar.
- $H_{1b}$ (endogeneidad del EMBI+) se contrasta con IV-2SLS sobre la especificación DOLS: no se
  puede cortar ninguna de las dos sin dejar $H_{1b}$ sin contrastar.
- $H_{1c}$ (quiebres estructurales) se contrasta con Zivot-Andrews y Bai-Perron: no se puede cortar.
- El VECM y el SVAR restringido (con la fórmula del FMI) son la técnica de referencia de la FRF: se
  quedan, ya confirmado.

Lo único sin una hipótesis o un objetivo que dependa de ello es la Etapa 6 (CIR + DCC-GARCH del DSA
estocástico): no alimenta a $H_{1a}$, $H_{1b}$ ni $H_{1c}$, solo la simulación de Monte Carlo de la
proyección 2026--2035. Pendiente de decidir con el usuario si se simplifica reemplazando el proceso
de difusión CIR y el DCC-GARCH por un muestreo directo de la covarianza de residuos del VECM/SVAR ya
estimado (misma simulación de Monte Carlo, sin el submodelo aparte), o si se deja como está.

## Fase 2c, Introducción y Antecedentes: fusionadas con el .tex oficial (2026-09-15)
Aparecieron dos versiones de Introducción/Antecedentes con literatura distinta: la de
`Introducción.docx`/`antecedentes.docx` (Medeiros 2012, Everaert-Jansen 2018, Adler-Sosa 2014,
Wijayanti-Rachmanira 2020, Cetrángolo et al. 1997, Calvo et al. 2003, Levy Yeyati-Sturzenegger 2021,
Hébert-Schreger 2017) y la de `tesis/capitulos/01_introduccion.tex`/`02_estado_del_arte.tex`
(Rodríguez 2023, Sanches 2019, Aruguete 2021, Roldán 2021, Bohoslavsky 2024, Cantamutto 2024,
Blanchard 1990/2019, Everaert 2017, González 2023), más la estructura formal de tesis (Trinidad
Lógica, Objetivos, Hipótesis Derivadas, Justificación con la Ley 27.612) que el docx no tiene.

Resuelto por el usuario: el docx corregido es la base, pero lo superior del .tex se queda. Se
fusionaron en `01_introduccion.tex` y `02_estado_del_arte.tex`: se mantuvo toda la estructura formal
del .tex, se agregó la cita a Medeiros (2012) en la Justificación como precedente metodológico
directo del SVAR (resuelve el hueco `[CITA: Medeiros 2012]` del docx), y se sumaron cuatro ejes
nuevos a Antecedentes (Quinto a Octavo) con la literatura del docx, sin duplicar a Rodríguez (2023)
que ya estaba citado en el .tex. Se purgaron además los guiones largos como inciso que también
tenía el propio `.tex` (mismo patrón que señaló Pablo en el docx), en estos dos capítulos
únicamente. El hueco `[DATO: OPC]` sobre vencimientos en moneda extranjera no se resolvió, sigue
pendiente de la cifra real. `Tesis.pdf` recompilado y verificado visualmente (96 páginas, notas al
pie, cursivas y citas correctas, sin guiones largos).

Los guiones largos como inciso siguen presentes en `03_marco_teorico.tex`, `05_datos.tex`,
`06_resultados.tex` y `07_discusion.tex`: no se tocaron todavía porque el orden acordado es
Introducción → Antecedentes → Metodología → resto, y esos capítulos no entraron en esta fase.

## Fase 3b, extensión de la ventana a 30 años: HECHO (2026-09-16)
A pedido del usuario ("me pedirán mínimo 30 años y óptimo desde la vuelta a la democracia"), se
investigó qué tan atrás se puede llevar el sistema de 4 variables (deuda, resultado primario, EMBI+,
TCRM). Deuda/pb/PIB ya llegaban a 1996 (empalme existente). El EMBI+ ya llegaba a 1983 (Fase 22, spread
Bonex/Brady/EMBI+ Global, idéntico punto a punto al EMBI+ real desde 1999). El único techo real es el
TCRM: el BCRA solo lo publica desde enero de 1997 (verificado contra el archivo crudo). Se construyó
`datos/dataset_consolidado_1996_2025.csv` (n=120, 30 años exactos), con el TCRM de 1996 (4 de 120
trimestres) aproximado por extrapolación de tendencia OLS sobre 1997-1999. Se reestimó todo el
protocolo (`codigo/modelos/fase23_reestimacion_1996_2025.py`): estacionariedad, Johansen, VECM, SVAR
restringido, TVECM. Verificado como robusto excluyendo los 4 trimestres aproximados (ventana real
1997-2025, `fase23b_*`): mismo resultado, no es un artefacto de la aproximación.

Hallazgo importante, verificado y escrito con toda la transparencia en el texto: la descomposición de
varianza del SVAR **se invierte** respecto de lo que decía la tesis. Antes (ventana 2004-2025):
fiscal+actividad explicaban 76% de la varianza de la deuda a 20 trimestres, cambiario+riesgo solo
11.5%. Ahora (ventana 1996-2025): inercia propia de la deuda explica 54.2%, cambiario+riesgo (25.8%)
supera a fiscal+actividad (20.0%). Coherente con que Johansen ya no rechaza la ausencia de
cointegración para ningún inicio de muestra entre 1996 y 1999 (antes solo dependía de si se incluía
1999). También apareció que deuda/PIB, con ADF y KPSS, ahora lee más cerca de I(0) que de I(1) en esta
ventana (antes I(1) sin ambigüedad); se mantiene el tratamiento I(1) por continuidad con el resto del
protocolo, dejando la tensión declarada en el texto en vez de ocultarla. El VECM/TVECM, en cambio, se
CONFIRMA y se fortalece: sin reacción fiscal (antes p=0.204, ahora p=0.996), EMBI+ absorbe el ajuste
(ahora significativo, antes no), umbral de ~2080-2104 pb replicado en tres especificaciones
independientes (Hansen en niveles, Hansen en Δpb, TVECM).

Se simplificó también la Etapa 6 (DSA estocástico): la covarianza de los shocks ahora se deriva
directamente de la matriz de impacto estructural del SVAR (de esta misma ventana de 30 años) en vez
de un proceso CIR + DCC-GARCH aparte. Nueva probabilidad de insolvencia a 2035: 26.1% (antes 31.2%
con la matriz calibrada a mano, 29.8% con CIR, 32.5% con DCC-GARCH). El CIR y el DCC-GARCH NO se
borraron: quedan documentados en `06_resultados.tex` como especificación alternativa, con sus propios
resultados intactos, para que el director decida cuál integrar a la versión final.

Todos los números reales (con las tablas completas) quedan en
`tesis_oficial_borradores/numeros_ventana_1996_2025.md`. Actualizados con estos números:
`00_abstract.tex`, `04_metodologia.tex`, `05_datos.tex`, `06_resultados.tex`, `07_discusion.tex`,
`08_conclusiones.tex`, `09_apendice.tex`. `fase19_svar_matriz_impacto_S.csv` y `fase19_fevd.csv`
(los archivos canónicos que usa el DSA) quedaron sobreescritos con los resultados de la ventana nueva;
los de la ventana vieja (2004-2025) quedan solo en `fase23_*` como trazabilidad si hace falta comparar.

## Fase 4, resto del documento
Marco teórico, datos y resultados ya existen en `tesis/` (no hay que escribirlos de cero), pero
siguen con guiones largos como inciso sin purgar (ver Fase 2c) y sin revisar contra el resto de los
comentarios de Pablo. Falta también el cronograma formal si la carrera lo exige aparte del plan de
labor interno.

## Fase 5, reenvío a Pablo
Reenviar Introducción y Antecedentes corregidos, dejando explícito en la entrega qué comentario se
resolvió con qué cambio (la tabla de trazabilidad de `introduccion_antecedentes_v2_corregido.md`
sirve para esto tal cual), y qué queda abierto: las dos citas a verificar y el párrafo de cierre
metodológico, ya redactable con la Fase 2 resuelta.
