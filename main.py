"""Ponto de entrada (CLI) do Analisador de Ações.

Exemplo:
    python main.py --tickers PETR4.SA VALE3.SA --inicio 2023-01-01 --benchmark ^BVSP
"""
from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

from src import analise, graficos
from src.coleta import baixar_varios
from src.utils import DIR_PROCESSED, garantir_pastas


def criar_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Analisador de Ações: coleta, análise e gráficos.")
    p.add_argument("--tickers", nargs="+", required=True, help="Ex: PETR4.SA VALE3.SA AAPL")
    p.add_argument("--inicio", default="2023-01-01", help="Data inicial (AAAA-MM-DD)")
    p.add_argument("--fim", default=date.today().isoformat(), help="Data final (AAAA-MM-DD)")
    p.add_argument("--benchmark", default=None, help="Índice de comparação (ex: ^BVSP)")
    return p


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = criar_parser().parse_args()
    garantir_pastas()

    tickers = list(args.tickers)
    if args.benchmark and args.benchmark not in tickers:
        tickers.append(args.benchmark)

    dados = baixar_varios(tickers, args.inicio, args.fim)
    if not dados:
        logging.error("Nenhum dado coletado. Encerrando.")
        return 1

    fechamentos = {t: df["Close"] for t, df in dados.items()}

    # Gráficos individuais
    for ticker, df in dados.items():
        graficos.grafico_preco(df, ticker)
        graficos.grafico_rsi(df, ticker)
        graficos.grafico_histograma_retornos(df, ticker)

    # Gráficos comparativos
    if len(fechamentos) > 1:
        graficos.grafico_retorno_acumulado(fechamentos)
        graficos.grafico_correlacao(fechamentos)

    # Tabela-resumo
    tabela = analise.tabela_comparativa(fechamentos)
    tabela.to_csv(DIR_PROCESSED / "resumo.csv")
    print("\nResumo dos ativos:\n")
    print(tabela.round(4).to_string())
    print("\nGráficos salvos em outputs/graficos/")
    print("Aviso: projeto educacional, não é recomendação de investimento.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
