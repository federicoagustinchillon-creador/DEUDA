# Sostenibilidad de la Deuda Pública Consolidada Argentina (2004–2025)

[![Licencia](https://img.shields.io/badge/Licencia-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LaTeX](https://img.shields.io/badge/LaTeX-MiKTeX%20%7C%20TeXLive-green.svg)](https://www.tug.org/texlive/)
[![Estado](https://img.shields.io/badge/Auditor%C3%ADa-Aprobada-success.svg)](#)

Repositorio y código fuente de la investigación econométrica y tesis de grado: **"La solvencia intertemporal de la deuda pública consolidada argentina post-2025: proyecciones a partir de sus determinantes macroeconómicos (2004–2025)"**, desarrollada en la Facultad de Ciencias Económicas de la Universidad Nacional de Cuyo (UNCuyo).

---

## 0. Guía Rápida: qué mirar primero y en qué orden

**¿Solo querés leer la tesis?** → [`tesis/Tesis.pdf`](tesis/Tesis.pdf). No hace falta tocar nada más.

**¿Querés editar el texto de un capítulo?** → [`tesis/capitulos/`](tesis/capitulos/), un `.tex` por capítulo (`00_abstract`, `01_introduccion`, ..., `09_apendice`). Después de editar, compilar según el paso 4 de la sección 3.

**¿Querés ver de dónde sale un número que aparece en la tesis, o recorrer el análisis estadístico paso a paso?** → **[`codigo/modelos/README.md`](codigo/modelos/README.md)** es el índice único y ordenado de las 18 fases: qué hace cada script, qué CSV produce y en qué tabla/sección de la tesis termina. Es la puerta de entrada al análisis completo.

**¿Querés entender los datos antes que los modelos?** → **[`datos/README.md`](datos/README.md)**: explica los tres niveles (crudos → procesados → panel consolidado), por qué hay dos versiones del dataset (ventana original de 88 obs. vs. ventana ampliada de 108) y remite al [`codebook.md`](datos/codebook.md) para el detalle de cada variable.

**¿Querés re-correr todo el pipeline desde cero?** → [`codigo/README.md`](codigo/README.md) explica el orden de las tres subcarpetas (`ingesta_datos/` → `modelos/` → `graficos/`); Sección 3 de este README tiene los comandos exactos.

**¿Querés entender la bibliografía?** → [`Bibliografia/`](Bibliografia/): `marco_legal/` (leyes citadas), `descargas_verificacion/` (papers descargados con verificación de que existen y dicen lo que la tesis les atribuye), `auditorias/busqueda_literatura_refutacion/` (búsqueda activa de trabajos que contradigan los hallazgos, con veredicto).

**¿Buscás versiones anteriores o el historial de decisiones metodológicas?** → [`historial_proyecto/`](historial_proyecto/).

**Ramas de git**: `main` conserva la versión original de la tesis (DOLS como técnica de referencia, ventana 2004-2025) como respaldo. `revision-var-vecm` es la versión vigente (VECM como técnica de referencia sobre ventana ampliada 1999-2025, DOLS como robustez) — es la que hay que mirar salvo que se busque explícitamente el original.

**Carpetas que NO son parte de la tesis** (para no perder tiempo buscando ahí): `_material_cursada_NO_es_parte_de_la_tesis/` es material de la cursada (consignas de TP, no insumo de la investigación) — el prefijo `_` es a propósito, para que no se confunda con las carpetas de la investigación.

**Dentro de `Bibliografia/`**: `descargas_verificacion/` tiene los PDFs de los papers efectivamente citados. `auditorias/` tiene los informes de verificación (qué se chequeó de cada cita, y la búsqueda de literatura que pudiera refutar el trabajo). `marco_legal/` tiene las leyes citadas. `material_metodologico_catedra/` es bibliografía metodológica de referencia (Marradi, plantilla de DSA).

**Un solo PDF de la tesis, sin ambigüedad**: `tesis/Tesis.pdf` es el único PDF versionado del repositorio, visible apenas entrás a la carpeta `tesis/`. El código fuente LaTeX vive en `tesis/fuente/` (`Tesis.tex`, `referencias.bib`); ahí también se genera una copia de trabajo del PDF al compilar, pero esa es solo un artefacto de build (`.gitignore`), no la oficial.

---

## 1. Resumen Ejecutivo

Este proyecto evalúa empíricamente la sostenibilidad fiscal e intertemporal de la deuda pública soberana de la República Argentina, sobre dos ventanas muestrales: la original, 2004T1–2025T4 ($n=88$), y una ampliada por empalme histórico, 1999T1–2025T4 ($n=108$). Se extiende la metodología econométrica tradicional mediante tres contribuciones centrales:

1. **Consolidación del Sector Público**: Integración de la deuda del Sector Público No Financiero (SPNF) con los pasivos monetarios y remunerados (LELIQ, NOTALIQ y Pases Pasivos) del Banco Central de la República Argentina (BCRA).
2. **VECM como técnica de referencia**: Estimación de la Función de Reacción Fiscal de Bohn (1998) mediante un Modelo de Vectores con Corrección de Error (VECM) sobre la ventana ampliada, que trata la endogeneidad del sistema completo (deuda, resultado primario, riesgo soberano, tipo de cambio) de forma estructural. DOLS con corrección IV-2SLS se conserva como ejercicio de robustez sobre la ventana original.
3. **DSA estocástico**: Análisis de Sostenibilidad de Deuda con calibración multivariada $t$-Student ($\nu \approx 4.8$, por método de momentos) y matrices de varianza-covarianza dinámica [[dcc-garch-dynamic-correlation|DCC-GARCH]].

### Principales Hallazgos Empíricos

- **Reacción Fiscal Débil, convergente entre técnicas**: Ni DOLS ($\rho=-0.0071$, $p=0.564$) ni el VECM sobre ninguna de las dos ventanas ($\alpha_{pb}=0.0044$, $p=0.204$ ampliada; $\alpha_{pb}=0.0014$, $p=0.559$ original) encuentran una reacción fiscal de largo plazo significativa.
- **Umbral de fatiga fiscal mixto**: marginal en niveles (Sup-LM $p=0.076$, partición muestral desigual) y sólido en primera diferencia ($p<0.001$).
- **Identificación instrumental robusta**: IV-2SLS con el spread soberano del ETF EMB Brasil como instrumento muestra relevancia de primera etapa ($F=13.00>10$) y no rechaza la validez de sobreidentificación (Sargan $p=0.436$).
- **Quiebres Estructurales Múltiples**: Bai & Perron (2003) identifica quiebres en 2007T2, 2014T3 y 2018T1 (deuda SPNF) y en 2007T2 y 2016T4 (deuda consolidada).
- **Riesgo estocástico de insolvencia**: el DSA estocástico proyecta a 2035 una probabilidad de superar el 100% del PIB del $31.2\%$ (escenario de Referencia).

Para el detalle completo y las cifras exactas de cada estimación, ver [`tesis/Tesis.pdf`](tesis/Tesis.pdf) — este resumen es orientativo, no reemplaza al documento.

---

## 2. Arquitectura del Repositorio

```text
Deuda/
├── .agents/AGENTS.md                # Directivas de gobernanza científica para asistentes de IA
├── Bibliografia/                    # Acervo bibliográfico y normativo completo — ver Bibliografia/README.md
│   ├── descargas_verificacion/      # PDFs de los papers centrales y metodología de frontera
│   ├── analisis_deuda_argentina_multienfoque/ # Acervo exhaustivo de análisis de deuda en Argentina (5 pilares)
│   ├── auditorias/                  # Informes de verificación de citas + análisis bibliométrico y red de citas
│   ├── marco_legal/                 # Textos oficiales de Leyes (24.144, 24.156, 25.152, 27.541, 27.612)
│   └── material_metodologico_catedra/ # Bibliografía metodológica de referencia
├── codigo/                          # Código fuente econométrico reproducible — ver codigo/README.md
│   ├── ingesta_datos/               # Paso 1: extracción y consolidación de series primarias
│   ├── modelos/                     # Paso 2: las 18 fases del análisis — ÍNDICE PRINCIPAL, ver modelos/README.md
│   ├── graficos/                    # Paso 3: generación de figuras vectoriales para la tesis
│   ├── codigo_completo_deuda.py     # Script único integrado de lectura secuencial
│   └── requirements.txt             # Dependencias del entorno Python
├── datos/                           # Data Pipeline — ver datos/README.md
│   ├── crudos/                      # Descargas originales sin procesar
│   ├── procesados/                  # Series intermedias por fuente, ya limpias
│   ├── dataset_consolidado_real.csv     # Panel ventana original 2004-2025 (n=88)
│   ├── dataset_consolidado_real_ext.csv # Panel ventana ampliada 1999-2025 (n=108) — referencia actual
│   └── codebook.md                  # Libro de códigos y metadatos de variables
├── historial_proyecto/              # Archivo histórico (planes, decisiones) -- NO la especificación vigente
├── resultados/tablas/               # Salida CSV de cada fase econométrica — ver tablas/README.md
├── tesis/                           # Manuscrito completo en LaTeX
│   ├── Tesis.pdf                    # EL PDF PARA LEER — único entregable oficial, versionado
│   ├── capitulos/                   # Archivos TeX por capítulo (00 a 09)
│   ├── figuras/                     # Gráficos e imágenes institucionales
│   └── fuente/                      # Código fuente LaTeX (Tesis.tex, referencias.bib)
├── _material_cursada_NO_es_parte_de_la_tesis/ # Apuntes/parciales de cursada previa -- no es la tesis
├── LICENSE                          # Licencia CC BY 4.0
└── README.md                        # Este documento
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
pip install -r codigo/requirements.txt
```

### 2. Ingestión de Datos y Construcción del Panel

Detalle completo del orden en [`codigo/ingesta_datos/README.md`](codigo/ingesta_datos/README.md). Resumen:

```bash
# Panel ventana original (2004-2025, n=88)
python codigo/ingesta_datos/construccion_dataset.py

# Panel ventana ampliada (1999-2025, n=108) -- técnica de referencia actual
python codigo/ingesta_datos/construir_dataset_ampliado.py
```

### 3. Ejecución de Modelos Econométricos

Las 18 fases, en orden y con su mapeo a resultados, están documentadas en **[`codigo/modelos/README.md`](codigo/modelos/README.md)**. Para correr todo de una vez:

```bash
python codigo/codigo_completo_deuda.py
```

O una fase puntual, por ejemplo:

```bash
python codigo/modelos/fase16_vecm_dataset_ampliado.py   # VECM, técnica de referencia
python codigo/modelos/fase3_reaccion_fiscal.py           # DOLS
python codigo/modelos/fase6_sostenibilidad_deuda.py      # DSA
```

### 4. Compilación del Manuscrito LaTeX

```bash
cd tesis/fuente
xelatex -interaction=nonstopmode Tesis.tex
biber Tesis
xelatex -interaction=nonstopmode Tesis.tex
xelatex -interaction=nonstopmode Tesis.tex
cd ..
cp fuente/Tesis.pdf Tesis.pdf   # el compilador escribe en fuente/; el oficial va un nivel arriba
```

---

## 4. Estructura de Datos y Codebook

Hay dos paneles consolidados — ver [`datos/README.md`](datos/README.md) para por qué son distintos. El de referencia actual es [`datos/dataset_consolidado_real_ext.csv`](datos/dataset_consolidado_real_ext.csv) (1999T1–2025T4, n=108). Columnas (nombres reales, tal como aparecen en el CSV):

| Variable | Descripción | Fuente Primaria | Transformación |
|---|---|---|---|
| `Date` | Trimestre de observación | N/A | Formato fecha |
| `deuda_pib` | Deuda pública / PIB (%) | Secretaría de Finanzas / MECON | % del PIB, fin de trimestre |
| `pb_pib` | Resultado primario SPNF / PIB (%) | Secretaría de Hacienda / MECON | % del PIB |
| `PIB_real` | PIB a precios constantes | INDEC | Índice de volumen |
| `g_gap` | Brecha del producto (output gap) | Derivado de `PIB_real` | Filtro HP, λ=1600 |
| `EMBI` | Riesgo país EMBI+ Argentina (puntos básicos) | Ámbito Financiero / BCRA / JP Morgan | Promedio trimestral |
| `TCRM` | Tipo de Cambio Real Multilateral | BCRA | Índice dic-2001=1, promedio trimestral |
| `VIX` | CBOE Volatility Index | Chicago Board Options Exchange | Promedio trimestral |
| `CER` | Coeficiente de Estabilización de Referencia | BCRA | Var. % acumulada trimestral |
| `es_interpolado` | Marca observaciones del tramo 1999–2003 obtenidas por empalme histórico vs. serie original | N/A | Booleano |

Definiciones completas, fuentes de fallback y notas metodológicas: [`datos/codebook.md`](datos/codebook.md).

---

## 5. Acervo Bibliográfico y Marco Legal

El repositorio incluye la totalidad de las fuentes secundarias y primarias citadas en la tesis:

- **Marco Legal Descargado**: Alojado en [`Bibliografia/marco_legal/`](Bibliografia/marco_legal/), con copias oficiales de la Ley N° 24.156, Ley N° 24.144 (Carta Orgánica BCRA) y Ley N° 27.612.
- **Documentos de Auditoría**: Informe AGN Actuación 294/2023 sobre la deuda con el FMI en [`datos/crudos/descargas_drive/`](datos/crudos/descargas_drive/).
- **Trazabilidad Bibliográfica**: Manifiesto de verificación exhaustiva de citas en [`Bibliografia/auditorias/verificacion_bibliografia_completa.md`](Bibliografia/auditorias/verificacion_bibliografia_completa.md).

---

## 6. Reglas de Gobernanza

Los asistentes de IA que colaboren en este repositorio deben ceñirse a las directivas definidas en [`.agents/AGENTS.md`](.agents/AGENTS.md).

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
