# Código

Tres carpetas. La replicación completa, con entorno, tiempos y parámetros, está en [`GUIA_DE_EJECUCION.md`](GUIA_DE_EJECUCION.md).

`ingesta_datos/` arma las series trimestrales de 1996-2025 desde las fuentes primarias, con los empalmes del EMBI y del TCRM (ver su [README](ingesta_datos/README.md)). `modelos/` contiene la estimación del SVARX, la simulación de Monte Carlo con el escenario del FMI, las robusteces, las figuras, el Apéndice y la hoja de números (ver su [README](modelos/README.md)). `requirements.txt` fija las versiones de las bibliotecas de Python.

Las pruebas automáticas están en [`../tests/`](../tests/) y se corren con `pytest tests`.
