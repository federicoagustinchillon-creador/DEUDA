# Apéndice estadístico

Fuente de todas las tablas: elaboración propia.

## A.1 Estadísticos descriptivos

Muestra efectiva de estimación, 1998T2-2025T4 (111 trimestres).

| Variable | Media | Desvío estándar | Mínimo | Máximo |
|---|---|---|---|---|
| Resultado primario (% del PIB, trimestral anualizado) | -0,04 | 3,23 | -12,16 | 7,02 |
| Crecimiento real trimestral (%) | 0,39 | 7,41 | -13,77 | 18,21 |
| EMBI+ (puntos básicos) | 1.561,19 | 1.611,94 | 210,22 | 6.658,98 |
| TCRM (diciembre de 2001 = 1) | 1,66 | 0,45 | 0,98 | 2,76 |
| Deuda consolidada neta, rezagada (% del PIB) | 57,74 | 27,07 | 26,13 | 136,60 |
| Variación de la tasa de la FED (puntos) | -0,01 | 0,52 | -1,43 | 1,69 |
| VIX | 20,20 | 7,33 | 10,31 | 58,60 |

## A.2 Propiedades de las series

**Raíz unitaria.** ADF (Dickey y Fuller, 1979; hipótesis nula: raíz unitaria) y KPSS (Kwiatkowski et al., 1992; hipótesis nula: estacionariedad), con constante. Una serie se clasifica como estacionaria solo si ADF rechaza y KPSS no rechaza al 5%, y con raíz unitaria en el caso inverso. Zivot y Andrews (1992) permiten un quiebre endógeno en el nivel. Muestra 1996T4-2025T4.

| Serie | ADF (p) | KPSS (p) | Clasificación | Zivot-Andrews (p) | Quiebre de Zivot-Andrews |
|---|---|---|---|---|---|
| Resultado primario | 0,591 | 0,010 | raíz unitaria | 0,982 | 2011T2 |
| Crecimiento real | 0,053 | 0,100 | ambigua | 0,236 | 2003T1 |
| EMBI+ | 0,151 | 0,100 | ambigua | 0,087 | 2005T2 |
| TCRM | 0,250 | 0,100 | ambigua | 0,000 | 2001T4 |
| Deuda consolidada neta | 0,099 | 0,100 | ambigua | 0,575 | 2005T1 |
| Tasa de la FED (nivel) | 0,019 | 0,047 | ambigua | 0,020 | 2021T2 |
| VIX | 0,000 | 0,100 | estacionaria | 0,028 | 2019T4 |

**Quiebres estructurales.** El procedimiento de Bai y Perron (2003) sobre la media de la deuda consolidada neta, con el número de quiebres elegido por el criterio de Schwarz, encuentra 3 quiebres: 2001T4, 2006T2 y 2018T1. Son los que entran como variables binarias en el SVARX.

**Cointegración.** Prueba de la traza de Johansen (1991) sobre las variables en niveles (resultado primario, EMBI+, TCRM y deuda), con los rezagos del VAR. El crecimiento se excluye porque es una tasa de variación: incluido, genera por sí solo una relación de cointegración trivial.

| Hipótesis nula | Traza | Valor crítico 5% | Rechaza |
|---|---|---|---|
| rango ≤ 0 | 43,7 | 47,9 | no |
| rango ≤ 1 | 20,0 | 29,8 | no |
| rango ≤ 2 | 10,8 | 15,5 | no |
| rango ≤ 3 | 3,3 | 3,8 | no |

## A.3 Selección del orden del VAR

Muestra efectiva común 1998T2-2025T4 (111 trimestres) para todos los órdenes (sección 4.5). El orden elegido es el mayor orden estable que no supera al que minimiza el AIC.

**Deuda consolidada neta, valor nominal (principal).** Orden elegido: 3.

| p | AIC | BIC | HQ | Raíz máxima | Estable | Portmanteau (p) |
|---|---|---|---|---|---|---|
| 1 | 12,351 | 13,914 | 12,985 | 0,855 | sí | 0,000 |
| 2 | 12,052 | 14,005 | 12,844 | 0,894 | sí | 0,039 |
| 3 | 12,125 | 14,468 | 13,075 | 0,964 | sí | 0,036 |
| 4 | 12,009 | 14,743 | 13,118 | 1,021 | no | 0,023 |
| 5 | 11,939 | 15,064 | 13,207 | 1,024 | no | 0,002 |
| 6 | 11,918 | 15,433 | 13,344 | 1,033 | no | 0,000 |

**Deuda consolidada neta, valor libros.** Orden elegido: 3.

| p | AIC | BIC | HQ | Raíz máxima | Estable | Portmanteau (p) |
|---|---|---|---|---|---|---|
| 1 | 12,326 | 13,888 | 12,960 | 0,855 | sí | 0,000 |
| 2 | 12,043 | 13,996 | 12,835 | 0,900 | sí | 0,034 |
| 3 | 12,122 | 14,466 | 13,073 | 0,961 | sí | 0,030 |
| 4 | 12,003 | 14,737 | 13,112 | 1,014 | no | 0,021 |
| 5 | 11,937 | 15,062 | 13,205 | 1,017 | no | 0,002 |
| 6 | 11,918 | 15,433 | 13,344 | 1,015 | no | 0,000 |

**Deuda consolidada bruta.** Orden elegido: 4.

| p | AIC | BIC | HQ | Raíz máxima | Estable | Portmanteau (p) |
|---|---|---|---|---|---|---|
| 1 | 12,378 | 13,940 | 13,011 | 0,818 | sí | 0,000 |
| 2 | 12,082 | 14,034 | 12,874 | 0,840 | sí | 0,071 |
| 3 | 12,170 | 14,514 | 13,121 | 0,923 | sí | 0,035 |
| 4 | 12,057 | 14,791 | 13,167 | 0,987 | sí | 0,020 |
| 5 | 11,984 | 15,108 | 13,251 | 1,004 | no | 0,002 |
| 6 | 11,968 | 15,483 | 13,394 | 1,027 | no | 0,000 |

## A.4 Diagnósticos de los residuos

Portmanteau con 12 rezagos (autocorrelación), Jarque-Bera multivariada (normalidad), ARCH-LM con cuatro rezagos por ecuación (heterocedasticidad condicional) y estabilidad (1 = estable).

| Prueba (p-valor salvo estabilidad) | neta, valor nominal (principal) | neta, valor libros | bruta |
|---|---|---|---|
| Portmanteau (12 rezagos) | 0,036 | 0,030 | 0,020 |
| Normalidad multivariada (p-valor) | 0,000 | 0,000 | 0,000 |
| Estable (1 = sí) | 1,000 | 1,000 | 1,000 |
| ARCH-LM(4) resultado primario (p-valor) | 0,991 | 0,988 | 0,993 |
| ARCH-LM(4) crecimiento (p-valor) | 0,989 | 0,990 | 0,978 |
| ARCH-LM(4) EMBI (p-valor) | 0,998 | 0,998 | 0,999 |
| ARCH-LM(4) TCRM (p-valor) | 0,867 | 0,824 | 0,395 |

## A.5 Matriz de impacto estructural

Efecto en el mismo trimestre de un shock estructural de un desvío estándar (especificación principal). Los ceros son las restricciones de identificación de la sección 4.4. Los dos shocks del bloque cambiario y de riesgo no tienen interpretación por separado: solo se usa su efecto conjunto.

| Variable | Shock fiscal | Shock de actividad | Shock cambiario y de riesgo 1 | Shock cambiario y de riesgo 2 |
|---|---|---|---|---|
| Resultado primario | 1,509 | 0,679 | 0,000 | 0,000 |
| Crecimiento | -0,266 | 2,717 | 0,000 | 0,000 |
| EMBI+ | -118,560 | -30,491 | 449,797 | 0,000 |
| TCRM | 0,022 | -0,014 | 0,011 | 0,096 |

## A.6 Ecuación del resultado primario

Ecuación del resultado primario del VARX en forma reducida, especificación principal (MCO, 1998T2-2025T4). No se muestran la constante, las variables binarias estacionales ni las de los quiebres. Los errores estándar y los p-valores son los de MCO y se informan como referencia: con regresores que pueden tener raíz unitaria su distribución no es la estándar (Sims et al., 1990), por lo que la inferencia del texto usa los intervalos del *bootstrap*.

| Regresor | Coeficiente | Error estándar | p-valor |
|---|---|---|---|
| Variación de la tasa de la FED, rezago 0 | 0,5297 | 0,5178 | 0,306 |
| Variación de la tasa de la FED, rezago 1 | -0,7911 | 0,5670 | 0,163 |
| Variación de la tasa de la FED, rezago 2 | 0,0030 | 0,5160 | 0,995 |
| VIX | -0,0253 | 0,0319 | 0,427 |
| Deuda consolidada neta, rezago 1 (reacción de Bohn) | 0,0505 | 0,0215 | 0,019 |
| Resultado primario, rezago 1 | 0,3404 | 0,1116 | 0,002 |
| Crecimiento, rezago 1 | 0,0901 | 0,0647 | 0,164 |
| EMBI+, rezago 1 | -0,0005 | 0,0004 | 0,189 |
| TCRM, rezago 1 | 3,6341 | 1,7183 | 0,034 |
| Resultado primario, rezago 2 | 0,3739 | 0,1190 | 0,002 |
| Crecimiento, rezago 2 | 0,1250 | 0,0633 | 0,048 |
| EMBI+, rezago 2 | 0,0001 | 0,0005 | 0,850 |
| TCRM, rezago 2 | -2,9019 | 2,3871 | 0,224 |
| Resultado primario, rezago 3 | 0,0149 | 0,1154 | 0,897 |
| Crecimiento, rezago 3 | -0,0330 | 0,0605 | 0,586 |
| EMBI+, rezago 3 | 0,0002 | 0,0004 | 0,520 |
| TCRM, rezago 3 | -0,2936 | 1,6455 | 0,858 |

## A.7 Resultados completos de la especificación principal

Estimación central con parámetros corregidos por sesgo (Kilian, 1998) y 20.000 trayectorias; intervalos de 200 réplicas con 1.000 trayectorias cada una. Autovalor máximo del VAR: 0,964 estimado y 0,9998 corregido.

| Medida | Estimación central | Intervalo de 90% |
|---|---|---|
| No estabilización 2031 (%) | 25,2 | [19,0; 27,7] |
| No estabilización 2035 (%) | 22,3 | [15,6; 24,9] |
| No estabilización 2031 con el resultado primario simulado (%) | 29,2 | [21,7; 31,1] |
| Probabilidad de que la deuda de 2031 supere a la de 2029 (%) | 22,0 | [13,2; 23,8] |
| Deuda mediana 2031 (% del PIB) | 39,5 | [38,8; 40,3] |
| Deuda media 2035 (% del PIB) | 31,3 | [29,5; 33,6] |
| Ancho del abanico 2031 (p5-p95) | 35,3 | [19,1; 37,6] |
| Varianza 2035: fiscal (%) | 32,1 | [4,4; 52,4] |
| Varianza 2035: actividad (%) | 9,3 | [3,8; 43,1] |
| Varianza 2035: cambiario y de riesgo (%) | 58,7 | [17,2; 86,0] |
| No fiscal menos fiscal (puntos) | 35,9 | [-4,8; 91,2] |
| Cambiario y de riesgo menos fiscal (puntos) | 26,6 | [-31,2; 80,3] |
| Promedio por shock cambiario y de riesgo menos fiscal (puntos) | -2,5 | [-40,7; 38,1] |
| FED, un desvío: diferencia en la probabilidad 2035 (pp) | 1,5 | [0,1; 3,1] |
| FED, un desvío: diferencia en la deuda 2035 (pp del PIB) | 1,0 | [-0,1; 2,4] |
| FED, senda 2022-2025: diferencia en la probabilidad 2031 (pp) | 2,4 | [-4,5; 11,4] |
| FED, senda 2022-2025: diferencia en la probabilidad 2035 (pp) | 13,0 | [1,0; 24,8] |
| FED, senda 2022-2025: diferencia en la deuda 2035 (pp del PIB) | 7,8 | [-1,4; 20,4] |

