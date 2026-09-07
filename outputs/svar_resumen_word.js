/**
 * Nota metodológica en Word — tesis sobre sostenibilidad de la deuda pública y
 * riesgo soberano en Argentina DESDE EL RETORNO A LA DEMOCRACIA (1983–2025).
 *
 * Objeto: dejar por escrito, para mostrar a profesores y compañeros,
 *   (1) el período de análisis y qué se puede estimar hoy sobre él;
 *   (2) el proceso completo (cadena de procesamiento);
 *   (3) el empalme de series y el proxy de largo plazo del EMBI+ (1983–2025),
 *       con los resultados de cada test y para qué sirve;
 *   (4) el VAR estructural restringido;
 *   (5) el resto del protocolo;
 *   (6) cómo iría la estructura de la tesis;
 *   (7) qué falta y los próximos pasos.
 *
 * Todas las cifras provienen de resultados/tablas/ y de los capítulos 4–9 de la
 * tesis. No hay valores fabricados.
 *
 * Formato: tipografía única (Calibri), sin saltos de página, ecuaciones nativas
 * de Word (OMML) — verificado visualmente convirtiendo a PDF con Word.
 *
 * Autores: Federico Chillón · Santiago Páez · Emiliano Carricondo — FCE UNCUYO
 * Salida:  outputs/SVAR_Metodologia_Resultados_Accesible.docx
 */

const docx = require("docx");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  Table,
  TableRow,
  TableCell,
  WidthType,
  AlignmentType,
  BorderStyle,
  LevelFormat,
  PageNumber,
  Footer,
  MathRun,
  MathSubScript,
  MathSuperScript,
  MathFraction,
  MathRadical,
  MathSum,
  convertInchesToTwip,
} = docx;
const MathBlock = docx.Math; // evita sombrear el global Math (Math.round)
const fs = require("fs");
const path = require("path");

// ───────────────────────── Estilo ──────────────────────────────────────────
const FONT = "Calibri";
const BODY = 22;
const SMALL = 19;
const RULE = "000000";

// ───────────────────────── Párrafos ────────────────────────────────────────
const H1 = (t) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 130 },
    children: [new TextRun({ text: t, bold: true, font: FONT, size: 27 })],
  });

const H2 = (t) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 100 },
    children: [new TextRun({ text: t, bold: true, font: FONT, size: 23 })],
  });

const P = (content) => {
  const runs = (Array.isArray(content) ? content : [{ t: content }]).map(
    (f) =>
      new TextRun({ text: f.t, italics: !!f.i, bold: !!f.b, font: FONT, size: BODY })
  );
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 140, line: 300 },
    children: runs,
  });
};

const DECISION = (text) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 60, after: 200, line: 288 },
    indent: { left: convertInchesToTwip(0.3) },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: RULE, space: 10 } },
    children: [
      new TextRun({ text: "Para la tesis final. ", bold: true, font: FONT, size: SMALL }),
      new TextRun({ text, font: FONT, size: SMALL }),
    ],
  });

const NOTE = (text) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 30, after: 190 },
    children: [
      new TextRun({ text: "Nota. ", italics: true, font: FONT, size: SMALL }),
      new TextRun({ text, italics: true, font: FONT, size: SMALL }),
    ],
  });

const BULLET = (content) => {
  const runs = (Array.isArray(content) ? content : [{ t: content }]).map(
    (f) => new TextRun({ text: f.t, italics: !!f.i, bold: !!f.b, font: FONT, size: BODY })
  );
  return new Paragraph({
    numbering: { reference: "vinetas", level: 0 },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 90, line: 300 },
    children: runs,
  });
};

const REF = (text) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 90, line: 264 },
    indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.35) },
    children: [new TextRun({ text, font: FONT, size: SMALL })],
  });

const GAP = () => new Paragraph({ text: "", spacing: { after: 60 } });

// ───────────────────────── Ecuaciones OMML ─────────────────────────────────
const arr = (x) =>
  x == null
    ? []
    : Array.isArray(x)
    ? x.flatMap(arr)
    : typeof x === "string"
    ? [new MathRun(x)]
    : [x];

const sub = (b, s) => new MathSubScript({ children: arr(b), subScript: arr(s) });
const sup = (b, s) => new MathSuperScript({ children: arr(b), superScript: arr(s) });
const frac = (n, d) => new MathFraction({ numerator: arr(n), denominator: arr(d) });
const rad = (x) => new MathRadical({ children: arr(x) });
const nary = (child, lo, hi) =>
  new MathSum({ children: arr(child), subScript: arr(lo), superScript: arr(hi) });

const EQ = (...parts) =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 130, after: 160 },
    children: [new MathBlock({ children: parts.flatMap(arr) })],
  });

// ───────────────────────── Tabla académica ─────────────────────────────────
function academicTable(headers, rows, widths, aligns) {
  const nb = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const thin = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  const thick = { style: BorderStyle.SINGLE, size: 8, color: RULE };
  const cell = (txt, i, { bold = false, top = nb, bottom = nb } = {}) =>
    new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      borders: { top, bottom, left: nb, right: nb },
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [
        new Paragraph({
          alignment: aligns[i] === "l" ? AlignmentType.LEFT : AlignmentType.RIGHT,
          spacing: { after: 0 },
          children: [new TextRun({ text: String(txt), bold, font: FONT, size: SMALL })],
        }),
      ],
    });
  const head = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => cell(h, i, { bold: true, top: thick, bottom: thin })),
  });
  const body = rows.map(
    (r, ri) =>
      new TableRow({
        children: r.map((c, i) => cell(c, i, { bottom: ri === rows.length - 1 ? thick : nb })),
      })
  );
  return new Table({
    columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows: [head, ...body],
  });
}

// ═══════════════════════════════════════════════════════════════════════════
const C = [];

// ── Encabezado ─────────────────────────────────────────────────────────────
C.push(
  new Paragraph({
    spacing: { after: 110 },
    children: [
      new TextRun({
        text:
          "Deuda Pública y Riesgo Soberano en Argentina desde el Retorno a la Democracia (1983–2025)",
        bold: true,
        font: FONT,
        size: 31,
      }),
    ],
  }),
  new Paragraph({
    spacing: { after: 210 },
    children: [
      new TextRun({
        text:
          "Nota metodológica — período de análisis, proceso completo, empalme de series para el proxy " +
          "de largo plazo del EMBI+, VAR estructural restringido y estructura de la tesis",
        italics: true,
        font: FONT,
        size: 23,
      }),
    ],
  }),
  new Paragraph({
    spacing: { after: 40 },
    children: [
      new TextRun({ text: "Santiago Páez  ·  Emiliano Carricondo  ·  Federico Chillón", font: FONT, size: 22 }),
    ],
  }),
  new Paragraph({
    spacing: { after: 240 },
    children: [
      new TextRun({
        text: "Facultad de Ciencias Económicas — Universidad Nacional de Cuyo · Mendoza, 2026",
        font: FONT,
        size: 20,
      }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 150, line: 300 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE },
    },
    children: [
      new TextRun({
        text:
          "El trabajo estudia la sostenibilidad de la deuda pública argentina tomando como marco temporal " +
          "los 42 años de democracia ininterrumpida (1983–2025). Hoy, la única serie que cubre todo ese " +
          "período es el costo de financiamiento soberano, reconstruido por empalme (Sección 3); el resto " +
          "del protocolo econométrico está acotado por la disponibilidad de datos fiscales trimestrales, " +
          "que arrancan en 2004. Este documento deja por escrito qué se puede estimar hoy sobre el " +
          "período completo, el proceso entero, los resultados de cada test con su utilidad, la estructura " +
          "propuesta de la tesis y los pasos que faltan para llevar toda la estimación a 1983.",
        font: FONT,
        size: BODY,
      }),
    ],
  })
);

// ═══════════════════ 1. EL PERÍODO DE ANÁLISIS ════════════════════════════
C.push(H1("1. El período de análisis: 1983–2025"));
C.push(
  P(
    "La decisión de fondo es que toda la investigación se enmarca en el período democrático completo, " +
      "1983T4–2025T4. El motivo no es solo de cobertura: es que la pregunta de la tesis —si la " +
      "penalización que los mercados le cobran a la deuda argentina y la fatiga fiscal son rasgos " +
      "estructurales o circunstanciales— solo puede responderse mirando varias décadas y varios " +
      "regímenes, no una ventana corta que coincide con una fase particular del ciclo."
  )
);
C.push(
  P(
    "Ahora bien, no todas las variables tienen la misma cobertura hoy. El costo de financiamiento " +
      "soberano se reconstruyó para los 169 trimestres completos. Las variables fiscales —resultado " +
      "primario y stock de deuda sobre PIB— solo tienen publicación trimestral verificable desde 2004; " +
      "hay un empalme parcial hasta 1996 y otro hasta 1999, pero nada llega a 1983."
  )
);
C.push(GAP());
C.push(
  academicTable(
    ["Variable", "Cobertura trimestral hoy", "Objetivo", "Fuente para cerrar la brecha 1983–2003"],
    [
      ["Spread soberano / EMBI+", "1983T4–2025T4 (empalmado)", "1983–2025", "— (ya cubierto)"],
      ["Deuda / PIB (SPNF)", "2004–2025 (1996–2025 empalmado anual→trim.)", "1983–2025", "Kehoe y Nicolini (2021), anual 1960–2017; Compendio Fiscal MECON"],
      ["Resultado primario / PIB", "2004–2025 (1996–2025 empalmado)", "1983–2025", "Kehoe y Nicolini (2021); Cetrángolo et al. (1997); FMI IFS"],
      ["PIB real / brecha del producto", "2004–2025 (1996–2025 encadenado)", "1983–2025", "INDEC / Banco Mundial, series anuales encadenadas"],
      ["TCRM", "1997–2025 (BCRA)", "1983–2025", "BCRA / CEPAL, índice de TCR real 1983–1996"],
    ],
    [1900, 2650, 900, 3550],
    ["l", "l", "l", "l"]
  )
);
C.push(GAP());
C.push(
  P(
    "En consecuencia, el estado actual es: el análisis de regímenes de riesgo soberano y de reversión a " +
      "la media (Sección 3) ya está hecho sobre 1983–2025; la función de reacción fiscal, el VAR " +
      "estructural y el análisis de sostenibilidad están hechos sobre 2004–2025, con robustez sobre " +
      "1999–2025. El paso que falta —descrito en la Sección 7— es reconstruir las tres series fiscales " +
      "para 1983–2003 a partir de fuentes históricas anuales, desagregarlas a trimestral por el método " +
      "de Denton (el mismo ya usado para 1996–2003) y volver a correr el protocolo completo sobre la " +
      "ventana de 42 años."
  )
);
C.push(
  DECISION(
    "el marco es 1983–2025 en todo el documento. La ventana 1999–2025 se conserva únicamente como " +
      "robustez de alta frecuencia, no como especificación de referencia. La FRF sobre el período " +
      "democrático completo puede estimarse de inmediato en frecuencia anual (n ≈ 43) con las fuentes " +
      "históricas de la última columna, mientras se completa el empalme trimestral."
  )
);

// ═══════════════════ 2. EL PROCESO COMPLETO ═══════════════════════════════
C.push(H1("2. El proceso completo (cadena de procesamiento)"));
C.push(
  P(
    "Todo resultado cuantitativo se produce mediante una cadena de scripts de Python reejecutable, sin " +
      "datos simulados. Cada etapa deja su salida en resultados/tablas/*.csv para trazabilidad. Los " +
      "nueve bloques:"
  )
);
C.push(GAP());
C.push(
  academicTable(
    ["Bloque", "Qué hace", "Salida principal", "Ventana"],
    [
      ["I. Ingesta y construcción", "Descarga BCRA, MECON/INDEC, Yahoo Finance; arma el panel trimestral", "dataset_consolidado_real.csv", "2004–2025"],
      ["II. Empalmes", "Empalme fiscal 1996–2003 (Denton); reconstrucción del spread 1983–2025 por eras", "dataset ampliado; spread_soberano_historico_1983_2025.csv", "1983 / 1999"],
      ["III. Estacionariedad y quiebres", "ADF, KPSS, PP, DF-GLS, Zivot-Andrews; Bai-Perron sobre deuda y sobre spread", "orden de integración; fechas de quiebre", "ambas"],
      ["IV. Cointegración y VECM", "Johansen (traza), selección de rezagos, VECM de sistema", "vector β, velocidades de ajuste α", "1999–2025"],
      ["V. VAR estructural (SVAR)", "Identificación Blanchard-Perotti / Favero-Giavazzi; IRF, FEVD", "matriz S, FEVD", "2004–2025"],
      ["VI. Umbrales y fatiga fiscal", "Umbral de Hansen (niveles y Δ), Threshold VECM", "τ*, Sup-LM", "2004–2025"],
      ["VII. Proceso CIR", "Calibración MLE exacta del spread como difusión con reversión a la media", "κ, θ, σ; condición de Feller", "1983–2025 y otras"],
      ["VIII. DSA estocástico", "Monte Carlo a 2035, perturbaciones t de Student, integración del CIR", "P(deuda > 100 % PIB); gráficos de abanico", "proyección"],
      ["IX. Gráficos", "Figuras de publicación (300 DPI)", "figuras de los capítulos 5 y 6", "—"],
    ],
    [1750, 3200, 2650, 900],
    ["l", "l", "l", "l"]
  )
);
C.push(GAP());
C.push(NOTE("El código íntegro está en codigo/, concatenado para lectura en codigo/codigo_completo_deuda.py. La estructura detallada por etapa está en el Apéndice de la tesis."));

// ═══════════════ 3. EMPALME Y PROXY DE LARGO PLAZO DEL EMBI+ ═══════════════
C.push(H1("3. Empalme de series: el proxy de largo plazo del EMBI+ (1983–2025)"));
C.push(
  P(
    "Este es el componente que ya cubre el período democrático completo y funciona como columna " +
      "vertebral del trabajo. El índice EMBI no existe antes de 1993 y el EMBI+ oficial de Argentina no " +
      "antes de 1998, de modo que la serie de 169 trimestres se construyó por empalme."
  )
);

C.push(H2("3.1. Reconstrucción por eras financieras"));
C.push(BULLET("Era Bonex (1983T4–1992T4): rendimiento en dólares de los Bonos Externos (Series 1982, 1984, 1987, 1989) menos la tasa del Treasury a 10 años, según Neumeyer y Perri (2005) y Kehoe y Nicolini (2021), con registros de CEMA, FIEL y BCRA."));
C.push(BULLET("Era Brady (1993T1–1997T4): JP Morgan EMBI Argentina stripped spread sobre bonos Brady Par, Discount y FRB (Uribe y Yue, 2006)."));
C.push(BULLET("Era EMBI+ (1998T1–2025T4): serie oficial de JP Morgan EMBI+ / EMBI Global Diversified Argentina."));

C.push(H2("3.2. Corrección de sesgo por solapamiento"));
C.push(
  P(
    "Para que los tramos empalmen sin un salto de nivel espurio, cada tramo antiguo se reescala al " +
      "nivel del siguiente por el cociente de medias en el trimestre de unión:"
  )
);
C.push(
  EQ(sub("k", "1"), " = ", frac(sub("EMBI", "Brady"), sub("Spread", "Bonex")), " = ",
    frac("850", "760"), " = 1,118", "          ",
    sub("k", "2"), " = ", frac(sub("EMBI+", " "), sub("EMBI", "Brady")), " = ",
    frac("540", "620"), " = 0,871")
);
C.push(
  P(
    "El factor compuesto Bonex → EMBI+ es 1,118 × 0,871 = 0,974. La serie final (169 trimestres, " +
      "spread_soberano_historico_1983_2025.csv) queda toda en escala EMBI+."
  )
);
C.push(
  NOTE(
    "El tramo Bonex 1983–1992 es una serie reconstruida a partir de la literatura y calibrada a hitos " +
      "trimestrales, no una serie de precios observada. Es un proxy de nivel y de régimen; no tiene la " +
      "misma calidad de dato que el EMBI+ posterior a 1998. Por eso los resultados sobre 1983–2025 se " +
      "leen en clave cualitativa (¿hay regímenes?, ¿el nivel de equilibrio es alto?), no de inferencia fina."
  )
);

C.push(H2("3.3. Test 1 — Quiebres estructurales de Bai-Perron (1983–2025)"));
C.push(
  P(
    "Se aplica programación dinámica sobre la media del spread (modelo L2, segmento mínimo 8 " +
      "trimestres) imponiendo cinco quiebres. Resultado: seis regímenes de financiamiento soberano."
  )
);
C.push(GAP());
C.push(
  academicTable(
    ["Régimen", "Período", "Media (pb)", "Desvío (pb)", "Hito de cierre"],
    [
      ["1", "1983T4–1988T4", "798", "359", "Colapso del Plan Austral"],
      ["2", "1989T1–1990T4", "3.574", "1.256", "Hiperinflaciones y Plan Bonex"],
      ["3", "1991T1–2001T4", "832", "427", "Convertibilidad y Plan Brady"],
      ["4", "2002T1–2005T2", "5.431", "638", "Default 2001–2002 (máximo histórico)"],
      ["5", "2005T3–2019T2", "684", "327", "Canjes 2005/2010, superávits gemelos"],
      ["6", "2019T3–2025T4", "1.732", "632", "PASO 2019, canje 2020, estabilización"],
    ],
    [850, 2000, 1050, 1000, 3600],
    ["l", "l", "r", "r", "l"]
  )
);
C.push(GAP());
C.push(
  P(
    "Los seis regímenes son persistentes (el más corto dura ocho trimestres) y recurrentes: Argentina " +
      "alterna entre un nivel “normal” de 680–830 puntos básicos y episodios de crisis de 1.700 a 5.400 " +
      "puntos. El umbral de fatiga fiscal de ~2.080 puntos estimado en la muestra 2004–2025 cae dentro " +
      "de ese rango histórico de tensión: no es un valor extremo ni un artefacto de la ventana corta."
  )
);
C.push(
  DECISION(
    "Bai-Perron sobre 42 años responde la pregunta central del marco: los regímenes de alto spread son " +
      "un rasgo repetido de toda la democracia, no de las últimas dos décadas. Entra en el cuerpo de la " +
      "tesis como evidencia de regularidad estructural."
  )
);

C.push(H2("3.4. Test 2 — Calibración CIR del riesgo soberano (1983–2025)"));
C.push(
  P("El proceso de Cox, Ingersoll y Ross (1985) modela el spread como una difusión con reversión a la media:")
);
C.push(
  EQ("d(", sub("risk", "t"), ") = κ ( θ − ", sub("risk", "t"), " ) dt + σ ",
    rad([sub("risk", "t")]), " d", sub("W", "t"))
);
C.push(
  P([
    { t: "κ es la velocidad de reversión (vida media ln 2 ⁄ κ), θ el nivel de equilibrio de largo plazo y σ la volatilidad. La no negatividad del spread está garantizada si se cumple la condición de Feller, " },
    { t: "2κθ > σ²", i: true },
    { t: ". Calibración por máxima verosimilitud exacta sobre la densidad Chi-cuadrado no central, sobre los 169 trimestres:" },
  ])
);
C.push(GAP());
C.push(
  academicTable(
    ["Parámetro", "Valor (1983–2025, n = 169)", "Lectura"],
    [
      ["Velocidad de reversión κ", "0,463", "Reversión rápida hacia el equilibrio"],
      ["Nivel de equilibrio θ", "1.457 pb", "Costo estructural medio de endeudarse en 42 años"],
      ["Volatilidad σ", "24,8", "Dispersión de las innovaciones"],
      ["Vida media", "1,50 años", "Duración típica de un ciclo de spread"],
      ["Condición de Feller (2κθ vs. σ²)", "1.349 > 614 → cumple (ratio 2,20)", "El spread simulado no puede volverse negativo"],
      ["AIC: CIR vs. AR(1)", "2.467 < 2.613 (ΔAIC −146)", "El CIR domina a un autorregresivo lineal"],
    ],
    [3100, 3350, 3550],
    ["l", "l", "l"]
  )
);
C.push(GAP());
C.push(
  P(
    "El parámetro clave es θ: el nivel al que revierte el spread en el largo plazo. Sobre 42 años da " +
      "1.457 puntos básicos. Como referencia, calibrado solo sobre 2004–2025 daría 1.032 puntos —un " +
      "valor sesgado a la baja porque esa ventana transcurre en su mayor parte dentro del régimen " +
      "comprimido 2005–2019—. La ventana larga es, por lo tanto, la que da el proxy correcto del piso " +
      "estructural del riesgo argentino."
  )
);
C.push(
  DECISION(
    "en el DSA de la tesis, la tasa de refinanciación externa de largo plazo se ancla en θ ≈ 1.457 pb " +
      "(calibración 1983–2025), no en el valor de la ventana corta. El θ corto (~1.032 pb) puede usarse " +
      "como escenario optimista, reportando la sensibilidad de la probabilidad de insolvencia a esa elección."
  )
);
C.push(
  NOTE(
    "El CIR trata el spread como proceso con reversión a la media; las vidas medias estimadas (menos " +
      "de dos años) implican reversión económica rápida, coherente con esa especificación. Los " +
      "contrastes de raíz unitaria, sensibles a los quiebres de 2001–2002, no la rechazan formalmente " +
      "en todas las ventanas, matiz que conviene declarar."
  )
);

C.push(H2("3.5. Test 3 — CIR de dos factores (riesgo global vs. riesgo local)"));
C.push(
  P(
    "Una calibración alternativa descompone el spread en un componente rápido, asociado al ciclo de " +
      "riesgo global, y uno lento, asociado al riesgo idiosincrático argentino:"
  )
);
C.push(EQ(sub("risk", "t"), " = ", sub("ξ", "t"), " + ", sub("χ", "t")));
C.push(GAP());
C.push(
  academicTable(
    ["Componente", "κ", "θ (pb)", "σ", "Vida media"],
    [
      ["Transitorio (global)", "2,10", "361", "18,8", "0,33 años"],
      ["Estructural (local)", "0,22", "671", "14,8", "3,15 años"],
    ],
    [2700, 700, 900, 900, 1400],
    ["l", "r", "r", "r", "r"]
  )
);
C.push(GAP());
C.push(
  P(
    "El componente estructural revierte lentamente hacia 671 puntos básicos: ese sería el proxy más " +
      "limpio del riesgo-país argentino de largo plazo, depurado del ruido del apetito de riesgo global."
  )
);
C.push(
  DECISION(
    "el CIR de dos factores es útil si la tesis quiere separar cuánto del spread es responsabilidad de " +
      "Argentina y cuánto es contexto externo. Como es una calibración exploratoria (sin bandas), va " +
      "como recuadro, no como resultado central."
  )
);

C.push(H2("3.6. El spread por administración presidencial (1983–2025)"));
C.push(GAP());
C.push(
  academicTable(
    ["Administración", "Período", "Trim.", "Media (pb)", "Mínimo", "Máximo"],
    [
      ["Alfonsín", "1983T4–1989T2", "23", "1.036", "409", "4.676"],
      ["Menem I", "1989T3–1995T1", "23", "1.578", "566", "5.455"],
      ["Menem II", "1995T2–1999T3", "18", "689", "357", "1.350"],
      ["De la Rúa", "1999T4–2001T3", "8", "811", "551", "1.469"],
      ["Rodríguez Saá / Duhalde", "2001T4–2003T1", "6", "5.355", "2.948", "6.659"],
      ["Néstor Kirchner", "2003T2–2007T3", "18", "2.776", "210", "5.801"],
      ["Cristina Fernández", "2007T4–2015T3", "32", "853", "388", "1.697"],
      ["Macri", "2015T4–2019T3", "16", "585", "360", "1.494"],
      ["Alberto Fernández", "2019T4–2023T3", "16", "2.049", "1.392", "3.103"],
      ["Milei", "2023T4–2025T4", "9", "1.195", "684", "2.258"],
    ],
    [2500, 1900, 700, 1100, 900, 900],
    ["l", "l", "r", "r", "r", "r"]
  )
);
C.push(GAP());
C.push(NOTE("Fuente: fase22_spread_por_regimen.csv. Spread empalmado, en puntos básicos."));

// ═══════════════ 4. VAR ESTRUCTURAL RESTRINGIDO ══════════════════════════
C.push(H1("4. VAR estructural restringido (transmisión de alta frecuencia)"));
C.push(
  P(
    "El SVAR aísla cómo se transmiten los shocks entre las cinco variables macro-fiscales. Requiere " +
      "datos fiscales trimestrales, así que hoy está estimado sobre 2004–2025 (86 observaciones con dos " +
      "rezagos). Extenderlo a 1983 depende del empalme fiscal descrito en las Secciones 1 y 7."
  )
);

C.push(H2("4.1. Identificación estructural"));
C.push(
  P(
    "Un VAR reducido tiene innovaciones correlacionadas que no son shocks económicos. Para pasar a " +
      "shocks estructurales, en vez de un ordenamiento de Cholesky arbitrario se imponen tres " +
      "restricciones con fundamento económico sobre el vector de cinco variables:"
  )
);
C.push(
  EQ(sub("A", "0"), " ", sub("u", "t"), " = B ", sub("e", "t"), "        ",
    sub("Y", "t"), " = ( ", sub("ỹ", "t"), ", ", sub("pb", "t"), ", ",
    sub("EMBI", "t"), ", ", sub("TCRM", "t"), ", ", sub("d", "t"), " )")
);
C.push(
  BULLET([
    { t: "Rigidez presupuestaria: el superávit primario solo reacciona dentro del trimestre a la brecha del producto por la semi-elasticidad cíclica automática de la recaudación, " },
    { t: "α", i: true },
    { t: "y", i: true },
    { t: " = 0,25 (estándar OCDE/FMI: Girouard y André 2005; Daude et al. 2011; Alberola et al. 2016)." },
  ])
);
C.push(BULLET("Ajuste financiero inmediato: el riesgo soberano y el tipo de cambio real absorben contemporáneamente todas las perturbaciones del período."));
C.push(BULLET("Identidad de acumulación de la deuda (Favero y Giavazzi, 2007):"));
C.push(
  EQ(sub("d", "t"), " = ", frac(["1 + ", sub("r", "t")], ["1 + ", sub("g", "t")]),
    " ", sub("d", "t-1"), " − ", sub("pb", "t"), " + ", sub("sft", "t"))
);
C.push(P("Frente a un Cholesky puro, la única restricción adicional es fijar el coeficiente del superávit sobre la brecha en 0,25 en lugar de estimarlo libremente."));

C.push(H2("4.2. Selección de rezagos"));
C.push(
  P(
    "AIC, FPE y HQIC seleccionan dos rezagos; BIC selecciona uno. Se adopta VAR(2) por mayoría " +
      "(AIC = 12,66; BIC = 14,23; HQIC = 13,29)."
  )
);

C.push(H2("4.3. Matriz de impacto contemporáneo (S)"));
C.push(P("S = A₀⁻¹B traduce un shock estructural de un desvío estándar en su efecto instantáneo:"));
C.push(GAP());
C.push(
  academicTable(
    ["Shock estructural", "→ EMBI+ (pb)", "→ Deuda/PIB (p.p.)"],
    [
      ["Riesgo soberano (propio)", "+473", "−0,43"],
      ["Superávit primario (negativo, 1 d.e.)", "−222", "−3,15"],
      ["Brecha del producto", "−179", "−2,89"],
      ["Tipo de cambio real", "—", "+0,59"],
    ],
    [3600, 2300, 2600],
    ["l", "r", "r"]
  )
);
C.push(GAP());
C.push(
  P(
    "Lectura: un deterioro del superávit primario de un desvío estándar eleva el EMBI+ en 222 puntos " +
      "dentro del mismo trimestre. Es la cuantificación del canal de credibilidad fiscal: el mercado " +
      "castiga el desvío de inmediato."
  )
);

C.push(H2("4.4. Descomposición de varianza del error de pronóstico (FEVD)"));
C.push(P("Reparte la varianza del error de pronóstico de cada variable entre los cinco shocks. Es el resultado principal del SVAR:"));
C.push(GAP());
C.push(
  academicTable(
    ["Horizonte", "Variable", "Brecha PIB", "Superávit", "EMBI+", "TCRM", "Propia"],
    [
      ["1 trim.", "Deuda / PIB", "32,9", "39,1", "0,7", "1,4", "25,9"],
      ["4 trim.", "Deuda / PIB", "29,4", "46,8", "1,7", "0,5", "21,6"],
      ["8 trim.", "Deuda / PIB", "28,5", "48,1", "4,4", "0,6", "18,4"],
      ["20 trim.", "Deuda / PIB", "28,6", "47,5", "4,2", "7,3", "12,4"],
      ["1 trim.", "EMBI+", "10,5", "16,1", "73,4", "0,0", "0,0"],
      ["8 trim.", "EMBI+", "17,6", "29,9", "49,7", "0,5", "2,3"],
      ["20 trim.", "EMBI+", "21,6", "36,5", "36,1", "1,8", "4,0"],
    ],
    [1100, 1700, 1150, 1150, 1000, 1000, 1000],
    ["l", "l", "r", "r", "r", "r", "r"]
  )
);
C.push(GAP());
C.push(
  P(
    "A mediano plazo la varianza de la deuda está dominada por el shock al resultado primario (47,5 % a " +
      "veinte trimestres) y por el shock a la brecha del producto (28,6 %); el shock cambiario y el de " +
      "riesgo soberano explican en conjunto 11,5 %. En la ecuación del EMBI+, el shock propio explica el " +
      "73 % de la varianza en el primer trimestre y cede hasta el 36 % a cinco años, cuando el shock " +
      "fiscal alcanza una participación equivalente: el mercado incorpora el historial fiscal a la prima."
  )
);
C.push(
  P([
    { t: "Esto describe " },
    { t: "qué perturbaciones mueven la deuda", i: true },
    { t: " (desbalances primarios y ciclo); no equivale a la existencia de una regla de reacción fiscal estabilizadora —cuya ausencia documentan DOLS y el VECM— ni a los canales por los que se resolvieron los sobreendeudamientos (depreciación real, licuación, reestructuraciones)." },
  ])
);

C.push(H2("4.5. Impulso-respuesta y diagnóstico del VAR reducido"));
C.push(P("Las funciones de impulso-respuesta se calculan con bandas bootstrap al 95 % (1.000 réplicas). El VAR reducido muestra:"));
C.push(BULLET("Deuda/PIB: fuertemente autorregresiva (primer rezago 1,06, t = 8,1); sin regresores cruzados significativos."));
C.push(BULLET("EMBI+: persistente (0,76, t = 6,7); responde con dos rezagos a la deuda (t = 2,0) y a la brecha (t = 1,9)."));
C.push(BULLET("Brecha del producto: la deuda rezagada la anticipa (t = −3,1 y t = 3,0), señal de causalidad de Granger deuda → actividad."));
C.push(BULLET("Superávit primario: solo su propio rezago es significativo (0,76, t = 5,5); no reacciona a rezagos de deuda, EMBI+ ni TCRM."));
C.push(
  P(
    "La matriz de correlación de residuos del VAR muestra que las relaciones contemporáneas que " +
      "importan son superávit–deuda (−0,47, la más fuerte) y superávit–EMBI+ (−0,21); la restricción de " +
      "identificación las preserva, de modo que no descarta información sustantiva."
  )
);
C.push(
  DECISION(
    "el SVAR entra en la tesis como módulo de transmisión de alta frecuencia y como validación " +
      "estructural del diagnóstico de DOLS/VECM: los desbalances primarios y el ciclo explican tres " +
      "cuartas partes de la varianza de la deuda. Su ventana (2004–2025) se declara como límite de " +
      "datos, con la ruta de extensión de la Sección 7. La matriz S y la FEVD van al cuerpo; el " +
      "diagnóstico del VAR reducido, al apéndice."
  )
);

// ═══════════════ 5. RESTO DEL PROTOCOLO ═══════════════════════════════════
C.push(H1("5. Función de reacción fiscal y sostenibilidad (resto del protocolo)"));
C.push(P("Los demás contrastes, con su ventana entre paréntesis:"));
C.push(BULLET("DOLS, muestra completa (2004–2025): coeficiente de reacción ρ = −0,0071 (error 0,012; p = 0,564). Sin reacción lineal significativa."));
C.push(BULLET("DOLS por subperíodos (2004–2025): ρ = 0,037 en 2004–2014 (p = 0,002) y 0,053 en 2015–2025 (p = 0,003). Positivo dentro de cada régimen; el promedio se anula por composición."));
C.push(BULLET("VECM (1999–2025): la velocidad de ajuste del superávit no es significativa (α = 0,0044; p = 0,204); la que ajusta es la deuda (α = −0,111; p < 0,001)."));
C.push(BULLET("IV-2SLS (2004–2025, instrumentos VIX y spread regional): F de primera etapa 13,0; Wu-Hausman p = 0,009 (EMBI+ endógeno); Sargan p = 0,436; coeficiente del EMBI+ instrumentado 0,0017 (p = 0,076)."));
C.push(BULLET("Umbral de Hansen (2004–2025): en niveles τ* = 449 pb, Sup-LM p = 0,076 (señal débil); en primera diferencia τ* = 2.083 pb, Sup-LM p < 0,001 (no linealidad sólida)."));
C.push(BULLET("Threshold VECM (2004–2025): τ* = 2.081 pb; la velocidad de ajuste fiscal cambia de signo entre regímenes (+0,006 → −0,008), pero el Sup-LM no es significativo (p = 0,625)."));
C.push(BULLET("Bai-Perron sobre la deuda (2004–2025): quiebres en 2007T2, 2014T3 y 2018T1 (SPNF); 2007T2 y 2016T4 (consolidada con el BCRA)."));
C.push(BULLET("DSA estocástico a 2035 (Monte Carlo, 1.000 iteraciones, perturbaciones t de Student ν ≈ 4,8): probabilidad de superar el 100 % del PIB del 31,2 % en el escenario de referencia (3,8 % optimista; 99,9 % de estrés); robusta entre 29,2 % y 33,4 %, y 29,8 % integrando el proceso CIR."));
C.push(
  DECISION(
    "estos ocho contrastes están cerrados sobre 2004–2025 (y 1999–2025 el VECM). Para el marco " +
      "democrático completo hay que reestimarlos sobre 1983–2025 una vez disponible el empalme fiscal; " +
      "el DOLS y la FRF de Bohn admiten una estimación anual inmediata sobre ese período."
  )
);

// ═══════════════ 6. ESTRUCTURA DE LA TESIS ═══════════════════════════════
C.push(H1("6. Cómo iría la estructura de la tesis"));
C.push(P("Ocho capítulos más apéndice. La última columna indica qué parte de esta nota alimenta cada capítulo."));
C.push(GAP());
C.push(
  academicTable(
    ["Capítulo", "Contenido", "Insumo de esta nota"],
    [
      ["1. Introducción", "Problema, preguntas, hipótesis (fatiga fiscal, umbrales, sostenibilidad), marco 1983–2025", "Secciones 1 y 7"],
      ["2. Estado del arte", "Sostenibilidad intertemporal, reglas fiscales, intolerancia a la deuda, caso argentino", "Referencias"],
      ["3. Marco teórico", "Restricción presupuestaria intertemporal, FRF de Bohn, fatiga fiscal de Ghosh et al., endogeneidad del riesgo soberano", "Ecuaciones de las Secciones 3 y 4"],
      ["4. Metodología", "Diseño, matriz de variables, las nueve etapas del protocolo, empalmes, software", "Sección 2 (proceso completo)"],
      ["5. Análisis descriptivo", "Evolución de deuda, resultado primario, spread 1983–2025; propiedades de integración; quiebres", "Secciones 3.3 y 3.6"],
      ["6. Desarrollo empírico y resultados", "Cointegración y VECM, DOLS, IV-2SLS, umbral de Hansen, TVECM, SVAR, CIR, spread histórico", "Secciones 3, 4 y 5"],
      ["7. Discusión", "Fatiga fiscal, transmisión macrofiscal, canales de ajuste stock-flujo, economía política", "Secciones 4.4 y 5"],
      ["8. Conclusiones", "Qué permite y qué no permite sostener la evidencia; agenda futura", "Secciones 3–5 y 7"],
      ["Apéndice", "Robustez adicional, estructura completa del código", "Sección 2"],
    ],
    [2500, 4600, 2000],
    ["l", "l", "l"]
  )
);
C.push(GAP());
C.push(
  P(
    "El eje narrativo es: el spread soberano tiene regímenes recurrentes y un nivel de equilibrio alto " +
      "a lo largo de toda la democracia (Sección 3); la política fiscal no exhibe una regla de reacción " +
      "estabilizadora estable (Sección 5) y sí señales de fatiga por encima de un umbral de riesgo " +
      "(~2.080 pb); y la sostenibilidad hacia 2035 depende más de los fundamentos macroeconómicos que " +
      "del ajuste fiscal discrecional (DSA)."
  )
);

// ═══════════════ 7. QUÉ FALTA Y PRÓXIMOS PASOS ═══════════════════════════
C.push(H1("7. Qué falta y próximos pasos"));
C.push(BULLET("Reconstruir deuda/PIB, resultado primario/PIB y PIB real para 1983–2003 a partir de fuentes anuales (Kehoe y Nicolini 2021; Compendio Fiscal MECON; Cetrángolo et al. 1997; FMI IFS)."));
C.push(BULLET("Desagregar esas series a frecuencia trimestral con el método de Denton, ancladas contra 2004–2006, como ya se hizo para 1996–2003."));
C.push(BULLET("Reestimar el protocolo completo (estacionariedad, cointegración, VECM, SVAR, umbrales, DSA) sobre 1983–2025."));
C.push(BULLET("En paralelo e inmediato: estimar la FRF de Bohn en frecuencia anual sobre 1983–2025 (n ≈ 43) para tener ya un resultado sobre el período democrático completo."));
C.push(BULLET("Decidir la variable de umbral del test de fatiga fiscal: EMBI+ (actual) frente a alternativas menos volátiles (ratio de deuda en moneda extranjera, cobertura de reservas sobre vencimientos)."));
C.push(BULLET("Reconstruir el TCRM 1983–1996 (BCRA / CEPAL) para completar el sistema de cointegración sobre la ventana larga."));
C.push(
  DECISION(
    "prioridad 1: la FRF anual 1983–2025, que no depende de ningún empalme trimestral y da un resultado " +
      "sobre el período completo de inmediato. Prioridad 2: el empalme fiscal trimestral y la " +
      "reestimación del SVAR y el DSA sobre 1983–2025."
  )
);

// ── Referencias ────────────────────────────────────────────────────────────
C.push(H1("Referencias"));
[
  "Alberola, E., Kataryniuk, I., Melguizo, Á. y Orozco, R. (2016). Fiscal policy and the cycle in Latin America: the role of financing conditions and fiscal rules. BIS Working Papers 543.",
  "Bai, J. y Perron, P. (2003). Computation and analysis of multiple structural change models. Journal of Applied Econometrics, 18(1), 1–22.",
  "Blanchard, O. y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. Quarterly Journal of Economics, 117(4), 1329–1368.",
  "Bohn, H. (1998). The behavior of U.S. public debt and deficits. Quarterly Journal of Economics, 113(3), 949–963.",
  "Cetrángolo, O., Damill, M., Frenkel, R. y Jiménez, J. P. (1997). La sostenibilidad de la política fiscal en América Latina: el caso argentino. Banco Interamericano de Desarrollo.",
  "Cox, J., Ingersoll, J. y Ross, S. (1985). A theory of the term structure of interest rates. Econometrica, 53(2), 385–407.",
  "Daude, C., Melguizo, Á. y Neut, A. (2011). Fiscal policy in Latin America: countercyclical and sustainable? Economics: The Open-Access, Open-Assessment E-Journal, 5, 2011-14.",
  "Favero, C. y Giavazzi, F. (2007). Debt and the effects of fiscal policy. NBER Working Paper 12822.",
  "Ghosh, A., Kim, J., Mendoza, E., Ostry, J. y Qureshi, M. (2013). Fiscal fatigue, fiscal space and debt sustainability in advanced economies. The Economic Journal, 123(566), F4–F30.",
  "Girouard, N. y André, C. (2005). Measuring cyclically-adjusted budget balances for OECD countries. OECD Economics Department Working Paper 434.",
  "Hansen, B. (1999). Threshold effects in non-dynamic panels: estimation, testing, and inference. Journal of Econometrics, 93(2), 345–368.",
  "Hansen, B. y Seo, B. (2002). Testing for two-regime threshold cointegration in vector error-correction models. Journal of Econometrics, 110(2), 293–318.",
  "Kehoe, T. y Nicolini, J. P. (eds.) (2021). A Monetary and Fiscal History of Latin America, 1960–2017. University of Minnesota Press.",
  "Neumeyer, P. y Perri, F. (2005). Business cycles in emerging economies: the role of interest rates. Journal of Monetary Economics, 52(2), 345–380.",
  "Staiger, D. y Stock, J. (1997). Instrumental variables regression with weak instruments. Econometrica, 65(3), 557–586.",
  "Stock, J. y Watson, M. (1993). A simple estimator of cointegrating vectors in higher order integrated systems. Econometrica, 61(4), 783–820.",
  "Uribe, M. y Yue, V. (2006). Country spreads and emerging countries: who drives whom? Journal of International Economics, 69(1), 6–36.",
].forEach((r) => C.push(REF(r)));

// ═══════════════════════════ Documento ════════════════════════════════════
const doc = new Document({
  creator: "Federico Chillón, Santiago Páez, Emiliano Carricondo — FCE UNCUYO",
  title:
    "Deuda Pública y Riesgo Soberano en Argentina desde el Retorno a la Democracia (1983–2025) — Nota metodológica",
  description:
    "Período de análisis, proceso completo, empalme de series y proxy de largo plazo del EMBI+, VAR estructural restringido, resto del protocolo, estructura de la tesis y próximos pasos.",
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  numbering: {
    config: [
      {
        reference: "vinetas",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "–",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: convertInchesToTwip(0.32), hanging: convertInchesToTwip(0.2) },
              },
            },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          margin: {
            top: convertInchesToTwip(1),
            bottom: convertInchesToTwip(1),
            left: convertInchesToTwip(1.1),
            right: convertInchesToTwip(1.1),
          },
        },
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: SMALL })],
            }),
          ],
        }),
      },
      children: C,
    },
  ],
});

const outPath = path.join(__dirname, "SVAR_Metodologia_Resultados_Accesible.docx");
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log("Documento Word generado:", outPath, "(" + buffer.length + " bytes)");
});
