"""
extraer_escenario_base_fmi_cr26105.py
=====================================
Extrae del PDF del FMI (2026), Informe de Pais No. 26/105 (Articulo IV 2026 y segunda revision
del EFF, staff report del 8 de mayo de 2026), el escenario base del analisis de sostenibilidad
(anexo SRDSF, Table 6, p. 77 impresa = p. 81 del PDF) y las metricas del abanico (Table 7, p. 78).

La lectura es por coordenadas (PyMuPDF): cada fila se ubica por su etiqueta y cada valor se asigna
al anio cuya columna esta mas cerca en x. No hay cifras tipeadas a mano.

Uso: python codigo/ingesta_datos/extraer_escenario_base_fmi_cr26105.py
Salida: datos/procesados/escenario_base_fmi_cr26105.csv (mismo formato que escenario_base_fmi_cr2595.csv)
"""

from __future__ import annotations

import pathlib
import re
from collections import defaultdict

import fitz  # PyMuPDF
import pandas as pd

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
PDF = BASE / "Bibliografia" / "descargas_verificacion" / "imf_cr26105_argentina_art4_second_review_eff_may2026.pdf"
SALIDA = BASE / "datos" / "procesados" / "escenario_base_fmi_cr26105.csv"
PAG_T6, PAG_T7 = 80, 81  # indices 0-based del PDF (paginas impresas 77 y 78)

# etiqueta de la fila en la Table 6 -> nombre de variable (mismos nombres srd_* que el CSV de CR 25/95)
FILAS = {
    "Public debt": "srd_deuda_publica",
    "Noninterest revenues": "srd_ingresos_no_intereses",
    "Noninterest expenditures": "srd_gastos_no_intereses",
    "Contribution of residual": "srd_residuo",
    "Relative inflation": "srd_inflacion_relativa",
    "Gross financing needs": "srd_necesidades_financiamiento_brutas",
    "Real GDP growth (percent)": "srd_pib_real_crecimiento",
    "Inflation (GDP deflator; percent)": "srd_inflacion_deflactor",
    "Effective interest rate (percent)": "srd_tasa_interes_efectiva",
}
NUM = re.compile(r"^-?\d+\.\d\.?$")


def tabla6() -> pd.DataFrame:
    pagina = fitz.open(PDF)[PAG_T6]
    filas: dict[int, list[tuple[float, str]]] = defaultdict(list)
    for x0, y0, _x1, _y1, palabra, *_ in pagina.get_text("words"):
        filas[round(y0)].append((x0, palabra))
    anios: dict[int, float] = {}
    for y, palabras in filas.items():
        cand = [(x, int(w)) for x, w in palabras if re.fullmatch(r"20[23]\d", w)]
        if len(cand) >= 10:
            anios = {a: x for x, a in cand}
            break
    if not anios:
        raise ValueError("No se encontro la fila de anios de la Table 6")
    registros = []
    for y, palabras in sorted(filas.items()):
        texto = " ".join(w for _, w in sorted(palabras) if not NUM.match(w))
        for etiqueta, var in FILAS.items():
            if texto.strip() == etiqueta:
                valores = [(x, float(w.rstrip("."))) for x, w in palabras if NUM.match(w)]
                if len(valores) != len(anios):
                    raise ValueError(f"{etiqueta}: {len(valores)} valores para {len(anios)} anios")
                for x, v in valores:
                    anio = min(anios, key=lambda a: abs(anios[a] - x))
                    registros.append({"variable": var, "anio": anio, "valor": v, "unidad": "% del PIB o % anual",
                                      "pagina": 77, "cuadro": "Table 6 (Argentina: Baseline Scenario)",
                                      "estado": "estimado" if anio == 2025 else "proyectado"})
    df = pd.DataFrame(registros)
    faltan = set(FILAS.values()) - set(df["variable"])
    if faltan:
        raise ValueError(f"Filas no encontradas en la Table 6: {faltan}")
    return df


def tabla7() -> pd.DataFrame:
    texto = fitz.open(PDF)[PAG_T7].get_text()
    out = []
    for patron, var in ((r"Fanchart width\s+(\d+\.\d)", "srd_ancho_abanico"),
                        (r"non-\s*(\d+\.\d)", "srd_prob_no_estabilizacion"),
                        (r"Debt fanchart index \(DFI\)\s+(\d+\.\d)", "srd_dfi")):
        m = re.search(patron, texto)
        if not m:
            raise ValueError(f"No se encontro {var} en la Table 7")
        out.append({"variable": var, "anio": 2031, "valor": float(m.group(1)), "unidad": "% del PIB o %",
                    "pagina": 78, "cuadro": "Table 7 (Medium-Term Risk Analysis)", "estado": "proyectado"})
    return pd.DataFrame(out)


def main() -> None:
    df = pd.concat([tabla6(), tabla7()], ignore_index=True)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA, index=False)
    piv = df[df.cuadro.str.startswith("Table 6")].pivot(index="anio", columns="variable", values="valor")
    piv["pb"] = piv["srd_ingresos_no_intereses"] - piv["srd_gastos_no_intereses"]
    print(piv.round(1).to_string())
    print(df[df.cuadro.str.startswith("Table 7")][["variable", "valor"]].to_string(index=False))
    print(f"[OK] {SALIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
