# Modelos

Los scripts corren en el orden de la tabla y escriben en `resultados/tablas/` (con el prefijo del script), en `tesis/figuras/` y en `tesis_oficial_borradores/`. `correr_todo.sh` los encadena con todas las variantes de robustez; `_correr_sin_empalmes.sh` repite el ejercicio con datos desde 1999.

| Script | Qué hace | Dónde termina |
|---|---|---|
| `fase24_svarx_1996_2025.py` | Carga los datos, elige los rezagos, estima el SVARX, identifica los *shocks*, calcula los diagnósticos y los intervalos por *bootstrap* | Capítulos 4 y 6, Apéndice A.3 a A.8 |
| `fase24b_propiedades_series.py` | Raíz unitaria (ADF, KPSS, Zivot y Andrews), Bai y Perron y Johansen | Apéndice A.3 |
| `fase25_simulacion_dsa_svarx.py` | Simulación de Monte Carlo sobre el escenario base del FMI, métricas de no estabilización, descomposición de la varianza, escenarios de la FED y variantes de robustez (`--help` lista las opciones) | Capítulos 6 y 7, Apéndice A.9 y A.10 |
| `fase25b_diagnostico_abanico_fmi.py` | Diagnóstico del abanico con *shocks* a la manera del FMI | Capítulo 7, Tabla 7.1 |
| `figuras_tesis.py`, `fig_abanico_deuda.py` | Figuras de los capítulos 5, 6 y 7 | `tesis/figuras/` |
| `apendice_tablas.py` | Genera el Apéndice estadístico completo | `tesis_oficial_borradores/apendice.md` |
| `hoja_de_numeros.py` | Reúne las cifras que cita el texto | `tesis_oficial_borradores/_hoja_de_numeros.md` |
| `exportar_excel_grupo.py` | Excel de datos y resultados para el grupo | `tesis_oficial_borradores/para_el_grupo/` |
| `bai_perron.py` | Módulo de quiebres múltiples, usado por `fase24` y `fase24b` | |

Las semillas son fijas, de modo que las cifras se reproducen exactamente. Las versiones anteriores del análisis (DOLS, IV-2SLS, umbral de Hansen, VECM, DSA con DCC-GARCH) viven en las ramas `var-restringido` y `revision-var-vecm`.
