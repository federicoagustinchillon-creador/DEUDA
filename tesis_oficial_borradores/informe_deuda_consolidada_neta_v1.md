# Deuda publica consolidada NETA de Argentina, 1996T1-2025T4 (v1)

Script: `codigo/ingesta_datos/construir_deuda_consolidada_neta_1996_2025.py`.
Datos: `datos/procesados/deuda_consolidada_neta_1996_2025.csv` y `..._control_fmi.csv`.
Figura: `resultados/figuras_borrador/deuda_consolidada_neta_1996_2025.png`.
Reutiliza el denominador y la deuda bruta de `informe_deuda_consolidada_v1.md`.

## 1. Definicion objetivo

FMI, CR 25/95, Annex II, Table 2, y FMI (2021), "Review of the DSF for MACs", Annex II, nota 2: consolidar es netear los
creditos del banco central contra el gobierno y sumar los pasivos de deuda del banco central excluidos moneda y depositos de
residentes.

    D_neta = B - T_BCRA - T_FGS + L_BCRA - DEP          (todo / PIB de los ultimos 4 trimestres)

B = deuda bruta federal; T_BCRA = deuda del Tesoro en poder del BCRA (titulos, Letras Intransferibles, adelantos transitorios);
T_FGS = deuda del Tesoro en poder del FGS-ANSES; L_BCRA = pasivos remunerados del BCRA (pesos: LEBAC/NOBAC, LELIQ/NOTALIQ,
pases; moneda extranjera: LEBAC-USD, LEDIV, BOPREAL, swap PBoC activado); DEP = depositos del Tesoro en el BCRA.

## 2. Componentes: fuente y cobertura

| Componente | Fuente | Cobertura | Estado |
|---|---|---|---|
| B bruta federal | MECON, Informe de Deuda 31/12/2025, hoja A.4.5 (USD) x TC hoja A.2.4; paridad 1:1 hasta 2001 | 1996T1-2025T4; 6 trimestres de 1996-97 interpolados linealmente en USD (bandera `flag_bruta_interpolada`) | completo |
| T_BCRA | BCRA, "Balance del Banco Central" historico, `https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/balbcrhis.xls`, hoja B.C.R.A., col. "Sector oficial - Total" (= pesos: adelantos transitorios + titulos publicos; + moneda extranjera: Letras Intransferibles y titulos en USD). Se valida col12 = col13 + col20 en todos los trimestres | 1996T1-2025T4, mensual, se toma el cierre de trimestre | completo, con desvio de valuacion (ver 3) |
| T_FGS | ANSES, Informe Estadistico Mensual del FGS y Anuarios | NO OBTENIDO | faltante (NaN) |
| L_BCRA pesos | API BCRA v4.0 ids 1258 (LEBAC/NOBAC), 1260 (LELIQ/NOTALIQ), 1261 (pases netos); reuso v1 | 1996-2025; ceros solo antes de la primera observacion de cada serie (1258 desde 2002-03, 1260 desde 2018-01), con bandera | completo |
| L_BCRA moneda extranjera | API BCRA v4.0 id 1259 (LEBAC/LEDIV/BOPREAL en moneda extranjera, valuadas en ARS); en 2023-12 y 2024-12 coincide con id 158 (USD) x TC | 2002-03 a 2025-12; antes de 2002-03 cero con bandera `flag_letras_fx_sin_serie` (24 trimestres; el instrumento no existe, la serie arranca ahi) | parcial: falta swap PBoC |
| Swap PBoC activado | no hay serie publica en API ni en `series.xlsm` (hojas dt, BASE MONETARIA, RESERVAS, DEPOSITOS, PRESTAMOS, TASAS, INSTRUMENTOS DEL BCRA) | -- | faltante (`flag_swap_pboc_faltante`=1 desde 2020) |
| DEP | API BCRA v4.0 id 1264 "Depositos del gobierno en el BCRA" (consistente con la col. "Sector oficial - Depositos" del Balance: 1.002.754 mm ARS en 2023-12) | 1996-2025 | completo |

Denominador: PIB nominal de los ultimos 4 trimestres, INDEC base 2004 empalmada con base 1993 (como v1). Stocks de fin de trimestre.
Nota: el crudo de PIB se leyo del cache local porque `apis.datos.gob.ar` dio timeout en la corrida; son los mismos CSV de v1.

Fuentes bloqueadas: `anses.gob.ar` devuelve HTTP 403 (proteccion anti-bot) a descargas automatizadas, de modo que ningun archivo del FGS
pudo leerse. No se usa ninguna cifra del FGS en el CSV.

## 3. Desvios respecto de la definicion del FMI (con justificacion)

1. **FGS no neteado.** Sin fuente primaria accesible; aproximar sin dato violaria la regla de no inventar. La serie es "neta excepto FGS"
   y es una COTA SUPERIOR de la neta FMI desde 2007T3. Antes (Decreto 897/2007, 13-jul-2007) el FGS no existe como tenedor.
2. **Swap PBoC activado omitido** (sin serie). Subestima L_BCRA en moneda extranjera desde 2020.
3. **Valuacion de T_BCRA a valor contable del BCRA**, no a valor nominal: desde dic-2019 (Ley 27.541, art. 62) las Letras Intransferibles se
   ajustan, y desde 7-may-2024 se valuan a costo amortizado (Res. Directorio 128/24). El FMI usa el stock de deuda del Tesoro. Efecto: tenencia
   BCRA subestimada y neta sobrestimada, cuantia no estimable sin el nominal.
4. **Bruta MECON = Administracion Central, excluida la deuda elegible pendiente de reestructuracion** (A.4.5); el FMI "federal gross" trae
   su propia cobertura. Brecha observada: 153,5 vs 155,4 (2023) y 82,1 vs 85,3 (2024).
5. **Otros tenedores intra-sector publico** (PAMI, organismos, bancos publicos segun cobertura FMI) no se netean: no hay serie trimestral.
6. **Pases en neto** (pasivos menos activos, id 1261): puede ser negativo (2024T4: LC = -0,06%); el FMI informa 0,0.
7. **Moneda de la bruta 1996-2001**: USD x 1 (convertibilidad), sin cambio de unidad.
8. **Deposito del Tesoro en moneda extranjera** incluido a la valuacion del BCRA.

## 4. Control contra el FMI (% PIB)

| Concepto | 2023 nuestro | 2023 FMI | 2024 nuestro | 2024 FMI |
|---|---|---|---|---|
| Bruta federal total (con intra-publico) | 153,5 | 155,4 | 82,1 | 85,3 |
| Intra-publico del Tesoro (aqui solo BCRA) | 48,6 | 62,5 (BCRA+FGS+otros) | 13,2 | 33,9 (idem) |
| Pasivos BCRA total | 14,6 | 18,4 | 1,6 | 2,2 |
|   en moneda local | 13,3 | 16,2 | -0,06 | 0,0 |
|   en moneda extranjera (sin swap) | 1,3 | 2,1 | 1,6 | 2,1 |
| Depositos del Tesoro en el BCRA | 0,52 | 0,5 | 2,10 | 2,1 |
| **Neta consolidada (excepto FGS)** | **119,0** | **110,8** | **68,3** | **51,5** |

Lectura: depositos, pasivos en moneda local y la bruta replican al FMI dentro de 0,0-3 puntos. Los desvios grandes estan en el intra-publico (brecha de
14,0 puntos en 2023 y 20,7 en 2024) y se traducen directo en la neta (+8,2 y +16,8 puntos). La brecha de 2024 supera con holgura lo que
explicaria el FGS y apunta a valuacion (desvio 3) y a otros tenedores; no puede cerrarse con los datos disponibles.
Cifras del FGS mencionadas por un buscador (Titulos Publicos Nacionales del FGS 28,47 y 56,63 billones de ARS a dic-2023 y dic-2024, Anuario 2024
de ANSES) NO fueron verificadas contra el archivo primario y no se usan en el CSV; son solo una pista del orden de magnitud (aproximadamente 14-15% y 9-10% del PIB).

## 5. Periodo comparable y recomendacion

- **Plenamente comparable con la definicion del FMI: ningun periodo.** Para 2007T3-2025T4 falta el FGS (y desde 2020 el swap PBoC); la unica
  validacion contra el FMI (2023, 2024) falla por 8 y 17 puntos.
- **1996T1-2007T2 (46 trimestres) tiene todos los componentes disponibles** (FGS inexistente, sin swap) y es el unico tramo "completo"
  (`comparable_fmi`=1), pero no hay control FMI para esos anios y la neta se aparta poco de la bruta (BCRA tenia 2-3% del PIB de credito al Tesoro).
- **Recomendacion para la muestra de estimacion 1996-2025:** usar como serie principal la deuda bruta federal o la consolidada bruta (v1), que es
  homogenea, completa y verificable en todo el periodo, y presentar la neta (excepto FGS) como serie de robustez, con la advertencia explicita
  de que es una cota superior de la neta del FMI y de que su nivel en 2023-2025 esta contaminado por la valuacion contable de las Letras
  Intransferibles. No presentarla como "la deuda neta del FMI". Para cerrar la brecha hacen falta: (i) las series FGS de ANSES (descarga manual del
  Informe Estadistico Mensual/Anuarios; ANSES bloquea scripts), (ii) el stock nominal de Letras Intransferibles/adelantos (MECON, informe trimestral
  por tenedor), (iii) el saldo del swap PBoC activado (Estados Contables del BCRA).

## 6. Reproduccion

`python codigo/ingesta_datos/construir_deuda_consolidada_neta_1996_2025.py`. Descarga `balbcrhis.xls` a `datos/crudos/deuda_consolidada_neta/`
(cache), consulta la API BCRA v4.0 y reutiliza `construir_deuda_consolidada_1996_2025.py`. No sobreescribe salidas previas. Banderas en el CSV:
`flag_fgs_faltante`, `flag_fgs_fondo_inexistente`, `flag_swap_pboc_faltante`, `flag_bruta_interpolada`, `flag_letras_fx_sin_serie`,
`flag_tenencia_bcra_faltante`, `flag_pases_neto_negativo`, `comparable_fmi`.
