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

## Fase 4, resto del documento
Pendiente de confirmar qué otras secciones existen o faltan: marco teórico, metodología completa
(ya con el alcance de la Fase 2 definido), datos, cronograma formal si la carrera lo exige aparte.
No se subieron archivos de esas secciones todavía, avisar cuando estén para sumarlas al plan.

## Fase 5, reenvío a Pablo
Reenviar Introducción y Antecedentes corregidos, dejando explícito en la entrega qué comentario se
resolvió con qué cambio (la tabla de trazabilidad de `introduccion_antecedentes_v2_corregido.md`
sirve para esto tal cual), y qué queda abierto: las dos citas a verificar y el párrafo de cierre
metodológico, ya redactable con la Fase 2 resuelta.
