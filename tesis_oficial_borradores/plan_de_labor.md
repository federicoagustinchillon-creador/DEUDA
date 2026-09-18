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

## Fase 6, justificación del SVAR, foco de shock e historiografía: HECHO (2026-09-17)
A pedido del usuario, se resolvieron seis puntos sueltos:

- **DOLS y endogeneidad**: confirmado que el texto ya distingue correctamente los dos sentidos de
  "endogeneidad" (la de corto plazo que DOLS purga con adelantos/rezagos, vs. la simultaneidad
  resultado fiscal-riesgo país que solo corrige IV-2SLS). No se encontró ninguna oración que atribuya
  a DOLS la corrección de la segunda. **Corrección tras la reunión del usuario con Pablo (2026-09-17)**:
  el encuadre correcto no es "se asume endógeno sin testear"; es que, en un sistema de series de
  tiempo, todo es endógeno salvo los shocks de alta frecuencia, y por eso no corresponde presentar un
  test como el que decide si el EMBI+ es endógeno. Reescrito en `04_metodologia.tex` (nueva Sección
  \ref{sec:etapa4_endogeneidad}, Etapa 4): el EMBI+ es endógeno por compartir la frecuencia trimestral
  del sistema (igual que $pb_t$, $d_t$, TCRM$_t$), y el VIX/BOVESPA\_VOL son instrumentos válidos
  precisamente por ser series de mayor frecuencia (diaria) que el sistema no puede causar hacia atrás
  en el tiempo. El párrafo de Wu-Hausman en `06_resultados.tex` se reescribió para no presentarlo como
  el test que decide si instrumentar hacía falta, sino como diagnóstico secundario de eficiencia.
- **Por qué esa matriz de SVAR y no otra, y por qué TCRM**: agregado en `04_metodologia.tex`
  (Sección \ref{sec:svar_metodologia}) con citas reales ya existentes en el repo, sin necesidad de
  buscar nada nuevo: Uribe y Yue (2006, causalidad spread-fundamentals), Neumeyer y Perri (2005,
  tasa externa contracíclica) y Eichengreen, Hausmann y Panizza (2003, *original sin*/descalce de
  moneda) justifican por qué EMBI+ y TCRM se tratan como bloque financiero de ajuste contemporáneo, y
  por qué TCRM no puede omitirse del sistema. Se explicitó también por qué no se usa un Cholesky
  simple (no hay razón teórica para ordenar EMBI+ y TCRM entre sí, así que esa transmisión queda sin
  restringir en vez de forzarse).
- **Foco de shock elegido**: entrada/salida de capitales (no shock monetario), porque ya hay
  respaldo bibliográfico directo (Uribe-Yue, Neumeyer-Perri) y porque no hay serie propia de tasa de
  política monetaria ni agregados monetarios con cobertura de 30 años en la base de datos actual.
  Documentado en el mismo párrafo de `04_metodologia.tex`.
- **Panel VAR/VECM con Chile ("siguiendo a Sturzenegger")**: buscado primero con un agente de
  investigación web, que no encontró un VAR/VECM de panel Argentina-Chile de Sturzenegger.
  **Corrección**: el usuario señaló que el paper real es el de 2021, que su compañero de tesis ya usa
  en antecedentes/introducción. Es el mismo que ya teníamos citado como `levyyeyati2021` (Levy Yeyati
  y Sturzenegger, WP 2021 / publicado 2023): la búsqueda anterior falló por buscar literalmente "panel
  VAR Chile" cuando el paper no es un panel conjunto, sino un VAR de 3 variables (PBI, TCR, tasa
  internacional) aplicado país por país, que efectivamente incluye a Chile (agregando el precio del
  cobre) además de Argentina — ya documentado en `antecedentes_notas_tecnicas.md` (línea 785 y 802),
  no hacía falta buscar nada nuevo. Los antecedentes de 2006 (Sturzenegger-Zettelmeyer, *Debt
  Defaults*; Cowan-Levy Yeyati-Panizza-Sturzenegger, *Sovereign Debt in the Americas*) siguen siendo
  reales pero no son la referencia que el usuario tenía en mente. Decisión del usuario: implementar un
  VAR/VECM de panel propio Argentina-Chile de verdad, pero no ahora, queda como línea de investigación
  futura (no como tarea de esta entrega). Agregado como primer paso concreto (antes de escalar al panel
  de 6-8 países ya mencionado) en la Sección "Agenda de Investigación Futura" de `08_conclusiones.tex`
  (línea Quinta), citando a Cowan et al. (2006) como fuente de datos ya armonizados y dejando
  explícito que un panel conjunto Argentina-Chile sería una contribución metodológica genuina, no la
  réplica de un protocolo existente (el propio Levy Yeyati-Sturzenegger aplica el VAR país por país,
  no como panel conjunto).
- **Historiografía en Introducción/Antecedentes**: la afirmación histórica general sobre crisis de
  deuda recurrentes en Argentina/Latinoamérica en `01_introduccion.tex` citaba solo papers técnicos
  de sostenibilidad fiscal (Mendoza-Oviedo, De Rasmo), no historiografía económica. Se agregaron,
  verificados uno por uno contra catálogos de editorial/JSTOR/Library of Congress (no de memoria):
  Díaz Alejandro (1970), della Paolera y Taylor (2001), Rapoport (2020) para la historia argentina
  específica, y Reinhart y Rogoff (2009) para el patrón más amplio de crisis de deuda soberana en
  perspectiva de siglos. Las seis entradas nuevas de bibliografía (`diazalejandro1970`,
  `dellapaolera2001`, `rapoport2020`, `reinhartrogoff2009`, `cowan2006`, `sturzenegger2006`) están en
  `tesis/fuente/referencias.bib`.
- **Otro paper de SVAR estructural para Argentina o países muy similares**: no se buscó específicamente
  porque el punto 2 (justificación de la matriz) ya quedó resuelto con literatura de shocks externos
  (Uribe-Yue, Neumeyer-Perri) en lugar de un precedente de SVAR aplicado línea por línea a Argentina;
  pendiente si el director pide un antecedente metodológico más directo de SVAR fiscal-cambiario para
  economías emergentes específicamente (no solo Blanchard-Perotti, que es para economías avanzadas).

`Tesis.pdf` recompilado y verificado (98 páginas antes de esta fase, sin warnings de referencias
nuevos) y commiteado.

## Fase 6b, reunión real con Pablo y primer recorte de tamaño: HECHO (2026-09-17)
Tras una reunión efectiva del usuario con el director (no una suposición nuestra), dos correcciones:

- **Endogeneidad**: Pablo no pidió una discusión de si el EMBI+ "se asume" o "se testea" endógeno.
  Dijo, en general para series de tiempo, que todo es endógeno salvo los shocks de alta frecuencia
  (razón por la que VIX/BOVESPA\_VOL sirven como instrumentos). El usuario fue explícito: **no
  nombrar** esta discusión en el cuerpo de la tesis a menos que el jurado o el director lo pregunten
  en la defensa. Se revirtió el párrafo agregado en la Fase 6 en `04_metodologia.tex` y
  `06_resultados.tex`, quedando el texto como estaba antes de esa fase. La explicación de frecuencias
  queda como conocimiento de respaldo para la defensa oral, no escrita.
- **Reducción de tamaño**: confirmado el objetivo de bajar de 100 páginas. Primer recorte ejecutado:
  el capítulo 8 (limitaciones (i)-(vi) y agenda futura) pasó de prosa corrida a listas, mismos números
  y citas, menos palabras. En el capítulo 5 se encontró una duplicación real (dos tablas descriptivas
  separadas para la misma submuestra 2004--2025, $n=88$) y se fusionaron en una sola tabla de 7
  variables, calculando de datos reales (no fabricado) la mediana, asimetría y Jarque-Bera de
  TCRM/CER/VIX que faltaban en ambas tablas originales. `Tesis.pdf`: 99 páginas (de 100). El resto del
  capítulo 5 no se tocó porque alimenta directamente Johansen/VECM/DOLS/instrumentación del Capítulo
  6, no es material periférico recortable sin tocar el núcleo. Pendiente si el usuario quiere seguir
  recortando otros capítulos (antecedentes, cap. 2, fue explícitamente descartado como candidato).

## Fase 6c, "ventana única" purgada del texto: HECHO (2026-09-18)
A pedido del usuario ("No nombres en ningún lado una ventana única, es implícito"), se sacaron las
51 menciones a "ventana única"/"ventana muestral única" repartidas en 6 capítulos (04 a 09). No se
tocó ningún número, cita o referencia cruzada, solo la auto-referencia a la propia elección
metodológica de usar un solo período. `Tesis.pdf`: 98 páginas (de 99).

## Fase 7, eliminación de H1b (endogeneidad/IV-2SLS): HECHO (2026-09-18)
El usuario, tras otra reunión con Pablo, señaló que la premisa de H1b ("el riesgo soberano no es
exógeno") ya no es algo que haga falta demostrar por separado: en series de tiempo todo es endógeno
salvo los shocks de mayor frecuencia que el sistema, y el VECM/SVAR ya tratan al EMBI+ como
conjuntamente endógeno por diseño. Pidió cortar H1b y su técnica (IV-2SLS) entera, sin dejarla
mencionada ni siquiera de nombre, y usar el espacio ganado para reforzar la justificación de la
matriz y los shocks del SVAR, que es "donde gira todo". No se tocó nada del SVAR ni del Monte Carlo
sobre sus residuos, como pidió explícitamente.

Cambios en los 11 archivos: 01 (dos hipótesis derivadas en vez de tres, H1c pasa a llamarse H1b,
sale el objetivo específico de IV-2SLS, el segundo pilar de la Justificación pasa a ser la
identificación estructural del SVAR); 02 (el área de vacancia se renombra de "Endogeneización
Pendiente" a "Identificación Estructural Pendiente de los Canales de Transmisión", sin nombrar
IV-2SLS ni "tratarlo de endógeno" en ningún lado, por pedido explícito del usuario en un mensaje
posterior); 04 (Etapa 4 completa eliminada, Hansen/TVECM pasa a ser Etapa 4, DSA a Etapa 5, sale la
fila de VIX/ETF EMB de la matriz operacional); 05 y 06 (sección/tabla IV-2SLS eliminada, ajustes de
conteo de técnicas); 07 y 08 (párrafos y fila de tabla de H1b eliminados, renumeración H1c→H1b); 09
(fila del apéndice de scripts eliminada); 00_abstract y 00_acronimos (IV-2SLS sacado).

Dos hallazgos no buscados, corregidos al pasar por esos párrafos: en `06_resultados.tex`, el párrafo
de magnitud económica de los coeficientes todavía tenía $\rho=-0.0071$ (valor pre-ventana única;
el valor correcto y ya usado en el resto del capítulo es $\rho=0.0159$), corregido. Y en
`09_apendice.tex`, la Tabla \ref{tab:limitaciones} ("Tabla Consolidada de Limitaciones
Metodológicas") sigue con números de la ventana vieja de 88 observaciones (Durbin-Watson $=0.321$,
ARCH-LM $p=0.0009$) que nunca se actualizaron cuando el resto de la tesis pasó a la ventana de 120
observaciones (donde esos valores son $0.117$ y $p<10^{-12}$ respectivamente, Capítulo 8). Solo se
corrigió la mención a IV-2SLS en esa tabla; el resto de sus números **sigue desactualizado** y queda
pendiente de una pasada aparte si el usuario la pide.

`Tesis.pdf`: 92 páginas (de 98). Recompilado y verificado sin referencias ni citas rotas.

## Fase 8, corrección "Ventana Única" en mayúscula, reestimación real y eliminación de DOLS: HECHO (2026-09-18)

**8a, títulos en mayúscula sin purgar**: al mapear la estructura completa de la tesis a
pedido del usuario, se encontraron 6 títulos de sección/captions con "Ventana Única" en
mayúscula que la purga de la Fase 6c (case-sensitive, buscaba minúscula) no detectó
(`05_datos.tex`, `06_resultados.tex`). Corregidos a "Muestra Completa".

**8b, el bloqueo de memoria era transitorio**: el usuario insistió en que sí se podía
reestimar CUSUM/subperíodos/Engle-Granger pese al error de OpenBLAS del día anterior. Se
reintentó y funcionó. Reestimados de verdad con el código real del repo
(`fase7_diagnosticos_robustez.py`, repuntado a `dataset_consolidado_1996_2025.csv`):
CUSUM ahora **sí** rechaza estabilidad paramétrica (antes no la rechazaba, hallazgo real y
distinto), sensibilidad por subperíodo (1996-2010 con reacción fuerte y significativa,
2011-2025 nula) y Engle-Granger (prácticamente igual a la ventana vieja). Los tres
convergen entre sí y con Bai-Perron. Corto período de vida: se cortaron enteros en 8c.

**8c, eliminación de DOLS**: el usuario preguntó si tenía sentido sacar DOLS ("Bohn se
aplica sobre VECM, no DOLS"), dado que VECM ya era "la técnica de referencia" y DOLS estaba
etiquetado como "ejercicio de robustez". Confirmado que VECM solo alcanza para H1 sin dejar
ningún hueco (no aristas faltantes). Se cortó DOLS de los 11 archivos que lo mencionaban, y
con él todo lo que testeaba específicamente la estabilidad de SU coeficiente (no una
robustez general de H1): el CUSUM/CUSUMSQ y la reestimación por subperíodo recién hechas en
8b (quedan en el historial de git, no en la tesis). El VECM ya tenía su propia robustez
aparte (sensibilidad de rezagos, interacción presidencial sobre el ECT), así que no queda
ningún hueco tampoco ahí. La lista de limitaciones de los capítulos 8 y 9 pasó de seis a
tres ítems (se caían las tres que eran diagnósticos de residuos de DOLS específicamente).
En el apéndice, las filas de scripts de DOLS (fase3, fase11) quedaron marcadas "no
incorporado a la versión final" en vez de eliminadas, siguiendo el mismo criterio ya usado
ahí para DCC-GARCH.

**8d, spread histórico 1983-2025 fuera de la tesis**: el usuario pidió sacar esta extensión
también ("por ahora no la necesitamos, no la elimines pero sacala"). Movida a
`tesis_oficial_borradores/extension_spread_historico_1983_2025.md`, mismo patrón que la
especificación alternativa DSA CIR/DCC-GARCH. Se encontró una dependencia real: la
metodología de empalme del EMBI+ para la ventana central 1996-2025 (`04_metodologia.tex`,
`sec:empalme`) citaba esta extensión como su propia fuente ("no hace falta un empalme
nuevo, el de esa sección ya cubre 1996-2025"). Se reescribió ese párrafo para que describa
la corrección de empalme ($k=0.8710$) de forma autocontenida, sin depender del archivo que
se sacó. También salió el objetivo específico correspondiente en el capítulo 1 y la fila de
la tabla de consistencia en el capítulo 8.

`Tesis.pdf`: 90 páginas (post 8a) → 85 páginas (post 8c) → **81 páginas** (post 8d).
Recompilado y verificado en cada paso, sin referencias ni citas rotas.
