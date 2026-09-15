# Plan de labor — Proyecto de Investigación (cátedra, tutor Pablo)

Distinto del repo de tesis individual (`tesis/`, `codigo/`, `resultados/`). Esto es el Proyecto de
Investigación conjunto con Santiago Páez y Emiliano Carricondo, tutorado por Pablo. Se arregla
por fases, cada una cerrable en una sesión.

## Fase 0 — Hecho (2026-09-15)
- [x] Introducción.docx y antecedentes.docx pasados a Markdown.
- [x] Extraídos los 30+ comentarios de Pablo del PDF anotado (no estaban visibles como texto plano,
      solo como anotaciones PDF — había que leer `/Annots` de cada página).
- [x] Confirmado: `Introducción.docx` es idéntico a la versión que Pablo comentó. Ninguna corrección
      aplicada todavía.
- [x] Redactada una v2 de la Introducción que resuelve los 6 comentarios de la página 1 (ver
      `introduccion_v2_propuesta.md`).

## Fase 1 — Introducción y Antecedentes (en curso)
1. Revisar `introduccion_v2_propuesta.md` — decidir las dos citas marcadas `[CITA: ...]`.
2. Aplicar a Antecedentes los cambios mecánicos listados en la Fase 1 del mismo archivo (sacar
   guiones largos, cursiva + nota al pie en términos en inglés, sacar la aclaración que pidió sacar
   Pablo).
3. Validar el detalle marcado como "buen detalle para tener en cuenta" — no tocar, ya está bien.
4. **No** escribir todavía el párrafo de cierre de Antecedentes (depende de la Fase 2).

## Fase 2 — Decisión metodológica del proyecto de cátedra
Pablo ya advirtió (en la entrevista con el grupo) que el proyecto de cátedra **no debe profundizar a
nivel tesis de grado** — pidió un análisis simple pero prolijo, no el desarrollo cuantitativo pesado
que sí tiene la tesis individual (SVAR, VECM, CIR, TVECM). Decisión pendiente, a tomar en conjunto
con Páez y Carricondo:

- **Opción A (recomendada por alcance)**: FRF simple a la Bohn (superávit primario ~ deuda rezagada +
  brecha del producto), el mismo tipo de ejercicio que hace Medeiros (2012) — que ya es la columna
  vertebral de la sección de Antecedentes — más un DSA determinista/Monte Carlo sencillo. Coherente con
  el pedido de Pablo de no pasarse de nivel.
- **Opción B**: reutilizar piezas ya construidas en la tesis individual (el repo `Deuda/`), citando el
  propio trabajo. Riesgo: contradice el pedido explícito de Pablo de mantenerlo simple, y mezcla un
  trabajo de cátedra grupal con una tesis individual — a evitar salvo que Pablo lo autorice.

Una vez elegida la opción, redactar el párrafo de cierre de Antecedentes que pide Pablo (por qué esa
metodología, por qué esas variables — tres razones posibles: no se probó antes / el contexto
evolucionó / hay una variable relevante ausente en los antecedentes revisados).

## Fase 3 — Fuente de datos para vencimientos en moneda extranjera
Ver respuesta completa abajo. Resumen: usar el informe mensual de la Oficina de Presupuesto del
Congreso (OPC), *Operaciones de Deuda Pública*, como fuente puntual para la cifra que se cita en la
Introducción. No existe una fuente única y homogénea para una serie histórica larga de vencimientos
por moneda — no vale la pena reconstruirla; alcanza con el stock "% deuda en moneda extranjera", que
ya está en la matriz de datos de la tesis individual como proxy de descalce cambiario.

## Fase 4 — Resto del documento del proyecto de cátedra
Pendiente de confirmar qué otras secciones existen o faltan (marco teórico, metodología, cronograma).
No se subieron archivos de esas secciones todavía — avisar cuando estén para sumarlas al plan.

## Fase 5 — Reenvío a Pablo
Reenviar Introducción + Antecedentes corregidos, dejando explícito en el mail/entrega qué comentario
se resolvió con qué cambio, y qué queda abierto (el párrafo de cierre metodológico, condicionado a la
Fase 2).

---

## Nota aparte: la tesis individual (repo `Deuda/`) sigue con su propio plan, ya definido la sesión
anterior en la nota metodológica (`outputs/SVAR_Metodologia_Resultados_Accesible.docx`, Sección 7):
1. FRF de Bohn anual 1983–2025 (prioridad 1, no depende de ningún empalme trimestral).
2. Empalme fiscal trimestral 1983–2003 y reestimación del SVAR y el DSA sobre la ventana completa
   (prioridad 2).
Los dos proyectos (cátedra vs. tesis individual) son independientes; no hace falta que avancen al
mismo ritmo ni que se mezclen.
