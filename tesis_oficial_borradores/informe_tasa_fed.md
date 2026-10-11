# Informe: tasa de politica de la Fed, trimestral 1996Q1-2025Q4 (v1)

## Fuentes
- FEDFUNDS, tasa efectiva de fondos federales, mensual, FRED: https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS (ultimo dato bajado: 2026-09).
- Tasa sombra de Wu-Xia, mensual, Atlanta Fed: https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/datafiles/cqer/research/wu-xia-shadow-federal-funds-rate/WuXiaShadowRate.xlsx (pagina: https://www.atlantafed.org/cqer/research/wu-xia-shadow-federal-funds-rate). Se usa la columna de la tasa sombra; la hoja termina en febrero de 2022.
- Copias crudas: `datos/crudos/tasa_fed/`. Codigo: `codigo/ingesta_datos/ingesta_tasa_fed_1996_2025.py`. Salida: `datos/procesados/tasa_fed_trimestral_1996_2025.csv`.

Citas (APA 7):
- Board of Governors of the Federal Reserve System (US). (s. f.). *Federal funds effective rate* [FEDFUNDS; conjunto de datos]. Federal Reserve Bank of St. Louis, FRED. https://fred.stlouisfed.org/series/FEDFUNDS
- Wu, J. C., y Xia, F. D. (2016). Measuring the macroeconomic impact of monetary policy at the zero lower bound. *Journal of Money, Credit and Banking, 48*(2-3), 253-291. https://doi.org/10.1111/jmcb.12300
- Federal Reserve Bank of Atlanta. (s. f.). *Wu-Xia shadow federal funds rate* [conjunto de datos]. https://www.atlantafed.org/cqer/research/wu-xia-shadow-federal-funds-rate

## Construccion
1. Cada serie mensual se promedia por trimestre calendario; `Date` es el fin de trimestre.
2. `tasa_politica_fed` = tasa sombra cuando el promedio trimestral de FEDFUNDS es menor a 0,25 % y los tres meses de la sombra estan disponibles; en el resto, FEDFUNDS. Umbral 0,25 %: el limite superior del rango objetivo en el piso cero fue 0,25 %, por lo que un promedio efectivo menor lo indica.
3. `fuente_flag`: `fedfunds` (84 trimestres), `shadow_wu_xia` (35), `fedfunds_zlb_sin_shadow` (1).

## Cobertura
- 120 trimestres, sin faltantes en `fedfunds` ni en `tasa_politica_fed`.
- La sombra se usa en 2009Q1-2015Q4 (28 trimestres) y 2020Q2-2021Q4 (7 trimestres).
- La serie sombra publicada termina en 2022-02. 2022Q1 esta en piso cero (FEDFUNDS = 0,12 %) pero tiene solo 2 de 3 meses de sombra; se usa FEDFUNDS y queda marcado `fedfunds_zlb_sin_shadow`. Los trimestres 2022Q2-2025Q4 usan FEDFUNDS (todos sobre el piso).
- Limitacion: el empalme sombra-efectiva en 2022Q1 introduce un salto de nivel de unos 1,7 pp entre 2021Q4 (-1,57) y 2022Q1 (0,12), que es un artefacto de la definicion de la serie y no un cambio de politica de un trimestre.

## Estadisticas (variacion trimestral de `tasa_politica_fed`, 1996Q1-2025Q4)
- Observaciones: 119 variaciones (la primera diferencia pierde 1996Q1).
- Media: -0,0123 pp por trimestre.
- Desvio estandar: 0,5047 pp (muestral, ddof = 1); poblacional (ddof = 0): 0,5026 pp.
- Ciclo 2022-2023: ultimo trimestre previo 2021Q4 (tasa combinada -1,5689 %, sombra) hasta el pico en 2023Q4 (5,33 %): suba acumulada de 6,90 pp. Medida con FEDFUNDS solo (0,08 % en 2021Q4): 5,25 pp, que es la magnitud comparable con el ciclo 2004-2006.
- Ciclo 2004-2006: base 2003Q4 (0,99 %) a pico en 2007Q1 (5,2567 %): suba acumulada de 4,26 pp.
