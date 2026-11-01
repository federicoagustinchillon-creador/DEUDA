# Fuente LaTeX

`Tesis.tex` define el formato de la tesis y arma el documento con los capítulos de `../capitulos/`, que se generan desde los `.md` de `tesis_oficial_borradores/`. No se editan a mano: se pisan en la próxima generación.

El PDF para leer está un nivel arriba, en [`../Tesis.pdf`](../Tesis.pdf). Para regenerar los capítulos y compilar:

```bash
python tesis_oficial_borradores/generar_latex.py --compilar
```

Compila con XeLaTeX en tres pasadas (con dos, los índices quedan desfasados) y copia el PDF a `tesis/Tesis.pdf`. Necesita `pandoc`, `xelatex` y la fuente Liberation Sans. Los archivos auxiliares de la compilación no se versionan.

La lista de referencias sale de `tesis_oficial_borradores/referencias_y_notas.md`; `referencias.bib` es un archivo de versiones anteriores y la compilación no lo usa.
