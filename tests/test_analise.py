import numpy as np
import pandas as pd
import pytest

from src import analise


@pytest.fixture
def precos() -> pd.Series:
    idx = pd.date_range("2024-01-01", periods=5, freq="D")
    return pd.Series([100.0, 110.0, 99.0, 108.9, 120.0], index=idx)


def test_retorno_diario(precos):
    r = analise.retorno_diario(precos)
    assert len(r) == 4
    assert r.iloc[0] == pytest.approx(0.10)


def test_retorno_acumulado(precos):
    assert analise.retorno_acumulado(precos).iloc[-1] == pytest.approx(0.20)


def test_drawdown_maximo(precos):
    # pico 110 -> vale 99 = -10%
    assert analise.drawdown_maximo(precos) == pytest.approx(-0.10)


def test_media_movel(precos):
    mm = analise.medias_moveis(precos, (2,))
    assert mm["MM2"].iloc[1] == pytest.approx(105.0)
    assert np.isnan(mm["MM2"].iloc[0])


def test_rsi_limites():
    sobe = pd.Series(np.arange(1, 60, dtype=float))
    desce = pd.Series(np.arange(60, 1, -1, dtype=float))
    assert analise.rsi(sobe).iloc[-1] == pytest.approx(100.0)
    assert analise.rsi(desce).iloc[-1] == pytest.approx(0.0, abs=1e-6)


def test_bollinger_ordem(precos):
    bb = analise.bandas_bollinger(precos, janela=3).dropna()
    assert (bb["superior"] >= bb["media"]).all()
    assert (bb["media"] >= bb["inferior"]).all()


def test_volatilidade_positiva(precos):
    assert analise.volatilidade_anualizada(analise.retorno_diario(precos)) > 0
