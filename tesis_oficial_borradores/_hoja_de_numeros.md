# Hoja de números (generada por codigo/modelos/hoja_de_numeros.py)

## Muestra y especificación
- Datos desde 1996-01-01; muestra efectiva 1998-06-30 a 2025-12-31, 111 trimestres.
- Rezagos: Schwarz elige 1; Portmanteau de ese orden p = 0,000; orden elegido 2 (Portmanteau p = 0,056). AIC sin restricción: 6; HQ: 2.
- Raíces máximas por orden: p=1: 0,844, p=2: 0,896, p=3: 0,938, p=4: 0,980, p=5: 0,999, p=6: 1,005 (inestable)
- Autovalor máximo del VAR principal: 0,896; mediana de las réplicas 0,842.
- Quiebres de Bai y Perron (deuda federal bruta 1996-2025): 2001T4, 2006T2, 2018T1
- Diagnósticos: normalidad multivariada p = 0,000; ARCH-LM p: pb_pib 0,988, crec 0,746, EMBI 0,996, TCRM 0,108
- Desvío de la variación trimestral de la FED en la muestra: 0,494 pp. AR(1) del VIX: 0,703; del nivel de la tasa de la FED: 0,970.
- Proporción en pesos: federal 0,422 (MECON, dic-2025); consolidada 0,315 (FMI, cuadro 2). λ = 0,282. Desvío máximo de la identidad respecto de la senda del FMI: 0,12 pp.
- Raíz unitaria (ADF p / KPSS p / clasificación): Resultado primario: 0,580 / 0,010 / I(1); Crecimiento real: 0,053 / 0,100 / ambigua; EMBI: 0,154 / 0,100 / ambigua; TCRM: 0,249 / 0,100 / ambigua; Deuda federal bruta: 0,094 / 0,100 / ambigua; Deuda consolidada con el BCRA: 0,094 / 0,100 / ambigua; Tasa de la FED (nivel): 0,031 / 0,013 / ambigua; VIX: 0,000 / 0,100 / I(0)
- Johansen (niveles, traza vs crítico 5%): r <= 0: 42,7 vs 47,9; r <= 1: 22,0 vs 29,8; r <= 2: 10,9 vs 15,5; r <= 3: 3,3 vs 3,8
- Empalme EMBI 1996T1-1998T3 con la tasa interbancaria en dólares del BCRA menos la tasa de fondos federales: superposición 1998T4-2001T3, n = 12, EMBI = 550,3 + 1,171 × diferencial, R2 = 0,89, correlación 0,944, RMSE dejando uno afuera 102 pb (desvío del EMBI 240 pb); fuera de muestra 2001T1-T3: real 750; 973; 1469, pronóstico 744; 801; 1033.
- Empalme TCRM 1996 con el tipo de cambio real efectivo amplio del BIS (inversa): correlación de variaciones trimestrales 0,92 (n = 115) y 0,98 en 1997-2001 (n = 19).
- Valores empalmados EMBI: 1996-03 598, 1996-06 576, 1996-09 645, 1996-12 666, 1997-03 637, 1997-06 595, 1997-09 667, 1997-12 740, 1998-03 672, 1998-06 612, 1998-09 712; TCRM 1996: 1996-03 1,235, 1996-06 1,248, 1996-09 1,252, 1996-12 1,244
- Sin empalme (datos desde 1999): no estabilización 2031 32,4 [26,6; 37,0], 2035 31,2 [26,4; 35,6]; no fiscal menos fiscal 75,5 [51,7; 86,3]; senda FED prob 2035 9,6 [2,5; 15,7].

## Estimación (fase24, intervalos de Hall al 90%)
- federal: reacción fiscal de impacto 0,0576 [0,0220; 0,0822]; largo plazo 0,199 [0,112; 0,328]
  - deuda → crec: 0,0498 [-0,0165; 0,0841]
  - deuda → EMBI: 15,2925 [-5,3414; 30,4721]
  - deuda → TCRM: -0,0012 [-0,0031; 0,0008]
- consolidada: reacción fiscal de impacto 0,0595 [0,0141; 0,0868]; largo plazo 0,223 [0,063; 0,375]
  - deuda → crec: 0,0519 [-0,0213; 0,0943]
  - deuda → EMBI: 20,0599 [-2,4077; 38,2494]
  - deuda → TCRM: -0,0001 [-0,0017; 0,0026]
- Respuestas a la FED: 2 de 84 intervalos excluyen el cero: fed_TCRM_h2 -0,032 [-0,053; -0,003], fed_TCRM_h3 -0,031 [-0,054; -0,003]

## Simulación principal (deuda federal bruta, intervalos de Hall al 90%)
- Percentiles de la deuda (p5, p25, mediana, p75, p95): 2026: 65,9, 69,2, 72,8, 75,8, 90,2; 2028: 52,0, 60,0, 65,0, 70,5, 83,1; 2031: 33,2, 44,5, 53,1, 62,7, 79,8; 2033: 24,0, 37,2, 48,0, 59,9, 81,8; 2035: 15,9, 30,0, 42,1, 57,3, 85,5
- Senda base (identidad sin shocks): 2031 53,9, 2035 42,7.
- No estabilización 2031: 31,8 [25,2; 36,4] %
- No estabilización 2035: 31,0 [26,8; 35,6] %
- No estabilización 2031 con pb simulado: 35,6 [30,9; 41,1] %
- Deuda 2031 > 2029: 25,8 [21,8; 31,2] %
- Deuda 2035 > 2033: 29,3 [25,0; 36,5] %
- Error de Monte Carlo 2031: 0,33 pp.
- Límite inferior al 95% (unilateral 2,50%): 2031 24,2, 2035 26,6.
- Límite inferior al 97.5% (unilateral 1,25%): 2031 23,4, 2035 26,1.
- Ancho del abanico 2031: 46,6 [36,8; 61,0]; mediana 2031 53,1; media 2035 45,3.
- Varianza 2035 por bloque: fiscal 10,8 [6,1; 21,3]; actividad 12,0 [0,2; 21,2]; cambiario_y_riesgo 32,3 [16,8; 48,9]; externo 44,9 [14,6; 59,0]
- H1a, no fiscal menos fiscal: 78,3 [57,3; 87,9] puntos.
- dif_fed_1de_p_noest_2031: 0,8 [0,1; 1,4]; al 95% (Bonferroni para dos escenarios): [-0,2; 1,5]
- dif_fed_1de_p_noest_2035: 1,1 [0,2; 1,9]; al 95% (Bonferroni para dos escenarios): [-0,0; 2,0]
- dif_fed_1de_d2035: 1,0 [0,0; 1,8]; al 95% (Bonferroni para dos escenarios): [-0,5; 2,0]
- dif_fed_2022_2025_p_noest_2031: 5,0 [0,2; 9,2]; al 95% (Bonferroni para dos escenarios): [-2,0; 10,3]
- dif_fed_2022_2025_p_noest_2035: 9,7 [4,2; 16,0]; al 95% (Bonferroni para dos escenarios): [3,6; 16,8]
- dif_fed_2022_2025_d2035: 9,0 [0,3; 16,2]; al 95% (Bonferroni para dos escenarios): [-4,1; 17,4]
- Costo directo de la senda de la FED en la deuda 2035: 8,6 pp de 9,0 (96%).
- Senda de la FED 2022-2025: de 0,08 (2021T4) a máximo 5,33 y 3,90 (2025T4); nivel final 3,82 pp por encima.

## Suficiencia del superávit (H1a, complemento)
- Máximo anual del resultado primario 1996-2025 sin rentas de la propiedad (definición principal): 3,29 en 2004; con rentas: 3,58 en 2004.
- Con el resultado primario en el máximo histórico en todos los años: P(2031) = 26,1% con 3,29 (sin rentas) y 24,5% con 3,58 (con rentas).
- Primer desplazamiento con P(2031) ≤ 1%: +8,00 pp, pb 2026 = 9,4% y pb 2031 = 10,3%.
- P(2035) mínima 0,71% con +6,50 pp; después sube a 2,91% con +10,00 (no monótona).

## Extensión consolidada
- No estabilización 2031 26,5 [19,1; 30,5]; 2035 24,1 [20,0; 30,0]; ancho 37,3; no fiscal menos fiscal 70,2 [43,2; 80,9]; senda FED prob 2035 10,1 [3,7; 17,2]; deuda 6,3 [-0,2; 11,8]; senda base 2031 31,9, 2035 21,8.

## Shocks a la manera del FMI
- federal_fmi: P2031 24,1%, P2035 20,6%, ancho 148,4.
- consolidada_fmi: P2031 22,2%, P2035 16,5%, ancho 100,2.
- Diagnóstico (P2031, P2035, ancho): todos_1997_2025: 24,1, 20,6, 148,4; sin_2002: 24,4, 21,9, 115,7; z_en_su_media: 22,8, 20,0, 122,8; r_en_su_media: 20,5, 18,3, 92,3; g_en_su_media: 30,0, 25,6, 129,7; pb_en_su_media: 24,2, 20,5, 155,9
- Impulsores 1997-2025: depreciación real media 3,0% (sin 2002: -2,0%); años con depreciación sobre la media 28% (sin 2002: 43%); correlación crecimiento-depreciación -0,48, crecimiento-resultado primario 0,42.

## Robustez: rango entre especificaciones del SVARX (ver Apéndice A.9)
- base_p_noest_2031: estimaciones entre 26,5 (consolidada) y 33,2 (federal_dom); menor límite inferior 19,1 (consolidada).
- base_p_noest_2035: estimaciones entre 24,1 (consolidada) y 34,8 (federal_dom); menor límite inferior 20,0 (consolidada).
- h1a_nofiscal_menos_fiscal: menor límite inferior 25,6 (federal_alfa0); todas las especificaciones excluyen el cero: True.
- dif_fed_2022_2025_p_noest_2035: incluyen el cero en 2 de 20: federal_desde2004, federal_kilian.
- dif_fed_2022_2025_d2035: incluyen el cero en 11 de 20: consolidada, federal_cr2595, federal_desde1999, federal_desde2004, federal_dom, federal_kilian, federal_lam0.15, federal_lam0.4, federal_p1, federal_sf0, federal_sin_quiebres.
- dif_fed_1de_p_noest_2035: incluyen el cero en 5 de 20: federal_cr2595, federal_desde1999, federal_desde2004, federal_dom, federal_p1.
- dif_fed_1de_d2035: incluyen el cero en 9 de 20: consolidada, federal_cr2595, federal_desde1999, federal_desde2004, federal_dom, federal_kilian, federal_lam0.15, federal_p1, federal_sin_quiebres.

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
