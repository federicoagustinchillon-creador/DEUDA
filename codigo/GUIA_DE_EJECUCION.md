# Guía de ejecución y replicabilidad

Esta guía permite a un tercero (por ejemplo, el tribunal examinador) verificar las cifras de la tesis.
Describe la versión vigente del análisis (SVARX 1996-2025, `fase24` y `fase25`). Los *scripts* de
`codigo/modelos/` con números de fase menores corresponden a versiones anteriores y no intervienen
en las cifras de la tesis.

## 1. Entorno

- Python 3.11 o superior. Dependencias: `pip install -r codigo/requirements.txt`.
- LaTeX (`xelatex`) y `pandoc` solo para recompilar el PDF.
- Las series ya están en `datos/procesados/`; no hace falta descargar nada para reestimar. El *script*
  `codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py` vuelve a descargar los empalmes del EMBI y del
  TCRM y requiere conexión; sus resultados ya están guardados en `datos/procesados/empalmes_1996_1998.csv`
  y `datos/crudos/empalmes/`.

## 2. Ejecución completa

```bash
bash codigo/modelos/correr_todo.sh
```

Reestima el modelo y todas las variantes de robustez (alrededor de 45 minutos en dos núcleos), genera las
figuras, el Apéndice y la hoja de números, y corre las pruebas automáticas (`pytest tests`). Cada paso deja
su registro en `resultados/registros/`.

## 3. Pasos por separado

| Paso | Comando | Salida |
|---|---|---|
| Estimación del SVARX y *bootstrap* de parámetros | `python codigo/modelos/fase24_svarx_1996_2025.py --deuda federal` | `resultados/tablas/fase24_federal_*.csv` |
| Propiedades de las series | `python codigo/modelos/fase24b_propiedades_series.py` | `fase24b_*.csv` |
| Simulación de Monte Carlo y contrastes | `python codigo/modelos/fase25_simulacion_dsa_svarx.py --suficiencia` | `fase25_federal_*.csv` |
| Variantes de robustez | opciones de `fase25` (véase `correr_todo.sh`) | `fase25_<variante>_*.csv` |
| Figuras | `python codigo/modelos/figuras_tesis.py` | `tesis/figuras/` |
| Apéndice y hoja de números | `python codigo/modelos/apendice_tablas.py`, `python codigo/modelos/hoja_de_numeros.py` | `tesis_oficial_borradores/` |
| Texto, Word y PDF | `python tesis_oficial_borradores/generar_latex.py --compilar` | `tesis/Tesis.pdf` |
| Control de consistencia del texto | `python tesis_oficial_borradores/verificar_consistencia.py` | código de salida 0 si no hay problemas |

## 4. Parámetros que fijan las cifras

- Semillas fijas en `fase24` y `fase25`; todas las especificaciones comparten los números aleatorios.
- `--B 1000` réplicas de parámetros y `--N 1000` trayectorias por réplica; la estimación central usa 20.000
  trayectorias.
- La especificación principal incluye las variables binarias presidenciales (`--sin-presidenciales` las
  quita) y estima la deuda consolidada con el BCRA desde 2002 (`INICIO_CONSOLIDADA` en `fase24`).
