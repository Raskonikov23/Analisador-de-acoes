# 📈 Analisador de Ações

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Testes](https://github.com/SEU-USUARIO/analisador-de-acoes/actions/workflows/tests.yml/badge.svg)
![Licença](https://img.shields.io/badge/licença-MIT-green)

Sistema em Python que **coleta dados da bolsa**, **analisa preços** e **gera gráficos de investimento** a partir de uma linha de comando.

> ⚠️ Projeto educacional. Não é recomendação de investimento.

## Prévia

<!-- Rode o projeto, copie 2 ou 3 PNGs de outputs/graficos/ para docs/ e atualize os caminhos abaixo -->
![Preço e médias móveis](docs/exemplo_preco.png)
![Retorno acumulado comparado](docs/exemplo_comparativo.png)

## Funcionalidades

- Coleta de dados históricos via **yfinance** (ações brasileiras `PETR4.SA`, internacionais `AAPL`, índices `^BVSP`)
- Cache local em CSV para evitar downloads repetidos
- Indicadores com **Pandas**: retorno diário e acumulado, médias móveis (20/50/200), volatilidade anualizada, drawdown máximo, RSI e Bandas de Bollinger
- Comparação entre vários ativos e contra um benchmark (ex: Ibovespa)
- Gráficos com **Matplotlib**: preço + médias + volume, RSI, histograma de retornos, retorno acumulado comparado e mapa de correlação
- Tabela-resumo exportada em CSV
- Testes automatizados com **pytest** e CI no GitHub Actions

## Tecnologias

Python · Pandas · NumPy · yfinance · Matplotlib · pytest

## Como rodar

```bash
git clone https://github.com/SEU-USUARIO/analisador-de-acoes.git
cd analisador-de-acoes

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Exemplo de uso:

```bash
python main.py --tickers PETR4.SA VALE3.SA --inicio 2023-01-01 --benchmark ^BVSP
```

| Argumento | Descrição |
|---|---|
| `--tickers` | Um ou mais códigos de ativos (obrigatório) |
| `--inicio` | Data inicial `AAAA-MM-DD` (padrão: 2023-01-01) |
| `--fim` | Data final `AAAA-MM-DD` (padrão: hoje) |
| `--benchmark` | Índice de comparação, ex: `^BVSP` |

Os gráficos são salvos em `outputs/graficos/` e o resumo em `data/processed/resumo.csv`.

## Testes

```bash
python -m pytest -v
```

## Estrutura

```
analisador-de-acoes/
├── main.py              # CLI
├── src/
│   ├── coleta.py        # download + cache (yfinance)
│   ├── analise.py       # indicadores (pandas)
│   ├── graficos.py      # visualizações (matplotlib)
│   └── utils.py         # caminhos e helpers
├── tests/               # testes dos indicadores
├── data/                # raw/ e processed/ (ignorados pelo git)
├── outputs/graficos/    # PNGs gerados
└── notebooks/           # exploração
```

## Aprendizados

<!-- Escreva com suas palavras: o que aprendeu sobre séries temporais, tratamento de erros, testes, estrutura de projeto... -->

## Próximos passos

- [ ] Dashboard interativo com Streamlit
- [ ] Gráficos de candlestick (mplfinance)
- [ ] Backtest de cruzamento de médias móveis
- [ ] Relatório automático em PDF/Excel
- [ ] Alertas de RSI

## Licença

MIT. Veja [LICENSE](LICENSE).
