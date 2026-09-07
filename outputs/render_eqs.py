"""
Renderiza las ecuaciones de la nota metodológica a PNG con tipografía
Computer Modern (mathtext 'cm'), para incrustarlas en el documento Word con
calidad idéntica a LaTeX. Emite outputs/eq_img/eq_NN.png y un manifiesto JSON
con las dimensiones en píxeles de cada imagen.

Uso: python outputs/render_eqs.py
"""

import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "serif"

OUT = pathlib.Path(__file__).parent / "eq_img"
OUT.mkdir(exist_ok=True)

DPI = 240
FONTSIZE = 19

# Clave -> LaTeX. Nombres de varias letras en \mathrm para que queden rectos,
# como en un paper. \mathbf{1} es la función indicadora.
EQS = {
    "igbc": r"$d_{t-1} = \sum_{j=0}^{\infty} \dfrac{sp_{t+j}}{(1+r)^{\,j+1}}$",
    "bohn": (
        r"$pb_t = \alpha + \rho\, d_{t-1} + \beta_1\, \tilde{y}_t"
        r" + \beta_2\, g_t^{\,\mathrm{exp}} + u_t$"
    ),
    "blanchard": (
        r"$\Delta d_t = \dfrac{r_t - g_t}{1 + g_t}\; d_{t-1} - sp_t$"
    ),
    "vecm": (
        r"$\Delta \mathbf{x}_t = \boldsymbol{\alpha}\boldsymbol{\beta}'\,"
        r"\mathbf{x}_{t-1} + \sum_{i=1}^{k-1} \boldsymbol{\Gamma}_i\,"
        r"\Delta \mathbf{x}_{t-i} + \boldsymbol{\delta}\, \tilde{y}_t"
        r" + \boldsymbol{\varepsilon}_t$"
    ),
    "svar": (
        r"$A_0\, \mathbf{u}_t = B\, \mathbf{e}_t"
        r" \qquad "
        r"\mathbf{Y}_t = \left(\, \tilde{y}_t,\ pb_t,\ \mathrm{EMBI}_t,\ "
        r"\mathrm{TCRM}_t,\ d_t \,\right)'$"
    ),
    "favero": (
        r"$d_t = \dfrac{1 + r_t}{1 + g_t}\; d_{t-1} - pb_t + \mathrm{sft}_t$"
    ),
    "dols": (
        r"$pb_t = \alpha + \rho\, d_{t-1} + \gamma\, \tilde{y}_t"
        r" + \sum_{j=-4}^{4} \phi_j\, \Delta d_{t-j} + \varepsilon_t$"
    ),
    "hansen": (
        r"$pb_t = \alpha + \beta_1\, d_{t-1}\, \mathbf{1}(\mathrm{EMBI}_t \leq \tau)"
        r" + \beta_2\, d_{t-1}\, \mathbf{1}(\mathrm{EMBI}_t > \tau)"
        r" + \gamma\, \tilde{y}_t + \varepsilon_t$"
    ),
    "cir": (
        r"$d(\mathrm{risk}_t) = \kappa\,(\theta - \mathrm{risk}_t)\, dt"
        r" + \sigma\, \sqrt{\mathrm{risk}_t}\;\, dW_t$"
    ),
    "feller": r"$2\,\kappa\,\theta > \sigma^{2}$",
}

manifest = {}
for key, tex in EQS.items():
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0.0, 0.0, tex, fontsize=FONTSIZE, color="black")
    path = OUT / f"eq_{key}.png"
    fig.savefig(
        path, dpi=DPI, bbox_inches="tight", pad_inches=0.04, transparent=True
    )
    plt.close(fig)
    from PIL import Image

    with Image.open(path) as im:
        manifest[key] = {"file": path.name, "w": im.width, "h": im.height}
    print(f"  {key:10s} {manifest[key]['w']}x{manifest[key]['h']}  ->  {path.name}")

(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"\nManifiesto: {OUT / 'manifest.json'}")
