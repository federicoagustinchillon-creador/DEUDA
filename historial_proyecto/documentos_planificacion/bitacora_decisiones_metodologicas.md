# DECISION LOG: Arquitectura de la Investigación

## Decisión Metodológica 001: Elección de la Unidad de Análisis
* **Fecha:** Julio 2026
* **Tema:** Unidad de Análisis para la matriz de datos.
* **Alternativas consideradas:** El ciudadano argentino vs. El período mensual/anual en Argentina.
* **Ventajas de la elegida:** Al utilizar series de datos de fuentes secundarias macroeconómicas (MECON/BCRA), la unidad de análisis metodológica real es el **período temporal agregativo (el mes o el año)**, evitando caer en la Falacia Ecológica de declarar al "ciudadano".
* **Sustento Metodológico:** Ynoub, Roxana (2007) - Capítulo III (La Matriz de Datos).

## Decisión Metodológica 002: Análisis de Sostenibilidad No Lineal
* **Fecha:** Julio 2026
* **Tema:** Algoritmo econométrico para la proyección.
* **Alternativas consideradas:** Enfoque contable determinístico clásico vs. Enfoque estocástico (Fan Charts).
* **Ventajas de la elegida:** La plantilla integrada de sostenibilidad de deuda del BID/FMI exige mapear la incertidumbre mediante simulaciones de Monte Carlo frente a shocks en las tasas de interés ($r$) y tasa de crecimiento ($g$).
* **Sustento Teórico:** Libman, De la Vega y Zack (2024).

## Decisión Metodológica 003: Deuda Bruta (no Neta) como Variable de Stock
* **Fecha:** Agosto 2026 (formalizada retroactivamente; la elección ya regía en el pipeline empírico).
* **Tema:** El TP3 original (`05_METODOLOGIA_Variables.md`) especificaba "Ratio Deuda Pública Consolidada Neta / PIB". La tesis final mide Deuda Bruta Consolidada SPNF / PIB.
* **Alternativas consideradas:** Deuda neta (de activos financieros del sector público) vs. deuda bruta/total del gobierno.
* **Ventajas de la elegida:** La Plantilla Integrada del BID (Borensztein, Cavallo, Cifuentes y Valencia, 2013, IDB-TN-576, p. 4) recomienda explícitamente centrar el ASD en "la deuda total del gobierno... en lugar de la medida tradicional de la deuda externa [neta]... a fin de reflejar la evolución de la gestión de la deuda y los mercados financieros durante las últimas dos décadas." Deuda neta, además, exige series de activos financieros del sector público (reservas, depósitos, activos del FGS) con calidad y frecuencia trimestral inconsistente para 2004-2025.
* **Sustento Metodológico:** Borensztein, Cavallo, Cifuentes y Valencia (2013), BID Nota Técnica IDB-TN-576, p. 4.

## Decisión Metodológica 004: Brecha del Producto (filtro HP), no Variación del EMAE, como Control Cíclico
* **Fecha:** Agosto 2026 (formalizada retroactivamente).
* **Tema:** El TP3 original especificaba "Variación interanual desestacionalizada del EMAE" para el desempeño real. La tesis final usa la Brecha del Producto ($\tilde{y}_t$, filtro Hodrick-Prescott, $\lambda=1600$, sobre PIB real).
* **Alternativas consideradas:** Tasa de variación del EMAE vs. brecha del producto (desvío porcentual respecto de la tendencia).
* **Ventajas de la elegida:** La Función de Reacción Fiscal de Bohn (1998) y su extensión de fatiga fiscal en Ghosh et al. (2013) -ya adoptada como sustento teórico de H1a en esta tesis- especifican el control cíclico como brecha del producto (desvío del nivel respecto de su tendencia), no como una tasa de variación interanual. Usar el EMAE en tasa de variación mezclaría una variable de nivel-relativo-a-tendencia (lo que la teoría de Bohn/Ghosh exige) con una de crecimiento puntual, sin equivalencia directa.
* **Sustento Teórico:** Bohn (1998); Ghosh et al. (2013), ya citados en el Marco Teórico (Nivel II) de esta tesis.