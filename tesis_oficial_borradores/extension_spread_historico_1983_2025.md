# Extensión de frontera: spread soberano 1983-2025 (42 años de democracia)

Este archivo es un documento de trabajo interno. No es parte de la tesis oficial y no se
pega en ningún capítulo. Se saca del cuerpo principal a pedido del usuario (2026-09-18):
"por ahora no la necesitamos, no la elimines pero sacala de la tesis". Queda documentado
acá en texto completo, listo para reincorporar si hace falta.

Vivió en `tesis/capitulos/06_resultados.tex`, sección `Extensión de Frontera: Reconstrucción
del Spread Soberano en 42 Años de Democracia (1983--2025)` (label `sec:spread_historico_1983_2025`),
justo antes de la "Síntesis de la Evidencia Empírica". Referenciada también desde la fila
"Extensión: Spread Histórico (1983--2025)" de la tabla `tab:mapa_consistencia` en
`08_conclusiones.tex` (esa fila se sacó de la tabla al mismo tiempo que esta sección).

**Nota técnica importante para una futura reincorporación**: la metodología de empalme del
EMBI+ para la ventana central 1996--2025 (Sección `sec:empalme` de `04_metodologia.tex`)
originalmente decía "no hace falta un empalme nuevo, el de esta sección ya cubre
1996--2025" y remitía a esta extensión para la construcción real de la serie. Al sacar esta
sección, `04_metodologia.tex` se reescribió para describir esa corrección de empalme
(el `k` de corrección proporcional de sesgo, $0.8710$) de forma autocontenida, sin depender
de este archivo. Si se reincorpora esta sección a la tesis, revisar que no quede duplicada
esa explicación.

---

## Extensión de Frontera: Reconstrucción del Spread Soberano en 42 Años de Democracia (1983-2025)

Para evaluar si la dinámica de riesgo crediticio soberano y los umbrales de fatiga fiscal
constituyen fenómenos circunscritos a las últimas dos décadas o si representan regularidades
empíricas invariantes de la economía política argentina, se procedió a reconstruir y empalmar
una serie trimestral homogénea de costo de financiamiento soberano a lo largo de los 42 años
de democracia ininterrumpida (1983T4-2025T4, n = 169 trimestres).

### Metodología de Reconstrucción por Eras Financieras

Ante la inexistencia del índice EMBI con anterioridad a 1993, la serie histórica se estructuró
a partir de los activos soberanos en moneda extranjera que fijaron el costo marginal de
endeudamiento en cada subperíodo:

1. **Era Bonex (1983T4-1992T4)**: Se utilizaron los rendimientos secundarios en dólares de los
   Bonos Externos de la República Argentina (Series 1982, 1984, 1987 y 1989) cotizados en el
   Mercado Abierto Electrónico y la Bolsa de Comercio de Buenos Aires, deduciendo la tasa del
   Bono del Tesoro de EE.UU. a 10 años (Spread_t = TIR_Bonex,t - r_US,10Y,t), conforme a la
   metodología canónica de Neumeyer y Perri (2005) y Kehoe et al. (2021).
2. **Era Brady (1993T1-1997T4)**: Se adoptó el JP Morgan EMBI Argentina *Stripped Spread* sobre
   bonos Brady Par, Discount y FRB (Uribe y Yue, 2006), descontando el valor presente de los
   bonos cupón cero del Tesoro estadounidense que colateralizaban el capital.
3. **Era EMBI+ y Global (1998T1-2025T4)**: Se integró la serie diaria oficial de JP Morgan EMBI+
   y EMBI Global Diversified Argentina.

Para evitar discontinuidades espurias en los puntos de unión, se aplicó una corrección
proporcional de sesgo en solapamiento (*Overlap Bias Correction*), vinculando la escala hacia
el benchmark moderno del EMBI+:

```
k1 = EMBI_Brady,1993T1(media) / Spread_Bonex,1992T4(media) = 850.0 / 760.0 = 1.1184
k2 = EMBI+_1998T1(media) / EMBI_Brady,1997T4(media) = 540.0 / 620.0 = 0.8710
```

Figura: Evolución Histórica del Spread Soberano Argentino en 42 Años de Democracia (1983-2025)
(`tesis/figuras/figura_spread_historico_1983_2025.png`).

### Quiebres Estructurales Múltiples de Bai-Perron en el Ciclo Histórico

La aplicación del algoritmo de programación dinámica de Bai y Perron (2003) sobre los 169
trimestres de democracia identifica cinco quiebres mayores y seis regímenes de financiamiento
soberano con diferencias de media altamente significativas.

| Régimen | Fecha Inicio | Fecha Fin | Trimestres | Media (pb) | Desvío (pb) | Hito Histórico / Ruptura |
|---|---|---|---|---|---|---|
| Régimen 1 | 1983T4 | 1988T4 | 21 | 797.84 | 359.44 | Transición democrática y colapso del Plan Austral |
| Régimen 2 | 1989T1 | 1990T4 | 8 | 3573.76 | 1255.84 | Hiperinflaciones de 1989/1990 y Plan Bonex |
| Régimen 3 | 1991T1 | 2001T4 | 44 | 831.66 | 427.31 | Ley de Convertibilidad y Plan Brady |
| Régimen 4 | 2002T1 | 2005T2 | 14 | 5431.33 | 638.09 | Default de la deuda externa y crisis de 2001-2002 |
| Régimen 5 | 2005T3 | 2019T2 | 56 | 683.54 | 326.60 | Canjes 2005/2010, superávits gemelos y desendeudamiento |
| Régimen 6 | 2019T3 | 2025T4 | 26 | 1732.05 | 632.45 | Shock PASO 2019, Canje 2020 y estabilización post-2023 |

Fuente: `resultados/tablas/fase22_bai_perron_1983_2025.csv`. Estimación por minimización de
pérdida L2 mediante programación dinámica sobre 169 observaciones trimestrales.

### Calibración del Proceso CIR y Métricas por Régimen Presidencial

La calibración por Máxima Verosimilitud exacta del proceso CIR a lo largo de las cuatro
décadas demuestra que la velocidad de reversión a la media de largo plazo es kappa = 0.4630
(vida media de 1.50 años), con un nivel incondicional de equilibrio de theta = 1456.98 pb. La
condición de Feller se satisface de forma holgada (2*kappa*theta = 1349.08 > sigma^2 = 613.96,
ratio = 2.1974 > 1.0), ratificando la robustez del modelado en tiempo continuo.

| Parámetro / Métrica | Valor Estimado (42 Años, n=169) | Interpretación Económica |
|---|---|---|
| Velocidad de Reversión (kappa) | 0.4630 | Reversión media hacia equilibrio |
| Nivel Incondicional (theta) | 1456.98 pb | Costo medio estructural de endeudamiento |
| Volatilidad de Difusión (sigma) | 24.7781 | Dispersión de innovaciones estocásticas |
| Vida Media de Reversión (t_1/2) | 1.50 años (18 meses) | Duración típica de los ciclos de spread |
| Condición de Feller (2*kappa*theta > sigma^2) | 1349.08 > 613.96, cumple | No negatividad estricta garantizada |
| Ratio de Feller (2*kappa*theta / sigma^2) | 2.1974 > 1.0 | Frontera en cero inaccesible (P=1) |
| Criterio AIC (CIR vs. AR(1)) | 2466.56 < 2612.53 | Delta AIC = -145.97, prefiere CIR |

Fuente: `resultados/tablas/fase22_cir_calibracion_1983_2025.csv`. Estimación exacta sobre la
función de densidad Chi-cuadrado no central.

**Dinámica del Spread Soberano por Régimen Presidencial (1983-2025)**

| Administración Presidencial | Período | Trimestres | Media (pb) | Mediana (pb) | Mínimo (pb) | Máximo (pb) |
|---|---|---|---|---|---|---|
| Raúl Alfonsín | 1983T4-1989T2 | 23 | 1035.52 | 701.36 | 409.13 | 4675.72 |
| Carlos Menem I | 1989T3-1995T1 | 23 | 1577.73 | 837.73 | 566.13 | 5455.01 |
| Carlos Menem II | 1995T2-1999T3 | 18 | 688.63 | 663.90 | 357.10 | 1350.00 |
| Fernando de la Rúa | 1999T4-2001T3 | 8 | 811.26 | 710.21 | 550.92 | 1468.94 |
| A. Rodríguez Saá / E. Duhalde | 2001T4-2003T1 | 6 | 5354.62 | 5873.34 | 2947.64 | 6658.98 |
| Néstor Kirchner | 2003T2-2007T3 | 18 | 2775.65 | 2644.15 | 210.22 | 5800.85 |
| Cristina Fernández de Kirchner | 2007T4-2015T3 | 32 | 853.48 | 734.62 | 387.78 | 1696.86 |
| Mauricio Macri | 2015T4-2019T3 | 16 | 584.87 | 477.95 | 360.23 | 1493.83 |
| Alberto Fernández | 2019T4-2023T3 | 16 | 2048.85 | 2038.76 | 1391.80 | 3103.00 |
| Javier Milei | 2023T4-2025T4 | 9 | 1195.30 | 870.36 | 684.00 | 2257.75 |

Fuente: `resultados/tablas/fase22_spread_por_regimen.csv`. Spread empalmado en puntos básicos.

### Conclusión de la extensión

Este análisis de ultra-largo plazo confirma que el umbral de fatiga fiscal estimado en la
tesis (tau* ≈ 2080-2083 pb) constituye una cota estructural: los episodios en que el spread
superó dicha marca coinciden de manera exacta con los períodos de crisis terminal de la deuda
(1989-1990, 2001-2005 y 2020-2023), demostrando que la restricción externa de financiamiento
rige la solvencia argentina con independencia del régimen monetario o político vigente.
