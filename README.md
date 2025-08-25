# ISCTE-ML 📊🤖

Projeto académico no âmbito da Pós-Graduação em Inteligência Artificial Aplicada à Gestão (ISCTE).

Este repositório contém um **pipeline completo de análise e previsão de vendas**:
- Limpeza e preparação de dados (tratamento de omissos, outliers e erros ortográficos).
- Análise exploratória (EDA) com exportação para Excel e relatórios interativos (Sweetviz).
- Divisão temporal dos dados (80% treino / 20% teste).
- Modelos de Machine Learning (Regressão Linear e Random Forest).
- Métricas de avaliação (RMSE, MAPE) e comparação de modelos.
- Identificação de variáveis mais relevantes para a previsão.
- Dashboard interativo em **Dash/Plotly** para exploração dos resultados.

---

## 📂 Estrutura do Projeto
scte-ml/
├── src/                   # scripts Python (ex.: clean_data.py, eda.py, model_train.py, app_dash.py)
├── data/
│   ├── raw/               # datasets originais
│   └── processed/         # datasets limpos / prontos para modelação
├── reports/               # outputs: EDA em Excel, Sweetviz em HTML, sumários
├── .venv/                 # ambiente virtual local (ignorado no GitHub)
├── requirements.txt       # bibliotecas necessárias
├── .gitignore             # ficheiros/pastas a ignorar no Git
└── README.md              # descrição e instruções do projeto
