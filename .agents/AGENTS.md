# Directivas de Gobernanza para Asistentes de Inteligencia Artificial

Este documento establece las reglas obligatorias e inmutables que cualquier agente o herramienta de inteligencia artificial (LLM, agente de código o script automatizado) debe cumplir al interactuar con el código, los datos o los manuscritos de este repositorio.

---

## 1. Principio de Inmutabilidad del Aporte Científico

1. **Preservación de Resultados Econométricos**: Queda strictly prohibido alterar o recalibrar los coeficientes estimados y métricas estadísticas fundamentales del trabajo:
   - Coeficiente de reacción fiscal DOLS: $\rho = -0.0071$ ($p = 0.564$).
   - Diagnósticos IV-2SLS: $F_{IV} = 23.39$, test de Sargan $p = 0.576$.
   - Sup-LM de Hansen: $p = 0.383$.
   - Cifra central de insolvencia DSA a 2035: $P(d_{2035} > 100\%) = 30.4\%$ (y sus robusteces del $31.9\%$ y $29.1\%$).
   - Fechas de quiebres estructurales Bai-Perron: 2007T2, 2014T3, 2018T1 (SPNF); 2007T2, 2016T4 (consolidada).
   - Tamaño muestral auditado: $n = 88$ observaciones trimestrales (2004T1–2025T4).

2. **Inmutabilidad de Datos de Origen**: Las carpetas `datos/crudos/` y el archivo `datos/dataset_consolidado_real.csv` constituyen la base de verdad empírica. No deben ser sobrescritos con datos sintéticos, interpolaciones no documentadas ni simulaciones ficticias.

---

## 2. Estándares de Lenguaje y Estilo ("Sin rastros de IA")

1. **Depuración de Muletillas y Marcas Artificiales**:
   - No incluir comentarios robóticos, firmas de agentes ("Generado por IA", "Instrucciones para el modelo", "As an AI...").
   - Evitar el tono defensivo o apologético en los comentarios o en el manuscrito ante resultados estadísticos no significativos ($p > 0.05$). La falta de significatividad debe reportarse como hallazgo empírico objetivo de inestabilidad teórica.

2. **Terminología Econométrica de Frontera**:
   - Todo código, docstring y documento de apoyo debe redactarse en español técnico, utilizando la terminología propia de la econometría de series de tiempo y las finanzas públicas (ej. *Dynamic OLS*, *estacionariedad*, *cointegración*, *quiebres estructurales*, *matriz de covarianza condicional dinámica*).

---

## 3. Protocolo de Verificación Obligatoria

1. **Validación de Código Python**:
   - Antes de dar por finalizada cualquier modificación en la carpeta `codigo/`, el agente debe verificar la sintaxis de todos los scripts ejecutando:
     ```bash
     python -c "import glob, py_compile; [py_compile.compile(f, doraise=True) for f in glob.glob('codigo/**/*.py', recursive=True)]"
     ```
   - Si se modifica el pipeline econométrico principal, se debe verificar que `codigo_completo_deuda.py` ejecute de principio a fin sin lanzar excepciones.

2. **Validación del Manuscrito LaTeX**:
   - Toda edición en la carpeta `tesis/` debe mantener la integridad de los paquetes y etiquetas de LaTeX.
   - Es obligatorio validar que la secuencia `pdflatex` -> `biber` -> `pdflatex` finalice sin errores de compilación ni citas no resueltas.

---

## 4. Control de Cambios y Git

1. **Commits Claros y Descriptivos**:
   - Los mensajes de commit generados por herramientas automatizadas deben seguir el estándar de commits convencionales (ej. `fix(econometria): ajustar especificacion DOLS`, `docs(legal): incorporar Ley 27612 al marco normativo`).
   - No incluir textos genéricos como "Update code", "AI changes" o "Refactoring".
