# Plan de labor — Tesis oficial (director Pablo)

Esta es la tesis, la versión oficial que arranca ahora con Pablo como director. Es distinta del
desarrollo cuantitativo que ya existe en `tesis/`, `codigo/` y `resultados/` (SVAR, VECM, CIR,
TVECM, DSA sobre 2004–2025 y la extensión 1983–2025): ese trabajo es previo/paralelo y todavía no
está decidido cómo entra en esta versión oficial — como insumo para el capítulo de resultados una
vez que la Fase 2 defina la metodología, como apéndice técnico, o reescrito a la medida de lo que
Pablo pida. No asumir nada al respecto sin que el usuario lo confirme. Se arregla por fases, cada
una cerrable en una sesión.

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

## Fase 2 — Decisión metodológica de la tesis oficial
En una entrevista previa con el grupo (Páez, Carricondo, Chillón), Pablo había pedido explícitamente
**no profundizar a nivel de tesis de grado** — un análisis simple pero prolijo. Esa conversación fue
antes de que esto se formalizara como la tesis oficial, así que hay que confirmar con él si ese
límite sigue en pie ahora que el documento es la tesis en serio, o si cambia el alcance. Sin esa
confirmación, no asumir ninguna de las dos cosas. Opciones sobre la mesa:

- **Opción A**: FRF simple a la Bohn (superávit primario ~ deuda rezagada + brecha del producto), el
  mismo tipo de ejercicio que hace Medeiros (2012) — que ya es la columna vertebral de la sección de
  Antecedentes — más un DSA determinista/Monte Carlo sencillo. La más alineada con lo que Pablo pidió
  en esa entrevista, si ese límite sigue vigente.
- **Opción B**: incorporar como cuerpo de la tesis el desarrollo cuantitativo que ya existe en
  `tesis/`, `codigo/` y `resultados/` (SVAR, VECM, CIR, TVECM, DSA), reescribiendo Introducción y
  Antecedentes para que encajen con esa profundidad. Viable si Pablo confirma que el alcance cambió.

Ninguna opción se elige sin que el usuario lo defina (con Pablo, si hace falta). Una vez elegida,
redactar el párrafo de cierre de Antecedentes que pide Pablo (por qué esa metodología, por qué esas
variables — tres razones posibles: no se probó antes / el contexto evolucionó / hay una variable
relevante ausente en los antecedentes revisados).

## Fase 3 — Fuente de datos para vencimientos en moneda extranjera
Ver respuesta completa abajo. Resumen: usar el informe mensual de la Oficina de Presupuesto del
Congreso (OPC), *Operaciones de Deuda Pública*, como fuente puntual para la cifra que se cita en la
Introducción. No existe una fuente única y homogénea para una serie histórica larga de vencimientos
por moneda — no vale la pena reconstruirla; si la Opción B avanza, alcanza con el stock "% deuda en
moneda extranjera" que ya está en la matriz de datos como proxy de descalce cambiario.

## Fase 4 — Resto del documento
Pendiente de confirmar qué otras secciones existen o faltan (marco teórico, metodología, cronograma,
y si la Opción B avanza, cómo se reordenan los capítulos ya escritos en `tesis/capitulos/`). No se
subieron archivos de esas secciones todavía — avisar cuando estén para sumarlas al plan.

## Fase 5 — Reenvío a Pablo
Reenviar Introducción + Antecedentes corregidos, dejando explícito en el mail/entrega qué comentario
se resolvió con qué cambio, y qué queda abierto (el párrafo de cierre metodológico y la decisión de
alcance, ambos condicionados a la Fase 2).
