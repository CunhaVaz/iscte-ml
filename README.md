# 📊 ISCTE - Trabalho A (Quantitativo)

Este repositório contém a resolução do **Trabalho A – Quantitativo** da disciplina de ADVIAG (ISCTE), onde se aplica **Machine Learning para previsão de vendas** com dados sintéticos.

---

## 🎯 Objetivo
- Construir um **pipeline automatizado** de análise preditiva em contexto empresarial.  
- Dataset sintético (≤500 linhas × 10 colunas) representando clientes, produtos, vendas e margens.  
- Identificar **questões de negócio**:  
   1. *Quanto vamos vender por período/cliente?*  
   2. *Quais são os principais drivers das vendas?*  

---

## 🛠️ Pipeline do Projeto

- `src/clean_data.py` → limpeza de dados (omissos, duplicados, outliers, correções ortográficas).  
- `src/eda_raw.py` → diagnóstico dos dados originais (antes da limpeza).  
- `src/eda_clean.py` → análise exploratória após limpeza (estatísticas + relatório Sweetviz).  
- `src/model_train.py` → split 80/20 (temporal), treino de **Regressão Linear** e **Random Forest**, cálculo de métricas (**RMSE, MAPE, R²**).  
- `src/feature_importance.py` → importância das variáveis (Random Forest).  
- `src/plot_metrics.py` → geração de gráficos comparativos (RMSE, MAPE, R²).  
- `src/app_dash.py` → **dashboard interativo** (Dash/Plotly).

---

## 📊 Principais Resultados

### Comparação dos Modelos
| Modelo             | RMSE_Treino | MAPE_Treino | R²_Treino | RMSE_Teste | MAPE_Teste | R²_Teste |
|--------------------|-------------|-------------|-----------|------------|------------|----------|
| Regressão Linear   | ~7 100      | 25%         | 0.70      | ~7 200     | 26%        | 0.70     |
| Random Forest      | ~1 500      | 3%          | 0.98      | ~3 000     | 7%         | 0.93     |

👉 **Random Forest** é o modelo selecionado (melhor RMSE, MAPE e R²).

### Variáveis mais relevantes
Ranking (Random Forest):
- **Margem_Valor**  
- **Produto**  
- **Cliente**  
- Ano / Mês (sazonalidade leve)

---

## 📈 Gráficos

- Histogramas e estatísticas descritivas (EDA)  
- Séries temporais de vendas  
- Top 5 clientes e produtos  
- Importância das variáveis (RF)  
- Comparação gráfica das métricas

![RMSE Treino/Teste](reports/plot_rmse_treino_teste.png)  
![MAPE Treino/Teste](reports/plot_mape_treino_teste.png)  
![R² Treino/Teste](reports/plot_r2_treino_teste.png)  
![Métricas Globais](reports/plot_metricas_globais.png)  

---

## 🧭 Dashboard Interativo (Dash/Plotly)

O projeto inclui um dashboard em **Dash/Plotly** para explorar os resultados:

- Vendas mensais + média móvel  
- Top 5 clientes por vendas  
- Top 5 produtos mais rentáveis  
- Importância das variáveis (RF)  
- Métricas dos modelos (tabela)

**Como correr:**
```bash
source .venv/bin/activate
python src/app_dash.py
```