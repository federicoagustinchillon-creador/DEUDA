"""Tres especificaciones del SVARX sobre el código de la tesis (fase24 y fase25), sin modificarlo.

    niveles      Y = (pb, crec, EMBI, TCRM)                 la de la tesis
    mixto        Y = (dpb, crec, EMBI, TCRM)                solo el resultado primario en diferencias
    diferencias  Y = (dpb, crec, dEMBI, dTCRM)              todas las que no son ya una tasa

crec ya es 100*dln(PIB): no se vuelve a diferenciar. La deuda rezagada, la tasa de la FED (en
variación), el VIX y las binarias quedan como en la tesis. Las tres usan la misma muestra efectiva
(se pierde el primer trimestre por la diferencia también en niveles, para comparar sobre el mismo
período). En la simulación, las variables diferenciadas se acumulan para obtener el desvío en nivel
que usa la identidad de la deuda.
"""
from __future__ import annotations

import inspect
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[3]
SALIDA = REPO / "resultados" / "tablas" / "robustez_diferencias"
sys.path.insert(0, str(REPO / "codigo" / "modelos"))
import fase24_svarx_1996_2025 as f24  # noqa: E402
import fase25_simulacion_dsa_svarx as f25  # noqa: E402

DIF: dict[str, list[str]] = {
    "niveles": [],
    "mixto": ["pb_pib"],
    "diferencias": ["pb_pib", "EMBI", "TCRM"],
}
_cargar_original = f24.cargar_datos


def activar(spec: str, salida: pathlib.Path, misma_muestra: bool = True) -> None:
    """Parchea cargar_datos (diferencia las columnas de la especificación) y simular (acumula)."""
    cols = DIF[spec]

    def cargar(tipo_deuda: str, rezagos_fed: int):
        Y, X, q = _cargar_original(tipo_deuda, rezagos_fed)
        Y = Y.copy()
        for c in cols:
            Y[c] = Y[c].diff()
        if cols or misma_muestra:
            Y, X = Y.iloc[1:], X.iloc[1:]
        return Y, X, q

    f24.cargar_datos = cargar
    salida.mkdir(parents=True, exist_ok=True)
    f24.TABLAS = f25.TABLAS = salida

    src = inspect.getsource(_simular_original)
    reemplazos = [
        ("    y = np.zeros((N, TRIM + p, k))\n",
         "    y = np.zeros((N, TRIM + p, k))\n    L = np.zeros((N, TRIM + 1, k))\n"),
        ("        y[:, p + t] = din + fed_t + np.outer(v_dev, gv) + np.outer(d_dev, gd) + u[:, t]\n",
         "        y[:, p + t] = din + fed_t + np.outer(v_dev, gv) + np.outer(d_dev, gd) + u[:, t]\n"
         "        L[:, t + 1] = np.where(DIFMASK, L[:, t] + y[:, p + t], y[:, p + t])\n"),
        ("        yy = y[:, p + t - 3: p + t + 1]\n", "        yy = L[:, t - 2: t + 2]\n"),
        ("(yy[:, -1, 3] - y[:, p + t - 4, 3])", "(yy[:, -1, 3] - L[:, t - 3, 3])"),
    ]
    for a, b in reemplazos:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    ns = f25.__dict__
    ns["DIFMASK"] = np.array([c in cols for c in f24.ENDOG])
    exec(compile(src, "simular_parcheado", "exec"), ns)  # redefine f25.simular


_simular_original = f25.simular
