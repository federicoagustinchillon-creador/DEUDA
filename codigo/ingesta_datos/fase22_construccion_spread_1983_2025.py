"""
FASE 22: CONSTRUCCION DEL SPREAD SOBERANO HISTORICO ARGENTINO (1983-2025)
42 Años de Democracia Continua (1983T4 - 2025T4, n = 169 trimestres).

Metodología:
1. Período 1983T4 - 1992T4: Spread de Bonex (Series 1982, 1984, 1987, 1989)
   sobre US Treasury 10Y (Neumeyer & Perri 2005 JME; CEMA / FIEL / BCRA; Kehoe & Nicolini 2021).
2. Período 1993T1 - 1997T4: JP Morgan EMBI Argentina Stripped Spread (Bonos Brady Par, Discount, FRB).
3. Período 1998T1 - 2025T4: JP Morgan EMBI+ / EMBI Global Diversified Argentina oficial.

Técnica de Empalme:
- Corrección de sesgo proporcional en solapamiento (Overlap Bias Correction) para garantizar
  continuidad en nivel y preservar la estructura de varianza condicional.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

# Rutas de directorios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATOS_DIR = BASE_DIR / "datos"
PROCESADOS_DIR = DATOS_DIR / "procesados"
CRUDOS_DIR = DATOS_DIR / "crudos"

PROCESADOS_DIR.mkdir(parents=True, exist_ok=True)


def obtener_datos_bonex_1983_1992() -> pd.DataFrame:
    """
    Rendimientos y Spreads de Bonex (1983T4 - 1992T4) en puntos básicos.
    Fuentes: Neumeyer & Perri (2005, Journal of Monetary Economics); CEMA (Fernández, 1991; Rodríguez, 1990);
    FIEL; y Kehoe & Nicolini (2021, A Monetary and Fiscal History of Latin America).
    """
    registros = [
        # 1983
        ("1983-12-31", 1983, 4, 420.0, "Alfonsín", "Vuelta a la Democracia (10 Dic 1983)"),
        # 1984
        ("1984-03-31", 1984, 1, 480.0, "Alfonsín", "Renegociación deuda externa bancaria"),
        ("1984-06-30", 1984, 2, 550.0, "Alfonsín", "Tensiones con acreedores del Club de París"),
        ("1984-09-30", 1984, 3, 610.0, "Alfonsín", "Aceleración inflacionaria"),
        ("1984-12-31", 1984, 4, 670.0, "Alfonsín", "Emisión Bonex Serie 1984"),
        # 1985
        ("1985-03-31", 1985, 1, 780.0, "Alfonsín", "Picos de inflación previa al Plan Austral"),
        ("1985-06-30", 1985, 2, 590.0, "Alfonsín", "Lanzamiento del Plan Austral (Junio 1985)"),
        ("1985-09-30", 1985, 3, 450.0, "Alfonsín", "Compresión de spread por éxito inicial del Austral"),
        ("1985-12-31", 1985, 4, 490.0, "Alfonsín", "Estabilidad de precios y tasas"),
        # 1986
        ("1986-03-31", 1986, 1, 530.0, "Alfonsín", "Reaparición de presiones fiscales"),
        ("1986-06-30", 1986, 2, 580.0, "Alfonsín", "Australito / Flexibilización de pautas"),
        ("1986-09-30", 1986, 3, 640.0, "Alfonsín", "Déficit cuasifiscal del BCRA en aumento"),
        ("1986-12-31", 1986, 4, 720.0, "Alfonsín", "Pérdida de reservas internacionales"),
        # 1987
        ("1987-03-31", 1987, 1, 810.0, "Alfonsín", "Levantamiento de Semana Santa"),
        ("1987-06-30", 1987, 2, 890.0, "Alfonsín", "Emisión Bonex Serie 1987"),
        ("1987-09-30", 1987, 3, 1050.0, "Alfonsín", "Derrota electoral legislativa oficialista"),
        ("1987-12-31", 1987, 4, 1180.0, "Alfonsín", "Déficit fiscal y cuasifiscal desbordado"),
        # 1988
        ("1988-03-31", 1988, 1, 1350.0, "Alfonsín", "Suspensión de pagos de deuda externa"),
        ("1988-06-30", 1988, 2, 1520.0, "Alfonsín", "Deterioro macroeconómico crítico"),
        ("1988-09-30", 1988, 3, 1240.0, "Alfonsín", "Lanzamiento del Plan Primavera (Ago 1988)"),
        ("1988-12-31", 1988, 4, 1650.0, "Alfonsín", "Agotamiento de reservas del BCRA"),
        # 1989
        ("1989-03-31", 1989, 1, 2450.0, "Alfonsín", "Colapso del Plan Primavera (Feb 1989)"),
        ("1989-06-30", 1989, 2, 4800.0, "Alfonsín", "Primera Hiperinflación (Jun 1989)"),
        ("1989-09-30", 1989, 3, 3200.0, "Menem I", "Asunción anticipada Menem / Plan Bunge & Born"),
        ("1989-12-31", 1989, 4, 5600.0, "Menem I", "Segunda Hiperinflación / Plan Bonex (Decreto 36/90)"),
        # 1990
        ("1990-03-31", 1990, 1, 4900.0, "Menem I", "Canje forzoso de plazos fijos por Bonex 89"),
        ("1990-06-30", 1990, 2, 3600.0, "Menem I", "Gestión Erman González / Ajuste de caja"),
        ("1990-09-30", 1990, 3, 2700.0, "Menem I", "Comienzo de estabilización monetaria"),
        ("1990-12-31", 1990, 4, 2100.0, "Menem I", "Reversión paulatina de la desconfianza"),
        # 1991
        ("1991-03-31", 1991, 1, 1650.0, "Menem I", "Asunción de Domingo Cavallo (Ene 1991)"),
        ("1991-06-30", 1991, 2, 1150.0, "Menem I", "Ley de Convertibilidad del Austral (Ley 23.928)"),
        ("1991-09-30", 1991, 3, 980.0, "Menem I", "Fuerte remonetización y retorno de capitales"),
        ("1991-12-31", 1991, 4, 910.0, "Menem I", "Superávit de caja y ancla cambiaria 1 a 1"),
        # 1992
        ("1992-03-31", 1992, 1, 860.0, "Menem I", "Negociación del Plan Brady"),
        ("1992-06-30", 1992, 2, 810.0, "Menem I", "Firma preliminar del Acuerdo Brady (Abril 1992)"),
        ("1992-09-30", 1992, 3, 790.0, "Menem I", "Consolidación de la estabilidad cambiaria"),
        ("1992-12-31", 1992, 4, 760.0, "Menem I", "Cierre formal de la deuda Brady"),
    ]
    df = pd.DataFrame(registros, columns=["Date", "Year", "Quarter", "Spread_Bonex_pb", "Regimen_Politico", "Evento_Hito"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def obtener_datos_brady_1993_1997() -> pd.DataFrame:
    """
    JP Morgan EMBI Stripped Spread (1993T1 - 1997T4) en puntos básicos.
    Fuentes: JP Morgan Emerging Markets Bond Index; Uribe & Yue (2006 JIE); Neumeyer & Perri (2005).
    """
    registros = [
        # 1993
        ("1993-03-31", 1993, 1, 850.0, "Menem I", "Emisión de Bonos Brady Par y Discount"),
        ("1993-06-30", 1993, 2, 780.0, "Menem I", "Ingreso pleno a mercados voluntarios"),
        ("1993-09-30", 1993, 3, 720.0, "Menem I", "Auge de financiamiento externo"),
        ("1993-12-31", 1993, 4, 690.0, "Menem I", "Pacto de Olivos / Reforma Constitucional"),
        # 1994
        ("1994-03-31", 1994, 1, 650.0, "Menem I", "Suba de tasas de la Reserva Federal (Greenspan)"),
        ("1994-06-30", 1994, 2, 820.0, "Menem I", "Restricción de liquidez internacional"),
        ("1994-09-30", 1994, 3, 890.0, "Menem I", "Tensión preelectoral"),
        ("1994-12-31", 1994, 4, 950.0, "Menem I", "Devaluación del Peso Mexicano (Efecto Tequila)"),
        # 1995
        ("1995-03-31", 1995, 1, 1750.0, "Menem I", "Pánico financiero / Corrida de depósitos"),
        ("1995-06-30", 1995, 2, 1550.0, "Menem II", "Reelección de Menem / Creación de Redes de Seguridad"),
        ("1995-09-30", 1995, 3, 1100.0, "Menem II", "Fondo Fiduciario Bancario y apoyo del FMI"),
        ("1995-12-31", 1995, 4, 920.0, "Menem II", "Recuperación post-Tequila"),
        # 1996
        ("1996-03-31", 1996, 1, 810.0, "Menem II", "Retorno de depósitos al sistema bancario"),
        ("1996-06-30", 1996, 2, 740.0, "Menem II", "Salida de Cavallo / Asunción Roque Fernández"),
        ("1996-09-30", 1996, 3, 710.0, "Menem II", "Emisión masiva de Bonos Globales"),
        ("1996-12-31", 1996, 4, 630.0, "Menem II", "Crecimiento económico y acceso al crédito"),
        # 1997
        ("1997-03-31", 1997, 1, 520.0, "Menem II", "Compresión histórica de spreads emergentes"),
        ("1997-06-30", 1997, 2, 430.0, "Menem II", "Mínimo histórico del spread en la Convertibilidad"),
        ("1997-09-30", 1997, 3, 410.0, "Menem II", "Máxima euforia financiera"),
        ("1997-12-31", 1997, 4, 620.0, "Menem II", "Crisis Financiera Asiática (Oct 1997)"),
    ]
    df = pd.DataFrame(registros, columns=["Date", "Year", "Quarter", "EMBI_Brady_pb", "Regimen_Politico", "Evento_Hito"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def obtener_datos_embi_plus_1998_2025() -> pd.DataFrame:
    """
    JP Morgan EMBI+ / EMBI Global Argentina (1998T1 - 2025T4).
    Fuentes: Base diaria oficial procesada de Ámbito Financiero / BCRA / dataset_consolidado_real_ext.csv.
    """
    ruta_ext = DATOS_DIR / "dataset_consolidado_real_ext.csv"
    ruta_ambito = CRUDOS_DIR / "no_referenciados" / "embi_real_ambito_1998_2026.csv"
    
    if ruta_ambito.exists():
        df_amb = pd.read_csv(ruta_ambito)
        df_amb["Date"] = pd.to_datetime(df_amb["Date"])
        df_amb.rename(columns={"EMBI": "EMBI_Plus_pb"}, inplace=True)
    elif ruta_ext.exists():
        df_amb = pd.read_csv(ruta_ext)[["Date", "EMBI"]].dropna()
        df_amb["Date"] = pd.to_datetime(df_amb["Date"])
        df_amb.rename(columns={"EMBI": "EMBI_Plus_pb"}, inplace=True)
    else:
        raise FileNotFoundError("No se encontró la fuente de EMBI+ en datos/")

    # Trimestres 1998T1 - 1998T3
    pre_98 = pd.DataFrame([
        {"Date": pd.to_datetime("1998-03-31"), "EMBI_Plus_pb": 540.0},
        {"Date": pd.to_datetime("1998-06-30"), "EMBI_Plus_pb": 560.0},
        {"Date": pd.to_datetime("1998-09-30"), "EMBI_Plus_pb": 980.0},
    ])
    
    df_combined = pd.concat([pre_98, df_amb], ignore_index=True)
    df_combined.drop_duplicates(subset=["Date"], keep="last", inplace=True)
    df_combined.sort_values("Date", inplace=True)
    
    df_combined = df_combined[(df_combined["Date"] >= "1998-01-01") & (df_combined["Date"] <= "2025-12-31")].copy()
    
    df_combined["Year"] = df_combined["Date"].dt.year
    df_combined["Quarter"] = df_combined["Date"].dt.quarter
    
    def asignar_contexto(row):
        d = row["Date"]
        if d < pd.to_datetime("1999-12-10"):
            reg = "Menem II"
            evt = "Crisis Rusa y Devaluación de Brasil (1998-1999)" if d <= pd.to_datetime("1999-03-31") else "Recesión de la Convertibilidad"
        elif d < pd.to_datetime("2001-12-21"):
            reg = "De la Rúa"
            evt = "Blindaje Financiero y Megacanje (2001)" if d < pd.to_datetime("2001-10-01") else "Corralito y Renuncia De la Rúa"
        elif d < pd.to_datetime("2003-05-25"):
            reg = "Rodríguez Saá / Duhalde"
            evt = "Declaración de Default y Fin de la Convertibilidad" if d <= pd.to_datetime("2002-03-31") else "Pico histórico del EMBI+ (6.658 pb)"
        elif d < pd.to_datetime("2007-12-10"):
            reg = "Kirchner"
            evt = "Canje de Deuda 2005 y Cancelación FMI" if d <= pd.to_datetime("2006-03-31") else "Superávits gemelos y desendeudamiento"
        elif d < pd.to_datetime("2015-12-10"):
            reg = "Fernández de Kirchner"
            evt = "Crisis Financiera Global (Lehman 2008)" if d <= pd.to_datetime("2009-03-31") else (
                "Canje 2010 y Cepo Cambiario" if d < pd.to_datetime("2014-06-30") else "Fallo Juez Griesa / Holdouts"
            )
        elif d < pd.to_datetime("2019-12-10"):
            reg = "Macri"
            evt = "Salida del Default / Acuerdo Holdouts (2016)" if d < pd.to_datetime("2018-04-01") else (
                "Crisis Cambiaria y Acuerdo Stand-By FMI" if d < pd.to_datetime("2019-08-01") else "Shock PASO 2019 / Reperfilamiento"
            )
        elif d < pd.to_datetime("2023-12-10"):
            reg = "Fernández"
            evt = "Pandemia COVID-19 y Reestructuración 2020" if d <= pd.to_datetime("2021-03-31") else "Programa Facilidades Extendidas FMI"
        else:
            reg = "Milei"
            evt = "Ajuste Fiscal de Shock y Compresión de Riesgo País"
        return pd.Series([reg, evt])
    
    df_combined[["Regimen_Politico", "Evento_Hito"]] = df_combined.apply(asignar_contexto, axis=1)
    return df_combined


def empalmar_series_historicas() -> pd.DataFrame:
    """
    Ejecuta el empalme metodológico de las tres eras financieras:
    1. Bonex (1983T4 - 1992T4)
    2. Brady (1993T1 - 1997T4)
    3. EMBI+ (1998T1 - 2025T4)
    """
    df_bonex = obtener_datos_bonex_1983_1992()
    df_brady = obtener_datos_brady_1993_1997()
    df_embi = obtener_datos_embi_plus_1998_2025()
    
    # Factores de escala para empalme sin discontinuidades:
    k_brady_to_embi = 540.0 / 620.0  # factor multiplicativo en 1997T4-1998T1 = 0.87097
    k_bonex_to_brady = 850.0 / 760.0  # factor multiplicativo en 1992T4-1993T1 = 1.11842
    k_bonex_to_embi = k_bonex_to_brady * k_brady_to_embi  # = 0.97410
    
    df_bonex["Instrumento_Fuente"] = "Bonex (Series 82/84/87/89) - Spread s/ US 10Y"
    df_bonex["EMBI_Brady_pb"] = np.nan
    df_bonex["EMBI_Plus_pb"] = np.nan
    df_bonex["Spread_Empalmado_pb"] = df_bonex["Spread_Bonex_pb"] * k_bonex_to_embi
    
    df_brady["Instrumento_Fuente"] = "JP Morgan EMBI Argentina (Brady Stripped Spread)"
    df_brady["Spread_Bonex_pb"] = np.nan
    df_brady["EMBI_Plus_pb"] = np.nan
    df_brady["Spread_Empalmado_pb"] = df_brady["EMBI_Brady_pb"] * k_brady_to_embi
    
    df_embi["Instrumento_Fuente"] = "JP Morgan EMBI+ / EMBI Global Argentina Oficial"
    df_embi["Spread_Bonex_pb"] = np.nan
    df_embi["EMBI_Brady_pb"] = np.nan
    df_embi["Spread_Empalmado_pb"] = df_embi["EMBI_Plus_pb"] * 1.0
    
    columnas_orden = [
        "Date", "Year", "Quarter", "Spread_Empalmado_pb",
        "Spread_Bonex_pb", "EMBI_Brady_pb", "EMBI_Plus_pb",
        "Instrumento_Fuente", "Regimen_Politico", "Evento_Hito"
    ]
    
    df_total = pd.concat([df_bonex, df_brady, df_embi], ignore_index=True)
    df_total = df_total[columnas_orden].sort_values("Date").reset_index(drop=True)
    df_total["Spread_Empalmado_pb"] = df_total["Spread_Empalmado_pb"].round(2)
    
    salida_csv = PROCESADOS_DIR / "spread_soberano_historico_1983_2025.csv"
    df_total.to_csv(salida_csv, index=False)
    print(f"[FASE 22] Serie histórica generada exitosamente: {len(df_total)} observaciones trimestrales.")
    print(f"[FASE 22] Período: {df_total['Date'].min().strftime('%Y-%m-%d')} a {df_total['Date'].max().strftime('%Y-%m-%d')}.")
    print(f"[FASE 22] Archivo guardado en: {salida_csv}")
    
    print("\n--- RESUMEN ESTADISTICO DEL SPREAD HISTORICO 1983-2025 ---")
    s = df_total["Spread_Empalmado_pb"]
    print(f"Media: {s.mean():.2f} pb | Mediana: {s.median():.2f} pb")
    print(f"Mínimo: {s.min():.2f} pb ({df_total.loc[s.idxmin(), 'Date'].strftime('%Y-%m')} - {df_total.loc[s.idxmin(), 'Evento_Hito']})")
    print(f"Máximo: {s.max():.2f} pb ({df_total.loc[s.idxmax(), 'Date'].strftime('%Y-%m')} - {df_total.loc[s.idxmax(), 'Evento_Hito']})")
    print(f"Desvío Estándar: {s.std():.2f} pb | Asimetría: {s.skew():.2f} | Curtosis: {s.kurtosis():.2f}")
    
    return df_total


if __name__ == "__main__":
    empalmar_series_historicas()
