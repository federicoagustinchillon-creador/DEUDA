"""
generacion_cronologia_quiebres.py
=================================
Linea de tiempo de quiebres estructurales multiples detectados de forma real
sobre la serie de Resultado Primario / PIB (pb_t), mediante el algoritmo de
Programacion Dinamica con costo L2 del paquete `ruptures` (Killick et al.,
2012; Truong, Oudre y Vayatis, 2020), en el espiritu del enfoque de particion
optima de quiebres multiples de Bai y Perron (2003).

Nota metodologica: este script NO reproduce el procedimiento secuencial de
contrastes F con errores robustos propuesto originalmente por Bai y Perron
(2003) -esa implementacion formal permanece como agenda de investigacion
futura, segun se documenta en el Capitulo 4-. Lo que aqui se reporta es una
deteccion exploratoria y realmente computada de quiebres multiples sobre la
serie real del proyecto (datos/dataset_consolidado_real.csv), util como
evidencia complementaria a la prueba de quiebre unico de Zivot-Andrews.

Salida: tesis/figuras/figura_5_4_quiebres_timeline.png
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import ruptures as rpt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "datos", "dataset_consolidado_real.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "tesis", "figuras")

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
})

EVENT_LABELS = {
    "2008-09": "Quiebre I: fin del ciclo de superávits\ny crisis financiera internacional",
    "2013-06": "Quiebre II: profundización del\ncontrol de cambios y estancamiento",
    "2019-03": "Quiebre III: recesión post-crisis\ncambiaria y programa con el FMI",
    "2024-03": "Quiebre IV: ajuste fiscal\nabrupto (shock de superávit)",
}


def detect_breaks(series, n_breaks=4):
    algo = rpt.Dynp(model="l2", min_size=6, jump=1).fit(series.values)
    bkps = algo.predict(n_bkps=n_breaks)
    return bkps[:-1]  # el último índice que devuelve ruptures es el fin de la serie, no un quiebre


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    bkps_idx = detect_breaks(df["pb_pib"], n_breaks=4)
    break_dates = [df.loc[idx, "Date"] for idx in bkps_idx]

    print("Quiebres estructurales detectados (Programación Dinámica, costo L2):")
    for d in break_dates:
        print(" ->", d.strftime("%Y-%m"))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(pd.to_datetime(["2004-01-01", "2025-12-31"]), [0, 0], color="#2C3E50", linewidth=2, zorder=1)

    levels = [1, -1, 1.2, -1.2]
    for i, d in enumerate(break_dates):
        key = d.strftime("%Y-%m")
        label = EVENT_LABELS.get(key, f"Quiebre detectado\n{key}")
        ax.scatter(d, 0, color="#D9534F", s=100, zorder=2, edgecolor="black")
        ax.vlines(d, 0, levels[i], color="#D9534F", linestyle="--", linewidth=1)
        ax.text(d, levels[i] + (0.05 if levels[i] > 0 else -0.15), label,
                horizontalalignment="center", verticalalignment="center",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#F8F9F9", edgecolor="gainsboro", alpha=0.9),
                fontsize=9, fontname="serif")

    ax.set_xlim(pd.to_datetime("2003-01-01"), pd.to_datetime("2026-12-31"))
    ax.set_ylim(-1.8, 1.8)
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, linestyle=":", alpha=0.6)
    for spine in ["left", "right", "top"]:
        ax.spines[spine].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlabel("Año")

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_5_4_quiebres_timeline.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[OK] Figura guardada en {out_path}")


if __name__ == "__main__":
    main()
