"""
fase7_diagnosticos_robustez.py
==========================
Diagnosticos adicionales solicitados por la auditoria academica externa,
computados sobre el proceso empírico real (no fabricados):

  1. ACF/PACF de las 4 series nucleo (pb_pib, deuda_pib, EMBI, g_gap).
  2. Test ARCH-LM (heterocedasticidad condicional) sobre los residuos del DOLS.
  3. CUSUM y CUSUMSQ (estabilidad estructural del DOLS, residuos recursivos).
  4. Test de cointegracion residual Engle-Granger (deuda_pib <-> pb_pib),
     como robustez complementaria en el mismo espiritu que Phillips-Ouliaris
     (ambos son tests de cointegracion de ecuacion unica basados en residuos;
     statsmodels no implementa Phillips-Ouliaris de forma nativa, por lo que
     se reporta Engle-Granger y se lo declara honestamente como tal).
  5. Sensibilidad temporal: reestimacion de la funcion de reaccion fiscal
     (MCO-HAC) en dos submuestras de igual tamano (2004-2014 vs 2015-2025).
  6. Probabilidad de insolvencia (Monte Carlo) por escenario (Optimista,
     Referencia, Estres), no solo bajo el escenario de Referencia.
  7. Causalidad de Granger (EMBI+ <-> Delta Resultado Primario), ambas
     direcciones, como evidencia complementaria y barata sobre la endogeneidad
     que motiva la Seccion 6.4 (IV-2SLS).
  8. Filtro de Hamilton (2018) como robustez del filtro HP (lambda=1600)
     usado para la brecha del producto (Cap. 5), comparando ambos ciclos.
  9. Covarianza del DSA: reemplazo parcial de la calibracion a ojo por
     GARCH(1,1) para las variables con serie real disponible (pb, g,
     delta_e); r_d y r_f permanecen calibrados por falta de serie propia.

Todos los resultados se guardan en resultados/tablas/ para trazabilidad.
"""

import os
import sys
import pathlib
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import recursive_olsresiduals, het_arch
from statsmodels.tsa.stattools import coint, grangercausalitytests
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fase6_sostenibilidad_deuda import (
    simulate_stochastic_dsa, SCENARIOS, ALPHA, D_INITIAL, DSA_STUDENT_T_NU, build_cov_matrix,
    STD_DEVS, CORR,
)
from arch import arch_model

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
CSV_PATH = BASE_DIR / "datos" / "dataset_consolidado_real.csv"
LATEX_DIR = BASE_DIR / "tesis" / "figuras"
TABLES_DIR = BASE_DIR / "resultados" / "tablas"
os.makedirs(TABLES_DIR, exist_ok=True)


def newey_west_lags(n):
    return int(np.ceil(4 * (n / 100) ** (2 / 9)))


def build_dols(df, max_m=4):
    df = df.copy()
    df['d_t_1'] = df['deuda_pib'].shift(1)
    df = df.dropna(subset=['pb_pib', 'd_t_1', 'g_gap'])
    df['diff_d'] = df['d_t_1'].diff()
    dols_features = ['d_t_1', 'g_gap', 'diff_d']
    for i in range(1, max_m + 1):
        df[f'diff_d_lag_{i}'] = df['diff_d'].shift(i)
        df[f'diff_d_lead_{i}'] = df['diff_d'].shift(-i)
        dols_features.extend([f'diff_d_lag_{i}', f'diff_d_lead_{i}'])
    df = df.dropna(subset=['pb_pib'] + dols_features)
    y = df['pb_pib']
    X = sm.add_constant(df[dols_features])
    n = len(df)
    hac_lags = newey_west_lags(n)
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': hac_lags})
    model_ols = sm.OLS(y, X).fit()  # sin HAC, necesario para residuos recursivos
    return df, y, X, model, model_ols


def section_1_acf_pacf(df):
    print("\n[1/9] ACF/PACF de las 4 series nucleo...")
    series = {
        'Resultado Primario / PIB ($pb_t$)': df['pb_pib'],
        'Deuda Publica / PIB ($d_t$)': df['deuda_pib'],
        'Riesgo Pais - EMBI+ ($risk_t$)': df['EMBI'],
        'Brecha del Producto ($\\tilde{y}_t$)': df['g_gap'],
    }
    fig, axes = plt.subplots(4, 2, figsize=(10, 14))
    for i, (name, s) in enumerate(series.items()):
        s = s.dropna()
        plot_acf(s, ax=axes[i, 0], lags=20, title=f'ACF: {name}')
        plot_pacf(s, ax=axes[i, 1], lags=20, method='ywm', title=f'PACF: {name}')
    plt.tight_layout()
    out_path = LATEX_DIR / 'figura_5_5_acf_pacf.png'
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f" -> Guardado: {out_path}")


def section_2_arch(model):
    print("\n[2/9] Test ARCH-LM sobre residuos del DOLS...")
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_arch(model.resid, nlags=4)
    print(f" -> LM stat = {lm_stat:.4f}, p-valor = {lm_pvalue:.4f}")
    pd.DataFrame([{
        'lm_stat': lm_stat, 'lm_pvalue': lm_pvalue,
        'f_stat': f_stat, 'f_pvalue': f_pvalue
    }]).to_csv(TABLES_DIR / 'fase7_test_arch.csv', index=False)
    return lm_stat, lm_pvalue, f_stat, f_pvalue


def section_3_cusum(model_ols, y, X):
    print("\n[3/9] CUSUM / CUSUMSQ (residuos recursivos)...")
    (rresid, rparams, rypred, rresid_standardized, rresid_scaled,
     rcusum, rcusumci) = recursive_olsresiduals(model_ols, skip=None, alpha=0.95)

    n_r = len(rcusum)
    n_ci = rcusumci.shape[1]
    idx = np.arange(1, n_r + 1)
    idx_ci = np.arange(n_r - n_ci + 1, n_r + 1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(idx, rcusum, color='#0B3C5D', label='CUSUM')
    axes[0].axhline(0, color='black', linewidth=0.8)
    axes[0].plot(idx_ci, rcusumci[0, :], 'r--', linewidth=1, label='Banda 95%')
    axes[0].plot(idx_ci, rcusumci[1, :], 'r--', linewidth=1)
    axes[0].set_title('CUSUM (Estabilidad Estructural, DOLS)')
    axes[0].set_xlabel('Observación recursiva')
    axes[0].legend(fontsize=8)

    rresid_scaled_aligned = rresid_scaled[-n_r:]
    cusumsq = np.cumsum(rresid_scaled_aligned ** 2) / np.sum(rresid_scaled_aligned ** 2)
    frac = np.arange(1, n_r + 1) / n_r
    c95 = 0.5959  # límite aproximado al 5% (Harvey, 1990) para muestras moderadas
    axes[1].plot(idx, cusumsq, color='#0B3C5D', label='CUSUMSQ')
    axes[1].plot(idx, np.clip(frac + c95, 0, 1.3), 'r--', linewidth=1, label='Banda 95%')
    axes[1].plot(idx, np.clip(frac - c95, -0.3, 1), 'r--', linewidth=1)
    axes[1].set_title('CUSUMSQ (Estabilidad Estructural, DOLS)')
    axes[1].set_xlabel('Observación recursiva')
    axes[1].legend(fontsize=8)

    plt.tight_layout()
    out_path = LATEX_DIR / 'figura_6_2_cusum.png'
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f" -> Guardado: {out_path}")

    cusum_ci_matched = rcusum[-n_ci:]
    exceeds_cusum = np.any((cusum_ci_matched < rcusumci[0, :]) | (cusum_ci_matched > rcusumci[1, :]))
    stable_cusum = not exceeds_cusum
    max_cusumsq_dev = np.max(np.abs(cusumsq - frac))
    stable_cusumsq = max_cusumsq_dev < c95

    print(f" -> CUSUM se mantiene dentro de bandas al 95%: {stable_cusum}")
    print(f" -> CUSUMSQ desviación máxima = {max_cusumsq_dev:.4f} (límite 5% = {c95}) -> estable: {stable_cusumsq}")

    pd.DataFrame([{
        'stable_cusum': stable_cusum,
        'max_cusumsq_deviation': max_cusumsq_dev,
        'cusumsq_boundary_5pct': c95,
        'stable_cusumsq': stable_cusumsq
    }]).to_csv(TABLES_DIR / 'fase7_cusum.csv', index=False)
    return stable_cusum, stable_cusumsq, max_cusumsq_dev


def section_4_engle_granger(df):
    print("\n[4/9] Test de cointegracion residual Engle-Granger (deuda_pib <-> pb_pib)...")
    d = df.dropna(subset=['deuda_pib', 'pb_pib'])
    eg_stat, eg_pvalue, eg_crit = coint(d['deuda_pib'], d['pb_pib'], trend='c')
    print(f" -> Estadistico = {eg_stat:.4f}, p-valor = {eg_pvalue:.4f}")
    print(f" -> Valores criticos (1%,5%,10%) = {eg_crit}")
    pd.DataFrame([{
        'eg_stat': eg_stat, 'eg_pvalue': eg_pvalue,
        'crit_1pct': eg_crit[0], 'crit_5pct': eg_crit[1], 'crit_10pct': eg_crit[2]
    }]).to_csv(TABLES_DIR / 'fase7_engle_granger.csv', index=False)
    return eg_stat, eg_pvalue, eg_crit


def section_5_subperiod_sensitivity(df):
    print("\n[5/9] Sensibilidad temporal: submuestras 2004-2014 vs 2015-2025...")
    df = df.copy()
    df['d_t_1'] = df['deuda_pib'].shift(1)
    df = df.dropna(subset=['pb_pib', 'd_t_1', 'g_gap'])

    sub1 = df[df.index <= '2014-12-31']
    sub2 = df[df.index >= '2015-01-01']

    results = {}
    for label, sub in [('2004-2014', sub1), ('2015-2025', sub2)]:
        y = sub['pb_pib']
        X = sm.add_constant(sub[['d_t_1', 'g_gap']])
        hac_lags = newey_west_lags(len(sub))
        m = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': hac_lags})
        results[label] = {
            'n': len(sub),
            'rho': m.params['d_t_1'],
            'se': m.bse['d_t_1'],
            'p': m.pvalues['d_t_1'],
            'r2': m.rsquared
        }
        print(f" -> {label} (n={len(sub)}): rho={m.params['d_t_1']:.4f} (p={m.pvalues['d_t_1']:.4f})")

    pd.DataFrame(results).T.to_csv(TABLES_DIR / 'fase7_sensibilidad_subperiodos.csv')
    return results


def section_6_scenario_probabilities():
    print("\n[6/9] Probabilidad de insolvencia (Monte Carlo) por escenario...")
    print("      (reutilizando simulate_stochastic_dsa, SCENARIOS y build_cov_matrix de fase6_sostenibilidad_deuda.py)")
    years = np.arange(2026, 2036)
    cov_matrix = build_cov_matrix()

    rows = []
    for name, params in SCENARIOS.items():
        d_paths = simulate_stochastic_dsa(ALPHA, D_INITIAL, params, cov_matrix, years, DSA_STUDENT_T_NU, n_simulations=1000)
        prob_100 = np.mean(d_paths[:, -1] > 1.0) * 100
        median_2035 = np.median(d_paths[:, -1]) * 100
        print(f" -> {name}: P(deuda/PIB > 100% en 2035) = {prob_100:.1f}% (mediana={median_2035:.1f}%)")
        rows.append({'escenario': name, 'prob_excede_100pct_2035': prob_100, 'mediana_2035': median_2035})

    pd.DataFrame(rows).to_csv(TABLES_DIR / 'fase7_probabilidades_escenarios.csv', index=False)
    return rows


def section_7_granger_causality(df, maxlag=4):
    """
    Causalidad de Granger EMBI+ <-> Resultado Primario, en ambas direcciones.
    EMBI (risk_t) es I(0) (Tabla 5.6); pb_pib es I(1) (misma tabla), por lo
    que se usa Delta pb_pib (estacionaria) junto al EMBI+ en niveles, evitando
    una regresion espuria sin necesitar el aparato completo de un VECM.
    """
    print("\n[7/9] Causalidad de Granger (EMBI+ <-> Resultado Primario)...")
    d = df.copy()
    d['d_pb'] = d['pb_pib'].diff()
    d = d.dropna(subset=['d_pb', 'EMBI'])

    rows = []
    # Direccion 1: EMBI+ ayuda a predecir Delta pb_pib?
    data_1 = d[['d_pb', 'EMBI']].values
    res_1 = grangercausalitytests(data_1, maxlag=maxlag, verbose=False)
    # Direccion 2: Delta pb_pib ayuda a predecir EMBI+?
    data_2 = d[['EMBI', 'd_pb']].values
    res_2 = grangercausalitytests(data_2, maxlag=maxlag, verbose=False)

    for lag in range(1, maxlag + 1):
        f_1, p_1 = res_1[lag][0]['ssr_ftest'][0], res_1[lag][0]['ssr_ftest'][1]
        f_2, p_2 = res_2[lag][0]['ssr_ftest'][0], res_2[lag][0]['ssr_ftest'][1]
        rows.append({
            'rezagos': lag,
            'F_EMBI_causa_dpb': f_1, 'p_EMBI_causa_dpb': p_1,
            'F_dpb_causa_EMBI': f_2, 'p_dpb_causa_EMBI': p_2,
        })
        print(f" -> Rezagos={lag}: EMBI+ -> Dpb (F={f_1:.3f}, p={p_1:.4f}) | "
              f"Dpb -> EMBI+ (F={f_2:.3f}, p={p_2:.4f})")

    pd.DataFrame(rows).to_csv(TABLES_DIR / 'fase7_causalidad_granger.csv', index=False)
    return rows


def section_8_hamilton_filter(df, h=8, p=4):
    """
    Filtro de Hamilton (2018) como robustez del filtro HP (lambda=1600, Cap. 5).
    Especificacion recomendada por el propio Hamilton para datos trimestrales:
    regresion de y_{t+h} sobre una constante y 4 rezagos de y_t (h=8, p=4).
    El residuo de esa regresion es el componente ciclico (analogo a g_gap).
    """
    print("\n[8/9] Filtro de Hamilton (2018) como robustez del HP (lambda=1600)...")
    y = np.log(df['PIB_real']).dropna()
    n = len(y)

    X_cols = {f'y_lag{h + i}': y.shift(h + i) for i in range(p)}
    reg_df = pd.DataFrame(X_cols)
    reg_df['y'] = y
    reg_df = reg_df.dropna()

    X = sm.add_constant(reg_df[list(X_cols.keys())])
    model = sm.OLS(reg_df['y'], X).fit()
    cycle_hamilton = model.resid * 100  # en % de desvio, comparable a g_gap

    comp = pd.DataFrame({'g_gap_HP': df['g_gap'], 'ciclo_Hamilton': cycle_hamilton}).dropna()
    corr = comp['g_gap_HP'].corr(comp['ciclo_Hamilton'])
    print(f" -> n valido tras rezagos h={h}+p={p}: {len(comp)} de {n} observaciones")
    print(f" -> Correlacion entre brecha HP (lambda=1600) y ciclo de Hamilton: r={corr:.4f}")

    comp.to_csv(TABLES_DIR / 'fase7_filtro_hamilton.csv')
    return comp, corr


def _garch_annual_std(series, annualize=True):
    """Ajusta un GARCH(1,1) a una serie (en % para estabilidad numerica) y
    devuelve la volatilidad condicional promedio. Si annualize=True, escala
    por sqrt(4) asumiendo que la serie es de innovaciones trimestrales sin
    componente estacional (varianza aditiva bajo shocks no correlacionados);
    si la serie ya es interanual (YoY), se deja sin reescalar."""
    s = series.dropna() * 100
    am = arch_model(s, mean='Zero', vol='GARCH', p=1, q=1, dist='normal')
    res = am.fit(disp='off')
    avg_cond_vol = np.sqrt(res.conditional_volatility ** 2).mean() / 100
    return avg_cond_vol * np.sqrt(4) if annualize else avg_cond_vol


def section_9_garch_dsa_covariance(df):
    """
    Reemplaza, para las variables con serie historica real disponible en el
    dataset (pb, g, delta_e), la volatilidad calibrada a ojo de
    fase6_sostenibilidad_deuda.py por una volatilidad estimada mediante
    GARCH(1,1). r_d y r_f (tasas de interes domestica y externa) no tienen
    serie propia en el dataset consolidado -> se mantienen calibradas, de
    forma explicita, y la matriz de correlacion tampoco se re-estima (exigiria
    las 5 series reales). Es una mejora parcial y honesta, no una
    re-estimacion completa del proceso estocastico del DSA.
    """
    print("\n[9/9] Covarianza del DSA: reemplazo parcial de la calibracion por GARCH(1,1)...")
    d = df.copy()
    pb_shock = d['pb_pib'].diff() / 100           # decimal, primera diferencia (pb_pib es I(1))
    delta_e_shock = d['TCRM'].pct_change()        # decimal, variacion trimestral del TCRM (sin estacionalidad marcada)
    # PIB_real tiene estacionalidad marcada por trimestre (verificado: media Q2 muy
    # por encima de Q1/Q3/Q4), por lo que la variacion trimestral simple confundiria
    # estacionalidad con volatilidad. Se usa crecimiento interanual (YoY, 4 rezagos),
    # que cancela el componente estacional y ya es directamente una tasa anual.
    g_shock = d['PIB_real'].pct_change(4)

    std_pb = _garch_annual_std(pb_shock)
    std_g = _garch_annual_std(g_shock, annualize=False)
    std_delta_e = _garch_annual_std(delta_e_shock)

    std_devs_garch = STD_DEVS.copy()
    std_devs_garch[0] = std_pb        # pb: calibrado 0.015 -> GARCH
    std_devs_garch[1] = std_g         # g: calibrado 0.040 -> GARCH
    std_devs_garch[4] = std_delta_e   # delta_e: calibrado 0.150 -> GARCH
    # r_d (idx 2) y r_f (idx 3): se mantienen calibrados, sin serie real disponible.

    print(f" -> Desvios calibrados originales : pb={STD_DEVS[0]:.4f}  g={STD_DEVS[1]:.4f}  delta_e={STD_DEVS[4]:.4f}")
    print(f" -> Desvios GARCH(1,1) anualizados : pb={std_pb:.4f}  g={std_g:.4f}  delta_e={std_delta_e:.4f}")
    print(" -> r_d y r_f permanecen calibrados (sin serie historica propia en el dataset).")

    cov_garch = np.outer(std_devs_garch, std_devs_garch) * CORR

    years = np.arange(2026, 2036)
    rows = []
    for name, params in SCENARIOS.items():
        d_paths_orig = simulate_stochastic_dsa(ALPHA, D_INITIAL, params, build_cov_matrix(), years, DSA_STUDENT_T_NU, n_simulations=1000)
        d_paths_garch = simulate_stochastic_dsa(ALPHA, D_INITIAL, params, cov_garch, years, DSA_STUDENT_T_NU, n_simulations=1000)
        prob_orig = np.mean(d_paths_orig[:, -1] > 1.0) * 100
        prob_garch = np.mean(d_paths_garch[:, -1] > 1.0) * 100
        print(f" -> {name}: P(>100% PIB, 2035) calibrado={prob_orig:.1f}%  vs.  GARCH-parcial={prob_garch:.1f}%")
        rows.append({'escenario': name, 'prob_calibrado': prob_orig, 'prob_garch_parcial': prob_garch})

    out = pd.DataFrame(rows)
    out.to_csv(TABLES_DIR / 'fase7_garch_comparacion_dsa.csv', index=False)
    pd.DataFrame([{
        'std_pb_calibrado': STD_DEVS[0], 'std_pb_garch': std_pb,
        'std_g_calibrado': STD_DEVS[1], 'std_g_garch': std_g,
        'std_delta_e_calibrado': STD_DEVS[4], 'std_delta_e_garch': std_delta_e,
    }]).to_csv(TABLES_DIR / 'fase7_garch_desvios.csv', index=False)
    return out


def main():
    print("=" * 75)
    print(" EXTENSIONES DE DIAGNOSTICO - AUDITORIA ACADEMICA EXTERNA ")
    print("=" * 75)
    df = pd.read_csv(CSV_PATH, parse_dates=['Date'], index_col='Date')

    section_1_acf_pacf(df)

    df_dols, y, X, model_hac, model_ols = build_dols(df, max_m=4)
    section_2_arch(model_hac)
    section_3_cusum(model_ols, y, X)
    section_4_engle_granger(df)
    section_5_subperiod_sensitivity(df)
    section_6_scenario_probabilities()
    section_7_granger_causality(df)
    section_8_hamilton_filter(df)
    section_9_garch_dsa_covariance(df)

    print("\n[OK] Todos los diagnosticos guardados en resultados/tablas/ y tesis/figuras/.")


if __name__ == '__main__':
    main()
