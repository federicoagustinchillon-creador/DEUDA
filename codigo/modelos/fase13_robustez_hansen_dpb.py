"""
H1 (optima) -- Re-correr el test de umbral de Hansen (2000) usando Delta pb_t
(primera diferencia del resultado primario, I(0) segun DF-GLS) como variable
dependiente, en lugar de pb_t en niveles (I(1)). Replica exactamente la logica
de codigo/modelos/fase5_umbral_hansen.py, cambiando solo y_col.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fase5_umbral_hansen import get_optimal_threshold, bootstrap_threshold_test

_base_dir = pathlib.Path(__file__).parent.parent.parent
csv_path = _base_dir / "datos" / "dataset_consolidado_real.csv"
df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')

df['d_t_1'] = df['deuda_pib'].shift(1)
df['dpb_pib'] = df['pb_pib'].diff()

subset_cols = ['dpb_pib', 'd_t_1', 'g_gap', 'EMBI']
df = df.dropna(subset=subset_cols).copy()
print(f"Observaciones validas (tras diferenciar pb_t): {len(df)}")

best_tau, best_model = get_optimal_threshold(
    df=df, y_col='dpb_pib', X_control_cols=['g_gap'],
    split_col='d_t_1', threshold_col='EMBI'
)
print(f"Umbral optimo (tau*): {best_tau:.1f} pb de EMBI+")

f_obs, p_val_boot = bootstrap_threshold_test(
    df=df, y_col='dpb_pib', X_control_cols=['g_gap'],
    split_col='d_t_1', threshold_col='EMBI', best_tau=best_tau, n_boot=1000
)
print(f"F-stat observado: {f_obs:.4f}")
print(f"p-value bootstrap (1000 iter): {p_val_boot:.4f}")
print()
print(best_model.summary().tables[1])

# Persistencia a CSV para trazabilidad (mismo criterio que el resto de las
# fases: todo resultado intermedio citado en la tesis debe quedar en
# resultados/tablas/, no solo impreso por consola).
tabla_coef = pd.DataFrame({
    "variable": best_model.params.index,
    "coeficiente": best_model.params.values,
    "error_estandar": best_model.bse.values,
    "estadistico_z": best_model.tvalues.values,
    "p_valor": best_model.pvalues.values,
})
tabla_coef.to_csv("resultados/tablas/fase13_hansen_dpb_coeficientes.csv", index=False)

tabla_resumen = pd.DataFrame([{
    "tau_optimo_pb": best_tau,
    "f_stat_observado": f_obs,
    "p_valor_bootstrap": p_val_boot,
    "n_bootstrap": 1000,
    "n_obs": len(df),
}])
tabla_resumen.to_csv("resultados/tablas/fase13_hansen_dpb_resumen.csv", index=False)
print("\nGuardado: resultados/tablas/fase13_hansen_dpb_coeficientes.csv, fase13_hansen_dpb_resumen.csv")
