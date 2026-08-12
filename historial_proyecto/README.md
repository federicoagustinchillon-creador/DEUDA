# Historial del proyecto — archivo, no especificación vigente

Todo lo que hay acá adentro es de una etapa anterior de la tesis. Nada de esto describe la estructura final: para eso está el [`README.md`](../README.md) de la raíz del repositorio y los capítulos en [`tesis/capitulos/`](../tesis/capitulos/). Se conserva esta carpeta como registro de cómo se llegó al diseño final, no como referencia para trabajar hoy.

Ejemplos concretos de por qué no hay que guiarse por estos documentos:
- `documentos_planificacion/05_METODOLOGIA_Variables.md` fija la Unidad de Análisis en "Mes/Año". La tesis final usa el **trimestre** (ver [`04_metodologia.tex`](../tesis/capitulos/04_metodologia.tex), sección Unidad de Análisis) — el mes se descartó porque el Resultado Primario y la Deuda Bruta del SPNF consolidado no tienen publicación mensual verificable.
- `documentos_planificacion/estructura_proyecto.md` describe capítulos `main.tex` y `latex/capitulos/05_analisis_descriptivo.tex` a `08_conclusiones.tex`. El documento real es `tesis/fuente/Tesis.tex`, con capítulos `00_abstract.tex` a `09_apendice.tex` — la numeración y el contenido cambiaron.
- `documentos_planificacion/notas_contexto_proyecto.md` ya trae su propia advertencia al inicio: registra el diseño aprobado en el TP3 de la cursada, previo a que H1 se refinara hacia el canal EMBI+/riesgo soberano.

## Qué hay en cada subcarpeta

- **`documentos_planificacion/`** — cronograma, bitácora de decisiones metodológicas, estándares de calidad y planes de mejora escritos durante el proceso. Útil si querés entender *por qué* se tomó una decisión (ver especialmente `bitacora_decisiones_metodologicas.md`), no *qué* dice la tesis hoy.
- **`versiones_pdf_anteriores/`** — PDFs compilados en etapas previas (`TesisAuditada.pdf`, `Tesis_APA7.pdf`). No son el PDF vigente: ese es [`tesis/Tesis.pdf`](../tesis/Tesis.pdf), siempre el más actualizado.
