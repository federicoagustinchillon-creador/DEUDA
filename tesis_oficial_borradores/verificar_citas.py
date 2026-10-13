"""
verificar_citas.py
==================
Control cruzado entre las citas del texto (autor, anio) y la lista de referencias de
referencias_y_notas.md: informa citas sin referencia y referencias que ningun capitulo cita.

Uso: python tesis_oficial_borradores/verificar_citas.py
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
CAPITULOS = ["resumen.md", "introduccion.md", "antecedentes.md", "marco_teorico.md", "metodologia.md", "datos.md",
             "resultados.md", "discusion.md", "conclusiones.md", "apendice.md"]


def plano(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def referencias() -> list[tuple[str, str, str]]:
    """(primer apellido normalizado, anio, entrada) de cada referencia."""
    t = (BASE / "referencias_y_notas.md").read_text(encoding="utf-8")
    t = t[: t.index("# Notas para el grupo")]
    out = []
    for linea in t.splitlines():
        if not linea.startswith("- "):
            continue
        m = re.search(r"\((\d{4})[a-z]?[,)]", linea)
        if not m:
            continue
        autor = plano(re.split(r"[,.(\[]", linea[2:])[0].strip())
        out.append((autor, m.group(1), linea[2:80]))
    return out


def citas(texto: str) -> set[tuple[str, str]]:
    """Pares (apellido, anio) citados en formato APA en el texto."""
    texto = texto[: texto.index("## Referencias\n")] if "## Referencias\n" in texto else texto
    pares = set()
    patron = re.compile(r"([A-ZÁÉÍÓÚÑ][\wáéíóúñü'\-]+(?: (?:de la|de|del|van|von|y) [A-ZÁÉÍÓÚÑ][\wáéíóúñü'\-]+)*)"
                        r"(?: et al\.)?(?:,? y [A-ZÁÉÍÓÚÑ][\wáéíóúñü'\-]+(?: [A-ZÁÉÍÓÚÑ][\wáéíóúñü'\-]+)?)?,? \(?((?:19|20)\d{2})")
    for m in patron.finditer(texto):
        pares.add((plano(m.group(1)), m.group(2)))
    for grupo in re.findall(r"\(([^()]*\d{4}[^()]*)\)", texto):
        for parte in grupo.split(";"):
            m = re.match(r"\s*([A-ZÁÉÍÓÚÑ][^,\d]*?)(?: et al\.)?,? ((?:19|20)\d{2})", parte)
            if m:
                pares.add((plano(m.group(1).split(" y ")[0].strip()), m.group(2)))
    return pares


SIGLAS = {"fmi": "fondo monetario", "bcra": "banco central", "indec": "instituto nacional", "ocde": "organizacion",
          "mecon": "ministerio", "opc": "oficina de presupuesto", "cepal": "comision economica"}


def main() -> None:
    refs = referencias()
    usadas = set()
    faltan = []
    todo = " ".join((BASE / c).read_text(encoding="utf-8") for c in CAPITULOS)
    for r in refs:  # normas: se citan por numero
        m = re.search(r"(Ley [\d.]+|Decreto [\d/]+)", r[2])
        if m and m.group(1) in todo:
            usadas.add(r)
    for cap in CAPITULOS:
        for autor, anio in sorted(citas((BASE / cap).read_text(encoding="utf-8"))):
            clave = SIGLAS.get(autor.split()[-1], autor.split()[0])
            cand = [r for r in refs if r[1] == anio and (r[0].startswith(clave) or clave in r[0])]
            if cand:
                usadas.update(cand)
            elif autor.split()[0] not in {"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                          "septiembre", "octubre", "noviembre", "diciembre", "ley", "tabla", "figura",
                                          "cuadro", "capitulo", "seccion", "anexo"}:
                faltan.append((cap, autor, anio))
    print("CITAS SIN REFERENCIA:")
    for f in faltan:
        print("  ", f)
    print("REFERENCIAS SIN CITA:")
    for r in refs:
        if r not in usadas:
            print("  ", r[2])


if __name__ == "__main__":
    main()
