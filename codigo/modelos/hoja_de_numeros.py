"""
hoja_de_numeros.py
==================
Reune en un solo archivo todas las cifras que cita el texto de la tesis, leidas de los
resultados guardados (fase24, fase24b, fase25, fase25b). Es la fuente de control para redactar y
revisar los capitulos: ningun numero del texto debe salir de otro lado.

Uso: python codigo/modelos/hoja_de_numeros.py
Salida: tesis_oficial_borradores/_hoja_de_numeros.md (documento interno, no se entrega)
"""

from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fase24_svarx_1996_2025 as f24  # noqa: E402
import fase25_simulacion_dsa_svarx as f25  # noqa: E402

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
T = BASE / "resultados" / "tablas"
SALIDA = BASE / "tesis_oficial_borradores" / "_hoja_de_numeros.md"


def n(x: float, d: int = 1) -> str:
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def iv(r: pd.DataFrame, k: str, f: float = 100, d: int = 1) -> str:
    return f"{n(r.loc[k, 'estimacion'] * f, d)} [{n(r.loc[k, 'p05'] * f, d)}; {n(r.loc[k, 'p95'] * f, d)}]"


def hall(rep: pd.DataFrame, est: float, k: str, nivel: float) -> tuple[float, float]:
    a = (1 - nivel) / 2
    q = rep[k].quantile([a, 1 - a])
    return 2 * est - q[1 - a], 2 * est - q[a]


def main() -> None:
    L: list[str] = ["# Hoja de números (generada por codigo/modelos/hoja_de_numeros.py)\n"]
    meta = json.loads((T / "fase25_federal_meta.json").read_text(encoding="utf-8"))
    r = pd.read_csv(T / "fase25_federal_resumen.csv", index_col=0)
    rep = pd.read_csv(T / "fase25_federal_replicas.csv")
    rc = pd.read_csv(T / "fase25_consolidada_resumen.csv", index_col=0)
    b = pd.read_csv(T / "fase24_federal_bootstrap.csv", index_col=0)
    bc = pd.read_csv(T / "fase24_consolidada_bootstrap.csv", index_col=0)
    rz = pd.read_csv(T / "fase24_federal_rezagos.csv")
    dg = pd.read_csv(T / "fase24_federal_diagnosticos.csv").set_index("prueba")["valor"]
    Y, X, quiebres = f24.cargar_datos("federal", 2)

    L.append("## Muestra y especificación")
    L.append(f"- Datos desde 1999T1; muestra efectiva {meta['muestra'][0]} a {meta['muestra'][1]}, {meta['trimestres_historicos']} trimestres.")
    L.append(f"- Rezagos: Schwarz elige {int(rz['p_sic'].iloc[0])}; Portmanteau de ese orden p = {n(rz.loc[rz.p == rz['p_sic'].iloc[0], 'portmanteau_12_p'].iloc[0], 3)}; orden elegido {meta['p']} (Portmanteau p = {n(dg['Portmanteau (12 rezagos)'], 3)}). AIC sin restricción: {int(rz['p_aic'].iloc[0])}; HQ: {int(rz.loc[rz.hqic.idxmin(), 'p'])}.")
    L.append(f"- Raíces máximas por orden: " + ", ".join(f"p={int(a)}: {n(c, 3)}{'' if e else ' (inestable)'}" for a, c, e in zip(rz.p, rz.modulo_raiz_max, rz.estable)))
    L.append(f"- Autovalor máximo del VAR principal: {n(meta['raiz_max_estimada'], 3)}; mediana de las réplicas {n(meta['raiz_max_mediana_replicas'], 3)}.")
    L.append(f"- Quiebres de Bai y Perron (deuda federal bruta 1996-2025): " + ", ".join(f"{q.year}T{q.quarter}" for q in quiebres))
    L.append(f"- Diagnósticos: normalidad multivariada p = {n(dg['Normalidad multivariada (p-valor)'], 3)}; ARCH-LM p: " + ", ".join(f"{k.split()[1]} {n(v, 3)}" for k, v in dg.items() if k.startswith("ARCH")))
    L.append(f"- Desvío de la variación trimestral de la FED en la muestra: {n(meta['sd_dfed'], 3)} pp. AR(1) del VIX: {n(meta['phi_vix'], 3)}; del nivel de la tasa de la FED: {n(meta['phi_fed'], 3)}.")
    L.append(f"- Proporción en pesos: federal {n(meta['alfa_pesos'], 3)} (MECON, dic-2025); consolidada {n(16.4 / 52.1, 3)} (FMI, cuadro 2). λ = {n(meta['lam'], 3)}. Desvío máximo de la identidad respecto de la senda del FMI: {n(meta['desvio_max_senda_fmi'], 2)} pp.")

    ru = pd.read_csv(T / "fase24b_raiz_unitaria.csv")
    L.append("- Raíz unitaria (ADF p / KPSS p / clasificación): " + "; ".join(f"{s}: {n(a, 3)} / {n(k, 3)} / {c}" for s, a, k, c in zip(ru.serie, ru.adf_p, ru.kpss_p, ru.clasificacion)))
    jo = pd.read_csv(T / "fase24b_johansen.csv")
    jn = jo[jo.variables == "niveles (sin crecimiento)"]
    L.append("- Johansen (niveles, traza vs crítico 5%): " + "; ".join(f"{a}: {n(t)} vs {n(c)}" for a, t, c in zip(jn.rango_nulo, jn.traza, jn.critico_95)))

    L.append("\n## Estimación (fase24, intervalos de Hall al 90%)")
    for nom, bb in (("federal", b), ("consolidada", bc)):
        L.append(f"- {nom}: reacción fiscal de impacto {n(bb.loc['rho_bohn', 'p50'], 4)} [{n(bb.loc['rho_bohn', 'p05'], 4)}; {n(bb.loc['rho_bohn', 'p95'], 4)}]; largo plazo {n(bb.loc['rho_largo_plazo', 'p50'], 3)} [{n(bb.loc['rho_largo_plazo', 'p05'], 3)}; {n(bb.loc['rho_largo_plazo', 'p95'], 3)}]")
        for v in f24.ENDOG[1:]:
            L.append(f"  - deuda → {v}: {n(bb.loc[f'deuda_a_{v}', 'p50'], 4)} [{n(bb.loc[f'deuda_a_{v}', 'p05'], 4)}; {n(bb.loc[f'deuda_a_{v}', 'p95'], 4)}]")
    f = b[b.index.str.startswith("fed_")]
    ex = f[(f.p05 > 0) | (f.p95 < 0)]
    L.append(f"- Respuestas a la FED: {len(ex)} de {len(f)} intervalos excluyen el cero: " + ", ".join(f"{i} {n(row.p50, 3)} [{n(row.p05, 3)}; {n(row.p95, 3)}]" for i, row in ex.iterrows()))

    L.append("\n## Simulación principal (deuda federal bruta, intervalos de Hall al 90%)")
    fc = pd.read_csv(T / "fase25_federal_fanchart.csv", index_col="anio")
    L.append("- Percentiles de la deuda (p5, p25, mediana, p75, p95): " + "; ".join(
        f"{a}: {n(fc.loc[a, 'p5'])}, {n(fc.loc[a, 'p25'])}, {n(fc.loc[a, 'p50'])}, {n(fc.loc[a, 'p75'])}, {n(fc.loc[a, 'p95'])}" for a in (2026, 2028, 2031, 2033, 2035)))
    L.append(f"- Senda base (identidad sin shocks): 2031 {n(r.loc['senda_base_d2031', 'estimacion'])}, 2035 {n(r.loc['senda_base_d2035', 'estimacion'])}.")
    for k, nom in [("base_p_noest_2031", "No estabilización 2031"), ("base_p_noest_2035", "No estabilización 2035"),
                   ("base_p_noest_sim_2031", "No estabilización 2031 con pb simulado"), ("base_p_sube2_2031", "Deuda 2031 > 2029"),
                   ("base_p_sube2_2035", "Deuda 2035 > 2033")]:
        L.append(f"- {nom}: {iv(r, k)} %")
    L.append(f"- Error de Monte Carlo 2031: {n(100 * r.loc['error_mc_p_noest_2031', 'estimacion'], 2)} pp.")
    for nivel in (0.95, 0.975):
        lo31, _ = hall(rep, r.loc["base_p_noest_2031", "estimacion"], "base_p_noest_2031", nivel)
        lo35, _ = hall(rep, r.loc["base_p_noest_2035", "estimacion"], "base_p_noest_2035", nivel)
        L.append(f"- Límite inferior al {int(nivel * 100 + 0.5) if nivel == 0.95 else 97.5}% (unilateral {n((1 - nivel) / 2 * 100, 2)}%): 2031 {n(100 * lo31)}, 2035 {n(100 * lo35)}.")
    L.append(f"- Ancho del abanico 2031: {iv(r, 'base_ancho_p5_p95_2031', 1)}; mediana 2031 {n(r.loc['base_d2031_mediana', 'estimacion'])}; media 2035 {n(r.loc['base_d2035_media', 'estimacion'])}.")
    L.append("- Varianza 2035 por bloque: " + "; ".join(f"{k[7:]} {iv(r, k, 1)}" for k in r.index if k.startswith("vshare_")))
    L.append(f"- H1a, no fiscal menos fiscal: {iv(r, 'h1a_nofiscal_menos_fiscal', 1)} puntos.")
    for k in ("dif_fed_1de_p_noest_2031", "dif_fed_1de_p_noest_2035", "dif_fed_1de_d2035", "dif_fed_2022_2025_p_noest_2031",
              "dif_fed_2022_2025_p_noest_2035", "dif_fed_2022_2025_d2035"):
        f_ = 1 if k.endswith("d2035") else 100
        lo, hi = hall(rep, r.loc[k, "estimacion"], k, 0.95)
        L.append(f"- {k}: {iv(r, k, f_)}; al 95% (Bonferroni para dos escenarios): [{n(lo * f_)}; {n(hi * f_)}]")
    d_dir = r.loc["dif_fed_2022_2025_d2035_solo_costo_directo", "estimacion"]
    L.append(f"- Costo directo de la senda de la FED en la deuda 2035: {n(d_dir)} pp de {n(r.loc['dif_fed_2022_2025_d2035', 'estimacion'])} ({n(100 * d_dir / r.loc['dif_fed_2022_2025_d2035', 'estimacion'], 0)}%).")
    ffr = pd.read_csv(BASE / "datos" / "procesados" / "tasa_fed_trimestral_1996_2025.csv", parse_dates=["Date"], index_col="Date")["fedfunds"]
    c = ffr.loc["2021-12-31":"2025-12-31"]
    L.append(f"- Senda de la FED 2022-2025: de {n(c.iloc[0], 2)} (2021T4) a máximo {n(c.max(), 2)} y {n(c.iloc[-1], 2)} (2025T4); nivel final {n(c.iloc[-1] - c.iloc[0], 2)} pp por encima.")

    su = pd.read_csv(T / "fase25_federal_suficiencia.csv")
    pbh = pd.read_csv(BASE / "datos" / "procesados" / "resultado_primario_1996_2025.csv", index_col=0, parse_dates=True)
    anual = pbh.loc[pbh.index.quarter == 4, ["pb_pib", "pb_pib_sin_rentas"]].loc["1999":]
    mx = anual["pb_pib"].max()
    L.append(f"\n## Suficiencia del superávit (H1a, complemento)")
    L.append(f"- Máximo anual del resultado primario 1999-2025 (definición del FMI, con rentas): {n(mx, 2)} en {anual['pb_pib'].idxmax().year}; sin rentas: {n(anual['pb_pib_sin_rentas'].max(), 2)}.")
    p_mx = np.interp(mx, su.pb_2031, su.p_noest_2031)
    L.append(f"- Con el resultado primario en el máximo histórico en todos los años (pb 2031 = {n(mx, 2)}): P(2031) = {n(100 * p_mx)}%.")
    cruce = su[su.p_noest_2031 <= 0.01].iloc[0]
    L.append(f"- Primer desplazamiento con P(2031) ≤ 1%: +{n(cruce.dpb, 2)} pp, pb 2026 = {n(cruce.pb_2026)}% y pb 2031 = {n(cruce.pb_2031)}%.")
    imin = su.p_noest_2035.idxmin()
    L.append(f"- P(2035) mínima {n(100 * su.p_noest_2035[imin], 2)}% con +{n(su.dpb[imin], 2)} pp; después sube a {n(100 * su.p_noest_2035.iloc[-1], 2)}% con +{n(su.dpb.iloc[-1], 2)} (no monótona).")

    L.append("\n## Extensión consolidada")
    L.append(f"- No estabilización 2031 {iv(rc, 'base_p_noest_2031')}; 2035 {iv(rc, 'base_p_noest_2035')}; ancho {n(rc.loc['base_ancho_p5_p95_2031', 'estimacion'])}; no fiscal menos fiscal {iv(rc, 'h1a_nofiscal_menos_fiscal', 1)}; senda FED prob 2035 {iv(rc, 'dif_fed_2022_2025_p_noest_2035')}; deuda {iv(rc, 'dif_fed_2022_2025_d2035', 1)}; senda base 2031 {n(rc.loc['senda_base_d2031', 'estimacion'])}, 2035 {n(rc.loc['senda_base_d2035', 'estimacion'])}.")

    L.append("\n## Shocks a la manera del FMI")
    for s in ("federal_fmi", "consolidada_fmi"):
        v = pd.read_csv(T / f"fase25_{s}_resumen.csv", index_col=0)["valor"]
        L.append(f"- {s}: P2031 {n(100 * v['p_noest_2031'])}%, P2035 {n(100 * v['p_noest_2035'])}%, ancho {n(v['ancho_p5_p95_2031'])}.")
    dgn = pd.read_csv(T / "fase25b_diagnostico_abanico_fmi.csv")
    L.append("- Diagnóstico (P2031, P2035, ancho): " + "; ".join(f"{a}: {n(100 * b_)}, {n(100 * c_)}, {n(d_)}" for a, b_, c_, d_ in dgn.values))

    imp = pd.read_csv(T / "fase25_federal_impulsores_historicos.csv", index_col=0)
    sin02 = imp.drop(2002)
    L.append(f"- Impulsores {imp.index.min()}-{imp.index.max()}: depreciación real media {n(imp.z.mean())}% (sin 2002: {n(sin02.z.mean())}%); "
             f"años con depreciación sobre la media {n(100 * ((imp.z - imp.z.mean()) > 0).mean(), 0)}% (sin 2002: {n(100 * ((sin02.z - sin02.z.mean()) > 0).mean(), 0)}%); "
             f"correlación crecimiento-depreciación {n(imp.corr().loc['g', 'z'], 2)}, crecimiento-resultado primario {n(imp.corr().loc['g', 'pb'], 2)}.")
    L.append("\n## Robustez: rango entre especificaciones del SVARX (ver Apéndice A.8)")
    vals = {}
    for f_ in T.glob("fase25_*_resumen.csv"):
        s = f_.stem[7:-8]
        if "fmi" in s or not (s == "federal" or s == "consolidada" or s.startswith("federal_")):
            continue
        rr = pd.read_csv(f_, index_col=0)
        vals[s] = rr
    for k in ("base_p_noest_2031", "base_p_noest_2035"):
        lo = min((v.loc[k, "p05"], s) for s, v in vals.items())
        e = sorted((v.loc[k, "estimacion"], s) for s, v in vals.items())
        L.append(f"- {k}: estimaciones entre {n(100 * e[0][0])} ({e[0][1]}) y {n(100 * e[-1][0])} ({e[-1][1]}); menor límite inferior {n(100 * lo[0])} ({lo[1]}).")
    k = "h1a_nofiscal_menos_fiscal"
    lo = min((v.loc[k, "p05"], s) for s, v in vals.items())
    L.append(f"- {k}: menor límite inferior {n(lo[0])} ({lo[1]}); todas las especificaciones excluyen el cero: {all(v.loc[k, 'p05'] > 0 for v in vals.values())}.")
    for k in ("dif_fed_2022_2025_p_noest_2035", "dif_fed_2022_2025_d2035", "dif_fed_1de_p_noest_2035", "dif_fed_1de_d2035"):
        no = sorted(s for s, v in vals.items() if v.loc[k, "p05"] <= 0 <= v.loc[k, "p95"])
        L.append(f"- {k}: incluyen el cero en {len(no)} de {len(vals)}: {', '.join(no) if no else 'ninguna'}.")
    SALIDA.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"[OK] {SALIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
