# Probabilidad de no estabilización de la deuda pública argentina, 2026-2035

Un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos.

Tesis Final de Grado, Facultad de Ciencias Económicas, Universidad Nacional de Cuyo (Mendoza, 2026).
Autores: Santiago Páez, Federico Chillón y Emiliano Carricondo. Director: Pablo Mahnic.

[![Licencia](https://img.shields.io/badge/Licencia-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)

## 0. Qué mirar primero

| Si querés... | Andá a |
|---|---|
| Leer la tesis | [`tesis/Tesis.pdf`](tesis/Tesis.pdf) |
| Comentar el texto en Word | [`tesis_oficial_borradores/para_el_grupo/Tesis_borrador.docx`](tesis_oficial_borradores/para_el_grupo/Tesis_borrador.docx) |
| Editar un capítulo | [`tesis_oficial_borradores/`](tesis_oficial_borradores/): un `.md` por capítulo (`resumen`, `introduccion`, `antecedentes`, `marco_teorico`, `metodologia`, `datos`, `resultados`, `discusion`, `conclusiones`, `apendice`). El LaTeX de `tesis/capitulos/` se genera desde ahí, no se edita a mano |
| Saber de dónde sale un número | [`tesis_oficial_borradores/_hoja_de_numeros.md`](tesis_oficial_borradores/_hoja_de_numeros.md), generada por `codigo/modelos/hoja_de_numeros.py` a partir de `resultados/tablas/` |
| Ver qué se decidió y por qué | [`tesis_oficial_borradores/_decisiones_finales.md`](tesis_oficial_borradores/_decisiones_finales.md) (decisiones D1 a D16) y [`revision_critica.md`](tesis_oficial_borradores/revision_critica.md) |
| Replicar las cifras | [`codigo/GUIA_DE_EJECUCION.md`](codigo/GUIA_DE_EJECUCION.md) |
| Documentos para el grupo y el director | [`tesis_oficial_borradores/para_el_grupo/`](tesis_oficial_borradores/para_el_grupo/): plan de labor, propuesta metodológica, guía de defensa, revisión crítica, seguimiento de tareas y Excel de datos y resultados |

**Ramas.** El trabajo del grupo avanza por ramas y *pull requests*. La versión más reciente está en `revision-final-19-10`; `main` queda en la versión del 17 de octubre de 2026 hasta que el grupo fusione la revisión final. Las ramas `revision-var-vecm` y `var-restringido` guardan versiones anteriores del modelo (VECM y DOLS sobre 2004-2025) que ya no intervienen en la tesis.

## 1. Pregunta y diseño

La tesis estima la probabilidad de que la deuda pública argentina no se estabilice en 2026-2035 y qué parte de esa incertidumbre explican el crecimiento, el tipo de cambio real, el riesgo país, el resultado primario y la tasa de la Reserva Federal (FED).

- **Datos.** Trimestrales, ventana 1996-2025. Las ecuaciones se estiman con 1998T2-2025T4 (111 trimestres), porque los primeros trimestres son condiciones iniciales de los rezagos. El EMBI de 1996T1-1998T3 se empalma con la tasa interbancaria en dólares del BCRA menos la tasa de fondos federales, y el TCRM de 1996 con el tipo de cambio real efectivo del BIS; la validación de ambos empalmes está en el Apéndice A.2 y la figura A.1.
- **Modelo.** SVARX con cuatro variables endógenas: resultado primario del Sector Público Nacional sin rentas de la propiedad, crecimiento real, riesgo país (diferencial del índice EMBI de J.P. Morgan para Argentina) y tipo de cambio real multilateral (TCRM). Exógenas: variación de la tasa de la FED (tasa sombra de Wu y Xia en el límite cero), VIX, estacionales, binarias por mandato presidencial, quiebres de Bai y Perron dentro de cada mandato y la deuda rezagada, que retroalimenta el sistema.
- **Identificación.** Restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con el bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto. Dos ordenamientos de Cholesky se informan como robustez.
- **Simulación.** La deuda federal bruta, el perímetro del análisis de sostenibilidad del FMI, se simula alrededor del escenario base del FMI (Informe de País 26/105, mayo de 2026) desde su mismo punto de partida, 80,3% del PIB a fines de 2025. Los intervalos de 90% salen de 1.000 réplicas de un *bootstrap* de bloques móviles con percentiles de Hall. La deuda consolidada con el BCRA, estimada desde 2002, es una extensión.
- **Métrica de no estabilización.** La definición operativa del FMI decide las hipótesis; una métrica anual, que suma la valuación de la deuda en moneda extranjera de cada año, se informa como complemento (decisión D16).
- **Robustez.** 21 especificaciones: rezagos, elasticidades, ordenamientos de Cholesky, sin binarias presidenciales, sin quiebres, sin retroalimentación, datos desde 1999 y desde 2004, corrección de sesgo de Kilian, canal de tasas en pesos y deuda consolidada, entre otras.

## 2. Resultados principales

Cifras de la especificación principal, con intervalos de 90% entre corchetes. Fuente: [`_hoja_de_numeros.md`](tesis_oficial_borradores/_hoja_de_numeros.md).

| Medida | 2031 | 2035 |
|---|---|---|
| Probabilidad de no estabilización, definición operativa del FMI | 3,1% [0,0; 6,3] | 5,1% [0,0; 10,2] |
| Probabilidad de no estabilización, métrica anual (complemento) | 27,7% [20,6; 34,7] | 29,0% [25,0; 36,1] |
| Cifra del FMI | cerca de 1% | menos de 3% |

- **H1b** (la probabilidad supera la del FMI): no respaldada con la definición del FMI; los intervalos incluyen las cifras del organismo.
- **H1a** (los *shocks* no fiscales dominan la incertidumbre): su contribución a la varianza de la deuda de 2035 supera a la del *shock* fiscal en 96,8 puntos [90,8; 99,8]; la condición de suficiencia del superávit no se cumple con la definición del FMI, de modo que H1a queda no respaldada.
- **H2** (la tasa de la FED eleva el riesgo): repetir en 2026-2029 la senda de 2022-2025 eleva la probabilidad de 2035 en 17,1 puntos [0,6; 32,6] con la definición del FMI y en 18,4 con la métrica anual. Parcialmente respaldada: el efecto sobre la deuda esperada incluye el cero, y el 77% del aumento de la deuda es el costo directo de la deuda en dólares.

## 3. Estructura del repositorio

```text
Deuda/
├── tesis/
│   ├── Tesis.pdf                  # PDF oficial de la tesis
│   ├── capitulos/                 # LaTeX por capítulo, generado desde tesis_oficial_borradores/
│   ├── figuras/                   # figuras del texto
│   └── fuente/                    # Tesis.tex y referencias
├── tesis_oficial_borradores/      # texto fuente (.md), hoja de números, decisiones y documentos del grupo
│   └── para_el_grupo/             # Word y Excel para el grupo y el director
├── codigo/
│   ├── ingesta_datos/             # construcción de las series 1996-2025 y empalmes
│   ├── modelos/                   # fase24 (estimación), fase25 (simulación), figuras, apéndice, hoja de números
│   └── GUIA_DE_EJECUCION.md       # cómo replicar las cifras
├── datos/
│   ├── dataset_consolidado_1996_2025.csv   # base trimestral del modelo
│   ├── procesados/                # deuda, resultado primario, tasa de la FED, escenario del FMI, empalmes
│   ├── crudos/                    # descargas originales
│   └── codebook.md                # definición de cada variable
├── resultados/tablas/             # salidas CSV de fase24 y fase25 por especificación
├── tests/                         # pruebas automáticas (pytest)
├── Bibliografia/                  # papers citados, marco legal, auditorías de citas
└── historial_proyecto/            # versiones y planes anteriores; no es la especificación vigente
```

Los *scripts* de `codigo/modelos/` con números de fase menores que 24 corresponden a versiones anteriores y no intervienen en las cifras de la tesis. `_material_cursada_NO_es_parte_de_la_tesis/` es material de la cursada.

## 4. Cómo replicar

```bash
pip install -r codigo/requirements.txt
bash codigo/modelos/correr_todo.sh
```

`correr_todo.sh` reestima el modelo y todas las variantes de robustez, genera figuras, Apéndice, hoja de números y Excel, y corre las pruebas. Las semillas son fijas, de modo que las cifras se reproducen exactamente. Los pasos por separado y los parámetros están en [`codigo/GUIA_DE_EJECUCION.md`](codigo/GUIA_DE_EJECUCION.md).

Para regenerar el texto y verificarlo:

```bash
python tesis_oficial_borradores/generar_latex.py --compilar
python tesis_oficial_borradores/verificar_consistencia.py
python tesis_oficial_borradores/generar_docx_grupo.py
```

`verificar_consistencia.py` controla que el texto use un solo período, un solo nombre para cada variable y la identificación, y que cada número citado figure en la hoja de números.

## 5. Datos

La base del modelo es [`datos/dataset_consolidado_1996_2025.csv`](datos/dataset_consolidado_1996_2025.csv). Las columnas `EMBI_fuente` y `TCRM_fuente` indican el origen de cada trimestre, y `es_interpolado`, `es_empalme_pib`, `es_empalme_embi` y `es_interpolado_tcrm` marcan los valores reconstruidos. Fuentes: Secretaría de Finanzas y Secretaría de Hacienda (MECON), INDEC, BCRA, J.P. Morgan (vía Ámbito Financiero), BIS, Reserva Federal, Wu y Xia (2016), CBOE y FMI. Definiciones completas en [`datos/codebook.md`](datos/codebook.md).

## 6. Citación

```bibtex
@thesis{paez_chillon_carricondo_2026,
  author  = {P{\'a}ez, Santiago and Chill{\'o}n, Federico and Carricondo, Emiliano},
  title   = {Probabilidad de no estabilizaci{\'o}n de la deuda p{\'u}blica argentina, 2026-2035: un modelo SVARX con determinantes macroecon{\'o}micos y pol{\'i}tica monetaria de Estados Unidos},
  school  = {Facultad de Ciencias Econ{\'o}micas, Universidad Nacional de Cuyo},
  year    = {2026},
  type    = {Tesis Final de Grado},
  address = {Mendoza, Argentina}
}
```

## Licencia

Creative Commons Atribución 4.0 Internacional ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es)).
