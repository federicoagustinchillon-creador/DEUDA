"""
exportar_excel_grupo.py
=======================
Arma el Excel "Datos y resultados" para el grupo con los datos de entrada del modelo y las tablas
de resultados de la especificacion principal y de la extension consolidada. Todo se lee de los
archivos del repositorio; la primera hoja describe cada hoja.

Uso: python codigo/modelos/exportar_excel_grupo.py [ruta_salida.xlsx]
"""

from __future__ import annotations

import pathlib
import sys

import pandas as pd

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
D = BASE / "datos"
R = BASE / "resultados" / "tablas"
SALIDA = BASE / "tesis_oficial_borradores" / "para_el_grupo" / "Datos_y_resultados.xlsx"

HOJAS: dict[str, tuple[pathlib.Path, str]] = {
    "Datos_trimestrales": (D / "dataset_consolidado_1996_2025.csv", "Base trimestral 1996-2025: EMBI, TCRM, PIB real y demas variables"),
    "Deuda": (D / "procesados" / "deuda_consolidada_neta_nominal_1996_2025.csv",
              "Deuda en % del PIB: bruta_federal_pib (principal) y deuda_consolidada_neta_nominal_pib (extension)"),
    "Resultado_primario": (D / "procesados" / "resultado_primario_1996_2025.csv",
                           "Resultado primario del SPN, % del PIB: con rentas (pb_pib) y sin rentas (pb_pib_sin_rentas)"),
    "Tasa_FED": (D / "procesados" / "tasa_fed_trimestral_1996_2025.csv", "Tasa de fondos federales y tasa sombra de Wu y Xia"),
    "Escenario_FMI": (D / "procesados" / "escenario_base_fmi_cr26105.csv", "Escenario base del FMI, Informe de Pais 26/105 (mayo de 2026), cuadros 6 y 7"),
    "Rezagos": (R / "fase24_federal_rezagos.csv", "Criterios de informacion, estabilidad y Portmanteau por orden del VAR"),
    "Diagnosticos": (R / "fase24_federal_diagnosticos.csv", "Diagnosticos de los residuos de la especificacion principal"),
    "Estimacion_intervalos": (R / "fase24_federal_bootstrap.csv", "Reaccion fiscal, efectos de la deuda y respuestas a la FED con intervalos de Hall al 90%"),
    "Impacto_S": (R / "fase24_federal_S.csv", "Matriz de impacto estructural"),
    "Simulacion_principal": (R / "fase25_federal_resumen.csv", "Probabilidades, efectos de la FED y varianza por bloque (estimacion e intervalo de Hall al 90%)"),
    "Abanico_principal": (R / "fase25_federal_fanchart.csv", "Percentiles de la deuda federal bruta simulada 2025-2035"),
    "Suficiencia": (R / "fase25_federal_suficiencia.csv", "Probabilidad de no estabilizacion segun el resultado primario (complemento de H1a)"),
    "Simulacion_consolidada": (R / "fase25_consolidada_resumen.csv", "Extension: deuda consolidada con el BCRA"),
    "Estilo_FMI": (R / "fase25_federal_fmi_resumen.csv", "Abanico con el procedimiento de shocks del FMI sobre la historia argentina"),
}


def main() -> None:
    salida = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SALIDA
    salida.parent.mkdir(parents=True, exist_ok=True)
    faltan = [str(p) for p, _ in HOJAS.values() if not p.exists()]
    if faltan:
        raise FileNotFoundError(f"Faltan archivos: {faltan}")
    with pd.ExcelWriter(salida) as w:
        pd.DataFrame({"Hoja": list(HOJAS), "Contenido": [d for _, d in HOJAS.values()]}).to_excel(w, sheet_name="Leeme", index=False)
        for hoja, (ruta, _) in HOJAS.items():
            pd.read_csv(ruta).to_excel(w, sheet_name=hoja[:31], index=False)
    print(f"[OK] {salida}")


if __name__ == "__main__":
    main()
