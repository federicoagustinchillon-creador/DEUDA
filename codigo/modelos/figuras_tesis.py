"""
figuras_tesis.py
================
Figuras de los Capitulos 5, 6 y 7 de la tesis, todas generadas desde archivos de datos y de
resultados del repositorio (ningun valor tipeado a mano, salvo los dos puntos de control del FMI
con su fuente). El abanico (figura 6.2) lo genera fig_abanico_deuda.py.

  fig5_1  Deuda federal bruta (principal) y consolidada con el BCRA 1996-2025, con los valores
          del FMI (2026, anexo II, cuadro 2) como control.
  fig5_2  Variables endogenas del SVARX con los quiebres de Bai-Perron.
  fig5_3  Tasa de politica de la FED (con la tasa sombra de Wu y Xia) y VIX.
  fig6_1  Respuestas al impulso a +1 desvio de la tasa de la FED, con bandas de 90%.
  fig6_2  Grafico de abanico (fig_abanico_deuda.py).
  fig6_3  Participacion de cada bloque de shocks en la varianza de la deuda en 2035.
  fig6_4  Probabilidad de no estabilizacion por especificacion, 2031 y 2035, contra los umbrales del FMI.
  fig6_5  Contraste de suficiencia del superavit (H1a).
  fig7_1  Abanicos con shocks del SVARX y con shocks a la manera del FMI.
  fig7_2  Impulsores historicos anuales de la deuda (2000-2025).

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

# FMI (2026), CR 26/105, anexo II, cuadro 2 (% PIB): linea 1, deuda federal bruta, y linea 5,
# deuda del sector publico consolidado con el BCRA (neta de tenencias intra sector publico).
CONTROL_FEDERAL = {2023: 154.6, 2024: 84.7, 2025: 80.3}
CONTROL_CONSOLIDADA = {2023: 111.1, 2024: 53.6, 2025: 52.1}


def leer(rel: str) -> pd.DataFrame:
    return pd.read_csv(DATOS / rel, parse_dates=["Date"], index_col="Date")


def guardar(fig, nombre: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG / nombre)
    plt.close(fig)
    print(f"[OK] tesis/figuras/{nombre}")


def fig5_1() -> None:
    n = leer("procesados/deuda_consolidada_neta_nominal_1996_2025.csv")
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(n.index, n["bruta_federal_pib"], color=AZUL, lw=1.8, label="Federal bruta (perímetro del FMI, principal)")
    ax.plot(n.index, n["deuda_consolidada_neta_nominal_pib"], color=GRIS, lw=1.3, label="Consolidada con el BCRA (extensión)")
    for ctrl, color, etiqueta in ((CONTROL_FEDERAL, ROJO, "FMI (2026), federal bruta"),
                                  (CONTROL_CONSOLIDADA, VERDE, "FMI (2026), consolidada")):
        ax.scatter([pd.Timestamp(f"{a}-12-31") for a in ctrl], list(ctrl.values()), color=color, zorder=5, s=20, label=etiqueta)
    inicio = pd.Timestamp(f24.INICIO_CONSOLIDADA)
    ax.axvspan(n.index.min(), inicio, color="#eeeeee", zorder=0)
    ax.axvline(inicio, color=GRIS, lw=0.8, ls="--")
    ax.text(n.index.min() + pd.Timedelta(days=120), 152, "Antes de 2002\nla consolidada\nno se estima", fontsize=7, color=GRIS, va="top", ha="left")
    ax.set_ylabel("% del PIB")
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.55, 1.0))
    guardar(fig, "fig5_1_deuda_1996_2025.png")


def fig5_2() -> None:
    Y, _, quiebres = f24.cargar_datos("federal", 2)
    titulos = {"pb_pib": "Resultado primario (% del PIB, trimestral anualizado)",
               "crec": "Crecimiento real trimestral (%)", "EMBI": "EMBI Argentina (puntos básicos)",
               "TCRM": "Tipo de cambio real multilateral (índice)"}
    fig = plt.figure(figsize=(7, 5.4))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.22], hspace=0.45)
    axs = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]
    for ax, c in zip(axs, f24.ENDOG):
        ax.plot(Y.index, Y[c], color=AZUL, lw=0.9)
        for q in quiebres:
            ax.axvline(q, color=ROJO, lw=0.7, ls=":")
        ax.set_title(titulos[c], fontsize=8)
        ax.set_xlim(Y.index.min(), Y.index.max())
    # Franja de gobiernos (Menem es la categoria de referencia de las binarias presidenciales).
    fin_ventana = Y.index.max() + pd.offsets.QuarterEnd(0)
    inicios = {"Menem": Y.index.min() - pd.offsets.QuarterEnd(1)}
    mandatos = {"Menem": (inicios["Menem"], pd.Timestamp(list(f24.MANDATOS.values())[0][0]) - pd.offsets.QuarterEnd(1))}
    etiquetas = {"Menem": "Menem", "De_la_Rua": "De la Rúa", "Duhalde": "Duh.", "N_Kirchner": "N. Kirchner",
                 "CF_Kirchner": "C. Fernández de Kirchner", "Macri": "Macri", "A_Fernandez": "A. Fernández", "Milei": "Milei"}
    for nombre, (ini, fin) in f24.MANDATOS.items():
        mandatos[nombre] = (pd.Timestamp(ini) - pd.offsets.QuarterEnd(1), pd.Timestamp(fin))
    axg = fig.add_subplot(gs[2, :])
    for k, (nombre, (ini, fin)) in enumerate(mandatos.items()):
        axg.axvspan(ini, fin, color=(AZUL if k % 2 == 0 else GRIS), alpha=0.28, lw=0)
        axg.text(ini + (fin - ini) / 2, 0.5, etiquetas[nombre], ha="center", va="center", fontsize=5.6 if nombre in ("Duhalde", "De_la_Rua") else 6.2)
    axg.set_xlim(Y.index.min(), Y.index.max())
    axg.set_yticks([])
    axg.grid(False)
    for lado in ("left", "bottom"):
        axg.spines[lado].set_visible(False)
    axg.tick_params(axis="x", length=0, labelbottom=False)
    fechas = ", ".join(f"{q.year}T{q.quarter}" for q in quiebres)
    fig.text(0.5, 0.005, f"Líneas punteadas: quiebres de Bai y Perron conservados ({fechas}). Franja inferior: gobiernos; Menem es la referencia de las binarias presidenciales.",
             ha="center", fontsize=6.3)
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
    q = pd.read_csv(TABLAS / "fase24_federal_bootstrap.csv", index_col=0)
    punto = pd.read_csv(TABLAS / "fase24_federal_respuesta_fed.csv", index_col=0)
    titulos = {"pb_pib": "Resultado primario (pp del PIB)", "crec": "Crecimiento real (pp)",
               "EMBI": "EMBI (puntos básicos)", "TCRM": "TCRM (índice)"}
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.6), sharex=True)
    for ax, c in zip(axs.flat, f24.ENDOG):
        filas = [f"fed_{c}_h{h}" for h in punto.index]
        ax.fill_between(punto.index, q.loc[filas, "p05"], q.loc[filas, "p95"], color=AZUL, alpha=0.2, lw=0,
                        label="Intervalo de 90% (Hall)")
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
    t = pd.read_csv(TABLAS / "fase25_federal_resumen.csv", index_col=0)
    bloques = {"vshare_fiscal": "Fiscal", "vshare_actividad": "Actividad", "vshare_cambiario_y_riesgo": "Cambiario y\nde riesgo",
               "vshare_externo": "Externo\n(FED y VIX)"}
    ext = {"vshare_externo_vix": "VIX\nsolo", "vshare_externo_fed": "FED\nsola", "vshare_externo_fed_directo": "FED, solo\nefecto directo"}
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(8.4, 3.2), gridspec_kw={"width_ratios": [4, 3]})
    vals = [_intervalo(t, c) for c in bloques]
    ax.bar(list(bloques.values()), [v[0] for v in vals], color=[ROJO, GRIS, AZUL, AZUL],
           yerr=[[v[1] for v in vals], [v[2] for v in vals]], capsize=4, error_kw={"lw": 0.8})
    for k, v in enumerate(vals):
        ax.text(k, 2, f"{v[0]:.1f}%".replace(".", ","), ha="center", color="white", fontsize=9, fontweight="bold")
    ax.set_ylabel("% de la varianza de la deuda en 2035")
    ax.set_title("Participación de cada bloque", fontsize=8.5)
    ax.grid(axis="x", visible=False)
    v2 = [_intervalo(t, c) for c in ext]
    bx.bar(list(ext.values()), [v[0] for v in v2], color=[AZUL, VERDE, VERDE],
           yerr=[[v[1] for v in v2], [v[2] for v in v2]], capsize=4, error_kw={"lw": 0.8})
    for k, v in enumerate(v2):
        bx.text(k, max(v[0] * 0.5, 2), f"{v[0]:.1f}%".replace(".", ","), ha="center", color="white", fontsize=8.5, fontweight="bold")
    bx.axhline(t.loc["vshare_externo", "estimacion"], color=GRIS, lw=0.9, ls="--")
    bx.text(2.45, t.loc["vshare_externo", "estimacion"], "bloque externo\ncompleto", fontsize=6.5, color=GRIS, ha="right", va="bottom")
    bx.set_title("Apertura del bloque externo (no aditiva)", fontsize=8.5)
    bx.grid(axis="x", visible=False)
    guardar(fig, "fig6_3_varianza_por_bloque.png")


ESPECIFICACIONES = {
    "federal": "Principal", "consolidada": "Consolidada\ncon el BCRA", "federal_dom": "Tasas\nen pesos",
    "federal_sin_retro": "Sin retro-\nalimentación", "federal_p3": "Tres\nrezagos", "federal_sin_default": "Sin shocks\ndel default",
    "federal_desde2004": "Datos\ndesde 2004", "federal_sin_presidenciales": "Sin binarias\npresidenciales", "federal_cr2595": "Escenario\nFMI 2025", "federal_kilian": "Corrección\nde Kilian",
}


def fig6_4() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    specs = [s for s in ESPECIFICACIONES if (TABLAS / f"fase25_{s}_resumen.csv").exists()]
    x = np.arange(len(specs) + 1)
    for anio, color, dx in ((2031, AZUL, -0.17), (2035, GRIS, 0.17)):
        vals = [_intervalo(pd.read_csv(TABLAS / f"fase25_{s}_resumen.csv", index_col=0), f"base_p_noest_{anio}", 100) for s in specs]
        fmi = pd.read_csv(TABLAS / "fase25_federal_fmi_resumen.csv", index_col=0)["valor"]
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
    t = pd.read_csv(TABLAS / "fase25_federal_suficiencia.csv")
    pb = pd.read_csv(DATOS / "procesados" / "resultado_primario_1996_2025.csv", index_col=0, parse_dates=True)["pb_pib_sin_rentas"]
    maximo = float(pb[pb.index.quarter == 4].loc["1996":].max())  # anio calendario, sin rentas de la propiedad
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(t["pb_2031"], 100 * t["p_noest_2031"], color=AZUL, lw=1.8, marker="o", ms=3, label="No estabilización en 2031, métrica anual")
    if "p_noest_fmi_2031" in t:
        ax.plot(t["pb_2031"], 100 * t["p_noest_fmi_2031"], color=GRIS, lw=1.5, ls="-.",
                label="No estabilización en 2031, definición operativa del FMI")
    ax.axhline(1, color=ROJO, lw=1.2, ls="--", label="FMI (2026): 1%")
    ax.axvline(maximo, color=GRIS, lw=1.0, ls=":", label=f"Máximo anual 1996-2025: {maximo:.1f}%".replace(".", ","))
    ax.axvline(float(t["pb_2031"].iloc[0]), color=AZUL, lw=0.8, ls=":", label="Escenario base del FMI")
    ax.set_xlabel("Resultado primario en 2031 (% del PIB)")
    ax.set_ylabel("%")
    ax.legend(fontsize=7)
    guardar(fig, "fig6_5_suficiencia_superavit.png")


def fig7_1() -> None:
    a = pd.read_csv(TABLAS / "fase25_federal_fanchart.csv", index_col="anio")
    b = pd.read_csv(TABLAS / "fase25_federal_fmi_fanchart.csv", index_col="anio")
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
    d = pd.read_csv(TABLAS / "fase25_federal_impulsores_historicos.csv", index_col=0)
    titulos = {"g": "Crecimiento real (%)", "r": "Tasa real efectiva (%)", "z": "Depreciación real (%)",
               "pb": "Resultado primario (% del PIB)"}
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.6), sharex=True)
    for ax, c in zip(axs.flat, ["g", "r", "z", "pb"]):
        ax.bar(d.index, d[c], color=[ROJO if a == 2002 else AZUL for a in d.index], width=0.8)
        ax.axhline(d[c].mean(), color="black", lw=0.8, ls="--")
        ax.set_title(titulos[c], fontsize=8)
        ax.grid(axis="x", visible=False)
    fig.text(0.5, 0.005, f"Línea punteada: media {d.index.min()}-{d.index.max()}. En rojo, 2002.", ha="center", fontsize=7)
    guardar(fig, "fig7_2_impulsores_historicos.png")


def figA_1() -> None:
    """Empalmes de 1996-1998: serie oficial contra la reconstruida con la variable puente."""
    v = pd.read_csv(TABLAS / "empalmes_validacion.csv").set_index("empalme")
    a_, b_ = float(v.loc["EMBI", "a"]), float(v.loc["EMBI", "b"])
    tasa = pd.read_csv(DATOS / "crudos" / "empalmes" / "bcra_tasa_interbancaria_usd_mensual.csv", parse_dates=["Date"], index_col="Date").iloc[:, 0]
    fed = leer("procesados/tasa_fed_trimestral_1996_2025.csv")["fedfunds"]
    puente = a_ + b_ * (tasa.resample("QE").mean() - fed) * 100
    base = leer("dataset_consolidado_1996_2025.csv")
    obs = base["EMBI"].where(base["EMBI_fuente"].str.startswith("J.P."))
    reer = pd.read_csv(DATOS / "crudos" / "empalmes" / "bis_reer_amplio_argentina_mensual.csv", parse_dates=["Date"], index_col="Date").iloc[:, 0]
    inv = 1.0 / reer.resample("QE").mean()
    t_obs = base["TCRM"].where(base["TCRM_fuente"].str.startswith("BCRA"))
    ancla = pd.Timestamp("1997-03-31")
    t_bis = t_obs.loc[ancla] * inv / inv.loc[ancla]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 5.2))
    a1.plot(obs.loc[:"2001-12-31"].index, obs.loc[:"2001-12-31"], color=AZUL, lw=1.8, label="EMBI observado (J.P. Morgan)")
    a1.plot(puente.loc["1996":"2001-09-30"].index, puente.loc["1996":"2001-09-30"], color=ROJO, lw=1.2, ls="--",
            label="Reconstruido con la tasa interbancaria en dólares (BCRA)")
    a1.axvspan(pd.Timestamp("1998-10-01"), pd.Timestamp("2001-09-30"), color=GRIS, alpha=0.12, lw=0)
    a1.set_ylabel("Puntos básicos")
    a1.set_title("EMBI: superposición 1998T4-2001T3 (sombreada) y tramo empalmado 1996-1998", fontsize=8)
    a1.legend(fontsize=7, loc="upper left")
    a2.plot(t_obs.loc[:"2003-12-31"].index, t_obs.loc[:"2003-12-31"], color=AZUL, lw=1.8, label="TCRM del BCRA")
    a2.plot(t_bis.loc["1996":"2003-12-31"].index, t_bis.loc["1996":"2003-12-31"], color=ROJO, lw=1.2, ls="--",
            label="Encadenado con el tipo de cambio real efectivo del BIS")
    a2.set_title("TCRM: tramo empalmado 1996 y comparación 1997-2003", fontsize=8)
    a2.legend(fontsize=7, loc="upper left")
    guardar(fig, "figA_1_empalmes.png")


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    for f in (fig5_1, fig5_2, fig5_3, fig6_1, fig6_3, fig6_4, fig6_5, fig7_1, fig7_2, figA_1):
        f()
    fig_abanico_deuda.main()


if __name__ == "__main__":
    main()
