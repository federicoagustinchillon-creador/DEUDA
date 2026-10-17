"""
generar_latex.py
================
Sincroniza la version LaTeX de la tesis (tesis/capitulos/*.tex) con los borradores Markdown de
esta carpeta, que son la fuente unica del texto. El Word para el grupo (generar_docx_grupo.py) y
el PDF (tesis/fuente/Tesis.tex) salen de los mismos .md, de modo que no pueden divergir.

Que hace:
  - Convierte cada capitulo con pandoc (markdown -> latex, capitulos como \\chapter).
  - Saca la numeracion manual de los titulos ("## 4.5 Rezagos" -> "## Rezagos"): LaTeX numera solo.
  - Las ecuaciones $...$ quedan como matematica LaTeX (en el Word van como texto plano).
  - Las figuras se referencian por nombre de archivo (Tesis.tex define \\graphicspath).
  - Resumen (resumen.md) y Referencias (referencias_y_notas.md, sin las notas para el grupo).

Uso:
    python tesis_oficial_borradores/generar_latex.py [--compilar]

Con --compilar corre xelatex dos veces en tesis/fuente y copia el PDF a tesis/Tesis.pdf.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
CAPS = BASE.parent / "tesis" / "capitulos"
FUENTE = BASE.parent / "tesis" / "fuente"

# archivo .md -> archivo .tex de destino (en el orden de la tesis)
CAPITULOS: dict[str, str] = {
    "introduccion.md": "01_introduccion.tex",
    "antecedentes.md": "02_antecedentes.tex",
    "marco_teorico.md": "03_marco_teorico.tex",
    "metodologia.md": "04_metodologia.tex",
    "datos.md": "05_datos.tex",
    "resultados.md": "06_resultados.tex",
    "discusion.md": "07_discusion.tex",
    "conclusiones.md": "08_conclusiones.tex",
    "apendice.md": "09_apendice.tex",
}


def _limpiar(md: str) -> str:
    """Quita la numeracion manual de los titulos y la ruta de las figuras."""
    md = re.sub(r"^(#{1,6})\s+\d+(?:\.\d+)*\.?\s+", r"\1 ", md, flags=re.M)
    md = re.sub(r"^(#{1,6})\s+[A-Z]\.\d+\s+", r"\1 ", md, flags=re.M)  # A.1, A.2 del apendice
    md = re.sub(r"!\[Figura [A-Z0-9]+\.\d+\.\s*", "![", md)  # LaTeX numera la figura (6.2, A.1)
    return md.replace("../tesis/figuras/", "")


def _cuerpo_introduccion() -> str:
    intro = (BASE / "introduccion.md").read_text(encoding="utf-8")
    inicio = intro.index("## 1.1 Contextualización")
    fin = intro.index("## Referencias\n")
    return "# 1. Introducción\n\n" + intro[inicio:fin].rstrip().rstrip("-").rstrip()


def _cortes_texttt(tex: str) -> str:
    """Permite cortar rutas y nombres de archivo largos (\\texttt) en '_' y '/', para que no
    desborden las celdas de las tablas."""
    def cortar(m: re.Match) -> str:
        return "\\texttt{" + m.group(1).replace("\\_", "\\_\\allowbreak{}").replace("/", "/\\allowbreak{}") + "}"
    return re.sub(r"\\texttt\{([^{}]*)\}", cortar, tex)


def _epigrafe_corto(tex: str) -> str:
    """\\caption{Oracion 1. Resto} -> \\caption[Oracion 1]{Oracion 1. Resto}, para que el indice
    de figuras muestre solo el titulo y no el epigrafe completo."""
    salida, i = [], 0
    while (k := tex.find("\\caption{", i)) != -1:
        j, nivel = k + len("\\caption{"), 1
        while nivel:
            nivel += {"{": 1, "}": -1}.get(tex[j], 0)
            j += 1
        cuerpo = tex[k + len("\\caption{"): j - 1]
        corto = re.split(r"(?<=[A-Za-záéíóú0-9)])\.\s+", cuerpo, maxsplit=1)[0].rstrip(".")
        corto = re.sub(r"\s+", " ", corto)
        salida.append(tex[i:k] + f"\\caption[{corto}]{{{cuerpo}}}")
        i = j
    return "".join(salida) + tex[i:]


def _pandoc(md: str, cursiva: bool = True) -> str:
    """Convierte a LaTeX; con cursiva=True pone en cursiva los términos en inglés (no en las referencias)."""
    if cursiva:
        from cursivas_ingles import cursivas
        md = cursivas(md)
    r = subprocess.run(
        ["pandoc", "-f", "markdown-auto_identifiers", "-t", "latex", "--top-level-division=chapter"],
        input=md, capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return _epigrafe_corto(_cortes_texttt(r.stdout))


def generar() -> list[Path]:
    """Escribe los .tex y devuelve la lista de archivos generados."""
    escritos = []
    for origen, destino in CAPITULOS.items():
        md = _cuerpo_introduccion() if origen == "introduccion.md" else (BASE / origen).read_text(encoding="utf-8")
        ruta = CAPS / destino
        ruta.write_text(_pandoc(_limpiar(md)), encoding="utf-8")
        escritos.append(ruta)

    resumen = (BASE / "resumen.md").read_text(encoding="utf-8")
    resumen = re.sub(r"^# Resumen\s*\n", "", resumen)
    (CAPS / "00_abstract.tex").write_text(_pandoc(resumen), encoding="utf-8")
    escritos.append(CAPS / "00_abstract.tex")

    refs = (BASE / "referencias_y_notas.md").read_text(encoding="utf-8")
    refs = refs[: refs.index("# Notas para el grupo")]
    refs = re.sub(r"^# Referencias\s*\n", "", refs)
    tex = _pandoc(refs, cursiva=False).replace("\\begin{itemize}", "\\begin{itemize}[label={},leftmargin=1.27cm,itemindent=-1.27cm,itemsep=0.6\\baselineskip]")
    (CAPS / "10_referencias.tex").write_text(tex, encoding="utf-8")
    escritos.append(CAPS / "10_referencias.tex")
    return escritos


def compilar() -> None:
    """Dos pasadas de xelatex (indice y referencias cruzadas) y copia del PDF oficial."""
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "Tesis.tex"],
                           cwd=FUENTE, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print(r.stdout[-3000:])
            raise RuntimeError("xelatex fallo; ver tesis/fuente/Tesis.log")
    shutil.copy(FUENTE / "Tesis.pdf", FUENTE.parent / "Tesis.pdf")
    print("[OK] tesis/Tesis.pdf")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--compilar", action="store_true")
    a = ap.parse_args()
    for ruta in generar():
        print(f"[OK] {ruta.relative_to(BASE.parent)}")
    if a.compilar:
        compilar()


if __name__ == "__main__":
    main()
