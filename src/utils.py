"""Funções auxiliares."""
from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROCESSED = RAIZ / "data" / "processed"
DIR_GRAFICOS = RAIZ / "outputs" / "graficos"


def garantir_pastas() -> None:
    """Cria as pastas de dados e saída caso não existam."""
    for pasta in (DIR_RAW, DIR_PROCESSED, DIR_GRAFICOS):
        pasta.mkdir(parents=True, exist_ok=True)


def nome_arquivo_seguro(ticker: str) -> str:
    """Converte um ticker em um nome de arquivo seguro (ex: ^BVSP -> BVSP)."""
    return "".join(c for c in ticker if c.isalnum() or c in "-_.")
