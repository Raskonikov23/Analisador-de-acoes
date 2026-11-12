"""Coleta de dados da bolsa com yfinance, com cache local em CSV."""
from __future__ import annotations

import logging

import pandas as pd
import yfinance as yf

from src.utils import DIR_RAW, garantir_pastas, nome_arquivo_seguro

logger = logging.getLogger(__name__)


class ErroColeta(Exception):
    """Erro ao coletar dados de um ativo."""


def baixar_dados(
    ticker: str,
    inicio: str,
    fim: str | None = None,
    usar_cache: bool = True,
) -> pd.DataFrame:
    """Baixa o histórico de preços de um ativo.

    Args:
        ticker: código do ativo (ex: "PETR4.SA", "AAPL", "^BVSP").
        inicio: data inicial no formato AAAA-MM-DD.
        fim: data final no formato AAAA-MM-DD (opcional).
        usar_cache: se True, reutiliza o CSV salvo em data/raw/.

    Returns:
        DataFrame com colunas Open, High, Low, Close, Volume e índice de datas.

    Raises:
        ErroColeta: se o ticker for inválido ou não houver dados.
    """
    garantir_pastas()
    caminho = DIR_RAW / f"{nome_arquivo_seguro(ticker)}_{inicio}_{fim or 'hoje'}.csv"

    if usar_cache and caminho.exists():
        logger.info("Usando cache: %s", caminho.name)
        return pd.read_csv(caminho, index_col=0, parse_dates=True)

    try:
        df = yf.download(
            ticker,
            start=inicio,
            end=fim,
            auto_adjust=True,
            progress=False,
        )
    except Exception as exc:  # falhas de rede, etc.
        raise ErroColeta(f"Falha ao baixar {ticker}: {exc}") from exc

    if df is None or df.empty:
        raise ErroColeta(f"Nenhum dado encontrado para '{ticker}'. Verifique o ticker e o período.")

    # Versões recentes do yfinance retornam colunas MultiIndex (campo, ticker)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.to_csv(caminho)
    return df


def baixar_varios(
    tickers: list[str],
    inicio: str,
    fim: str | None = None,
) -> dict[str, pd.DataFrame]:
    """Baixa vários ativos, ignorando (e registrando) os que falharem."""
    resultado: dict[str, pd.DataFrame] = {}
    for t in tickers:
        try:
            resultado[t] = baixar_dados(t, inicio, fim)
        except ErroColeta as exc:
            logger.warning("%s", exc)
    return resultado
