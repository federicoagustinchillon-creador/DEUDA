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
    "Datos_trimestrales": (D / "dataset_consolidado_1996_2025.csv", "Base trimestral auxiliar 1996-2025 con las marcas de lo reconstruido: es_interpolado (deuda, 6 trimestres), es_empalme_pib (32), es_empalme_embi (11) y es_interpolado_tcrm (4). Las series que entran al modelo estan en la hoja Datos_modelo"),
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


DESCR_MODELO = ("Series que entran a la especificacion principal, tal como las arma fase24 (cargar_datos): resultado "
                "primario sin rentas, crecimiento real (PIB INDEC base 1993 empalmado a base 2004), EMBI, TCRM, variacion "
                "de la tasa de la FED con las cuatro transiciones corregidas, VIX y deuda federal bruta rezagada; "
                "1998T2-2025T4 es la muestra de estimacion")


def datos_modelo() -> pd.DataFrame:
    """Datos de entrada de la especificacion principal, desde las mismas funciones que usa la estimacion."""
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import fase24_svarx_1996_2025 as f24  # noqa: E402
    Y, X, _ = f24.cargar_datos("federal", 2)
    cols = ["dFED_l0", "VIX", "deuda_l1"]
    df = Y.join(X[cols]).rename(columns={"pb_pib": "resultado_primario_pib", "crec": "crecimiento_real",
                                         "dFED_l0": "variacion_tasa_fed", "deuda_l1": "deuda_federal_bruta_pib_rezagada"})
    df.index = [f"{d.year}T{d.quarter}" for d in df.index]
    return df.rename_axis("trimestre").reset_index()


def main() -> None:
    salida = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SALIDA
    salida.parent.mkdir(parents=True, exist_ok=True)
    faltan = [str(p) for p, _ in HOJAS.values() if not p.exists()]
    if faltan:
        raise FileNotFoundError(f"Faltan archivos: {faltan}")
    modelo = datos_modelo()
    descr = {"Datos_modelo": DESCR_MODELO, **{h: d for h, (_, d) in HOJAS.items()}}
    with pd.ExcelWriter(salida) as w:
        pd.DataFrame({"Hoja": list(descr), "Contenido": list(descr.values())}).to_excel(w, sheet_name="Leeme", index=False)
        modelo.to_excel(w, sheet_name="Datos_modelo", index=False)
        for hoja, (ruta, _) in HOJAS.items():
            df = pd.read_csv(ruta)
            if hoja == "Datos_trimestrales":
                # columnas de versiones anteriores que no usa el modelo: se quitan para no confundirlas
                # (deuda_pib y pb_pib son series viejas; VIX esta incompleta; PIB_real de 1996-2003 no es el empalme del INDEC que usa
                # el modelo; g_gap y CER no intervienen)
                df = df.drop(columns=[c for c in ("deuda_pib", "pb_pib", "PIB_real", "VIX", "g_gap", "CER") if c in df.columns])
            df.to_excel(w, sheet_name=hoja[:31], index=False)
    print(f"[OK] {salida}")


if __name__ == "__main__":
    main()
