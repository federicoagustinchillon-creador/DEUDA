"""
fase25b_diagnostico_abanico_fmi.py
==================================
Diagnostico de la variante con shocks a la manera del FMI (fase25 --shocks fmi): que impulsor
historico explica el ancho del abanico y la probabilidad de no estabilizacion. Se repite la
simulacion (deuda federal bruta, perimetro del FMI, 20.000 trayectorias, misma semilla) quitando el anio 2002 o fijando un
impulsor en su media historica. Se usa en el Capitulo 7 (Discusion).

Uso: python codigo/modelos/fase25b_diagnostico_abanico_fmi.py
Salida: resultados/tablas/fase25b_diagnostico_abanico_fmi.csv
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase25_simulacion_dsa_svarx as f25  # noqa: E402


def main() -> None:
    esc = f25.escenario_fmi()
    d0, alfa, a_fmi, _ = f25.condiciones_iniciales("federal", esc)
    dr = f25.drivers_historicos()
    variantes = {
        f"todos_{dr.index.min()}_{dr.index.max()}": dr,
        "sin_2002": dr.drop(2002),
        "z_en_su_media": dr.assign(z=dr["z"].mean()),
        "r_en_su_media": dr.assign(r=dr["r"].mean()),
        "g_en_su_media": dr.assign(g=dr["g"].mean()),
        "pb_en_su_media": dr.assign(pb=dr["pb"].mean()),
    }
    filas = []
    for nombre, sub in variantes.items():
        s = f25.simular_fmi(sub, esc, d0, alfa, a_fmi, 20_000, np.random.default_rng(f25.SEMILLA + 1))  # misma semilla que la estimacion central
        filas.append({"variante": nombre, "p_noest_2031": s["no_est_2031"].mean(),
                      "p_noest_2035": s["no_est_2035"].mean(),
                      "ancho_p5_p95_2031": np.subtract(*np.percentile(s["d"][:, 6], [95, 5]))})
    out = pd.DataFrame(filas)
    out.to_csv(f25.TABLAS / "fase25b_diagnostico_abanico_fmi.csv", index=False)
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
