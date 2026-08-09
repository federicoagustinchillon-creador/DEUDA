"""
H3 (optima) -- Descomposicion ilustrativa del Ajuste Stock-Flujo (SF_t) para
2005, 2018 y 2020, usando la identidad d_t = (1+r_t)/(1+g_t) d_{t-1} - pb_t + SF_t.

Fuentes:
 - d_t, d_{t-1}, pb_t: dataset propio de la tesis (deuda_consolidada_pib, pb_pib),
   datos/dataset_consolidado_real.csv.
 - r_t (tasa de interes real efectiva): APROXIMACION construida en tres pasos a
   partir de series del IMF WEO DataMapper (perimetro "general government", NO
   idéntico al perimetro SPNF+BCRA de la tesis):
     1. interes_t (%PIB) = balance_primario_IMF_t - balance_global_IMF_t
     2. tasa nominal implicita_t = interes_t / deuda_IMF_{t-1}
     3. tasa real_t = Fisher[(1+tasa nominal_t)/(1+inflacion_IMF_t)] - 1
 - g_t (crecimiento real del PIB): PIB_real (indice), dataset propio de la tesis.

Esto es una aproximacion ilustrativa, NO una serie de tasa de interes real
propia de la tesis: mezcla el perimetro de deuda "general government" del FMI
(para estimar la tasa implicita) con el perimetro SPNF+BCRA propio de la tesis
(para d_t, d_{t-1}, pb_t). Se documenta explicitamente como limitacion.
"""
import json
import pathlib
import pandas as pd

current_file = pathlib.Path(__file__).resolve()
BASE_DIR = current_file.parent
while BASE_DIR.parent != BASE_DIR:
    if (BASE_DIR / "Bibliografia").exists() and (BASE_DIR / "datos").exists():
        break
    BASE_DIR = BASE_DIR.parent


IMF_DIR = BASE_DIR / "Bibliografia" / "descargas_verificacion" / "imf_weo_datamapper_ARG"


overall = json.load(open(IMF_DIR / "GGXCNL_NGDP_overall_balance.json"))["values"]["GGXCNL_NGDP"]["ARG"]
primary = json.load(open(IMF_DIR / "pb_primary_balance.json"))["values"]["pb"]["ARG"]
debt_imf = json.load(open(IMF_DIR / "GGXWDG_NGDP_gross_debt.json"))["values"]["GGXWDG_NGDP"]["ARG"]
infl = json.load(open(IMF_DIR / "PCPIPCH_inflation.json"))["values"]["PCPIPCH"]["ARG"]

df = pd.read_csv(BASE_DIR / "datos" / "dataset_consolidado_real.csv", parse_dates=['Date'], index_col='Date')
if "deuda_consolidada_pib" not in df.columns:
    if "pasivos_bcra_pib" in df.columns:
        df["deuda_consolidada_pib"] = df["deuda_pib"] + df["pasivos_bcra_pib"]
    else:
        df["deuda_consolidada_pib"] = df["deuda_pib"]

def annual_d(year):
    return df.loc[f"{year}-12-31", "deuda_consolidada_pib"] / 100


def annual_pb(year):
    return df.loc[f"{year}", "pb_pib"].sum() / 100

def annual_g_real(year):
    pib_t = df.loc[f"{year}", "PIB_real"].sum()
    pib_t1 = df.loc[f"{year-1}", "PIB_real"].sum()
    return pib_t / pib_t1 - 1

print(f"{'Anio':<6}{'d_t':>8}{'d_t-1':>8}{'pb_t':>8}{'i_nom(FMI)':>12}{'infl(FMI)':>10}{'r_real':>9}{'g_real':>9}{'SF_t implicito':>16}")
resultados = {}
for year in [2005, 2018, 2020]:
    d_t = annual_d(year)
    d_t1 = annual_d(year - 1)
    pb_t = annual_pb(year)
    interes_pib = primary[str(year)] - overall[str(year)]
    i_nom = interes_pib / debt_imf[str(year - 1)]
    pi = infl[str(year)] / 100
    r_real = (1 + i_nom) / (1 + pi) - 1
    g_real = annual_g_real(year)
    sf_t = d_t - (1 + r_real) / (1 + g_real) * d_t1 + pb_t
    resultados[year] = dict(d_t=d_t, d_t1=d_t1, pb_t=pb_t, i_nom=i_nom, pi=pi, r_real=r_real, g_real=g_real, sf_t=sf_t)
    print(f"{year:<6}{d_t*100:>7.1f}%{d_t1*100:>7.1f}%{pb_t*100:>7.1f}%{i_nom*100:>11.1f}%{pi*100:>9.1f}%{r_real*100:>8.1f}%{g_real*100:>8.1f}%{sf_t*100:>15.1f}%")

print()
print("Nota: SF_t > 0 significa que la deuda crecio mas de lo que explican el diferencial r-g y el resultado primario (efecto de valuacion/reconocimiento neto positivo sobre el stock).")

# Persistencia a CSV para trazabilidad (mismo criterio que el resto de las
# fases: todo resultado intermedio citado en la tesis debe quedar en
# resultados/tablas/, no solo impreso por consola).
tabla = pd.DataFrame.from_dict(resultados, orient="index")
tabla.index.name = "anio"
tabla.to_csv("resultados/tablas/fase15_sft_decomposicion_ilustrativa.csv")
print("\nGuardado: resultados/tablas/fase15_sft_decomposicion_ilustrativa.csv")
