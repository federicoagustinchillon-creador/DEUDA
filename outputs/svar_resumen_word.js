/**
 * Genera la nota metodológica en Word del componente econométrico de la tesis
 * "Deuda Pública Consolidada y Fatiga Fiscal en Argentina (2004–2025)".
 *
 * El documento reúne, con las ecuaciones del protocolo y las cifras estimadas,
 * el modelo SVAR restringido, los contrastes de umbral (Hansen y TVECM), la
 * reconstrucción del spread soberano 1983–2025 y el análisis de sostenibilidad
 * estocástico. Todas las cifras provienen de resultados/tablas/ y de los
 * capítulos 4 a 8 de la tesis; no hay valores fabricados.
 *
 * Formato: una sola tipografía (Calibri), sin saltos de página. Las ecuaciones
 * se incrustan como imagen renderizada con Computer Modern (LaTeX) por
 * render_eqs.py, para que se vean igual en cualquier versión de Word.
 * Ejecutar antes: python outputs/render_eqs.py
 *
 * Autores: Federico Chillón · Santiago Páez · Emiliano Carricondo
 * Facultad de Ciencias Económicas — Universidad Nacional de Cuyo
 *
 * Salida: outputs/SVAR_Metodologia_Resultados_Accesible.docx
 */

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
  ImageRun,
  convertInchesToTwip,
} = require("docx");
const fs = require("fs");
const path = require("path");

// Manifiesto de imágenes de ecuaciones (generado por render_eqs.py, tipografía
// Computer Modern, DPI 240). Se incrustan como imagen para que rendericen con
// calidad LaTeX de forma idéntica en cualquier versión de Word.
const EQ_DIR = path.join(__dirname, "eq_img");
const EQ_MANIFEST = JSON.parse(
  fs.readFileSync(path.join(EQ_DIR, "manifest.json"), "utf-8")
);
const EQ_SOURCE_DPI = 240;
const EQ_DISPLAY_DPI = 150; // efectivo: cuanto mayor, más pequeña la ecuación
const EQ_MAX_WIDTH_PX = 600; // ancho de caja de texto de la página, a 96 DPI

// ───────────────────────── Parámetros de estilo ─────────────────────────────

const FONT = "Calibri";
const BODY = 22; // 11 pt
const SMALL = 19; // 9.5 pt
const RULE = "000000";

// ───────────────────────── Helpers de párrafo ───────────────────────────────

const H1 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 340, after: 130 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 26 })],
  });

const H2 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 100 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 23 })],
  });

// Prosa corrida. Acepta un array de fragmentos {t, i?, b?} o un string.
const P = (content, opts = {}) => {
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
    indent:
      opts.firstLine === false
        ? undefined
        : { firstLine: convertInchesToTwip(0.3) },
    children: runs,
  });
};

const NOTE = (text) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 40, after: 200 },
    children: [
      new TextRun({ text: "Nota. ", italics: true, font: FONT, size: SMALL }),
      new TextRun({ text, italics: true, font: FONT, size: SMALL }),
    ],
  });

const BULLET = (content) => {
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
    indent: {
      left: convertInchesToTwip(0.35),
      hanging: convertInchesToTwip(0.35),
    },
    children: [new TextRun({ text, font: FONT, size: SMALL })],
  });

// ── Ecuación: imagen Computer Modern centrada, escalada a la página ─────────
const EQ = (key) => {
  const m = EQ_MANIFEST[key];
  if (!m) throw new Error("ecuación no encontrada en el manifiesto: " + key);
  let w = (m.w * 96) / EQ_DISPLAY_DPI;
  let h = (m.h * 96) / EQ_DISPLAY_DPI;
  if (w > EQ_MAX_WIDTH_PX) {
    const f = EQ_MAX_WIDTH_PX / w;
    w *= f;
    h *= f;
  }
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 140, after: 170 },
    children: [
      new ImageRun({
        type: "png",
        data: fs.readFileSync(path.join(EQ_DIR, m.file)),
        transformation: { width: Math.round(w), height: Math.round(h) },
      }),
    ],
  });
};

// ───────────────────────── Tabla sobria (solo reglas horizontales) ──────────

function academicTable(headers, rows, widths, aligns) {
  const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const thin = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  const thick = { style: BorderStyle.SINGLE, size: 8, color: RULE };

  const mkCell = (
    txt,
    i,
    { bold = false, top = noBorder, bottom = noBorder } = {}
  ) =>
    new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      borders: { top, bottom, left: noBorder, right: noBorder },
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [
        new Paragraph({
          alignment:
            aligns[i] === "l" ? AlignmentType.LEFT : AlignmentType.RIGHT,
          spacing: { after: 0 },
          children: [
            new TextRun({ text: String(txt), bold, font: FONT, size: SMALL }),
          ],
        }),
      ],
    });

  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) =>
      mkCell(h, i, { bold: true, top: thick, bottom: thin })
    ),
  });

  const bodyRows = rows.map(
    (r, ri) =>
      new TableRow({
        children: r.map((c, i) =>
          mkCell(c, i, {
            bottom: ri === rows.length - 1 ? thick : noBorder,
          })
        ),
      })
  );

  return new Table({
    columnWidths: widths,
    width: {
      size: widths.reduce((a, b) => a + b, 0),
      type: WidthType.DXA,
    },
    rows: [headerRow, ...bodyRows],
  });
}

const GAP = () => new Paragraph({ text: "", spacing: { after: 60 } });

// ═══════════════════════════ CUERPO DEL DOCUMENTO ═══════════════════════════

const children = [];

// ── Encabezado del documento ───────────────────────────────────────────────
children.push(
  new Paragraph({
    spacing: { before: 0, after: 120 },
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
    spacing: { after: 220 },
    children: [
      new TextRun({
        text:
          "Nota metodológica: función de reacción fiscal, VAR estructural restringido, " +
          "umbrales de fatiga fiscal y sostenibilidad estocástica",
        italics: true,
        font: FONT,
        size: 24,
      }),
    ],
  }),
  new Paragraph({
    spacing: { after: 40 },
    children: [
      new TextRun({
        text: "Santiago Páez  ·  Emiliano Carricondo  ·  Federico Chillón",
        font: FONT,
        size: 22,
      }),
    ],
  }),
  new Paragraph({
    spacing: { after: 260 },
    children: [
      new TextRun({
        text:
          "Facultad de Ciencias Económicas — Universidad Nacional de Cuyo · Mendoza, 2026",
        font: FONT,
        size: 20,
      }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 160, line: 300 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE },
    },
    children: [
      new TextRun({
        text:
          "Este documento resume, con las ecuaciones del protocolo y las cifras estimadas, el " +
          "componente econométrico de la tesis. Acompaña al texto completo y a la guía de defensa; " +
          "su propósito es que cualquiera de los tres autores y el director puedan seguir de " +
          "principio a fin qué se estimó, con qué datos y qué arrojó cada modelo. Las series, tablas " +
          "y coeficientes que se citan están en el repositorio del proyecto, en resultados/tablas/, y " +
          "se corresponden con los capítulos 4 a 8 de la tesis.",
        font: FONT,
        size: BODY,
      }),
    ],
  })
);

// ── 1. Objeto y preguntas ──────────────────────────────────────────────────
children.push(H1("1. Objeto de estudio y preguntas"));
children.push(
  P(
    "La pregunta que ordena el trabajo es si el comportamiento fiscal argentino del período " +
      "2004–2025 satisface la restricción presupuestaria intertemporal del gobierno, o si, por el " +
      "contrario, la trayectoria de la deuda es insostenible en un sentido estadístico verificable. " +
      "Es una pregunta empíricamente falseable: el coeficiente de reacción fiscal puede resultar no " +
      "significativo o negativo, y de hecho así resulta en la especificación lineal de muestra completa."
  )
);
children.push(
  P(
    "Argentina ofrece un caso poco común. La historia fiscal reciente concentra la salida del default " +
      "de 2001, las reestructuraciones de 2005 y 2010, el default técnico con holdouts de 2014, el " +
      "programa con el Fondo Monetario Internacional de 2018, la reestructuración de 2020 y la " +
      "consolidación fiscal iniciada en 2024. El riesgo país medido por el EMBI+ promedió 2.416 puntos " +
      "básicos en el período, con un desvío estándar de 876 puntos, y recién en 2024–2025 comprimió " +
      "hacia el rango de 561 a 1.100 puntos. Esa variabilidad de régimen es, a la vez, el principal " +
      "obstáculo econométrico y el objeto que el trabajo se propone modelar."
  )
);
children.push(H2("Preguntas específicas"));
children.push(
  BULLET(
    "¿El coeficiente de reacción del resultado primario ante el stock de deuda rezagado es positivo y " +
      "significativo, una vez controlado el ciclo económico?"
  )
);
children.push(
  BULLET(
    "¿La corrección de la endogeneidad del riesgo soberano mediante variables instrumentales modifica " +
      "esa conclusión respecto de la estimación por mínimos cuadrados?"
  )
);
children.push(
  BULLET(
    "¿Existen quiebres estructurales múltiples en la ratio de deuda, detectados de forma endógena, que " +
      "invaliden un modelo de parámetros constantes para todo el período?"
  )
);
children.push(
  BULLET(
    "¿Hay un umbral de riesgo soberano por encima del cual la respuesta fiscal se atenúa o se invierte " +
      "—fatiga fiscal—, y en qué nivel se sitúa?"
  )
);
children.push(
  BULLET(
    "¿Cuál es la probabilidad de que la deuda supere el 100 % del PIB hacia 2035, bajo distintos " +
      "escenarios macroeconómicos y con perturbaciones de colas pesadas?"
  )
);

// ── 2. Datos y variables ───────────────────────────────────────────────────
children.push(H1("2. Datos y variables"));
children.push(
  P(
    "La unidad de análisis es el trimestre macroeconómico consolidado de Argentina. Se trabaja con dos " +
      "ventanas muestrales complementarias. La ventana original, 2004T1–2025T4 (88 observaciones), tiene " +
      "cobertura primaria homogénea de todas las variables y sostiene la estimación DOLS de referencia " +
      "junto con el resto del protocolo de robustez. La ventana ampliada, 1999T1–2025T4 (108 " +
      "observaciones), incorpora un tramo empalmado 1996–2003 mediante coeficiente de enlace y " +
      "desagregación de Denton, y sostiene la estimación del sistema de vectores con corrección de " +
      "error, que reemplaza a DOLS como técnica de referencia para la relación de largo plazo, a pedido " +
      "del director."
  )
);
children.push(
  P(
    "La deuda pública corresponde al stock bruto consolidado del Sector Público No Financiero, según " +
      "los estándares del Manual de Estadísticas de Finanzas Públicas del FMI. Se excluyen de la " +
      "definición central los pasivos remunerados del BCRA (LEBAC, LELIQ y pases), que se suman en una " +
      "serie consolidada alternativa como prueba de robustez: en promedio añaden 5,5 puntos del PIB, con " +
      "un pico de 10,6 % en 2018."
  )
);
children.push(GAP());
children.push(
  academicTable(
    ["Variable", "Símbolo", "Indicador operacional", "Fuente"],
    [
      ["Esfuerzo fiscal primario", "pb(t)", "Resultado primario del SPNF sobre PIB nominal (admite negativos)", "Hacienda (MECON)"],
      ["Stock de deuda heredado", "d(t−1)", "Deuda bruta consolidada del SPNF sobre PIB, rezagada un trimestre", "Finanzas (MECON)"],
      ["Ciclo macroeconómico", "ỹ(t)", "Brecha del producto, filtro HP (λ = 1600) sobre PIB real", "INDEC"],
      ["Riesgo soberano", "EMBI(t)", "Riesgo país EMBI+, promedio trimestral, en puntos básicos", "BCRA / Bloomberg"],
      ["Tipo de cambio real", "TCRM(t)", "Índice de tipo de cambio real multilateral (base BCRA)", "BCRA / datos.gob.ar"],
      ["Instrumentos externos", "—", "VIX (CBOE) y diferencial de riesgo soberano regional (ETF EMB)", "Yahoo Finance / Bloomberg"],
    ],
    [1900, 1000, 4100, 1800],
    ["l", "l", "l", "l"]
  )
);
children.push(GAP());
children.push(
  NOTE(
    "Un chequeo de trazabilidad reveló que, en la matriz original de 88 observaciones, el EMBI+ y el " +
      "TCRM provenían en su totalidad de fuentes de contingencia y no de una consulta API exitosa. La " +
      "matriz ampliada los reemplaza por las series reales del BCRA y de Ámbito Financiero en toda su " +
      "cobertura 1999–2025. El detalle está en la Sección 4.2.2 de la tesis."
  )
);

// ── 3. Marco formal ────────────────────────────────────────────────────────
children.push(H1("3. Marco formal de la sostenibilidad"));
children.push(
  P(
    "El punto de partida es la restricción presupuestaria intertemporal del gobierno. La condición de " +
      "solvencia exige que el valor presente descontado de los superávits primarios futuros iguale, al " +
      "menos, al stock de deuda vigente:"
  )
);
children.push(
  EQ("igbc")
);
children.push(
  P(
    "Esta condición no es directamente contrastable. Bohn (1998, 2007) propone una condición suficiente " +
      "que sí lo es: si el resultado primario responde positivamente al stock de deuda rezagado, la " +
      "restricción intertemporal se cumple de forma asintótica, sin necesidad de suponer una tasa de " +
      "descuento ni de proyectar a infinito, y sin exigir estacionariedad de las series. La función de " +
      "reacción fiscal, en su forma canónica, es:"
  )
);
children.push(
  EQ("bohn")
);
children.push(
  P([
    { t: "La hipótesis de sostenibilidad exige " },
    { t: "ρ > 0", i: true },
    { t: " con significatividad estadística. La proyección de trayectorias se apoya en la ecuación de movimiento de la ratio de deuda (Blanchard, 2019), donde el término " },
    { t: "(r − g)", i: true },
    { t: " gobierna el efecto de bola de nieve:" },
  ])
);
children.push(
  EQ("blanchard")
);
children.push(
  P(
    "El modelo de Ghosh et al. (2013) advierte que esta regla lineal esconde un límite: si la reacción " +
      "es positiva a niveles bajos de deuda o de riesgo, pero se anula o se vuelve negativa por encima " +
      "de cierto umbral, el contraste lineal informa sostenibilidad donde en realidad hay fatiga fiscal. " +
      "De ahí que el protocolo incluya modelos de umbral con punto de quiebre estimado de forma endógena."
  )
);

// ── 4. Estrategia econométrica ─────────────────────────────────────────────
children.push(H1("4. Estrategia econométrica"));
children.push(
  P(
    "El protocolo tiene seis etapas encadenadas, cada una diseñada para neutralizar un sesgo concreto " +
      "de la anterior: raíces unitarias y regresión espuria, endogeneidad de corto plazo, endogeneidad " +
      "del riesgo soberano, no linealidad de umbral y, finalmente, incertidumbre de escenario."
  )
);

children.push(H2("4.1. Estacionariedad y quiebres"));
children.push(
  P(
    "Sobre cada serie se aplican los contrastes ADF y KPSS, de hipótesis nulas opuestas, más el DF-GLS " +
      "de Elliott, Rothenberg y Stock (1996), de mayor potencia en muestras de este tamaño. Ante " +
      "diagnóstico ambiguo se añade el test de quiebre endógeno de Zivot y Andrews (1992), que estima la " +
      "fecha de ruptura por búsqueda del punto que minimiza el estadístico t del parámetro " +
      "autorregresivo. Sobre la ratio de deuda se implementa además el procedimiento de Bai y Perron " +
      "(2003): programación dinámica exacta sobre la suma de cuadrados residuales, con selección del " +
      "número de quiebres por criterio BIC."
  )
);

children.push(H2("4.2. Cointegración y vector con corrección de error"));
children.push(
  P(
    "El procedimiento de máxima verosimilitud de Johansen verifica si el sistema formado por la ratio " +
      "de deuda, el resultado primario, el riesgo soberano y el tipo de cambio real admite al menos una " +
      "combinación lineal estacionaria. El sistema se estima como vector con corrección de error:"
  )
);
children.push(
  EQ("vecm")
);
children.push(
  P([
    { t: "El vector " },
    { t: "β", i: true },
    { t: " recoge la relación de largo plazo, normalizada sobre la deuda; el vector " },
    { t: "α", i: true },
    { t: " contiene las velocidades de ajuste de cada variable hacia el equilibrio. La brecha del producto entra como variable exógena estacionaria. El rango de cointegración se fija en uno; en la ventana ampliada esa imposición no es neutral, porque el contraste de Johansen es sensible a incluir o no el año 1999, y esa fragilidad se documenta en lugar de ocultarse." },
  ])
);

children.push(H2("4.3. VAR estructural restringido"));
children.push(
  P(
    "Para identificar la transmisión de perturbaciones sin recurrir a un ordenamiento de Cholesky " +
      "arbitrario, se estima un VAR estructural restringido sobre el vector de cinco variables, " +
      "siguiendo el esquema de identificación contemporánea de Blanchard y Perotti (2002) y la " +
      "restricción de acumulación de deuda de Favero y Giavazzi (2007). El sistema estructural es:"
  )
);
children.push(
  EQ("svar")
);
children.push(P("Las restricciones, todas con fundamento teórico, son tres:"));
children.push(
  BULLET([
    { t: "Rigidez de la decisión presupuestaria. El resultado primario reacciona dentro del trimestre a la brecha del producto solo a través de la semi-elasticidad cíclica automática de la recaudación, " },
    { t: "αy = 0,25", i: true },
    { t: " (estándar OCDE/FMI para Argentina: Girouard y André, 2005; Daude et al., 2011; Alberola et al., 2016), y es rígido frente a shocks de riesgo y de tipo de cambio en el mismo trimestre." },
  ])
);
children.push(
  BULLET(
    "Ajuste inmediato de los precios financieros. El riesgo soberano y el tipo de cambio real absorben " +
      "contemporáneamente las perturbaciones macroeconómicas y fiscales del período."
  )
);
children.push(
  BULLET(
    "Identidad dinámica de acumulación. La deuda evoluciona restringida por la identidad de Favero y Giavazzi:"
  )
);
children.push(
  EQ("favero")
);
children.push(
  P([
    { t: "A partir de la matriz de impacto estructural estimada " },
    { t: "S = A0⁻¹ B", i: true },
    { t: " se calculan las funciones de impulso-respuesta con bandas bootstrap al 95 % (1.000 réplicas) y la descomposición de varianza del error de pronóstico." },
  ])
);
children.push(
  P(
    "DOLS no se descarta: se conserva como comparación metodológica sobre la ventana original, con la " +
      "especificación de Stock y Watson (1993), aumentada con cuatro adelantos y rezagos de la primera " +
      "diferencia de la deuda:"
  )
);
children.push(
  EQ("dols")
);

children.push(H2("4.4. Corrección de la endogeneidad del riesgo soberano"));
children.push(
  P(
    "La teoría predice causalidad inversa entre el resultado fiscal y el riesgo soberano: un deterioro " +
      "fiscal eleva la prima que exigen los acreedores, y una suba exógena del EMBI+ encarece el " +
      "financiamiento y presiona las cuentas públicas. Se instrumenta el EMBI+ con el índice de " +
      "volatilidad global VIX y un diferencial de riesgo soberano regional, y se estima por variables " +
      "instrumentales en dos etapas. La fuerza del diseño se evalúa con el estadístico F de primera " +
      "etapa (umbral de Staiger y Stock: mayor que 10), el test de endogeneidad de Wu-Hausman y el test " +
      "de sobreidentificación de Sargan."
  )
);

children.push(H2("4.5. Modelos de umbral y fatiga fiscal"));
children.push(
  P(
    "El contraste canónico de fatiga fiscal es el modelo de umbral de Hansen (1999), con punto de " +
      "quiebre determinado por el nivel de riesgo soberano:"
  )
);
children.push(
  EQ("hansen")
);
children.push(
  P([
    { t: "El umbral óptimo " },
    { t: "τ*", i: true },
    { t: " se estima por mínima suma de cuadrados residuales sobre una grilla de percentiles de la distribución empírica del EMBI+. La significatividad del quiebre se contrasta con el estadístico Sup-LM, cuya distribución bajo linealidad se aproxima por remuestreo con 1.000 réplicas (Hansen, 2000). El análisis se extiende al marco multivariado con el Threshold VECM de Hansen y Seo (2002), que permite que las velocidades de ajuste del vector " },
    { t: "α", i: true },
    { t: " conmuten de régimen según el estado del mercado financiero." },
  ])
);

children.push(H2("4.6. Simulación estocástica y proceso CIR"));
children.push(
  P(
    "El análisis de sostenibilidad se resuelve con una simulación de Monte Carlo de 1.000 iteraciones " +
      "en la que las variables fundamentales reciben perturbaciones de una distribución t de Student " +
      "multivariada con ν ≈ 4,8 grados de libertad —colas pesadas, calibradas a partir de la curtosis " +
      "histórica— acopladas a correlaciones dinámicas. La tasa de refinanciación externa se dota de " +
      "consistencia con la teoría de estructura temporal modelando el riesgo soberano como un proceso de " +
      "difusión con reversión a la media (Cox, Ingersoll y Ross, 1985):"
  )
);
children.push(
  EQ("cir")
);
children.push(
  P([
    { t: "El parámetro " },
    { t: "κ", i: true },
    { t: " es la velocidad de reversión, " },
    { t: "θ", i: true },
    { t: " el nivel de equilibrio de largo plazo y " },
    { t: "σ", i: true },
    { t: " la volatilidad de difusión. La no negatividad estricta del spread queda garantizada si se satisface la condición de Feller, " },
    { t: "2 κ θ > σ²", i: true },
    { t: ". La calibración se realiza por máxima verosimilitud exacta sobre la densidad de transición Chi-cuadrado no central." },
  ])
);

// ── 5. Resultados ──────────────────────────────────────────────────────────
children.push(H1("5. Resultados"));

children.push(H2("5.1. Reacción fiscal lineal: DOLS y VECM"));
children.push(
  P(
    "En la ventana original, el contraste de Johansen indica exactamente una relación de cointegración " +
      "entre las cuatro variables del sistema. La estimación DOLS de muestra completa no encuentra una " +
      "reacción lineal significativa al endeudamiento: el coeficiente es ρ = −0,0071, con error estándar " +
      "0,012 y p = 0,564; el R² del ajuste conjunto es 0,586. Un incremento de diez puntos del PIB en la " +
      "deuda rezagada se asocia con una variación de apenas −0,07 puntos en el resultado primario: la " +
      "falta de significatividad no enmascara un efecto cuantitativamente relevante."
  )
);
children.push(
  P(
    "El VECM de la ventana ampliada converge al mismo diagnóstico por una vía distinta. La velocidad de " +
      "ajuste del resultado primario hacia el equilibrio de largo plazo no es significativa " +
      "(α = 0,0044, p = 0,204), y tampoco lo es en cuatro de las cinco especificaciones alternativas de " +
      "rezagos. Es la propia deuda la que carga con la velocidad de ajuste significativa del sistema " +
      "(α = −0,111, p < 0,001): el sistema corrige desvíos, pero no a través de la política fiscal."
  )
);
children.push(GAP());
children.push(
  academicTable(
    ["Ecuación del sistema", "α (velocidad de ajuste)", "p", "¿Corrige?"],
    [
      ["Deuda / PIB", "−0,111", "< 0,001", "Sí"],
      ["Resultado primario", "+0,0044", "0,204", "No"],
      ["EMBI+", "+3,13", "0,306", "No"],
      ["Tipo de cambio real", "−0,001", "0,181", "No"],
    ],
    [3400, 2400, 1200, 1400],
    ["l", "r", "r", "r"]
  )
);
children.push(GAP());
children.push(
  NOTE(
    "VECM de la ventana ampliada 1999–2025, rango de cointegración uno, rezago por BIC. Vector de largo " +
      "plazo normalizado sobre la deuda: coeficientes 1,077 para el resultado primario, −0,012 para el " +
      "EMBI+ y 17,08 para el tipo de cambio real. Fuente: resultados/tablas/fase16_vecm_final_alpha.csv " +
      "y fase16_vecm_final_beta.csv."
  )
);

children.push(H2("5.2. Inestabilidad de parámetros entre subperíodos"));
children.push(
  P(
    "El coeficiente nulo de muestra completa oculta heterogeneidad. Estimado por subperíodos, el " +
      "parámetro de reacción resulta positivo y significativo en ambos: 0,037 en 2004–2014 (p = 0,002 " +
      "por mínimos cuadrados; 0,038 por DOLS con un adelanto/rezago, p = 0,063) y 0,053 en 2015–2025 " +
      "(p = 0,003 por mínimos cuadrados; 0,036 por DOLS, p = 0,038). El promedio de muestra completa se " +
      "acerca a cero porque combina regímenes con niveles de superávit muy distintos, no porque no haya " +
      "respuesta dentro de cada uno. Es el mismo fenómeno que detecta Bai-Perron."
  )
);

children.push(H2("5.3. VAR estructural restringido: qué mueve la deuda"));
children.push(
  P(
    "El SVAR se estima con dos rezagos sobre 86 observaciones (2004T1–2025T2). La matriz de impacto " +
      "contemporáneo cuantifica el canal de credibilidad fiscal: un shock estructural al riesgo soberano " +
      "equivale a unos 473 puntos básicos de perturbación instantánea, y un shock negativo de un desvío " +
      "estándar al resultado primario eleva el EMBI+ en 222 puntos dentro del mismo trimestre. La " +
      "descomposición de varianza del error de pronóstico reparte la variabilidad de cada variable entre " +
      "los cinco shocks estructurales:"
  )
);
children.push(GAP());
children.push(
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
children.push(GAP());
children.push(
  NOTE(
    "Descomposición de varianza en porcentaje. Identificación de Blanchard-Perotti (semi-elasticidad " +
      "0,25, rigidez intra-trimestral) e identidad de acumulación de Favero-Giavazzi. Fuente: " +
      "resultados/tablas/fase19_fevd.csv."
  )
);
children.push(
  P(
    "A horizontes de mediano plazo, la variabilidad de la deuda está dominada por los shocks al " +
      "resultado primario —47,5 % a veinte trimestres— y por los shocks a la brecha del producto " +
      "—28,6 %—, mientras que los shocks cambiarios y de riesgo soberano explican en conjunto apenas " +
      "11,5 % y la inercia propia de la deuda cae de 26 % a 12 % con el horizonte. Conviene ser preciso: " +
      "esto describe qué perturbaciones mueven la deuda período a período —desbalances primarios y " +
      "ciclo—, y no debe confundirse con la existencia de una regla de reacción estabilizadora, cuya " +
      "ausencia documentan DOLS y el VECM, ni con los canales por los que se resolvieron históricamente " +
      "los episodios de sobreendeudamiento —depreciación real, licuación inflacionaria y " +
      "reestructuraciones con quita—, que operan sobre el ajuste stock-flujo. En la ecuación del riesgo " +
      "soberano, el shock propio explica el 73 % de la varianza en el primer trimestre pero cede terreno " +
      "hasta el 36 % a cinco años, cuando el shock fiscal alcanza una participación equivalente: el " +
      "mercado termina incorporando el historial fiscal a la prima de riesgo."
  )
);

children.push(H2("5.4. Endogeneidad del riesgo soberano (IV-2SLS)"));
children.push(
  P(
    "Los instrumentos son relevantes: el estadístico F de primera etapa alcanza 13,00 (p = 0,002), por " +
      "encima del umbral de 10. El test de Wu-Hausman confirma que el EMBI+ es endógeno al esfuerzo " +
      "fiscal (7,32, p = 0,009). El test de Sargan no rechaza la validez conjunta de los instrumentos " +
      "(0,608, p = 0,436). El coeficiente del EMBI+ instrumentado es positivo (0,0017) y marginalmente " +
      "significativo al 10 % (p = 0,076), sobre una muestra reducida a 73 observaciones por la cobertura " +
      "del instrumento: un incremento de 100 puntos básicos en el riesgo soberano se asociaría con una " +
      "mejora de 0,17 puntos del PIB en el superávit primario. La evidencia es débil, pero con la serie " +
      "real ya no permite afirmar, como ocurría con la serie de contingencia, que la ausencia de " +
      "reacción por el canal de riesgo soberano esté firmemente establecida."
  )
);

children.push(H2("5.5. Umbrales de fatiga fiscal: Hansen y TVECM"));
children.push(
  P(
    "El modelo de umbral en niveles localiza un quiebre candidato en τ* = 449 puntos básicos, con una " +
      "reacción menor en el régimen de estrés (β₂ = 0,0126, p = 0,385) que en el régimen normal " +
      "(β₁ = 0,0305, p = 0,171), en el orden que predice la fatiga fiscal. El contraste Sup-LM rechaza " +
      "la linealidad solo al 10 % (p = 0,076), y la partición es muy desigual —14 trimestres normales " +
      "frente a 74 de estrés—, la condición en que un contraste de umbral es menos confiable; ninguno de " +
      "los dos coeficientes de régimen es individualmente significativo. Es una señal débil y frágil."
  )
);
children.push(
  P(
    "La especificación en primeras diferencias, que satisface el supuesto de estacionariedad exigido por " +
      "el test, ofrece evidencia más contundente: τ* = 2.083 puntos básicos, Sup-LM con p < 0,001, ambos " +
      "coeficientes de régimen significativos y con el patrón de atenuación esperado, sobre una " +
      "partición inversa (74 frente a 14) que no concentra el resultado en unas pocas observaciones. La " +
      "evidencia de umbral es, entonces, sensible a la especificación, pero ya no unilateralmente débil."
  )
);
children.push(
  P(
    "El Threshold VECM multivariado localiza un umbral casi idéntico, τ* = 2.081 puntos básicos, y una " +
      "inversión de signo en la velocidad de ajuste fiscal: α pasa de +0,0064 en el régimen de " +
      "normalidad (73 trimestres) a −0,0079 en el régimen de estrés (13 trimestres). El punto estimado " +
      "es coherente con la fatiga fiscal, pero su contraste Sup-LM no alcanza significatividad (52,24, " +
      "p = 0,625): el test multivariado pierde potencia al estimar 48 parámetros sobre 86 observaciones " +
      "repartidas de forma muy desigual entre regímenes."
  )
);

children.push(H2("5.6. Quiebres estructurales en la ratio de deuda"));
children.push(
  P(
    "El procedimiento de Bai-Perron identifica tres quiebres endógenos en la deuda del Sector Público No " +
      "Financiero: 2007T2, 2014T3 y 2018T1. Para la serie consolidada con los pasivos del BCRA, los " +
      "quiebres son dos: 2007T2 y 2016T4. Las fechas coinciden con hitos verificables —el pico del " +
      "superávit gemelo y la intervención del INDEC, el default técnico con holdouts, y la crisis " +
      "cambiaria con el acuerdo con el FMI— y confirman que un modelo de parámetros constantes para todo " +
      "el período está mal especificado."
  )
);

children.push(H2("5.7. El spread soberano en 42 años de democracia (1983–2025)"));
children.push(
  P(
    "No existía una serie continua y homogénea de spread soberano para todo el período democrático. Se " +
      "construyó empalmando tres fuentes: spread implícito de los Bonex para 1983–1992, calibrado con " +
      "Neumeyer y Perri (2005) y registros del CEMA, FIEL y BCRA; EMBI de bonos Brady para 1993–1997; y " +
      "EMBI+ oficial de JP Morgan desde 1998. El empalme usa corrección proporcional de sesgo en los " +
      "tramos de solapamiento. Sobre los 169 trimestres resultantes, Bai-Perron detecta cinco quiebres " +
      "que definen seis regímenes:"
  )
);
children.push(GAP());
children.push(
  academicTable(
    ["Régimen", "Período", "Media (pb)", "Desvío (pb)", "Hito de cierre"],
    [
      ["1", "1983T4–1988T4", "798", "359", "Agotamiento de reservas del BCRA"],
      ["2", "1989T1–1990T4", "3.574", "1.256", "Reversión de la desconfianza hiperinflacionaria"],
      ["3", "1991T1–2001T4", "832", "427", "Default y fin de la Convertibilidad"],
      ["4", "2002T1–2005T2", "5.431", "638", "Canje 2005 y cancelación del FMI"],
      ["5", "2005T3–2019T2", "684", "327", "Crisis cambiaria y acuerdo Stand-By con el FMI"],
      ["6", "2019T3–2025T4", "1.732", "632", "Cierre de muestra"],
    ],
    [900, 2100, 1100, 1000, 3400],
    ["l", "l", "r", "r", "l"]
  )
);
children.push(GAP());
children.push(
  NOTE("Fuente: resultados/tablas/fase22_bai_perron_1983_2025.csv. Test de Bai-Perron con cinco quiebres.")
);

children.push(H2("5.8. Calibración del proceso CIR"));
children.push(
  P(
    "Sobre la muestra homogénea 2004–2025, el proceso CIR del EMBI+ arroja una velocidad de reversión " +
      "κ = 0,923 —vida media de 0,75 años—, un nivel de equilibrio de largo plazo θ = 1.032 puntos " +
      "básicos y una volatilidad de difusión σ = 26,9. La condición de Feller se cumple con holgura " +
      "(2 κ θ = 1.905 > σ² = 725; ratio 2,63), de modo que el spread simulado no puede volverse " +
      "negativo, y el criterio AIC prefiere el CIR frente a un AR(1) (1.279 frente a 1.342). Sobre la " +
      "serie histórica de 42 años, la reversión es más lenta (κ = 0,463, vida media de 1,5 años) y el " +
      "nivel de equilibrio sube a 1.457 puntos básicos: la penalización de largo plazo al crédito " +
      "argentino es una regularidad estructural, no un rasgo del período reciente."
  )
);

children.push(H2("5.9. Análisis de sostenibilidad estocástico hacia 2035"));
children.push(
  P(
    "Partiendo de una ratio inicial del 74 % del PIB en 2025, la simulación de Monte Carlo proyecta la " +
      "trayectoria de la deuda a diez años bajo tres escenarios. El resultado central es la probabilidad " +
      "de que la ratio supere el 100 % del PIB hacia 2035:"
  )
);
children.push(GAP());
children.push(
  academicTable(
    ["Escenario", "Supuestos (superávit / crecimiento)", "P(deuda > 100 % PIB)", "Mediana 2035"],
    [
      ["Optimista", "2,5 % / 4,5 % anual", "3,8 %", "45,1 % PIB"],
      ["Referencia", "1,5 % / 3,5 % anual", "31,2 %", "80,7 % PIB"],
      ["Estrés", "0,5 % / contracción + 25 % de depreciación real", "99,9 %", "816,5 % PIB"],
    ],
    [1300, 3600, 2100, 1600],
    ["l", "l", "r", "r"]
  )
);
children.push(GAP());
children.push(
  NOTE(
    "Monte Carlo con 1.000 iteraciones y perturbaciones t de Student (ν ≈ 4,8). La cifra del 31,2 % del " +
      "escenario de Referencia es robusta a la especificación de la dependencia entre shocks: 29,2 % con " +
      "cópula gaussiana, 32,5 % con correlaciones dinámicas reestimadas, 33,4 % con volatilidad GARCH " +
      "parcial y 29,8 % integrando el proceso CIR en la tasa de refinanciación. Fuente: Sección 7.3 de la tesis."
  )
);
children.push(
  P(
    "La lectura es que la probabilidad de insolvencia depende mucho más del escenario macroeconómico de " +
      "origen que de cualquier ajuste fiscal discrecional marginal: va de prácticamente nula en el " +
      "escenario optimista a prácticamente segura en el de estrés. El 31,2 % del escenario de referencia " +
      "debe entenderse como una medida de vulnerabilidad estructural pasiva frente a la volatilidad " +
      "histórica de los fundamentos, no como una probabilidad que ya incorpore una respuesta correctiva."
  )
);

// ── 6. Lectura de conjunto ─────────────────────────────────────────────────
children.push(H1("6. Lectura de conjunto"));
children.push(
  P(
    "Cinco estrategias de estimación, sobre dos ventanas muestrales que comparten apenas 88 de 108 " +
      "observaciones, convergen en un diagnóstico común. La evidencia de una regla de reacción fiscal " +
      "lineal, estable y de nivel es débil o nula: lo sostienen DOLS de muestra completa (ρ = −0,0071, " +
      "p = 0,564), el VECM en ambas ventanas (velocidad de ajuste fiscal no significativa) y el " +
      "ordenamiento de la descomposición de varianza del SVAR, donde los desbalances primarios y el " +
      "ciclo —no una respuesta sistemática— son lo que mueve la deuda. La evidencia de un umbral de " +
      "fatiga fiscal, en cambio, se fortalece bajo las especificaciones no lineales: el contraste de " +
      "Hansen sobre la primera diferencia del resultado primario rechaza la linealidad con holgura en " +
      "torno a 2.083 puntos básicos, y el TVECM localiza el mismo umbral con una inversión de signo en " +
      "la velocidad de ajuste, aunque sin significar su contraste multivariado."
  )
);
children.push(
  P(
    "Los resultados no se contradicen entre sí. La ausencia de reacción del DOLS es coherente con que el " +
      "VECM tampoco encuentre ajuste por la vía del resultado primario. Los quiebres de Bai-Perron " +
      "—2007T2, 2014T3, 2018T1— coinciden con los episodios de mayor deterioro fiscal, que son también " +
      "los que la descomposición de varianza del SVAR atribuye a shocks primarios. El umbral de Hansen " +
      "en diferencias (2.083 puntos) y el del TVECM (2.081 puntos) coinciden entre sí, y ambos con los " +
      "episodios históricos de ajuste más marcados. Y la probabilidad de insolvencia del 31,2 % es " +
      "consistente con un nivel de deuda cercano al 74 % del PIB y con la dificultad, documentada en la " +
      "serie histórica, de sostener superávits primarios elevados de forma prolongada."
  )
);
children.push(
  P(
    "El aporte del trabajo no es confirmar una tesis previa, sino delimitar con precisión qué permite y " +
      "qué no permite sostener la evidencia argentina 2004–2025: no permite sostener una regla de " +
      "reacción fiscal activa ni un canal causal fuerte entre riesgo soberano y esfuerzo primario; " +
      "permite sostener un umbral de fatiga fiscal de manera parcial y sensible a la especificación; y " +
      "sí permite sostener que la ratio de deuda tiene quiebres estructurales múltiples, que el " +
      "parámetro de reacción es inestable entre subperíodos, y que la probabilidad de superar el 100 % " +
      "del PIB hacia 2035 es un riesgo de cola no despreciable."
  )
);

// ── Referencias ────────────────────────────────────────────────────────────
children.push(H1("Referencias"));
[
  "Alberola, E., Kataryniuk, I., Melguizo, Á. y Orozco, R. (2016). Fiscal policy and the cycle in Latin America: the role of financing conditions and fiscal rules. BIS Working Papers 543.",
  "Bai, J. y Perron, P. (2003). Computation and analysis of multiple structural change models. Journal of Applied Econometrics, 18(1), 1–22.",
  "Blanchard, O. (2019). Public debt and low interest rates. American Economic Review, 109(4), 1197–1229.",
  "Blanchard, O. y Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. Quarterly Journal of Economics, 117(4), 1329–1368.",
  "Bohn, H. (1998). The behavior of U.S. public debt and deficits. Quarterly Journal of Economics, 113(3), 949–963.",
  "Bohn, H. (2007). Are stationarity and cointegration restrictions really necessary for the intertemporal budget constraint? Journal of Monetary Economics, 54(7), 1837–1847.",
  "Cox, J., Ingersoll, J. y Ross, S. (1985). A theory of the term structure of interest rates. Econometrica, 53(2), 385–407.",
  "Daude, C., Melguizo, Á. y Neut, A. (2011). Fiscal policy in Latin America: countercyclical and sustainable? Economics: The Open-Access, Open-Assessment E-Journal, 5, 2011-14.",
  "Elliott, G., Rothenberg, T. y Stock, J. (1996). Efficient tests for an autoregressive unit root. Econometrica, 64(4), 813–836.",
  "Favero, C. y Giavazzi, F. (2007). Debt and the effects of fiscal policy. NBER Working Paper 12822.",
  "Ghosh, A., Kim, J., Mendoza, E., Ostry, J. y Qureshi, M. (2013). Fiscal fatigue, fiscal space and debt sustainability in advanced economies. The Economic Journal, 123(566), F4–F30.",
  "Girouard, N. y André, C. (2005). Measuring cyclically-adjusted budget balances for OECD countries. OECD Economics Department Working Paper 434.",
  "Hansen, B. (1999). Threshold effects in non-dynamic panels: estimation, testing, and inference. Journal of Econometrics, 93(2), 345–368.",
  "Hansen, B. (2000). Sample splitting and threshold estimation. Econometrica, 68(3), 575–603.",
  "Hansen, B. y Seo, B. (2002). Testing for two-regime threshold cointegration in vector error-correction models. Journal of Econometrics, 110(2), 293–318.",
  "Neumeyer, P. y Perri, F. (2005). Business cycles in emerging economies: the role of interest rates. Journal of Monetary Economics, 52(2), 345–380.",
  "Reinhart, C., Rogoff, K. y Savastano, M. (2003). Debt intolerance. Brookings Papers on Economic Activity, 2003(1), 1–74.",
  "Staiger, D. y Stock, J. (1997). Instrumental variables regression with weak instruments. Econometrica, 65(3), 557–586.",
  "Stock, J. y Watson, M. (1993). A simple estimator of cointegrating vectors in higher order integrated systems. Econometrica, 61(4), 783–820.",
  "Zivot, E. y Andrews, D. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. Journal of Business & Economic Statistics, 10(3), 251–270.",
].forEach((r) => children.push(REF(r)));

// ═══════════════════════════ Documento ═════════════════════════════════════

const doc = new Document({
  creator: "Federico Chillón, Santiago Páez, Emiliano Carricondo — FCE UNCUYO",
  title:
    "Deuda Pública Consolidada y Fatiga Fiscal en Argentina (2004–2025) — Nota metodológica",
  description:
    "Nota metodológica del componente econométrico de la tesis: SVAR restringido, umbrales de fatiga fiscal, spread histórico y sostenibilidad estocástica.",
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
  },
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
                  left: convertInchesToTwip(0.35),
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
              children: [
                new TextRun({
                  children: [PageNumber.CURRENT],
                  font: FONT,
                  size: SMALL,
                }),
              ],
            }),
          ],
        }),
      },
      children,
    },
  ],
});

const outPath = path.join(__dirname, "SVAR_Metodologia_Resultados_Accesible.docx");
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log("Documento Word generado en:", outPath, "(" + buffer.length + " bytes)");
});
