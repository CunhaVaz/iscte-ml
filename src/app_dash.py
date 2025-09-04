# src/app_dash.py
from pathlib import Path
import os
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# ---------------- Config ----------------
ROOT = Path(".").resolve()

DATA_CLEAN   = ROOT / "data" / "processed" / "dataset_biagio_clean.xlsx"
RESULTS_XLSX = ROOT / "reports" / "model_results.xlsx"          # abas: comparacao_modelos, global
FEAT_XLSX    = ROOT / "reports" / "feature_importance.xlsx"     # ranking de features

# ---------------- Load data ----------------
def load_clean_data():
    if DATA_CLEAN.exists():
        return pd.read_excel(DATA_CLEAN)
    return pd.DataFrame({"info": ["Ficheiro de dados limpos não encontrado."]})

def load_results():
    if RESULTS_XLSX.exists():
        try:
            return pd.read_excel(RESULTS_XLSX, sheet_name="comparacao_modelos")
        except Exception:
            return pd.read_excel(RESULTS_XLSX)
    return pd.DataFrame({"info": ["Faltam resultados em reports/model_results.xlsx"]})

def load_feat_importance():
    if FEAT_XLSX.exists():
        return pd.read_excel(FEAT_XLSX)
    return pd.DataFrame({"feature": ["sem dados"], "importance": [0.0]})

df = load_clean_data()
results = load_results()
feat_imp = load_feat_importance()

# ---------------- Data prep ----------------
if {"Ano", "Mês"}.issubset(df.columns):
    df["Data"] = pd.to_datetime(
        df["Ano"].astype(int).astype(str) + "-" + df["Mês"].astype(int).astype(str) + "-01"
    )
else:
    poss = [c for c in df.columns if "data" in c.lower() or "date" in c.lower()]
    df["Data"] = pd.to_datetime(df[poss[0]]) if poss else pd.NaT

# ---------------- Figures ----------------
# 1) Vendas mensais + média móvel
if df.get("Data", pd.Series()).notna().any() and "Vendas" in df.columns:
    vendas_mensais = df.groupby("Data", as_index=False)["Vendas"].sum().sort_values("Data")
    fig_vendas = px.line(vendas_mensais, x="Data", y="Vendas", title="Vendas Mensais (série temporal)")
    vendas_mensais["MM3"] = vendas_mensais["Vendas"].rolling(window=3).mean()
    fig_vendas.add_scatter(
        x=vendas_mensais["Data"], y=vendas_mensais["MM3"],
        mode="lines", name="Média móvel (3M)", line=dict(color="red")
    )
else:
    fig_vendas = px.line(title="Vendas Mensais (sem coluna temporal identificada ou sem 'Vendas')")

# 2) Top 5 clientes
if "Cliente" in df.columns and "Vendas" in df.columns:
    top_clientes = (df.groupby("Cliente")["Vendas"]
                      .sum().sort_values(ascending=False).head(5).reset_index())
    fig_clientes = px.bar(top_clientes, x="Cliente", y="Vendas",
                          title="Top 5 Clientes por Vendas")
else:
    fig_clientes = px.bar(title="Top 5 Clientes (colunas 'Cliente'/'Vendas' não encontradas)")

# 3) Top 5 produtos (Margem_Valor)
if {"Produto", "Margem_Valor"}.issubset(df.columns):
    top_produtos = (df.groupby("Produto")["Margem_Valor"]
                      .sum().sort_values(ascending=False).head(5).reset_index())
    fig_produtos = px.bar(top_produtos, x="Produto", y="Margem_Valor",
                          title="Top 5 Produtos mais Rentáveis (Margem_Valor)")
else:
    fig_produtos = px.bar(title="Top 5 Produtos (colunas 'Produto'/'Margem_Valor' não encontradas)")

# 4) Importância de variáveis
if not feat_imp.empty and "feature" in feat_imp.columns and "importance" in feat_imp.columns:
    topN = 15
    feat_plot = feat_imp.head(topN).iloc[::-1]
    fig_feat = px.bar(feat_plot, x="importance", y="feature",
                      orientation="h", title="Importância das Variáveis (Random Forest)")
else:
    fig_feat = px.bar(title="Importância das Variáveis (ficheiro não encontrado ou inválido)")

# ---------------- Dash app ----------------
app = dash.Dash(__name__, title="Dashboard Previsão de Vendas - Biagio")
server = app.server  # necessário para Gunicorn/Render

def metrics_table(df_metrics: pd.DataFrame):
    if df_metrics.empty:
        return html.Div("Sem métricas para apresentar (ver reports/model_results.xlsx).")
    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df_metrics.columns])),
        html.Tbody([
            html.Tr([html.Td(df_metrics.iloc[i][col]) for col in df_metrics.columns])
            for i in range(len(df_metrics))
        ])
    ], style={"width": "100%", "display": "inline-block"})

app.layout = html.Div([
    html.H1("Dashboard Previsão de Vendas - Biagio"),

    html.Div([
        html.H2("Vendas Mensais"),
        dcc.Graph(figure=fig_vendas),
    ], style={"width": "100%", "display": "inline-block"}),

    html.Div([
        html.Div([html.H2("Top 5 Clientes"), dcc.Graph(figure=fig_clientes)],
                 style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([html.H2("Top 5 Produtos (Margem_Valor)"), dcc.Graph(figure=fig_produtos)],
                 style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"width": "100%", "display": "inline-block"}),

    html.H2("Importância das Variáveis (RF)"),
    dcc.Graph(figure=fig_feat),

    html.H2("Métricas dos Modelos (80/20)"),
    metrics_table(results)
])

# Execução local e compatível com Render
if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8050))
    )