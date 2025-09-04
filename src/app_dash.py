# src/app_dash.py  (versão com DEBUG no layout)
from pathlib import Path
import os
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# =========================
# Config e paths
# =========================
ROOT = Path(".").resolve()
DATA_CLEAN   = ROOT / "data" / "processed" / "dataset_biagio_clean.xlsx"
RESULTS_XLSX = ROOT / "reports" / "model_results.xlsx"           # aba 'comparacao_modelos'
FEAT_XLSX    = ROOT / "reports" / "feature_importance.xlsx"      # colunas ['feature','importance']

# =========================
# Helpers de leitura
# =========================
def read_excel_df(path: Path, sheet_name=None):
    """
    Lê um Excel e devolve SEMPRE um DataFrame:
      - se sheet_name=None e read_excel devolver um dict (pandas 2.x) -> apanha a 1ª folha
      - se sheet_name for passado -> lê essa folha
      - se falhar -> devolve df com 'info'
    """
    if not path.exists():
        return pd.DataFrame({"info": [f"ficheiro não encontrado: {path}"]})
    try:
        obj = pd.read_excel(path, sheet_name=sheet_name)
        if isinstance(obj, dict):                  # pandas 2.x quando não passamos sheet_name
            obj = next(iter(obj.values()))         # primeira folha
        return obj
    except Exception as e:
        return pd.DataFrame({"info": [f"erro a ler '{path.name}': {e}"]})

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve o DF com os nomes de colunas em minúsculas (sem espaços laterais)."""
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

def load_clean_data() -> pd.DataFrame:
    df = read_excel_df(DATA_CLEAN)
    if "info" in df.columns:      # erro ou não existe
        return df
    df = normalize_columns(df)
    # garantir colunas mínimas
    needed = ["ano","mês","cliente","vendas","produto","canal","margem_%","margem_valor"]
    for c in needed:
        if c not in df.columns:
            df[c] = pd.Series(dtype="float64") if c in ["vendas","margem_%","margem_valor"] else pd.Series(dtype="object")
    return df

def load_results() -> pd.DataFrame:
    df = read_excel_df(RESULTS_XLSX, sheet_name="comparacao_modelos")
    if "info" in df.columns or df.empty:
        df = read_excel_df(RESULTS_XLSX)  # fallback 1ª folha
    if "info" in df.columns:
        return df
    return normalize_columns(df)

def load_feat_importance() -> pd.DataFrame:
    df = read_excel_df(FEAT_XLSX)
    if "info" in df.columns or df.empty:
        return df
    df = normalize_columns(df)
    # garantir ['feature','importance']
    if not {"feature","importance"}.issubset(df.columns):
        if len(df.columns) >= 2:
            df = df.iloc[:, :2]
            df.columns = ["feature", "importance"]
        else:
            df = pd.DataFrame({"feature": [], "importance": []})
    return df

# =========================
# Carregar dados
# =========================
df = load_clean_data()
results = load_results()
feat_imp = load_feat_importance()

# DEBUG no terminal
print("\n[DEBUG] dataset_biagio_clean.xlsx:", "shape=", getattr(df, "shape", "?"), "cols=", list(getattr(df, "columns", []))[:10])
print("[DEBUG] model_results.xlsx:", "shape=", getattr(results, "shape", "?"), "cols=", list(getattr(results, "columns", [])))
print("[DEBUG] feature_importance.xlsx:", "shape=", getattr(feat_imp, "shape", "?"), "cols=", list(getattr(feat_imp, "columns", [])))

# =========================
# Preparar coluna Data
# =========================
if "info" not in df.columns:
    if {"ano","mês"}.issubset(df.columns):
        df["data"] = pd.to_datetime(
            df["ano"].astype("Int64").astype(str) + "-" +
            df["mês"].astype("Int64").astype(str) + "-01",
            errors="coerce"
        )
    else:
        poss = [c for c in df.columns if "data" in c or "date" in c]
        df["data"] = pd.to_datetime(df[poss[0]], errors="coerce") if poss else pd.NaT

# =========================
# Figuras principais
# =========================
# 1) Vendas mensais
if "info" not in df.columns and "vendas" in df.columns and df.get("data", pd.Series()).notna().any():
    vendas_mensais = (df[["data","vendas"]]
                      .dropna()
                      .groupby("data", as_index=False)["vendas"].sum()
                      .sort_values("data"))
    fig_vendas = px.line(vendas_mensais, x="data", y="vendas", title="Vendas Mensais (série temporal)")
    vendas_mensais["mm3"] = vendas_mensais["vendas"].rolling(window=3).mean()
    fig_vendas.add_scatter(x=vendas_mensais["data"], y=vendas_mensais["mm3"],
                           mode="lines", name="Média móvel (3M)", line=dict(color="red"))
else:
    fig_vendas = px.line(title="Vendas Mensais (sem coluna temporal identificada ou sem 'Vendas')")

# 2) Top 5 clientes
if "info" not in df.columns and {"cliente","vendas"}.issubset(df.columns) and df["cliente"].notna().any():
    top_clientes = (df.groupby("cliente", as_index=False)["vendas"]
                      .sum().sort_values("vendas", ascending=False).head(5))
    fig_clientes = px.bar(top_clientes, x="cliente", y="vendas", title="Top 5 Clientes por Vendas")
else:
    fig_clientes = px.bar(title="Top 5 Clientes (colunas 'Cliente'/'Vendas' não encontradas)")

# 3) Top 5 produtos
if "info" not in df.columns and {"produto","margem_valor"}.issubset(df.columns) and df["produto"].notna().any():
    top_produtos = (df.groupby("produto", as_index=False)["margem_valor"]
                      .sum().sort_values("margem_valor", ascending=False).head(5))
    fig_produtos = px.bar(top_produtos, x="produto", y="margem_valor",
                          title="Top 5 Produtos mais Rentáveis (Margem_Valor)")
else:
    fig_produtos = px.bar(title="Top 5 Produtos (colunas 'Produto'/'Margem_Valor' não encontradas)")

# =========================
# Importância e Métricas  (com DEBUG no layout)
# =========================
# Importância
try:
    df_imp_dbg = pd.read_excel(FEAT_XLSX)
    df_imp_dbg.columns = [c.lower() for c in df_imp_dbg.columns]
    if {"feature","importance"}.issubset(df_imp_dbg.columns) and not df_imp_dbg.empty:
        feat_plot = df_imp_dbg[["feature","importance"]].copy().head(15).iloc[::-1]
        fig_feat = px.bar(feat_plot, x="importance", y="feature",
                          orientation="h", title="Importância das Variáveis (Random Forest)")
    else:
        fig_feat = px.bar(title="Importância das Variáveis (ficheiro sem colunas 'feature'/'importance')")
except Exception as e:
    fig_feat = px.bar(title=f"Importância das Variáveis (erro: {e})")

# Métricas (sheet 'comparacao_modelos')
def metrics_table_direct():
    try:
        dfm = pd.read_excel(RESULTS_XLSX, sheet_name="comparacao_modelos")
        dfm.columns = [c.lower() for c in dfm.columns]
        keep = ["modelo","rmse_treino","mape_treino","r2_treino",
                "rmse_teste","mape_teste","r2_teste"]
        cols = [c for c in keep if c in dfm.columns]
        if not cols:
            return html.Div("Faltam colunas esperadas em reports/model_results.xlsx (comparacao_modelos).")
        dfm = dfm[cols]
        # DEBUG no layout: imprime as primeiras linhas
        return html.Div([
            html.Table([
                html.Thead(html.Tr([html.Th(col) for col in dfm.columns])),
                html.Tbody([
                    html.Tr([html.Td(dfm.iloc[i][col]) for col in dfm.columns])
                    for i in range(len(dfm))
                ])
            ], style={"width": "100%", "display": "inline-block"}),
            html.Hr(),
            html.Pre(str(dfm.head()))
        ])
    except Exception as e:
        return html.Div(f"Erro a ler metrics: {e}")

# =========================
# Dash app
# =========================
app = dash.Dash(__name__, title="Dashboard Previsão de Vendas - Biagio")
server = app.server  # necessário para Render

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
    ]),

    html.H2("Importância das Variáveis (RF)"),
    dcc.Graph(figure=fig_feat),
    html.Pre(str(feat_imp.head())),   # <<< DEBUG no layout

    html.H2("Métricas dos Modelos (80/20)"),
    metrics_table_direct(),           # <<< tabela + head() no layout
])

if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8051))  # usa 8051 para evitar conflito
    )
