"""
cursivas_ingles.py
==================
Regla del director: los términos en inglés van en cursiva y con nota al pie en su primera
aparición. Este módulo hace las dos cosas sobre el texto de la tesis:

  - notas_primera_aparicion(): agrega, una sola vez, la nota al pie en la primera aparición de
    cada término (en el orden de los capítulos), fuera de títulos, tablas y epígrafes.
  - cursivas(md): pone en cursiva todas las apariciones que todavía no lo están. La usan
    generar_docx_grupo.py y generar_latex.py al armar los documentos.

Uso (solo para agregar las notas): python tesis_oficial_borradores/cursivas_ingles.py
"""

from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ORDEN = ["introduccion.md", "antecedentes.md", "marco_teorico.md", "metodologia.md", "datos.md",
         "resultados.md", "discusion.md", "conclusiones.md"]
DEFINICIONES = {
    "shock": "Perturbación inesperada que afecta a una variable del sistema y se transmite a las demás.",
    "spread": "Diferencia de rendimiento entre un bono y otro de referencia; en el caso soberano, entre los bonos del país y los del Tesoro de Estados Unidos.",
    "default": "Cesación de pagos de la deuda.",
    "bootstrap": "Método de remuestreo que aproxima la distribución de un estimador repitiendo la estimación sobre muestras generadas a partir de los propios datos.",
    "stock": "Saldo de una variable en un momento dado, por oposición a un flujo.",
    "swap": "Acuerdo de intercambio de monedas entre bancos centrales.",
}
PATRON = re.compile(r"(?<![\w*\-/])(shocks?|spreads?|default|bootstrap|stocks?|swaps?)(?![\w*\-/])", re.IGNORECASE)


def cursivas(md: str) -> str:
    """Pone en cursiva los términos que todavía no lo están (no toca rutas ni enlaces)."""
    lineas = []
    for linea in md.split("\n"):
        if linea.lstrip().startswith("![") or "](" in linea and linea.lstrip().startswith("!"):
            lineas.append(PATRON.sub(lambda m: f"*{m.group(1)}*", linea.split("](")[0]) + ("](" + linea.split("](", 1)[1] if "](" in linea else ""))
            continue
        lineas.append(PATRON.sub(lambda m: f"*{m.group(1)}*", linea))
    return "\n".join(lineas)


def _raiz(termino: str) -> str:
    t = termino.lower()
    return t[:-1] if t.endswith("s") and t[:-1] in DEFINICIONES else t


def notas_primera_aparicion() -> None:
    pendientes = set(DEFINICIONES)
    patron = re.compile(r"(?<![\w\-/])\*?(shocks?|spreads?|default|bootstrap|stocks?|swaps?)\*?(?![\w\-/])", re.IGNORECASE)
    for nombre in ORDEN:
        if not pendientes:
            break
        ruta = BASE / nombre
        texto = ruta.read_text(encoding="utf-8")
        inicio = texto.index("## 1.1") if nombre == "introduccion.md" else 0
        fin = texto.index("## Referencias\n") if nombre == "introduccion.md" else len(texto)
        notas = []
        lineas = texto[inicio:fin].split("\n")
        for k, linea in enumerate(lineas):
            if linea.startswith(("#", "|", "![", "[^")):
                continue
            for m in list(patron.finditer(linea)):
                raiz = _raiz(m.group(1))
                if raiz in pendientes and f"[^en-{raiz}]" not in texto:
                    linea = linea[:m.end()] + f"[^en-{raiz}]" + linea[m.end():]
                    notas.append(f"[^en-{raiz}]: *{raiz.capitalize()}*: {DEFINICIONES[raiz][0].lower() + DEFINICIONES[raiz][1:]}")
                    pendientes.discard(raiz)
                    break
            lineas[k] = linea
        if notas:
            texto = texto[:inicio] + "\n".join(lineas) + texto[fin:]
            if nombre == "introduccion.md":
                i = texto.index("## Referencias\n")
                texto = texto[:i].rstrip() + "\n\n" + "\n".join(notas) + "\n\n" + texto[i:]
            else:
                texto = texto.rstrip() + "\n\n" + "\n".join(notas) + "\n"
            ruta.write_text(texto, encoding="utf-8")
            print(f"[OK] {nombre}: {', '.join(n.split(']')[0][5:] for n in notas)}")
    if pendientes:
        print(f"Términos sin aparición: {sorted(pendientes)}")


if __name__ == "__main__":
    notas_primera_aparicion()
