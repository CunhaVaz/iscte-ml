# 📊 ISCTE - Trabalho A (Quantitativo)

Este repositório contém a resolução do **Trabalho A – Quantitativo** da disciplina de ADVIAG (ISCTE).

---

## 🎯 Objetivo
Aplicar Machine Learning a um dataset sintético (≤500 linhas × 10 colunas) para:
1. Prever **vendas** por período/cliente.  
2. Identificar os **principais drivers** das vendas.  

---

## 🛠️ Pipeline

- `src/clean_data.py` → limpeza de dados (omissos, duplicados, outliers, ortografia).  
- `src/eda_raw.py` → diagnóstico inicial (dados originais).  
- `src/eda_clean.py` → EDA após limpeza (estatísticas, Sweetviz).  
- `src/model_train.py` → split 80/20, treino de **Regressão Linear** e **Random Forest**, métricas (RMSE, MAPE, R²).  
- `src/feature_importance.py` → ranking das variáveis mais relevantes (Random Forest).  
- `src/plot_metrics.py` → gráficos comparativos (RMSE, MAPE, R²).  
- `src/app_dash.py` → **dashboard interativo** (Dash/Plotly).  

---

## 📊 Resultados

### Comparação dos Modelos
| Modelo            | RMSE_Treino | MAPE_Treino | R²_Treino | RMSE_Teste | MAPE_Teste | R²_Teste |
|-------------------|-------------|-------------|-----------|------------|------------|----------|
| Regressão Linear  | ~7 100      | 25%         | 0.70      | ~7 200     | 26%        | 0.70     |
| Random Forest     | ~1 500      | 3%          | 0.98      | ~3 000     | 7%         | 0.93     |

👉 **Random Forest** foi o modelo selecionado.

### Variáveis mais relevantes
- **Margem_Valor**  
- **Produto**  
- **Cliente**  
- Ano/Mês (sazonalidade leve)  

---

## 📈 Visualizações

- Séries temporais de vendas  
- Top 5 clientes e produtos  
- Importância das variáveis  
- Gráficos comparativos de métricas  
 
---

## 🧭 Dashboard Interativo (Dash/Plotly)

O projeto inclui um dashboard para exploração interativa dos resultados.
Abrir no browser:
👉 http://127.0.0.1:8050

### Como correr
1. Ativar o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```
2. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Executar o dashboard:
   ```bash
   python src/app_dash.py
   ```

---

## 📂 Estrutura do Projeto

```
├── data/
│   └── vendas.csv
├── reports/
│   └── *.png
├── src/
│   ├── clean_data.py
│   ├── eda_raw.py
│   ├── eda_clean.py
│   ├── model_train.py
│   ├── feature_importance.py
│   ├── plot_metrics.py
│   └── app_dash.py
├── requirements.txt
└── README.md
```

---

## 📬 Contacto

Dúvidas ou sugestões: [cunha.vaz@sapo.pt](mailto:cunha.vaz.pt)
