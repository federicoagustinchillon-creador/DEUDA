# Área de vacancia (versión 1, borrador para revisar)

Reemplaza el "Área de vacancia" de `Introduccion_corregida.docx` (Santiago) y se fusiona con la
sección `sec:vacancia` de `tesis/capitulos/02_estado_del_arte.tex`. Las marcas `[VERIFICAR]` son
pendientes.

## Qué había y por qué hay que cambiarlo

Santiago planteó la vacancia así: los modelos de sostenibilidad restringen el perímetro al SPNF,
y "los marcos estandarizados, incluido el SRDSF del FMI, excluyen los pasivos remunerados del
Banco Central". Esa afirmación no se sostiene:

1. La revisión del marco del FMI (FMI, 2021, anexo II, párr. 5) establece que las letras de
   liquidez del banco central se incluyen en la deuda pública si se cumple al menos una de tres
   condiciones: que puedan financiar al gobierno, que el gobierno responda de hecho por su
   servicio o que representen un riesgo fiscal material. La nota 8 del mismo documento menciona
   a Argentina: las letras del BCRA sumaban 5% del PIB a fines de 2018.
2. Todo indica que el análisis de deuda del FMI para Argentina de 2025 (Informe de País
   N.° 25/95, anexo I) incluye una línea de "deuda del BCRA (títulos)" en sus tablas.
   [VERIFICAR en el PDF original: el sitio del FMI bloquea la descarga automática y esto surge de
   resúmenes de búsqueda, no de la lectura directa. Hay que bajarlo a mano.]

Si la vacancia se presenta como "nadie incluye al BCRA", el primer jurado que conozca el marco
del FMI la tira abajo. Hay que reformularla sobre lo que efectivamente nadie hizo.

La vacancia que ya tenía el `.tex` (identificación estructural de los canales) sigue siendo
válida y es el núcleo. La propuesta es combinar las dos en una sola vacancia de tres partes.

## Texto propuesto

### Área de vacancia

La literatura revisada deja tres aspectos sin cubrir de manera conjunta para el caso argentino.

El primero es la identificación estructural de los canales de transmisión. La literatura local, tanto desde el enfoque contable (Rodríguez, 2023; Sanches, 2019) como desde la economía política (Aruguete, 2021; Bohoslavsky y Cantamutto, 2024; Cantamutto et al., 2024), vincula el esfuerzo fiscal y el riesgo soberano de forma argumentativa, pero no estima un sistema en el que los shocks se propaguen entre el resultado fiscal, el riesgo país, el tipo de cambio real y la actividad. La literatura internacional sí modela esa transmisión, pero sobre paneles de países (Medeiros, 2012; Adler y Sosa, 2014). En la evaluación más reciente de funciones de reacción fiscal para América Latina, Argentina ni siquiera integra el grupo de países con series aptas para una estimación individual (González y Hernández, 2023). El *fan chart* del FMI, por su parte, aplica al escenario base shocks extraídos de la historia de los determinantes de la deuda, sin identificar su origen (FMI, 2021, párr. 52). Por eso no permite atribuir el riesgo a una perturbación concreta.

El segundo es la cuantificación de un shock externo identificado. Los efectos de la política monetaria de la FED sobre América Latina se estudiaron en paneles regionales y sobre flujos de capital, spreads y actividad (Klemm et al., 2014; Adler y Sosa, 2014). No se los tradujo en un cambio en la probabilidad de que la deuda argentina no se estabilice. Levy Yeyati y Sturzenegger (2023) incluyen la tasa internacional en su VAR, pero su variable de interés es el patrimonio neto del sector público, no la dinámica de la deuda, y su sistema no incluye el riesgo soberano ni la respuesta fiscal.

El tercero es el perímetro de la deuda en la estimación. El marco del FMI prevé incluir los pasivos del banco central en el stock de deuda cuando representan un riesgo fiscal (FMI, 2021). Sin embargo, su *fan chart* no estima cómo esos pasivos evolucionaron históricamente junto con el resto de los determinantes. En Argentina, los pasivos remunerados del BCRA llegaron a cerca del 9,5% del PIB en 2022-2023 y respondieron a los mismos shocks cambiarios y de riesgo que la deuda del Tesoro. Un modelo estimado solo con la deuda del SPNF omite esa parte del endeudamiento y puede subestimar la sensibilidad de la deuda a esos shocks. Esto vale aunque, desde 2024, el stock de esos pasivos se haya reducido a niveles mínimos: la proyección parte de un BCRA casi sin pasivos, pero los parámetros que la gobiernan se estiman sobre tres décadas en las que no lo estuvo.

Esta tesis atiende las tres omisiones con un solo diseño: un SVARX de caso único para Argentina (1996-2025), estimado sobre la deuda consolidada del SPNF y el BCRA, con identificación estructural de los canales y la tasa de la FED como variable exógena. Sus resultados alimentan una simulación de Monte Carlo que expresa el riesgo con las métricas del propio FMI.

## Qué hay que verificar antes de cerrar

| Afirmación | Estado |
|---|---|
| FMI 2021 incluye letras del banco central bajo condiciones (anexo II, párr. 5) | Verificado en el PDF local `Bibliografia/descargas_verificacion/imf2021_dsf_mac_review.pdf` |
| FMI 2021 menciona 5% del PIB de letras del BCRA a fines de 2018 (nota 8) | Verificado, mismo PDF |
| *Fan chart* del FMI con shocks históricos, sin identificación (párr. 52) | Verificado, mismo PDF |
| El análisis del FMI de 2025 para Argentina incluye "BCRA debt (securities)" | **Pendiente**: bajar a mano el Informe de País 25/95 |
| 9,5% del PIB de pasivos del BCRA en 2022-2023 | Dato de nuestra serie (`ingesta_bcra_pasivos.py`); revisar en el paso de datos |
| Levy Yeyati y Sturzenegger: VAR con tasa internacional, sin riesgo soberano | Según `antecedentes_notas_tecnicas.md`; releer el paper para confirmar que no incluyen riesgo soberano |
| González y Hernández (2023) excluyen a Argentina de la estimación individual | Ya estaba en el `.tex`; confirmar la referencia completa en `referencias.bib` |
| Klemm et al. (2014) trabajan en panel regional | **Pendiente**: leer el capítulo |
