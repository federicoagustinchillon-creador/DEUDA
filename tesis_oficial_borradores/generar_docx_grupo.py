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
    "plan_de_labor_grupo.md": "Plan_de_labor.docx",
    "_capitulos_1_2_v3.md": "Tesis_borrador_v3.docx",
}

# Documento unico para el grupo: cuerpo de la Introduccion (secciones 1.1 a 1.8, sin el
# encabezado interno ni las notas de trabajo del borrador), Antecedentes con la vacancia,
# y al final referencias y notas para el grupo.
TITULO_CAP_1_2 = "% Introducción y Antecedentes (versión 3, borrador para el grupo)\n\n"


def armar_capitulos_1_2() -> Path:
    """Concatena los borradores de los capitulos 1 y 2 en un unico Markdown temporal."""
    intro = (BASE / "introduccion_v3.md").read_text(encoding="utf-8")
    inicio = intro.index("## 1.1 Contextualización")
    fin = intro.index("## Referencias\n")
    cuerpo_intro = intro[inicio:fin].rstrip().rstrip("-").rstrip()
    antecedentes = (BASE / "antecedentes_v3.md").read_text(encoding="utf-8")
    refs_notas = (BASE / "referencias_y_notas_cap1_2_v3.md").read_text(encoding="utf-8")
    texto = (TITULO_CAP_1_2 + "# 1. Introducción\n\n" + cuerpo_intro + "\n\n"
             + antecedentes + "\n\n"
             + (BASE / "metodologia_v3.md").read_text(encoding="utf-8") + "\n\n" + refs_notas)
    destino = BASE / "_capitulos_1_2_v3.md"
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
                 "--reference-doc", str(referencia), "-o", str(ruta_salida)],
                check=True,
            )
            bordes_finos(ruta_salida)
            print(f"[OK] {ruta_salida.relative_to(BASE.parent)}")
    temporal.unlink()


if __name__ == "__main__":
    main()
