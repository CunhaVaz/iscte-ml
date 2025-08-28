from pathlib import Path
import pandas as pd

import matplotlib.pyplot as plt

ROOT = Path(".").resolve()
RESULTS_XLSX = ROOT / "reports" / "model_results.xlsx"
OUT_DIR = ROOT / "reports"; OUT_DIR.mkdir(exist_ok=True)

def plot_metric(df, metric_cols, title, filename):
    """Cria gráfico de barras lado a lado para cada métrica em metric_cols."""
    ax = df.set_index("Modelo")[metric_cols].plot(kind="bar", figsize=(9,5))
    ax.set_title(title)
    ax.set_ylabel("valor")
    ax.legend(title="Métrica")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename, dpi=150)
    plt.close()

def main():
    # ler as duas abas
    df_tt = pd.read_excel(RESULTS_XLSX, sheet_name="comparacao_modelos")
    df_gl = pd.read_excel(RESULTS_XLSX, sheet_name="global")

    # Gráficos de treino/teste
    plot_metric(
        df_tt,
        ["RMSE_Treino","RMSE_Teste"],
        "Comparação RMSE (Treino vs Teste)",
        "plot_rmse_treino_teste.png"
    )

    plot_metric(
        df_tt,
        ["MAPE_Treino","MAPE_Teste"],
        "Comparação MAPE (Treino vs Teste)",
        "plot_mape_treino_teste.png"
    )

    plot_metric(
        df_tt,
        ["R2_Treino","R2_Teste"],
        "Comparação R² (Treino vs Teste)",
        "plot_r2_treino_teste.png"
    )

    # Gráficos globais
    ax = df_gl.set_index("Modelo")[["RMSE_Global","MAPE_Global","R2_Global"]].plot(
        kind="bar", figsize=(9,5)
    )
    ax.set_title("Métricas Globais (RMSE / MAPE / R²)")
    ax.set_ylabel("valor")
    ax.legend(title="Métrica")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "plot_metricas_globais.png", dpi=150)
    plt.close()

    print("✅ Gráficos gerados na pasta 'reports/'")

if __name__ == "__main__":
    main()