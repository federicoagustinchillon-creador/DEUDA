"""
fase8_deuda_consolidada.py
===========================
Mejora Dimensión IV: consolidación de la deuda del Sector Público Nacional
No Financiero (SPNF, `deuda_pib`) con los pasivos remunerados del BCRA
(LEBAC/NOBAC, LELIQ/NOTALIQ y posición neta de pases, `pasivos_bcra_pib`,
construidos en `codigo/ingesta_datos/ingesta_bcra_pasivos.py` a partir de series
oficiales del BCRA v4.0 y de PIB nominal INDEC).

  deuda_consolidada_pib_t = deuda_pib_t + pasivos_bcra_pib_t

No se aplica neteo adicional entre ambas series: `deuda_pib` (SPNF) y
`pasivos_bcra_ars` (pasivos del BCRA frente al sistema financiero) son
instrumentos emitidos por entidades y a acreedores distintos, por lo que no
existe una tenencia cruzada directa entre ambos stocks que deba eliminarse
(a diferencia de, por ejemplo, las Letras Intransferibles que el Tesoro
coloca en el activo del BCRA como contrapartida de reservas, que ya están
implícitamente netas en la cifra de deuda "neta" del SPNF y no vuelven a
sumarse aquí).

Salidas:
  - datos/dataset_consolidado_real.csv actualizado con las columnas
    `pasivos_bcra_pib` y `deuda_consolidada_pib`.
  - resultados/tablas/fase8_deuda_consolidada.csv: comparación trimestral.
  - tesis/figuras/figura_8_1_deuda_consolidada.png: SPNF vs SPNF+BCRA.
"""

import os
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
import warnings

warnings.filterwarnings("ignore")

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
CSV_PATH = BASE_DIR / "datos" / "dataset_consolidado_real.csv"
BCRA_PASIVOS_PATH = BASE_DIR / "datos" / "procesados" / "bcra_pasivos_trimestral.csv"
LATEX_DIR = BASE_DIR / "tesis" / "figuras"
TABLES_DIR = BASE_DIR / "resultados" / "tablas"
os.makedirs(TABLES_DIR, exist_ok=True)


def main():
    print("=" * 75)
    print(" FASE 8: Consolidación de la Deuda SPNF + Pasivos Remunerados BCRA")
    print("=" * 75)

    df = pd.read_csv(CSV_PATH, parse_dates=["Date"], index_col="Date")
    bcra = pd.read_csv(BCRA_PASIVOS_PATH, parse_dates=["fecha"], index_col="fecha")

    # El dataset consolidado puede ya traer estas columnas de una ejecución
    # previa de este mismo script; se recalculan siempre desde la fuente BCRA
    # en lugar de arrastrar valores viejos, para que el script sea re-ejecutable
    # de forma idempotente sin colisión de nombres en el merge.
    columnas_derivadas = ["pasivos_bcra_pib", "pib_nominal_es_extrapolado", "deuda_consolidada_pib"]
    df = df.drop(columns=[c for c in columnas_derivadas if c in df.columns])

    print(f"\n[1/4] Fusionando pasivos_bcra_pib ({len(bcra)} trimestres) "
          f"con el dataset consolidado ({len(df)} trimestres)...")
    df = df.merge(bcra[["pasivos_bcra_pib", "pib_nominal_es_extrapolado"]],
                   left_index=True, right_index=True, how="left")
    df["deuda_consolidada_pib"] = df["deuda_pib"] + df["pasivos_bcra_pib"]

    print("\n[2/4] Estadísticas comparativas (deuda SPNF vs. deuda consolidada SPNF+BCRA)...")
    resumen = df[["deuda_pib", "pasivos_bcra_pib", "deuda_consolidada_pib"]].describe().round(2)
    print(resumen.to_string())

    brecha_media = df["pasivos_bcra_pib"].mean()
    pico = df["pasivos_bcra_pib"].idxmax()
    print(f"\n -> Brecha promedio (2004-2025) por cuasi-fiscal BCRA: {brecha_media:.2f} pp del PIB")
    print(f" -> Pico de pasivos remunerados BCRA/PIB: {df.loc[pico, 'pasivos_bcra_pib']:.2f}% "
          f"en {pico.date()} (deuda SPNF={df.loc[pico, 'deuda_pib']:.1f}%, "
          f"deuda consolidada={df.loc[pico, 'deuda_consolidada_pib']:.1f}%)")

    print("\n[3/4] Estacionariedad de la serie consolidada (ADF/KPSS, robustez)...")
    d_cons = df["deuda_consolidada_pib"].dropna()
    adf_p = adfuller(d_cons, autolag="AIC")[1]
    kpss_p = kpss(d_cons, regression="c", nlags="auto")[1]
    adf_p_diff = adfuller(d_cons.diff().dropna(), autolag="AIC")[1]
    kpss_p_diff = kpss(d_cons.diff().dropna(), regression="c", nlags="auto")[1]
    print(f" -> Niveles:   ADF p={adf_p:.4f} | KPSS p={kpss_p:.4f}")
    print(f" -> Diferencias: ADF p={adf_p_diff:.4f} | KPSS p={kpss_p_diff:.4f}")

    print("\n[4/4] Guardando resultados...")
    df.to_csv(CSV_PATH)
    print(f" -> Dataset consolidado actualizado: {CSV_PATH}")

    tabla = df[["deuda_pib", "pasivos_bcra_pib", "deuda_consolidada_pib"]].copy()
    tabla.to_csv(TABLES_DIR / "fase8_deuda_consolidada.csv")
    pd.DataFrame([{
        "adf_p_nivel": adf_p, "kpss_p_nivel": kpss_p,
        "adf_p_diff": adf_p_diff, "kpss_p_diff": kpss_p_diff,
        "brecha_media_pp_pib": brecha_media,
        "pico_pasivos_bcra_pib": df["pasivos_bcra_pib"].max(),
        "fecha_pico": str(pico.date()),
    }]).to_csv(TABLES_DIR / "fase8_deuda_consolidada_diagnosticos.csv", index=False)
    print(f" -> Tabla comparativa: {TABLES_DIR / 'fase8_deuda_consolidada.csv'}")

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["deuda_pib"], label="Deuda SPNF / PIB (original)",
              color="#0B3C5D", linewidth=1.8)
    plt.plot(df.index, df["deuda_consolidada_pib"],
              label="Deuda consolidada SPNF + Pasivos Remunerados BCRA / PIB",
              color="#B33951", linewidth=1.8, linestyle="--")
    plt.fill_between(df.index, df["deuda_pib"], df["deuda_consolidada_pib"],
                      color="#B33951", alpha=0.15, label="Brecha cuasi-fiscal (BCRA)")
    plt.title("Deuda Pública: SPNF vs. Consolidada con Pasivos Remunerados del BCRA")
    plt.xlabel("Trimestre")
    plt.ylabel("% del PIB")
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out_fig = LATEX_DIR / "figura_8_1_deuda_consolidada.png"
    plt.savefig(out_fig, dpi=300)
    plt.close()
    print(f" -> Gráfico: {out_fig}")

    print("\n[OK] Fase 8 completa.")


if __name__ == "__main__":
    main()
