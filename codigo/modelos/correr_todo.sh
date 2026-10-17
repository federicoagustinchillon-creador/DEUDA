#!/usr/bin/env bash
# Corre la estimacion (fase24), la simulacion principal y todas las variantes de robustez
# (fase25), y el diagnostico del abanico a la manera del FMI (fase25b). Deja un registro por
# corrida en resultados/registros/. Uso: bash codigo/modelos/correr_todo.sh
set -u
cd "$(dirname "$0")/../.."
R=resultados/registros
mkdir -p "$R"
M=codigo/modelos

correr() {  # nombre, comando...
    local nombre=$1; shift
    echo "[$(date +%H:%M:%S)] $nombre"
    "$@" > "$R/$nombre.log" 2>&1 || echo "  FALLO $nombre (ver $R/$nombre.log)"
}

correr empalmes python codigo/ingesta_datos/empalme_embi_tcrm_1996_1998.py
correr f24_federal python $M/fase24_svarx_1996_2025.py --deuda federal
correr f24_consolidada python $M/fase24_svarx_1996_2025.py --deuda consolidada
correr f24b_propiedades python $M/fase24b_propiedades_series.py

S="python $M/fase25_simulacion_dsa_svarx.py"
correr f25_federal $S --suficiencia
correr f25_consolidada $S --deuda consolidada --suficiencia
correr f25_pb_alt $S --pb-alternativa
correr f25_dom $S --canal-domestico
correr f25_sin_retro $S --sin-retroalimentacion
correr f25_p1 $S --p 1
correr f25_p3 $S --p 3
correr f25_chol $S --identificacion cholesky_fiscal_primero
correr f25_chol_ultimo $S --identificacion cholesky_fiscal_ultimo
correr f25_alfa0 $S --alpha-y 0
correr f25_alfa05 $S --alpha-y 0.5
correr f25_sin_default $S --sin-default
correr f25_desde1999 $S --desde 1999-01-01
correr f25_desde2004 $S --desde 2004-01-01
correr f25_sin_quiebres $S --sin-quiebres
correr f25_sf0 $S --sf-cero
correr f25_lam015 $S --lam 0.15
correr f25_lam040 $S --lam 0.40
correr f25_cr2595 $S --escenario cr2595
correr f25_kilian $S --kilian
correr f25_fmi_federal $S --shocks fmi
correr f25_fmi_consolidada $S --shocks fmi --deuda consolidada
correr f25b_diagnostico python $M/fase25b_diagnostico_abanico_fmi.py
correr figuras python $M/figuras_tesis.py
correr apendice python $M/apendice_tablas.py
correr hoja_de_numeros python $M/hoja_de_numeros.py
correr excel python $M/exportar_excel_grupo.py
correr pruebas python -m pytest tests -q
echo "[$(date +%H:%M:%S)] fin"
