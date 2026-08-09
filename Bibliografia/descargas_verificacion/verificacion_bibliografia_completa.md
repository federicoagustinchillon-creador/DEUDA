# Auditoría completa de `referencias.bib` (agosto 2026)

Verificación exhaustiva de las ~50 entradas de `tesis/referencias.bib` contra
fuente primaria (no contra memoria ni contra bibliografías de terceros), a
pedido explícito del usuario tras encontrar dos citas mal atribuidas
(`mauro2013`, `everaert2017`) durante la descarga de fuentes de acceso abierto.
Complementa `verificacion_citas_cap2.md` (que cubre el bloque de antecedentes
locales del Cap. 2) y `verificacion_citas_revision_pares.md` (citas agregadas en
la revisión de pares de H1-H7).

## 1. Errores encontrados y corregidos

| Clave | Problema encontrado | Corrección |
|---|---|---|
| `mauro2013` → **`ostry2010`** | El título "Fiscal Space" estaba atribuido a Mauro, Romeu, Binder y Zaman (IMF WP 13/67) — un paper real de esos autores, pero sobre otro tema ("A Modern History of Fiscal Prudence and Profligacy", WP/13/5). El artículo que realmente formaliza "espacio fiscal" como distancia entre deuda vigente y límite de deuda es Ostry, Ghosh, Kim y Qureshi (2010), IMF Staff Position Note SPN/10/11. | Entrada reemplazada por `ostry2010`; cita actualizada en `01_introduccion.tex`. PDF descargado y verificado (portada confirma título/autores/número). |
| `everaert2017` | Título "Debt Sustainability in Emerging Markets: A Dynamic Panel Threshold Analysis" (De Nederlandsche Bank) no corresponde a ningún trabajo real de estos autores. El paper real es "On the Estimation of Panel Fiscal Reaction Functions: Heterogeneity or Fiscal Fatigue?", National Bank of Belgium WP No. 320 — panel OCDE (no economías emergentes), con hallazgo más matizado (heterogeneidad entre países, fatiga fiscal no generalizada). | `.bib` corregido a la fuente real. Párrafo de `01_introduccion.tex` reescrito para reflejar fielmente el hallazgo real (ver diff). PDF descargado y verificado (abstract confirma autores/año/hallazgo). |
| `blanchard2021` | Número y año equivocados: "Peterson Institute Policy Brief 21-4, 2021" no existe con ese contenido. El *policy brief* real de Blanchard con ese título es PB19-2 (2019). | Número/año corregidos a 19-2/2019 (se mantuvo la clave `.bib` `blanchard2021` para no romper referencias cruzadas). |
| `everaert2017` (número) | Ya corregido arriba junto con el título/institución. | — |
| `mendoza2007` | Journal, volumen, año y página final equivocados: decía "Economía", vol. 7(2), 2007, pp. 133-173. La publicación real es *Economía Mexicana. Nueva Época*, vol. XVIII, núm. 2, **2009**, pp. 133-**177**. | Corregido. PDF descargado (redalyc.org) y verificado contra portada. |
| `bassi2015` | Título, autoría y editorial equivocados: decía "Formulación del diseño de investigación", autoría única de Bassi, editorial Prometeo. El libro real es *"Formulación de proyectos de tesis en ciencias sociales: Manual de supervivencia para estudiantes de pre- y posgrado"*, coautoría con Pablo Hernández, Santiago de Chile, FACO/El Buen Aire (2015). | Corregido. No se consiguió PDF de acceso abierto verificable (el enlace de ResearchGate devolvió una página de login, no el archivo); se documenta el enlace de reseña verificado en la sección 3. |
| `cohen2019` | Título equivocado: decía "Validez y confiabilidad instrumental". El libro real es *"Metodología de la investigación, ¿para qué? La producción de los datos y los diseños"* (Cohen, Néstor y Gómez Rojas, Gabriela, Teseo, 2019). | Corregido. PDF descargado (CLACSO, acceso abierto) y verificado contra portada. |
| `engle1982` | Página final: decía 987-1007; el consenso de fuentes primarias es 987-**1008**. | Corregido (diferencia menor de una página). |

Las entradas `libman2024` y `cantamutto2020` fueron retiradas del `.bib` en un
paso previo de esta misma sesión (ver nota en `referencias.bib` y sección
"Reclasificación..." de `verificacion_citas_cap2.md`) — no son un error de dato,
sino una reclasificación por jerarquía de citación (informes técnicos sin
referato usados como evidencia de vacancia local, reemplazados por
`celasun2006` y `damill2015` donde correspondía, o mantenidos como mención no
bibliográfica).

## 2. Entradas verificadas sin cambios

Título, autoría, journal/editorial, volumen y páginas confirmados exactos
contra fuente primaria (Econometric Society, Oxford Academic, Wiley, MIT
Press, ScienceDirect, editoriales de cada libro, etc.): `aruguete2021`,
`bachelard1938`, `bai2003`, `blanchard1990`, `blanchard2019`, `blanchard2022`,
`bohn1998`, `bohn2007`, `bohoslavsky2024`, `bollerslev1990`, `bound1995`,
`brown1975`, `caner2004`, `cantamutto2024`, `celasun2006`, `damill2015`,
`demarta2005`, `derasmo2016`, `eichengreen2003`, `elliott1996`, `engle1987`,
`engle2002`, `feliz2021`, `ghosh2013`, `hamilton2018`, `hansen1999`,
`hansen2000`, `imf2003`, `imf2021`, `marradi2007`, `ostry2010`, `phillips1990`,
`rodriguez2023`, `rojas2013`, `roldan2021`, `samaja1993`, `sanches2019`,
`sargent1981`, `staiger1997`, `stock1993`, `truong2020`, `ynoub2007`,
`zivot1992`.

## 3. Acceso a las fuentes que no se descargaron (paywall o libro sin edición abierta)

Siguiendo la instrucción de no intentar sortear paywalls, para las citas
verificadas que no tienen edición de acceso abierto se deja constancia del
enlace oficial/DOI en lugar del PDF completo:

| Clave | Enlace oficial verificado |
|---|---|
| `engle1982` | https://www.econometricsociety.org/publications/econometrica/1982/07/01/autoregressive-conditional-heteroscedasticity-estimates |
| `engle1987` | https://www.econometricsociety.org/publications/econometrica/1987/03/01/co-integration-and-error-correction-representation-estimation |
| `engle2002` | https://ideas.repec.org/a/bes/jnlbes/v20y2002i3p339-50.html |
| `bollerslev1990` | https://public.econ.duke.edu/~boller/Published_Papers/restat_90.pdf (versión de autor, acceso abierto) |
| `brown1975` | https://doi.org/10.1111/j.2517-6161.1975.tb01532.x |
| `stock1993` | https://www.econometricsociety.org/publications/econometrica/1993/07/01/simple-estimator-cointegrating-vectors-higher-order-integrated |
| `bai2003` | https://doi.org/10.1002/jae.659 |
| `elliott1996` | https://www.econometricsociety.org/publications/econometrica/1996/07/01/efficient-tests-autoregressive-unit-root |
| `phillips1990` | https://academic.oup.com/restud/article-abstract/57/1/99/1610097 |
| `staiger1997` | https://www.econometricsociety.org/publications/econometrica/1997/05/01/instrumental-variables-regression-weak-instruments |
| `zivot1992` | https://doi.org/10.1080/07350015.1992.10509904 |
| `bohn1998` | https://doi.org/10.1162/003355398555793 (The Quarterly Journal of Economics) |
| `bohn2007` | https://doi.org/10.1016/j.jmoneco.2006.12.013 |
| `ghosh2013` | https://doi.org/10.1111/ecoj.12010 -- versión de trabajo de acceso abierto: https://www.nber.org/system/files/working_papers/w16782/w16782.pdf |
| `hamilton2018` | https://doi.org/10.1162/rest_a_00706 -- versión de trabajo de acceso abierto: https://www.nber.org/system/files/working_papers/w23429/w23429.pdf |
| `derasmo2016` | https://doi.org/10.1016/bs.hesmac.2016.03.007 -- versión de trabajo de acceso abierto: https://www.nber.org/system/files/working_papers/w21574/w21574.pdf |
| `blanchard2019` | https://doi.org/10.1257/aer.109.4.1197 -- versión de trabajo de acceso abierto: https://www.piie.com/sites/default/files/documents/wp19-4.pdf |
| `blanchard2022` | https://www.imf.org/en/Publications/fandd/issues/2022/03/Deciding-when-debt-becomes-unsafe-Blanchard (acceso abierto, revista de divulgación del FMI) |
| `truong2020` | https://doi.org/10.1016/j.sigpro.2019.107299 -- versión de trabajo de acceso abierto: https://arxiv.org/abs/1801.00718 |
| `bassi2015` | https://www.redalyc.org/articulo.oa?id=53744426015 (reseña con datos bibliográficos completos; no se encontró el libro completo en acceso abierto verificable) |

Libros de metodología/epistemología de cátedra (`bachelard1938`, `samaja1993`,
`ynoub2007`, `rojas2013`) no se buscaron en acceso abierto: son textos con
derechos de autor vigentes, y `marradi2007` ya está físicamente disponible en
`Bibliografia/` (ejemplar completo). Documentar su ficha bibliográfica
verificada (como se hizo en la Sección 2) es suficiente sin necesidad de
alojar una copia completa.

## 4. PDFs nuevos descargados en esta sesión (Bibliografia/descargas_verificacion/)

- `ostry_ghosh_kim_qureshi_2010_imf_spn.pdf`
- `celasun_debrun_ostry_2006_imf_staffpapers.pdf`
- `damill_frenkel_rapetti_2015_ces.pdf`
- `bohn2005_cesifo_wp1446.pdf`
- `mendoza2004_nber_w10637.pdf`
- `mendoza_oviedo_2009_economia_mexicana.pdf`
- `blanchard1990_oecd_wp79.pdf`
- `sargent_wallace_1981_minneapolisfed.pdf`
- `everaert_jansen_2017_nbb_wp320.pdf`
- `imf2003_sustainability_assessments.pdf`
- `imf2021_dsf_mac_review.pdf`
- `cohen_gomezrojas_2019_teseo.pdf`

Todas verificadas por extracción de texto de la portada/abstract, no solo por
tamaño de archivo o código de respuesta HTTP.

## 5. Acervo de Marco Legal Descargado (Bibliografia/marco_legal/)

- `ley_24156_administracion_financiera.txt` (Ley N° 24.156, Arts. 56 a 66)
- `ley_24144_carta_organica_bcra.txt` (Ley N° 24.144, Arts. 18, 19, 20 y 22)
- `ley_25152_solvencia_fiscal.txt` (Ley N° 25.152)
- `ley_27541_solidaridad_social_deuda.txt` (Ley N° 27.541)
- `ley_27612_fortalecimiento_sostenibilidad_deuda.txt` (Ley N° 27.612)
- `decretos_canje_y_reestructuracion_deuda.md` (Decretos 1735/2004, 563/2010, 332/2020 y 676/2020)
- `marco_legal_deuda_argentina.md` (Compendio sintético de aplicación empírica)

Textos oficiales verificados contra la publicación del Boletín Oficial de la República Argentina.

