# Dashboard Inteligente de Estoque

Projeto analítico desenvolvido em Python com foco em **gestão de estoque**, **priorização de materiais** e **suporte à tomada de decisão** por meio de indicadores estratégicos e visualizações executivas.

---

## Visão Geral

Este projeto simula um cenário industrial onde diferentes materiais precisam ser monitorados com base em:

- consumo histórico
- estoque disponível
- lead time
- estoque de segurança
- cobertura em dias
- criticidade operacional

A partir dessas variáveis, o sistema identifica riscos, prioriza materiais e gera relatórios gerenciais.

---

## Objetivo de Negócio

Reduzir risco de ruptura, melhorar previsibilidade operacional e apoiar decisões de compras e abastecimento.

---

## Principais Entregas

### Dashboard Executivo (PNG)

Painel visual com:

- indicadores principais
- materiais críticos
- cobertura média
- ranking de prioridades
- distribuição por status

### Relatório Executivo (PDF)

Documento gerencial contendo:

- resumo analítico
- principais achados
- recomendações de ação
- painel consolidado

### Base Analítica (CSV)

Tabela consolidada com métricas calculadas para todos os materiais.

---

## Tecnologias Utilizadas

- Python
- Pandas
- Matplotlib
- FPDF2
- CSV

---

## Estrutura do Projeto

```text
dashboard-estoque-inteligente/
├── data/
│   ├── estoque_atual.csv
│   └── consumo_historico.csv
│
├── outputs/
│   ├── analise_estoque.csv
│   ├── dashboard_estoque.png
│   └── relatorio_estoque.pdf
│
├── src/
│   ├── preprocess.py
│   ├── metrics.py
│   ├── visualize.py
│   ├── report.py
│   └── main.py
│
├── requirements.txt
└── README.md
