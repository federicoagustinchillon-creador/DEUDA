"""Veredicto de H1a, H1b y H2 por especificación, con los criterios de la tesis (metodología, 4.6)."""
import pathlib

import pandas as pd

AQUI = pathlib.Path(__file__).resolve().parents[3] / "resultados" / "tablas" / "robustez_diferencias"
CORRIDAS = {"niveles": ("niveles", ""), "mixto": ("mixto", ""), "diferencias": ("diferencias", ""),
            "mixto_p1": ("mixto", "_p1"), "diferencias_p4": ("diferencias", "_p4")}
DPB_MAX = 1.0  # desplazamiento que lleva el resultado primario de 2031 a su máximo de 1996-2025 (3,3%)
filas = []
for nombre, (carpeta, suf) in CORRIDAS.items():
    r = AQUI / carpeta / f"fase25_federal{suf}_resumen.csv"
    s = AQUI / carpeta / f"fase25_federal{suf}_suficiencia.csv"
    if not r.exists() or not s.exists():
        continue
    r = pd.read_csv(r, index_col=0)
    s = pd.read_csv(s).set_index("dpb")
    g = lambda k, c="estimacion": float(r.loc[k, c])
    h1a_i = g("h1a_nofiscal_menos_fiscal", "p05") > 0
    p_max = float(s.loc[DPB_MAX, "p_noest_fmi_2031"])
    h1a_ii = p_max > 0.01
    h1b = g("base_p_noest_fmi_2031", "p05") > 0.01 and g("base_p_noest_fmi_2035", "p05") > 0.03
    esc = []
    for e in ("fed_1de", "fed_2022_2025"):
        prob = g(f"dif_{e}_p_noest_fmi_2035", "p05") > 0 or g(f"dif_{e}_p_noest_fmi_2035", "p95") < 0
        deuda = g(f"dif_{e}_d2035", "p05") > 0 or g(f"dif_{e}_d2035", "p95") < 0
        esc.append((prob, deuda))
    n_ok = sum(a + b for a, b in esc)
    h2 = "respaldada" if n_ok == 4 else ("parcial" if n_ok > 0 else "no respaldada")
    filas.append({
        "spec": nombre,
        "fiscal_%var": f"{g('vshare_fiscal'):.1f} [{g('vshare_fiscal','p05'):.1f}; {g('vshare_fiscal','p95'):.1f}]",
        "nofiscal-fiscal_p05": round(g("h1a_nofiscal_menos_fiscal", "p05"), 1),
        "H1a(i)": h1a_i, "p2031_en_max_pb": round(100 * p_max, 2), "H1a(ii)": h1a_ii,
        "H1a": "respaldada" if h1a_i and h1a_ii else "no respaldada",
        "p_fmi_2031": f"{100*g('base_p_noest_fmi_2031'):.1f} [{100*g('base_p_noest_fmi_2031','p05'):.1f}; {100*g('base_p_noest_fmi_2031','p95'):.1f}]",
        "p_fmi_2035": f"{100*g('base_p_noest_fmi_2035'):.1f} [{100*g('base_p_noest_fmi_2035','p05'):.1f}; {100*g('base_p_noest_fmi_2035','p95'):.1f}]",
        "H1b": "respaldada" if h1b else "no respaldada",
        "fed2225_dprob2035": f"{100*g('dif_fed_2022_2025_p_noest_fmi_2035'):.1f} [{100*g('dif_fed_2022_2025_p_noest_fmi_2035','p05'):.1f}; {100*g('dif_fed_2022_2025_p_noest_fmi_2035','p95'):.1f}]",
        "fed2225_ddeuda2035": f"{g('dif_fed_2022_2025_d2035'):.1f} [{g('dif_fed_2022_2025_d2035','p05'):.1f}; {g('dif_fed_2022_2025_d2035','p95'):.1f}]",
        "fed1de_dprob2035": f"{100*g('dif_fed_1de_p_noest_fmi_2035'):.1f} [{100*g('dif_fed_1de_p_noest_fmi_2035','p05'):.1f}; {100*g('dif_fed_1de_p_noest_fmi_2035','p95'):.1f}]",
        "fed1de_ddeuda2035": f"{g('dif_fed_1de_d2035'):.1f} [{g('dif_fed_1de_d2035','p05'):.1f}; {g('dif_fed_1de_d2035','p95'):.1f}]",
        "H2": h2,
        "deuda2035_media": round(g("base_d2035_media"), 1),
    })
t = pd.DataFrame(filas).set_index("spec").T
t.to_csv(AQUI / "veredictos.csv")
pd.set_option("display.width", 250, "display.max_colwidth", 40)
print(t.to_string())
