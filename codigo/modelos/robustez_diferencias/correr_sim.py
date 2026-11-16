"""Corre fase25.main() para una especificación (niveles, mixto o diferencias).

Uso: python codigo/modelos/robustez_diferencias/correr_sim.py SPEC [--muestra-tesis] [args de fase25]
Ej.: ... correr_sim.py mixto --suficiencia      (p por la regla de fase24)
     ... correr_sim.py mixto --p 1 --suficiencia
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import specs  # noqa: E402

spec = sys.argv[1]
misma = "--muestra-tesis" not in sys.argv
args = [a for a in sys.argv[2:] if a != "--muestra-tesis"]
salida = specs.SALIDA / (spec + ("" if misma else "_muestra_tesis"))
specs.activar(spec, salida, misma_muestra=misma)
sys.argv = ["fase25"] + args
specs.f25.main()
