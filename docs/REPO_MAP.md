# Compact AST Repository Map (Deuda)
> **Propósito**: Mapa ultracompacto de símbolos, docstrings y conectividad para alimentar a agentes de IA con pocos tokens.
> **Directorios escaneados**: codigo (42 módulos)
> **'conectado'** = referenciado (import o nombre de archivo) desde otro lugar del repo. 'sin referencias externas' no implica código roto -- puede ser un script standalone válido que nadie documentó todavía en SKILL_ROUTER.md.

### [`codigo_completo_deuda.py`](codigo/codigo_completo_deuda.py) — ⚠️ sin referencias externas encontradas
> CODIGO COMPLETO DEL PROCESO EMPIRICO - Tesis "La solvencia intertemporal de la deuda
- `download_vix(start_date, end_date)` — Descarga el índice VIX desde Yahoo Finance y resamplea a trimestral. (L127)
- `fetch_embi_ambito()` — Intenta obtener EMBI+ desde la API pública de Ámbito Financiero. (L148)
- `fetch_embi_datos_gob()` — Intenta obtener EMBI+ desde la API de datos.gob.ar (BCRA/MECON). (L183)
- `get_embi_fallback()` — Retorna la serie histórica verificada del EMBI+ argentino (fallback). (L213)
- `download_embi()` — Orquesta la obtención del EMBI+ con cascada de fuentes. (L224)
- `main()` (L234)
- `fetch_datos_gob(series_id, label, collapse, agg)` — Descarga una serie desde apis.datos.gob.ar. (L354)
- `get_fallback(data_dict, label)` — Construye DataFrame desde diccionario de fallback. (L384)
- *...y 82 funciones más*

### [`generacion_cronologia_quiebres.py`](codigo/graficos/generacion_cronologia_quiebres.py) — 🔗 conectado
> generacion_cronologia_quiebres.py
- `detect_breaks(series, n_breaks)` (L47)
- `main()` (L53)

### [`generacion_graficos_tesis.py`](codigo/graficos/generacion_graficos_tesis.py) — 🔗 conectado
> generacion_graficos_tesis.py
- `load_data()` (L89)
- `fig_5_1_deuda_resultado_primario(df)` — Figura 5.1 (estándar académico AER / Econometrica / FMI): (L95)
- `fig_5_3_dispersion_fatiga_fiscal(df)` — Figura 5.3 (estándar académico): Dispersión empírica (d_{t-1}, pb_t) con ajuste (L156)
- `fig_6_1_diagnostico_primera_etapa(df)` — Figura 6.1 (estándar académico): Diagnóstico de instrumentos IV-2SLS (EMBI+ real vs. (L190)
- `fig_svar_irf()` — Genera las Funciones de Impulso-Respuesta Estructurales (SVAR IRF) con bandas al 95% (L256)
- `fig_svar_fevd()` — Genera la Descomposición de Varianza del Error de Pronóstico (FEVD) a estándar editorial. (L316)
- `fig_cir_simulacion()` — Genera la simulación Monte Carlo del proceso CIR (1985) con abanico estocástico limpio (L351)
- `fig_spread_historico_1983_2025()` — Genera la figura panorámica del spread soberano histórico de 42 años (1983–2025) (L432)
- *...y 1 funciones más*

### [`actualizar_tcrm_embi_real.py`](codigo/ingesta_datos/actualizar_tcrm_embi_real.py) — 🔗 conectado
> actualizar_tcrm_embi_real.py
- `main()` (L33)

### [`construccion_dataset.py`](codigo/ingesta_datos/construccion_dataset.py) — 🔗 conectado
> construccion_dataset.py
- `run_all_ingestion()` — Ejecuta los tres módulos de ingestión y combina los resultados. (L36)
- `quality_report(df)` — Imprime un informe de calidad del dataset. (L115)
- `save_codebook(df, path)` — Genera el codebook de datos (AEA Data Policy). (L133)
- `main()` (L177)

### [`construir_dataset_1996_2025.py`](codigo/ingesta_datos/construir_dataset_1996_2025.py) — ⚠️ sin referencias externas encontradas
> construir_dataset_1996_2025.py
- `cargar_serie_empalmada(nombre_col, path_empalme)` (L43)
- `backcast_tcrm_1996()` (L53)
- `main()` (L68)

### [`construir_dataset_ampliado.py`](codigo/ingesta_datos/construir_dataset_ampliado.py) — 🔗 conectado
> construir_dataset_ampliado.py
- `cargar_serie_empalmada(nombre_col, path_empalme)` — Concatena el tramo empalmado (pre-2004) con el tramo real (real.csv). (L41)
- `main()` (L52)

### [`empalme_historico_pre2004.py`](codigo/ingesta_datos/empalme_historico_pre2004.py) — 🔗 conectado
> empalme_historico_pre2004.py
- `denton_sin_indicador(valores_anuales, anios, anclas_futuras)` — Distribuye una serie de valores anuales (promedios, no sumas -por eso (L84)
- `construir_serie_trimestral(dict_anual, link, anio_inicio, anio_fin, anclas_futuras)` (L134)
- `main()` (L143)

### [`empalme_pib_real_pre2004.py`](codigo/ingesta_datos/empalme_pib_real_pre2004.py) — ⚠️ sin referencias externas encontradas
> empalme_pib_real_pre2004.py
- `main()` (L40)

### [`fase22_construccion_spread_1983_2025.py`](codigo/ingesta_datos/fase22_construccion_spread_1983_2025.py) — 🔗 conectado
> FASE 22: CONSTRUCCION DEL SPREAD SOBERANO HISTORICO ARGENTINO (1983-2025)
- `obtener_datos_bonex_1983_1992()` — Rendimientos y Spreads de Bonex (1983T4 - 1992T4) en puntos básicos. (L30)
- `obtener_datos_brady_1993_1997()` — JP Morgan EMBI Stripped Spread (1993T1 - 1997T4) en puntos básicos. (L90)
- `obtener_datos_embi_plus_1998_2025()` — JP Morgan EMBI+ / EMBI Global Argentina (1998T1 - 2025T4). (L127)
- `empalmar_series_historicas()` — Ejecuta el empalme metodológico de las tres eras financieras: (L198)

### [`ingesta_bcra.py`](codigo/ingesta_datos/ingesta_bcra.py) — 🔗 conectado
> ingesta_bcra.py
- `fetch_datos_gob(series_id, label, collapse, agg)` — Descarga una serie desde apis.datos.gob.ar. (L85)
- `get_fallback(data_dict, label)` — Construye DataFrame desde diccionario de fallback. (L115)
- `main()` (L126)

### [`ingesta_bcra_pasivos.py`](codigo/ingesta_datos/ingesta_bcra_pasivos.py) — 🔗 conectado
> ingesta_bcra_pasivos.py
- `fetch_bcra_variable(id_variable, desde, hasta)` — Descarga la serie diaria completa de una variable BCRA (con paginación). (L66)
- `build_bcra_pasivos_diarios(desde, hasta)` — Combina LEBAC/NOBAC + LELIQ/NOTALIQ + posición neta de pases (diario). (L96)
- `fetch_pib_nominal(desde, hasta)` — PIB nominal trimestral (precios corrientes), con extrapolación explícita (L116)
- `main()` (L160)

### [`ingesta_datos_financieros.py`](codigo/ingesta_datos/ingesta_datos_financieros.py) — 🔗 conectado
> ingesta_datos_financieros.py
- `download_vix(start_date, end_date)` — Descarga el índice VIX desde Yahoo Finance y resamplea a trimestral. (L65)
- `fetch_embi_ambito()` — Intenta obtener EMBI+ desde la API pública de Ámbito Financiero. (L86)
- `fetch_embi_datos_gob()` — Intenta obtener EMBI+ desde la API de datos.gob.ar (BCRA/MECON). (L121)
- `get_embi_fallback()` — Retorna la serie histórica verificada del EMBI+ argentino (fallback). (L151)
- `download_embi()` — Orquesta la obtención del EMBI+ con cascada de fuentes. (L162)
- `main()` (L172)

### [`ingesta_instrumentos_1996_2025.py`](codigo/ingesta_datos/ingesta_instrumentos_1996_2025.py) — 🔗 conectado
> ingesta_instrumentos_1996_2025.py
- `download_vix()` (L44)
- `download_bovespa_vol()` (L57)
- `main()` (L73)

### [`ingesta_mecon_indec.py`](codigo/ingesta_datos/ingesta_mecon_indec.py) — 🔗 conectado
> ingesta_mecon_indec.py
- `fetch_datos_gob(series_id, label, collapse, agg)` (L132)
- `get_fallback(data_dict, label)` (L162)
- `compute_output_gap(pib_idx, lambda_hp)` — Calcula la brecha del producto con filtro HP (lambda=1600). (L172)
- `main()` (L185)

### [`ingesta_spread_regional.py`](codigo/ingesta_datos/ingesta_spread_regional.py) — 🔗 conectado
> ingesta_spread_regional.py
- `download_emb(start_date, end_date)` (L52)
- `main()` (L69)

### [`bai_perron.py`](codigo/modelos/bai_perron.py) — 🔗 conectado
> bai_perron.py
- `_ssr_table(y)` — Prefijos de y y de y^2 para computar SSR(i,j) de un ajuste de media (L39)
- `_optimal_partition(y, m, h)` — Partición óptima exacta de y en m+1 segmentos (m quiebres), con (L56)
- `bai_perron_breaks(series, max_breaks, trimming)` — Estima quiebres estructurales múltiples en la media de `series` (L108)

### [`dcc_garch.py`](codigo/modelos/dcc_garch.py) — 🔗 conectado
> dcc_garch.py
- `fit_univariate_garch(series)` — Ajusta un GARCH(1,1) univariado (media cero, t de Student) a una (L36)
- `_dcc_neg_loglik(params, Z)` (L46)
- `fit_dcc(Z, a0, b0)` — Estima (a, b) del DCC(1,1) por QML sobre la matriz de residuos (L68)
- `dcc_correlation_path(Z, a, b)` — Reconstruye la trayectoria completa R_1,...,R_T dado (a, b). (L81)

### [`fase10_dcc_garch.py`](codigo/modelos/fase10_dcc_garch.py) — 🔗 conectado
> fase10_dcc_garch.py
- `build_shocks(df)` (L57)
- `main()` (L66)

### [`fase11_dols_subperiodos.py`](codigo/modelos/fase11_dols_subperiodos.py) — 🔗 conectado
> fase11_dols_subperiodos.py
- `newey_west_lags(n)` — Lags de Newey-West segun m = 4*(T/100)^(2/9). (L40)
- `estimar_estatico(sub)` — MCO estatico pb_t = a + rho*d_{t-1} + gamma*y_gap + e_t, errores HAC. (L45)
- `estimar_dols(sub, m)` — DOLS con m adelantos y m rezagos de Delta d, errores HAC. (L59)
- `run(csv_path)` (L87)

### [`fase12_diagnosticos_complementarios.py`](codigo/modelos/fase12_diagnosticos_complementarios.py) — 🔗 conectado
> fase12_diagnosticos_complementarios.py
- `seleccionar_rezagos(df, maxlags)` — Orden de rezagos del VAR en niveles segun AIC, BIC(SC), HQ y FPE. (L39)
- `sensibilidad_johansen(df, ordenes)` — Rango de cointegracion estimado para cada orden de rezagos plausible. (L53)
- `diagnostico_multicolinealidad(df)` — VIF y numero de condicion de la ecuacion de reaccion fiscal. (L84)
- `run(csv_path)` (L122)

### [`fase13_robustez_hansen_dpb.py`](codigo/modelos/fase13_robustez_hansen_dpb.py) — 🔗 conectado
> H1 (optima) -- Re-correr el test de umbral de Hansen (2000) usando Delta pb_t

### [`fase14_dsa_tail_dependence.py`](codigo/modelos/fase14_dsa_tail_dependence.py) — 🔗 conectado
> H6 (optima) -- Robustez del DSA estocastico bajo shocks t marginales
- `simulate_path_from_shocks(shocks_5xN, alpha, d_initial, base_params, years)` (L35)

### [`fase15_sft_decomposicion_ilustrativa.py`](codigo/modelos/fase15_sft_decomposicion_ilustrativa.py) — 🔗 conectado
> H3 (optima) -- Descomposicion ilustrativa del Ajuste Stock-Flujo (SF_t) para
- `annual_d(year)` (L48)
- `annual_pb(year)` (L52)
- `annual_g_real(year)` (L55)

### [`fase16_vecm_dataset_ampliado.py`](codigo/modelos/fase16_vecm_dataset_ampliado.py) — 🔗 conectado
> fase16_vecm_dataset_ampliado.py
- `adf_test(series, signif)` (L50)
- `kpss_test(series, signif)` (L56)
- `analizar_estacionariedad(df, columns)` (L62)
- `tabla_orden_rezagos(df, maxlags)` (L90)
- `tabla_sensibilidad_lags(df, k_ar_diffs)` (L97)
- `tabla_sensibilidad_inicio_muestra(df_completo, k_ar_diff, fechas_inicio)` (L120)
- `main()` (L139)

### [`fase17_calibracion_nu_dsa.py`](codigo/modelos/fase17_calibracion_nu_dsa.py) — 🔗 conectado
> fase17_calibracion_nu_dsa.py
- `nu_mle_conjunto(serie)` — MLE conjunto (loc, scale, nu) vía scipy.stats.t.fit -método original-. (L44)
- `nu_metodo_momentos(serie)` — nu = 4 + 6/curtosis_exceso, válido para curtosis_exceso > 0 (nu>4). (L50)
- `main()` (L58)

### [`fase18_dummies_presidenciales.py`](codigo/modelos/fase18_dummies_presidenciales.py) — ⚠️ sin referencias externas encontradas
> fase18_dummies_presidenciales.py
- `newey_west_lags(n)` (L39)
- `construir_dummies_presidenciales(df)` (L42)
- `ejecutar_fase18(csv_path)` (L54)

### [`fase19_var_restringido_macro.py`](codigo/modelos/fase19_var_restringido_macro.py) — 🔗 conectado
> fase19_var_restringido_macro.py
- `cargar_datos()` (L55)
- `estimar_svar_restringido(data, nlags, n_boot, horizon)` (L70)
- `exportar_resultados(res)` (L229)

### [`fase1_estacionariedad.py`](codigo/modelos/fase1_estacionariedad.py) — 🔗 conectado
> fase1_estacionariedad.py
- `adf_test(series, signif)` — Test Augmented Dickey-Fuller. (L28)
- `kpss_test(series, signif)` — Test KPSS. (L35)
- `phillips_perron_test(series, signif)` — Test Phillips-Perron (intenta usar arch.unitroot si está disponible). (L42)
- `dfgls_test(series, trend)` — Test DF-GLS (Elliott, Rothenberg y Stock, 1996), vía arch.unitroot.DFGLS. (L53)
- `zivot_andrews_test(series, lags, trend, trim)` — Test de Zivot-Andrews (1992) con quiebre estructural endógeno, Modelo C (L66)
- `analyze_dfgls(df, columns)` — Aplica DF-GLS en nivel (tendencia+constante) y primera diferencia (L83)
- `analyze_stationarity(df, columns)` — Realiza análisis completo I(0) vs I(1) para las columnas dadas. (L113)
- `structural_break_cusum(df, col_y, col_x)` — Test CUSUM de residuos OLS para detectar inestabilidad estructural. (L150)
- *...y 1 funciones más*

### [`fase20_cir_embi_calibracion.py`](codigo/modelos/fase20_cir_embi_calibracion.py) — ⚠️ sin referencias externas encontradas
> fase20_cir_embi_calibracion.py
- `cargar_embi_series()` (L48)
- `fit_cir_mle(series, dt)` — Estima los parámetros de un proceso CIR vía MLE exacta con densidad de Bessel. (L62)
- `fit_cir_2factor(series, dt)` — Calibra el modelo CIR de 2 Factores (Transitorio global + Estructural local). (L135)
- `simular_dsa_cir(n_sims, horizon_anios)` — Simulación de Monte Carlo del DSA integrando el proceso CIR para la tasa externa. (L169)
- `main()` (L234)

### [`fase21_tvecm_hansen_seo.py`](codigo/modelos/fase21_tvecm_hansen_seo.py) — 🔗 conectado
> fase21_tvecm_hansen_seo.py
- `cargar_datos()` (L38)
- `estimar_tvecm(data, trimming, n_boot)` (L52)
- `main()` (L169)

### [`fase22_analisis_historico_1983_2025.py`](codigo/modelos/fase22_analisis_historico_1983_2025.py) — ⚠️ sin referencias externas encontradas
> FASE 22: ANALISIS ECONOMETRICO DEL SPREAD SOBERANO HISTORICO (1983-2025)
- `cargar_datos_historicos()` (L28)
- `estimar_quiebres_bai_perron(df, n_quiebres)` — Detección de quiebres estructurales múltiples mediante programación dinámica (Bai-Perron / Dynp). (L37)
- `cir_log_likelihood(params, r, dt)` — Log-verosimilitud negativa exacta del proceso CIR con densidad Chi-cuadrado no central. (L83)
- `calibrar_cir_historico(df)` — Calibra el modelo CIR sobre la muestra completa de 42 años (1983-2025). (L129)
- `estadisticas_por_regimen(df)` — Agrupa estadísticas descriptivas por administración presidencial. (L200)
- `main()` (L227)

### [`fase23_reestimacion_1996_2025.py`](codigo/modelos/fase23_reestimacion_1996_2025.py) — 🔗 conectado
> fase23_reestimacion_1996_2025.py
- `cargar_datos()` (L43)
- `main()` (L49)

### [`fase2_cointegracion.py`](codigo/modelos/fase2_cointegracion.py) — 🔗 conectado
> fase2_cointegracion.py
- `select_var_lags(df, maxlags)` — Selecciona el número óptimo de rezagos para el VAR usando AIC/BIC. (L23)
- `johansen_test(df, det_order, k_ar_diff)` — Realiza el test de cointegración de Johansen. (L32)
- `main()` (L63)

### [`fase3_reaccion_fiscal.py`](codigo/modelos/fase3_reaccion_fiscal.py) — 🔗 conectado
> fase3_reaccion_fiscal.py
- `newey_west_lags(n)` — Calcula lags óptimos de Newey-West según m = 4*(T/100)^(2/9). (L26)
- `select_dols_lags(df, y_col, x_cols, d_col, max_m)` — Selecciona el número de rezagos y adelantos (m) para DOLS (L30)
- `ejecutar_fase3_econometria(csv_path)` (L66)

### [`fase3b_reaccion_fiscal_vecm.py`](codigo/modelos/fase3b_reaccion_fiscal_vecm.py) — 🔗 conectado
> fase3b_reaccion_fiscal_vecm.py
- `seleccionar_rango_cointegracion(df, det_order, k_ar_diff, alpha)` — Determina el rango de cointegración r mediante el test de Johansen, (L36)
- `estimar_vecm(df, coint_vars, exog_vars, k_ar_diff, coint_rank)` — Estima el VECM con rango de cointegración impuesto (coint_rank) y (L56)
- `estimar_var_restringido_diferencias(df, coint_vars, exog_vars, k_ar_diff)` — Alternativa cuando NO hay cointegración: VAR restringido a primeras (L77)
- `main()` (L91)

### [`fase4_variables_instrumentales.py`](codigo/modelos/fase4_variables_instrumentales.py) — 🔗 conectado
> fase4_variables_instrumentales.py
- `ejecutar_fase4_econometria(csv_path)` (L48)

### [`fase5_umbral_hansen.py`](codigo/modelos/fase5_umbral_hansen.py) — 🔗 conectado
> fase5_umbral_hansen.py
- `bootstrap_threshold_test(df, y_col, X_control_cols, split_col, threshold_col)` — Test de significancia del umbral (Hansen 2000) mediante Bootstrap. (L24)
- `get_optimal_threshold(df, y_col, X_control_cols, split_col, threshold_col)` — Busca el umbral óptimo (tau) iterando entre el percentil 15 y 85 (L78)
- `ejecutar_fase5_econometria(csv_path)` (L127)

### [`fase6_sostenibilidad_deuda.py`](codigo/modelos/fase6_sostenibilidad_deuda.py) — 🔗 conectado
> fase6_sostenibilidad_deuda.py
- `_build_corr_from_svar(corr_rd_rf)` — Matriz de correlacion del DSA, orden [pb, g, r_d, r_f, delta_e], derivada (L67)
- `build_cov_matrix()` (L116)
- `simulate_dsa_path(alpha, d_initial, pb, g, r_d)` — Simula una trayectoria determinista de la deuda. (L119)
- `simulate_stochastic_dsa(alpha, d_initial, base_params, cov_matrix, years)` — Simula trayectorias estocásticas usando Monte Carlo. (L134)
- `main()` (L175)

### [`fase7_diagnosticos_robustez.py`](codigo/modelos/fase7_diagnosticos_robustez.py) — 🔗 conectado
> fase7_diagnosticos_robustez.py
- `newey_west_lags(n)` (L59)
- `build_dols(df, max_m)` (L63)
- `section_1_acf_pacf(df)` (L83)
- `section_2_arch(model)` (L125)
- `section_3_cusum(model_ols, y, X)` (L136)
- `section_4_engle_granger(df)` (L199)
- `section_5_subperiod_sensitivity(df)` (L212)
- `section_6_scenario_probabilities()` (L240)
- *...y 5 funciones más*

### [`fase8_deuda_consolidada.py`](codigo/modelos/fase8_deuda_consolidada.py) — 🔗 conectado
> fase8_deuda_consolidada.py
- `main()` (L47)

### [`fase9_bai_perron.py`](codigo/modelos/fase9_bai_perron.py) — 🔗 conectado
> fase9_bai_perron.py
- `analyze_series(df, col, label, max_breaks, trimming)` (L42)
- `main()` (L57)

