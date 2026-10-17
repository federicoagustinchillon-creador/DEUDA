# Seguimiento de tareas de la tesis (documento interno del grupo)

Documento de trabajo del grupo. Última actualización: 17 de octubre de 2026.

## 1. Para qué sirve este documento

Ordena qué está hecho, qué se decidió y qué falta, para que todos trabajemos sobre la misma base. Cada decisión tiene su justificación en el documento de decisiones finales (D1 a D14). Cada número viene de la hoja de números (`codigo/modelos/hoja_de_numeros.py`) o del Apéndice (`codigo/modelos/apendice_tablas.py`). Lo que todavía no está hecho aparece como pendiente.

## 2. Estado al 17 de octubre de 2026

- **Modelo rehecho** según las decisiones D1 a D12, después de la revisión adversarial del 11/10/2026, y **reestimado** el 17/10/2026 con la ventana única 1996-2025 (D2), con los empalmes del EMBI de 1996T1-1998T3 y del TCRM de 1996 validados en el Apéndice A.2.
- **Revisión de un compañero** (inconsistencias de período, nombre del EMBI, nombre de la identificación, números viejos y *commits* que no se veían en la rama por defecto): resuelta con las reglas D2 y D2b, el control automático `tesis_oficial_borradores/verificar_consistencia.py` y la fusión de la rama de trabajo con `main` (Revisión crítica, sección 5).
- **Error propio en el resultado primario** (detectado en la lectura final): la justificación de la serie con rentas como definición del FMI era falsa, porque el FMI excluye las utilidades del BCRA. Se pasó a una definición única sin rentas de la propiedad (D4) y el modelo se volvió a correr; los resultados casi no cambian (Revisión crítica, sección 6).
- **Texto**: los capítulos y el Apéndice se actualizan con los números nuevos; los documentos del grupo (plan de labor, propuesta metodológica, guía de defensa, revisión crítica y este seguimiento) ya están actualizados.
- **Pendiente**: la validación del grupo de D1 y D13, los informes del FGS y el control final de la extensión (sección 5).

### Scripts que generan los resultados

| Qué | Archivo |
|---|---|
| Propiedades de las series (ADF, KPSS, Zivot-Andrews, Bai-Perron, Johansen) | `codigo/modelos/fase24b_propiedades_series.py` |
| Estimación del SVARX, selección de rezagos, diagnósticos y *bootstrap* | `codigo/modelos/fase24_svarx_1996_2025.py` |
| Simulación de Monte Carlo con el escenario del FMI | `codigo/modelos/fase25_simulacion_dsa_svarx.py` |
| *Shocks* a la manera del FMI y su diagnóstico | `codigo/modelos/fase25b_diagnostico_abanico_fmi.py` |
| Empalmes del EMBI (1996T1-1998T3) y del TCRM (1996) | `codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py` |
| Hoja de números y tablas del Apéndice | `codigo/modelos/hoja_de_numeros.py`, `codigo/modelos/apendice_tablas.py` |
| Control de consistencia del texto (período, EMBI, identificación, números) | `tesis_oficial_borradores/verificar_consistencia.py` |
| Figuras | `codigo/modelos/figuras_tesis.py`, `codigo/modelos/fig_abanico_deuda.py` |

## 3. Decisiones tomadas

| N.° | Decisión | Justificación |
|---|---|---|
| D1 | Especificación principal: deuda federal bruta, con el *stock* del FMI a fines de 2025 (80,3% del PIB) como punto de partida. Extensión: deuda consolidada con el BCRA (52,1% del PIB en la definición del FMI). | Es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, punto de partida, escenario y métrica. |
| D2 | Ventana única 1996-2025 y proyección 2026-2035; ecuaciones estimadas con 1998T2-2025T4 (111 trimestres). EMBI de 1996T1-1998T3 empalmado con la tasa interfinanciera en dólares del BCRA menos la tasa de fondos federales; TCRM de 1996 encadenado con el BIS. | Decisión del grupo. Los primeros trimestres son condiciones iniciales de los rezagos (Lütkepohl, 2005, sec. 4.3). El empalme del EMBI se valida en la superposición 1998T4-2001T3 (R² = 0,89) y con datos desde 1999 el resultado casi no cambia (32,4% contra 31,8% en 2031). |
| D2b | Reglas de consistencia: un solo período, un solo nombre para el EMBI, el TCRM, la deuda, la FED y la identificación. | Revisión de un compañero; lo verifica `verificar_consistencia.py`. |
| D3 | Rezagos: Schwarz entre los órdenes estables y, si sus residuos están autocorrelacionados, el menor orden mayor que no lo esté. Resultado: 2 rezagos. | Ivanov y Kilian (2005) recomiendan Schwarz para datos trimestrales con menos de 120 observaciones; adecuación de residuos según Lütkepohl (2005, sec. 4.4). |
| D4 | Una sola definición del resultado primario: Sector Público Nacional sin rentas de la propiedad. Con rentas, como robustez. | El FMI excluye de su resultado primario las transferencias de utilidades del BCRA (FMI, 2026, cuadro 1, nota 4) y el MECON no las separa del resto de las rentas de la propiedad. En el perímetro consolidado esas utilidades también son un flujo interno. |
| D5 | Tasa de la FED con la tasa sombra de Wu y Xia (2016) en el límite cero; en 2022T1 la variación se calcula con la tasa efectiva. | No confundir el cambio de serie con un cambio de política. |
| D6 | VIX y nivel de la tasa de la FED simulados con procesos AR(1). | La incertidumbre externa forma parte del abanico. |
| D7 | Remuestreo de *shocks* en bloques de ocho trimestres. | Como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI). |
| D8 | Estimación central con MCO; intervalos con *bootstrap* de bloques y percentiles de Hall; números aleatorios comunes; Kilian (1998) como robustez. | Brüggemann et al. (2016); Hall (1992). |
| D9 | Ajuste *stock*-flujo e inflación relativa escalados por moneda; métrica con el ajuste *stock*-flujo; proporción en pesos fija; retroalimentación anual. | Definición del FMI (2021, párr. 53 y anexo VI). |
| D10 | H1a con su criterio original; la suficiencia como complemento descriptivo. | Se elimina el cambio de criterio de la versión anterior. |
| D11 | H1b con el mismo perímetro, punto de partida, escenario, horizonte y métrica del FMI; Bonferroni por los dos horizontes. | Comparación de lo mismo con lo mismo. |
| D12 | H2 contrastada en 2035; 2031 se informa. | El efecto de una tasa más alta se acumula. |
| D13 | Título: "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos". | El título anterior prometía más de lo que se mide. |
| D14 | Tabla completa de robustez al Apéndice (A.9); ejes 2, 3 y 8 de Antecedentes reducidos. | Extensión. |

Las decisiones anteriores al 12/10 que siguen vigentes: la Introducción del 7/10 como base; el umbral de 100% del PIB fuera de las hipótesis; el canal cuasifiscal de la FED redactado en pasado; el módulo de balanza de pagos como línea futura; todo umbral, corte o tamaño de *shock* con justificación escrita; la identificación principal con restricciones de impacto en la línea de Blanchard y Perotti (2002) para el bloque fiscal y de actividad, con un bloque cambiario y de riesgo (EMBI y TCRM) identificado en conjunto, y dos ordenamientos de Cholesky (resultado primario primero y resultado primario último) como robustez.

## 4. Etapas

Estado: **hecho**, **en curso** o **pendiente**.

### Etapa 1. Introducción y Antecedentes (hecha)

- Introducción reescrita con el perímetro de D1 y los criterios de D10 a D12. Antecedentes con los ejes 2, 3 y 8 reducidos (D14).

### Etapa 2. Datos (hecha)

- Series de 1996-2025 con fuentes publicadas (MECON, BCRA, INDEC, FRED, BIS y Ámbito Financiero para el EMBI), con los empalmes del EMBI de 1996T1-1998T3 y del TCRM de 1996. Se eliminaron los valores del EMBI de 1993-1998 escritos a mano de la base anterior. Deuda federal bruta y deuda consolidada con el BCRA. Resultado primario sin rentas de la propiedad para los dos perímetros (D4).

### Etapa 3. Metodología y estimación (hecha)

- SVARX con 2 rezagos, ecuaciones estimadas con 1998T2-2025T4, autovalor máximo 0,896. Reacción fiscal de impacto 0,0576 [0,0220; 0,0822] y de largo plazo 0,199 [0,112; 0,328]. Residuos sin autocorrelación (Portmanteau p = 0,056).

### Etapa 4. Simulación y contrastes (hecha)

- H1a respaldada con su criterio original: 78,3 puntos [57,3; 87,9], en las 20 especificaciones. Complemento descriptivo: con el resultado primario en su máximo de 1996-2025 (3,29% del PIB) todos los años, la probabilidad en 2031 es 26,1%; llevarla al 1% exige sumar 8,00 puntos al resultado primario del escenario.
- H1b respaldada: 31,8% [25,2; 36,4] en 2031 y 31,0% [26,8; 35,6] en 2035, contra 1% y menos de 3% del FMI, en las 20 especificaciones.
- H2 respaldada en el efecto de la senda 2022-2025 sobre la probabilidad (+9,7 puntos en 2035 [4,2; 16,0]), que es robusto. El efecto sobre la deuda (+9,0 [0,3; 16,2]) y el del desvío estándar sobre la probabilidad (+1,1 [0,2; 1,9]) no resisten Bonferroni. El 96% del efecto sobre la deuda es el costo directo de la deuda en dólares.
- Variante sin empalme (datos desde 1999): 32,4% [26,6; 37,0] en 2031; H1a y H2 no cambian.
- *Shocks* a la manera del FMI sobre la deuda federal bruta: 24,1% en 2031, con un ancho del abanico de 148,4.

### Etapa 5. Redacción (en curso)

- Documentos del grupo actualizados con la ventana 1996-2025 y los números nuevos (17/10/2026). Capítulos y Apéndice en actualización; el control `verificar_consistencia.py` tiene que terminar sin problemas antes de cerrar.

### Etapa 6. Validación y entrega (en curso)

- Validación del grupo y del director, control de extensión y pasaje al formato final.

## 5. Qué falta (actualizado el 17/10/2026)

### 5.1 Validación del grupo

| Qué | Estado |
|---|---|
| D1: deuda federal bruta como especificación principal y consolidada como extensión | Pendiente |
| D2: ventana 1996-2025 | Decidida por el grupo |
| D13: título nuevo | Pendiente |

### 5.2 Informes del FGS

| Qué | Por qué importa | Cómo se resuelve | Estado |
|---|---|---|---|
| Títulos públicos en cartera del FGS (ANSES), 2008-2025 | La serie histórica de deuda consolidada no descuenta la deuda del Tesoro en manos del FGS. La especificación principal no se ve afectada, y la simulación de la extensión parte del *stock* del FMI, que sí lo descuenta. | ANSES bloquea la descarga automática (protección anti-bots); hay que bajar los PDF a mano desde el navegador y guardarlos en `datos/crudos/fgs/`. Archivos: Informe Estadístico Mensual de enero de 2026 (https://www.anses.gob.ar/sites/default/files/archivo/2026-03/IEM-FGS-2026-01.pdf), Anuario 2024 (https://www.anses.gob.ar/sites/default/files/inline-files/Anuario%202024.pdf), Consejo del FGS de diciembre de 2025 (https://www.anses.gob.ar/sites/default/files/archivo/2026-02/Consejo%20FGS-Diciembre-2025.pdf) y, para años anteriores, los anuarios e informes de la página del FGS (https://www.anses.gob.ar/fgs-fondo-de-garantia-de-sustentabilidad). De cada uno se toma la fila "Títulos Públicos Nacionales" al cierre de cada año o trimestre. El script `codigo/ingesta_datos/construir_tenencias_fgs.py` ya está listo para leerlos. | Pendiente: bajar a mano |
| Deuda en manos de Agencias del Sector Público (Secretaría de Finanzas) | Dato descriptivo de la deuda intra sector público. No se usa para restar, porque incluye otras entidades y duplicaría parte de lo que ya se consolida. | Está en `datos/procesados/tenencias_fgs_1996_2025.csv`, con los PDF de Finanzas en `datos/crudos/fgs/`. | Hecho |

### 5.3 Control final de extensión

- Contar las páginas del texto reescrito. Si supera unas 60, acordar en el grupo qué se recorta. La tabla completa de robustez ya pasó al Apéndice y los ejes 2, 3 y 8 de Antecedentes ya se redujeron (D14).

### 5.4 Registro de verificaciones de citas (sin cambios desde el 11/10)

| Qué | Estado |
|---|---|
| Braun y Joy (1968), restricción externa | No hay copia abierta (Oxford y JSTOR). Si alguien tiene acceso por la facultad, se verifica contra el original. |
| Adler, Djigbenou y Sosa (2016) | Verificada sobre el documento de trabajo del FMI (WP/14/60), no sobre la versión de la revista. |
| Brüggemann, Jentsch y Trenkler (2016) y Hall (1992) | Se agregan a las referencias por D8. |
| Las otras citas del marco teórico | Verificadas contra el texto completo, con página (ver `verificacion_citas_marco.md`). |

## Referencias de este documento

- Brüggemann, R., Jentsch, C., y Trenkler, C. (2016). Inference in VARs with conditional heteroskedasticity of unknown form. *Journal of Econometrics*, *191*(1), 69-85. https://doi.org/10.1016/j.jeconom.2015.10.004
- Fondo Monetario Internacional [FMI]. (2021). *Review of the debt sustainability framework for market access countries* (IMF Policy Paper).
- Fondo Monetario Internacional [FMI]. (2026). *Argentina: 2026 Article IV consultation, second review under the extended arrangement under the Extended Fund Facility* (IMF Country Report No. 26/105).
- Hall, P. (1992). *The bootstrap and Edgeworth expansion*. Springer. https://doi.org/10.1007/978-1-4612-4384-7
- Ivanov, V., y Kilian, L. (2005). A practitioner's guide to lag order selection for VAR impulse response analysis. *Studies in Nonlinear Dynamics and Econometrics*, *9*(1), artículo 2. https://doi.org/10.2202/1558-3708.1219
- Kilian, L. (1998). Small-sample confidence intervals for impulse response functions. *Review of Economics and Statistics*, *80*(2), 218-230. https://doi.org/10.1162/003465398557465
- Lütkepohl, H. (2005). *New introduction to multiple time series analysis*. Springer.
- Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking*, *48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300
