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
4. `src/eda_clean.py` → EDA após limpeza: estatísticas finais, gráficos e relatório Sweetviz (`reports/eda_sweetviz_clean.html`).  
5. `src/model_train.py` → divide em treino/teste (80/20) e treina **Regressão Linear** e **Random Forest**. Calcula métricas RMSE, MAPE e R² (treino, teste e global).  
6. `src/plot_metrics.py` → gera gráficos comparativos (PNG) das métricas.  
7. `src/feature_importance.py` → calcula importância das variáveis (Random Forest) e exporta ranking para Excel/PNG.  
8. `src/app_dash.py` → **Dashboard interativo** (Dash/Plotly) com vendas mensais, top clientes/produtos, importância das variáveis e métricas.  
9. `src/infografico_final_com_imagens.py` → cria `reports/infografico_trabalhoA.pptx`, o slide extra (10+1) com resumo visual do trabalho.  

---

## 📊 Principais Resultados

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

Exemplos de gráficos estáticos (PNG exportados para o README):

![RMSE Treino/Teste](reports/plot_rmse_treino_teste.png)  
![MAPE Treino/Teste](reports/plot_mape_treino_teste.png)  
![R² Treino/Teste](reports/plot_r2_treino_teste.png)  
![Métricas Globais](reports/plot_metricas_globais.png)  

> Para gráficos interativos, correr o **Dashboard**:
```bash
python src/app_dash.py

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


---

## 📬 Contacto

Dúvidas ou sugestões: [cunha.vaz@sapo.pt](mailto:cunha.vaz.pt)
