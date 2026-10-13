# Seguimiento de tareas de la tesis (documento interno del grupo)

Documento de trabajo del grupo. Última actualización: 12 de octubre de 2026.

## 1. Para qué sirve este documento

Ordena qué está hecho, qué se decidió y qué falta, para que todos trabajemos sobre la misma base. Cada decisión tiene su justificación en el documento de decisiones finales (D1 a D14). Cada número viene de la hoja de números (`codigo/modelos/hoja_de_numeros.py`) o del Apéndice (`codigo/modelos/apendice_tablas.py`). Lo que todavía no está hecho aparece como pendiente.

## 2. Estado al 12 de octubre de 2026

- **Modelo rehecho** según las decisiones D1 a D12, después de la revisión adversarial del 11/10/2026.
- **Texto reescrito**: los capítulos, el Apéndice y los documentos del grupo (plan de labor, propuesta metodológica, guía de defensa y revisión crítica) usan los números nuevos.
- **Pendiente**: la validación del grupo, los informes del FGS y el control final de la extensión (sección 5).

### Scripts que generan los resultados

| Qué | Archivo |
|---|---|
| Propiedades de las series (ADF, KPSS, Zivot-Andrews, Bai-Perron, Johansen) | `codigo/modelos/fase24b_propiedades_series.py` |
| Estimación del SVARX, selección de rezagos, diagnósticos y *bootstrap* | `codigo/modelos/fase24_svarx_1996_2025.py` |
| Simulación de Monte Carlo con el escenario del FMI | `codigo/modelos/fase25_simulacion_dsa_svarx.py` |
| *Shocks* a la manera del FMI y su diagnóstico | `codigo/modelos/fase25b_diagnostico_abanico_fmi.py` |
| Hoja de números y tablas del Apéndice | `codigo/modelos/hoja_de_numeros.py`, `codigo/modelos/apendice_tablas.py` |
| Figuras | `codigo/modelos/figuras_tesis.py`, `codigo/modelos/fig_abanico_deuda.py` |

## 3. Decisiones tomadas

| N.° | Decisión | Justificación |
|---|---|---|
| D1 | Especificación principal: deuda bruta del gobierno federal, con el *stock* del FMI a fines de 2025 (80,3% del PIB) como punto de partida. Extensión: deuda consolidada con el BCRA (52,1% del PIB en la definición del FMI). | Es la única forma de comparar con la probabilidad del FMI con el mismo perímetro, punto de partida, escenario y métrica. |
| D2 | Datos desde 1999T1; muestra efectiva común 2000T3-2025T4 (102 trimestres). | Desde 1999 todas las series tienen fuente publicada y verificable (EMBI+ de la serie diaria de Ámbito Financiero). Todos los órdenes de rezago se comparan sobre la misma muestra (Lütkepohl, 2005, sec. 4.3). |
| D3 | Rezagos: Schwarz entre los órdenes estables y, si sus residuos están autocorrelacionados, el menor orden mayor que no lo esté. Resultado: 2 rezagos. | Ivanov y Kilian (2005) recomiendan Schwarz para datos trimestrales con menos de 120 observaciones; adecuación de residuos según Lütkepohl (2005, sec. 4.4). |
| D4 | Resultado primario con rentas de la propiedad para la deuda federal y sin rentas para la consolidada. | Coherencia con cada perímetro; con rentas es la definición del FMI para el gobierno federal. |
| D5 | Tasa de la FED con la tasa sombra de Wu y Xia (2016) en el límite cero; en 2022T1 la variación se calcula con la tasa efectiva. | No confundir el cambio de serie con un cambio de política. |
| D6 | VIX y nivel de la tasa de la FED simulados con procesos AR(1). | La incertidumbre externa forma parte del abanico. |
| D7 | Remuestreo de *shocks* en bloques de ocho trimestres. | Como los bloques de dos años del abanico del FMI (FMI, 2021, anexo VI). |
| D8 | Estimación central con MCO; intervalos con *bootstrap* de bloques y percentiles de Hall; números aleatorios comunes; Kilian (1998) como robustez. | Brüggemann et al. (2016); Hall (1992). |
| D9 | Ajuste *stock*-flujo e inflación relativa escalados por moneda; métrica con el ajuste *stock*-flujo; proporción en pesos fija; retroalimentación anual. | Definición del FMI (2021, párr. 53 y anexo VI). |
| D10 | H1a con su criterio original; la suficiencia como complemento descriptivo. | Se elimina el cambio de criterio de la versión anterior. |
| D11 | H1b con el mismo perímetro, punto de partida, escenario, horizonte y métrica del FMI; Bonferroni por los dos horizontes. | Comparación de lo mismo con lo mismo. |
| D12 | H2 contrastada en 2035; 2031 se informa. | El efecto de una tasa más alta se acumula. |
| D13 | Título: "Probabilidad de no estabilización de la deuda pública argentina, 2026-2035: un modelo SVARX con determinantes macroeconómicos y política monetaria de Estados Unidos". | El título anterior prometía más de lo que se mide. |
| D14 | Tabla completa de robustez al Apéndice (A.8); ejes 2, 3 y 8 de Antecedentes reducidos. | Extensión. |

Las decisiones anteriores al 12/10 que siguen vigentes: la Introducción del 7/10 como base; el umbral de 100% del PIB fuera de las hipótesis; el canal cuasifiscal de la FED redactado en pasado; el módulo de balanza de pagos como línea futura; todo umbral, corte o tamaño de *shock* con justificación escrita; la identificación de Blanchard y Perotti como principal y Cholesky como robustez.

## 4. Etapas

Estado: **hecho**, **en curso** o **pendiente**.

### Etapa 1. Introducción y Antecedentes (hecha)

- Introducción reescrita con el perímetro de D1 y los criterios de D10 a D12. Antecedentes con los ejes 2, 3 y 8 reducidos (D14).

### Etapa 2. Datos (hecha)

- Series desde 1999T1 con fuentes publicadas (MECON, BCRA, INDEC, FRED, Ámbito Financiero para el EMBI+). Deuda federal bruta y deuda consolidada con el BCRA. Resultado primario por perímetro (D4).

### Etapa 3. Metodología y estimación (hecha)

- SVARX con 2 rezagos sobre 2000T3-2025T4, autovalor máximo 0,849. Reacción fiscal de impacto 0,0495 [0,0099; 0,0799] y de largo plazo 0,167 [0,057; 0,296]. Residuos sin autocorrelación (Portmanteau p = 0,296).

### Etapa 4. Simulación y contrastes (hecha)

- H1a respaldada con su criterio original: 82,6 puntos [65,8; 92,4], en las 19 especificaciones.
- H1b respaldada: 32,8% [26,8; 37,9] en 2031 y 31,3% [27,0; 35,3] en 2035, contra 1% y menos de 3% del FMI, en las 19 especificaciones.
- H2 respaldada en su efecto sobre la probabilidad (senda 2022-2025: +11,3 puntos en 2035 [4,4; 17,9]), no en su mecanismo.

### Etapa 5. Redacción (hecha)

- Capítulos, Apéndice y documentos del grupo reescritos con los números nuevos.

### Etapa 6. Validación y entrega (en curso)

- Validación del grupo y del director, control de extensión y pasaje al formato final.

## 5. Qué falta (actualizado el 12/10/2026)

### 5.1 Validación del grupo

| Qué | Estado |
|---|---|
| D1: deuda federal bruta como especificación principal y consolidada como extensión | Pendiente |
| D2: datos desde 1999 | Pendiente |
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
- Hall, P. (1992). *The bootstrap and Edgeworth expansion*. Springer. https://doi.org/10.1007/978-1-4612-4384-7
- Ivanov, V., y Kilian, L. (2005). A practitioner's guide to lag order selection for VAR impulse response analysis. *Studies in Nonlinear Dynamics and Econometrics*, *9*(1), artículo 2. https://doi.org/10.2202/1558-3708.1219
- Kilian, L. (1998). Small-sample confidence intervals for impulse response functions. *Review of Economics and Statistics*, *80*(2), 218-230. https://doi.org/10.1162/003465398557465
- Lütkepohl, H. (2005). *New introduction to multiple time series analysis*. Springer.
- Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking*, *48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300
