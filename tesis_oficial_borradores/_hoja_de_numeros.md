# Hoja de números (generada por codigo/modelos/hoja_de_numeros.py)

## Muestra y especificación
- Datos desde 1999T1; muestra efectiva 2000-09-30 a 2025-12-31, 102 trimestres.
- Rezagos: Schwarz elige 1; Portmanteau de ese orden p = 0,000; orden elegido 2 (Portmanteau p = 0,296). AIC sin restricción: 5; HQ: 2.
- Raíces máximas por orden: p=1: 0,828, p=2: 0,849, p=3: 0,922, p=4: 0,972, p=5: 0,998, p=6: 1,011 (inestable)
- Autovalor máximo del VAR principal: 0,849; mediana de las réplicas 0,818.
- Quiebres de Bai y Perron (deuda federal bruta 1996-2025): 2001T4, 2006T2, 2018T1
- Diagnósticos: normalidad multivariada p = 0,000; ARCH-LM p: pb_pib 0,988, crec 0,868, EMBI 0,998, TCRM 0,114
- Desvío de la variación trimestral de la FED en la muestra: 0,504 pp. AR(1) del VIX: 0,700; del nivel de la tasa de la FED: 0,960.
- Proporción en pesos: federal 0,422 (MECON, dic-2025); consolidada 0,315 (FMI, cuadro 2). λ = 0,282. Desvío máximo de la identidad respecto de la senda del FMI: 0,12 pp.
- Raíz unitaria (ADF p / KPSS p / clasificación): Resultado primario: 0,651 / 0,010 / I(1); Crecimiento real: 0,005 / 0,100 / I(0); EMBI+: 0,330 / 0,100 / ambigua; TCRM: 0,272 / 0,054 / ambigua; Deuda federal bruta: 0,091 / 0,100 / ambigua; Deuda consolidada con el BCRA: 0,101 / 0,100 / ambigua; Tasa de la FED (nivel): 0,014 / 0,046 / ambigua; VIX: 0,000 / 0,100 / I(0)
- Johansen (niveles, traza vs crítico 5%): r <= 0: 45,0 vs 47,9; r <= 1: 24,0 vs 29,8; r <= 2: 9,6 vs 15,5; r <= 3: 2,9 vs 3,8

## Estimación (fase24, intervalos de Hall al 90%)
- federal: reacción fiscal de impacto 0,0495 [0,0099; 0,0799]; largo plazo 0,167 [0,057; 0,296]
  - deuda → crec: 0,0473 [-0,0177; 0,0907]
  - deuda → EMBI: 15,5302 [-4,2245; 29,6825]
  - deuda → TCRM: -0,0014 [-0,0036; 0,0005]
- consolidada: reacción fiscal de impacto 0,0620 [0,0128; 0,0889]; largo plazo 0,249 [0,059; 0,420]
  - deuda → crec: 0,0529 [-0,0194; 0,1045]
  - deuda → EMBI: 20,1073 [-1,9175; 37,8660]
  - deuda → TCRM: -0,0001 [-0,0021; 0,0026]
- Respuestas a la FED: 3 de 84 intervalos excluyen el cero: fed_TCRM_h2 -0,040 [-0,062; -0,007], fed_TCRM_h3 -0,038 [-0,063; -0,009], fed_TCRM_h4 -0,026 [-0,051; -0,001]

## Simulación principal (deuda federal bruta, intervalos de Hall al 90%)
- Percentiles de la deuda (p5, p25, mediana, p75, p95): 2026: 65,0, 68,8, 72,3, 76,7, 90,6; 2028: 50,6, 59,3, 64,7, 71,1, 85,0; 2031: 31,8, 43,6, 52,6, 62,7, 80,1; 2033: 22,5, 35,8, 46,8, 59,5, 82,6; 2035: 13,7, 28,1, 41,1, 57,1, 87,4
- Senda base (identidad sin shocks): 2031 53,9, 2035 42,7.
- No estabilización 2031: 32,8 [26,8; 37,9] %
- No estabilización 2035: 31,3 [27,0; 35,3] %
- No estabilización 2031 con pb simulado: 35,4 [30,3; 40,8] %
- Deuda 2031 > 2029: 27,5 [23,9; 33,1] %
- Deuda 2035 > 2033: 30,8 [27,5; 38,2] %
- Error de Monte Carlo 2031: 0,33 pp.
- Límite inferior al 95% (unilateral 2,50%): 2031 26,3, 2035 26,4.
- Límite inferior al 97.5% (unilateral 1,25%): 2031 25,6, 2035 26,3.
- Ancho del abanico 2031: 48,3 [39,9; 63,1]; mediana 2031 52,6; media 2035 44,6.
- Varianza 2035 por bloque: fiscal 8,7 [3,8; 17,1]; actividad 12,4 [3,6; 21,8]; cambiario_y_riesgo 32,3 [20,0; 48,0]; externo 46,6 [18,3; 58,6]
- H1a, no fiscal menos fiscal: 82,6 [65,8; 92,4] puntos.
- dif_fed_1de_p_noest_2031: 0,9 [0,0; 1,5]; al 95% (Bonferroni para dos escenarios): [-0,2; 1,6]
- dif_fed_1de_p_noest_2035: 1,5 [0,5; 2,6]; al 95% (Bonferroni para dos escenarios): [0,2; 2,7]
- dif_fed_1de_d2035: 1,5 [0,1; 2,5]; al 95% (Bonferroni para dos escenarios): [-0,0; 2,6]
- dif_fed_2022_2025_p_noest_2031: 5,1 [-0,2; 9,1]; al 95% (Bonferroni para dos escenarios): [-0,8; 11,1]
- dif_fed_2022_2025_p_noest_2035: 11,3 [4,4; 17,9]; al 95% (Bonferroni para dos escenarios): [1,4; 18,6]
- dif_fed_2022_2025_d2035: 12,6 [1,2; 21,8]; al 95% (Bonferroni para dos escenarios): [-0,5; 22,2]
- Costo directo de la senda de la FED en la deuda 2035: 9,4 pp de 12,6 (75%).
- Senda de la FED 2022-2025: de 0,08 (2021T4) a máximo 5,33 y 3,90 (2025T4); nivel final 3,82 pp por encima.

## Suficiencia del superávit (H1a, complemento)
- Máximo anual del resultado primario 1999-2025 (definición del FMI, con rentas): 3,58 en 2004; sin rentas: 3,29.
- Con el resultado primario en el máximo histórico en todos los años (pb 2031 = 3,58): P(2031) = 25,5%.
- Primer desplazamiento con P(2031) ≤ 1%: +7,75 pp, pb 2026 = 9,2% y pb 2031 = 10,0%.
- P(2035) mínima 1,35% con +6,25 pp; después sube a 2,05% con +8,00 (no monótona).

## Extensión consolidada
- No estabilización 2031 26,8 [20,3; 31,0]; 2035 24,1 [20,4; 29,6]; ancho 38,0; no fiscal menos fiscal 67,1 [36,8; 86,1]; senda FED prob 2035 10,1 [2,5; 16,7]; deuda 6,7 [-0,3; 12,4]; senda base 2031 31,9, 2035 21,8.

## Shocks a la manera del FMI
- federal_fmi: P2031 16,6%, P2035 15,1%, ancho 151,1.
- consolidada_fmi: P2031 15,3%, P2035 12,3%, ancho 103,4.
- Diagnóstico (P2031, P2035, ancho): todos_2000_2025: 16,6, 15,1, 151,1; sin_2002: 23,6, 21,4, 104,3; z_en_su_media: 17,6, 18,6, 102,0; r_en_su_media: 20,4, 18,4, 97,8; g_en_su_media: 29,1, 23,7, 128,3; pb_en_su_media: 16,7, 15,0, 153,4
- Impulsores 2000-2025: depreciación real media 4,0% (sin 2002: -1,6%); años con depreciación sobre la media 31% (sin 2002: 44%); correlación crecimiento-depreciación -0,51, crecimiento-resultado primario 0,44.

## Robustez: rango entre especificaciones del SVARX (ver Apéndice A.8)
- base_p_noest_2031: estimaciones entre 26,8 (consolidada) y 33,6 (federal_dom); menor límite inferior 20,3 (consolidada).
- base_p_noest_2035: estimaciones entre 24,1 (consolidada) y 34,2 (federal_dom); menor límite inferior 20,4 (consolidada).
- h1a_nofiscal_menos_fiscal: menor límite inferior 31,4 (federal_chol); todas las especificaciones excluyen el cero: True.
- dif_fed_2022_2025_p_noest_2035: incluyen el cero en 1 de 19: federal_desde2004.
- dif_fed_2022_2025_d2035: incluyen el cero en 7 de 19: consolidada, federal_desde2004, federal_dom, federal_kilian, federal_p1, federal_pb_alt, federal_sin_quiebres.
- dif_fed_1de_p_noest_2035: incluyen el cero en 2 de 19: federal_desde2004, federal_pb_alt.
- dif_fed_1de_d2035: incluyen el cero en 8 de 19: consolidada, federal_cr2595, federal_desde2004, federal_dom, federal_kilian, federal_lam0.15, federal_p1, federal_pb_alt.
