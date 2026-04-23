# Dashboard Inteligente de Estoque e Criticidade de Materiais

Sistema desenvolvido em Python e Streamlit para análise de estoque, cobertura e criticidade de materiais com base em dados simulados de consumo e parâmetros operacionais.

## Objetivo

Apoiar decisões de planejamento, compras e gestão de estoque a partir de indicadores analíticos que mostram quais materiais exigem ação prioritária.

## Funcionalidades

- Leitura de bases simuladas de estoque e consumo
- Cálculo de consumo médio mensal e diário
- Cálculo de cobertura em dias
- Comparação entre cobertura e lead time
- Classificação dos materiais em Crítico, Atenção e Saudável
- Dashboard interativo com filtro por categoria
- Ranking dos materiais mais sensíveis

## Estrutura do projeto

```text
dashboard-estoque-inteligente/
├── data/
│   ├── estoque_atual.csv
│   └── consumo_historico.csv
├── src/
│   ├── preprocess.py
│   ├── metrics.py
│   └── app.py
├── requirements.txt
├── .gitignore
└── README.md