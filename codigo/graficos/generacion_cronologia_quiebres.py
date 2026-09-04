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

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.plot(pd.to_datetime(["2004-01-01", "2025-12-31"]), [0, 0], color="#1B365D", linewidth=2.2, zorder=2)

    levels = [1, -1, 1.2, -1.2]
    for i, d in enumerate(break_dates):
        key = d.strftime("%Y-%m")
        label = EVENT_LABELS.get(key, f"Quiebre detectado\n{key}")
        ax.scatter(d, 0, color="#8B1E1E", s=90, zorder=3, edgecolor="white", linewidth=1.5)
        ax.vlines(d, 0, levels[i], color="#8B1E1E", linestyle="--", linewidth=1.0, alpha=0.85)
        ax.text(d, levels[i] + (0.06 if levels[i] > 0 else -0.16), label,
                horizontalalignment="center", verticalalignment="center",
                bbox=dict(boxstyle="square,pad=0.5", facecolor="white", edgecolor="#CBD5E1", alpha=0.98),
                fontsize=8.8, fontfamily="serif")

    ax.set_xlim(pd.to_datetime("2003-06-01"), pd.to_datetime("2026-06-30"))
    ax.set_ylim(-1.85, 1.85)
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4, color="#E2E8F0")
    for spine in ["left", "right", "top"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#64748B")
    ax.spines["bottom"].set_linewidth(0.8)
    ax.get_yaxis().set_visible(False)
    ax.set_xlabel("Año", fontsize=10, fontfamily="serif")
    ax.tick_params(axis='x', labelsize=9.5)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "figura_5_4_quiebres_timeline.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[OK] Figura guardada en {out_path}")


if __name__ == "__main__":
    main()
