# Deuda publica consolidada 1996T1-2025T4: decisiones, fuentes y control

Script: `codigo/ingesta_datos/construir_deuda_consolidada_1996_2025.py`
Salida: `datos/procesados/deuda_consolidada_1996_2025.csv` (120 trimestres, fin de trimestre),
`datos/procesados/deuda_consolidada_1996_2025_control_fmi.csv`,
figura `resultados/figuras_borrador/deuda_consolidada_1996_2025.png`.
Crudos nuevos: `datos/crudos/deuda_consolidada_1996/` (PIB y BCRA, cache de las descargas).

## 1. Que denominador usan hoy las series del repo (evidencia)

- `pasivos_bcra_pib` (`ingesta_bcra_pasivos.py`, docstring l.26-45 y l.174): divide el stock de fin de
  trimestre por el PIB nominal trimestral **anualizado de ese trimestre** (serie INDEC 166.2_PPIB_0_0_3).
  Verificado: el promedio de los cuatro trimestres de un anio reproduce el PIB anual, es decir, la serie
  esta a tasa anual. En 2023T4 el PIB anualizado es 284,9 billones de ARS contra 193,9 billones del PIB
  del anio 2023; por eso el cociente da 9,05% y no 13,3%. Es el problema de denominador planteado.
- Defecto adicional de ese script (l.116-152): la serie 166.2 empieza en 2006, y el script **extrapola** 2004-2005.
  Hay una serie INDEC real que cubre 2004T1+ (4.4_OGP_2004_T_17); por ejemplo 2004T1 real = 439.196 vs extrapolado 411.303.
  Tambien hace `fillna(0.0)` de los tramos sin dato, que es suponer ceros sin evidencia.
- `deuda_pib` (SPNF): **no es un cociente calculado de un stock en pesos.** 2004-2025 sale del diccionario
  `DEUDA_PIB_TRIM` escrito a mano (`ingesta_mecon_indec.py` l.77+; el propio docstring l.24-33 dice que
  los IDs de datos.gob.ar, entre ellos 174.1_DEUDA_PUBLICA_TOTAL_0_0_21, devuelven HTTP 400 y que el 100%
  de las 88 observaciones viene del diccionario, contrastado con el FMI WEO como promedio anual). 1996-2003 sale del
  Compendio Fiscal (cociente anual "% del PIB en dolares", `empalme_historico_pre2004.py` l.63-76), multiplicado por un
  coeficiente de enlace 110,25/127,30 y desagregado con Denton. Por lo tanto no tiene un denominador trimestral definido
  (el de la fuente es un PIB anual) y su serie en pesos no existe. Recomendacion: no usar `deuda_pib` del dataset
  actual para esta consolidacion; los valores del diccionario son redondos y no trazables a un archivo de origen
  (regla de grounding del repo).

## 2. Denominador elegido (uno solo para ambos terminos)

PIB4T_t = promedio de los ultimos cuatro valores trimestrales anualizados = suma de los ultimos cuatro flujos trimestrales
de PIB nominal.

Justificacion:
1. El FMI (CR 25/95, Annex II, Table 2, nota 1: "debt-to-GDP ratio is based on average period GDP") divide stock de fin de
   periodo por el PIB del anio. En el cuarto trimestre PIB4T coincide con esa convencion (verificado: 2023 da 155,4% de
   deuda bruta vs 153,5% propio).
2. Un stock es una variable de fin de periodo y el PIB es un flujo anual; dividir por un flujo de un solo trimestre anualizado
   mezcla estacionalidad y, en alta inflacion (2023T4 vs 2023: +47%), sobre-infla el denominador. La suma de cuatro
   trimestres elimina la estacionalidad y es la practica estandar en series trimestrales de deuda/PIB.
3. Contrapartida: con inflacion de tres digitos (2023-2024) PIB4T es un promedio rezagado y subestima el PIB corriente
   del fin de periodo; el ratio queda algo sobrestimado en la aceleracion y subestimado en la desinflacion. Se declara
   en `denominador_tipo`.

Ambos ratios se recalculan desde stocks en pesos: `deuda_spnf_ars_mm / pib_4t_mm` y `pasivos_bcra_ars_mm / pib_4t_mm`.

### PIB 1996-2025 (IDs)
- 2004T1-2025T4: datos.gob.ar 4.4_OGP_2004_T_17 (INDEC, PIB a precios de comprador corrientes, base 2004; idéntico a
  166.2_PPIB_0_0_3 en 2006+).
- 1995T1-2003T4: datos.gob.ar 2.4_OGP_1993_T_17 (INDEC, base 1993, termina 2013T3), empalmado multiplicando por el
  coeficiente de enlace 1,0837 = media 2004 (base 2004) / media 2004 (base 1993), cuatro trimestres solapados.
  Limite: la razon base2004/base1993 no es constante (por trimestre de 2004 va de 1,07 a 1,12 por estacionalidad
  distinta, y deriva a 1,27 en 2013), de modo que el nivel pre-2004 tiene incertidumbre; `pib_origen` marca
  `base1993_empalmada`.

## 3. Deuda SPNF (en pesos)

- Fuente: MECON, Informe de Deuda Publica al 31/12/2025, hoja A.4.5 (deuda bruta total en miles de millones de USD,
  trimestral 1998T1-2025T4; 1994-1997 solo diciembre), multiplicada por el tipo de cambio de fin de trimestre de
  la hoja A.2.4 (U$S/Peso; control: 31/12/2023 = 808,45 = cociente USD/ARS de A.1.1 del informe 2023). 1996-2001: paridad legal 1:1 (Ley 23.928).
  Nota: A.2.4 trae una fila con fecha 2022-03-31 duplicada, claramente 2002-03-31 (CER 1,0481 intercalado); el script la reasigna
  de forma explicita y solo si detecta la duplicacion.
- Perimetro: es la deuda bruta de la Administracion Central/SPN (no el SPNF consolidado), excluye la deuda elegible pendiente de reestructuracion,
  y es **bruta**: incluye tenencias del BCRA, FGS y otros organismos publicos.
- 1996T1-T3 y 1997T1-T3 (6 trimestres) estan interpolados linealmente en USD entre cierres de diciembre
  (`spnf_origen = interpolado_lineal_usd`); el resto (114) es dato trimestral del informe.

## 4. Pasivos remunerados del BCRA

API BCRA v4.0, mismos ids: 1258 (LEBAC/NOBAC), 1260 (LELIQ/NOTALIQ), 1261 (posicion neta de pases). Consulta desde 1996-01-01:
- 1258: primera observacion 2002-03-15 (la API no devuelve nada antes) -> cero antes de 2002T1, bandera `lebac_nobac_sin_serie=1`.
- 1260: primera observacion 2018-01-02 -> cero antes, bandera `leliq_notaliq_sin_serie=1`.
- 1261: desde 1996-01-02, sin huecos de cobertura.
- Dato sensible: 1261 es **neta** (pases pasivos - pases activos) y es negativa en 2001T2-2002T2 (BCRA prestamista neto) y en 2024T4-2025T1;
  esos trimestres tienen `pasivos_bcra_neto_negativo=1` y el total reduce la deuda. El concepto "pasivos" estricto seria bruto
  (id 152 = pases pasivos, 154 = activos, existen desde 2004-05); no se uso para respetar los ids acordados. Queda como sensibilidad abierta.

## 5. Neteo de tenencias intra-sector publico

No se implementa. Con datos reales no es posible 1996-2025 trimestral: MECON A.4.5 clasifica por residencia (externo/interno), no por sector
tenedor; las tenencias del BCRA y del FGS solo estan en el FMI para 2023-2026 (Table 2, linea 2). Sesgo del concepto bruto, con las cifras del FMI:
la deuda federal excluyendo tenencias intra-sector publico es 92,9% del PIB en 2023 y 51,4% en 2024, contra 155,4% y 85,3% brutas:
la serie bruta sobrestima la deuda con el sector privado en ~62,5 pp (2023) y ~33,9 pp (2024). Ademas el FMI resta los depositos del Tesoro en el BCRA
(0,5% y 2,1%). En consecuencia `deuda_consolidada_pib` es un **techo bruto**, no la deuda neta consolidada del FMI, y no es comparable con ella en nivel.

## 6. Tabla de control vs FMI CR 25/95, Annex II, Table 2 (PDF p. 68)

| Concepto (% PIB) | 2023 propio | 2023 FMI | 2024 propio | 2024 FMI |
|---|---|---|---|---|
| Deuda federal bruta | 153,5 | 155,4 | 82,1 | 85,3 |
| Pasivos BCRA (ids 1258+1260+1261) | 13,3 | 18,4 | -0,06 | 2,2 |
| Pasivos BCRA con PIB anualizado del Q4 (metodo anterior) | 9,05 | - | -0,05 | - |
| Consolidada bruta (propia) / consolidada neta (FMI) | 166,8 | 110,8 | 82,0 | 51,5 |

Diferencias:
- Deuda bruta: el FMI agrega intereses capitalizados, holdouts y reclamos por el cupon PIB (nota 1 de la tabla), que no estan en los informes MECON; y usa
  la version de PIB de su informe (2024 especialmente: la serie INDEC actual es posterior). Diferencia -1,9 y -3,2 pp.
- BCRA: el FMI incluye ademas BOPREAL y la porcion activada del swap con el PBoC (nota de texto, p. 68), instrumentos fuera de los tres ids.
  En 2023 el FMI da US$43,5 mil millones (~35,7 billones de ARS) contra 25,8 billones propios: la brecha de ~9,9 billones (~5,1 pp) es compatible con
  esos componentes pero no la verifico con datos. Con el denominador del FMI el cociente propio sube de 9,05% a 13,3%: el 4,25 pp
  de diferencia es puramente de denominador. En 2024 los pasivos remunerados pasaron al Tesoro (LEFI) y quedan dentro de la deuda bruta MECON; los 2,2% del FMI son
  BOPREAL/otros, no cubiertos aqui.
- Consolidado: no comparable (bruto vs neto de tenencias intra-publicas y depositos). La comparacion homogenea seria bruta FMI + BCRA FMI = 173,8% (2023) y 87,5% (2024)
  contra 166,8% y 82,0% propios.

## 7. Participacion de la deuda en pesos

Disponible solo a cierre de diciembre, para 2007-2009 y 2013-2025 (columnas `share_pesos_spnf_dic`, `share_pesos_consolidada_dic`): moneda local (incluye CER) /
total de la misma tabla MECON (A.7 en 2007-09; "por moneda" en 2013+), con el BCRA entero considerado en pesos (los tres instrumentos lo son). Se aplica el share al stock de A.4.5, por lo tanto
es aproximado (+-0,6% por el perimetro de cada tabla). Faltan: 2010-2012 (informes 31/12 no descargados; solo existe el de marzo 2010), 1996-2006
(no descargados informes de esa epoca) y todos los trimestres que no son diciembre (los informes dan la moneda solo a la fecha del informe).
Con los informes faltantes se podria completar; no se interpola.

## 8. Resultados principales (diciembre, % PIB4T)

SPNF / BCRA / consolidada bruta: 1996: 32,9 / 1,4 / 34,3; 2002: 137,8 / 0,7 / 138,6; 2008: 43,8 / 3,9 / 47,8; 2011: 35,3 / 3,6 / 39,0; 2017: 56,0 / 10,3 / 66,3; 2020: 103,0 / 10,3 / 113,3; 2023: 153,5 / 13,3 / 166,8; 2024: 82,1 / -0,06 / 82,0.

## 9. Asuntos abiertos

1. BOPREAL y swap PBoC (y LEFI como pasivo del Tesoro) para alinear con el concepto BCRA del FMI; ids BCRA/IMF por revisar.
2. Pases brutos (ids 152/154) como alternativa al neto 1261; el neto negativo (2001-02, 2024-25) debe discutirse en el texto.
3. Informes MECON 2010-2012 y pre-2007 para share en pesos y para sustituir las 6 observaciones interpoladas de 1996-97.
4. Coeficiente de enlace PIB base 1993/2004 (incertidumbre del nivel pre-2004).
5. `deuda_pib`/`ingesta_bcra_pasivos.py`/`fase8_deuda_consolidada.py` existentes siguen con el denominador viejo y el diccionario manual; no se tocaron.
6. Neteo intra-publico no factible con datos disponibles (solo FMI 2023-26).
