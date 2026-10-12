"""
figuras_tesis.py
================
Figuras de los Capitulos 5, 6 y 7 de la tesis, todas generadas desde archivos de datos y de
resultados del repositorio (ningun valor tipeado a mano, salvo los dos puntos de control del FMI
con su fuente). El abanico (figura 6.2) lo genera fig_abanico_deuda.py.

  fig5_1  Deuda consolidada 1996-2025: bruta, neta a valor libros y neta nominal (principal),
          con los valores del FMI (2025, anexo II, cuadro 2) como control.
  fig5_2  Variables endogenas del SVARX con los quiebres de Bai-Perron.
  fig5_3  Tasa de politica de la FED (con la tasa sombra de Wu y Xia) y VIX.
  fig6_1  Respuestas al impulso a +1 desvio de la tasa de la FED, con bandas de 90%.
  fig6_2  Grafico de abanico (fig_abanico_deuda.py).
  fig6_3  Participacion de cada bloque de shocks en la varianza de la deuda en 2035.
  fig6_4  Probabilidad de no estabilizacion por especificacion, 2031 y 2035, contra los umbrales del FMI.
  fig6_5  Contraste de suficiencia del superavit (H1a).
  fig7_1  Abanicos con shocks del SVARX y con shocks a la manera del FMI.
  fig7_2  Impulsores historicos anuales de la deuda (1997-2025).

Uso: python codigo/modelos/figuras_tesis.py
Salida: tesis/figuras/*.png
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase24_svarx_1996_2025 as f24  # noqa: E402
import fig_abanico_deuda  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
DATOS = BASE / "datos"
TABLAS = BASE / "resultados" / "tablas"
FIG = BASE / "tesis" / "figuras"

AZUL, GRIS, ROJO, VERDE = "#1f4e79", "#7f7f7f", "#a23b2a", "#4f7f3a"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.5,
                     "legend.frameon": False, "figure.dpi": 200})

# FMI (2025), CR 25/95, anexo II, cuadro 2: deuda consolidada neta del sector publico (% PIB).
CONTROL_FMI = {2023: 110.8, 2024: 51.5}


def leer(rel: str) -> pd.DataFrame:
    return pd.read_csv(DATOS / rel, parse_dates=["Date"], index_col="Date")


def guardar(fig, nombre: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG / nombre)
    plt.close(fig)
    print(f"[OK] tesis/figuras/{nombre}")


def fig5_1() -> None:
    b = leer("procesados/deuda_consolidada_1996_2025.csv")
    n = leer("procesados/deuda_consolidada_neta_nominal_1996_2025.csv")
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(b.index, b["deuda_consolidada_pib"], color=GRIS, lw=1.2, label="Consolidada bruta (SPNF + pasivos del BCRA)")
    ax.plot(n.index, n["deuda_consolidada_neta_libros_pib"], color=AZUL, lw=1.0, ls="--", label="Consolidada neta, Letras a valor libros")
    ax.plot(n.index, n["deuda_consolidada_neta_nominal_piso_pib"], color=AZUL, lw=1.8, label="Consolidada neta, Letras a valor nominal (principal)")
    ax.scatter([pd.Timestamp(f"{a}-12-31") for a in CONTROL_FMI], list(CONTROL_FMI.values()), color=ROJO,
               zorder=5, s=22, label="FMI (2025), consolidada neta")
    ax.set_ylabel("% del PIB")
    ax.legend(fontsize=7.5, loc="upper left")
    guardar(fig, "fig5_1_deuda_consolidada_1996_2025.png")


def fig5_2() -> None:
    Y, _, quiebres = f24.cargar_datos("neta", 2)
    titulos = {"pb_pib": "Resultado primario (% del PIB, trimestral anualizado)",
               "crec": "Crecimiento real trimestral (%)", "EMBI": "EMBI+ Argentina (puntos básicos)",
               "TCRM": "Tipo de cambio real multilateral (índice)"}
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.8), sharex=True)
    for ax, c in zip(axs.flat, f24.ENDOG):
        ax.plot(Y.index, Y[c], color=AZUL, lw=0.9)
        for q in quiebres:
            ax.axvline(q, color=ROJO, lw=0.7, ls=":")
        ax.set_title(titulos[c], fontsize=8)
    fig.text(0.5, 0.005, "Líneas punteadas: quiebres estructurales de Bai y Perron (2001T4, 2006T2, 2018T1)",
             ha="center", fontsize=7)
    guardar(fig, "fig5_2_variables_endogenas.png")


def fig5_3() -> None:
    f = leer("procesados/tasa_fed_trimestral_1996_2025.csv")
    v = leer("procesados/instrumentos_1996_2025.csv")["VIX"]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 4.2), sharex=True)
    a1.plot(f.index, f["fedfunds"], color=GRIS, lw=1.0, label="Tasa de fondos federales")
    a1.plot(f.index, f["tasa_politica_fed"], color=AZUL, lw=1.6, label="Tasa de política usada (sombra de Wu y Xia en el límite cero)")
    a1.axhline(0, color="black", lw=0.5)
    a1.set_ylabel("%")
    a1.legend(fontsize=7.5)
    a2.plot(v.index, v, color=AZUL, lw=1.0)
    a2.set_ylabel("VIX")
    guardar(fig, "fig5_3_fed_y_vix.png")


def fig6_1() -> None:
    q = pd.read_csv(TABLAS / "fase24_neta_bootstrap.csv", index_col=0)
    punto = pd.read_csv(TABLAS / "fase24_neta_respuesta_fed.csv", index_col=0)
    titulos = {"pb_pib": "Resultado primario (pp del PIB)", "crec": "Crecimiento real (pp)",
               "EMBI": "EMBI+ (puntos básicos)", "TCRM": "TCRM (índice)"}
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.6), sharex=True)
    for ax, c in zip(axs.flat, f24.ENDOG):
        filas = [f"fed_{c}_h{h}" for h in punto.index]
        ax.fill_between(punto.index, q.loc[filas, "p05"], q.loc[filas, "p95"], color=AZUL, alpha=0.2, lw=0,
                        label="Banda de 90% (bootstrap)")
        ax.plot(punto.index, punto[c], color=AZUL, lw=1.5, label="Estimación puntual")
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(titulos[c], fontsize=8)
    for ax in axs[1]:
        ax.set_xlabel("Trimestres después del shock")
    axs[0, 0].legend(fontsize=7)
    guardar(fig, "fig6_1_respuesta_fed.png")


def _intervalo(t: pd.DataFrame, fila: str, escala: float = 1.0) -> tuple[float, float, float]:
    """Estimacion central y longitudes de error (no negativas) hasta los percentiles 5 y 95."""
    c, lo, hi = (escala * t.loc[fila, k] for k in ("estimacion", "p05", "p95"))
    return c, max(c - lo, 0.0), max(hi - c, 0.0)


def fig6_3() -> None:
    t = pd.read_csv(TABLAS / "fase25_neta_resumen.csv", index_col=0)
    bloques = {"vshare_fiscal": "Fiscal", "vshare_actividad": "Actividad", "vshare_cambiario_y_riesgo": "Cambiario y de riesgo"}
    vals = [_intervalo(t, c) for c in bloques]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(list(bloques.values()), [v[0] for v in vals], color=[GRIS, GRIS, AZUL],
           yerr=[[v[1] for v in vals], [v[2] for v in vals]], capsize=4, error_kw={"lw": 0.8})
    for k, v in enumerate(vals):
        ax.text(k, 2, f"{v[0]:.1f}%".replace(".", ","), ha="center", color="white", fontsize=9, fontweight="bold")
    ax.set_ylabel("% de la varianza de la deuda en 2035")
    ax.grid(axis="x", visible=False)
    guardar(fig, "fig6_3_varianza_por_bloque.png")


ESPECIFICACIONES = {
    "neta": "Principal", "neta_libros": "Neta en\nlibros", "bruta": "Bruta", "tesoro": "Solo\nTesoro",
    "neta_dom": "Tasas\nen pesos", "neta_sin_retro": "Sin retro-\nalimentación", "neta_sin_default": "Sin shocks\ndel default",
    "neta_cr2595": "Escenario\nFMI 2025",
}


def fig6_4() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    specs = [s for s in ESPECIFICACIONES if (TABLAS / f"fase25_{s}_resumen.csv").exists()]
    x = np.arange(len(specs) + 1)
    for anio, color, dx in ((2031, AZUL, -0.17), (2035, GRIS, 0.17)):
        vals = [_intervalo(pd.read_csv(TABLAS / f"fase25_{s}_resumen.csv", index_col=0), f"base_p_noest_{anio}", 100) for s in specs]
        fmi = pd.read_csv(TABLAS / "fase25_neta_fmi_resumen.csv", index_col=0)["valor"]
        vals.append((100 * fmi[f"p_noest_{anio}"], 0.0, 0.0))
        ax.bar(x + dx, [v[0] for v in vals], width=0.34, color=color, capsize=3, error_kw={"lw": 0.8},
               yerr=[[v[1] for v in vals], [v[2] for v in vals]],
               label=f"{anio} ({'mediano plazo' if anio == 2031 else 'diez años'})")
    ax.axhline(1, color=ROJO, lw=1.2, ls="--", label="FMI (2026), mediano plazo: 1%")
    ax.axhline(3, color=ROJO, lw=1.0, ls=":", label="FMI (2026), diez años: menos de 3%")
    ax.set_xticks(x, [ESPECIFICACIONES[s] for s in specs] + ["Shocks a la\nmanera del FMI"], fontsize=7)
    ax.set_ylabel("Probabilidad de no estabilización (%)")
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=7, loc="upper left")
    guardar(fig, "fig6_4_probabilidad_no_estabilizacion.png")


def fig6_5() -> None:
    t = pd.read_csv(TABLAS / "fase25_neta_suficiencia.csv")
    pb = pd.read_csv(DATOS / "procesados" / "resultado_primario_1996_2025.csv", index_col=0, parse_dates=True)["pb_pib"]
    maximo = float(pb.max())
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(t["pb_2031"], 100 * t["p_noest_2031"], color=AZUL, lw=1.8, marker="o", ms=3, label="Probabilidad de no estabilización en 2031")
    ax.axhline(1, color=ROJO, lw=1.2, ls="--", label="FMI (2026): 1%")
    ax.axvline(maximo, color=GRIS, lw=1.0, ls=":", label=f"Máximo histórico 1996-2025: {maximo:.1f}%".replace(".", ","))
    ax.axvline(float(t["pb_2031"].iloc[0]), color=AZUL, lw=0.8, ls=":", label="Escenario base del FMI")
    ax.set_xlabel("Resultado primario en 2031 (% del PIB)")
    ax.set_ylabel("%")
    ax.legend(fontsize=7)
    guardar(fig, "fig6_5_suficiencia_superavit.png")


def fig7_1() -> None:
    a = pd.read_csv(TABLAS / "fase25_neta_fanchart.csv", index_col="anio")
    b = pd.read_csv(TABLAS / "fase25_neta_fmi_fanchart.csv", index_col="anio")
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.fill_between(b.index, b["p5"], b["p95"], color=GRIS, alpha=0.25, lw=0, label="Shocks a la manera del FMI, p5-p95")
    ax.plot(b.index, b["p50"], color=GRIS, lw=1.4, ls="--", label="Shocks a la manera del FMI, mediana")
    ax.fill_between(a.index, a["p5"], a["p95"], color=AZUL, alpha=0.35, lw=0, label="SVARX, p5-p95")
    ax.plot(a.index, a["p50"], color=AZUL, lw=1.6, label="SVARX, mediana")
    ax.set_ylabel("% del PIB")
    ax.set_xticks(a.index)
    ax.legend(fontsize=7.5, loc="upper left")
    guardar(fig, "fig7_1_abanico_svarx_vs_fmi.png")


def fig7_2() -> None:
    d = pd.read_csv(TABLAS / "fase25_impulsores_historicos_1997_2025.csv", index_col=0)
    titulos = {"g": "Crecimiento real (%)", "r": "Tasa real efectiva (%)", "z": "Depreciación real (%)",
               "pb": "Resultado primario (% del PIB)"}
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.6), sharex=True)
    for ax, c in zip(axs.flat, ["g", "r", "z", "pb"]):
        ax.bar(d.index, d[c], color=[ROJO if a == 2002 else AZUL for a in d.index], width=0.8)
        ax.axhline(d[c].mean(), color="black", lw=0.8, ls="--")
        ax.set_title(titulos[c], fontsize=8)
        ax.grid(axis="x", visible=False)
    fig.text(0.5, 0.005, "Línea punteada: media 1997-2025. En rojo, 2002.", ha="center", fontsize=7)
    guardar(fig, "fig7_2_impulsores_historicos.png")


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    for f in (fig5_1, fig5_2, fig5_3, fig6_1, fig6_3, fig6_4, fig6_5, fig7_1, fig7_2):
        f()
    fig_abanico_deuda.main()


if __name__ == "__main__":
    main()
