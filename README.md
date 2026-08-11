# Sostenibilidad de la Deuda Pública Consolidada Argentina (2004–2025)

[![Licencia](https://img.shields.io/badge/Licencia-CC--BY--4.0-blue.svg)](https.creativecommons.org/licenses/by/4.0/)
[![Python](https.img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LaTeX](https://img.shields.io/badge/LaTeX-MiKTeX%20%7C%20TeXLive-green.svg)](https://www.tug.org/texlive/)
[![Estado](https://img.shields.io/badge/Auditor%C3%ADa-Aprobada-success.svg)](#)

Repositorio y código fuente de la investigación econométrica y tesis de grado: **"La solvencia intertemporal de la deuda pública consolidada argentina post-2025: proyecciones a partir de sus determinantes macroeconómicos (2004–2025)"**, desarrollada en la Facultad de Ciencias Económicas de la Universidad Nacional de Cuyo (UNCuyo).

---

## 0. Guía Rápida: qué mirar primero y en qué orden

**¿Solo querés leer la tesis?** → [`tesis/fuente/Tesis.pdf`](tesis/fuente/Tesis.pdf). No hace falta tocar nada más.

**¿Querés editar el texto de un capítulo?** → [`tesis/capitulos/`](tesis/capitulos/), un `.tex` por capítulo (`00_abstract`, `01_introduccion`, ..., `09_apendice`). Después de editar, compilar según el paso 4 de la sección 3.

**¿Querés ver de dónde sale un número que aparece en la tesis?** → Tres pasos:
1. Buscá el script que lo generó en la tabla del [Apéndice, Sección "Estructura de la Cadena de Procesamiento de Código"](tesis/capitulos/09_apendice.tex) — ahí está mapeado cada resultado a su script.
2. El script vive en [`codigo/modelos/faseN_*.py`](codigo/modelos/) (`N` = número de etapa).
3. Su salida (tabla/número) queda en [`resultados/tablas/faseN_*.csv`](resultados/tablas/).

**¿Querés re-correr todo el pipeline desde cero?** → Sección 3 de este README, en orden: entorno virtual → ingesta de datos → fases econométricas → compilar LaTeX.

**¿Querés entender la bibliografía?** → [`Bibliografia/`](Bibliografia/): `marco_legal/` (leyes citadas), `descargas_verificacion/` (papers descargados con verificación de que existen y dicen lo que la tesis les atribuye), `busqueda_literatura_refutacion/` (búsqueda activa de trabajos que contradigan los hallazgos, con veredicto).

**¿Buscás versiones anteriores o el historial de decisiones metodológicas?** → [`historial_proyecto/`](historial_proyecto/).

**Ramas de git**: `main` conserva la versión original de la tesis (DOLS como técnica de referencia, ventana 2004-2025) como respaldo. `revision-var-vecm` es la versión vigente (VECM como técnica de referencia sobre ventana ampliada 1999-2025, DOLS como robustez) — es la que hay que mirar salvo que se busque explícitamente el original.

**Carpetas que NO son parte de la tesis** (para no perder tiempo buscando ahí): `_material_cursada_NO_es_parte_de_la_tesis/` es material de la cursada (consignas de TP, no insumo de la investigación) — el prefijo `_` es a propósito, para que no se confunda con las carpetas de la investigación.

**Dentro de `Bibliografia/`**: `descargas_verificacion/` tiene los PDFs de los papers efectivamente citados. `auditorias/` tiene los informes de verificación (qué se chequeó de cada cita, y la búsqueda de literatura que pudiera refutar el trabajo). `marco_legal/` tiene las leyes citadas. `material_metodologico_catedra/` es bibliografía metodológica de referencia (Marradi, plantilla de DSA).

**Un solo PDF de la tesis, sin ambigüedad**: `tesis/fuente/Tesis.pdf` es el único PDF de la tesis en el repositorio (se eliminó una copia duplicada y desactualizada que había quedado suelta en `tesis/`).

---

## 1. Resumen Ejecutivo

Este proyecto evalúa empíricamente la sostenibilidad fiscal e intertemporal de la deuda pública soberana de la República Argentina, sobre dos ventanas muestrales: la original, 2004T1–2025T4 ($n=88$), y una ampliada por empalme histórico, 1999T1–2025T4 ($n=108$). Se extiende la metodología econométrica tradicional mediante tres contribuciones centrales:

1. **Consolidación del Sector Público**: Integración de la deuda del Sector Público No Financiero (SPNF) con los pasivos monetarios y remunerados (LELIQ, NOTALIQ y Pases Pasivos) del Banco Central de la República Argentina (BCRA).
2. **VECM como técnica de referencia**: Estimación de la Función de Reacción Fiscal de Bohn (1998) mediante un Modelo de Vectores con Corrección de Error (VECM) sobre la ventana ampliada, que trata la endogeneidad del sistema completo (deuda, resultado primario, riesgo soberano, tipo de cambio) de forma estructural. DOLS con corrección IV-2SLS se conserva como ejercicio de robustez sobre la ventana original.
3. **DSA estocástico**: Análisis de Sostenibilidad de Deuda con calibración multivariada $t$-Student ($\nu \approx 4.8$, por método de momentos) y matrices de varianza-covarianza dinámica DCC-GARCH.

### Principales Hallazgos Empíricos

- **Reacción Fiscal Débil, convergente entre técnicas**: Ni DOLS ($\rho=-0.0071$, $p=0.564$) ni el VECM sobre ninguna de las dos ventanas ($\alpha_{pb}=0.0044$, $p=0.204$ ampliada; $\alpha_{pb}=0.0014$, $p=0.559$ original) encuentran una reacción fiscal de largo plazo significativa.
- **Umbral de fatiga fiscal mixto**: marginal en niveles (Sup-LM $p=0.076$, partición muestral desigual) y sólido en primera diferencia ($p<0.001$).
- **Identificación instrumental robusta**: IV-2SLS con el spread soberano del ETF EMB Brasil como instrumento muestra relevancia de primera etapa ($F=13.00>10$) y no rechaza la validez de sobreidentificación (Sargan $p=0.436$).
- **Quiebres Estructurales Múltiples**: Bai & Perron (2003) identifica quiebres en 2007T2, 2014T3 y 2018T1 (deuda SPNF) y en 2007T2 y 2016T4 (deuda consolidada).
- **Riesgo estocástico de insolvencia**: el DSA estocástico proyecta a 2035 una probabilidad de superar el 100% del PIB del $31.2\%$ (escenario de Referencia).

Para el detalle completo y las cifras exactas de cada estimación, ver `tesis/fuente/Tesis.pdf` — este resumen es orientativo, no reemplaza al documento.

---

## 2. Arquitectura del Repositorio

```text
Deuda/
├── .agents/                         # Reglas de gobernanza
│   └── AGENTS.md                    # Directivas para colaboradores y asistentes
├── .github/                         # Configuración GitHub
│   └── CONTRIBUTING.md              # Guía de contribución
├── Bibliografia/                    # Acervo bibliográfico y normativo descargado
│   ├── descargas_verificacion/      # PDFs de los papers efectivamente citados
│   ├── auditorias/                  # Informes de verificación de citas + búsqueda de literatura refutatoria
│   ├── marco_legal/                 # Textos oficiales de Leyes (24.156, 24.144, 27.541, 27.612, etc.)
│   └── material_metodologico_catedra/ # Bibliografía metodológica de referencia
├── codigo/                          # Código fuente econométrico reproducible
│   ├── ingesta_datos/               # Extracción y consolidación de series primarias
│   ├── modelos/                     # Scripts de estimación (Fases 1 a 18)
│   ├── graficos/                    # Generación de figuras vectoriales para la tesis
│   ├── codigo_completo_deuda.py     # Script único integrado de lectura secuencial
│   └── requirements.txt             # Dependencias del entorno Python
├── datos/                           # Data Pipeline
│   ├── crudos/                      # Descargas originales y reportes AGN
│   ├── procesados/                  # Series intermedias neteadas
│   ├── dataset_consolidado_real.csv # Panel trimestral 2004-2025 auditado (n=88)
│   └── codebook.md                  # Libro de códigos y metadatos de variables
├── historial_proyecto/              # Documentación metodológica y planes de revisión
├── resultados/                      # Salidas numéricas y tablas econométricas
│   └── tablas/                      # Exportación CSV de estimaciones y diagnósticos
├── tesis/                           # Manuscrito completo en LaTeX
│   ├── capitulos/                   # Archivos TeX por capítulo (00 a 09)
│   ├── figuras/                     # Gráficos e imágenes institucionales
│   └── fuente/                      # Documento maestro (Tesis.tex) y referencias.bib
├── LICENSE                          # Licencia MIT de código y datos
└── README.md                        # Documento maestro del repositorio
```


---

## 3. Guía de Reproducción Empírica

### Requisitos Previos

- **Python**: Versión 3.10 o superior.
- **LaTeX**: Distribución MiKTeX (Windows) o TeX Live (Linux/macOS) con `biber`.

### 1. Configuración del Entorno Virtual

```bash
# Clonar el repositorio
git clone https://github.com/usuario/Deuda.git
cd Deuda

# Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ingestión de Datos y Construcción del Panel

Para ejecutar el pipeline de descarga de APIS (BCRA, Datos Argentina, Yahoo Finance) y generación de `datos/dataset_consolidado_real.csv`:

```bash
python codigo/ingesta_datos/construccion_dataset.py
```

### 3. Ejecución de Modelos Econométricos

Cada fase econométrica puede ejecutarse de manera independiente o integrada:

```bash
# Ejecutar la secuencia completa de estimación
python codigo/codigo_completo_deuda.py

# O ejecutar fases específicas:
python codigo/modelos/fase1_estacionariedad.py
python codigo/modelos/fase3_reaccion_fiscal.py
python codigo/modelos/fase4_variables_instrumentales.py
python codigo/modelos/fase6_sostenibilidad_deuda.py
```

### 4. Compilación del Manuscrito LaTeX

Para generar el archivo PDF de la tesis (`Tesis.pdf`):

```bash
cd tesis/fuente
pdflatex -interaction=nonstopmode Tesis.tex
biber Tesis
pdflatex -interaction=nonstopmode Tesis.tex
pdflatex -interaction=nonstopmode Tesis.tex
```

---

## 4. Estructura de Datos y Codebook

El dataset principal [`datos/dataset_consolidado_real.csv`](file:///c:/Users/fedea/Deuda/datos/dataset_consolidado_real.csv) contiene 88 observaciones trimestrales con las siguientes variables clave:

| Variable | Descripción | Fuente Primaria | Transformación |
|---|---|---|---|
| `periodo` | Trimestre de observación (2004Q1–2025Q4) | N/A | Formato `YYYY-MM-DD` |
| `d_spnf` | Deuda Bruta SPNF / PIB nominal (%) | Secretaría de Finanzas / INDEC | Ratio trimestral |
| `d_consolidada` | Deuda SPNF + Pasivos BCRA netos / PIB (%) | Sec. Finanzas + BCRA / INDEC | Consolidación activa |
| `pb_t` | Resultado Primario SPNF / PIB nominal (%) | Secretaría de Hacienda / INDEC | Ratio trimestral |
| `embi` | Risk-premium EMBI+ Argentina (puntos básicos) | JP Morgan / BCRA | Promedio trimestral |
| `vix` | CBOE Volatility Index (VIX) | Chicago Board Options Exchange | Promedio trimestral |
| `emb_br` | Spread ETF iShares J.P. Morgan EMB Brasil | Yahoo Finance / FRED | Instrumento IV-2SLS |

Para mayor detalle sobre definiciones, unidades y tratamientos de datos, consultar el [`datos/codebook.md`](file:///c:/Users/fedea/Deuda/datos/codebook.md).

---

## 5. Acervo Bibliográfico y Marco Legal

El repositorio incluye la totalidad de las fuentes secundarias y primarias citadas en la tesis:

- **Marco Legal Descargado**: Alojado en [`Bibliografia/marco_legal/`](file:///c:/Users/fedea/Deuda/Bibliografia/marco_legal/), con copias oficiales de la Ley N° 24.156, Ley N° 24.144 (Carta Orgánica BCRA), Ley N° 25.152, Ley N° 27.541 y Ley N° 27.612.
- **Documentos de Auditoría**: Informe AGN Actuación 294/2023 sobre la deuda con el FMI en [`datos/crudos/descargas_drive/`](file:///c:/Users/fedea/Deuda/datos/crudos/descargas_drive/).
- **Trazabilidad Bibliográfica**: Manifiesto de verificación exhaustiva de citas en [`Bibliografia/descargas_verificacion/verificacion_bibliografia_completa.md`](file:///c:/Users/fedea/Deuda/Bibliografia/descargas_verificacion/verificacion_bibliografia_completa.md).

---

## 6. Reglas de Gobernanza y Colaboración

Para mantener la integridad científica del proyecto y permitir que investigadores y colaboradores trabajen de forma segura:

- **Colaboradores Humanos**: Consultar la guía [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) para conocer las convenciones de Git, pruebas econométricas requeridas y normas PEP8.
- **Asistentes de Inteligencia Artificial**: Las herramientas y agentes de IA deben ceñirse estrictamente a las directivas normativas definidas en [`.agents/AGENTS.md`](.agents/AGENTS.md).

---

## 7. Citación Académica

Si utiliza este código, dataset o manuscrito en investigaciones académicas, por favor cite de la siguiente forma:

```bibtex
@thesis{paez_chillon_carricondo_2026,
  author       = {P{\'a}ez, Santiago and Chill{\'o}n, Federico and Carricondo, Emiliano},
  title        = {La solvencia intertemporal de la deuda p{\'u}blica consolidada argentina post-2025: proyecciones a partir de sus determinantes macroecon{\'o}micos (2004--2025)},
  school       = {Facultad de Ciencias Econ{\'o}micas, Universidad Nacional de Cuyo},
  year         = {2026},
  type         = {Tesis Final de Grado},
  address      = {Mendoza, Argentina}
}
```

---

## Licencia

Este proyecto está bajo la Licencia Creative Commons Atribución 4.0 Internacional ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es)).
