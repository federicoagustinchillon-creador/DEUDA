# Código — Orientación

Tres subcarpetas, en el orden en que se ejecutan:

1. **[`ingesta_datos/`](ingesta_datos/README.md)** — descarga y arma el panel de datos desde las fuentes primarias (BCRA, MECON/INDEC, Yahoo Finance). Corre primero.
2. **[`modelos/`](modelos/README.md)** — las 18 fases del análisis econométrico (estacionariedad, cointegración, VECM, DOLS, Hansen, DSA, robustez). **Este es el corazón de la tesis** — el README de esa carpeta tiene la tabla completa fase → resultado → capítulo.
3. **`graficos/`** — genera las figuras del manuscrito a partir de los resultados de `modelos/`. Corre último.

Además:
- `codigo_completo_deuda.py`: concatena y ejecuta el pipeline íntegro (las tres carpetas de arriba, en orden) en un solo script de lectura secuencial.
- `notebook_analisis_completo.ipynb` / `notebook_codigo_completo.ipynb`: mismo contenido en formato Jupyter, para exploración interactiva.
- `requirements.txt`: dependencias Python (`pip install -r codigo/requirements.txt`).
