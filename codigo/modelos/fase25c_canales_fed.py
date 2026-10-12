"""
fase25c_canales_fed.py
======================
Descompone el efecto del escenario de la FED de 2022-2023 (+5,25 pp en ocho trimestres) sobre la
deuda consolidada neta en 2035 en dos partes, con los parametros puntuales de la especificacion
principal (Capitulo 6, seccion 6.5):

  - costo directo: el mayor costo de refinanciar la deuda en dolares, con la respuesta de las
    variables domesticas a la FED anulada (gamma_fed = 0);
  - canales indirectos: la diferencia con el efecto total (respuesta del EMBI+, el TCRM, el
    crecimiento y el resultado primario).

Uso: python codigo/modelos/fase25c_canales_fed.py
Salida: resultados/tablas/fase25c_canales_fed.csv
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase24_svarx_1996_2025 as f24  # noqa: E402
import fase25_simulacion_dsa_svarx as f25  # noqa: E402

N_TRAYECTORIAS = 20_000


def main() -> None:
    f25.LAM = f25.velocidad_refinanciacion(f25.ESC)
    Y, X, _ = f24.cargar_datos("neta", 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    Y, X = f24.recortar(Y, X, p)
    res = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    par = f25.parametros(res, list(X.columns))
    esc = f25.escenario_fmi()
    d0, alfa, tcrm0 = f25.condiciones_iniciales("neta")
    eps = np.linalg.solve(par["S"], res.resid.values.T).T
    rng = np.random.default_rng(f25.SEMILLA)
    shocks = eps[rng.integers(0, len(eps), size=(N_TRAYECTORIAS, f25.TRIM))]
    fed = np.r_[np.full(8, 5.25 / 8), np.zeros(f25.TRIM - 8)]

    def correr(parametros: dict, camino: np.ndarray) -> tuple[float, float]:
        s = f25.simular(parametros, shocks, camino, esc, d0, alfa, tcrm0)
        return float(s["d"][:, -1].mean()), float(s["no_est_2035"].mean())

    base = correr(par, np.zeros(f25.TRIM))
    total = correr(par, fed)
    directo = correr(dict(par, gamma_fed=np.zeros_like(par["gamma_fed"])), fed)
    out = pd.DataFrame({
        "efecto": ["total", "costo_directo", "canales_indirectos"],
        "d2035_pp": [total[0] - base[0], directo[0] - base[0], total[0] - directo[0]],
        "p_noest_2035_pp": [100 * (total[1] - base[1]), 100 * (directo[1] - base[1]), 100 * (total[1] - directo[1])],
    })
    out["participacion_d2035"] = out["d2035_pp"] / out.loc[0, "d2035_pp"]
    out.to_csv(f25.TABLAS / "fase25c_canales_fed.csv", index=False)
    print(f"escenario={f25.ESC} lam={f25.LAM:.3f}")
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
