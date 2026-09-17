# Especificación alternativa del DSA estocástico: calibración a mano, GARCH, DCC-GARCH y CIR

Documento de trabajo, fuera de la tesis. Sacado del cuerpo principal (y del apéndice) a pedido
del usuario el 2026-09-16, para mostrárselo al director y que decida si algo de esto se integra
a la versión final. La tesis, tal como queda, documenta como especificación de referencia del
componente estocástico del DSA la covarianza derivada de los residuos del SVAR restringido
(Sección "Simulación Estocástica del DSA con Covarianza del SVAR Restringido" del Capítulo de
Resultados), con una probabilidad de insolvencia hacia 2035 del 26,1%.

Antes de esa especificación, se había desarrollado y validado una calibración a mano de la matriz
de covarianzas, con dos extensiones sucesivas hacia procesos estimados (GARCH(1,1) univariado y
DCC-GARCH) y un proceso de difusión continua Cox-Ingersoll-Ross (CIR) para el riesgo soberano.
Ninguno de estos tres resultados se descartó ni se recalculó bajo la covarianza nueva: quedan acá
documentados en su totalidad, con sus valores originales intactos.

## 1. Calibración a mano y probabilidad por escenario

La matriz de covarianzas se calibró inicialmente a partir de órdenes de magnitud razonables de la
volatilidad histórica argentina para las cinco perturbaciones del DSA (resultado primario,
crecimiento, tasa doméstica, tasa externa, variación del tipo de cambio real), con una
distribución *t* de Student multivariada (ν≈4,8, calibrado por método de momentos sobre la
curtosis en exceso muestral). Bajo esta calibración, la probabilidad de que la ratio Deuda/PIB
supere el 100% del producto hacia 2035 en el escenario de Referencia es del 31,2%, con una
mediana de 80,7% del PIB.

| Escenario | Probabilidad de superar 100% del PIB | Mediana 2035 (% PIB) |
|---|---|---|
| Optimista | 3,8% | 45,1% |
| Referencia | 31,2% | 80,7% |
| Estrés | 99,9% | 816,5% |

Bajo el escenario Optimista, la probabilidad de cruzar el umbral crítico se reduce a apenas 3,8%,
con una mediana de deuda en 2035 (45,1% del PIB) muy por debajo del nivel inicial de 2025 (74%).
En el extremo opuesto, el escenario de Estrés arroja una probabilidad de insolvencia del 99,9%,
prácticamente segura.

## 2. Robustez de la calibración: desvíos estándar estimados vía GARCH

Como chequeo de robustez sobre la calibración a mano, se reestimaron los desvíos estándar del
resultado primario, del crecimiento del producto y de la variación del tipo de cambio real
mediante un modelo GARCH(1,1) univariado por serie, mientras que la matriz de correlación
histórica y los desvíos de las tasas de interés se mantuvieron en su valor calibrado original.

| Perturbación | Calibrado | GARCH(1,1) |
|---|---|---|
| Resultado primario (σ_pb) | 0,0150 | 0,0114 |
| Crecimiento del PIB (σ_g) | 0,0400 | 0,0640 |
| Variación TCR (σ_Δe) | 0,1500 | 0,1300 |

Los tres desvíos GARCH se ubican en el mismo orden de magnitud que la calibración original: el
resultado primario y el tipo de cambio real resultan algo menos volátiles bajo GARCH, mientras
que el crecimiento resulta algo más volátil, un resultado plausible dado que la serie de PIB real
exhibe conglomerados de volatilidad (*volatility clustering*).

| Escenario | Prob. calibrada | Prob. GARCH parcial |
|---|---|---|
| Optimista | 3,8% | 5,8% |
| Referencia | 31,2% | 33,4% |
| Estrés | 99,9% | 99,9% |

La probabilidad de insolvencia del escenario de Referencia se desplaza de 31,2% a 33,4% bajo la
calibración GARCH parcial: una diferencia de apenas 2,2 puntos porcentuales.

## 3. Correlación Condicional Dinámica: DCC-GARCH

Como extensión adicional sobre la calibración a mano, se estimó un modelo de Correlación
Condicional Dinámica (DCC-GARCH, Engle 2002) en dos etapas de Cuasi-Máxima Verosimilitud (QML)
sobre los residuos estandarizados de los GARCH(1,1) univariados.

La estimación por QML converge, sobre la serie real de TCRM, a un parámetro de reactividad a≈0:
el DCC(1,1) colapsa nuevamente a Correlación Condicional Constante (CCC, Bollerslev 1990). El
aporte de esta etapa es la reestimación por QML del *nivel* de correlación:

- Resultado primario–crecimiento: 0,40 calibrada vs. 0,11 QML.
- Resultado primario–tipo de cambio real: -0,30 calibrada vs. +0,20 QML (con la serie real el
  signo de esta correlación se invierte respecto de la calibración original).
- Crecimiento–tipo de cambio real: -0,50 vs. -0,17.

Sustituyendo estas correlaciones en el DSA, la probabilidad de insolvencia del escenario de
Referencia hacia 2035 pasa de 31,2% a 32,5%, confirmando la robustez cualitativa del resultado
pese al cambio de signo puntual en una de las tres correlaciones reestimadas.

## 4. Robustez a la dependencia en colas

La distribución *t* multivariada de la calibración a mano introduce dependencia en colas (*tail
dependence*) que podría sobreestimar la frecuencia de eventos extremos simultáneos. El
coeficiente de dependencia en colas es λ = 2·T_{ν+1}(-√((ν+1)(1-ρ)/(1+ρ))), que para ν=4,8 y la
correlación QML estimada (ρ=0,11, resultado primario-crecimiento) resulta λ≈0,076 (7,6%)
(Demarta y McNeil, 2005).

| Especificación de las perturbaciones | P(d_2035>100%) |
|---|---|
| (1) Cópula-t (ν≈4,8) + correlación histórica | 31,2% |
| (2) Cópula gaussiana + correlación histórica | 29,2% |
| (3) Cópula gaussiana + sin correlación | 24,6% |

La probabilidad se desplaza de 31,2% a 29,2% al remover el exceso de dependencia en colas de la
cópula-t, y a 24,6% al remover además la correlación entre perturbaciones. En ambos casos el
desplazamiento es moderado (entre 2,0 y 6,6 puntos porcentuales) y no revierte ninguna conclusión
cualitativa.

## 5. Calibración del proceso estocástico CIR del EMBI+

Como extensión distinta de las dos anteriores, se calibró el riesgo soberano (EMBI+) como un
proceso de difusión continua con reversión a la media de Cox-Ingersoll-Ross (CIR 1985), en lugar
de un shock discreto calibrado o estimado por GARCH.

| Parámetro estimado | Muestra homogénea (2004-2025) | Muestra ampliada (1999-2025) |
|---|---|---|
| Velocidad de reversión (κ) | 0,9229 | 0,4279 |
| Nivel de equilibrio (θ, en pb) | 1032,25 | 1590,41 |
| Volatilidad de difusión (σ) | 26,9175 | 26,4954 |
| Vida media de reversión (t½=ln(2)/κ) | 0,75 años | 1,62 años |
| Condición de Feller (2κθ>σ²) | 1905,30 > 724,55, cumple | 1361,14 > 702,00, cumple |
| Ratio de Feller (2κθ/σ²) | 2,6296 > 1,0 | 1,9389 > 1,0 |
| Criterio AIC (CIR vs. AR(1)) | 1278,69 < 1342,34, prefiere CIR | 1594,84 < 1673,14, prefiere CIR |

Fuente: `resultados/tablas/fase20_cir_calibracion.csv`. Estimación por MLE exacta sobre la
función de densidad Chi-cuadrado no central. La figura de la simulación (trayectorias + densidad
terminal) está en `tesis/figuras/figura_cir_simulacion.png` (no se movió, es un archivo de código
del repo, no de la tesis compilada).

Al integrar las 1.000 trayectorias continuas del proceso CIR en el módulo de proyección
estocástica del DSA hacia 2035 (sustituyendo la tasa de refinanciación externa fija por
r_f,t = r_US,t + CIR_t), la probabilidad estimada de insolvencia (P(d_2035>100%)) se sitúa en
29,8%, convergiendo con gran consistencia con la cifra central de la calibración a mano de este
documento (31,2%) y sus robusteces (30,4% a 31,9%), y del mismo orden de magnitud que la
especificación de referencia de la tesis, fundada en el SVAR (26,1%).

---

**Nota de trazabilidad.** Este contenido vivió, en algún momento de este proceso, primero en el
cuerpo principal de la tesis (Resultados y Discusión, con la calibración a mano como especificación
de referencia), y después, brevemente, en un apéndice de la tesis (Apéndice A.3) una vez que la
covarianza del SVAR pasó a ser la referencia. Se sacó del documento entero a pedido explícito del
usuario ("no, al apéndice no, a otro lado, no en la tesis"). Los archivos de código y resultados que
lo sostienen (`codigo/modelos/fase20_cir_embi_calibracion.py`, `codigo/modelos/dcc_garch.py`,
`codigo/modelos/fase10_dcc_garch.py`, `resultados/tablas/fase20_*.csv`) tampoco se tocaron y siguen
en el repo tal cual estaban.
