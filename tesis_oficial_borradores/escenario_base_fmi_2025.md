# Escenario base del FMI para Argentina (Country Report No. 25/95, abril 2025)

**Fuente:** IMF (2025), *Argentina: Request for an Extended Arrangement under the Extended Fund Facility*, IMF Country Report No. 25/95, abril de 2025. Archivo local: `Bibliografia/descargas_verificacion/1argea2025002-print-pdf.pdf` (138 páginas).

**Uso previsto:** escenario base citable para la simulación Monte Carlo de deuda de la tesis y punto de comparación con el fanchart del propio FMI (probabilidad de estabilización de la deuda en torno a 97 %, Anexo II, párrafos 6 y 8).

**Serie numérica en formato largo:** `datos/procesados/escenario_base_fmi_cr2595.csv` (columnas `variable, anio, valor, unidad, pagina, cuadro, estado`; 779 filas).

## Convenciones de esta nota

- **Páginas:** "p. NN" es la página del PDF (1 a 138). La numeración impresa del informe es la del PDF menos 3 (por ejemplo, PDF p. 49 corresponde a la página impresa 46).
- **Celdas vacías ("—"):** el informe no publica el dato. No se estima ni se completa ningún valor faltante.
- **2023 y 2024** son datos observados o estimaciones del staff. Las proyecciones arrancan en 2025.
- Los valores se transcribieron de la extracción de texto del PDF (pypdf; PyMuPDF para el Cuadro 7 del Anexo II) y se controlaron con las identidades del propio cuadro. Por ejemplo, en el Cuadro 6 del Anexo II el cambio de la deuda es igual a los flujos identificados más el residuo: 2025 = −13,8 + 1,6 = −12,2.

### Convenciones de denominador y perímetro (notas al pie)

| Tema | Lo que dice el informe | Fuente |
|---|---|---|
| Denominador del ratio deuda/PIB | "Debt-to-GDP ratio is based on average period GDP." La deuda se valúa al tipo de cambio de fin de período. | p. 68, Anexo II Cuadro 2, nota 1/ |
| Ratio alternativo | El Cuadro 4 publica además la deuda federal sobre el **PIB del cuarto trimestre anualizado**. Para 2030 informa 53,1, contra 40,6 en 2029: es un salto anómalo que se reproduce tal cual, sin corregir. | p. 53, Cuadro 4 |
| Deuda en moneda local | "Local currency debt assessed at end of period exchange rate." | p. 56, Cuadro 6, nota 1/ |
| Perímetro del DSA (SRDSF) | Deuda bruta del gobierno central (federal) en manos del sector privado, del sector oficial y del sector público. Excluye las provincias y municipios, la deuda del BCRA, los cupones PBI y el swap bilateral del BCRA (por debajo del umbral de 1 % del PIB). Solo incluye al "budgetary central government". | p. 73, Anexo II Cuadro 3 |
| Stock de deuda | Es mayor que el de los informes mensuales del MEcon porque incluye i) los intereses capitalizados hasta el vencimiento, ii) los holdouts y iii) el fallo de Londres sobre los cupones PBI. | p. 68, Anexo II Cuadro 2, nota 1/ |
| Resultado primario federal | Excluye las transferencias de utilidades del BCRA (p. 49, Cuadro 1, nota 5/). Los intereses excluyen los cupones de los bonos cupón cero emitidos antes de 2025, que se registran "below the line" (p. 52, Cuadro 3b, nota 5/). | p. 49 y p. 52 |
| Perímetro "federal government" del programa | Sector Público Nacional No Financiero: administración central, instituciones de seguridad social, organismos descentralizados, PAMI, fondos fiduciarios y otros entes y empresas del gobierno federal. Base caja, "Esquema IMIG". | p. 99, MTE/TMU párr. 4–5 |
| Deuda neta de tenencias públicas | "Gross federal debt, net of debt held by BCRA and FGS." | p. 53, Cuadro 4, nota 7/ |
| Deuda federal en Cuadro 3b | "Includes federal debt held by the BCRA and FGS." | p. 52, Cuadro 3b, nota 11/ |

## 1. Supuestos macroeconómicos

| Variable | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| PIB real, var. % | -1,6 | -1,7 | 5,5 | 4,5 | 4,0 | 3,2 | 3,1 | 3,0 | p. 49, Cuadro 1 |
| Brecha del producto (% PIB potencial) | -0,8 | -4,9 | -2,7 | -1,2 | -0,3 | -0,1 | 0,0 | 0,0 | p. 49, Cuadro 1 |
| Inflación IPC, fin de período, % | 211,4 | 117,8 | [18–23] | [10–15] | 7,5 | 7,5 | 7,5 | 7,5 | p. 49, Cuadro 1 |
| Inflación IPC, promedio, % | 133,5 | 219,9 | [33–38] | [12–17] | 9,4 | 7,5 | 7,5 | 7,5 | p. 49, Cuadro 1 |
| PIB nominal, US$ miles de millones | 236,7 | 561,0 | 632,9 | 671,5 | 681,6 | 685,1 | 721,4 | 759,0 | p. 56, Cuadro 6 |
| Cuenta corriente (% PIB) | -3,2 | 1,0 | -0,4 | -0,3 | 0,2 | 0,6 | 1,1 | 1,2 | p. 49, Cuadro 1 |
| Reservas brutas (US$ miles de millones) | 10,1 | 16,6 | 36,3 | 44,6 | 54,3 | 65,3 | 77,0 | 89,0 | p. 49, Cuadro 1 |

- **Inflación 2025–2026.** El informe publica solo rangos, entre corchetes. En el CSV se cargan como límites inferior y superior (`*_rango_inf`, `*_rango_sup`), sin calcular un punto medio. El Recuadro 1 del Anexo II (p. 71) dice que la inflación anual llegaría a un dígito en 2027.
- **PIB nominal en pesos.** El informe no lo publica en forma directa. Podría deducirse dividiendo el Cuadro 3a (ARS) por el Cuadro 3b (% PIB), pero acá no se hace.
- **Horizonte extendido 2031–2035.** Solo figura en el Cuadro 6 del Anexo II (sección 4): crecimiento real de 3,0 % y deflactor del PIB de 7,5 % todos los años.

## 2. Resultado fiscal

### 2a. Gobierno federal (SPNNF, base caja, % del PIB)

| Variable | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| Ingresos | 16,7 | 16,9 | 16,8 | 17,3 | 17,4 | 17,4 | 17,4 | 17,4 | p. 52, Cuadro 3b |
| Gasto primario | 19,6 | 15,1 | 15,4 | 15,1 | 14,9 | 14,9 | 14,9 | 14,9 | p. 52, Cuadro 3b |
| **Resultado primario** | -2,8 | 1,8 | 1,3 | 2,2 | 2,5 | 2,5 | 2,5 | 2,5 | p. 52, Cuadro 3b (= p. 49, Cuadro 1) |
| Intereses (caja) | 2,2 | 1,5 | 1,3 | 2,2 | 2,0 | 2,1 | 2,1 | 2,1 | p. 52, Cuadro 3b |
| **Resultado global** | -5,1 | 0,3 | 0,0 | 0,0 | 0,4 | 0,4 | 0,4 | 0,4 | p. 52, Cuadro 3b |
| Resultado primario estructural (% PIB potencial) | -3,2 | 2,5 | 1,9 | 2,5 | 2,6 | 2,5 | 2,5 | 2,5 | p. 52, Cuadro 3b |

Los mismos conceptos en ARS miles de millones están en la p. 51 (Cuadro 3a) y se cargaron en el CSV. Resultado primario: −5.440 / 10.496 / 10.520 / 20.980 / 26.958 / 30.360 / 33.420 / 37.060.

### 2b. Gobierno general y sector público consolidado (% del PIB)

| Variable | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| Resultado primario del gobierno general (federal + provincias) | -2,8 | 2,5 | 1,8 | 3,7 | 3,9 | 3,9 | 3,7 | 3,7 | p. 53, Cuadro 4 |
| de ello: provincias | 0,0 | 0,7 | 0,5 | 1,5 | 1,4 | 1,3 | 1,2 | 1,1 | p. 53, Cuadro 4 |
| Resultado global del gobierno general | -5,4 | 0,9 | 0,4 | 1,4 | 1,8 | 1,7 | 1,6 | 1,5 | p. 53, Cuadro 4 |
| Resultado del sector público consolidado (federal + provincias + cuasifiscal BCRA) | -13,7 | -0,7 | 1,0 | 1,9 | 2,2 | 2,2 | 2,1 | 2,1 | p. 53, Cuadro 4, nota 6/ |
| Costo cuasifiscal del BCRA | 8,4 | 1,6 | -0,5 | -0,5 | -0,5 | -0,5 | -0,5 | -0,6 | p. 49, Cuadro 1 |

El informe no presenta un resultado del SPNF que agregue las empresas públicas con un perímetro distinto del SPNNF federal. El Cuadro 4 agrega solo federal y provincias.

### 2c. Resultado primario en el DSA (SRDSF)

El Cuadro 6 del Anexo II (p. 76) usa el "primary deficit" del perímetro federal: −1,8 (2024), −1,3, −2,2, y −2,5 todos los años entre 2027 y 2035 (signo negativo = superávit). Las líneas de ingresos y gastos sin intereses de ese cuadro (24,2 a 27,0 y 22,4 a 24,5 % del PIB) tienen otra escala que el Cuadro 3b. El informe no explica esa diferencia de cobertura; se reportan tal cual.

## 3. Deuda pública

### 3a. Deuda federal (Cuadros 3b, 4 y 6 del informe principal)

| Variable | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| **Deuda federal bruta (perímetro DSA), % PIB** | 155,4 | 85,3 | 73,1 | 68,2 | 65,1 | 63,3 | 59,3 | 55,7 | p. 52, Cuadro 3b; p. 56, Cuadro 6 |
| Deuda federal bruta, US$ miles de millones | 367,9 | 478,7 | 462,6 | 458,2 | 444,0 | 433,9 | 428,0 | 422,5 | p. 56, Cuadro 6 |
| Acreedores oficiales | 33,3 | 13,8 | 15,2 | 14,7 | 14,4 | 13,8 | 12,4 | 10,5 | p. 52, Cuadro 3b |
| Sector privado | 59,6 | 37,6 | 29,0 | 24,6 | 22,9 | 21,7 | 19,9 | 18,6 | p. 52, Cuadro 3b |
| de ello: en moneda extranjera | 40,1 | 17,1 | 14,2 | 13,6 | 13,5 | 13,3 | 12,6 | 12,1 | p. 52, Cuadro 3b |
| Entidades públicas (BCRA, FGS) | 62,5 | 33,9 | 28,9 | 28,9 | 27,9 | 27,8 | 27,0 | 26,5 | p. 52, Cuadro 3b |
| **Deuda federal neta de tenencias del BCRA y el FGS** | 92,9 | 51,4 | 44,2 | 39,4 | 37,2 | 35,6 | 32,3 | 29,2 | p. 53, Cuadro 4 |
| Deuda federal / PIB Q4 anualizado | 105,4 | 71,1 | 53,9 | 47,8 | 44,6 | 43,1 | 40,6 | 53,1 | p. 53, Cuadro 4 |
| Deuda federal + títulos del BCRA | 171,6 | 87,0 | 74,5 | 69,3 | 65,2 | 63,4 | 59,3 | 55,7 | p. 56, Cuadro 6 |
| Deuda federal en moneda local | 44,5 | 39,5 | 31,4 | 28,2 | 25,4 | 23,9 | 22,0 | 24,9 | p. 56, Cuadro 6 |
| Deuda federal en moneda extranjera | 110,9 | 45,8 | 41,7 | 40,0 | 39,8 | 39,4 | 37,3 | 30,8 | p. 56, Cuadro 6 |
| Deuda provincial | 9,3 | 3,1 | 2,2 | 1,3 | 1,0 | 0,8 | 0,7 | 1,1 | p. 53, Cuadro 4 |
| Títulos del BCRA | 16,2 | 1,7 | 1,4 | 1,0 | 0,0 | 0,0 | 0,0 | 0,0 | p. 53, Cuadro 4 |

**Participación de la moneda extranjera en la deuda federal bruta.** El informe no la publica como porcentaje. La cuenta aritmética sobre los US$ del Cuadro 6 (p. 56) da 71,4 / 53,7 / 57,0 / 58,7 / 61,1 / 62,2 / 62,9 / 55,4 % para 2023–2030. Es un derivado, no una cifra del FMI, y por eso no está en el CSV. Entre 2029 y 2030 la deuda en moneda local salta de 22,0 a 24,9 % del PIB y la de moneda extranjera cae de 37,3 a 30,8 %. Así figura en la fuente, que no lo explica.

### 3b. Deuda neta consolidada incluido el BCRA (Anexo II, Cuadro 2, p. 68; solo 2023–2026)

| Concepto | 2023 | 2024 | 2025 | 2026 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| | US$ mm | US$ mm | US$ mm | US$ mm | % PIB | % PIB | % PIB | % PIB |
| 1. Deuda federal bruta (perímetro DSA) | 367,9 | 478,7 | 462,6 | 458,2 | 155,4 | 85,3 | 73,1 | 68,2 |
| 2. Deuda federal sin tenencias intra-sector público | 220,0 | 288,6 | 279,7 | 264,3 | 92,9 | 51,4 | 44,2 | 39,4 |
| 2a. en moneda extranjera | 173,8 | 173,4 | 186,6 | 190,5 | 73,4 | 30,9 | 29,5 | 28,4 |
| FMI | 40,6 | 40,6 | 55,7 | 56,1 | 17,1 | 7,2 | 8,8 | 8,3 |
| Sector oficial | 38,3 | 37,0 | 40,7 | 42,8 | 16,2 | 6,6 | 6,4 | 6,4 |
| Sector privado | 92,5 | 91,8 | 86,1 | 87,7 | 39,1 | 16,4 | 13,6 | 13,1 |
| Holdouts y litigios firmes | 2,4 | 4,0 | 4,0 | 4,0 | 1,0 | 0,7 | 0,6 | 0,6 |
| 2b. en moneda local | 46,2 | 115,3 | 93,2 | 73,8 | 19,5 | 20,5 | 14,7 | 11,0 |
| 3. Deuda del Tesoro intra-sector público (BCRA, FGS) | 147,9 | 190,1 | 182,9 | 193,8 | 62,5 | 33,9 | 28,9 | 28,9 |
| 4. Pasivos del BCRA (BOPREAL, swap PBoC, otros) | 43,5 | 12,3 | 11,7 | 9,7 | 18,4 | 2,2 | 1,8 | 1,4 |
| 4a. en moneda extranjera | 5,1 | 12,0 | 11,6 | 9,6 | 2,1 | 2,1 | 1,8 | 1,4 |
| 4b. en moneda local | 38,4 | 0,3 | 0,1 | 0,0 | 16,2 | 0,0 | 0,0 | 0,0 |
| 5. Depósitos del Tesoro en el BCRA | 1,2 | 11,9 | 11,9 | 11,9 | 0,5 | 2,1 | 1,9 | 1,8 |
| **6. Deuda neta consolidada del sector público (2 + 4 − 5)** | 262,2 | 289,0 | 279,5 | 262,1 | **110,8** | **51,5** | **44,2** | **39,0** |
| 6b. Deuda neta consolidada en moneda local (2b + 4b − 5) | 83,3 | 103,6 | 81,3 | 62,0 | 35,2 | 18,5 | 12,9 | 9,2 |

- El informe no publica la deuda neta consolidada para 2027–2030. No se extrapola.
- El párrafo 3 del Anexo II (p. 68) da "52 percent of GDP at end-2024" para la deuda neta consolidada, contra 51,5 en el Cuadro 2. Es una diferencia de redondeo en el texto.
- La nota 2 (p. 67) indica que el DSA supone la recompra a valor nominal de las Letras Intransferibles en ME en poder del BCRA que vencen en 2025 (US$ 11 mil millones).

### 3c. Tasa de interés efectiva implícita (Anexo II, Cuadro 6, p. 76)

| | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tasa efectiva, % | 3,4 | 2,4 | 4,1 | 3,9 | 4,0 | 4,0 | 4,1 | 4,0 | 4,0 | 4,1 | 4,2 | 3,9 |

Según el comentario del cuadro, la baja de 2025 refleja las colocaciones a mayor plazo y menor rendimiento y los bonos cupón cero. El aumento posterior acompaña la salida de los controles cambiarios. En la sección 5 (Recuadro 1, p. 72) está la tasa real de las colocaciones en pesos.

## 4. Descomposición de la dinámica de la deuda (Anexo II, Cuadro 6 "Baseline Scenario", p. 76)

Perímetro: deuda federal bruta. Unidades: % del PIB o puntos porcentuales del PIB. 2024 es dato observado, 2025–2030 es la proyección de mediano plazo y 2031–2035 la proyección extendida.

| Concepto | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Deuda pública** | 85,3 | 73,1 | 68,2 | 65,1 | 63,3 | 59,3 | 55,7 | 52,0 | 48,5 | 45,1 | 41,8 | 38,2 |
| Cambio en la deuda | -70,1 | -12,2 | -4,9 | -3,1 | -1,8 | -4,0 | -3,7 | -3,6 | -3,5 | -3,4 | -3,3 | -3,6 |
| Flujos identificados | -26,3 | -13,8 | -7,4 | -5,8 | -4,6 | -4,5 | -4,2 | -4,1 | -4,0 | -3,9 | -3,8 | -3,8 |
| Déficit primario | -1,8 | -1,3 | -2,2 | -2,5 | -2,5 | -2,5 | -2,5 | -2,5 | -2,5 | -2,5 | -2,5 | -2,5 |
| Ingresos sin intereses | 24,2 | 25,3 | 26,9 | 27,0 | 27,1 | 27,0 | 27,0 | 27,0 | 27,0 | 27,0 | 27,0 | 27,0 |
| Gastos sin intereses | 22,4 | 24,0 | 24,7 | 24,5 | 24,6 | 24,5 | 24,5 | 24,5 | 24,5 | 24,5 | 24,5 | 24,5 |
| Dinámica automática | -24,5 | -12,5 | -5,2 | -3,3 | -2,1 | -2,0 | -1,7 | -1,6 | -1,5 | -1,4 | -1,3 | -1,3 |
| Tasa real e inflación relativa | -30,8 | -8,0 | -2,0 | -0,7 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | -0,1 |
| Tasa de interés real | -104,2 | -17,4 | -6,3 | -3,3 | -2,0 | -2,0 | -1,8 | -1,8 | -1,6 | -1,5 | -1,4 | -1,3 |
| Inflación relativa | 73,4 | 9,3 | 4,3 | 2,6 | 2,0 | 2,0 | 1,9 | 1,7 | 1,6 | 1,5 | 1,4 | 1,3 |
| Crecimiento real | 2,7 | -4,5 | -3,2 | -2,6 | -2,0 | -1,9 | -1,7 | -1,6 | -1,5 | -1,4 | -1,3 | -1,2 |
| Tipo de cambio real | 3,7 | — | — | — | — | — | — | — | — | — | — | — |
| Otros flujos identificados | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| Residuo | -43,8 | 1,6 | 2,5 | 2,7 | 2,8 | 0,5 | 0,5 | 0,5 | 0,5 | 0,5 | 0,5 | 0,2 |
| Necesidades brutas de financiamiento (GFN) | 19,6 | 17,3 | 12,1 | 14,3 | 10,8 | 14,1 | 9,7 | 13,0 | 10,5 | 11,3 | 9,2 | 9,0 |
| de ello: servicio de deuda | 21,4 | 18,6 | 14,3 | 16,8 | 13,4 | 16,6 | 12,2 | 15,5 | 13,0 | 13,8 | 11,7 | 11,5 |
| moneda local | 16,3 | 14,4 | 10,2 | 12,4 | 8,0 | 9,7 | 6,7 | 7,9 | 5,9 | 7,1 | 5,2 | 1,2 |
| moneda extranjera | 5,1 | 4,2 | 4,1 | 4,4 | 5,4 | 7,0 | 5,5 | 7,6 | 7,0 | 6,7 | 6,4 | 5,7 |
| *Memo:* PIB real, var. % | -1,7 | 5,5 | 4,5 | 4,0 | 3,2 | 3,1 | 3,0 | 3,0 | 3,0 | 3,0 | 3,0 | 3,0 |
| *Memo:* deflactor del PIB, var. % | 206,3 | 30,4 | 14,5 | 9,4 | 7,5 | 7,5 | 7,5 | 7,5 | 7,5 | 7,5 | 7,5 | 7,5 |
| *Memo:* PIB nominal, var. % | 202,6 | 37,3 | 19,7 | 13,7 | 10,9 | 10,9 | 10,7 | 10,7 | 10,7 | 10,7 | 10,7 | 10,7 |
| *Memo:* tasa de interés efectiva, % | 3,4 | 2,4 | 4,1 | 3,9 | 4,0 | 4,0 | 4,1 | 4,0 | 4,0 | 4,1 | 4,2 | 3,9 |

- **Tipo de cambio real.** El cuadro solo informa la contribución de 2024. Para 2025–2035 muestra "…": no hay contribución cambiaria separada en la proyección.
- **Residuo.** Es grande en 2024–2028 (+1,6 a +2,8 pp por año). Según el comentario del cuadro, los residuos de 2024–25 son ajustes stock-flujo por la diferencia entre el tipo de cambio de fin de período y el promedio. El informe no explica los de 2026–2028.
- **Uso en la simulación.** Para reproducir la trayectoria del FMI hay que incorporar ese residuo como un flujo exógeno. Si no, la identidad deuda-dinámica da una caída más rápida que la publicada.

## 5. Supuestos de financiamiento, tipo de cambio y condiciones globales

### Supuestos de financiamiento (Anexo II, Recuadro 1, "Key DSA Financing Assumptions", p. 72)

| Variable | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|---|
| Oficial (sin FMI): desembolsos, US$ mm | 6,7 | 5,0 | 5,0 | 5,0 | 5,0 | 5,0 |
| Oficial (sin FMI): financiamiento neto, US$ mm | 4,3 | 2,0 | 2,1 | 2,0 | 2,0 | 2,0 |
| Oficial: tasa nominal, % | 3,9 | 3,8 | 3,8 | 3,8 | 3,8 | 3,8 |
| Mercados internacionales: emisión, US$ mm | 0,0 | 4,0 | 5,0 | 5,0 | 6,0 | 6,0 |
| Mercados internacionales: spread, pb | 550 | 500 | 450 | 450 | 450 | 450 |
| Plazo / gracia, años | 7 / 4 | 7 / 4 | 7 / 4 | 7 / 4 | 7 / 4 | 7 / 4 |
| Pesos: corto plazo a tasa fija, % de la emisión | 50 | 50 | 30 | 30 | 30 | 30 |
| Pesos: CER, % | 50 | 40 | 40 | 20 | 20 | 20 |
| Pesos: largo plazo a tasa fija, % | 0 | 10 | 30 | 50 | 50 | 50 |
| Pesos: tasa de interés real, % | 4,0 | 4,0 | 4,7 | 5,0 | 5,4 | 5,6 |

El texto del Recuadro 1 (p. 72) dice que Argentina volvería a los mercados con spreads de 400–500 pb ("in line with some Argentine corporates"). También dice que la tasa real interna sube gradualmente a 5½ % en 2029.

### Tipo de cambio

- **Trayectoria nominal.** El informe no publica una trayectoria proyectada del tipo de cambio nominal ARS/US$ ni un índice proyectado del TCRM. No se completa.
- **Referencia del programa.** El tipo de cambio del programa es de 1.053,50 ARS por US$, el del BCRA al 31-ene-2025 (p. 99, MTE/TMU, Cuadro 1 "Program Exchange Rates"). Se usa para medir las metas, no es una proyección.
- **Supuesto del SRDSF.** "The REER is projected to gradually converge to a level consistent with medium-term fundamentals over the medium term, in the context of greater FX flexibility" (p. 71, Anexo II Recuadro 1).
- **Brecha del TCRM.** El Anexo I estima una brecha del TCRM de entre 15 y 25 % (sobrevaluación) respecto del primer trimestre de 2025, con "exceptionally high uncertainty" (p. 65, Anexo I, sección "Real Exchange Rate").
- **Nuevo régimen.** Flotación dentro de una banda cambiaria "sufficiently wide", con compras de divisas dentro de la banda (p. 22, párr. 24).

### Tasa de interés de EE. UU. y condiciones financieras globales

- **No hay supuesto explícito.** No se encontró un supuesto numérico sobre la tasa de EE. UU. (Fed, UST, SOFR) en el escenario base. Las búsquedas de "U.S. Treasury", "SOFR", "federal funds" y "US interest" no dieron resultados pertinentes. El costo externo se expresa solo como spread en pb (p. 72) y como tasa nominal oficial de 3,8–3,9 % (p. 72).
- **Las condiciones globales aparecen como riesgo a la baja, no como supuesto.** Las tensiones comerciales podrían llevar a "tighter global financial conditions and lower commodity prices" (p. 6, Executive Summary; p. 16, párr. 16; p. 91, MEFP párr. 13).

## 6. Resultados del SRDSF: fanchart, GFN e índice de mediano plazo

### Evaluación de riesgo (Anexo II, Cuadro 1, p. 66)

| Horizonte | Señal mecánica | Evaluación final |
|---|---|---|
| General | … | Alto |
| Corto plazo | n.a. | n.a. |
| Mediano plazo | Moderado | Moderado |
| Fanchart | Moderado | … |
| GFN | Moderado | … |
| Largo plazo | … | Alto |
| Sostenibilidad | — | "Sustainable but not with high probability" |
| ¿Estabilización de la deuda en el escenario base? | Sí | |

### Fanchart de mediano plazo, 2025–2030 (Anexo II, Cuadro 7, p. 77)

| Indicador | Valor | Contribución al índice | Fuente |
|---|---|---|---|
| Ancho del fanchart (pp del PIB) | 74,2 | 1,1 | p. 77, Cuadro 7 |
| Probabilidad de **no** estabilización de la deuda (%) | 3,0 | 0,0 | p. 77, Cuadro 7 |
| Deuda terminal/PIB × índice de instituciones | 40,4 | 0,9 | p. 77, Cuadro 7 |
| **Debt Fanchart Index (DFI)** | **2,0** | | p. 77, Cuadro 7 |
| Señal de riesgo | Moderado (umbrales: bajo si DFI < 1,13; alto si DFI > 2,08) | | p. 77, Cuadro 7, nota 3/ |
| Probabilidad de estabilización (texto) | "around 97 percent" | | p. 70, Anexo II párr. 6 |

- El DFI de 2,0 queda apenas debajo del umbral de riesgo alto (2,08).
- Los percentiles del fanchart (bandas 5–25, 25–50, 50–75 y 75–95) solo están en el gráfico, sin valores numéricos. No se transcriben.

### Módulo GFN (Anexo II, Cuadro 7, p. 77)

| Indicador | Valor | Contribución |
|---|---|---|
| GFN promedio del escenario base (% PIB) | 13,1 | 4,5 |
| Tenencia inicial de los bancos frente al gobierno general (% de los activos bancarios) | 30,1 | 9,8 |
| Cambio de esa tenencia en el escenario de estrés (% de los activos bancarios) | 9,1 | 3,1 |
| **GFN Financeability Index (GFI)** | **17,3** | |
| Señal | Moderado (bajo < 7,6; alto > 17,9) | |

Texto complementario:

- El GFN del escenario base promedia alrededor de 13 % del PIB en 2025–30 y alrededor de 9 % para la deuda en manos del sector privado y oficial (p. 69, Anexo II párr. 5).
- El GFN de la deuda que no está en manos de otras entidades públicas rondaría 5 % del PIB en 2025–2032 (p. 71, párr. 9).

### Índice de mediano plazo (Anexo II, Cuadro 7, p. 77)

| Componente | Valor | Valor normalizado | Ponderación | Contribución |
|---|---|---|---|---|
| Debt fanchart index | 2,0 | 0,4 | 0,5 | 0,2 |
| GFN financeability index | 17,3 | 0,3 | 0,5 | 0,2 |
| **Medium-term index** | | | | **0,4** |
| Señal | Moderado (bajo < 0,26; alto > 0,40) | | | |
| Evaluación final | Moderado | | | |
| Probabilidad de crisis no anticipada, 2025–2030 | 27,3 % | | | |
| Probabilidad de falsa alarma, 2025–2030 | 10,2 % | | | |

Estos valores se tomaron de la extracción posicional del texto (PyMuPDF), con un decimal, tal como los imprime el informe.

### Fanchart a 10 años, hasta 2034 (Anexo II, párr. 8, p. 70)

- "The probability of debt stabilization in a fan chart ending in 2034 is close to 97 percent, consistent with debt sustainability, although with substantial risks."
- El informe **no publica** el ancho del fanchart, el DFI ni los percentiles de la versión a 10 años. Quedan en blanco.

### Otros datos relevantes del Anexo II

- **Intereses.** Pasan de 1,3 % del PIB en 2025 a alrededor de 2,1 % en promedio en 2026–30 (p. 68–69, párr. 4).
- **Intereses capitalizados.** Alrededor de 40 % de la deuda en pesos capitaliza intereses, que se registran "below the line". En 2025 equivalen a cerca de 1,6 % del PIB (p. 69, nota 3).
- **Pasivo contingente.** El escenario ilustrativo es un shock único de 6 % del PIB, equivalente a la deuda provincial o a los litigios. La dinámica queda "very close to the baseline" (p. 70, párr. 7).
- **Umbral de 40 %.** La deuda federal sin tenencias del BCRA y el FGS caería por debajo del umbral de 40 % del PIB de la Nota Técnica de marzo de 2020 (p. 71, párr. 9). En el Cuadro 4 ocurre en 2026 (39,4).
- **Realismo del escenario base.** El análisis de realismo señala optimismo en la reducción de la deuda y en la trayectoria cambiaria: la reducción a 3 años está en el percentil 93,6 de la muestra (p. 75, Anexo II Cuadro 5).

## 7. Vacíos (no publicados en CR 25/95)

- PIB nominal en pesos.
- Trayectoria proyectada del tipo de cambio nominal y del TCRM.
- Deuda neta consolidada con BCRA para 2027–2030.
- Participación de la moneda extranjera en la deuda como porcentaje publicado (solo hay un derivado aritmético, en la sección 3a).
- Contribución cambiaria en la descomposición para 2025–2035.
- Percentiles numéricos del fanchart.
- Métricas del fanchart a 10 años, salvo la probabilidad (~97 %).
- Supuesto explícito sobre la tasa de EE. UU.
- Inflación IPC puntual para 2025–2026 (solo hay rangos).
