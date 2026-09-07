/**
 * Nota metodológica en Word — tesis "Deuda Pública Consolidada y Fatiga Fiscal
 * en Argentina (2004–2025)".
 *
 * Objeto del documento: reunir los RESULTADOS DE LOS TESTS de los dos
 * componentes que todavía hay que decidir cómo entran en la tesis final —
 * (A) el VAR estructural restringido y (B) el empalme de series para un proxy
 * de largo plazo del EMBI+ — y, para cada uno, explicar para qué sirve, de modo
 * de poder elegir después qué versión se usa.
 *
 * Todas las cifras provienen de resultados/tablas/ y de los capítulos 4–8 de la
 * tesis. No hay valores fabricados.
 *
 * Formato: tipografía única (Calibri), sin saltos de página. Ecuaciones nativas
 * de Word (OMML), no imágenes.
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
const BODY = 22; // 11 pt
const SMALL = 19; // 9.5 pt
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
      new TextRun({
        text: f.t,
        italics: !!f.i,
        bold: !!f.b,
        font: FONT,
        size: BODY,
      })
  );
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 140, line: 300 },
    children: runs,
  });
};

// bloque "Para la tesis final:" — sangría y barra a la izquierda
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

const mr = (t) => new MathRun(t);
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
        children: r.map((c, i) =>
          cell(c, i, { bottom: ri === rows.length - 1 ? thick : nb })
        ),
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
        text: "Deuda Pública Consolidada y Fatiga Fiscal en Argentina, 2004–2025",
        bold: true,
        font: FONT,
        size: 32,
      }),
    ],
  }),
  new Paragraph({
    spacing: { after: 210 },
    children: [
      new TextRun({
        text:
          "Nota metodológica — resultados de los tests del VAR estructural restringido y del " +
          "empalme de series para un proxy de largo plazo del EMBI+",
        italics: true,
        font: FONT,
        size: 24,
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
          "Este documento reúne los resultados de los contrastes econométricos de dos componentes de " +
          "la tesis que todavía hay que decidir cómo entran en la versión final: el VAR estructural " +
          "restringido (Parte A) y el empalme de series para reconstruir un proxy de largo plazo del " +
          "riesgo soberano (Parte B). Para cada test se indica qué mide, qué resultado dio y para qué " +
          "sirve al momento de elegir la especificación. La Parte C sintetiza la decisión; la Parte D " +
          "deja registrado el resto del protocolo. Toda cifra proviene de resultados/tablas/ y de los " +
          "capítulos 4 a 8.",
        font: FONT,
        size: BODY,
      }),
    ],
  })
);

// ═══════════════════════ PARTE A — VAR ESTRUCTURAL RESTRINGIDO ══════════════
C.push(H1("A. VAR estructural restringido (SVAR)"));

C.push(H2("A.1. Qué es y qué decide"));
C.push(
  P(
    "Un VAR reducido describe cómo cada variable depende de los rezagos de todas las demás, pero sus " +
      "innovaciones están correlacionadas entre sí y no pueden interpretarse como shocks económicos. " +
      "Para pasar de esas innovaciones a shocks estructurales hace falta imponer restricciones. El " +
      "ordenamiento de Cholesky lo hace de forma puramente estadística —según el orden en que se listan " +
      "las variables— y es arbitrario. El SVAR restringido reemplaza ese orden por tres restricciones " +
      "con fundamento económico, sobre el vector de cinco variables:"
  )
);
C.push(EQ(sub("A", "0"), " ", sub("u", "t"), " = B ", sub("e", "t"), "        ",
  sub("Y", "t"), " = ( ", sub("ỹ", "t"), ", ", sub("pb", "t"), ", ",
  sub("EMBI", "t"), ", ", sub("TCRM", "t"), ", ", sub("d", "t"), " )"));
C.push(
  BULLET([
    { t: "Rigidez de la decisión presupuestaria. El superávit primario solo reacciona dentro del trimestre a la brecha del producto a través de la semi-elasticidad cíclica automática de la recaudación, " },
    { t: "α", i: true },
    { t: "y", i: true },
    { t: " = 0,25 (estándar OCDE/FMI: Girouard y André 2005; Daude et al. 2011; Alberola et al. 2016). No reacciona dentro del trimestre a shocks de riesgo ni de tipo de cambio." },
  ])
);
C.push(
  BULLET(
    "Ajuste financiero inmediato. El riesgo soberano y el tipo de cambio real, como precios de mercado, " +
      "absorben contemporáneamente todas las perturbaciones del período."
  )
);
C.push(BULLET("Identidad de acumulación de la deuda (Favero y Giavazzi, 2007):"));
C.push(EQ(sub("d", "t"), " = ", frac(["1 + ", sub("r", "t")], ["1 + ", sub("g", "t")]),
  " ", sub("d", "t-1"), " − ", sub("pb", "t"), " + ", sub("sft", "t")));
C.push(
  P(
    "Frente a un Cholesky puro, la única restricción adicional es fijar el coeficiente del superávit " +
      "sobre la brecha en 0,25 en lugar de estimarlo libremente: el sistema queda sobreidentificado en " +
      "un grado."
  )
);

C.push(H2("A.2. Selección de rezagos y especificación"));
C.push(
  P(
    "Se estima con dos rezagos sobre 86 observaciones (2004T1–2025T2, la ventana original con dos " +
      "trimestres consumidos por los rezagos). Los cuatro criterios de información no coinciden: AIC, " +
      "FPE y HQIC seleccionan dos rezagos; BIC selecciona uno. Se adopta dos por mayoría. El VAR(2) " +
      "arroja AIC = 12,66, BIC = 14,23 y HQIC = 13,29."
  )
);
C.push(
  DECISION(
    "el orden de rezagos no es unánime. La especificación de referencia es VAR(2); conviene reportar " +
      "en un anexo la FEVD con un solo rezago para mostrar que el ordenamiento cualitativo (dominancia " +
      "del shock primario y del ciclo) no cambia."
  )
);

C.push(H2("A.3. Matriz de impacto contemporáneo (S)"));
C.push(
  P(
    "La matriz S = A₀⁻¹B traduce un shock estructural de un desvío estándar en el efecto instantáneo " +
      "sobre cada variable. Los coeficientes relevantes (fase19_svar_matriz_impacto_S.csv):"
  )
);
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
    "Lectura: un shock estructural al riesgo soberano equivale a unos 473 puntos básicos de " +
      "perturbación instantánea; un deterioro del superávit primario de un desvío estándar eleva el " +
      "EMBI+ en 222 puntos dentro del mismo trimestre. Esto cuantifica el canal de credibilidad " +
      "fiscal: el mercado castiga el desvío fiscal de inmediato."
  )
);
C.push(
  DECISION(
    "la matriz S es el resultado más citable del canal fiscal → riesgo país. Sirve para el argumento " +
      "de que la consolidación fiscal tiene un retorno inmediato en spread, complementario al DSA."
  )
);

C.push(H2("A.4. Descomposición de varianza del error de pronóstico (FEVD)"));
C.push(
  P(
    "La FEVD reparte la varianza del error de pronóstico de cada variable, a cada horizonte, entre los " +
      "cinco shocks estructurales. Es el resultado principal del SVAR (fase19_fevd.csv):"
  )
);
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
    "A mediano plazo, la varianza de la deuda está dominada por el shock al resultado primario (47,5 % " +
      "a veinte trimestres) y por el shock a la brecha del producto (28,6 %); los shocks cambiario y de " +
      "riesgo soberano explican en conjunto 11,5 % y la inercia propia cae de 26 % a 12 %. En la " +
      "ecuación del EMBI+, el shock propio explica el 73 % de la varianza en el primer trimestre pero " +
      "cede hasta el 36 % a cinco años, cuando el shock fiscal alcanza una participación equivalente: " +
      "el mercado incorpora el historial fiscal a la prima con el tiempo."
  )
);
C.push(
  P([
    { t: "Precisión importante: esto describe " },
    { t: "qué perturbaciones mueven la deuda", i: true },
    { t: " período a período (desbalances primarios y ciclo), y no debe confundirse con la existencia de una regla de reacción fiscal estabilizadora —cuya ausencia documentan DOLS y el VECM— ni con los canales por los que se resolvieron históricamente los sobreendeudamientos (depreciación real, licuación, reestructuraciones)." },
  ])
);
C.push(
  DECISION(
    "la FEVD entra en la tesis como validación estructural del diagnóstico de DOLS/VECM, no como " +
      "contraste de la hipótesis de reacción fiscal. El titular es: los desbalances primarios y el " +
      "ciclo explican tres cuartas partes de la varianza de la deuda; el riesgo país y el tipo de " +
      "cambio, un papel acotado."
  )
);

C.push(H2("A.5. Impulso-respuesta y diagnóstico del VAR reducido"));
C.push(
  P(
    "Las funciones de impulso-respuesta se calculan con bandas bootstrap al 95 % (1.000 réplicas por " +
      "remuestreo residual). El VAR reducido, ecuación por ecuación, muestra una estructura de " +
      "persistencia marcada y coeficientes cruzados casi todos no significativos:"
  )
);
C.push(
  BULLET(
    "Deuda/PIB: fuertemente autorregresiva (coeficiente del primer rezago 1,06, t = 8,1); ningún " +
      "regresor cruzado significativo."
  )
);
C.push(
  BULLET(
    "EMBI+: persistente (primer rezago 0,76, t = 6,7); responde con dos rezagos a la deuda (43,7, " +
      "t = 2,0) y a la brecha (19,7, t = 1,9)."
  )
);
C.push(
  BULLET(
    "Brecha del producto: la deuda rezagada la anticipa (primer rezago −0,65, t = −3,1; segundo " +
      "+0,65, t = 3,0), señal de causalidad de Granger deuda → actividad."
  )
);
C.push(
  BULLET(
    "Superávit primario: solo su propio rezago es significativo (0,76, t = 5,5); no reacciona a " +
      "rezagos de deuda, EMBI+ ni TCRM —consistente con la ausencia de regla de reacción."
  )
);
C.push(
  P(
    "La matriz de correlación de residuos del VAR indica que las relaciones contemporáneas que " +
      "importan son superávit–deuda (−0,47, la más fuerte) y superávit–EMBI+ (−0,21); superávit–TCRM " +
      "es +0,17. La restricción de identificación (rigidez intra-trimestral del superávit) preserva " +
      "estas dos: el superávit se deja reaccionar al ciclo por la vía automática y su co-movimiento con " +
      "deuda y riesgo queda capturado por la identidad de acumulación y por la fila del EMBI+."
  )
);
C.push(
  DECISION(
    "el diagnóstico del VAR reducido es el respaldo de que la restricción de identificación no " +
      "descarta información sustantiva. Va en el anexo metodológico, no en el cuerpo."
  )
);

// ═══════════════ PARTE B — EMPALME Y PROXY DE LARGO PLAZO DEL EMBI+ ═════════
C.push(H1("B. Empalme de series: proxy de largo plazo del EMBI+"));

C.push(H2("B.1. El problema"));
C.push(
  P(
    "El índice EMBI no existe antes de 1993 y el EMBI+ oficial de Argentina no antes de 1998. La " +
      "muestra central (2004–2025) cubre apenas dos décadas y coincide, en su mayor parte, con un " +
      "régimen de riesgo soberano comprimido (2005–2019). Para responder si el umbral de fatiga fiscal " +
      "de ~2.080 puntos básicos y el nivel de equilibrio del spread son regularidades estructurales o " +
      "artefactos de la ventana, se reconstruye una serie trimestral homogénea de costo de " +
      "financiamiento soberano para los 42 años de democracia (1983T4–2025T4, 169 trimestres)."
  )
);

C.push(H2("B.2. Reconstrucción por eras financieras"));
C.push(BULLET("Era Bonex (1983T4–1992T4): rendimiento en dólares de los Bonos Externos (Series 1982, 1984, 1987, 1989) menos la tasa del Treasury a 10 años, según Neumeyer y Perri (2005) y Kehoe y Nicolini (2021), con registros de CEMA, FIEL y BCRA."));
C.push(BULLET("Era Brady (1993T1–1997T4): JP Morgan EMBI Argentina stripped spread sobre bonos Brady Par, Discount y FRB (Uribe y Yue, 2006)."));
C.push(BULLET("Era EMBI+ (1998T1–2025T4): serie oficial de JP Morgan EMBI+ / EMBI Global Diversified Argentina."));
C.push(
  P(
    "Para evitar saltos de nivel en los puntos de unión se aplica una corrección proporcional de sesgo " +
      "en el solapamiento: cada tramo antiguo se reescala al nivel del tramo siguiente mediante el " +
      "cociente de medias en el trimestre de empalme."
  )
);
C.push(
  EQ(sub("k", "1"), " = ", frac(sub("EMBI", "Brady, 1993T1"), sub("Spread", "Bonex, 1992T4")),
    " = ", frac("850", "760"), " = 1,118", "        ",
    sub("k", "2"), " = ", frac(sub("EMBI+", "1998T1"), sub("EMBI", "Brady, 1997T4")),
    " = ", frac("540", "620"), " = 0,871")
);
C.push(
  P(
    "El factor compuesto Bonex → EMBI+ es 1,118 × 0,871 = 0,974. La serie resultante queda toda " +
      "expresada en escala EMBI+ (spread_empalmado, en fase22 / spread_soberano_historico_1983_2025.csv)."
  )
);
C.push(
  NOTE(
    "El tramo Bonex 1983–1992 es una serie reconstruida a partir de la literatura y calibrada a hitos " +
      "trimestrales, no una serie de precios observada. Es un proxy de nivel y de régimen, no un dato " +
      "de mercado con la misma calidad que el EMBI+ post-1998."
  )
);
C.push(
  DECISION(
    "la serie de 42 años sirve para robustez cualitativa —¿hay regímenes persistentes?, ¿el nivel de " +
      "equilibrio es alto?— y no para inferencia fina. En la tesis va como “extensión de frontera”, no " +
      "como muestra de estimación principal."
  )
);

C.push(H2("B.3. Test 1 — Quiebres estructurales de Bai-Perron (1983–2025)"));
C.push(
  P(
    "Sobre los 169 trimestres se aplica el algoritmo de programación dinámica de Bai y Perron (2003) " +
      "en la media del spread (modelo L2, tamaño mínimo de segmento 8 trimestres). Se imponen cinco " +
      "quiebres —no se seleccionan por criterio de información como en la muestra central—, que definen " +
      "seis regímenes de financiamiento:"
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
    [850, 2050, 1050, 1000, 3550],
    ["l", "l", "r", "r", "l"]
  )
);
C.push(GAP());
C.push(
  P(
    "Los seis regímenes son persistentes (el más corto dura ocho trimestres) y recurrentes: Argentina " +
      "alterna entre un nivel “normal” de 680–830 puntos básicos y episodios de crisis de 1.700 a 5.400 " +
      "puntos. El régimen 6 (media 1.732) y el régimen 4 (media 5.431) encuadran el umbral de fatiga " +
      "fiscal de ~2.080 puntos estimado en la muestra central: ese umbral cae dentro del rango " +
      "histórico de tensión, no en un valor extremo."
  )
);
C.push(
  DECISION(
    "Bai-Perron histórico responde la pregunta “¿el umbral es estructural?”: sí, en el sentido de que " +
      "los regímenes de alto spread son un rasgo repetido de 42 años. Entra como argumento de que la " +
      "fatiga fiscal no es un fenómeno de las últimas dos décadas."
  )
);

C.push(H2("B.4. Test 2 — Calibración CIR del riesgo soberano, tres ventanas"));
C.push(
  P(
    "El proceso de Cox, Ingersoll y Ross (1985) modela el spread como una difusión con reversión a la " +
      "media y no negatividad estricta:"
  )
);
C.push(
  EQ("d(", sub("risk", "t"), ") = κ ( θ − ", sub("risk", "t"), " ) dt + σ ",
    rad([sub("risk", "t")]), " d", sub("W", "t"))
);
C.push(
  P([
    { t: "κ es la velocidad de reversión (la vida media es ln 2 ⁄ κ), θ el nivel de equilibrio de largo plazo y σ la volatilidad. La no negatividad del spread está garantizada si se cumple la condición de Feller, " },
    { t: "2κθ > σ²", i: true },
    { t: ". La calibración es por máxima verosimilitud exacta sobre la densidad de transición Chi-cuadrado no central. Se estima sobre las tres ventanas:" },
  ])
);
C.push(GAP());
C.push(
  academicTable(
    ["Ventana", "n", "κ", "θ (pb)", "Vida media", "σ", "Feller (ratio)", "AIC: CIR vs. AR(1)"],
    [
      ["2004–2025", "87", "0,923", "1.032", "0,75 años", "26,9", "cumple (2,63)", "1.279 < 1.342"],
      ["1999–2025", "108", "0,428", "1.590", "1,62 años", "26,5", "cumple (1,94)", "1.595 < 1.673"],
      ["1983–2025", "169", "0,463", "1.457", "1,50 años", "24,8", "cumple (2,20)", "2.467 < 2.613"],
    ],
    [1250, 500, 700, 800, 1050, 650, 1300, 1650],
    ["l", "r", "r", "r", "r", "r", "l", "l"]
  )
);
C.push(GAP());
C.push(
  NOTE(
    "Fuentes: fase20_cir_calibracion.csv (ventanas 2004–2025 y 1999–2025) y " +
      "fase22_cir_calibracion_1983_2025.csv (42 años). En las tres ventanas el CIR domina a un AR(1) " +
      "por AIC y se cumple la condición de Feller."
  )
);
C.push(
  P(
    "El parámetro que importa para la decisión es θ, el nivel de spread al que Argentina revierte en el " +
      "largo plazo. La ventana corta 2004–2025 da 1.032 puntos básicos, un valor sesgado a la baja por " +
      "haber transcurrido en su mayor parte dentro del régimen comprimido 2005–2019. Las ventanas que " +
      "incorporan la crisis de 2001–2002 y/o la década de 1980 elevan θ a 1.457–1.590 puntos: un proxy " +
      "más creíble del piso estructural del riesgo argentino. La velocidad de reversión, en cambio, es " +
      "más estable en términos económicos: la vida media va de nueve meses a año y medio, todas dentro " +
      "de un rango que implica reversión rápida."
  )
);
C.push(
  DECISION(
    "para el DSA de la tesis conviene usar θ de la ventana larga (≈1.457 pb) o de la 1999–2025 " +
      "(≈1.590 pb) como escenario base de la tasa de refinanciación, y θ de la ventana corta " +
      "(≈1.032 pb) como escenario optimista. Reportar la sensibilidad de la probabilidad de " +
      "insolvencia a esa elección."
  )
);

C.push(H2("B.5. Test 3 — CIR de dos factores (riesgo global vs. riesgo local)"));
C.push(
  P(
    "Una calibración alternativa descompone el spread en dos componentes independientes, uno rápido " +
      "asociado al ciclo de riesgo global y otro lento asociado al riesgo idiosincrático argentino:"
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
    [2600, 700, 900, 900, 1400],
    ["l", "r", "r", "r", "r"]
  )
);
C.push(GAP());
C.push(
  P(
    "El componente estructural revierte lentamente (vida media de más de tres años) hacia 671 puntos " +
      "básicos: ese sería el proxy más limpio del riesgo-país argentino de largo plazo, depurado del " +
      "ruido del apetito de riesgo global. El componente transitorio, rápido y de nivel bajo, recoge el " +
      "contexto externo."
  )
);
C.push(
  DECISION(
    "el CIR de dos factores es útil si la tesis quiere separar cuánto del EMBI+ es “responsabilidad de " +
      "Argentina” y cuánto es contexto. Como es una calibración exploratoria (fase20_cir_2factores.csv, " +
      "sin bandas), va como recuadro, no como resultado central."
  )
);

C.push(H2("B.6. Contexto — el spread por administración presidencial"));
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

// ═══════════════════════ PARTE C — DECISIÓN ════════════════════════════════
C.push(H1("C. Síntesis: qué usar en la tesis final"));
C.push(GAP());
C.push(
  academicTable(
    ["Componente", "Resultado principal", "Rol recomendado en la tesis"],
    [
      [
        "SVAR — FEVD",
        "Deuda: 47,5 % superávit, 28,6 % ciclo, 11,5 % EMBI+/TCRM (h = 20)",
        "Cuerpo. Validación estructural del diagnóstico DOLS/VECM.",
      ],
      [
        "SVAR — matriz S",
        "Shock fiscal negativo → +222 pb de EMBI+ en el trimestre",
        "Cuerpo. Evidencia del retorno inmediato de la consolidación en spread.",
      ],
      [
        "SVAR — IRF y VAR reducido",
        "Persistencia alta; sin reacción del superávit a rezagos de deuda/EMBI+",
        "Anexo metodológico.",
      ],
      [
        "Empalme 1983–2025",
        "Serie homogénea de 169 trimestres, escala EMBI+",
        "Extensión de frontera. Declarar la limitación del tramo Bonex.",
      ],
      [
        "Bai-Perron histórico",
        "6 regímenes; el umbral de ~2.080 pb cae dentro del rango de tensión histórico",
        "Cuerpo. Argumento de que la fatiga fiscal no es un fenómeno reciente.",
      ],
      [
        "CIR — tres ventanas",
        "θ: 1.032 pb (2004–25) vs. 1.457–1.590 pb (ventanas largas)",
        "Cuerpo. θ largo como base del DSA, θ corto como optimista.",
      ],
      [
        "CIR — dos factores",
        "Riesgo local estructural θ ≈ 671 pb, vida media 3,15 años",
        "Recuadro exploratorio.",
      ],
    ],
    [2100, 3600, 3600],
    ["l", "l", "l"]
  )
);
C.push(GAP());
C.push(
  P(
    "La tensión de fondo es longitud muestral contra homogeneidad institucional. La ventana corta es " +
      "la más limpia en datos pero la menos representativa del riesgo estructural argentino; la larga es " +
      "la más representativa pero descansa en una reconstrucción para su primer tercio. La " +
      "recomendación operativa es usar la ventana 1999–2025 como puente —incorpora la crisis de " +
      "2001–2002 con datos reales de EMBI+— y la de 42 años solo para el argumento de regularidad " +
      "estructural."
  )
);

// ═══════════════════════ PARTE D — RESTO DEL PROTOCOLO ═════════════════════
C.push(H1("D. Resto del protocolo (registro breve)"));
C.push(
  P(
    "Para completar el cuadro, los otros contrastes de la Función de Reacción Fiscal, ya cerrados en " +
      "la tesis:"
  )
);
C.push(
  BULLET(
    "DOLS, muestra completa 2004–2025: coeficiente de reacción ρ = −0,0071 (error 0,012; p = 0,564). " +
      "No hay reacción lineal significativa."
  )
);
C.push(
  BULLET(
    "DOLS por subperíodos: ρ = 0,037 en 2004–2014 (p = 0,002) y 0,053 en 2015–2025 (p = 0,003). El " +
      "coeficiente es positivo dentro de cada régimen; el promedio se anula por composición."
  )
);
C.push(
  BULLET(
    "VECM, ventana ampliada 1999–2025: la velocidad de ajuste del superávit no es significativa " +
      "(α = 0,0044; p = 0,204); la que ajusta es la deuda (α = −0,111; p < 0,001)."
  )
);
C.push(
  BULLET(
    "IV-2SLS (instrumentos VIX y riesgo regional): F de primera etapa 13,0; Wu-Hausman p = 0,009 " +
      "(EMBI+ endógeno); Sargan p = 0,436 (instrumentos válidos); coeficiente del EMBI+ instrumentado " +
      "0,0017 (p = 0,076)."
  )
);
C.push(
  BULLET(
    "Umbral de Hansen: en niveles τ* = 449 pb, Sup-LM p = 0,076 (señal débil, partición 14 vs. 74); " +
      "en primera diferencia τ* = 2.083 pb, Sup-LM p < 0,001 (evidencia sólida de no linealidad)."
  )
);
C.push(
  BULLET(
    "Threshold VECM (Hansen-Seo): umbral τ* = 2.081 pb; la velocidad de ajuste fiscal cambia de signo " +
      "entre regímenes (+0,006 → −0,008), pero el contraste Sup-LM no es significativo (p = 0,625)."
  )
);
C.push(
  BULLET(
    "Bai-Perron sobre la deuda 2004–2025: quiebres en 2007T2, 2014T3 y 2018T1 (SPNF); 2007T2 y 2016T4 " +
      "(serie consolidada con el BCRA)."
  )
);
C.push(
  BULLET(
    "DSA estocástico a 2035 (Monte Carlo, 1.000 iteraciones, perturbaciones t de Student ν ≈ 4,8): " +
      "probabilidad de que la deuda supere el 100 % del PIB del 31,2 % en el escenario de referencia " +
      "(3,8 % optimista; 99,9 % de estrés); robusta entre 29,2 % y 33,4 % según la estructura de " +
      "dependencia, y 29,8 % integrando el proceso CIR."
  )
);

// ── Referencias ────────────────────────────────────────────────────────────
C.push(H1("Referencias"));
[
  "Alberola, E., Kataryniuk, I., Melguizo, Á. y Orozco, R. (2016). Fiscal policy and the cycle in Latin America: the role of financing conditions and fiscal rules. BIS Working Papers 543.",
  "Bai, J. y Perron, P. (2003). Computation and analysis of multiple structural change models. Journal of Applied Econometrics, 18(1), 1–22.",
  "Blanchard, O. y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. Quarterly Journal of Economics, 117(4), 1329–1368.",
  "Bohn, H. (1998). The behavior of U.S. public debt and deficits. Quarterly Journal of Economics, 113(3), 949–963.",
  "Cox, J., Ingersoll, J. y Ross, S. (1985). A theory of the term structure of interest rates. Econometrica, 53(2), 385–407.",
  "Daude, C., Melguizo, Á. y Neut, A. (2011). Fiscal policy in Latin America: countercyclical and sustainable? Economics: The Open-Access, Open-Assessment E-Journal, 5, 2011-14.",
  "Favero, C. y Giavazzi, F. (2007). Debt and the effects of fiscal policy. NBER Working Paper 12822.",
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
    "Deuda Pública Consolidada y Fatiga Fiscal en Argentina (2004–2025) — Nota metodológica (SVAR y empalme de series)",
  description:
    "Resultados de los tests del VAR estructural restringido y del empalme de series para un proxy de largo plazo del EMBI+, con criterio de decisión para la tesis final.",
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
                indent: {
                  left: convertInchesToTwip(0.32),
                  hanging: convertInchesToTwip(0.2),
                },
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
  console.log("Documento Word generado en:", outPath, "(" + buffer.length + " bytes)");
});
