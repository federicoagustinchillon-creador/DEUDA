# Auditoría de citas — Capítulo 2 (Estado del Arte)

Contexto: el `.bib` original (bloque "NUEVOS PLACEHOLDERS FASE 7B") contenía 10 citas con
autores reales del campo pero títulos, revistas y coautorías total o parcialmente
fabricados. Cada entrada de esta tabla fue reemplazada por la fuente real, descargada
en esta carpeta para que se pueda verificar sin depender de mi palabra. Fecha de la
auditoría: agosto de 2026.

| Clave `.bib` | Archivo local (esta carpeta) | Fuente / URL de origen | Qué verifiqué |
|---|---|---|---|
| `sanches2019` | `sanches_2019_tesis_utdt.pdf` | Ya estaba en `Bibliografia/` (`MECAP_Sanches_2020 (1).pdf`) | Tesis de Maestría en Economía Aplicada, Pablo Sanches, UTDT, tutor Manuel Macera. Portada + resumen leídos íntegros. NO es un paper de journal — corregido de "Journal of Financial Stability" a tesis de maestría. |
| `libman2024` ⚠️ retirado del `.bib`, ver "Reclasificación" abajo | `libman_delavega_zack_2024_fundar.pdf` | Ya estaba en `data/raw/drive_download/` | Informe de Fundar (think tank), no de "Revista de CEPAL" como decía el bib original. Confirmado también por búsqueda web (fund.ar). |
| `rodriguez2023` | `rodriguez_2023_ciencias_economicas_unl.pdf` | Ya estaba en `data/raw/drive_download/`; DOI real: https://doi.org/10.14409/rce.2023.20.e0032 | Agustín Rodríguez, revista *Ciencias Económicas* (UNL), vol. 2, núm. 20, 2023. Leí portada, resumen y 2 páginas de marco teórico. Hallazgo real citado en el Cap. 2: indicador "efectos sobre la deuda pública" negativo en 68% del período 2001-2022. |
| `aruguete2021` | `aruguete_2021_flacso_epp16.pdf` | Ya estaba en `data/raw/drive_download/` | Eugenia Aruguete, *Revista Estado y Políticas Públicas* Nº16 (FLACSO), pp. 101-123. Revista con referato "doble ciego" confirmado (verificado en la página "Sobre la Revista" del mismo número, pág. 3). |
| `roldan2021` | `roldan_2021_tesina_unr.pdf` | Ya estaba en `data/raw/drive_download/` | Valentina Roldán, tesina de grado, Lic. en RRII, UNR, noviembre 2021, tutor José Fernández Alonso. Confirmé por búsqueda de texto completo que sí trata Teoría de Juegos y Cláusulas de Acción Colectiva (20+ páginas con esos términos). |
| `cantamutto2024` | `cantamutto_lobato_rodriguezenriquez_feliz_2024_edulp.pdf` | Ya estaba en `data/raw/drive_download/` (`pm.7502.pdf`) | Cap. 7 de *Deuda y derechos humanos: claves desde el sistema interamericano* (Bohoslavsky y Clérico, eds., EDULP, 2024), pp. 170-195. Leí portada, índice completo del libro y ficha del capítulo. NO verifiqué el cuerpo argumental completo del capítulo (solo título + ubicación editorial) — la caracterización en el Cap. 2 de la tesis es deliberadamente conservadora por eso. |
| `cantamutto2020` ⚠️ retirado del `.bib`, ver "Reclasificación" abajo | `cantamutto_2020_la_deuda_en_nuestras_vidas_FES.pdf` | Descargado de http://collections.fes.de/publikationen/download/pdf/452633 | Cap. 1 "Una vez más, la deuda", Francisco Cantamutto, pp. 2-3, en *La deuda en nuestras vidas: crisis, negociaciones y alternativas* (9 autores), Friedrich-Ebert-Stiftung, septiembre 2020. Leí el capítulo completo (no solo la portada). |
| `feliz2021` | `cantamutto_feliz_2021_nuestramerica.pdf` | Ya estaba en `data/raw/drive_download/` (`pr.15901.pdf`) | Cantamutto y Féliz (2021), "Argentina entre la sostenibilidad de la deuda y la vida", *Revista Nuestramérica*, vol. 7, núm. 17, e6167845. La coautoría la confirmé de dos formas: (1) búsqueda web (Zenodo, CONICET, JSTOR listan 2 autores) y (2) leyendo el cuerpo del artículo, que usa primera persona plural en todo el texto ("Argumentamos que la sostenibilidad de la deuda se opone a la sostenibilidad de la vida..."), inconsistente con autoría única. El PDF descargado solo lista a Féliz en la ficha de depósito de FAHCE-UNLP, lo que parece ser indexación incompleta de ese repositorio puntual, no un error de coautoría real. Cerrado. |
| `bohoslavsky2024` | `bohoslavsky_cantamutto_2024_FACES.pdf` | Descargado de https://nulan.mdp.edu.ar/id/eprint/4109/1/FACES-30-62-bohoslavsky-cantamutto.pdf | Bohoslavsky y Cantamutto (2024), *FACES: Revista Iberoamericana de Ciencias Económicas y Sociales* (UNMDP), vol. 30, núm. 62, pp. 1-18. Agregada como fuente Nivel 1 (con referato) para anclar la sección de Cantamutto, que de otro modo solo tenía capítulos de libro. |

## Eliminadas (no readmitidas)

- **`lagorio2021`** y **`sacco2021`**: los autores (Franco Lagorio, Irene Sacco) y el
  contenido son reales — los encontré en `Análisis CIPEI-GEFI, Edición Especial,
  octubre 2021` (Universidad Nacional de Rosario) — pero esa publicación se
  autodescribe en su propia página editorial como una colección de "reflexiones
  de jóvenes estudiantes y graduados", sin proceso de referato. No cumple ningún
  nivel de la jerarquía de citación de `estandar_calidad.md`. Se sacaron del
  `.bib` y de la subsección del Cap. 2 que las citaba.
- **`campos2021`**: duplicado fabricado de la misma fuente real que `feliz2021`
  (mismo tema, año y autores, título y revista distintos). Se eliminó la entrada
  duplicada; se mantuvo `feliz2021`.

## Lo que NO hice

No releí el cuerpo argumental completo de los libros/informes de más de 20 páginas
(Cantamutto et al. 2024, Libman et al. 2024) — verifiqué portada, índice, ficha
bibliográfica y, cuando fue posible, el resumen o la sección directamente relevante.
Si se necesita verificación línea por línea de algún argumento específico atribuido
a estas fuentes en el Cap. 2, avisame cuál y lo reviso a fondo.

## Reclasificación por jerarquía de citación (agosto 2026)

Revisión posterior de las ~48 entradas de `referencias.bib` contra la jerarquía
Nivel 1/2/3 de `estandar_calidad.md`. `libman2024` (Fundar) y `cantamutto2020`
(Friedrich-Ebert-Stiftung) son informes técnicos/de divulgación, sin referato,
usados en el Cap. 2 y Cap. 7 como evidencia de vacancia y de fundamentación
interpretativa — el punto exacto donde la jerarquía de citación de la cátedra
aplica. Se buscó reemplazo Nivel 1/2 y se resolvió así:

- **`libman2024`** (aporte metodológico: DSA estocástico con simulación de
  Monte Carlo para la Argentina): se agregó **`celasun2006`** (Celasun, Debrun
  y Ostry, *Primary Surplus Behavior and Risks to Fiscal Sustainability in
  Emerging Market Countries: A "Fan-Chart" Approach*, IMF Working Paper WP/06/67,
  2006 — Nivel 2, FMI) como anclaje del argumento metodológico general, que es
  en efecto anterior y más general que la aplicación de Libman et al. al caso
  argentino. `libman2024` se retiró de `referencias.bib` y del aparato de citas
  formal; se mantiene mencionado por nombre en el cuerpo del texto (Cap. 2 y
  Cap. 7) como informe técnico, explícitamente calificado como tal, sin
  `\citep`/`\citet`. PDF descargado: `celasun_debrun_ostry_2006_imf_staffpapers.pdf`
  (fuente: imf.org, acceso abierto).
- **`cantamutto2020`** (argumento de restricción externa/margen fiscal
  bimonetario): se agregó **`damill2015`** (Damill, Frenkel y Rapetti,
  *Macroeconomic Policy in Argentina During 2002–2013*, *Comparative Economic
  Studies*, 57(3), 369-400, 2015 — Nivel 1, revista con referato) para ese
  punto específico. Para el argumento distinto y no sustituible sobre
  "condiciones de reproducción social" (07\_discusion.tex, economía
  feminista/social reproduction, fuera del alcance de Damill et al.), no se
  encontró reemplazo Nivel 1: se aplicó la mención no bibliográfica (se retiró
  del `.bib`, se mantiene como cita nombrada y calificada como informe sin
  referato). PDF descargado: `damill_frenkel_rapetti_2015_ces.pdf` (fuente:
  repositorio institucional CONICET, acceso abierto, versión aceptada del
  autor).

Las 10 citas adicionales identificadas como *working papers* o documentos
institucionales sin referato (Bohn 2005 CESifo, Mendoza 2004/2009, Eichengreen
2003 NBER, Blanchard 1990/2021/2022, Sargent 1981, Everaert 2017, Mauro 2013
FMI) se dejaron sin cambios: se usan en Marco Teórico/Discusión/Conclusiones
como fundamentación teórica canónica de la literatura internacional de
sostenibilidad de deuda, nunca como antecedente empírico local en el Cap. 2 —
el contexto textual en el que la jerarquía de citación de la cátedra aplica —,
y citar *working papers* de NBER/CESifo/OCDE/FMI para ese fin es práctica
estándar en el campo.
