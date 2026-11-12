"""
verificar_citas.py
==================
Cruza cada cita autor-año del texto (APA 7, en español) con la lista de referencias y cada
referencia con las citas del texto. Una cita coincide con una referencia si tienen el mismo
primer autor, la misma cantidad de autores (uno, dos o "et al." para tres o más) y el mismo año,
con su letra (2025a, 2025b) cuando la hay.

Uso:
    python tesis_oficial_borradores/verificar_citas.py
    python tesis_oficial_borradores/verificar_citas.py texto1.md texto2.md --refs lista.md

Sin argumentos revisa los capítulos de la tesis contra referencias_y_notas.md. Imprime las citas
sin referencia y las referencias sin cita. Las citas de organismos con sigla ("FMI", "OPC")
coinciden con la sigla entre corchetes de la referencia.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
CAPITULOS = ["introduccion.md", "antecedentes.md", "marco_teorico.md", "metodologia.md", "datos.md",
             "resultados.md", "discusion.md", "conclusiones.md", "apendice.md"]

LETRA = r"[A-ZÁÉÍÓÚÑÖŞÇ]"
CHAR = r"[\wáéíóúñüöşçÁÉÍÓÚÑÖŞÇ'\-]"
PART = r"(?:de la|della|del|de|van|von|da|di|le|la)"
CONECT = r"(?:of|the|de|del|la|y|para|and|for)"
# Apellido o nombre de organismo ("Board of Governors of the Federal Reserve System").
APELLIDO = rf"(?:{PART} )?{LETRA}{CHAR}+(?:(?: {CONECT})* {LETRA}{CHAR}+)*"
ANIO = r"(?:\d{4}[a-z]?|s\. ?f\.)(?!T\d)"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", "", s).strip()


def leer_referencias(ruta: Path) -> list[dict]:
    txt = ruta.read_text(encoding="utf-8")
    if "# Notas para el grupo" in txt:
        txt = txt[: txt.index("# Notas para el grupo")]
    items: list[str] = []
    for linea in txt.split("\n"):
        if linea.startswith("- "):
            items.append(linea[2:].strip())
        elif items and linea.startswith("  ") and linea.strip():
            items[-1] += " " + linea.strip()
    refs = []
    for it in items:
        m = re.search(r"\((\d{4}[a-z]?|s\. ?f\.)(?:, [^)]*)?\)", it)
        if not m:
            continue
        cabeza = it[: m.start()].strip()
        personas = re.findall(rf"({APELLIDO}), (?:{LETRA}\. ?)+(?:-{LETRA}\.)?", cabeza)
        if personas:
            autores, n = [norm(p) for p in personas], len(personas)
        else:
            sigla = re.findall(r"\[([^\]]+)\]", cabeza)
            autores = [norm(re.sub(r"\s*\[.*?\]", "", cabeza.rstrip(".")))] + [norm(s) for s in sigla]
            n = 1
        refs.append({"raw": it, "autores": autores, "anio": m.group(1).replace(" ", ""), "n": n})
    return refs


def citas_del_texto(txt: str) -> list[tuple[str, str, str]]:
    txt = re.sub(r"`[^`]*`", " ", txt)
    txt = re.sub(r"\$[^$]*\$", " ", txt)
    salida = []
    for m in re.finditer(r"\(([^()]*?(?:\d{4}|s\. ?f\.)[^()]*)\)", txt):
        dentro = m.group(1)
        antes = txt[max(0, m.start() - 90): m.start()]
        if re.match(rf"^\s*{ANIO}", dentro):  # cita narrativa: Autor (2005), Autor y Autor (2005, p. 3)
            mm = re.search(rf"({APELLIDO}(?: y {APELLIDO})?(?: et al\.)?)\s*$", antes)
            cab = re.match(rf"^\s*({ANIO}(?:, {ANIO})*)", dentro)
            if mm and cab:
                for a in re.findall(ANIO, cab.group(1)):
                    salida.append((mm.group(1), a.replace(" ", ""), antes[-40:] + "(" + dentro[:30]))
            continue
        for parte in dentro.split(";"):  # cita entre paréntesis: (Autor, 2005; Autor y Autor, 2006)
            parte = parte.strip()
            mm = re.match(rf"^(?:véase |ver |cf\. )?({APELLIDO}(?: y {APELLIDO})?(?: et al\.)?(?: \[[^\]]+\])?),? ({ANIO}(?:, {ANIO})*)", parte)
            if mm:
                for a in re.findall(ANIO, mm.group(2)):
                    salida.append((mm.group(1), a.replace(" ", ""), parte[:50]))
    return salida


def coincide(cita: tuple[str, str, str], refs: list[dict]) -> dict | None:
    autor, anio, _ = cita
    et_al = "et al" in autor
    base = re.sub(r" et al\.", "", autor)
    base = re.sub(r"\s*\[[^\]]+\]", "", base)
    base = re.sub(r"^(?:de la |del |de |el |la |El |La |De )(?=[A-ZÁÉÍÓÚÑ])", "", base) if not base.startswith("De la Rúa") else base
    partes = [norm(p) for p in base.split(" y ")]
    for r in refs:
        if r["anio"] != anio:
            continue
        a = r["autores"]
        if et_al:
            if a and a[0] == partes[0] and r["n"] >= 3:
                return r
        elif len(partes) == 2:
            if r["n"] == 2 and a[:2] == partes:
                return r
        elif r["n"] == 1 and partes[0] in a:
            return r
    return None


def main() -> None:
    args = sys.argv[1:]
    refs_ruta = BASE / "referencias_y_notas.md"
    if "--refs" in args:
        k = args.index("--refs")
        refs_ruta = Path(args[k + 1])
        args = args[:k] + args[k + 2:]
    archivos = [Path(a) for a in args] or [BASE / c for c in CAPITULOS]
    refs = leer_referencias(refs_ruta)
    print(f"{len(refs)} referencias en {refs_ruta.name}")
    usadas, total = set(), 0
    for f in archivos:
        txt = f.read_text(encoding="utf-8")
        if f.name == "introduccion.md":
            txt = txt.split("## Referencias")[0]
        if "# Referencias bibliográficas" in txt:
            txt = txt.split("# Referencias bibliográficas")[0]
        sin = []
        for c in citas_del_texto(txt):
            r = coincide(c, refs)
            if r is None:
                sin.append(c)
            else:
                usadas.add(r["raw"])
        total += len(sin)
        print(f"{f.name}: {len(sin)} citas sin referencia")
        for autor, anio, ctx in sin:
            print(f"    {autor} {anio} | {ctx.strip()[:70]}")
    sobran = [r["raw"] for r in refs if r["raw"] not in usadas]
    print(f"\nReferencias sin cita en estos textos: {len(sobran)}")
    for s in sobran:
        print("    ", s[:110])
    print(f"\n{total} citas sin referencia")


if __name__ == "__main__":
    main()
