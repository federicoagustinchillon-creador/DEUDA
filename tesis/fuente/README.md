# Fuente LaTeX — no es acá donde está el PDF para leer

Esta carpeta tiene el **código fuente** de la tesis: `Tesis.tex`, `referencias.bib`, y los archivos que genera la compilación (`.aux`, `.log`, `.bbl`, etc. — no están versionados).

**El PDF para leer está un nivel arriba: [`../Tesis.pdf`](../Tesis.pdf).**

Al compilar acá adentro, `xelatex` también escribe un `Tesis.pdf` en esta misma carpeta — es un artefacto de build (está en `.gitignore`, no se sube a git), no confundirlo con el oficial. Después de compilar, copiá el resultado a la carpeta de arriba:

```bash
cd tesis/fuente
xelatex -interaction=nonstopmode Tesis.tex
xelatex -interaction=nonstopmode Tesis.tex
cd ..
cp fuente/Tesis.pdf Tesis.pdf
```

## Los capítulos se generan desde los Markdown

El texto de la tesis vive en `tesis_oficial_borradores/*.md`. Los `.tex` de `tesis/capitulos/` se generan con

```bash
python tesis_oficial_borradores/generar_latex.py --compilar
```

que convierte los capítulos, el resumen y las referencias, compila con XeLaTeX y copia el PDF a `tesis/Tesis.pdf`. No editar los `.tex` de los capítulos a mano: se pisan en la próxima generación. Ya no se usa biber; las referencias salen de `referencias_y_notas.md`.
