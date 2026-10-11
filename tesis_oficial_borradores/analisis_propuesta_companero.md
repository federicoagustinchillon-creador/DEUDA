# Análisis de la propuesta del compañero (2026-10-10)

Documento de trabajo interno, no se pega en la tesis. Compara los tres archivos que subió el
compañero (`Introduccion_corregida.docx`, `Introducción_completo_pie_pagina2.docx`,
`metodologia.docx`) contra el estado real de la tesis (`tesis/capitulos/`, `codigo/`,
`resultados/tablas/`, `plan_de_labor.md` hasta la Fase 8).

## 0. Qué es cada archivo

| Archivo | Qué es | Estado |
|---|---|---|
| `Introducción_completo_pie_pagina2.docx` | Versión vieja de Intro + Antecedentes. Objetivo sobre "deuda pública internacional", sin pregunta ni hipótesis. | Superada por la otra. No usar. |
| `Introduccion_corregida.docx` | Versión nueva: pregunta, pregunta específica (shock FED), objetivos, H1a/H1b/H2, antecedentes ampliados y un "Área de vacancia" (perímetro SPNF + BCRA). | Base de discusión. Tiene huecos `[COMPLETAR]` y un párrafo cortado a mitad de oración ("absorción monetaria creciente media"). |
| `metodologia.docx` | Notas de trabajo, no texto redactable. Mezcla tres borradores, restos de respuestas de chat de IA ("En el modelo de tu tesis tenés dos formas...") y marcas de citas de NotebookLM sin limpiar ("1more_horiz", "3738", "8more_horiz"). | Lista de ideas. No pegar nada tal cual. |

## 1. Lo central: la propuesta es compatible con lo que ya tenés

La arquitectura que propone (VAR estructural con variables macro, identidad de acumulación con
descalce de monedas, Monte Carlo con fan chart, insolvencia = deuda > 100% del PIB en 2035) es
la misma que ya está corrida en la tesis. Varias cosas que él plantea como "a hacer" ya existen:

| Propone | Ya está en la tesis | Archivo |
|---|---|---|
| SVAR con PIB, TCRM, EMBI+, pb, deuda | SVAR restringido con g_gap, pb, EMBI, TCRM, deuda_pib, 1996-2025, n=120 | `fase23_reestimacion_1996_2025.py` |
| Ley de movimiento con separación de monedas (su "Opción B") | `simulate_dsa_path` ya separa tramo en pesos (alpha = 0,463) y en dólares con efecto de valuación (1+Δe) | `fase6_sostenibilidad_deuda.py:119-130` |
| Monte Carlo 1.000 trayectorias, fan chart p10-p90 | Igual, con shocks t de Student y covarianza derivada de la matriz de impacto del SVAR | `fase6_sostenibilidad_deuda.py:134` |
| Probabilidad de insolvencia = P(d_2035 > 100% PIB) | **26,1%**, mismo umbral | `resultados/tablas/fase6_dsa_probabilidad.csv` |
| ADF/KPSS, Zivot-Andrews, Bai-Perron | Hechos (Etapa 1 y H1b actual) | `numeros_ventana_unica_1996_2025.md` §4-5 |
| "Hacer el test de FRF para demostrar que no aplica a Argentina" | **Ya está demostrado**: el VECM no encuentra reacción fiscal (p = 0,996) y el pb explica solo 12,7% de la varianza de la deuda a 20 trimestres | `numeros_ventana_1996_2025.md` §6 |

Este último punto es el más valioso: la intuición de tu compañero (con Adler y Sosa, 2014) de
que la FRF no aplica a la Argentina **coincide con tu resultado empírico**. No hay que hacer un
test nuevo: tu VECM y tu FEVD son ese test. Eso permite unir las dos líneas sin tirar nada.

## 2. Evaluación punto por punto

### 2.1 Pregunta de investigación

Su pregunta general es buena y más precisa que la actual (explicita perímetro SPNF+BCRA,
período histórico y horizonte). Problema: es larga y repite el objetivo casi palabra por
palabra. Recomendación: adoptarla, acortada.

> ¿En qué medida los determinantes macroeconómicos de Argentina (1996-2025) condicionan la
> sostenibilidad de su deuda pública consolidada en el horizonte 2026-2035, y cuál es la
> probabilidad de que esa trayectoria resulte insostenible?

### 2.2 Pregunta específica: shock de la FED

**Adoptarla.** Es la mejor idea nueva de la propuesta, por tres razones:

1. Responde al pedido de Pablo de justificar "dónde gira todo" el SVAR con un shock concreto y
   bien fundamentado (los cuatro canales que enumera están bien citados).
2. Corrige una justificación débil que hoy tiene la tesis (Fase 6 del plan): se descartó el
   shock monetario "porque no hay serie de tasa de política con 30 años". Eso vale para la tasa
   del BCRA, no para la FED: la Fed Funds y la tasa sombra de Wu-Xia (para 2009-2015 y 2020-2021,
   cuando la tasa estuvo en cero) están completas para 1996-2025 en FRED.
3. Es exógena para Argentina por construcción, así que entra como variable exógena (SVARX) sin
   necesidad de discutir endogeneidad, que Pablo pidió no nombrar.

Cuidado técnico que hay que resolver antes de escribir: meter la tasa de la FED en nivel no es un
"shock". Opciones, de más simple a más rigurosa:
- (a) Δ de la tasa sombra de Wu-Xia como exógena. Simple y defendible para grado.
- (b) Serie de shocks de política monetaria de alta frecuencia (Bauer-Swanson 2023 o
  Jarociński-Karadi 2020) agregada a trimestral. Más limpia, pero la cobertura termina antes de
  2025 en algunas versiones: verificar antes.

Recomiendo (a) en el cuerpo y mencionar (b) como robustez si da el tiempo.

Además, el Monte Carlo necesita una regla para la variable exógena en 2026-2035. Lo simple:
escenario base con la tasa según el sendero de los *dots* de la FED, y escenario de shock con
+100 o +200 pb sostenidos. La H2 se contrasta comparando las dos probabilidades de insolvencia.

### 2.3 Hipótesis

| Propuesta | Juicio | Qué hacer |
|---|---|---|
| H1a: los determinantes condicionan la sostenibilidad; el superávit primario solo no basta | Bien orientada y **ya respaldada por tus datos** (FEVD: inercia 54,2%, cambiario+riesgo 25,8%, fiscal+actividad 20,0%; VECM sin reacción fiscal). Tal como está redactada repite la pregunta. | Reescribir como contrastable: "la varianza de la deuda/PIB está dominada por los canales cambiario y de riesgo soberano antes que por el fiscal, y la reacción del resultado primario a la deuda no es significativa". Se contrasta con VECM + FEVD, que ya están. |
| H1b: la trayectoria no ofrece margen; la probabilidad de insolvencia supera un umbral | Necesaria, pero tiene dos `[COMPLETAR]`. | **Superado (2026-10-10)**: se usa la probabilidad de no estabilización del FMI con corte en 50%, justificado en `introduccion_v3.md`, nota 1. El criterio de 100% del PIB sale de las hipótesis por falta de fuente. |
| H2: shock de la FED aumenta deuda y probabilidad de insolvencia | Buena y contrastable. | Mantener. Agregar la magnitud del shock con criterio justificado (ver `introduccion_v3.md`, nota 2). |

Qué pasa con tus hipótesis actuales:
- **H1a actual (umbral de Hansen/TVECM)**: resultado mixto (Hansen niveles significativo con
  p = 0,000; TVECM no, p = 0,632). No encaja en el esquema de tu compañero. Recomiendo bajarlo
  a resultado complementario dentro de H1a nueva ("además, la reacción fiscal solo aparece por
  encima de ~2.100-2.460 pb"), no a hipótesis propia. Es el patrón "disciplina gatillada por
  crisis", que refuerza que el superávit no es una respuesta sistemática.
- **H1b actual (quiebres estructurales)**: pasa a ser parte del diagnóstico de datos (Etapa 1) y
  justifica las dummies que tu compañero menciona sin desarrollar. Deja de ser hipótesis.

Resultado: tres hipótesis (H1a, H1b, H2) alineadas con pregunta general + pregunta específica,
cada una con una técnica: VECM/FEVD, Monte Carlo base, Monte Carlo con shock FED.

### 2.4 Área de vacancia: perímetro consolidado SPNF + BCRA

La idea es buena y ya estaba en tu Justificación ("la consolidación de los pasivos remunerados
del BCRA... constituye una extensión que la literatura no ha desarrollado"). Pero hay un problema
real que hay que resolver antes de presentarla como el aporte principal:

**Tu SVAR y tu DSA hoy corren sobre deuda SPNF, no sobre la consolidada.** La serie de pasivos
remunerados del BCRA (`pasivos_bcra_pib`) solo existe para 2004-2025 (`fase8_deuda_consolidada.py`,
n=88), y en la Fase 9 se corrigió justamente un bug que rellenaba con cero 1996-2003. O sea, la
tesis promete "deuda consolidada" pero la estimación de 30 años es sobre SPNF.

**Decisión (usuario, 2026-10-10): todo se corre sobre la deuda consolidada, SVAR y DSA.** No se
usa la opción de "SPNF en el SVAR y BCRA solo en el DSA".

Cómo se construye 1996-2025 sin inventar datos: `ingesta_bcra_pasivos.py` ya usa tres series de
la API del BCRA. La de posición neta de pases (idVariable 1261) cubre 1996-2025 según su propio
docstring; LEBAC/NOBAC (1258) arranca en 2002 por diseño del instrumento, no por falta de datos,
así que antes de 2002 vale cero de verdad. El corte en 2004 viene del denominador (PIB nominal
INDEC base 2004), no de los pasivos. Falta: bajar 1996-2003 de las series 1258/1261, empalmar el
PIB nominal base 1993 con el base 2004 y verificar que `deuda_pib` y `pasivos_bcra_pib` usen el
mismo denominador antes de sumarlos.

Nota: con la consolidación, el alpha de deuda en pesos cambia (los pasivos del BCRA son en
pesos). Hay que recalcular `ALPHA = 0.463` para el perímetro consolidado; su "70% en moneda
extranjera" no tiene fuente y no coincide con el 53,7% que usa tu código.

### 2.5 Metodología: qué adoptar y qué no

**Adoptar (barato, mejora la tesis):**
- Protocolo de diagnóstico de residuos del SVAR: LM/Portmanteau, ARCH multivariado,
  Jarque-Bera, raíces dentro del círculo unitario. Cuatro tests, una tabla. Si ya están,
  ordenarlos así.
- Selección de rezagos por AIC/BIC/HQ con residuos sin autocorrelación.
- Dummies de quiebre (2001-09, 2006-03, 2017-09 de tu Bai-Perron) en el SVARX: ahora tu H1b
  actual tiene un uso directo.
- Cholesky como **robustez** del SVAR restringido (no como modelo principal).

**No adoptar o postergar:**
- **Cholesky como identificación principal**: contradice la justificación que ya aprobó Pablo
  (no hay razón teórica para ordenar EMBI+ y TCRM entre sí). Además el documento propone tres
  ordenamientos distintos e incompatibles (uno de 7 variables con PIB mundial adentro, otro de 5
  con TCRM antes del EMBI, otro con Pasivos BCRA como variable). El PIB mundial no puede ir en el
  vector endógeno: es exógeno, va en S_t^ext.
- **Restricciones de signo + Blanchard-Quah**: tres esquemas de identificación es nivel
  maestría. Blanchard-Quah exige neutralidad de largo plazo del TCRM, difícil de defender con 30
  años de Argentina. Descartar ambos.
- **Módulo de balanza de pagos completo** (exportaciones por sector, importaciones con
  elasticidades, IED con Vaca Muerta/RIGI, ecuación satélite de FAE, tasas de rollover local,
  externa y privada, desembolsos de organismos, GFN, absorción bancaria 15%, deuda provincial con
  Chow-Lin). Es otra tesis entera. El propio documento admite que falta "especificar con
  precisión algorítmica" la regla de penalización. Contradice además el recorte acordado
  (tesis de grado, bajar de 100 páginas; hoy en 81). Como máximo: un indicador de cobertura
  (servicio en USD / exportaciones) calculado sobre las trayectorias simuladas, sin
  retroalimentación al VAR. El resto, a "agenda de investigación futura".
- **X-13-ARIMA-SEATS**: solo si alguna serie no viene desestacionalizada. El EMBI+ y el TCRM no
  lo necesitan. Verificar qué hace hoy `construir_dataset_1996_2025.py` antes de agregarlo.
- **VIF < 5 y número de condición < 30**: en un VAR la colinealidad entre rezagos es esperable y
  no invalida las IRF. Sacarlo; era pertinente solo para la ecuación de FAE, que se descarta.

### 2.5b Las dos arquitecturas que plantea `metodologia.docx`

El documento no lo dice con esas palabras, pero mezcla dos diseños distintos:

- **Arquitectura A, SVAR + DSA por separado.** El SVARX proyecta solo las variables macro (g,
  TCRM, EMBI+, pb) y la deuda se acumula afuera, con la ley de movimiento con descalce de
  monedas. Es la que corresponde a la sección "Identidad de Acumulación de Deuda" y a la "Opción
  B". La deuda no retroalimenta al resto de las variables.
- **Arquitectura B, efectos conjuntos.** La deuda consolidada entra como variable endógena del
  SVARX ("la esponja contable del sistema"), así que el nivel de deuda afecta al EMBI+, al TCRM
  y al pb en los trimestres siguientes. El módulo de balanza de pagos con regla de penalización
  (si la cobertura de reservas cruza un umbral, sube el EMBI+ o salta el TCRM en t+1) es una
  versión más extrema de esta misma idea.

Recomendación: **B en su versión acotada**, que es lo que la tesis ya hace con el SVAR restringido.
La deuda está adentro del VAR, pero su ecuación de impacto está restringida por la identidad del
FMI. Así se tienen efectos conjuntos y la acumulación sigue siendo contablemente consistente. A
pura (sin restricción) pierde justo lo que pregunta H2: que el shock de la FED vuelva sobre la
deuda por el canal riesgo-tipo de cambio y que la deuda más alta realimente el riesgo. La regla
de penalización de balanza de pagos queda afuera porque no está especificada. Para la tesis, A
sirve como contraste: la diferencia entre A y B mide cuánto pesa la retroalimentación.

### 2.6 Antecedentes (Introduccion_corregida)

Buen trabajo. Mejoras respecto de la versión vieja: cita de Celasun et al. (2006) como origen de
los fan charts, Hébert-Schreger corregido a "10 puntos porcentuales", Levy Yeyati-Sturzenegger
unificado a 2023. Pendientes:
- Párrafo de Porto (2020) cortado a mitad de oración.
- El cierre "La sección [N] presenta [COMPLETAR]" sin completar.
- Mendoza y Oviedo (2007): referencia incompleta en la bibliografía ("Economía" sin volumen ni páginas).
- Comín Comín (2014) termina sin punto.
- Dato "156,7% del PBI" (FMI 2024) convive con tu "94,5%" de deuda consolidada en la
  Introducción del .tex: son medidas distintas (bruta total vs. tu perímetro). Hay que aclararlo
  en una nota o el jurado lo va a señalar.
- Al fusionar con `02_estado_del_arte.tex` no duplicar Rodríguez (2023) ni Levy Yeyati (ya están
  como `levyyeyati2021`).

### 2.7 Citas a verificar antes de usar (no usar sin ver el paper)

| Cita | Problema |
|---|---|
| "Tesis UNCUYO (Páez et al., 2026)" | Es la propia tesis (autor de los docx: Santiago Hernán Páez Albornoz, según los metadatos). No se cita como antecedente: sacarla. |
| Garud (2023) en metodología vs. Garud (2025) en intro | Mismo autor con dos años. Es una tesis de maestría de Tokio: fuente débil para sostener la regla ADF+KPSS (citar Kwiatkowski et al., 1992, o Lütkepohl, 2005). |
| Adler & Sosa (2013); "Adler, Djigbenou & Sosa (FMI)" | No aparecen en su bibliografía. Verificar existencia y año. |
| Lanteri (2019), DT N° 84 del BCRA | Verificar número de documento. |
| Rezk et al. (2005) para X-13 | X-13 es de 2012; en 2005 existía X-12. Anacronismo. |
| Mountford & Uhlig (2009), Canova & Ferroni (2022), Ivanov & Kilian (2001) | Reales, pero solo si se usan esas técnicas. Si se descartan las restricciones de signo, sacar las dos primeras. |

## 3. Plan recomendado

1. **Reunión corta con tu compañero** para acordar tres cosas: (i) adoptar su pregunta, su
   pregunta específica FED y sus tres hipótesis con la reformulación de 2.3; (ii) el módulo de
   balanza de pagos queda afuera; (iii) identificación principal = tu SVAR restringido, Cholesky
   solo como robustez.
2. **Llevarle a Pablo** la nueva pregunta y las hipótesis antes de tocar código. Cambia el eje
   de la tesis (de "umbral/fatiga" a "shock externo + perímetro consolidado"), y él ya pidió
   cambios sobre H1b y endogeneidad: conviene que lo apruebe.
3. **Datos**: construir la deuda consolidada SPNF+BCRA 1996-2025 (ver 2.4) y recalcular alpha;
   bajar Fed Funds y tasa sombra Wu-Xia (FRED), trimestralizar 1996-2025.
4. **Código**: pasar el SVAR restringido a SVARX (exógenas: Δ tasa FED, VIX, opcional precios de
   commodities; dummies de Bai-Perron), IRF de la deuda al shock FED, y Monte Carlo en dos
   escenarios (base y shock FED), con y sin BCRA. Reportar las cuatro probabilidades.
5. **Texto**: Introducción con la pregunta/hipótesis nuevas; fusionar sus antecedentes nuevos y
   su área de vacancia en `02_estado_del_arte.tex`; reescribir Metodología con la Etapa del
   SVARX; Hansen/TVECM como resultado complementario de H1a.
6. **Antes de escribir conclusiones**: si la probabilidad con shock FED o con BCRA da algo que
   contradiga lo que ya dice la tesis, frenar y revisarlo juntos.
