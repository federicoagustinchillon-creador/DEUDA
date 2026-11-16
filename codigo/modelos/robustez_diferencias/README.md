# Robustez: niveles, mixto y diferencias

Responde al comentario del director sobre el plan de labor (V2, página 9): "El VAR requiere que las
variables sean estacionarias. Si no lo son, se transforman para que lo sean." Compara la
especificación de la tesis (variables endógenas en niveles) con dos alternativas, usando el código
de `fase24` y `fase25` sin modificarlo: `specs.py` lo parchea en memoria.

| Especificación | Variables endógenas |
|---|---|
| niveles (tesis) | resultado primario, crecimiento, EMBI, TCRM |
| mixto | variación del resultado primario, crecimiento, EMBI, TCRM |
| diferencias | variación del resultado primario, crecimiento, variación del EMBI, variación del TCRM |

El crecimiento ya es 100 × dln(PIB real) y no se vuelve a diferenciar. La deuda rezagada, la tasa de
la FED (en variación), el VIX y las binarias quedan como en la tesis. Las tres usan la misma muestra
efectiva (1998T3-2025T4, 110 trimestres), porque la diferencia consume un trimestre. En la simulación,
las variables diferenciadas se acumulan para obtener el desvío en nivel que entra en la identidad de
la deuda.

## Scripts

Se corren desde la raíz del repositorio; las salidas van a `resultados/tablas/robustez_diferencias/`.

1. `raiz_diferencias.py`: ADF y KPSS en niveles (reproduce el apéndice A.3) y en primeras diferencias.
2. `correr_sim.py SPEC [opciones de fase25]`: simulación y medidas de H1a, H1b y H2 para una
   especificación. `--muestra-tesis` usa la muestra de la tesis (1998T2) para verificar que la versión
   en niveles reproduce sus números.
3. `diagnostico_y_pronostico.py`: rezagos (regla de la tesis y regla con Hannan-Quinn del plan),
   diagnóstico de residuos y pronóstico fuera de muestra con origen recursivo desde 2015T4
   (h = 1 a 8), comparado con la prueba de Diebold y Mariano con la corrección de Harvey, Leybourne
   y Newbold.
4. `veredictos.py`: veredicto de cada hipótesis con los criterios de la metodología (sección 4.6).

Orden completo (unos 20 minutos en dos núcleos):

```
python codigo/modelos/robustez_diferencias/raiz_diferencias.py
python codigo/modelos/robustez_diferencias/correr_sim.py niveles --muestra-tesis
python codigo/modelos/robustez_diferencias/correr_sim.py niveles --suficiencia
python codigo/modelos/robustez_diferencias/correr_sim.py mixto --suficiencia
python codigo/modelos/robustez_diferencias/correr_sim.py diferencias --suficiencia
python codigo/modelos/robustez_diferencias/correr_sim.py mixto --p 1 --suficiencia
python codigo/modelos/robustez_diferencias/correr_sim.py diferencias --p 4 --suficiencia
python codigo/modelos/robustez_diferencias/diagnostico_y_pronostico.py
python codigo/modelos/robustez_diferencias/veredictos.py
```

`mixto --p 1` y `diferencias --p 4` son los órdenes que elige la regla del plan (Schwarz entre los
estables; si los residuos tienen autocorrelación, el menor orden mayor que la elimina; si ninguno,
Hannan-Quinn). Sin `--p` se usa la regla de `fase24`.

## Resultados

Las tablas se generan en `resultados/tablas/robustez_diferencias/` (`veredictos.txt` y `diagnostico_y_pronostico.txt` resumen todo).
