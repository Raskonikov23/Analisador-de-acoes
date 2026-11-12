"""Visualizações com Matplotlib."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sem janela; salva direto em arquivo
import matplotlib.pyplot as plt
import pandas as pd

from src import analise
from src.utils import DIR_GRAFICOS, garantir_pastas, nome_arquivo_seguro


def _salvar(fig: plt.Figure, nome: str) -> Path:
    garantir_pastas()
    caminho = DIR_GRAFICOS / f"{nome}.png"
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho


def grafico_preco(df: pd.DataFrame, ticker: str) -> Path:
    """Preço de fechamento, médias móveis, Bandas de Bollinger e volume."""
    fechamento = df["Close"]
    mms = analise.medias_moveis(fechamento, (20, 50, 200))
    bb = analise.bandas_bollinger(fechamento)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    ax1.plot(fechamento, label="Fechamento", linewidth=1.4)
    for col in mms:
        ax1.plot(mms[col], label=col, linewidth=1)
    ax1.fill_between(bb.index, bb["inferior"], bb["superior"], alpha=0.12, label="Bollinger")
    ax1.set_title(f"{ticker}: preço e médias móveis")
    ax1.set_ylabel("Preço")
    ax1.legend(loc="upper left", ncol=3)
    ax1.grid(alpha=0.3)

    ax2.bar(df.index, df["Volume"], width=1.0)
    ax2.set_ylabel("Volume")
    ax2.grid(alpha=0.3)
    return _salvar(fig, f"{nome_arquivo_seguro(ticker)}_preco")


def grafico_rsi(df: pd.DataFrame, ticker: str) -> Path:
    """RSI com linhas de sobrecompra (70) e sobrevenda (30)."""
    valores = analise.rsi(df["Close"])
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(valores, linewidth=1.2)
    ax.axhline(70, linestyle="--", color="red", alpha=0.6)
    ax.axhline(30, linestyle="--", color="green", alpha=0.6)
    ax.set_ylim(0, 100)
    ax.set_title(f"{ticker}: RSI (14)")
    ax.grid(alpha=0.3)
    return _salvar(fig, f"{nome_arquivo_seguro(ticker)}_rsi")


def grafico_retorno_acumulado(fechamentos: dict[str, pd.Series]) -> Path:
    """Retorno acumulado comparado entre ativos."""
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker, serie in fechamentos.items():
        ax.plot(analise.retorno_acumulado(serie) * 100, label=ticker)
    ax.set_title("Retorno acumulado (%)")
    ax.set_ylabel("%")
    ax.legend()
    ax.grid(alpha=0.3)
    return _salvar(fig, "comparativo_retorno_acumulado")


def grafico_histograma_retornos(df: pd.DataFrame, ticker: str) -> Path:
    """Distribuição dos retornos diários."""
    ret = analise.retorno_diario(df["Close"]) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(ret, bins=50, edgecolor="white")
    ax.axvline(ret.mean(), color="red", linestyle="--", label=f"Média: {ret.mean():.2f}%")
    ax.set_title(f"{ticker}: distribuição dos retornos diários")
    ax.set_xlabel("Retorno diário (%)")
    ax.legend()
    return _salvar(fig, f"{nome_arquivo_seguro(ticker)}_histograma")


def grafico_correlacao(fechamentos: dict[str, pd.Series]) -> Path:
    """Mapa de calor da correlação entre ativos."""
    corr = analise.matriz_correlacao(fechamentos)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)), corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr)), corr.index)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(im)
    ax.set_title("Correlação entre retornos diários")
    return _salvar(fig, "comparativo_correlacao")
