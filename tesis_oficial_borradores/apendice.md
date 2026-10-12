# Apéndice estadístico

Tablas generadas con `codigo/modelos/apendice_tablas.py` a partir de los resultados de `fase24_svarx_1996_2025.py` y `fase25_simulacion_dsa_svarx.py`.

## A.0 Estadísticos descriptivos

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

## A.1 Selección del orden del VAR

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

## A.2 Diagnósticos de los residuos

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

## A.3 Matriz de impacto estructural

Efecto en el mismo trimestre de un shock estructural de un desvío estándar (especificación principal). Los ceros son las restricciones de identificación de la sección 4.4. Los dos shocks del bloque cambiario y de riesgo no tienen interpretación por separado: solo se usa su efecto conjunto.

| Variable | Shock fiscal | Shock de actividad | Shock cambiario y de riesgo 1 | Shock cambiario y de riesgo 2 |
|---|---|---|---|---|
| Resultado primario | 1,509 | 0,679 | 0,000 | 0,000 |
| Crecimiento | -0,266 | 2,717 | 0,000 | 0,000 |
| EMBI+ | -118,560 | -30,491 | 449,797 | 0,000 |
| TCRM | 0,022 | -0,014 | 0,011 | 0,096 |

## A.4 Ecuación del resultado primario

Ecuación del resultado primario del VARX en forma reducida, especificación principal (MCO, 1998T2-2025T4). No se muestran la constante, las variables binarias estacionales ni las de los quiebres. Los p-valores son los de MCO; el intervalo de la reacción de Bohn que se usa en el texto es el del bootstrap.

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

## A.5 Resultados completos de la simulación por especificación

Media entre réplicas de parámetros y, entre corchetes, percentiles 5 y 95 (300 réplicas por 400 trayectorias).

| Indicador | Neta (principal) | Neta en libros | Bruta | Neta con tasas en pesos | Neta sin retroalimentación |
|---|---|---|---|---|---|
| No estabilización 2030 (%) | 11,5 [7,7; 15,2] | 12,7 [8,8; 17,0] | 12,3 [8,5; 16,3] | 12,2 [8,5; 16,2] | 11,5 [7,8; 15,8] |
| No estabilización 2035 (%) | 6,6 [3,2; 10,5] | 7,4 [3,8; 11,8] | 7,8 [4,5; 11,8] | 8,8 [4,2; 14,5] | 6,1 [3,2; 10,0] |
| Deuda media 2035 (% PIB) | 16,4 [15,4; 17,6] | 17,7 [16,8; 19,1] | 22,8 [21,9; 24,0] | 17,1 [15,7; 19,1] | 16,3 [15,3; 17,4] |
| Ancho p5-p95 2030 | 18,6 [14,4; 23,3] | 19,0 [14,5; 23,9] | 19,3 [15,8; 24,3] | 21,0 [15,7; 27,2] | 19,9 [15,6; 24,9] |
| Varianza 2035: fiscal (%) | 21,2 [4,0; 43,3] | 20,8 [4,6; 41,7] | 23,7 [3,1; 53,7] | 17,9 [2,8; 41,3] | 21,0 [4,1; 44,0] |
| Varianza 2035: actividad (%) | 19,0 [3,4; 45,2] | 20,2 [3,2; 52,1] | 24,9 [5,4; 55,4] | 14,0 [2,4; 37,1] | 18,4 [4,2; 44,8] |
| Varianza 2035: cambiario y de riesgo (%) | 59,8 [12,6; 90,0] | 59,1 [14,5; 88,8] | 51,5 [5,7; 86,7] | 68,1 [27,5; 92,7] | 60,5 [12,3; 88,7] |
| H1a: no fiscal menos fiscal | 57,7 [13,4; 92,0] | 58,5 [16,6; 90,8] | 52,6 [-7,5; 93,7] | 64,2 [17,4; 94,5] | 57,9 [11,9; 91,8] |
| H2: FED 1 desvío, Δ probabilidad 2035 (pp) | 0,7 [0,0; 1,7] | 0,8 [0,0; 1,8] | 0,7 [0,0; 1,5] | 0,8 [0,0; 2,0] | 0,6 [0,0; 1,5] |
| H2: FED 2022-2023, Δ probabilidad 2035 (pp) | 9,5 [3,7; 19,0] | 10,1 [3,8; 20,3] | 8,7 [2,8; 15,8] | 11,0 [3,0; 25,0] | 8,2 [3,8; 15,8] |
| H2: FED 2022-2023, Δ deuda 2035 (pp PIB) | 7,8 [1,9; 17,5] | 8,4 [2,1; 18,8] | 7,5 [0,6; 15,9] | 8,8 [1,1; 21,7] | 7,6 [2,2; 16,0] |

