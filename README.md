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
## 🚀 Instalação e Ambiente

Para recriar o ambiente do projeto, siga os passos abaixo:

1. **Criar ambiente virtual (Python 3.11 recomendado)**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   .venv\Scripts\activate      # Windows

# 📊 Análise Exploratória (EDA) — Dataset Limpo

## 1. Estatísticas descritivas da variável alvo (`Vendas`)
- N.º registos: **497**  
- Média: **27 352**  
- Mediana: **27 352**  
- Desvio-padrão: **13 098**  
- Mínimo: **5 003**  
- Máximo: **53 053**  

👉 Distribuição relativamente simétrica, centrada na média ≈ 27 mil.

---

## 2. Histograma de Vendas
- Mostra concentração em torno da média/mediana.  
- Poucos registos nos extremos → outliers já foram removidos.

---

## 3. Evolução das Vendas Mensais
- Gráfico linear mostra flutuação regular ao longo dos meses.  
- Linha de tendência (média móvel 3M) evidencia estabilidade com pequenas oscilações.  

---

## 4. Top Clientes
- **Intermarket Angola**, **Padaria Nova Era** e **Hipermercado Maxi** concentram o maior volume de vendas.  
- Os 5 maiores clientes confirmam a regra **80/20** (poucos clientes geram a maioria da receita).

---

## 5. Produtos mais rentáveis
- **Creme Pasteleiro**, **Chantili Instantâneo** e **Geleia Neutra** são os produtos mais rentáveis.  
- Demonstra que a rentabilidade não é uniforme entre produtos.

---

## 6. Correlações (heatmap)
- **Vendas ↔ Margem_Valor**: 0.82 → correlação **muito forte**.  
- **Vendas ↔ Margem_%**: –0.03 → irrelevante.  
- **Ano/Mês ↔ Vendas**: fracos isoladamente, mas capturam sazonalidade.

---

## 7. Matriz de Confusão (exploratória)
- Clientes classificados em **“Alto Volume” vs “Baixo Volume”** com base na mediana.  
- Usando apenas **Margem_Valor** como preditor → taxa de acerto ≈ **82%**.  
- Confirma a importância da margem como driver de vendas.

---

## ✅ Conclusões da EDA
- O dataset limpo está consistente, sem omissos, duplicados ou outliers extremos.  
- **Margem_Valor** é a variável mais relevante para previsão de vendas.  
- Forte **concentração em clientes e produtos** (regra 80/20).  
- Vendas apresentam **sazonalidade leve**, mas com estabilidade global.