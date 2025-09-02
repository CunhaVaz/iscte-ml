# 📊 ISCTE - Trabalho A (Quantitativo)

Este repositório contém a resolução do **Trabalho A – Quantitativo** da disciplina de ADVIAG (ISCTE), cujo tema é:

**“Machine Learning para análise preditiva no contexto empresarial”**

---

## 🎯 Objetivo
- Aplicar **Machine Learning** a um dataset sintético (≤500 linhas × 10 colunas).  
- Responder a duas questões de investigação:
  1. *Quanto vamos vender por período/cliente?*  
  2. *Quais são os principais drivers das vendas?*  
- Demonstrar a **utilidade da automatização** na tomada de decisão.  

---

## 🛠️ Pipeline do Projeto

1. `src/gerador_dataset.py` → gera o dataset sintético `data/raw/dataset_biagio.xlsx` (com omissos, duplicados, outliers e erros ortográficos).  
2. `src/eda_raw.py` → **1.ª análise** (dados brutos): estatísticas iniciais, relatório Sweetviz (`reports/eda_raw_sweetviz.html`) e exportação em Excel/TXT.  
3. `src/clean_data.py` → limpeza dos dados: corrige erros, remove duplicados/outliers e gera `data/processed/dataset_biagio_clean.xlsx`.  
4. `src/sweetviz_compare_raw_clean.py` → gera `reports/sweetviz_raw_vs_clean.html`, relatório Sweetviz que compara lado a lado o dataset bruto e o dataset limpo.  
5. `src/eda_clean.py` → EDA após limpeza: estatísticas finais, gráficos e relatório Sweetviz (`reports/eda_sweetviz_clean.html`).  
6. `src/model_train.py` → divide em treino/teste (80/20) e treina **Regressão Linear** e **Random Forest**. Calcula métricas RMSE, MAPE e R² (treino, teste e global).  
7. `src/plot_metrics.py` → gera gráficos comparativos (PNG) das métricas.  
8. `src/feature_importance.py` → calcula importância das variáveis (Random Forest) e exporta ranking para Excel/PNG.  
9. `src/app_dash.py` → **Dashboard interativo** (Dash/Plotly) com vendas mensais, top clientes/produtos, importância das variáveis e métricas.  
10. `src/infografico_final_com_imagens.py` → cria `reports/infografico_trabalhoA.pptx`, o slide extra (10+1) com resumo visual do trabalho.  

---

## 📂 Estrutura de Pastas
iscte-ml/
│
├── data/
│   ├── raw/                  # datasets originais
│   └── processed/            # datasets limpos
│
├── reports/                  # outputs (Excel, Sweetviz, métricas, gráficos, infográficos)
│
├── src/                      # scripts Python
│   ├── gerador_dataset.py
│   ├── eda_raw.py
│   ├── clean_data.py
│   ├── sweetviz_compare_raw_clean.py
│   ├── eda_clean.py
│   ├── model_train.py
│   ├── feature_importance.py
│   ├── plot_metrics.py
│   ├── create_infografico_with_images_fixed.py
│   └── app_dash.py
│
├── README.md
├── requirements.txt
└── requirements_full.txt

---

## 📊 Principais Resultados

### Regressão Linear
- **Treino**: RMSE = 6 915 | MAPE = 26,0% | R² = 0,74  
- **Teste**: RMSE = 7 924 | MAPE = 23,3% | R² = 0,53  
- **Global**: RMSE = 7 129 | MAPE = 25,5% | R² = 0,70  

### Random Forest
- **Treino**: RMSE = 855 | MAPE = 2,4% | R² = 0,996  
- **Teste**: RMSE = 3 051 | MAPE = 7,4% | R² = 0,93  
- **Global**: RMSE = 1 568 | MAPE = 3,4% | R² = 0,99  

### Interpretação
- O **Random Forest** apresentou consistentemente melhor desempenho, com **R² elevado** em todas as fases (≈0,93 no teste e ≈0,99 no global), **erro baixo** (RMSE) e **precisão elevada** (MAPE < 8%).  
- A **Regressão Linear** obteve resultados razoáveis, mas com desempenho inferior, sobretudo no conjunto de teste (R² = 0,53).  
- A análise global confirma que o **Random Forest generaliza melhor**, sendo o modelo mais adequado para previsão das vendas.  

- **Modelo vencedor**: Random Forest  
  - RMSE (teste) ≈ 3 000  
  - MAPE (teste) ≈ 7%  
  - R² (teste) ≈ 0.93  

- **Variáveis mais relevantes**:  
  - Margem_Valor  
  - Produto  
  - Cliente  
  - Ano/Mês (sazonalidade leve)  

---

## 📈 Visualizações

O pipeline gera automaticamente:

- **EDA (Raw e Clean)** com relatórios Sweetviz e Excel.  
- **Relatório comparativo Raw vs Clean (Sweetviz):** `reports/sweetviz_raw_vs_clean.html` → mostra a eliminação de omissos, duplicados e outliers, a normalização de `Margem_%` e a correção de erros de categorias em `Cliente`.  
- **Gráficos de métricas** (RMSE, MAPE, R²) para treino, teste e global.  
- **Ranking de variáveis** (Random Forest).  
- **Infográfico final em PPTX** com síntese dos resultados.  

---

## 🌐 Dashboard Interativo (Dash/Plotly)

Inclui um dashboard para explorar:

- Vendas mensais + média móvel  
- Top 5 clientes por vendas  
- Top 5 produtos mais rentáveis  
- Importância das variáveis (RF)  
- Métricas dos modelos (tabela)  

### ▶️ Para executar:

```bash
python -m src.app_dash

Abrir 👉 http://127.0.0.1:8050

✅ Conclusões
	1.	Quanto vamos vender? → Random Forest permite prever vendas com erro médio de ~7%.
	2.	Quais são os drivers das vendas? → Margem_Valor, Produto e Cliente são os principais fatores explicativos.

⸻

🏢 Utilidade da Ferramenta
	•	Automatiza todo o ciclo: limpeza → EDA → modelos → métricas → insights.
	•	Reduz tempo e erros.
	•	Suporta decisões estratégicas: planeamento de vendas e gestão de clientes/produtos prioritários.

⸻

💡 Reflexão Crítica
	•	Mudanças esperadas: maior foco em clientes/produtos-chave, decisões mais data-driven.
	•	Obstáculos: qualidade dos dados, concentração 80/20, sazonalidade.
	•	Mitigação: pipeline de limpeza, treino/teste, variáveis de calendário.
	•	Lições: Random Forest supera modelos lineares em relações não lineares.
	•	Futuro: modelos temporais (ARIMA/Prophet), dashboards executivos, integração contínua.

⸻

📬 Contacto

Dúvidas ou sugestões: cunha.vaz@sapo.pt