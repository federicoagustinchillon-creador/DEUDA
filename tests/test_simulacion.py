"""Pruebas de la estimacion y la simulacion (fase24 y fase25).

Verifican propiedades que el texto de la tesis afirma: que la identidad reproduce la senda del
FMI, que el remuestreo por bloques usa trimestres consecutivos, que el intervalo de Hall esta bien
construido y acotado, que la regla de rezagos devuelve un VAR estable con residuos sin
autocorrelacion y que sin shocks la simulacion reproduce la senda determinista.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "codigo" / "modelos"))
import fase24_svarx_1996_2025 as f24  # noqa: E402
import fase25_simulacion_dsa_svarx as f25  # noqa: E402


@pytest.fixture(scope="module")
def escenario() -> pd.DataFrame:
    return f25.escenario_fmi()


def test_identidad_reproduce_senda_fmi(escenario: pd.DataFrame) -> None:
    _, _, a_fmi, _ = f25.condiciones_iniciales("federal", escenario)
    assert f25.verificar_escenario(escenario, a_fmi) < 0.5


def test_bloques_consecutivos() -> None:
    idx = f25.indices_bloques(np.random.default_rng(0), n=100, N=50, T=40, L=8)
    assert idx.shape == (50, 40)
    assert idx.min() >= 0 and idx.max() < 100
    bloques = idx.reshape(50, 5, 8)
    assert np.all(np.diff(bloques, axis=2) == 1)


def test_intervalo_hall() -> None:
    est = pd.Series({"a": 1.0})
    rep = pd.DataFrame({"a": np.linspace(0.0, 1.0, 1001)})
    h = f24.intervalo_hall(est, rep)
    assert h.loc["a", "inf"] == pytest.approx(2 - 0.95, abs=1e-9)
    assert h.loc["a", "sup"] == pytest.approx(2 - 0.05, abs=1e-9)


def test_acotar_probabilidades_y_participaciones() -> None:
    h = pd.DataFrame({"inf": [-0.1, -5.0, -150.0, -0.2], "sup": [1.2, 120.0, 130.0, 0.3]},
                     index=["base_p_noest_2031", "vshare_fiscal", "h1a_nofiscal_menos_fiscal", "dif_fed_1de_p_noest_2035"])
    a = f25.acotar(h)
    assert a.loc["base_p_noest_2031"].tolist() == [0.0, 1.0]
    assert a.loc["vshare_fiscal"].tolist() == [0.0, 100.0]
    assert a.loc["h1a_nofiscal_menos_fiscal"].tolist() == [-100.0, 100.0]
    assert a.loc["dif_fed_1de_p_noest_2035"].tolist() == [-0.2, 0.3]  # las diferencias no se acotan


def test_regla_de_rezagos() -> None:
    Y, X, _ = f24.cargar_datos("federal", 2)
    p, _, tabla = f24.elegir_rezagos(Y, X)
    fila = tabla[tabla.p == p].iloc[0]
    assert bool(fila.estable)
    assert fila.portmanteau_12_p >= 0.05 or p == int(tabla.p_sic.iloc[0])
    assert p >= int(tabla.p_sic.iloc[0])


def test_sin_shocks_reproduce_senda_base(escenario: pd.DataFrame) -> None:
    Y, X, _ = f24.cargar_datos("federal", 2)
    p, _, _ = f24.elegir_rezagos(Y, X)
    Y, X = f24.recortar(Y, X, p)
    res = f24.VAR(Y, exog=X).fit(maxlags=p, ic=None, trend="c")
    phi, _ = f25.procesos_externos(res.resid.index)
    par = f25.parametros(res, list(X.columns), phi)
    d0, alfa, a_fmi, tcrm0 = f25.condiciones_iniciales("federal", escenario)
    k = len(f24.ENDOG)
    s = f25.simular(par, np.zeros((3, f25.TRIM, k)), np.zeros((3, f25.TRIM, 2)), np.zeros(f25.TRIM),
                    escenario, d0, alfa, a_fmi, tcrm0)
    senda = f25.senda_base(escenario, d0, alfa, a_fmi)
    assert np.allclose(s["d"], senda[None, :], atol=1e-9)


def test_dfed_empalmado_sin_salto_en_2022() -> None:
    fed = pd.read_csv(f24.DATOS / "procesados" / "tasa_fed_trimestral_1996_2025.csv", parse_dates=["Date"], index_col="Date")
    d = f24.dfed_empalmado(fed)
    assert abs(d.loc["2022-03-31"] - (fed.loc["2022-03-31", "fedfunds"] - fed.loc["2021-12-31", "fedfunds"])) < 1e-12
