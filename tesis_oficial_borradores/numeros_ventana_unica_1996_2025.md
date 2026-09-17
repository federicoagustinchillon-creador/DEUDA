# Ventana única 1996-2025: todos los números reales (segunda ronda)

Continúa a `numeros_ventana_1996_2025.md` (que cubría VECM/SVAR/TVECM/DSA). Este
archivo cubre la segunda ronda: DOLS, IV-2SLS, Hansen niveles, Bai-Perron,
Etapa 1 (DF-GLS/Zivot-Andrews), todo reestimado sobre `dataset_consolidado_1996_2025.csv`
(n=120) para que **todo el protocolo corra sobre una única ventana de medición**,
a pedido explícito del usuario ("el rango de medición debe ser único, no múltiples").

**Cambio de framing importante, decidido por el usuario**: la ventana "original"
2004-2025 (n=88) deja de ser una segunda ventana de estimación paralela. Sigue
existiendo como la sub-muestra de cobertura 100% real (sin empalme) dentro de
la ventana única, útil para descriptivos que no quieren mezclar tramo empalmado
con tramo real, pero **ya no sostiene ninguna técnica del protocolo por separado**.
Todo (DF-GLS, Johansen, VECM, DOLS, IV-2SLS, Hansen, TVECM, SVAR, Bai-Perron, DSA)
corre sobre 1996-2025.

## Reencuadre de H1a: de "fatiga fiscal" a "régimen de reacción extremo"

Confirmado con el usuario: el patrón real (ver Hansen niveles abajo) no es fatiga
fiscal (reacción que se debilita bajo estrés) sino lo opuesto — el gobierno no
reacciona en absoluto en el régimen normal, y reacciona fuerte y significativamente
solo por encima de un umbral extremo de riesgo soberano. Es un patrón de "disciplina
fiscal gatillada por crisis" / reacción de régimen extremo, no una función de
reacción continua que se atenúa. H1a debe reescribirse en este sentido en
Introducción, Resultados, Discusión y Conclusiones.

## 1. DOLS (fase3_reaccion_fiscal.py, ventana única, n=110 tras ampliación dinámica)

- ρ (coeficiente sobre d_t_1) = **0,0159** (antes -0,0071), p=0,218. Sigue NO
  significativo, pero el signo pasa de negativo a **positivo** (dirección
  correcta según Bohn, aunque sin significatividad).
- m óptimo (adelantos/rezagos AIC) = 4, igual que antes.
- MCO estático previo: d_t_1 coef=0,0220, p=0,061 (marginal al 10%); Hausman
  p=0,0000 (endogeneidad detectada, igual que antes, obligatorio usar DOLS/IV).
- Diagnósticos: Breusch-Godfrey p=0,0000, Breusch-Pagan p=0,0032, Jarque-Bera
  p=0,0150, RESET p=0,0000 (todos rechazan, igual patrón que antes).
- Archivo: `resultados/tablas/fase3_resultados_dols.csv` (sobreescrito).

## 2. IV-2SLS (fase4_variables_instrumentales.py, ventana única, n=119)

**Instrumento nuevo**: el ETF EMB (usado antes) cotiza recién desde dic-2007, no
cubre 1996-2025. Se investigaron alternativas reales: EWZ, PCY, BZF no tienen
historia antes de 2000-2007 vía Yahoo Finance. El índice Bovespa (^BVSP) sí tiene
serie diaria real desde 1994. Nuevo instrumento: `BOVESPA_VOL` = desvío estándar
de los retornos logarítmicos diarios del Bovespa por trimestre, anualizado
(×√252, en pp). Construido en `codigo/ingesta_datos/ingesta_instrumentos_1996_2025.py`,
datos reales de Yahoo Finance, sin aproximación. VIX también se extendió con datos
reales (^VIX cotiza desde 1990).

Resultado real:
- Ecuación: pb_pib ~ 1 + d_t_1 + g_gap + [EMBI ~ VIX + BOVESPA_VOL]
- Coeficiente EMBI (β): **0,0012** (antes 0,0017), p=**0,0239** (significativo al
  5%, antes marginal al 10% con p=0,076)
- F de primera etapa (instrumentos excluidos): **15,87** (p=0,0004) — mejor que
  el 13,00 anterior, supera holgadamente el criterio de Staiger-Stock (>10)
- Wu-Hausman (endogeneidad): stat=2,17, **p=0,1435** — **NO rechaza exogeneidad**
  (antes rechazaba categóricamente, p<0,001). Cambio importante: la evidencia
  de endogeneidad del EMBI+ se debilita bajo el instrumento nuevo.
- Sargan (sobreidentificación): stat=0,0059, **p=0,9390** — instrumentos muy
  cómodamente válidos (antes p=0,436)
- d_t_1: coef=-0,0313, p=0,1879 (no significativo)
- g_gap: coef=0,0578, p=0,0882 (marginal al 10%)
- Archivos: `resultados/tablas/fase4_resultados_iv.csv`,
  `resultados/tablas/fase4_diagnosticos_iv.csv` (sobreescritos).

Lectura: el canal EMBI+→pb sale MÁS fuerte y ahora sí significativo al 5%, pero
la prueba formal de que el EMBI+ sea endógeno (Wu-Hausman) se debilita. Conviene
matizar, no forzar una lectura única: podría reflejar que BOVESPA_VOL, al ser un
instrumento de renta variable y no de renta fija soberana, capta una porción
distinta (más débil en el canal de endogeneidad specific) del riesgo regional que
el ETF de bonos original.

## 3. Hansen en niveles (fase5_umbral_hansen.py, ventana única, n=119)

- τ* = **2462,1** pb (antes 449 pb en la ventana original; más cercano ahora a
  los ~2080-2104 pb de Hansen-Δpb y TVECM, aunque sigue siendo el más alto de
  las tres estimaciones de umbral)
- Sup-LM bootstrap: F=0,1857, **p=0,0000** — SIGNIFICATIVO (antes p=0,076,
  marginal)
- Régimen normal (EMBI≤2462): coef=**-0,0044**, p=0,665, NO significativo
- Régimen de estrés (EMBI>2462): coef=**+0,0201**, p=**0,006**, SIGNIFICATIVO
- g_gap: coef=0,0375, p=0,216 (no significativo)
- Veredicto impreso por el propio script: "[SOSTENIBLE] El Estado logra
  sostener la reacción fiscal positiva incluso en crisis."
- Archivo: `resultados/tablas/fase5_resultados_hansen.csv` (sobreescrito).

Patrón: NO es fatiga fiscal (que predeciría reacción atenuada bajo estrés). Es
reacción nula en normalidad y reacción fuerte solo bajo estrés extremo — un
régimen de reacción discontinuo/gatillado por crisis, no una función continua
que se degrada.

## 4. Bai-Perron (fase9_bai_perron.py, ventana única para deuda_pib SPNF; deuda
   consolidada BCRA acotada a su cobertura real 2004-2025)

**Bug corregido**: el script rellenaba con `fillna(0)` los pasivos del BCRA
anteriores a 2004 para construir "deuda_consolidada_pib", lo que asumía
falsamente pasivos remunerados nulos del BCRA en 1996-2003. Corregido: ya no
se rellena, esa serie queda acotada a su cobertura real (2004-2025, n=88).

Deuda SPNF sola (deuda_pib), ventana completa 1996-2025 (n=120):
- m* = 3 quiebres (BIC)
- Quiebres: **2001-09**, 2006-03, 2017-09 (antes, con la ventana 2004-2025,
  no podía detectarse el quiebre de 2001 porque la muestra arrancaba después)
- Segmentos: 1996-03/2001-09 (media 34,68%, n=23); 2001-12/2006-03 (media
  106,85%, n=18); 2006-06/2017-09 (media 50,72%, n=46); 2017-12/2025-12
  (media 81,24%, n=33)

Deuda consolidada SPNF+BCRA, cobertura real 2004-2025 (n=88):
- m* = 2 quiebres (BIC)
- Quiebres: 2007-06, 2016-12
- Segmentos: 2004-03/2007-06 (media 81,76%, n=14); 2007-09/2016-12 (media
  53,46%, n=38); 2017-03/2025-12 (media 86,36%, n=36)

Archivos: `resultados/tablas/fase9_bai_perron_bic.csv`,
`fase9_bai_perron_quiebres.csv`, `fase9_bai_perron_segmentos_deuda_pib.csv`,
`fase9_bai_perron_segmentos_deuda_consolidada.csv`, figura
`tesis/figuras/figura_9_1_bai_perron.png` (todos regenerados).

## 5. Etapa 1: estacionariedad, DF-GLS, Zivot-Andrews (fase1_estacionariedad.py,
   ventana única, n=120; CER excluido, no existe antes de feb-2002)

ADF/KPSS combinado (mismo resultado que ya estaba escrito en 05_datos.tex):
deuda_pib linda con I(0) (ADF p=0,042 rechaza raíz unitaria, KPSS p=0,10 no
rechaza estacionariedad); pb_pib, EMBI, TCRM claramente I(1); g_gap I(0).

**DF-GLS (Elliott-Rothenberg-Stock), más potente que ADF simple**:
- pb_pib: stat=-1,30 (crít 5%=-3,01) → I(1)
- deuda_pib: stat=-2,65 (crít 5%=-3,01) → **I(1)** (a diferencia del ADF simple,
  DF-GLS SÍ respalda tratar la deuda como I(1); útil para reforzar la decisión
  ya tomada de mantener el tratamiento I(1) pese a la ambigüedad del ADF/KPSS)
- EMBI: stat=-2,30 (crít 5%=-3,01) → I(1)
- g_gap: stat=-3,46 (crít 5%=-3,02) → I(0)

**Zivot-Andrews (quiebre único endógeno, deuda_pib)**:
- t=-4,50, quiebre óptimo en 2004-06-30
- Críticos: 1%=-5,58, 5%=-5,07, 10%=-4,83
- NO significativo ni al 10% (mismo patrón que antes: Zivot-Andrews no
  encuentra quiebre único significativo, es Bai-Perron el que sí lo hace con
  múltiples quiebres)

Archivos: `resultados/tablas/fase1_estacionariedad.csv`, `fase1_dfgls.csv`,
`fase1_zivot_andrews.csv` (sobreescritos).

## 6. Qué queda igual / no cambia
- SVAR restringido, VECM, TVECM, Johansen, DSA con covarianza del SVAR: ya
  reestimados y escritos en la ronda anterior (`numeros_ventana_1996_2025.md`),
  sin cambios adicionales en esta ronda.
- CIR/DCC-GARCH (Etapa 6 alternativa): sigue fuera de la tesis, en
  `tesis_oficial_borradores/especificacion_alternativa_dsa_cir_dccgarch.md`.
- Extensión histórica 1983-2025 (spread + Bai-Perron + CIR de fechado): se
  queda en la tesis, sin cambios, uso distinto del CIR.
