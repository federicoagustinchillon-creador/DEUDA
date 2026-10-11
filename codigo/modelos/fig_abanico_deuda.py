"""
fig_abanico_deuda.py
====================
Grafico de abanico de la deuda consolidada neta simulada (fase25, especificacion principal)
para el Capitulo 6. Bandas p5-p95, p10-p90 y p25-p75 y mediana, 2025-2035.

Uso: python codigo/modelos/fig_abanico_deuda.py
Salida: tesis/figuras/fig6_2_abanico_deuda_neta.png
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
ENTRADA = BASE / "resultados" / "tablas" / "fase25_neta_fanchart.csv"
SALIDA = BASE / "tesis" / "figuras" / "fig6_2_abanico_deuda_neta.png"


def main() -> None:
    f = pd.read_csv(ENTRADA, index_col="anio")
    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=200)
    for lo, hi, alpha in (("p5", "p95", 0.18), ("p10", "p90", 0.28), ("p25", "p75", 0.42)):
        ax.fill_between(f.index, f[lo], f[hi], color="#1f4e79", alpha=alpha, linewidth=0,
                        label=f"Percentiles {lo[1:]}-{hi[1:]}")
    ax.plot(f.index, f["p50"], color="#1f4e79", linewidth=1.8, label="Mediana")
    ax.set_xlabel("Año")
    ax.set_ylabel("% del PIB")
    ax.set_xticks(f.index)
    ax.grid(axis="y", color="#cccccc", linewidth=0.5)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA)
    print(f"[OK] {SALIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
