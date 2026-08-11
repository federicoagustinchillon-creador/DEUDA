# Fuente LaTeX — no es acá donde está el PDF para leer

Esta carpeta tiene el **código fuente** de la tesis: `Tesis.tex`, `referencias.bib`, y los archivos que genera la compilación (`.aux`, `.log`, `.bbl`, etc. — no están versionados).

**El PDF para leer está un nivel arriba: [`../Tesis.pdf`](../Tesis.pdf).**

Al compilar acá adentro, `xelatex` también escribe un `Tesis.pdf` en esta misma carpeta — es un artefacto de build (está en `.gitignore`, no se sube a git), no confundirlo con el oficial. Después de compilar, copiá el resultado a la carpeta de arriba:

```bash
cd tesis/fuente
xelatex -interaction=nonstopmode Tesis.tex
biber Tesis
xelatex -interaction=nonstopmode Tesis.tex
xelatex -interaction=nonstopmode Tesis.tex
cd ..
cp fuente/Tesis.pdf Tesis.pdf
```
