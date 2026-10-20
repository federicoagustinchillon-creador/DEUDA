"""
verificar_consistencia.py
=========================
Control de consistencia de todo el texto de la tesis y de los documentos para el director. Falla
(codigo de salida 1) si encuentra alguna de estas inconsistencias:

  - un periodo de estudio distinto de la ventana unica 1996-2025 (proyeccion 2026-2035);
  - nombres alternativos del riesgo pais (EMBI+, EMBI Global, spread sin cursiva, "diferencial
    soberano") o "spread" fuera de su definicion;
  - nombres de deuda fuera de la nomenclatura ("deuda consolidada neta");
  - Cholesky mencionado sin decir que es robustez;
  - numeros con decimales que no estan en la hoja de numeros, el apendice o las decisiones;
  - rayas, conectores de relleno y contrastes retoricos (filtros de estilo del director).

Uso: python tesis_oficial_borradores/verificar_consistencia.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
TEXTOS = ["resumen.md", "introduccion.md", "antecedentes.md", "marco_teorico.md", "metodologia.md", "datos.md",
          "resultados.md", "discusion.md", "conclusiones.md", "plan_de_labor.md"]
REGLAS: list[tuple[str, str]] = [
    (r"\b(1997|1998|1999|2000|2004)\s*[-–]\s*2025\b", "período distinto de la ventana 1996-2025"),
    (r"\b2000T3\b|\b1999T1\b", "fecha de inicio distinta de la ventana"),
    (r"EMBI\s*\+|EMBI\+|EMBI Global", "nombre alternativo del EMBI"),
    (r"(?<!\*)\bspreads?\b(?!\*)", "spread sin cursiva o fuera de la definición"),
    (r"diferencial soberano", "nombre alternativo del riesgo país"),
    (r"deuda consolidada neta", "nombre de deuda fuera de la nomenclatura"),
    (r"[—–]", "raya"),
    (r"\b(Además|Asimismo|Por último|Dicho de otro modo|Es decir|En este sentido|Cabe destacar|Resta determinar)\b",
     "conector de relleno"),
    (r"\bno solo\b|\bno sólo\b", "contraste retórico"),
    (r"\bno es [^.]{0,60}, sino\b", "contraste retórico"),
]
PERMITIDO_PERIODO = re.compile(r"desde 1999|datos desde 2004|desde 2004")


def numeros_validos() -> set[str]:
    t = "".join((BASE / f).read_text(encoding="utf-8") for f in ("_hoja_de_numeros.md", "apendice.md", "_decisiones_finales.md"))
    nums = set(re.findall(r"-?\d+,\d+", t))
    # Las columnas con dos decimales del Apéndice se citan en el texto redondeadas a uno.
    for x in [x for x in nums if len(x.split(",")[1]) == 2]:
        nums.add(f"{float(x.replace(',', '.')):.1f}".replace(".", ","))
    return nums


def main() -> None:
    problemas = []
    validos = numeros_validos()
    for f in TEXTOS:
        texto = (BASE / f).read_text(encoding="utf-8")
        if f == "introduccion.md":
            texto = texto[: texto.index("## Referencias\n")]
        if f == "plan_de_labor.md":
            texto = texto[: texto.index("# 5. Referencias")]
        for n, linea in enumerate(texto.splitlines(), start=1):
            for patron, motivo in REGLAS:
                for m in re.finditer(patron, linea):
                    ctx = linea[max(0, m.start() - 40): m.end() + 40]
                    if motivo.startswith("período") and PERMITIDO_PERIODO.search(ctx):
                        continue
                    problemas.append(f"{f}:{n}: {motivo}: ...{ctx}...")
            if "Cholesky" in linea and not re.search(r"robustez|alternativ|variante", linea, re.I):
                problemas.append(f"{f}:{n}: Cholesky sin indicar que es robustez")
            if f not in ("introduccion.md", "plan_de_labor.md", "antecedentes.md", "marco_teorico.md"):
                for num in re.findall(r"(?<![\w.,])-?\d+,\d+", linea):
                    if num not in validos and num.lstrip("-") not in validos and num not in {"0,25", "0,5", "0,15", "0,40"}:
                        problemas.append(f"{f}:{n}: número sin fuente en la hoja: {num}")
    for p in problemas:
        print(p)
    print(f"\n{len(problemas)} problemas")
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
