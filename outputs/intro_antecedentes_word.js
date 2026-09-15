/**
 * Genera el Word de Introducción + Antecedentes, tesis oficial (director Pablo),
 * con los comentarios de Pablo ya aplicados: sin guiones largos como inciso, sin
 * "narrativa oficial", términos en inglés en cursiva con nota al pie real de Word,
 * dos huecos de cita marcados en corchetes para completar antes de entregar.
 *
 * Formato: Calibri, sin saltos de página, sin tablas ni cajas; es el cuerpo del
 * capítulo, no una nota técnica.
 *
 * Salida: tesis_oficial_borradores/Introduccion_Antecedentes_v2.docx
 */

const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  AlignmentType,
  FootnoteReferenceRun,
  convertInchesToTwip,
} = require("docx");
const fs = require("fs");
const path = require("path");

const FONT = "Calibri";
const BODY = 22;

const H1 = (t) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 300, after: 140 },
    children: [new TextRun({ text: t, bold: true, font: FONT, size: 27 })],
  });

// Construye un párrafo a partir de fragmentos: texto plano, itálica, o nota al pie.
// frag: { t: "texto" } | { t: "texto", i: true } | { fn: N } (referencia a footnote N)
const P = (frags) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 200, line: 300 },
    indent: { firstLine: convertInchesToTwip(0.3) },
    children: frags.map((f) =>
      f.fn
        ? new FootnoteReferenceRun(f.fn)
        : new TextRun({ text: f.t, italics: !!f.i, font: FONT, size: BODY })
    ),
  });

const t = (text) => ({ t: text });
const i = (text) => ({ t: text, i: true });
const fn = (n) => ({ fn: n });

const doc = new Document({
  creator: "Federico Chillón, FCE UNCUYO",
  title: "Introducción y Antecedentes, Tesis (v2, comentarios de Pablo aplicados)",
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  footnotes: {
    1: {
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text:
                "Interrupción abrupta e inesperada del financiamiento externo hacia una economía, " +
                "término acuñado en la literatura de crisis financieras internacionales.",
              font: FONT,
              size: 18,
            }),
          ],
        }),
      ],
    },
    2: {
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text:
                "Representación gráfica de una distribución de probabilidad de trayectorias futuras " +
                "de una variable, mediante bandas de percentiles que se abren como un abanico a " +
                "medida que aumenta el horizonte de proyección.",
              font: FONT,
              size: 18,
            }),
          ],
        }),
      ],
    },
    3: {
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text:
                "Determinante externo al país receptor que impulsa movimientos de capital, en " +
                "contraste con los factores pull, asociados a condiciones domésticas de atracción " +
                "de inversión.",
              font: FONT,
              size: 18,
            }),
          ],
        }),
      ],
    },
    4: {
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text:
                "Modelos estadísticos diseñados para anticipar la probabilidad de una crisis " +
                "mediante indicadores de alerta temprana, sin pretender explicar el mecanismo " +
                "causal subyacente.",
              font: FONT,
              size: 18,
            }),
          ],
        }),
      ],
    },
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
      children: [
        H1("1. Introducción"),

        P([
          t(
            "La historia macroeconómica de América Latina, y en particular de la República " +
              "Argentina, está atravesada por un patrón recurrente de endeudamiento externo, " +
              "vulnerabilidad ante interrupciones repentinas del flujo de capitales ("
          ),
          i("sudden stops"),
          t(")"),
          fn(1),
          t(
            " y crisis de impago soberano [CITA: Reinhart, Rogoff y Savastano (2003), " +
              "Debt Intolerance, verificar]. Desde la declaración de default en 2001 hasta la " +
              "reestructuración del año 2020, la inestabilidad en el acceso al crédito internacional " +
              "ha puesto de manifiesto la extrema fragilidad de una economía condicionada por la " +
              "restricción externa de divisas. En la coyuntura actual, la administración ingresante " +
              "enfrenta una severa encrucijada: la recepción de una abultada herencia de pasivos " +
              "internacionales, la ausencia de crédito voluntario en los mercados financieros " +
              "exteriores y un apretado cronograma de vencimientos en moneda extranjera [DATO: " +
              "Oficina de Presupuesto del Congreso, Operaciones de Deuda Pública, informe mensual " +
              "vigente, completar con la cifra concreta]."
          ),
        ]),

        P([
          t(
            "Este escenario reabre un interrogante decisivo para la estabilidad de mediano plazo: " +
              "¿resultan la consolidación del superávit fiscal primario y la intención explícita de " +
              "pago condición suficiente para garantizar la solvencia intertemporal, o la evidencia " +
              "sobre la intolerancia a la deuda de los países con historial de default sugiere lo " +
              "contrario? La literatura sobre sostenibilidad fiscal muestra que la solvencia de la " +
              "deuda en moneda extranjera no depende únicamente del resultado presupuestario: está " +
              "condicionada por la capacidad de generación de divisas, la evolución del tipo de " +
              "cambio real, la volatilidad del riesgo país (EMBI+) y los límites de absorción " +
              "política que impone el ajuste prolongado."
          ),
        ]),

        P([
          t(
            "El objetivo principal de este trabajo es evaluar la dinámica de la deuda pública " +
              "internacional argentina a partir de sus determinantes macroeconómicos pasados, para " +
              "estimar su sostenibilidad intertemporal en el horizonte post-2025 [CITA: Medeiros " +
              "(2012)]. Específicamente, la investigación busca determinar si la trayectoria fiscal " +
              "y macroeconómica proyectada ofrece un margen de solvencia real para honrar los " +
              "compromisos externos asumidos."
          ),
        ]),

        H1("2. Antecedentes"),

        P([
          t(
            "La literatura empírica sobre sostenibilidad de deuda soberana se desplazó, en la " +
              "última década y media, de las proyecciones determinísticas de un único escenario " +
              "base hacia ejercicios de simulación estocástica capaces de generar distribuciones de " +
              "probabilidad sobre la trayectoria de la deuda. El punto de partida empírico de este " +
              "giro es Medeiros (2012), quien estimó un modelo VAR irrestricto y una función de " +
              "reacción fiscal (FRF) de panel para quince países de la Unión Europea, combinando " +
              "ambos instrumentos para simular miles de trayectorias de deuda/PBI y construir los " +
              "primeros "
          ),
          i("fan charts"),
          fn(2),
          t(
            " de uso sistemático en un organismo oficial (la Comisión Europea). Su hallazgo más " +
              'citado es que el balance primario exhibe "fatiga fiscal": la reacción del superávit ' +
              "ante el aumento de la deuda se debilita y eventualmente se revierte por encima de " +
              "cierto umbral. Ese hallazgo fue incorporado después como supuesto de comportamiento " +
              "en marcos de sostenibilidad de organismos multilaterales, entre ellos el Marco de " +
              "Riesgo Soberano y Sostenibilidad de la Deuda del FMI (SRDSF), aplicado a Argentina en " +
              "su Octava Revisión del Servicio Ampliado (FMI, 2024)."
          ),
        ]),

        P([
          t(
            'Esa misma "fatiga fiscal" fue puesta en discusión por Everaert y Jansen (2018), ' +
              "quienes retomaron el panel de países de la OCDE (1970-2014) que sirve de base a buena " +
              "parte de esta literatura y testearon si el patrón no lineal de Medeiros (2012) era " +
              "una regularidad de comportamiento genuina o un artefacto de agregar países " +
              "heterogéneos en un único panel. Usando el estimador Mean Group de Pesaran y Smith, " +
              "que permite una pendiente de reacción fiscal distinta para cada país en lugar de " +
              "imponer un coeficiente común, encontraron heterogeneidad significativa: la fatiga " +
              "fiscal no es una característica compartida por todos los países del panel, sino el " +
              "promedio estadístico de comportamientos fiscales muy distintos entre sí. La " +
              "implicancia directa para cualquier ejercicio de simulación aplicado a un país " +
              "individual, y en particular a Argentina, es que la FRF panel estimada sobre economías " +
              "avanzadas o de la Unión Europea no es transferible sin más: la propia arquitectura del " +
              "marco FMI aplicado a Argentina hereda parámetros de comportamiento fiscal calibrados " +
              "sobre un grupo de países con marcos de disciplina institucional (Pacto de Estabilidad, " +
              "vigilancia de la Comisión Europea) ausentes en el caso argentino."
          ),
        ]),

        P([
          t(
            "Un segundo cuerpo de literatura empírica trasladó el problema de sostenibilidad a " +
              "economías emergentes expuestas a shocks externos de términos de intercambio y a " +
              "interrupciones súbitas del financiamiento. Adler y Sosa (2014), dentro del volumen " +
              "editado por el FMI sobre América Latina, estimaron modelos VAR globales (GVAR) y de " +
              "panel (PVAR) para un conjunto de países de la región, introduciendo como variable " +
              "exógena internacional el Índice de Precios Netos de Materias Primas (NCPI) " +
              "desarrollado por Adler y Magud (2014), que pondera cada commodity por la posición " +
              "neta exportadora o importadora del país. El resultado empírico central de ese " +
              "ejercicio, que más de la mitad de la variabilidad de las entradas de capital de corto " +
              "plazo a economías como la argentina responde a condiciones internacionales (tasa de " +
              "la Reserva Federal, índice VIX) y no a variables de atracción local, reforzó la idea " +
              "de que la sostenibilidad de la deuda en la región depende en gran medida de factores "
          ),
          i("push"),
          fn(3),
          t(
            " ajenos a la política doméstica. El mismo estudio documentó, sin embargo, una " +
              "asimetría específica de Argentina: mientras que en economías desarrolladas los " +
              "residentes repatrían activos externos para amortiguar una crisis, en el caso " +
              "argentino el capital residente tiende a sumarse a la salida, amplificando en lugar de " +
              "atenuar la inestabilidad financiera."
          ),
        ]),

        P([
          t("En paralelo, la literatura de sistemas de alerta temprana ("),
          i("early warning systems"),
          t(")"),
          fn(4),
          t(
            " buscó anticipar crisis de deuda soberana con una estrategia metodológica distinta: no " +
              "explicar mecanismos, sino maximizar poder predictivo. Wijayanti y Rachmanira (2020) " +
              "aplicaron el ratio de ruido a señal de Kaminsky, Lizondo y Reinhart y una regresión " +
              "logística binomial sobre un panel de 43 países en desarrollo entre 1960 y 2017, " +
              "logrando predecir el 61,5% de las crisis de deuda con dos años de anticipación bajo " +
              "un umbral de probabilidad del 30%. El resultado, moderado pero no trivial, expone una " +
              "tensión metodológica relevante para cualquier antecedente que se apoye en el marco del " +
              "FMI: los sistemas de alerta temprana están diseñados para maximizar poder predictivo " +
              "agregado sobre un panel amplio de países, mientras que el "
          ),
          i("fanchart"),
          t(
            " estocástico del SRDSF busca representar la distribución de riesgo de un país " +
              "específico; ambos abordajes pueden, y de hecho suelen, dar señales distintas frente a " +
              "un mismo episodio."
          ),
        ]),

        P([
          t(
            "Dentro de la literatura específicamente centrada en Argentina, dos trabajos " +
              "independientes, con instrumentos metodológicos casi opuestos, llegaron a diagnósticos " +
              "convergentes en la antesala de la crisis de 2001-2002. Cetrángolo, Damill, Frenkel y " +
              "Jiménez (1997) reconstruyeron el esquema ahorro-inversión del Sector Público Nacional " +
              "no Financiero para 1975-1996, desagregaron el presupuesto en ocho rubros de ingresos " +
              "y siete de gasto, vincularon cada uno a su variable macroeconómica relevante mediante " +
              "coeficientes fijos, y aplicaron el filtro de Hodrick-Prescott para separar tendencia " +
              "de ciclo y así calcular un déficit macroeconómicamente ajustado (DMA) y un impulso " +
              "fiscal (siguiendo la metodología de Blanchard, 1990). Su conclusión fiscal fue " +
              "tranquilizadora: el riesgo fiscal cíclico bajo Convertibilidad era pequeño (0,3-0,6% " +
              "del PBI), muy inferior a la volatilidad de los años setenta y ochenta, y la mejora de " +
              "recaudación 1991-96 era mayoritariamente estructural, no un artefacto del boom " +
              "económico. Sin embargo, el propio documento advirtió, en su escenario central de " +
              "proyección para 1997-2001, que el desequilibrio de cuenta corriente externa crecía " +
              "hasta superar el 7% del PBI hacia 2001, anticipando, desde una lente estrictamente " +
              "fiscal, que el verdadero riesgo no era fiscal sino de sostenibilidad externa."
          ),
        ]),

        P([
          t(
            "Calvo, Izquierdo y Talvi (2003), que trabajaron con un instrumental completamente " +
              "distinto (contabilidad de balanza de pagos, calibración de elasticidades de demanda " +
              "de no transables y la identidad estándar de dinámica de deuda), llegaron a la misma " +
              "advertencia por otra vía. Su marco “CDM” (economía cerrada, dolarizada y con " +
              "descalce de balances) mostró que, ante un "
          ),
          i("sudden stop"),
          t(
            " como el desatado por la crisis rusa de 1998, la magnitud del ajuste de tipo de cambio " +
              "real necesario para restablecer el equilibrio externo dependía críticamente de la " +
              "apertura comercial y del descalce de moneda de los pasivos, dos rasgos en los que " +
              "Argentina se ubicaba en el peor extremo posible entre los casos comparados " +
              "(Argentina, Brasil, Chile, Colombia, Ecuador). El diálogo entre ambos trabajos es " +
              "directo: uno detecta el problema por el lado del flujo (cuenta corriente), el otro " +
              "por el lado del stock (descalce patrimonial), y ambos, escritos antes o " +
              "inmediatamente después del default, coinciden en que el diagnóstico fiscal de corto " +
              "plazo no bastaba para juzgar la sostenibilidad."
          ),
        ]),

        P([
          t(
            "Dos décadas después, la literatura sobre Argentina se dividió en torno a un problema " +
              "metodológico específico: si el ratio Deuda/PBI es o no una medida confiable de riesgo " +
              "cuando media un salto cambiario abrupto. Rodríguez (2023) revisó el financiamiento y " +
              "la sostenibilidad de la deuda pública argentina entre 2001 y 2022 y mostró que la " +
              "abrupta caída del ratio Deuda/PBI durante 2003-2011 no reflejó un desendeudamiento " +
              "estructural, sino un efecto contable de apreciación del tipo de cambio real (el PBI " +
              "medido en dólares creció más rápido que el stock de deuda). El mismo mecanismo, en " +
              "sentido inverso, explica por qué el salto cambiario de fines de 2023 llevó " +
              "mecánicamente el ratio al 156,7% del PBI y disparó, dentro del SRDSF del FMI, una " +
              'alarma roja de "Riesgo Alto" (ancho de '
          ),
          i("fanchart"),
          t(
            " de 122,7 puntos) que el propio staff del organismo debió matizar cualitativamente por " +
              "no reflejar el riesgo real de mediano plazo (FMI, 2024). La controversia queda así " +
              "planteada de manera explícita entre dos antecedentes: un marco de benchmarking " +
              "estadístico mecánico (percentiles históricos, umbrales fijos) y una lectura " +
              "estructural que atribuye buena parte del movimiento del indicador a un efecto de " +
              "valuación antes que a un cambio genuino de solvencia."
          ),
        ]),

        P([
          t(
            "Levy Yeyati y Sturzenegger (2021, publicado en 2023) llevaron esta discusión un paso " +
              "más allá al proponer reemplazar el ratio Deuda/PBI por el patrimonio neto del sector " +
              "público (valor presente de impuestos menos valor presente de gastos y pasivos " +
              "explícitos), simulado mediante bootstrap de un VAR de tres variables (PBI, tipo de " +
              "cambio real, tasa internacional). Aplicado a Argentina, el ejercicio arrojó un " +
              "patrimonio neto medio de 2,2 veces el PBI sin territorio negativo en la distribución " +
              "simulada, y un hallazgo llamativo: una devaluación real del 20% apenas mueve ese " +
              "patrimonio neto (de 2,225 a 2,214 del PBI), porque el mayor costo en dólares de la " +
              "deuda se compensa con más recaudación de rubros transables y la licuación de gastos " +
              "en pesos. Este resultado entra en tensión directa con el cálculo tradicional que los " +
              "propios autores citan de Calvo et al. (2003): bajo el enfoque clásico de descalce de " +
              "moneda, una devaluación del 50% eleva el ratio Deuda/PBI argentino de 36,5% a 50,8%. " +
              "Dos antecedentes centrados en el mismo país y el mismo tipo de shock, una devaluación " +
              "real, llegan a conclusiones opuestas sobre su severidad fiscal según si el " +
              "instrumento utilizado es el ratio de deuda o el balance patrimonial completo. Los " +
              "propios autores advierten, no obstante, que su resultado benigno depende de que " +
              "Argentina, tras 2001, redujo fuertemente la dolarización de su deuda pública, y que " +
              "el mismo ejercicio aplicado a la estructura de deuda de 2001 habría arrojado un " +
              "deterioro fiscal severo ante el mismo shock."
          ),
        ]),

        P([
          t(
            "Un último antecedente relevante no discute la sostenibilidad ex ante, sino el costo ex " +
              "post del evento que estos marcos buscan evitar. Hébert y Schreger (2017) explotaron el " +
              "litigio República Argentina v. NML Capital como un experimento natural: los fallos " +
              "judiciales sucesivos alteraron exógenamente la probabilidad de default percibida por " +
              "el mercado, sin depender de las noticias económicas del día. Mediante identificación " +
              "por heterocedasticidad (Rigobon y Rigobon-Sack), estimaron que un aumento del 10% en " +
              "la probabilidad de default (medida por CDS) provocó una caída del 6% en el índice " +
              "ponderado de acciones argentinas, y que el paso de 40% a 100% de probabilidad de " +
              "default, lo efectivamente observado, implicó una destrucción de valor de mercado de " +
              "las firmas cotizantes de entre 30% y 45%, concentrada en exportadoras y filiales de " +
              "multinacionales. Este antecedente complementa, desde el lado de las consecuencias " +
              "reales, a la literatura de sostenibilidad ex ante revisada arriba: cuantifica el " +
              "costo del evento de cola que los marcos estocásticos (Medeiros, 2012; FMI, 2024) " +
              "intentan mantener con baja probabilidad, y que los enfoques de balance completo (Levy " +
              "Yeyati y Sturzenegger, 2021) sugieren que, bajo la estructura de deuda actual, sería " +
              "menos probable que en 2001."
          ),
        ]),
      ],
    },
  ],
});

const outPath = path.join(
  __dirname,
  "..",
  "tesis_oficial_borradores",
  "Introduccion_Antecedentes_v2.docx"
);
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log("Documento generado:", outPath, "(" + buffer.length + " bytes)");
});
