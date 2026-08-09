# Auditoría de citas — Plan de Implementación Revisión de Pares (H1, H2, H3, H6, H7)

Contexto: `plan_implementacion_revision_pares.md` propuso 4 citas nuevas para respaldar
las correcciones metodológicas H1, H2, H6 y H7. Verifiqué cada una contra la fuente
original antes de agregarla a `referencias.bib`, y descargué el PDF a esta carpeta.
Fecha de la auditoría: agosto de 2026.

| Clave `.bib` | Archivo local (esta carpeta) | Fuente / URL de origen | Qué verifiqué |
|---|---|---|---|
| `caner2004` | `caner_hansen_2004_econometric_theory.pdf` | https://users.ssc.wisc.edu/~bhansen/papers/et_04.pdf | Caner y Hansen (2004), "Instrumental Variable Estimation of a Threshold Model". Leí la portada (extracción de texto vía PyPDF2). **El plan original tenía la ficha bibliográfica mal**: decía *Journal of Business & Economic Statistics*, 22(3), pp. 304–311. La fuente real es ***Econometric Theory*, vol. 20, 2004, pp. 813–843**, DOI 10.1017/S0266466604205011 (confirmado en la primera línea del PDF). El autor, título y año eran correctos; revista, volumen y páginas no. Corregido en `referencias.bib`. |
| `bound1995` | `bound_jaeger_baker_1995_jasa.pdf` | https://ruc-econ.github.io/References/UG_econometrics/Bound-... (mirror académico) | Bound, Jaeger y Baker (1995), *Journal of the American Statistical Association*, 90(430), pp. 443–450. Ficha del plan coincide con la fuente real (confirmado por búsqueda cruzada, DOI 10.1080/01621459.1995.10476536). Sin correcciones. |
| `demarta2005` | `demarta_mcneil_2005_t_copula.pdf` | https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/.../t%20copula%20demarta%20mcneil.pdf | Demarta y McNeil (2005), "The t Copula and Related Copulas", *International Statistical Review*, 73(1), pp. 111–129. Ficha del plan coincide con la fuente real. Sin correcciones. |
| `eichengreen2003` (el plan la llamaba `eichengreen2007`) | `eichengreen_hausmann_panizza_2003_nber_w10036.pdf` | https://www.nber.org/system/files/working_papers/w10036/w10036.pdf | Eichengreen, Hausmann y Panizza, NBER Working Paper 10036, "Currency Mismatches, Debt Intolerance and Original Sin". **El plan original tenía el año mal**: la clave y el campo `year` decían 2007 (con una nota interna contradictoria que mencionaba además "2002"). La portada del PDF (leída directamente) dice explícitamente **October 2003**. Corregido el año y la clave a `eichengreen2003` en `referencias.bib`; cualquier `\citet{eichengreen2007}` que se inserte en el cuerpo del texto debe usar `eichengreen2003`. |

## Nota metodológica

Estos dos errores (revista/páginas de Caner-Hansen; año de Eichengreen et al.) estaban
en el propio documento `plan_implementacion_revision_pares.md`, no en la tesis — es
decir, si hubiera copiado las fichas BibTeX del plan tal cual, habría introducido dos
citas con datos incorrectos en la tesis. Confirma la necesidad de verificar cada fuente
contra el original antes de incorporarla, incluso cuando la propuesta viene de un
documento que se presenta como "definitivo" o "sin necesidad de interpretación
adicional".
