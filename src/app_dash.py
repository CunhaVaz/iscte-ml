import dash
from dash import dcc, html
import pandas as pd
from pathlib import Path

import plotly.express as px

ROOT = Path(".").resolve()

# --- Caminhos ---
DATA_CLEAN  = ROOT / "data" / "processed" / "dataset_biagio_clean.xlsx"
RESULTS_XLSX = ROOT / "reports" / "model_results.xlsx"           # tem abas: comparacao_modelos, global
FEAT_XLSX    = ROOT / "reports" / "feature_importance.xlsx"      # ranking de features

# --- Carregar dados limpos ---
df = pd.read_excel(DATA_CLEAN)

# --- Construir coluna Data a partir de Ano/Mês, se existir ---
if {"Ano","Mês"}.issubset(df.columns):
    df["Data"] = pd.to_datetime(df["Ano"].astype(int).astype(str)
                                + "-" + df["Mês"].astype(int).astype(str) + "-01")
else:
    # fallback: tenta descobrir uma coluna com data
    poss = [c for c in df.columns if "data" in c.lower() or "date" in c.lower()]
    if poss:
        df["Data"] = pd.to_datetime(df[poss[0]])
    else:
        df["Data"] = pd.NaT

# --- Vendas mensais + média móvel ---
if df["Data"].notna().any():
    vendas_mensais = df.groupby("Data")["Vendas"].sum().reset_index()
    fig_vendas = px.line(vendas_mensais, x="Data", y="Vendas",
                         title="Vendas Mensais (série temporal)")
    # média móvel 3M
    vendas_mensais["MM3"] = vendas_mensais["Vendas"].rolling(window=3).mean()
    fig_vendas.add_scatter(x=vendas_mensais["Data"], y=vendas_mensais["MM3"],
                           mode="lines", name="Média móvel (3M)", line=dict(color="red"))
else:
    fig_vendas = px.line(title="Vendas Mensais (sem coluna temporal identificada)")

# --- Top 5 clientes ---
if "Cliente" in df.columns:
    top_clientes = (df.groupby("Cliente")["Vendas"]
                      .sum().sort_values(ascending=False).head(5).reset_index())
    fig_clientes = px.bar(top_clientes, x="Cliente", y="Vendas",
                          title="Top 5 Clientes por Vendas")
else:
    fig_clientes = px.bar(title="Top 5 Clientes (coluna 'Cliente' não encontrada)")

# --- Top 5 produtos mais rentáveis por Margem_Valor ---
if {"Produto","Margem_Valor"}.issubset(df.columns):
    top_produtos = (df.groupby("Produto")["Margem_Valor"]
                      .sum().sort_values(ascending=False).head(5).reset_index())
    fig_produtos = px.bar(top_produtos, x="Produto", y="Margem_Valor",
                          title="Top 5 Produtos mais Rentáveis (Margem_Valor)")
else:
    fig_produtos = px.bar(title="Top 5 Produtos (colunas 'Produto'/'Margem_Valor' não encontradas)")

# --- Importância das variáveis (se existir o ficheiro) ---
if FEAT_XLSX.exists():
    feat_imp = pd.read_excel(FEAT_XLSX)
    topN = 15
    feat_plot = feat_imp.head(topN).iloc[::-1]   # invertido para barras horizontais
    fig_feat = px.bar(feat_plot, x="importance", y="feature",
                      orientation="h", title="Importância das Variáveis (Random Forest)")
else:
    fig_feat = px.bar(title="Importância das Variáveis (ficheiro não encontrado)")

# --- Métricas dos modelos (comparacao_modelos) ---
if RESULTS_XLSX.exists():
    results = pd.read_excel(RESULTS_XLSX, sheet_name="comparacao_modelos")
else:
    results = pd.DataFrame({
        "info": ["Ficheiro 'reports/model_results.xlsx' não encontrado."]
    })

# ----------------------- APP DASH -----------------------
app = dash.Dash(__name__, title="Dashboard Previsão de Vendas - Biagio")

app.layout = html.Div([
    html.H1("Dashboard Previsão de Vendas - Biagio"),

    html.Div([
        html.Div([html.H2("Vendas Mensais"), dcc.Graph(figure=fig_vendas)],
                 style={"width": "100%", "display": "inline-block"})
    ]),

    html.Div([
        html.Div([html.H2("Top 5 Clientes"), dcc.Graph(figure=fig_clientes)],
                 style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([html.H2("Top 5 Produtos (Margem_Valor)"), dcc.Graph(figure=fig_produtos)],
                 style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"width": "100%"}),

    html.H2("Importância das Variáveis (RF)"),
    dcc.Graph(figure=fig_feat),

    html.H2("Métricas dos Modelos (80/20)"),
    html.Table([
        html.Thead(html.Tr([html.Th(col) for col in results.columns])),
        html.Tbody([
            html.Tr([html.Td(results.iloc[i][col]) for col in results.columns])
            for i in range(len(results))
        ])
    ], style={"width": "100%", "display": "inline-block"})
])

app = dash.Dash(__name__, title="Dashboard Previsão de Vendas - Biagio")
server = app.server   # <-- ADICIONAR ESTA LINHA

import os

if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8050))
    )