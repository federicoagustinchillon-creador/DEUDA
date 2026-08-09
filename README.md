# Sostenibilidad de la Deuda Pública Consolidada Argentina (2004–2025)

[![Licencia](https://img.shields.io/badge/Licencia-CC--BY--4.0-blue.svg)](https.creativecommons.org/licenses/by/4.0/)
[![Python](https.img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LaTeX](https://img.shields.io/badge/LaTeX-MiKTeX%20%7C%20TeXLive-green.svg)](https://www.tug.org/texlive/)
[![Estado](https://img.shields.io/badge/Auditor%C3%ADa-Aprobada-success.svg)](#)

Repositorio y código fuente de la investigación econométrica y tesis de grado: **"La solvencia intertemporal de la deuda pública consolidada argentina post-2025: proyecciones a partir de sus determinantes macroeconómicos (2004–2025)"**, desarrollada en la Facultad de Ciencias Económicas de la Universidad Nacional de Cuyo (UNCuyo).

---

## 1. Resumen Ejecutivo

Este proyecto evalúa empíricamente la sostenibilidad fiscal e intertemporal de la deuda pública soberana de la República Argentina para el período trimestral 2004T1–2025T4 ($n=88$ observaciones). Se extiende la metodología econométrica tradicional mediante dos contribuciones centrales:

1. **Consolidación del Sector Público**: Integración de la deuda del Sector Público No Financiero (SPNF) con las pasivos monetarios y remunerados (LELIQ, NOTALIQ y Pases Pasivos) del Banco Central de la República Argentina (BCRA).
2. **Función de Reacción Fiscal Dinámica y DSA**: Estimación de la regla de reacción fiscal de Bohn (1998) mediante *Dynamic OLS* (DOLS) con corrección de endogeneidad por Variables Instrumentales (IV-2SLS), acompañada de un Análisis de Sostenibilidad de Deuda (DSA) estocástico con calibración multivariada $t$-Student ($\nu \approx 5.1$) y matrices de varianza-covarianza dinámica DCC-GARCH.

### Principales Hallazgos Empíricos

- **Reacción Fiscal Débil**: El coeficiente de respuesta del resultado primario ante la deuda acumulada es estadísticamente no significativo ($\rho = -0.0071$, $p = 0.564$), confirmando la inoperancia de la regla de Bohn en el período analizado.
- **Identificación Instrumental Robusta**: La estimación IV-2SLS utilizando el spread soberano del ETF EMB Brasil como instrumento externo muestra relevancia estricta ($F_{IV} = 23.39 > 10$) y validez de sobreidentificación (Sargan $p = 0.576$).
- **Quiebres Estructurales Múltiples**: El procedimiento de Bai & Perron (2003) identifica quiebres significativos en 2007T2, 2014T3 y 2018T1 para la deuda SPNF, y en 2007T2 y 2016T4 para la deuda consolidada.
- **Riesgo Estocástico de Insolvencia**: El DSA estocástico proyecta a 2035 una probabilidad de que la relación Deuda/PIB supere el 100% igual al $30.4\%$ bajo la especificación base de colas pesadas ($t$-multivariada), con robusteces del $31.9\%$ bajo GARCH(1,1) y $29.1\%$ bajo DCC-GARCH.

---

## 2. Arquitectura del Repositorio

```text
Deuda/
├── .agents/                         # Reglas de gobernanza
│   └── AGENTS.md                    # Directivas para colaboradores y asistentes
├── .github/                         # Configuración GitHub
│   └── CONTRIBUTING.md              # Guía de contribución
├── Bibliografia/                    # Acervo bibliográfico y normativo descargado
│   ├── descargas_verificacion/      # Papers académicos y documentos oficiales en PDF
│   └── marco_legal/                 # Textos oficiales de Leyes (24.156, 24.144, 27.612, etc.)
├── codigo/                          # Código fuente econométrico reproducible
│   ├── ingesta_datos/               # Extracción y consolidación de series primarias
│   ├── modelos/                     # Scripts de estimación (Fases 1 a 15)
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
