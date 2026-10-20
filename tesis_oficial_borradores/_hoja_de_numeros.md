# Hoja de números (generada por codigo/modelos/hoja_de_numeros.py)

## Muestra y especificación
- Datos desde 1996-01-01; muestra efectiva 1998-06-30 a 2025-12-31, 111 trimestres.
- Rezagos: Schwarz elige 1; Portmanteau de ese orden p = 0,000; orden elegido 2 (Portmanteau p = 0,031). AIC sin restricción: 6; HQ: 2.
- Raíces máximas por orden: p=1: 0,746, p=2: 0,776, p=3: 0,862, p=4: 0,953, p=5: 1,005 (inestable), p=6: 1,008 (inestable)
- Autovalor máximo del VAR principal: 0,776; mediana de las réplicas 0,773.
- Quiebres de Bai y Perron (deuda federal bruta 1996-2025): 2006T2, 2018T1
- Diagnósticos: normalidad multivariada p = 0,000; ARCH-LM p: pb_pib 0,960, crec 0,833, EMBI 0,925, TCRM 0,000
- Desvío de la variación trimestral de la FED en la muestra: 0,501 pp. AR(1) del VIX: 0,703; del nivel de la tasa de la FED: 0,972.
- Proporción en pesos: federal 0,422 (MECON, dic-2025; 57,8% en moneda extranjera); consolidada 0,315 (FMI, cuadro 2). λ = 0,282. Desvío máximo de la identidad respecto de la senda del FMI: 0,12 pp.
- Raíz unitaria (ADF p / KPSS p / clasificación): Resultado primario: 0,580 / 0,010 / I(1); Crecimiento real: 0,053 / 0,100 / ambigua; EMBI: 0,154 / 0,100 / ambigua; TCRM: 0,249 / 0,100 / ambigua; Deuda federal bruta: 0,094 / 0,100 / ambigua; Deuda consolidada con el BCRA: 0,396 / 0,095 / ambigua; Tasa de la FED (nivel): 0,104 / 0,010 / I(1); VIX: 0,000 / 0,100 / I(0)
- Johansen (niveles, traza vs crítico 5%): r <= 0: 42,7 vs 47,9; r <= 1: 22,0 vs 29,8; r <= 2: 10,9 vs 15,5; r <= 3: 3,3 vs 3,8
- Empalme EMBI 1996T1-1998T3 con la tasa interbancaria en dólares del BCRA menos la tasa de fondos federales: superposición 1998T4-2001T3, n = 12, EMBI = 550,3 + 1,171 × diferencial, R2 = 0,89, correlación 0,944, RMSE dejando uno afuera 102 pb (desvío del EMBI 240 pb); fuera de muestra 2001T1-T3: real 750; 973; 1469, pronóstico 744; 801; 1033.
- Empalme TCRM 1996 con el tipo de cambio real efectivo amplio del BIS (inversa): correlación de variaciones trimestrales 0,92 (n = 115) y 0,98 en 1997-2001 (n = 19).
- Valores empalmados EMBI: 1996-03 598, 1996-06 576, 1996-09 645, 1996-12 666, 1997-03 637, 1997-06 595, 1997-09 667, 1997-12 740, 1998-03 672, 1998-06 612, 1998-09 712; TCRM 1996: 1996-03 1,235, 1996-06 1,248, 1996-09 1,252, 1996-12 1,244
- Sin empalme (datos desde 1999): no estabilización 2031 29,5 [22,5; 36,7], 2035 30,7 [27,4; 38,2]; no fiscal menos fiscal 95,7 [88,9; 99,8]; senda FED prob 2035 18,0 [5,6; 28,3].

## Estimación (fase24, intervalos de Hall al 90%)
- federal: reacción fiscal de impacto 0,0466 [0,0231; 0,0835]; largo plazo 0,079 [0,062; 0,147]
  - deuda → crec: 0,0715 [-0,0014; 0,1255]
  - deuda → EMBI: 34,8578 [13,9380; 47,6147]
  - deuda → TCRM: -0,0003 [-0,0024; 0,0023]
- consolidada: reacción fiscal de impacto 0,0481 [0,0106; 0,0887]; largo plazo 0,062 [0,019; 0,117]
  - deuda → crec: 0,0457 [-0,0227; 0,1327]
  - deuda → EMBI: 36,7360 [13,1464; 52,3615]
  - deuda → TCRM: 0,0006 [-0,0031; 0,0010]
- Respuestas a la FED: 11 de 84 intervalos excluyen el cero: fed_pb_pib_h0 0,317 [0,016; 0,705], fed_TCRM_h2 -0,031 [-0,049; -0,006], fed_TCRM_h3 -0,029 [-0,051; -0,006], fed_EMBI_h4 62,306 [1,529; 122,240], fed_pb_pib_h5 -0,109 [-0,240; -0,004], fed_EMBI_h5 62,685 [16,757; 128,045], fed_pb_pib_h6 -0,104 [-0,207; -0,003], fed_EMBI_h6 43,152 [2,016; 99,602], fed_pb_pib_h7 -0,097 [-0,193; -0,019], fed_pb_pib_h8 -0,072 [-0,153; -0,015], fed_pb_pib_h9 -0,047 [-0,110; -0,002]
- Redondeos para el texto: deuda → EMBI federal 34,9, 13,9, 47,6; consolidada 36,7, 13,1, 52,4; deuda → crec federal 0,07, -0,00, 0,13; deuda → crec federal con tres decimales -0,001, 0,126; coeficiente de enlace del PIB 1993-2004 (informe de construcción de datos) 1,751; coeficiente de Bohn de referencia 0,05; respuestas del resultado primario a la FED entre -0,05 y -0,11; parte indirecta del efecto de la FED en la deuda 2035: 4,5 pp (diferencia entre el total y el costo directo).

## Simulación principal (deuda federal bruta, intervalos de Hall al 90%)
- Percentiles de la deuda (p5, p25, mediana, p75, p95): 2026: 67,2, 70,3, 72,5, 74,9, 87,7; 2028: 54,1, 60,4, 64,8, 70,2, 80,4; 2031: 36,0, 45,7, 52,9, 61,4, 76,5; 2033: 26,7, 38,1, 47,4, 58,6, 78,9; 2035: 17,7, 30,4, 41,4, 55,9, 84,3
- Senda base (identidad sin shocks): 2031 53,9, 2035 42,7.
- No estabilización 2031: 27,7 [20,6; 34,7] %
- No estabilización 2035: 29,0 [25,0; 36,1] %
- No estabilización 2031 con pb simulado: 29,7 [23,5; 37,3] %
- Deuda 2031 > 2029: 20,0 [17,3; 26,7] %
- Deuda 2035 > 2033: 25,1 [19,9; 34,7] %
- Error de Monte Carlo 2031: 0,32 pp.
- No estabilización 2031, definición operativa del FMI: 3,1 [0,0; 6,3] %
- No estabilización 2035, definición operativa del FMI: 5,1 [0,0; 10,2] %
- No estabilización 2031, definición operativa del FMI con pb simulado: 4,8 [0,0; 9,4] %
- No estabilización 2035, definición operativa del FMI con pb simulado: 6,1 [0,0; 12,2] %
- No estabilización 2031, recuadro 3 con todo promediado en la trayectoria: 0,0 [0,0; 0,0] %
- No estabilización 2035, recuadro 3 con todo promediado en la trayectoria: 0,9 [0,0; 1,8] %
- Definición operativa del FMI, límite inferior al 95% (Bonferroni): 2031 -3,7, 2035 -5,8.
- dif_fed_1de_p_noest_fmi_2035: 1,1 [-0,5; 2,2]; al 95%: [-1,0; 2,2]
- dif_fed_2022_2025_p_noest_fmi_2031: 9,1 [-2,1; 17,7]; al 95%: [-5,9; 18,1]
- dif_fed_2022_2025_p_noest_fmi_2035: 17,1 [0,6; 32,6]; al 95%: [-3,6; 33,6]
- Límite inferior al 95% (unilateral 2,50%): 2031 19,0, 2035 24,1.
- Límite inferior al 97.5% (unilateral 1,25%): 2031 17,6, 2035 23,3.
- Ancho del abanico 2031: 40,5 [32,4; 54,5]; mediana 2031 52,9; media 2035 45,0.
- Varianza 2035 por bloque: fiscal 1,6 [0,1; 4,6]; actividad 10,7 [1,6; 24,1]; cambiario_y_riesgo 28,3 [7,8; 42,6]; externo 59,4 [40,3; 88,3]; externo_vix 113,2 [51,6; 222,5]; externo_fed 13,3 [2,9; 55,6]; externo_fed_directo 7,6 [3,7; 29,1]; externo_fed_indirecto 5,7 [-6,9; 36,6]
- H1a, no fiscal menos fiscal: 96,8 [90,8; 99,8] puntos.
- dif_fed_1de_p_noest_2031: 1,0 [-0,3; 1,6]; al 95% (Bonferroni para dos escenarios): [-0,6; 1,7]
- dif_fed_1de_p_noest_2035: 1,9 [0,3; 3,2]; al 95% (Bonferroni para dos escenarios): [-0,1; 3,3]
- dif_fed_1de_d2035: 2,0 [0,4; 3,2]; al 95% (Bonferroni para dos escenarios): [-0,4; 3,4]
- dif_fed_2022_2025_p_noest_2031: 6,7 [0,6; 12,8]; al 95% (Bonferroni para dos escenarios): [-1,0; 15,2]
- dif_fed_2022_2025_p_noest_2035: 18,4 [6,3; 29,1]; al 95% (Bonferroni para dos escenarios): [4,1; 30,8]
- dif_fed_2022_2025_d2035: 19,3 [-0,3; 31,3]; al 95% (Bonferroni para dos escenarios): [-8,4; 32,8]
- Costo directo de la senda de la FED en la deuda 2035: 14,8 pp de 19,3 (77%).
- Senda de la FED 2022-2025: de 0,08 (2021T4) a máximo 5,33 y 3,90 (2025T4); nivel final 3,82 pp por encima.

## Suficiencia del superávit (H1a, complemento)
- Máximo anual del resultado primario 1996-2025 sin rentas de la propiedad (definición principal): 3,29 en 2004; con rentas: 3,58 en 2004.
- Con un desplazamiento uniforme que lleva el resultado primario de 2031 al máximo histórico: P(2031) = 23,0% con 3,29 (sin rentas) y 21,6% con 3,58 (con rentas).
- Resultado primario del escenario base: 2026 1,40%, 2031 2,30%; con el desplazamiento al máximo de 2031, 2026 queda en 2,39%.
- Primer desplazamiento con P(2031) ≤ 1%: +7,25 pp, pb 2026 = 8,65% y pb 2031 = 9,55%.
- Definición operativa del FMI: P(2031) con el máximo histórico = 0,9%; sin desplazamiento = 3,1%; primer desplazamiento con P(2031) ≤ 1%: +1,00 pp.
- P(2035) mínima 0,12% con +6,25 pp; después sube a 1,99% con +10,00 (no monótona).

## Extensión consolidada
- No estabilización 2031 31,1 [27,6; 41,5]; 2035 35,0 [32,3; 49,8]; ancho 55,2; no fiscal menos fiscal 100,0 [96,8; 100,0]; senda FED prob 2035 19,2 [3,2; 33,8]; réplicas con media de la deuda 2035 explosiva (|d|>1000): 368 de 1000 (no se informa la media de la deuda consolidada); senda base 2031 31,9, 2035 21,8.

## Shocks a la manera del FMI
- federal_fmi: P2031 24,1%, P2035 20,6%, ancho 148,4; definición operativa del FMI: P2031 29,1%, P2035 19,1%.
- consolidada_fmi: P2031 26,2%, P2035 19,4%, ancho 63,4; definición operativa del FMI: P2031 16,1%, P2035 7,3%.
- Diagnóstico (P2031, P2035, ancho): todos_1997_2025: 24,1, 20,6, 148,4; sin_2002: 24,4, 21,9, 115,7; z_en_su_media: 22,8, 20,0, 122,8; r_en_su_media: 20,5, 18,3, 92,3; g_en_su_media: 30,0, 25,6, 129,7; pb_en_su_media: 24,2, 20,5, 155,9
- Impulsores 1997-2025: depreciación real media 3,0% (sin 2002: -2,0%); años con depreciación sobre la media 28% (sin 2002: 43%); correlación crecimiento-depreciación -0,48, crecimiento-resultado primario 0,42.

## Robustez: rango entre especificaciones del SVARX (ver Apéndice A.10)
- base_p_noest_2031: estimaciones entre 25,3 (federal_sf0) y 31,8 (federal_sin_presidenciales); menor límite inferior 16,2 (federal_p3).
- base_p_noest_2035: estimaciones entre 22,4 (federal_sf0) y 35,0 (consolidada); menor límite inferior 18,0 (federal_sf0).
- base_p_noest_fmi_2031: estimaciones entre 0,9 (federal_cr2595) y 11,0 (consolidada); menor límite inferior 0,0 (federal).
- base_p_noest_fmi_2035: estimaciones entre 0,3 (federal_sin_retro) y 17,4 (federal_dom); menor límite inferior 0,0 (federal).
- Diferencia no fiscal menos fiscal por especificación (estimación [p5; p95]): consolidada: 100,0 [96,8; 100,0]; federal: 96,8 [90,8; 99,8]; federal_alfa0: 85,6 [72,3; 99,5]; federal_alfa0.5: 99,4 [88,0; 99,7]; federal_chol: 85,6 [72,3; 99,5]; federal_chol_ultimo: 99,4 [93,9; 99,8]; federal_cr2595: 96,4 [90,1; 99,8]; federal_desde1999: 95,7 [88,9; 99,8]; federal_desde2004: 90,3 [83,4; 100,0]; federal_dom: 98,9 [94,5; 100,0]; federal_kilian: 93,6 [78,1; 99,8]; federal_lam0.15: 96,0 [89,3; 99,7]; federal_lam0.4: 97,3 [91,9; 99,9]; federal_p1: 99,9 [90,7; 99,9]; federal_p3: 91,6 [80,2; 99,6]; federal_pb_alt: 99,5 [92,0; 99,8]; federal_sf0: 95,9 [89,4; 99,8]; federal_sin_default: 97,1 [91,1; 99,8]; federal_sin_presidenciales: 77,9 [67,3; 99,4]; federal_sin_quiebres: 93,9 [88,2; 99,8]; federal_sin_retro: 95,1 [88,1; 99,6]
- h1a_nofiscal_menos_fiscal: menor límite inferior 67,3 (federal_sin_presidenciales); todas las especificaciones excluyen el cero: True.
- base_p_noest_fmi_2031: límite inferior por encima de la cifra del FMI (1% en 2031, 3% en 2035) en 2 de 21: consolidada, federal_dom.
  Estimaciones por especificación: consolidada 11,0 [2,7; 20,2]; federal 3,1 [0,0; 6,3]; federal_alfa0 3,1 [0,0; 6,3]; federal_alfa0.5 3,1 [0,0; 6,3]; federal_chol 3,1 [0,0; 6,3]; federal_chol_ultimo 3,1 [0,0; 6,3]; federal_cr2595 0,9 [0,0; 1,8]; federal_desde1999 3,6 [0,0; 7,2]; federal_desde2004 6,2 [0,0; 12,5]; federal_dom 9,0 [2,7; 17,0]; federal_kilian 6,0 [0,0; 11,5]; federal_lam0.15 1,8 [0,0; 3,6]; federal_lam0.4 4,8 [0,0; 9,3]; federal_p1 3,9 [0,0; 7,7]; federal_p3 2,5 [0,0; 5,1]; federal_pb_alt 2,9 [0,0; 5,8]; federal_sf0 2,2 [0,0; 4,5]; federal_sin_default 3,8 [0,0; 7,5]; federal_sin_presidenciales 6,2 [0,2; 11,9]; federal_sin_quiebres 2,3 [0,0; 4,7]; federal_sin_retro 1,3 [0,0; 2,7]
- base_p_noest_fmi_2035: límite inferior por encima de la cifra del FMI (1% en 2031, 3% en 2035) en 2 de 21: consolidada, federal_dom.
  Estimaciones por especificación: consolidada 17,3 [7,4; 32,3]; federal 5,1 [0,0; 10,2]; federal_alfa0 5,1 [0,0; 10,2]; federal_alfa0.5 5,1 [0,0; 10,2]; federal_chol 5,1 [0,0; 10,2]; federal_chol_ultimo 5,1 [0,0; 10,2]; federal_cr2595 2,0 [0,0; 3,9]; federal_desde1999 5,6 [0,0; 11,2]; federal_desde2004 4,9 [0,0; 9,8]; federal_dom 17,4 [9,7; 32,3]; federal_kilian 10,8 [0,0; 21,2]; federal_lam0.15 1,7 [0,0; 3,4]; federal_lam0.4 8,1 [0,0; 15,9]; federal_p1 7,3 [0,0; 14,4]; federal_p3 3,7 [0,0; 7,4]; federal_pb_alt 5,5 [0,0; 10,9]; federal_sf0 3,0 [0,0; 6,0]; federal_sin_default 6,7 [0,0; 13,3]; federal_sin_presidenciales 8,3 [0,3; 16,4]; federal_sin_quiebres 2,3 [0,0; 4,6]; federal_sin_retro 0,3 [0,0; 0,6]
- dif_fed_2022_2025_p_noest_2035: incluyen el cero en 1 de 21: federal_desde2004.
- dif_fed_2022_2025_d2035: incluyen el cero en 10 de 21: consolidada, federal, federal_desde1999, federal_desde2004, federal_dom, federal_kilian, federal_lam0.4, federal_p1, federal_sin_default, federal_sin_presidenciales.
- dif_fed_1de_p_noest_2035: incluyen el cero en 2 de 21: federal_desde2004, federal_sin_presidenciales.
- dif_fed_1de_d2035: incluyen el cero en 6 de 21: consolidada, federal_desde2004, federal_dom, federal_kilian, federal_p1, federal_sin_presidenciales.

## Tabla 5.2: deuda de esta tesis y del FMI (diciembre, % del PIB)
- Propia, Deuda federal bruta: 2023: 153,5, 2024: 82,1, 2025: 77,7
- Propia, Deuda del Tesoro en poder del BCRA: 2023: 39,4, 2024: 20,4, 2025: 17,2
- Propia, Pasivos del BCRA: 2023: 14,6, 2024: 1,6, 2025: 1,3
- Propia, Depósitos del Tesoro en el BCRA: 2023: 0,5, 2024: 2,1, 2025: 0,8
- Propia, Deuda consolidada con el BCRA: 2023: 128,2, 2024: 61,1, 2025: 61,0
- FMI, Línea 1, deuda federal bruta: 2023: 154,6, 2024: 84,7, 2025: 80,3
- FMI, Línea 3, deuda del Tesoro en poder del sector público: 2023: 62,1, 2024: 33,7, 2025: 31,4
- FMI, Línea 4, pasivos del BCRA: 2023: 19,2, 2024: 2,6, 2025: 3,3
- FMI, Línea 5, deuda consolidada: 2023: 111,1, 2024: 53,6, 2025: 52,1
- FMI, Swap con el PBoC: 2023: 2,1, 2024: 0,9, 2025: 0,9
- FMI, Deuda en moneda extranjera / deuda total (%): 2023: 69,3, 2024: 61,9, 2025: 68,5
- Brecha consolidada propia menos FMI: 17,1, 7,5, 8,9; federal FMI menos propia: 1,1, 2,6, 2,6
