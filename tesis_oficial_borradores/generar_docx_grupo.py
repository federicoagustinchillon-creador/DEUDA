"""
generar_docx_grupo.py
=====================
Convierte los borradores Markdown de tesis_oficial_borradores/ a Word para mandar al grupo.

Formato (criterio del grupo para entregables Word): Calibri 11 en todo el documento,
títulos en negro, sin saltos de página, tablas sobrias con bordes finos, notas al pie
reales de Word (pandoc convierte las notas [^n] de Markdown).

Uso:
    python tesis_oficial_borradores/generar_docx_grupo.py

Salida: tesis_oficial_borradores/para_el_grupo/*.docx
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

BASE = Path(__file__).resolve().parent
SALIDA = BASE / "para_el_grupo"

ARCHIVOS: dict[str, str] = {
    "plan_de_labor.md": "Plan_de_labor.docx",
    "_tesis_borrador.md": "Tesis_borrador.docx",
    "guia_de_defensa.md": "Guia_de_defensa.docx",
    "propuestas_de_santiago.md": "Propuestas_de_Santiago.docx",
}

# Documento unico de la tesis: capitulos en orden (los que todavia no existen como
# borrador se omiten), y al final referencias y notas para el grupo.
TITULO_TESIS = "% Tesis: borrador de trabajo\n\n"
CAPITULOS: list[str] = ["antecedentes.md", "marco_teorico.md", "metodologia.md", "datos.md",
                        "resultados.md", "discusion.md", "conclusiones.md", "apendice.md"]


_SUB = str.maketrans("0123456789+-t", "₀₁₂₃₄₅₆₇₈₉₊₋ₜ")
_SIMBOLOS = {r"\varepsilon": "ε", r"\rho": "ρ", r"\alpha": "α", r"\gamma": "γ", r"\beta": "β",
             r"\ge": "≥", r"\geq": "≥", r"\le": "≤", r"\leq": "≤", r"\left(": "(", r"\right)": ")",
             r"\,": "", r"\;": " ", r"\cdot": "·", r"\times": "×"}


def _latex_a_texto(expr: str) -> str:
    """Convierte una expresion LaTeX simple a texto plano Unicode (criterio del grupo:
    en los Word, las ecuaciones van como texto, no como objetos de ecuacion).
    Cubre fracciones (incluso anidadas), letras griegas, subindices t, t-1, t+k y
    superindices L/F de la identidad de la deuda."""
    import re
    for k in sorted(_SIMBOLOS, key=len, reverse=True):
        expr = expr.replace(k, _SIMBOLOS[k])
    patron = re.compile(r"\\frac\{([^{}]*)\}\{([^{}]*)\}")
    while patron.search(expr):
        expr = patron.sub(lambda m: f"({m.group(1)})/({m.group(2)})", expr)
    expr = re.sub(r"\^\{?L\}?", "ᴸ", expr)
    expr = re.sub(r"\^\{?F\}?", "ᶠ", expr)
    expr = re.sub(r"_\{([0-9t+\-]+)\}", lambda m: m.group(1).replace(" ", "").translate(_SUB), expr)
    expr = re.sub(r"_([0-9t])", lambda m: m.group(1).translate(_SUB), expr)
    expr = expr.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", expr).strip()


def _matematica_a_texto(texto: str) -> str:
    """Reemplaza $$...$$ (en parrafo propio) y $...$ (en linea) por texto plano."""
    import re
    texto = re.sub(r"\$\$(.+?)\$\$", lambda m: "\n\n" + _latex_a_texto(m.group(1)) + "\n\n", texto, flags=re.S)
    return re.sub(r"\$([^$\n]+?)\$", lambda m: _latex_a_texto(m.group(1)), texto)


def armar_capitulos_1_2() -> Path:
    """Concatena la Introduccion (secciones 1.1 a 1.8) y los capitulos disponibles en un
    unico Markdown temporal."""
    intro = (BASE / "introduccion.md").read_text(encoding="utf-8")
    inicio = intro.index("## 1.1 Contextualización")
    fin = intro.index("## Referencias\n")
    cuerpo_intro = intro[inicio:fin].rstrip().rstrip("-").rstrip()
    resumen = (BASE / "resumen.md").read_text(encoding="utf-8").rstrip()
    partes = [TITULO_TESIS + resumen, "# 1. Introducción\n\n" + cuerpo_intro]
    for nombre in CAPITULOS:
        ruta = BASE / nombre
        if ruta.exists():
            partes.append(ruta.read_text(encoding="utf-8").rstrip())
    partes.append((BASE / "referencias_y_notas.md").read_text(encoding="utf-8"))
    from cursivas_ingles import cursivas  # términos en inglés en cursiva (no en las referencias)
    partes = [cursivas(t) for t in partes[:-1]] + partes[-1:]
    texto = _matematica_a_texto("\n\n".join(partes))
    destino = BASE / "_tesis_borrador.md"
    destino.write_text(texto, encoding="utf-8")
    return destino

FUENTE = "Calibri"


def _fijar_fuente(estilo, tamano: float, negrita: bool | None = None) -> None:
    """Fija Calibri (incluida la variante de Asia oriental) y color negro en un estilo."""
    estilo.font.name = FUENTE
    estilo.font.size = Pt(tamano)
    estilo.font.color.rgb = RGBColor(0, 0, 0)
    if negrita is not None:
        estilo.font.bold = negrita
    rpr = estilo.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for atributo in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(atributo), FUENTE)
    for tema in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(tema)) is not None:
            del rfonts.attrib[qn(tema)]


def construir_referencia(destino: Path) -> None:
    """Genera el reference.docx de pandoc y le aplica el formato del grupo."""
    with open(destino, "wb") as fh:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            check=True,
            stdout=fh,
        )
    doc = Document(str(destino))
    tamanos = {"Heading 1": 16, "Heading 2": 13, "Heading 3": 12, "Heading 4": 11, "Title": 18}
    for estilo in doc.styles:
        try:
            nombre = estilo.name
            if not hasattr(estilo, "font"):
                continue
        except (AttributeError, ValueError):
            continue
        if nombre in tamanos:
            _fijar_fuente(estilo, tamanos[nombre], negrita=True)
            estilo.paragraph_format.page_break_before = False
        elif nombre in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text",
                        "Footnote Text", "Table", "Hyperlink"):
            _fijar_fuente(estilo, 10 if nombre == "Footnote Text" else 11)
    for nombre in ("Body Text", "First Paragraph"):
        if nombre in [s.name for s in doc.styles]:
            doc.styles[nombre].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            doc.styles[nombre].paragraph_format.space_after = Pt(6)
    doc.save(str(destino))


def bordes_finos(ruta: Path) -> None:
    """Aplica bordes simples de 0,5 pt a todas las tablas y Calibri a cada corrida de texto."""
    doc = Document(str(ruta))
    for tabla in doc.tables:
        tbl_pr = tabla._tbl.tblPr
        bordes = OxmlElement("w:tblBorders")
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
            borde = OxmlElement(f"w:{lado}")
            borde.set(qn("w:val"), "single")
            borde.set(qn("w:sz"), "4")
            borde.set(qn("w:color"), "808080")
            bordes.append(borde)
        existente = tbl_pr.find(qn("w:tblBorders"))
        if existente is not None:
            tbl_pr.remove(existente)
        tbl_pr.append(bordes)
        for fila in tabla.rows:
            for celda in fila.cells:
                for parrafo in celda.paragraphs:
                    for corrida in parrafo.runs:
                        corrida.font.name = FUENTE
                        corrida.font.size = Pt(10)
    doc.save(str(ruta))


def main() -> None:
    SALIDA.mkdir(exist_ok=True)
    temporal = armar_capitulos_1_2()
    with tempfile.TemporaryDirectory() as tmp:
        referencia = Path(tmp) / "referencia.docx"
        construir_referencia(referencia)
        for origen, destino in ARCHIVOS.items():
            ruta_salida = SALIDA / destino
            subprocess.run(
                ["pandoc", str(BASE / origen), "-f", "markdown", "-t", "docx",
                 "--reference-doc", str(referencia), "--resource-path", str(BASE), "-o", str(ruta_salida)],
                check=True,
            )
            bordes_finos(ruta_salida)
            print(f"[OK] {ruta_salida.relative_to(BASE.parent)}")
    temporal.unlink()


if __name__ == "__main__":
    main()
