Octava Revisión del Servicio Ampliado del Fondo (EFF) para Argentina (IMF Country Report No. 24/167).

Marco de Riesgo Soberano y Sostenibilidad de la Deuda (SRDSF): 

Estructura el análisis de riesgos en tres horizontes bien definidos:

Corto Plazo (1 a 2 años): Evaluado mediante un modelo estadístico multivariado (logit) que calcula la probabilidad de estrés soberano inminente basándose en datos actuales.

Mediano Plazo (hasta 5 años): Utiliza tres módulos integrados: un gráfico de abanico (fanchart) para medir la probabilidad de estabilización, un módulo de financiabilidad de GFN para evaluar riesgos de refinanciación según los acreedores, y pruebas de estrés activadas por factores específicos (como desastres naturales o shocks de commodities).

Largo Plazo (más de 5 años): Incorpora herramientas opcionales para evaluar presiones lentas pero profundas, como el envejecimiento de la población, el cambio climático y amortizaciones futuras concentradas.

Construcción del Escenario Base Macroeconómico

Balance primario (déficit/superávit sin intereses) 

Diferencial tasa de interés real – crecimiento (r–g), separado en tasa y crecimiento reales del PBI 

Efecto del tipo de cambio real (relevante en Argentina por la dolarización de la deuda) 

Ajustes de flujo-stock (SFA) y un residual

Test de realismo de los supuestos: FMI diseñado para auditar si las proyecciones macroeconómicas y fiscales de un programa son técnicamente viables o si sufren del "sesgo de optimismo del programador"

el FMI no evalúa el escenario base en el vacío, sino contra su propio historial de pronósticos y contra un grupo de comparación (economías emergentes exportadoras de commodities con programa del FMI). Concretamente:

Forecast track record: compara errores de pronóstico pasados del staff (deuda/PBI, balance primario, r–g, depreciación) a horizontes t+1, t+3, t+5, ubicándolos en percentiles de la distribución histórica de errores de todos los países del grupo comparador.

Percentil de ajuste fiscal a 3 años: la consolidación fiscal proyectada (en Argentina, un ajuste muy grande) se ubica en el percentil de la distribución histórica de ajustes fiscales de 1990–2019 en economías avanzadas y emergentes bajo programa. En este informe, el ajuste de 3 años cae en el percentil 91, marcado como optimista. 

Reducción de deuda a 3 años: mismo ejercicio — la reducción proyectada de deuda cae en el percentil 100, la más optimista posible. 

Multiplicadores fiscales: se simulan trayectorias de crecimiento con distintos multiplicadores (0.5, 1, 1.5) para chequear consistencia entre el ajuste fiscal supuesto y el crecimiento proyectado.

Esto es esencialmente benchmarking estadístico no paramétrico (percentiles empíricos) contra una base de datos panel de países. Se ubica el error del país en la distribución histórica global del grupo comparador23:

Verde: Pronóstico conservador o pesimista (<25 percentil).

Amarillo / Naranja: Pronóstico dentro del rango medio intermedio (25-75 percentil).

Rojo: Pronóstico marcadamente optimista (>75 percentil).

La regla de política fiscal (Función de Reacción Fiscal - FRF)

Módulo de riesgo de mediano plazo

 Se toma la ecuación de dinámica de deuda y se le aplican shocks estocásticos a sus componentes (crecimiento, tasa de interés, tipo de cambio, balance primario), calibrados con la volatilidad histórica de cada variable para ese país (o un panel si no hay suficiente historia). Simulación Estocástica de Deuda (DSA). Estimación del Modelo de Vectores Autorregresivos (VAR), para capturar la volatilidad histórica y las interdependencias cruzadas entre las variables macroeconómicas, se estima un modelo VAR no restringido con datos históricos del país



Se corren miles de trayectorias simuladas de deuda/PBI a 5 años, generando una distribución de probabilidad (el "abanico" o fanchart) con bandas de percentiles 5-25, 25-50, 50-75, 75-95, colas menos esperados, a más esperados.



Enfoque Paramétrico (Monte Carlo bajo Normalidad): Se asume que los errores del VAR siguen una distribución normal multivariada y se generan números aleatorios a través de una descomposición de Cholesky de la matriz de covarianza.

Enfoque No Paramétrico (Bootstrapping / Remuestreo): Se realizan extracciones aleatorias con reemplazo directamente sobre los residuos reales históricos estimados por el VAR (sea individuales o por bloques de dos años). Este método es preferido cuando los datos muestran colas pesadas o asimetría, evitando imponer el supuesto de normalidad.

Paso 1: Extracción de Residuos Históricos: Se calculan las desviaciones o desviaciones empíricas entre las variables macroeconómicas reales (crecimiento del PBI, tasa de interés, tipo de cambio y balance primario) y sus proyecciones históricas pasadas.

Paso 2: Remuestreo Aleatorio (Bootstrapping): En lugar de utilizar un generador de ecuaciones con distribuciones gaussianas, la simulación extrae aleatoriamente (con reemplazo) combinaciones reales de shocks observados en la historia del país o de un panel de países comparables. 

Paso 3: Preservación de la Co-dependencia: Al tomar vectores de shocks ocurridos simultáneamente en el pasado, se respeta la correlación empírica intrínseca entre las variables (por ejemplo, cómo cayó el PBI en el mismo trimestre en que ocurrió un salto cambiario) sin necesidad de estimar una matriz de covarianza rígida.

Paso 4: Captura de Colas Pesadas (Fat Tails): Permite incorporar eventos extremos y shocks asimétricos observados en la realidad —como colapsos financieros o crisis cambiarias— que las distribuciones paramétricas convencionales suelen suavizar o subestimar. 

Ancho del Abanico (Fanchart Width): Se mide como la distancia entre el percentil 95 y el percentil 5 en el año 5 (). Un abanico muy ancho refleja alta vulnerabilidad a shocks externos o volatilidad macroeconómica.

Probabilidad de No Estabilización: Proporción de simulaciones donde la deuda/PBI al año 5 termina en un nivel superior al año inicial (). Si este porcentaje es elevado, el FMI señala una señal de alerta (high risk) sobre la sostenibilidad de la deuda.

Shocks sesgados (Skewed Shocks) para corregir el optimismo: Si el examen de realismo detecta que las proyecciones del gobierno son demasiado optimistas (por ejemplo, asumiendo un crecimiento mágico sin reformas), la herramienta de fanchart aplica shocks sesgados de forma asimétrica hacia la derecha. Esto significa que, estadísticamente, el modelo aplica de forma deliberada más shocks negativos (devaluaciones, subas de tasas o caídas del PIB) para forzar al abanico a mostrar el verdadero riesgo de que la deuda se dispare.



 De ahí salen tres estadísticos (Tabla 6): 

Ancho del fanchart (122.7 puntos de PBI en Argentina — muy alto, reflejo de la devaluación de diciembre 2023)

Probabilidad de que la deuda no se estabilice (5.06%)

Nivel terminal de deuda ponderado por un índice institucional: Se obtiene la proyección estocástica o el valor mediano del ratio Deuda Pública/PIB para el quinto año del horizonte simulado ($t+5$) a partir del modelo fanchart. 

Cálculo del Índice de Calidad Institucional (WGI): Se extrae de la base de datos de los Worldwide Governance Indicators (WGI) del Banco Mundial, calculando el promedio simple de dos indicadores estructurales:

Efectividad del Gobierno (Government Effectiveness).

Calidad Regulatoria (Regulatory Quality).



Escalamiento Inverso (Rescaling)

Para poder interactuar de forma matemática con el nivel de deuda, el índice obtenido se escala de la siguiente manera:

0 corresponde a la máxima calidad institucional (menor riesgo).

1 corresponde a la mínima calidad institucional (mayor riesgo).

el valor del índice se mantiene fijo o congelado en su último nivel histórico observado

Módulo GFN Financeability (necesidades brutas de financiamiento)

Chequea si el país puede efectivamente colocar la deuda que necesita rollear, no solo si el nivel de deuda es sostenible en el papel:

GFN promedio del baseline (8.9% del PBI) bajo un escenario de estrés que combina shocks de tasa, tipo de cambio y crecimiento simultáneamente (no solo separados). Utiliza elasticidades mecánicas fijas (ej. por cada  que cae el commodity, la recaudación cae  y el PBI ).

Exposición bancaria al gobierno (bank claims on government, 15% de activos bancarios) y su cambio bajo estrés (22.7 puntos), para capturar el riesgo de que el sistema financiero doméstico no pueda absorber más emisión en un escenario adverso.

¿Cómo funciona la dinámica de estrés en el modelo GFN?

El modelo del FMI simula un canal de transmisión estocástico y de comportamiento de mercado (holder shock):

Mecanismo de choque de tenedores (Holder Shock): En un escenario de turbulencia o recesión, los inversores extranjeros o acreedores privados imponen un recorte en la renovación de la deuda (rollover), negándose a comprar nuevos títulos públicos o exigiendo la cancelación de amortizaciones. DSA

El banco como amortiguador residual: Ante la fuga o retiro de los acreedores privados, la primera línea de defensa del Estado son sus colchones de liquidez financiera. Si estos no alcanzan, el modelo asume que el déficit sobrante debe ser absorbido obligatoriamente por el sistema bancario comercial local.

El límite empírico de saturación bancaria: La evidencia histórica internacional analizada por el FMI muestra que el crédito bancario al sector público rara vez supera el 20% de los activos totales de la banca en situaciones normales. Cuando un banco ya tiene un porcentaje elevado de bonos soberanos en sus balances, su disposición y margen normativo para seguir comprando deuda pública decae fuertemente.

Estos tres indicadores también se normalizan y combinan en un índice GFN (15.5), comparado contra umbrales (bajo: <7.6; alto: >17.9) — en Argentina cae en zona "Moderate".

Combinación en el Índice de Mediano Plazo (MTI)

El índice de fanchart y el índice GFN se normalizan (0-100) y se promedian con ponderadores fijos (0.5 y 0.5 en este caso, según Tabla 6) para producir un Medium-Term Index (MTI) único, que a su vez se compara contra umbrales (bajo <0.3; alto >0.4). El MTI de Argentina resultó en zona de riesgo alto

Riesgo de largo plazo — Fanchart a 10 años

Se repite la lógica de Monte Carlo del punto 4 pero extendiendo el horizonte a 2033. En Argentina, la probabilidad de estabilización de deuda a 10 años da 86%, insumo separado del índice de mediano plazo.

IMF (2014). Latin America: New Challenges to Growth and Stability

Función de Producción Cobb-Douglas y Filtros de Tendencia

Paso 1 (Construcción de insumos): Se estimó el stock de capital () mediante el método de inventarios perpetuos con tasa de depreciación , el insumo trabajo () utilizando la fuerza laboral efectivamente empleada y el capital humano () derivado de los años de escolaridad de la base Barro-Lee. 

¿Para qué se usa? Se utiliza para la contabilidad del crecimiento (Growth Accounting) desde el lado de la oferta. Permite descomponer el crecimiento del PIB en las contribuciones de los factores productivos (capital y trabajo) y la Productividad Total de los Factores (PTF). También sirve para estimar el PIB potencial y calcular la brecha del producto (output gap).

Paso 2 (Estimación de la PTF): Se descompuso el producto mediante la ecuación , identificando la Productividad Total de los Factores () como el residuo de Solow.

Paso 3 (Filtrado del PIB potencial): Se aplicaron filtros estadísticos (Hodrick-Prescott con  y , Baxter-King y Christiano-Fitzgerald) a las subseries hasta 2017 para suavizar las fluctuaciones cíclicas y proyectar el producto potencial.

El filtro HP se utilizó para extraer el componente cíclico de las series macroeconómicas y de flujos (como el PIB o el volumen de capitales), separándolos de su tendencia de largo plazo:



Donde  es la serie observada,  es la tendencia,  es el componente cíclico y  es el parámetro de suavización ( para datos trimestrales). Su objetivo es garantizar la estacionariedad de las series para la estimación del VAR y aislar la brecha del producto (output gap).

Modelos Econométricos Dinámicos (GVAR, Panel VAR y VECM)

Paso 1 (Construcción de métricas de shocks): Se diseñó un Índice de Precios Netos de Materias Primas (NCPI) específico por país y una métrica de ganancia extraordinaria (windfall) que pondera los términos de intercambio por la apertura comercial ().

NCPI (Net Commodity Price Index / Índice de Precios Netos de Materias Primas)

¿Qué es? Es un índice estadístico (desarrollado por el FMI y la literatura macroeconómica) diseñado para medir el efecto neto que tienen las variaciones de los precios internacionales de las materias primas sobre el ingreso real de un país determinado.

Diferencia clave: A diferencia de los índices tradicionales centrados únicamente en las exportaciones, el NCPI utiliza ponderaciones basadas en las exportaciones netas () de cada commodity.

Si un país es exportador neto de un bien (ej. soja o maíz), un incremento en su precio internacional representa un shock de ingreso positivo.

Si el país es importador neto (ej. petróleo o gas), un alza de precio actúa como un shock negativo.

¿Cómo se usó en el modelo? Se introdujo como variable exógena internacional dentro de la estructura del SVAR, GVAR y PVAR. Permitió aislar las fluctuaciones internacionales de precios de las respuestas internas de producción, evaluando con precisión la magnitud del choque externo que enfrenta la economía.

Para estimar la evolución futura de las materias primas y proyectar el NCPI (Índice de Precios Netos de Materias Primas), se combinaron precios de contratos de futuros financieros de mercado con pronósticos macroeconómicos globales del FMI (WEO) integrados mediante proyecciones condicionadas.

Curva de Precios de Futuros Financieros

Fuentes de mercado: Se extrajeron las cotizaciones de los contratos de futuros a mediano plazo (de 1 a 5 años) en las principales bolsas internacionales (como el Chicago Board of Trade o NYMEX) para cada commodity individual (soja, maíz, petróleo, cobre, etc.).

Expectativa de mercado: Se utilizó la curva de futuros como una estimación no sesgada (unbiased expectation) de los precios spot (contado) que el mercado financiero anticipa para los siguientes años.

Pronóstico Condicionado en el Modelo Econométrico (Conditional Forecasting)

En los modelos GVAR y SVAR, los precios de las materias primas no se dejaron evolucionar libremente según la memoria del modelo, sino que se fijó su trayectoria exógenamente mediante la técnica de pronóstico condicionado.

Se corrieron simulaciones bajo dos escenarios contrafácticos principales:

Escenario de Futuros: Se evaluó el impacto en la economía asumiendo que el NCPI seguía exactamente la curva descendente/ascendente que predecían los mercados de futuros.

Escenario de Precios Constantes: Se simuló un escenario donde el NCPI se congelaba en el nivel alcanzado al final del periodo del boom, lo que permitió aislar cuánto del ajuste económico futuro respondería exclusivamente a la caída esperada de precios.

PVAR: Agrupa el panel de países emergentes para estimar coeficientes promedio de la región, controlando por efectos fijos no observados ().

 GVAR: Estima modelos VARX* individuales por país y los conecta mediante matrices de peso  (basadas en comercio o flujos financieros) para capturar la transmisión indirecta de shocks globales entre países.

GVAR para un solo país (Aptitud: Focalizada dentro de una red)

No se puede construir un "GVAR de un solo país" de forma aislada porque la "G" representa Global. Sin embargo, sí se usa para estudiar a Argentina insertándola como un nodo específico dentro de una matriz multipaís.

Métrica de Windfall (Ganancia o Renta Extraordinaria)

¿Qué es? Es un indicador cuantitativo que mide la cuantía del "viento a favor" o la renta imprevista que recibe una economía durante un ciclo de bonanza en los mercados internacionales.

¿Cómo se calcula? Se obtiene acumulando o calculando la desviación de las variaciones del NCPI respecto a su promedio histórico, escalado por la apertura comercial de materias primas sobre el tamaño de la economía (). Expresa numéricamente cuántos puntos porcentuales del PIB adicional ingresaron a la economía exclusivamente por el choque exógeno de precios.

¿Cómo se usó en la investigación?

Evaluación del ahorro macroeconómico: Determinó si los países aprovecharon la bonanza para acumular reservas internacionales y fortalecer sus balances, o si el ingreso extraordinario financió gasto corriente o salida de capitales.

Transmisión a los flujos brutos de capital: Dentro del marco SVAR/PVAR, se utilizó para simular cómo reaccionan las entradas extranjeras y la repatriación/fuga de residentes ante un choque equivalente a un windfall de cierto porcentaje del PIB. Esto permitió confirmar si las bonanzas atenuaron o exacerbaron la volatilidad financiera local.

Construcción del NCPI y del Windfall

Selección y variación de precios (): Se toma la evolución de los precios internacionales de los bienes primarios clave (agrícolas, energéticos y minerales).

Ponderación por exportaciones netas (): Para cada país  y producto , se calcula el peso asignado según el saldo neto ():



Un peso positivo indica que el país es exportador neto del bien ; un peso negativo indica que es importador neto.

 Construcción del NCPI:



  Métrica de Windfall (Ganancia Extraordinaria): Pondera la variación de precios por el peso de las exportaciones netas sobre el Producto Interno Bruto (), incorporando explícitamente la apertura comercial ():



  Paso 2 (Modelado de transmisión dinámico): Se utilizaron Vectores Autorregresivos Globales (GVAR) y de Panel (PVAR) para simular la transmisión de shocks externos (política monetaria de EE. UU., desaceleración de China y volatilidad del VIX) sobre el producto y las variables financieras locales.

  Paso 3 (Descomposición de flujos brutos): Mediante VAR estructurales (SVAR), se desagregaron los flujos de capital en entradas de no residentes y repatriación de activos de residentes.

Para transformar los residuos correlacionados del modelo reducido () en shocks estructurales puros e independientes (), se aplica  imponiendo restricciones:

Cholesky / Ordenamiento Causal: Se asume que las variables internacionales afectan instantáneamente a las locales, pero las decisiones de Argentina no afectan instantáneamente al VIX o a la Fed.

Restricciones de Signo: Se restringe la matriz  para que un shock de aversión al riesgo imponga teóricamente un impacto no positivo sobre los ingresos extranjeros.

Son los dos componentes fundamentales de los flujos brutos de capital dentro de la Balanza de Pagos, permitiendo diferenciar si las variaciones de dinero en una economía provienen de decisiones de inversionistas extranjeros o de actores locales.

¿Qué es cada concepto?

Entradas de no residentes (Incurrencia Neta de Pasivos): Mide el capital internacional que ingresa o sale según las decisiones de extranjeros. Incluye la compra de bonos o acciones locales, la Inversión Extranjera Directa (IED) y préstamos otorgados por bancos internacionales a entidades locales.

Salida o Repatriación de residentes (Adquisición Neta de Activos): Mide el comportamiento del capital de los ciudadanos y empresas locales en el exterior:

Salida (Salida de Capitales / Fuga): Residentes adquiriendo activos en el extranjero (comprar dólares para atesoramiento, abrir cuentas bancarias fuera del país o comprar inmuebles en el exterior).

Repatriación (Retrenchment): Residentes liquidando sus activos afuera para traer ese capital de regreso a la economía doméstica.

¿Cómo se mide?

Se registra en la Cuenta Financiera de la Balanza de Pagos bajo las normas del Manual de Balanza de Pagos del FMI (BPM6):

Flujo Extranjero (Inflows): Cambios en los pasivos financieros del país con el exterior (). Un número positivo indica que los extranjeros compraron más activos locales de los que vendieron.

Flujo Residente (Outflows): Cambios en los activos financieros del país en el exterior (). Un número positivo representa adquisición neta de activos externos (salida/fuga); un número negativo indica venta o repatriación.

Fuente de datos: En Argentina, además del reporte trimestral del INDEC, el Banco Central (BCRA) los mide a alta frecuencia mediante el Balance Cambiario (MULC), que registra las liquidaciones efectivas de divisas en el mercado oficial.

¿Cómo se estima en los modelos econométricos?

En los modelos macroeconómicos (como los SVAR y PVAR utilizados en las investigaciones):

Diferenciación de series: Se desacopla la serie del Flujo Neto (Entradas - Salidas) para construir dos series independientes de frecuencia mensual o trimestral en términos reales (o desestacionalizadas vía filtro HP).

Modelación de causales (Shock Push vs. Pull): Se estima la respuesta de cada flujo por separado asignándoles vectores de control. Por ejemplo, las entradas extranjeras se modelan en respuesta a la aversión al riesgo global (VIX), mientras que la salida de residentes suele reaccionar con mayor fuerza a choques de incertidumbre política doméstica o brecha cambiaria.

¿Para qué sirve analizarlos por separado?

Diagnóstico preciso de las crisis (Sudden Stop vs. Capital Flight): Permite saber quién provoca la escasez de divisas. Un desplome en las reservas puede deberse a que los extranjeros dejaron de prestar (Sudden Stop) o a que los locales están cambiando sus ahorros masivamente a dólares (Fuga de capitales).

Evaluar mecanismos de amortiguación: En economías desarrolladas, cuando ocurre una crisis externa, los residentes suelen repatriar capital para aprovechar activos locales baratos (actúan como "amortiguador"). En Argentina, el modelo SVAR permite probar si el residente actúa como amortiguador o si, por el contrario, amplifica la crisis aumentando la salida de fondos.

Diseño de política económica: Guía al Banco Central para saber dónde aplicar regulaciones: si la presión proviene del sector exterior, se requieren medidas de liquidez internacional o líneas swap; si proviene de residentes, suelen aplicarse incentivos de tasa de interés local o controles cambiarios.



Modelos de Sostenibilidad de Deuda y Prociclicidad Fiscal

Paso 1: Se vincularon variables internacionales con los determinantes de la deuda (tipo de cambio real, prima de riesgo, tasa de interés y balance primario).

Simulaciones e Inferencia Dinámica

Funciones de Impulso-Respuesta (IRF): Se simula un "shock" exógeno equivalente a un desvío estándar () en una variable externa y se gráfica la trayectoria de respuesta de las entradas y salidas de capital a lo largo de  periodos futuros.

Simulaciones Bootstrap (Monte Carlo): Se corren entre 1.000 y 5.000 repeticiones estocásticas para construir intervalos de confianza (bandas del 90% o 95%) alrededor de la trayectoria de las IRF.

Descomposición de Varianza (FEVD): Cuantifica qué porcentaje exacto de la fluctuación de las entradas y salidas de capital en Argentina es atribuible a shocks internacionales versus choques domésticos.

En un modelo VARX o SVARX, los shocks exógenos observables (como el VIX, la tasa de la Fed o el NCPI) no forman parte del vector endógeno, sino que actúan como regresores determinísticos o de control externo.

Estructura Matricial:

Se define el sistema matricial para cada periodo :



Donde  es un vector de  variables exógenas contemporáneas (y opcionalmente sus rezagos ), y  es una matriz de dimensiones  de coeficientes de impacto directo.

Supuesto de Exogeneidad Estricta (Bloque-Exogeneidad):

Se asume formalmente que  para todo . Esto matemáticamente implica una transmisión unidireccional: las variaciones en  alteran inmediatamente a , pero ninguna innovación  derivada del sistema local (ej. Argentina) puede retroalimentar o modificar a .

Cálculo de los Multiplicadores Dinámicos:

Para simular el impacto de un choque exógeno puro en , se reescribe el modelo en su representación de Media Móvil ():



Las matrices de multiplicadores  miden la respuesta marginal acumulada de las variables endógenas (flujos de capital) en el periodo  ante un incremento unitario del shock exógeno en el periodo .

Descomposición Triangulada de Cholesky Paso a Paso

Los residuos estimados por Mínimos Cuadrados Ordinarios (MCO), , están correlacionados contemporáneamente (). Cholesky es un método algebraico para transformar  en shocks estructurales ortogonales e independientes (), donde .

1. Estimación del VAR Reducido

Se obtienen los residuos  y se calcula la matriz de varianzas y covarianzas muestral  (matriz simétrica y definida positiva de tamaño ).

2. Factorización Matricial

Por el teorema de Cholesky, cualquier matriz simétrica y definida positiva  se descompones de forma única en el producto de una matriz triangular inferior  y su transpuesta :



3. Sistema de Ecuaciones Cortada (Relación Contemporánea)

La relación  para un sistema de 3 variables se visualiza así:

Variable 1 (): Reacciona contemporáneamente solo a su propio shock estructural  ().

Variable 2 (): Reacciona a  y a su propio shock  ().

Variable 3 (): Reacciona instantáneamente a todos los shocks estructurales del sistema.

Este ordenamiento impone exactamente  restricciones de ceros en la matriz , que es el número justo para lograr la identificación exacta del modelo SVAR.

4. Extracción de los Shocks Estructurales

Para obtener los shocks ortogonalizados que se graficarán en las IRF, se despeja:



Paso 2: Se ejecutaron pruebas de estrés simulando escenarios macroeconómicos adversos para proyectar trayectorias de deuda pública y externa.

DSA (Análisis de Sostenibilidad de la Deuda / Debt Sustainability Analysis) estocástico o bajo estrés, mientras que la FRF (Función de Reacción Fiscal) se empleó como una herramienta de diagnóstico complementaria.

El modelo final conectado al DSA es el SVARX país por país (VAR Estocástico Condicionado).

No se utiliza un VAR teórico abstracto para el DSA, sino las Funciones de Impulso-Respuesta (IRF) y las simulaciones estocásticas extraídas del SVARX del país objeto de estudio.

¿Cómo interactúan el SVARX y el DSA?

El DSA proyecta la relación Deuda/PIB () mediante la ley de movimiento:



  Un choque exógeno en el SVAR (ej. caída en el  o salto en el ) genera trayectorias simuladas para el crecimiento económico (), la tasa de interés de financiamiento () y la depreciación del tipo de cambio ().

  La Función de Reacción Fiscal (FRF) aporta la respuesta del resultado primario () ante el ciclo.

  El DSA toma esas trayectorias endógenas provenientes del SVAR y calcula mediante simulaciones de Monte Carlo la probabilidad de que la senda de la deuda pública se vuelva insostenible ante el shock simulado.

Conclusiones Principales para Argentina

Alta vulnerabilidad a shocks externos (Push): Las entradas de no residentes muestran una extrema sensibilidad a incrementos en la tasa de la Fed o del índice VIX, provocando frenadas bruscas (sudden stops).

Comportamiento de residentes (Capital Flight vs. Retrenchment): A diferencia de mercados desarrollados donde los residentes repatrían activos externos para amortiguar crisis internas, en Argentina el capital residente tiende a sumarse a la salida (fuga de capitales), amplificando la inestabilidad por desconfianza institucional y régimen cambiario.

Predominio de factores globales: Más del 50% de la variabilidad de las entradas de capitales a corto plazo responde a condiciones internacionales y no a variables de atracción local (Pull) como la tasa de interés interna.

Early Warning System for Government Debt Crisis in Developing Countries (2020)

Prueba T de diferencia de medias

Comparan la media de cada indicador (inflación, deuda externa/exportaciones, tipo de cambio, etc.) en períodos de crisis vs. no-crisis, usando un t-test estándar. Esto es exploratorio: solo confirma si un indicador "se comporta distinto" en crisis, sin poder predictivo aún.

las 7 categorías del paper (macro, deuda privada, deuda externa, pagos de interés, deuda corto plazo, servicio de deuda, fiscal).

Test de raíz unitaria (ADF) para verificar estacionariedad de cada serie. 

T-test de diferencia de medias crisis vs. no-crisis por indicador.

Análisis de eventos (event analysis)

Normalizan cada indicador con z-score y corren una regresión panel con variables dummy para cada período relativo a la crisis (T-3, T-2, T-1, T, T+1, T+2, T+3, con efectos fijos por país). Esto permite ver la "trayectoria" del indicador antes y después del evento —por ejemplo, ver que la deuda externa empieza a subir 3 años antes de la crisis.



Ratio de ruido a señal (Noise-to-Signal Ratio, NTSR)

Método de Kaminsky, Lizondo y Reinhart (1998). Para cada indicador:

Definen un umbral (media de largo plazo + entre 0.5 y 3 desvíos estándar)

Si el indicador cruza el umbral, "emite señal"

Clasifican cada señal en una matriz 2x2: señal+crisis (A), señal+no-crisis (B, ruido/falsa alarma), no señal+crisis (C, crisis perdida), no señal+no-crisis (D)

Calculan NTSR = (B/(B+D)) / (A/(A+C)) — cuanto más bajo, mejor el indicador

Prueban distintas ventanas de predicción (1, 2 y 4 años antes de la crisis)

Regresión logística binomial (el modelo "general")

Variable dependiente: 1 si hay crisis, 0 si no

Toman los indicadores significativos de la etapa NTSR, los normalizan, y corren logit por categorías (deuda pública, deuda privada, deuda externa, pagos de intereses, deuda de corto plazo, servicio de deuda)

Los indicadores significativos y con signo "correcto" (intuitivo) pasan a un modelo general único con 9 variables

Usan test de Hausman para elegir entre efectos aleatorios/fijos (eligen aleatorios)

Evalúan poder predictivo con un corte de probabilidad del 30% (preferido para minimizar crisis no detectadas) → logran predecir 61.5% de las crisis con 2 años de anticipación

  Logit por categoría: correr regresión logística binomial separada para cada grupo de indicadores, filtrando por significancia y signo esperado. 

 Construir modelo general: combinar los indicadores significativos de todas las categorías en un único logit. 

 Validar el modelo: Pseudo R², BIC/AIC, test de Hausman (efectos fijos vs. aleatorios). 

 Evaluar poder predictivo: fijar un umbral de probabilidad (ellos usan 30%), construir matriz de confusión y calcular % de crisis correctamente predichas.

Stochastic debt simulation using VAR models and a panel fiscal reaction function: results for a selected number of countries (European Economy, Economic Papers No. 459, July 2012)

Modelo VAR (Vector Autoregression) — no restringido

  Variables incluidas (hasta 6): inflación, crecimiento del PBI, tasa de interés real, tipo de cambio real efectivo (REER), crecimiento de Alemania, tasa de interés real de Alemania (esta última porque el estudio es sobre países de la UE, Alemania actúa como "ancla") 

  Se estima un VAR por país (no panel), con datos trimestrales 

 Protocolo de 4 pasos para construir cada VAR: 

Elegir variables endógenas (mínimo 3: inflación, crecimiento, tasa real)

Testear raíz unitaria (ADF o Phillips-Perron) → si la variable no es estacionaria, se diferencia

Elegir el rezago óptimo (criterio de Schwarz si N<120 obs, Hannan-Quinn si N>120)

Testear cambio estructural (test EFP, "empirical fluctuation processes")

la estimación se obtienen los residuos (shocks históricos) y la matriz de varianzas-covarianzas de esos residuos. Eso es lo que después se usa para generar shocks aleatorios "realistas" (que respetan cómo se mueven juntas la inflación, el crecimiento, la tasa, el tipo de cambio en la historia de ese país).

Dos formas de generar los shocks aleatorios

a) Errores normales: asumir que los residuos siguen una distribución normal multivariada, usando la matriz de varianza-covarianza estimada y la descomposición de Cholesky para generar draws correlacionados.

b) Bootstrapping: en vez de asumir una forma funcional (normal), se re-samplea con reposición directamente de los residuos históricos observados. Esto es más robusto porque el paper encuentra (con el test de Jarque-Bera) que los residuos no son normales — tienen colas más pesadas o asimetría. El paper concluye que el bootstrapping es preferible.

bootstrap de residuos estandarizados de un modelo GARCH (a veces "filtered historical simulation" o "GARCH-bootstrap"). No es una ocurrencia rara, es el punto de encuentro natural entre las dos familias que estabas comparando, y resuelve exactamente la debilidad que señalé del bootstrap puro. Te explico cómo funciona y por qué tu propia ampliación de la muestra (que mencionás) lo hace más viable todavía.

La idea central: separar "forma" de "sorpresa"

El truco está en no bootstrapear los shocks crudos (los valores históricos de crecimiento, tipo de cambio, resultado primario tal cual vinieron), sino bootstrapear los residuos estandarizados que salen de tu propio modelo GARCH — es decir, la parte de cada shock que ya no se explica por la volatilidad cambiante que el GARCH captura.

Concretamente, así se arma:

Paso 1 — Estimás el GARCH(1,1), como ya hiciste
Para cada variable (resultado primario, crecimiento, tipo de cambio real), el modelo te da una volatilidad condicional σt​ que cambia en cada trimestre, capturando los clusters de volatilidad.

Paso 2 — "Blanqueás" la serie
Dividís cada shock histórico observado por la volatilidad que el GARCH predijo para ese momento:

zt​=σt​εt​​ 

Este zt​ es el "residuo estandarizado" — lo que queda del shock una vez que le sacás la parte de volatilidad cambiante que el GARCH ya explicó. Si el GARCH está bien especificado, esta serie zt​ debería comportarse de forma mucho más "pareja" en el tiempo (sin los clusters de volatilidad que tenía la serie original).

Paso 3 — Bootstrapeás esos residuos, no los shocks crudos
Resorteás con reemplazo esta serie de zt​ (o bloques de zt​, para preservar la dependencia entre variables en el mismo trimestre) — que es una serie más "limpia" y homogénea que los shocks originales.

Paso 4 — Reconstruís nuevos shocks combinando ambas piezas
Para cada trayectoria simulada de tu Monte Carlo, generás una nueva volatilidad condicional siguiendo la dinámica GARCH (que sí puede generar escenarios de volatilidad que nunca ocurrieron exactamente igual), y la multiplicás por un residuo bootstrapeado (que sí viene de la distribución empírica real, no de un supuesto teórico como la t-Student):

εtsimulado​=σtsimulado​×ztbootstrapeado​ 

Por qué esto resuelve exactamente lo que te preocupaba de cada método por separado

Del GARCH puro con t-Student, heredás la capacidad de generar dinámicas de volatilidad nuevas y de mantener la correlación cambiante en el tiempo (vía tu DCC-GARCH) — no quedás limitado a repetir la historia tal cual.

Del bootstrap puro, heredás que la "forma" de la sorpresa no depende de ningún supuesto de distribución teórica (t-Student u otra) que puede estar mal especificada — usás la distribución empírica real de los residuos, con toda su asimetría y sus colas gordas genuinas, sin tener que asumir que se parecen a una t con ν≈5.1 grados de libertad como hacés hoy.

Y el problema central que señalé del bootstrap puro (pocos episodios de crisis) se atenúa, porque al trabajar sobre los residuos estandarizados en vez de los shocks crudos, la parte de "esto fue un evento extremo" ya está parcialmente absorbida por la volatilidad condicional del GARCH — lo que te queda para bootstrapear es una serie más corta en amplitud, con lo cual tenés más margen para recombinar sin simplemente repetir el mismo evento de 2018-2020 una y otra vez.

Por qué la ampliación de la muestra que mencionás lo hace más atractivo todavía

Acá está el punto que agregás vos, y es válido: el problema que señalé del bootstrap puro (pocos episodios independientes de los que resortear) depende directamente del tamaño de la muestra. Si extendés la serie hacia atrás (por ejemplo, a 1997 como discutimos antes, sumando la crisis de 2001-2002), no solo ganás observaciones en términos absolutos — ganás un segundo evento de estrés severo genuinamente distinto al de 2018-2020 (distinta causa, distinta dinámica cambiaria, la salida de la Convertibilidad no es lo mismo que el cierre de mercados voluntarios post-2018). Eso le da al bootstrap (puro o combinado con GARCH) más de un "arquetipo" de crisis para recombinar, en vez de un solo patrón que se repite. Con panel de países (la otra vía de ampliación que discutimos extensamente) el beneficio sería todavía mayor, porque sumarías episodios de crisis de otros países con dinámicas distintas a las dos argentinas.

Panel Fiscal Reaction Function (FRF)

Qué es: Una regresión panel que estima cómo reacciona el balance primario (superávit/déficit antes de intereses) de un gobierno ante:

El nivel de deuda/PBI rezagado (¿el gobierno se "endereza" cuando la deuda sube?)

La brecha del producto (output gap, componente cíclico)

Variables institucionales (ej. índice de reglas fiscales)

Hallazgo clave — "fatiga fiscal" (fiscal fatigue): ajustan un polinomio cúbico de la deuda rezagada, y encuentran que la respuesta fiscal (cuánto ajusta el gobierno su superávit primario cuando sube la deuda) deja de aumentar y empieza a caer una vez que la deuda supera ~80-90% del PBI. Es decir, los gobiernos "se cansan" de ajustar a niveles de deuda muy altos — el modelo captura ese comportamiento no lineal.

Simulación de Montecarlo (2000 iteraciones)

Cómo funciona la mecánica de la simulación (ecuaciones 3i-3iii del paper):

Cada año, se dibuja un shock aleatorio (normal o bootstrapped) para las variables macro

Ese shock alimenta el VAR → genera una trayectoria de crecimiento, inflación, tasa de interés, tipo de cambio para ese año

Con esos valores, se calcula el output gap

El output gap y la deuda rezagada alimentan el FRF estimado → se obtiene el balance primario simulado para ese año

Con el balance primario, la tasa de interés implícita, y el crecimiento nominal, se actualiza la deuda/PBI usando la identidad contable estándar de dinámica de deuda:
dt​=1+nt​1+it​​⋅dt−1​−pbt​ (deuda hoy = deuda ayer ajustada por diferencial tasa-crecimiento, menos el superávit primario)

Se repite para 5 años (2012-2016), y todo el proceso se repite 2000 veces → se obtiene una distribución empírica completa de trayectorias posibles

Filtro Hodrick-Prescott (HP)

Qué es: una técnica estadística de suavizado que separa una serie de tiempo en un componente de "tendencia" (producto potencial) y un componente "cíclico" (output gap), minimizando una función de pérdida que penaliza tanto el ajuste a los datos como la curvatura de la tendencia (controlada por un parámetro λ, acá usan 1600 para datos trimestrales, el valor estándar).

Para qué se usa: en cada una de las 2000 simulaciones, se corre el filtro HP sobre el PBI simulado para reestimar el output gap "consistente" con esa trayectoria simulada (no usan un output gap fijo del pasado).

Es puramente un ejercicio de contabilidad estadística: "dado este PBI simulado, ¿cuánto de eso es ciclo y cuánto es tendencia?" El filtro se corre 2000 veces, una por cada simulación de Montecarlo, porque cada trayectoria simulada de PBI es distinta, así que el output gap resultante también lo es en cada una.

Dónde entra la relación con el superávit

Esa medida de output gap (ya calculada) se enchufa después como variable explicativa en la ecuación de la FRF (ecuación 3ii del paper):

pb​i,t​=α^0​+η^​i​+ρ^​⋅d^i,t−1​+γ^​⋅gapi,t​+ε^i,t​ 

El coeficiente γ (gamma) es positivo y significativo en todas las especificaciones (~0.69-0.73 en la Tabla 3). Eso significa: sí, cuando el output gap es positivo (auge, economía por encima de su potencial), el balance primario simulado tiende a ser más alto (más superávit / menos déficit). Eso captura tanto estabilizadores automáticos (más recaudación en el auge) como comportamiento discrecional.

No neutralidad del shock de envejecimiento: El modelo asume que los pasivos futuros están fuertemente condicionados por variables demográficas exógenas e inevitables (costos presupuestarios ligados al envejecimiento / ageing costs) que actúan como shocks de acumulación de deuda ajenos al ciclo32.

 Tests estadísticos usados

  Jarque-Bera: testear si los residuos del VAR son normales 

 Shapiro-Wilk: testear si la distribución simulada de deuda final es normal 

  EFP (empirical fluctuation processes, Zeileis et al. 2002): detectar quiebres estructurales en las ecuaciones del VAR, basado en la suma acumulada de residuos OLS 

 Test de Hausman

Dificultades para aplicar esto a Argentina

1. El FRF panel fue estimado sobre economías avanzadas de la UE — no es transferible
El "mean reversion" fiscal que estima el panel FRF refleja el comportamiento promedio de países con marcos institucionales de disciplina fiscal fuertes (Pacto de Estabilidad, vigilancia de la Comisión Europea). Aplicado a Argentina, ese parámetro de reversión a la media sería completamente irrelevante — necesitarías estimar un FRF específico para Argentina (o LatAm) con series propias, algo que el paper mismo reconoce como necesario cuando dice que la "fatiga fiscal" depende del marco institucional.

2. Estacionariedad y quiebres estructurales constantes
El protocolo VAR asume relativa estabilidad estructural (de hecho testean explícitamente que no haya quiebres, y en los 15 países de la UE no los encuentran). En Argentina, con múltiples regímenes cambiarios (convertibilidad, flotación sucia, cepo, dólar oficial/blue/CCL), crisis recurrentes, y cambios de régimen monetario, es altamente probable que cualquier VAR mostraría quiebres estructurales significativos, violando un supuesto central del protocolo.

3. Tipo de cambio real efectivo y series de inflación con problemas de calidad
El REER y la inflación son dos de las variables centrales del VAR. En Argentina hubo períodos de manipulación estadística (INDEC 2007-2015) y múltiples tipos de cambio simultáneos (oficial, blue, MEP, CCL), lo que hace muy difícil construir una serie única y confiable de "el" tipo de cambio real o "la" inflación para alimentar el modelo.

4. La tasa de interés real y el acceso al financiamiento son discontinuos
El modelo asume que el gobierno puede seguir financiándose a una tasa "implícita" que evoluciona suavemente (ecuación 6i-6ii). Argentina tiene episodios de cierre total del acceso al mercado de deuda (2001-2016, 2019-presente en gran medida) donde no hay "tasa de mercado" relevante — el financiamiento pasa a ser monetario (emisión) o vía organismos multilaterales, lo cual rompe la lógica de "tasa implícita ponderada" del modelo.

5. Denominación en moneda extranjera de la deuda
El modelo de dinámica de deuda (ecuación 3iii) está pensado implícitamente para deuda en moneda doméstica de países con bajo riesgo cambiario relativo (euro, corona, libra). En Argentina, gran parte de la deuda está en dólares, por lo que la dinámica de deuda/PBI es extremadamente sensible a shocks cambiarios grandes y abruptos (maxi-devaluaciones), que son eventos de cola gruesa mal capturados por VARs entrenados en períodos "normales".

6. Datos trimestrales de calidad y profundidad histórica limitados
El protocolo exige series trimestrales largas (120+ observaciones ideales) de PBI, inflación, tasas reales, REER. Para Argentina, series consistentes y comparables (sin cambios de metodología o de año base) de esa longitud son más difíciles de conseguir que para un país de la UE con Eurostat.

On the estimation of panel fiscal reaction functions: Heterogeneity or fiscal fatigue?

Los autores testean si la "fatiga fiscal" (fiscal fatigue) —la idea de que el balance primario responde cada vez menos a la deuda a medida que esta crece, hasta volverse negativa a niveles muy altos— es una característica genuina de la política fiscal, o si es un artefacto estadístico de estimar un panel homogéneo cuando en realidad hay heterogeneidad entre países.

2. Los datos

Panel no balanceado de 21 países OECD, 1970-2014 (datos anuales).

Variable dependiente: balance primario (% PBI).

Variable clave: deuda/PBI rezagada (lineal, cuadrática, cúbica).

Controles: output gap, inflación, tasa de interés implícita, cuenta corriente, apertura comercial, dummies (euro, elecciones, regla fiscal), proporción de población mayor (actual y futura).

Además, un panel de datos trimestrales (interés real, crecimiento del PBI real, inflación) para estimar VARs país por país.

3. Herramientas econométricas y cómo funcionan

a) Regresión de panel con efectos fijos (país y tiempo)
Sirve para controlar heterogeneidad no observada constante en el tiempo por país (institucionales, culturales) y shocks comunes a todos los países en un año dado (crisis del petróleo, crisis financiera global). Técnicamente, se le resta a cada variable su media por país (o por año) antes de estimar por MCO.

b) GLS de Prais-Winsten (corrección AR(1))
En la especificación base (estática), el error se modela como autorregresivo de orden 1: εit = ρεi,t-1 + µit. El GLS transforma los datos para "blanquear" esa autocorrelación y obtener estimadores eficientes. Los autores muestran que esta corrección "mecánica" oculta el verdadero problema (persistencia genuina, no solo ruido autocorrelacionado).

c) Modelo dinámico (panel con variable dependiente rezagada)
Agregan pbi,t-1 como regresor para capturar la lentitud política real del ajuste presupuestario, en vez de forzarla dentro del error vía AR(1). Esto introduce el conocido sesgo de Nickell (fixed effects + lag en panels con T finito), pero como T=45 es "grande", el sesgo es teóricamente despreciable (lo verifican comparando con GMM de Arellano-Bover/Blundell-Bond y con corrección de Kiviet, sin diferencias relevantes).

d) Variables instrumentales (IV/2SLS)
El output gap, la cuenta corriente y la tasa de interés implícita son potencialmente endógenas (la política fiscal afecta al ciclo, y viceversa). Se instrumentan con sus propios rezagos (t-1, t-2) y, para el output gap, con un promedio ponderado (por comercio) del output gap de otros países ("foreign output gap"). La lógica: estos instrumentos están correlacionados con la variable endógena pero son predeterminados respecto al shock contemporáneo del balance primario.

e) Estimador Mean Group (Pesaran & Smith / Pesaran 2006)
Para testear heterogeneidad de pendientes: en vez de imponer un único coeficiente β para todos los países, se estima una regresión separada para cada país (β̂i) y luego se promedian esos coeficientes (β̂MG = (1/N)Σβ̂i), con un error estándar no paramétrico basado en la dispersión entre países (ecuación 5). Esto permite distinguir "fatiga fiscal generalizada" de "heterogeneidad entre países".

f) Test de Wald de heterogeneidad
Testea H0: β1 = β2 = ... = βN (todas las pendientes país-específicas son iguales) vs. la alternativa de que difieren. Usa matriz de covarianza robusta a heteroscedasticidad.

g) Test de Cumby-Huizinga (1992)
Test de autocorrelación de primer orden robusto a heteroscedasticidad, aplicable cuando la regresión se estimó por variables instrumentales (a diferencia del Durbin-Watson clásico, que no sirve con IV).

h) VAR (Vector Autoregresivo) por país
Para simular trayectorias futuras de deuda, estiman un VAR trimestral irrestricto por país con: tasa de interés real (promedio corto/largo plazo), crecimiento del PBI real e inflación. El orden de rezagos se elige con criterio de Schwarz (muestras <120 obs) o Hannan-Quinn (muestras más largas).

i) Simulación de Montecarlo / bootstrap de innovaciones
Como el test de Jarque-Bera rechaza normalidad de los residuos del VAR, en vez de asumir shocks normales, remuestrean con reemplazo los residuos históricos del VAR (bootstrap), manteniendo la correlación cruzada entre variables (remuestreo conjunto por período). Con esto generan 2000 trayectorias de 5 años para cada país, combinando el VAR (para interés, crecimiento, inflación) con la FRF estimada (para el balance primario) y la ecuación dinámica de deuda (ecuación 6), produciendo los "fan charts".

j) Filtro de Hodrick-Prescott (λ=1600)
Se usa para extraer el output gap a partir de las trayectorias simuladas de crecimiento del PBI (con extensión de 4 trimestres para evitar el problema de "final de muestra").

El concepto del paper: Everaert y Jansen explican que los países con reacciones fiscales históricamente débiles ante la acumulación de deuda (menor pendiente de reacción) naturalmente terminan registrando mayores niveles de endeudamiento a lo largo del tiempo. Al estimar una FRF agregada u homogénea, los modelos tradicionales asumen que el país sufre "fatiga fiscal" en niveles altos de deuda, cuando en realidad el problema es simplemente que ese país siempre tuvo una pendiente de reacción baja debido a factores institucionales e históricos no modelados.

Aplicación a Argentina post-2025: Este argumento es perfecto para describir la "intolerancia a la deuda" de Argentina (en los términos de Reinhart, Rogoff y Savastano). Argentina no reacciona fiscalmente igual que un promedio de mercados emergentes o avanzados. Su historia institucional de defaults, devaluaciones y cepos cambiarios configura una pendiente de reacción fiscal heterogénea y altamente persistente. Tu tesis puede utilizar este marco para justificar metodológicamente por qué se requiere un indicador específico de descalce de monedas y dinámica interna (como el EFS de Rodríguez) en lugar de un modelo de reacción fiscal homogéneo.

entonces es una justificación de porqué la fatiga fiscal estudiada en econometría no aplica a argentina, y que las simulaciones de fatiga fiscal pueden subestimar la reacción de la política fiscal

Financiamiento y sostenibilidad de la deuda pública: el caso de la economía argentina (2001-2022)

Paso a paso de la metodología

Reconstrucción histórica del esquema ahorro-inversión (1975-1996) del Sector Público Nacional no Financiero, en base devengado, a partir de series oficiales homogeneizadas por los propios autores (porque las publicaciones oficiales cambiaron de metodología varias veces).

Desagregación del presupuesto en componentes elementales: 8 rubros de ingresos (IVA interno, IVA importaciones, ganancias, combustibles, aranceles, exportaciones, nómina salarial, internos) y 7 de gasto (personal, seguridad social, bienes y servicios, transferencias a provincias, capital, intereses internos, intereses externos).

Vinculación de cada rubro con su variable macroeconómica relevante (VMR) mediante coeficientes fijos (elasticidad implícita), estimados en tres "fotografías" de la estructura fiscal: 1991 (inicio de Convertibilidad), 1994 (post reforma previsional) y 1996 (post crisis del Tequila).

Test de raíz unitaria con quiebre estructural (Perron 1994, sobre ADF estándar) para confirmar que el PBI tiene un quiebre de tendencia en 1991:1 (arranque de la Convertibilidad) y no es simplemente una caminata aleatoria.

Filtro de Hodrick-Prescott (HP) aplicado a las series macro relevantes (PBI, consumo, exportaciones, importaciones, inversión) para separar tendencia de componente cíclico.

Resolución del modelo con datos observados vs. datos de tendencia: se corre el mismo sistema de ecuaciones lineales dos veces —una con los valores efectivamente observados de las VMR y otra con sus valores de tendencia— manteniendo fijos los coeficientes de cada estructura fiscal. La diferencia es el déficit macroeconómicamente ajustado (DMA).

Cálculo del "impulso fiscal" (metodología de Blanchard, 1990): usando 1991 como año base, se aísla qué parte del cambio en el déficit se debe a la macroeconomía y cuál a decisiones de política tributaria/gasto (o a mejoras en la administración tributaria).

Proyección 1997-2001 usando la estructura fiscal de 1996 y una trayectoria supuesta de variables exógenas (crecimiento, exportaciones, tasa Libor, riesgo país), en un escenario central y uno alternativo (menor crecimiento + mayor tasa de interés externa).

Estimación separada del "déficit ajustado por tendencias estructurales" (DTE): incorpora compromisos de largo plazo no capturados por el modelo cíclico —principalmente el desequilibrio actuarial del sistema previsional reformado, descontado a valor presente— para llegar a una medida más completa de sostenibilidad de largo plazo.

Herramientas y cómo funcionan

Modelo de ecuaciones lineales ingreso-gasto: cada rubro fiscal = coeficiente × su VMR correspondiente (ej. IVA interno depende del consumo desestacionalizado; el gasto en personal depende del salario medio público y la planta de empleados). Los coeficientes se recalculan para tres momentos distintos porque la estructura tributaria argentina cambió radicalmente entre 1991-96 (privatizaciones, reforma previsional, reducción de aportes patronales, etc.).

Filtro HP: separa cada serie en tendencia (crecimiento estructural, ej. 4,6-4,75% anual en los 90) y ciclo (desvíos transitorios respecto a esa tendencia). Permite calcular cuánto del "boom" de ingresos 1991-94 fue estructural (permanente) y cuánto puramente cíclico (transitorio, reversible).

Déficit macroeconómicamente ajustado (DMA): mide el "riesgo fiscal" de corto plazo — cuánto se desvía el déficit observado del que resultaría si la economía estuviera en su sendero de tendencia. Resultado: apenas 0,3-0,6% del PIB en los 90, comparado con las violentas oscilaciones de los 70-80 (picos de 10-13% del PIB).

Impulso fiscal de Blanchard: aísla el efecto puramente discrecional/administrativo de la política fiscal, descontando el efecto macro. Mostró un fuerte impulso contractivo entre 1992-95 (hasta -2,1% del PIB en 1995), insuficiente para compensar la pérdida de ingresos por privatizaciones.

Proyección actuarial del sistema previsional (basada en trabajos externos de Schulthess-Demarco y Durán): calcula el valor presente de los desequilibrios futuros del sistema de pensiones descontando a una tasa del 10% anual hasta 2025 — la pieza clave para capturar compromisos de largo plazo que el análisis cíclico convencional no ve.

Conclusiones aplicables a Argentina (todo el paper es sobre Argentina)

El riesgo fiscal cíclico en Convertibilidad era chico (0,3-0,6% del PIB), muy inferior a la volatilidad fiscal de los 70-80, porque se habían desactivado los mecanismos clásicos de inestabilidad (aceleración inflacionaria, efecto Olivera-Tanzi, shocks de tasa internacional).

La mejora fiscal observada 1991-96 fue mayoritariamente estructural (reformas tributarias, mejor administración) y no un artefacto del ciclo económico expansivo — el "boom" de recaudación no era solo transitorio.

El escenario central de proyección (1997-2001) mostraba un déficit fiscal decreciente y sostenible en sentido estricto — pero el propio documento advierte que el desequilibrio de cuenta corriente externa crecía hasta superar 7% del PIB en 2001, señal de que el verdadero riesgo no era fiscal sino de sostenibilidad externa (aquí el paper anticipa, en 1997, el problema que efectivamente detonó la crisis de 2001-02).

Bajo el escenario alternativo (tasa de interés externa +2 puntos, menor crecimiento), la estructura fiscal de 1996 dejaba de ser sostenible: la relación deuda pública/PIB pasaba de 30,5% a 33,7% en 5 años, y deuda/recursos de 187% a 210%.

La reforma previsional de 1994 no resolvió el problema estructural del sistema: el valor presente de los desequilibrios futuros hasta 2025 alcanzaba ~29% del PIB de 1996 (31% si el salario real crecía 2% anual), lo que sumaba ~1 punto adicional del PIB al déficit "verdadero" respecto al que arrojaba el análisis cíclico solo.

Conclusión metodológica central: el déficit fiscal observado, incluso ajustado por ciclo, no alcanza para juzgar sostenibilidad — hace falta mirar también el sector externo y los compromisos actuariales de largo plazo (previsión, coparticipación, educación).

Qué herramienta "no vale la pena" usar (o usar sola)

El propio documento señala explícitamente sus límites:

El déficit fiscal ajustado por ciclo, usado en soledad, es insuficiente y hasta engañoso: da una imagen de sostenibilidad ("el déficit tiende a declinar... incluso dando lugar a aumentos de salarios reales") mientras el desequilibrio externo se dispara — es decir, el mismo escenario que el modelo cataloga como fiscalmente sostenible resulta externalmente insostenible. Usar solo esta herramienta sin mirar el balance de pagos habría llevado a una conclusión equivocada.

Los coeficientes fijos calibrados sobre la estructura de 1996-97 no son un buen instrumento para proyectar a mediano/largo plazo: los propios autores advierten que esa estructura reflejaba un esquema fiscal "extremo", diseñado para enfrentar la emergencia post-Tequila, y que la presión política típica (bajar impuestos, subir gasto) una vez superada la crisis lo volvía inestable — el modelo asume implícitamente que esa fotografía de política tributaria se mantiene constante, algo que la propia historia argentina desmentía sistemáticamente.

El supuesto de financiamiento simplificado (toda la deuda nueva colocada a 5 años, bullet, un solo cupón) para proyectar la deuda es una simplificación que no captura riesgos de refinanciamiento (rollover risk) — exactamente el tipo de riesgo que, 25 años después, el marco del FMI que revisamos en el documento anterior sí trata de capturar explícitamente con el módulo GFN.

La justificación teórica de por qué "falla" el fanchart del FMI

En tu tesis, necesitarás discutir por qué las señales mecánicas de los organismos internacionales a menudo no funcionan bien en Argentina. El paper de Rodríguez te da el argumento de defensa perfecto: el ratio Deuda/PIB bruto es sumamente engañoso porque está excesivamente distorsionado por las fluctuaciones de precios y del tipo de cambio real.

Rodríguez demuestra que durante el periodo 2003–2011, la abrupta caída del ratio Deuda/PIB no se debió a un desendeudamiento estructural, sino a un efecto contable de apreciación del tipo de cambio real (el PIB medido en dólares creció más rápido que el stock de deuda).

Este concepto explica de forma exacta la distorsión que reportó el FMI en 2024: el salto cambiario de finales de 2023 disparó matemáticamente la deuda al 156.7% del PIB. Este movimiento de valuación ensanchó de tal manera el abanico probabilístico (fanchart width de 122.7) que activó una alarma roja mecánica de "Riesgo Alto". El propio personal del FMI tuvo que anular la señal mecánica reconociendo que no reflejaba el riesgo real de mediano plazo. Al citar a Rodríguez, le darás un riguroso sustento académico a tu crítica sobre las limitaciones de los ratios estáticos del FMI.

Sudden Stops, the Real Exchange Rate, and Fiscal Sustainability: Argentina’s Lessons (NBER Working Paper No. 9828, July 2003)

Establecer el hecho estilizado (contagio)
Muestran que la crisis rusa de 1998 generó un "Sudden Stop" (frenazo brusco e inesperado de capitales) que golpeó a toda América Latina, no solo a países con fundamentals débiles. Herramienta: series de tiempo de spreads (EMBI+) y flujos de capital

Medir cuánto debía ajustar el tipo de cambio real (RER)
Construyen un modelo de equilibrio parcial muy simple:

Definen el "coeficiente de absorción no apalancada" ω = (Y−S)/A*** (oferta de transables neta de pagos de factores, sobre absorción de transables). Cuanto más bajo ω, más cerrada/apalancada la economía.

De una ecuación de demanda de no-transables log-lineal derivan que la depreciación real necesaria es −dp = (1−ω)/c, donde c es la elasticidad-precio de demanda de no-transables.

Calibran con c = 0.4 (el valor más bajo de la literatura) y comparan Argentina, Brasil, Chile, Colombia, Ecuador.

Herramienta: contabilidad de balanza de pagos + calibración (no estiman c ni ω econométricamente, los toman de datos observados/literatura).

Paso 3 — Traducir el RER a sostenibilidad fiscal
Usan la ecuación estándar de dinámica de deuda: b̄ = s·(1+θ)/(r−θ) para encontrar el superávit primario necesario para estabilizar la deuda/PIB. Luego muestran cómo una devaluación real afecta b según la fórmula de valuación b = (B+eB)/(Y+eY)**, que depende del "descalce" entre denominación de deuda (pesos vs. dólares) y denominación de ingresos.

Construyen un índice de descalce (B/eB*)/(Y/eY*) por país.

Simulan un shock hipotético (RER +50%) y recalculan deuda/PIB y superávit primario requerido (Tablas 6-9).

Paso 4 — Sumar pasivos contingentes
Agregan al ejercicio el costo fiscal de rescatar bancos y empresas dolarizadas (estimación directa en dólares, no modelo).

Paso 5 — Explicación política (economía política)
No cuantitativa: aplican el marco de "guerra de desgaste" (Alesina-Drazen / Sturzenegger-Tommasi) para explicar por qué la redistribución de la carga fiscal se demoró políticamente.

El marco "CDM" (Closed, Dollarized, Mismatched) que proponen los autores sigue siendo la lente correcta, pero la Argentina de 2026 luce distinta en varios de esos ejes según los datos más recientes:

Fiscal: hay superávit primario sostenido desde 2024 (~1,4% del PIB en 2025), algo que Argentina no tenía en 2001. El pilar central del programa económico continúa siendo el equilibrio fiscal tras el quiebre en 2024 cuando se revirtieron años de déficits fiscales persistentes a superávit primario. Esto reduce el canal "deuda pública vulnerable a la reevaluación por RER" que el paper identifica como clave. bbvaresearch

Régimen cambiario: ya no hay convertibilidad/paridad fija; hay un esquema de bandas que se ajusta con la inflación. El esquema cambiario también se adapta a la nueva lógica de sostenibilidad externa, con un régimen de bandas que se actualiza en función al último dato de inflación disponible. Esto es justamente la "flexibilidad cambiaria" que el paper señala como paliativo parcial (lección #5), aunque ellos mismos advierten que sin resolver el resto (C, D, M) el float por sí solo no resuelve el problema de fondo. eleconomista

Reservas y deuda: durante el primer semestre de 2026 las reservas netas internacionales aumentaron y bajo metodología FMI el incremento fue de cerca de USD 9.200 millones, superando la meta prevista para junio, pero al mismo tiempo el stock de deuda pública supera el 70% del PIB según estimaciones del Ministerio de Economía en 2026, un nivel de endeudamiento alto en términos históricos. deloittefortunaweb

Dolarización/descalce: sigue siendo alta —buena parte de la deuda pública y privada está en dólares o indexada—, y eso es exactamente el "M" del marco CDM que los autores señalan como el ingrediente más peligroso porque amplifica cualquier salto cambiario sobre los balances.

Apertura comercial ("C"): Argentina sigue siendo una economía relativamente cerrada en comparación con Chile, el ejemplo "exitoso" del paper, aunque hay liberalización en curso (eliminación de controles cambiarios) que las calificadoras ven con cautela porque podría reavivar desequilibrios macroeconómicos que pondrían en peligro la sostenibilidad de la balanza de pagos. larepublica

Conclusiones relevantes que podés sacar

El diagnóstico fiscal "de flujo" no basta. El paper muestra que en 1998 Argentina no lucía insolvente por su déficit corriente; el problema era la exposición patrimonial (stock) a un salto del tipo de cambio real. Hoy, el superávit fiscal es una buena noticia, pero el ejercicio de los autores sugiere mirar también el descalce de moneda del stock de deuda y de los balances privados, no solo el resultado fiscal del año.

Apertura comercial reduce el tamaño del ajuste cambiario necesario ante un shock externo. Cuanto más exportadora sea la economía relativa a su absorción de transables, menor es el "salto" de RER que un frenazo de capitales exige — y por lo tanto menor el daño a los balances dolarizados. Es el argumento más "estructural" y de política pública de todo el paper.

La dolarización de pasivos es más peligrosa que el nivel de deuda en sí. Dos países con igual deuda/PIB pueden tener destinos opuestos según cómo esté denominada esa deuda respecto a sus ingresos (comparación Argentina-Chile-Brasil de 1998).

El régimen cambiario (fijo vs. flotante) es secundario frente a los fundamentals CDM. Los autores son explícitos: si persisten cierre comercial, deuda alta y dolarización, ni el float evita la crisis — solo cambia la velocidad y forma en que se manifiesta. Relevante hoy porque el debate en Argentina suele centrarse mucho en el esquema cambiario y poco en el descalce de balances.

Los pasivos contingentes (rescates bancarios/corporativos) pueden ser tan grandes como la deuda "visible". Cualquier análisis de sostenibilidad que ignore la exposición bancaria al sector privado dolarizado subestima el riesgo real.

La resolución política de "quién paga el ajuste" puede ser más determinante que la economía misma. La guerra de desgaste retrasó decisiones y profundizó la crisis; es una advertencia para cualquier proceso de ajuste fiscal sostenido en el tiempo con apoyo político frágil.

The Costs of Sovereign Default: Evidence from Argentina (NBER Working Paper No. 22270, Mayo 2016)

1. Identificación del "experimento natural".
Usan el litigio República Argentina v. NML Capital: tras el default de 2001, el fondo NML (un "fondo buitre") no entró en los canjes de deuda de 2005 y 2010 y demandó en tribunales de EE.UU. (la deuda estaba bajo ley de Nueva York). Los jueces (Griesa, la Cámara de Apelaciones del 2º Circuito, la Corte Suprema) fueron emitiendo fallos que subían o bajaban la probabilidad de que Argentina volviera a caer en default. La clave: estos fallos son shocks exógenos a la probabilidad de default — no dependen de las noticias económicas del día.

2. Construcción de la base de eventos.
Armaron manualmente una lista de fallos judiciales (usando prensa financiera, LexisNexis, y hasta los metadatos de creación de los PDFs de las sentencias) y definieron "ventanas de evento" de dos días alrededor de cada fallo, comparándolas con ventanas de "no-evento" (días sin fallos).

3. Modelo econométrico — identificación por heterocedasticidad.
En vez de una simple regresión (que estaría sesgada porque los retornos accionarios también podrían influir en la probabilidad de default, y ambos podrían moverse por un factor común no observado), usan el método de Rigobon y Rigobon-Sack (2003, 2004): comparan la matriz de covarianzas entre retornos accionarios y cambios en la probabilidad de default en días de evento vs. días sin evento. La identificación se apoya en el supuesto de que la varianza del shock de default es mayor en los días de fallos judiciales, mientras que la varianza de los demás shocks es igual en ambos tipos de días. De ahí sale su "estimador CDS-IV" (equivalente a variables instrumentales).

4. Estimación de magnitudes.
Con ese estimador, calculan cuánto cae el valor de las empresas argentinas ante un aumento dado en la probabilidad de default, y extrapolan a los movimientos reales observados (~60 puntos porcentuales de aumento en la probabilidad de default durante el período estudiado).

5. Análisis de corte transversal (cross-section).
Comparan qué tipo de empresas sufren más: exportadoras, importadoras, bancos, filiales de multinacionales, grandes vs. chicas — para inferir por qué canal el default afecta a la economía real (contagio bancario, pérdida de reputación, restricciones de crédito para importar insumos, etc.).

6. Pruebas de robustez e interpretación.
Chequean que el efecto no se explique por: expectativas de un acuerdo con los holdouts, cambios generales en el derecho de deuda soberana (usan Brasil, México y otros ~30 países como "placebo"), iliquidez del mercado de CDS argentino, o riesgo de convertibilidad/controles de cambio.

Herramientas y datos utilizados (y por qué)

ADRs de empresas argentinas (certificados que cotizan en NYSE/NASDAQ) y acciones locales en pesos → para captar tanto la valoración "en dólares" como la doméstica, y comparar (útil para detectar riesgo de convertibilidad).

CDS (Credit Default Swaps) a 5 años, con datos de Markit → para extraer la probabilidad de default neutral al riesgo implícita en el mercado (usando el modelo estándar de ISDA).

VIX, índice MSCI Asia emergente, CDX High Yield/Investment Grade, precio del petróleo (WTI) → controles para aislar factores globales de aversión al riesgo y no confundirlos con el shock argentino específico.

Clasificación Fama-French de industrias y datos de intensidad de importación/exportación (Gopinath-Neiman 2014) → para el análisis por sector.

Método de Rigobon (heterocedasticidad como estrategia de identificación) → la pieza metodológica central, tomada de la literatura de shocks de política monetaria (Rigobon-Sack, Bernanke-Kuttner).

Bootstrap para los errores estándar e intervalos de confianza.

Conclusiones relevantes (para Argentina, hoy)

Un aumento del 10% en la probabilidad de default (medida por CDS) causó una caída del ~6% en el índice ponderado de acciones argentinas y una depreciación del ~1% en el dólar paralelo/blue (no en el oficial, por los controles cambiarios).

Extrapolando, pasar de 40% a 100% de probabilidad de default (lo que efectivamente vivió Argentina) implicó una caída de valor de mercado de firmas de ~30%; un default totalmente inesperado, ~45%.

La pérdida de valor de mercado de las empresas cotizantes superó ampliamente el monto que Argentina debía a los holdouts — es decir, el costo real fue mucho mayor que el "costo directo" del litigio.

Las empresas exportadoras y las filiales de multinacionales extranjeras sufrieron más — consistente con teorías de pérdida de reputación internacional y de represalias comerciales a exportadores tras un default.

Los bancos mostraron sensibilidad económica alta (aunque no siempre significativa), pero cuando se controla por apalancamiento, no parece que sus activos estuvieran especialmente dañados — Argentina no cayó en default de deuda local en pesos, lo cual amortiguó ese canal.

Los autores mismos advierten sobre la validez externa: Argentina ya estaba parcialmente excluida de los mercados internacionales antes de estos fallos, así que el costo estimado podría ser un piso (si el país "no tenía mucho que perder") o un techo (porque Argentina decidió no pagar pudiendo hacerlo, a diferencia de países que no pueden pagar). Es decir, generalizar estos números a otro episodio de default (2020, por ejemplo) o a otro país requiere cautela.

A Balance-Sheet Approach to Fiscal Sustainability

La idea central del paper es que mirar solo la deuda explícita del gobierno para juzgar la sostenibilidad fiscal es engañoso. Proponen construir un balance completo del sector público —activos y pasivos, explícitos e implícitos— y calcular el patrimonio neto (net worth) del gobierno como medida resumen de sostenibilidad, en lugar de usar el ratio deuda/PBI tradicional.



Definir variables exógenas y modelarlas con un VAR. Usan PBI, tipo de cambio real (TCR) y tasa de interés internacional (para Chile agregan el precio del cobre). Estiman un VAR estructural (economía pequeña y abierta: la tasa internacional es exógena al resto) para capturar la dinámica conjunta de estas variables.

Para "forzar" el supuesto de economía pequeña y abierta, restringen la matriz A(L) de manera que:

La tasa de interés internacional (US rate) es exógena al tipo de cambio real y al crecimiento del PBI doméstico. Es decir, el valor rezagado del TCR o del crecimiento argentino/chileno no puede entrar con coeficiente distinto de cero en la ecuación que explica la tasa de EE.UU.

Además, modelan la tasa internacional como un proceso AR separado e independiente del resto del sistema, en lugar de estimarla dentro del VAR conjunto.

Limitaciones del VAR estructural que usan

Asumen que la política fiscal es exógena a las variables reales, lo cual es fuerte y potencialmente circular.
Los propios autores lo reconocen en una nota: "this implies that we assume that the evolution of output and the real exchange rate are independent of fiscal policy in the short run". Pero justamente lo que se está analizando es sostenibilidad fiscal — si la política fiscal afecta al crecimiento o al tipo de cambio (lo cual es plausible, sobre todo en crisis), el ejercicio subestima feedbacks importantes. El supuesto es que el crecimiento del PBI y el tipo de cambio real (las variables del VAR) no son afectados por lo que el gobierno decide hacer con sus impuestos y gastos

Inestabilidad estructural / quiebres.
Tuvieron que meter a mano una dummy de quiebre estructural para la devaluación argentina de 2002 porque el VAR lineal estándar no puede capturar un salto discreto de régimen cambiario (de convertibilidad a flotación). Esto es un síntoma general: los VAR asumen relaciones estables en el tiempo, y economías emergentes con crisis recurrentes violan eso constantemente.

Sensibilidad a elecciones de especificación.
El caso de Chile lo muestra explícitamente: modelar el cobre como random walk vs. AR(1) cambia el patrimonio neto medio de 7,1 a 4,5 PBI — una diferencia enorme, puramente por una decisión de especificación del investigador, no por los datos "hablando por sí solos".

El bootstrap asume que la distribución histórica de shocks es representativa del futuro.
Si el futuro trae shocks sin precedente histórico (una crisis "nueva", no vista en la muestra), el ejercicio de simulación subestima la probabilidad de colas extremas. Es una limitación clásica de cualquier enfoque basado en bootstrapping de residuos.



Estimar funciones de respuesta de ingresos y gastos. Para cada rubro fiscal (IVA, ganancias, exportaciones, gasto corriente, transferencias, capital, etc.) corren regresiones OLS de la forma:
ln(Ingreso/PBI) = f(crecimiento del PBI, log del TCR, otros controles)
Esto captura la "elasticidad" de cada partida fiscal al ciclo y al tipo de cambio (qué tan "transable" es cada ingreso/gasto).

Los autores necesitaban proyectar hacia el futuro cada rubro de ingresos y gastos del gobierno (IVA, ganancias, exportaciones, gasto en consumo, transferencias, gasto de capital, etc.), pero no querían modelar el déficit total como un solo bloque — porque cada tipo de ingreso o gasto reacciona de forma distinta al ciclo económico y al tipo de cambio.

Entonces corrieron, para cada rubro fiscal por separado, una regresión tipo:

ln(PBIt​Ingresot​​)=α+β⋅(crecimiento del PBI)+γ⋅ln(TCRt​)+controles+εt​ 

Esto les daba, para cada partida, dos coeficientes clave:

La elasticidad al crecimiento (cuánto sube o baja esa partida cuando crece la economía)

La elasticidad al tipo de cambio real (cuánto sube o baja esa partida cuando hay una depreciación) — esto es lo que llaman el grado de "tradability" (transabilidad) de cada ítem fiscal

Ejemplos concretos que aparecen en el paper (Tabla 2a y 2b para Argentina)

El IVA e impuesto a las ganancias suben con el crecimiento del PBI, pero caen como % del PBI cuando sube el TCR (una devaluación fuerte suele coincidir con recesión).

Las exportaciones (y su impuesto asociado) muestran una elasticidad fuerte y positiva al TCR — lógico, porque una devaluación abarata los productos locales en dólares y estimula exportaciones.

El gasto en consumo público y de capital sube con el crecimiento pero cae con una devaluación — porque son gastos en pesos que se licuan en términos reales.

Las transferencias (jubilaciones, planes sociales) suben con el TCR pero no responden al crecimiento.

Por qué esto era clave para el argumento central del paper

Estas regresiones OLS son el corazón empírico que permite el resultado más importante del trabajo: mostrar que una devaluación no necesariamente empeora las cuentas públicas, porque si bien encarece la deuda en dólares, también:

aumenta la recaudación de rubros "transables" (como exportaciones), y

licúa gastos "no transables" (salarios públicos, jubilaciones, en pesos)

Sin estimar estas elasticidades rubro por rubro, los autores no podrían haber capturado ese efecto compensador — solo habrían visto el lado de la deuda, como hace el análisis tradicional.

Simular trayectorias futuras (bootstrap). Usan los residuos del VAR para generar 5.000 trayectorias simuladas de las variables exógenas (con gráficos de "abanico"/fan-charts), y con las elasticidades del paso 2 generan flujos de ingresos y gastos consistentes con cada trayectoria simulada.

Agregar todo y descontar. Suman los flujos predeterminados (deuda, seguridad social) y los "esqueletos" (pasivos contingentes no reconocidos, estimados como residuo de la ecuación de dinámica de deuda), calculan el superávit primario resultante en cada escenario, y lo descuentan a la tasa libre de riesgo internacional (no la tasa de mercado con riesgo país, porque usar esa tasa sería circular: presupone lo que se quiere probar). El resultado es una distribución de 5.000 valores de patrimonio neto.

Conclusiones relevantes para Argentina

La deuda explícita, aunque relevante, suele representar una porción pequeña del pasivo total del gobierno — para Argentina, el pasivo total en VPN era de 4.700 mil millones de pesos, de los cuales la deuda explícita representaba apenas el 5,7%.

El patrimonio neto estimado para Argentina tiene una media de ~2,2 PBI y una mediana de ~2,0 PBI, sin territorio negativo en la distribución simulada — es decir, bajo la política fiscal vigente en ese momento (post-reestructuración, con superávit primario alto), Argentina resultaba sostenible en casi todos los escenarios simulados.

Un dato clave: una devaluación real del 20% apenas mueve el patrimonio neto de Argentina (de 2,225 a 2,214 como % del PBI en la simulación base con shock). Esto es contraintuitivo respecto al enfoque tradicional (que solo mira el descalce de moneda de la deuda explícita), porque el aumento del costo de la deuda en dólares se compensa con la mejora en recaudación (impuestos a exportaciones) y la dilución de gastos en pesos (salarios y jubilaciones).

Esto contrasta fuertemente con el análisis tradicional: usando el enfoque clásico, una devaluación del 50% hacía saltar el ratio deuda/PBI argentino del 36,5% al 50,8% (citando a Calvo et al. 2003) — un resultado mucho más alarmante que el que arroja el enfoque de balance completo.

Advertencia importante que hacen los propios autores: el resultado depende de que Argentina, tras la crisis de 2001, redujo fuertemente la dolarización de su deuda — el mismo ejercicio aplicado a 2001 (con alta dolarización) habría arrojado un deterioro fiscal grande ante una devaluación. Es decir, la conclusión es sensible a la estructura de moneda vigente al momento del análisis, no es un resultado permanente.

Limitación que ellos mismos señalan: los resultados asumen que la política fiscal actual (impuestos, tasas) se mantiene constante hacia adelante, y no incorporan pagos a holdouts ni al Club de París, lo cual podría alterar la imagen de sostenibilidad si se los incluyera.





