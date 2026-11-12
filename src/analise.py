"""Indicadores e métricas de análise de preços."""
from __future__ import annotations

import numpy as np
import pandas as pd

DIAS_UTEIS_ANO = 252


def retorno_diario(precos: pd.Series) -> pd.Series:
    """Retorno percentual diário."""
    return precos.pct_change().dropna()


def retorno_acumulado(precos: pd.Series) -> pd.Series:
    """Retorno acumulado desde o primeiro dia (0.10 = +10%)."""
    return precos / precos.iloc[0] - 1


def medias_moveis(precos: pd.Series, janelas: tuple[int, ...] = (20, 50, 200)) -> pd.DataFrame:
    """Médias móveis simples para as janelas informadas."""
    return pd.DataFrame({f"MM{j}": precos.rolling(j).mean() for j in janelas})


def volatilidade_anualizada(retornos: pd.Series) -> float:
    """Desvio padrão dos retornos diários, anualizado."""
    return float(retornos.std() * np.sqrt(DIAS_UTEIS_ANO))


def drawdown(precos: pd.Series) -> pd.Series:
    """Queda percentual em relação ao pico anterior."""
    pico = precos.cummax()
    return precos / pico - 1


def drawdown_maximo(precos: pd.Series) -> float:
    """Maior queda pico-a-vale do período (valor negativo)."""
    return float(drawdown(precos).min())


def rsi(precos: pd.Series, periodo: int = 14) -> pd.Series:
    """Índice de Força Relativa (RSI) com suavização de Wilder."""
    delta = precos.diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    media_ganho = ganho.ewm(alpha=1 / periodo, min_periods=periodo, adjust=False).mean()
    media_perda = perda.ewm(alpha=1 / periodo, min_periods=periodo, adjust=False).mean()
    rs = media_ganho / media_perda
    resultado = 100 - 100 / (1 + rs)
    # Sem perdas no período => RSI = 100
    return resultado.where(media_perda != 0, 100.0).where(media_ganho.notna())


def bandas_bollinger(precos: pd.Series, janela: int = 20, num_desvios: float = 2.0) -> pd.DataFrame:
    """Bandas de Bollinger (média, superior e inferior)."""
    media = precos.rolling(janela).mean()
    desvio = precos.rolling(janela).std()
    return pd.DataFrame(
        {
            "media": media,
            "superior": media + num_desvios * desvio,
            "inferior": media - num_desvios * desvio,
        }
    )


def resumo(precos: pd.Series) -> dict[str, float]:
    """Métricas-chave de um ativo."""
    ret = retorno_diario(precos)
    return {
        "preco_inicial": float(precos.iloc[0]),
        "preco_final": float(precos.iloc[-1]),
        "retorno_total": float(retorno_acumulado(precos).iloc[-1]),
        "retorno_medio_diario": float(ret.mean()),
        "volatilidade_anual": volatilidade_anualizada(ret),
        "drawdown_maximo": drawdown_maximo(precos),
        "rsi_atual": float(rsi(precos).iloc[-1]),
    }


def tabela_comparativa(fechamentos: dict[str, pd.Series]) -> pd.DataFrame:
    """Tabela com o resumo de vários ativos lado a lado."""
    return pd.DataFrame({t: resumo(s) for t, s in fechamentos.items()}).T


def matriz_correlacao(fechamentos: dict[str, pd.Series]) -> pd.DataFrame:
    """Correlação entre os retornos diários dos ativos."""
    retornos = pd.DataFrame({t: retorno_diario(s) for t, s in fechamentos.items()})
    return retornos.corr()
