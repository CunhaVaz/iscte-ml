 # gerar_dataset_biagio.py
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pathlib import Path
import random

# -------------------------------
# Configuração
# -------------------------------
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# Caminhos (ajusta conforme o teu projeto)
INPUT_PATH  = Path("dataset_biagio_enriquecido.xlsx")  # <-- coloca aqui o ficheiro base
OUTPUT_DIR  = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

SEM_EXPORT_PATH     = OUTPUT_DIR / "dataset_biagio_sem_exportacao.xlsx"
FINAL_500_PATH      = OUTPUT_DIR / "dataset_biagio_500linhas.xlsx"
FINAL_500_ANOM_PATH = OUTPUT_DIR / "dataset_biagio_500linhas_anomalias.xlsx"

# Parâmetros
TARGET_ROWS = 500
CANAL_COL   = "Canal"
VENDAS_COL  = "Vendas"
MARGEM_PCT  = "Margem_%"
MARGEM_VAL  = "Margem_Valor"

# Colunas esperadas (para validação rápida)
COLS_ESPERADAS = ["Ano", "Mês", "Cliente", VENDAS_COL, "Produto", CANAL_COL, MARGEM_PCT, MARGEM_VAL]

# -------------------------------
# Funções auxiliares
# -------------------------------
def validar_colunas(df: pd.DataFrame):
    faltam = [c for c in COLS_ESPERADAS if c not in df.columns]
    if faltam:
        raise ValueError(f"As seguintes colunas em falta no ficheiro de entrada: {faltam}\n"
                         f"Colunas encontradas: {df.columns.tolist()}")

def remover_exportacao(df: pd.DataFrame) -> pd.DataFrame:
    # remove linhas cujo canal contenha 'exportação' (case insensitive)
    mask = df[CANAL_COL].astype(str).str.lower().str.contains("exportação")
    return df.loc[~mask].copy()

def expandir_para_500(df: pd.DataFrame, target_rows: int = TARGET_ROWS) -> pd.DataFrame:
    """Amostra com reposição para atingir target_rows e aplica pequenas variações às métricas."""
    if len(df) >= target_rows:
        return df.sample(target_rows, random_state=SEED).reset_index(drop=True)

    rows_to_add = target_rows - len(df)
    adicional = df.sample(rows_to_add, replace=True, random_state=SEED).copy()

    # Pequenas variações para evitar duplicação exata
    adicional[VENDAS_COL]   = adicional[VENDAS_COL]   * np.random.uniform(0.90, 1.10, size=rows_to_add)
    adicional[MARGEM_PCT]   = adicional[MARGEM_PCT]   * np.random.uniform(0.95, 1.05, size=rows_to_add)
    adicional[MARGEM_VAL]   = adicional[MARGEM_VAL]   * np.random.uniform(0.90, 1.10, size=rows_to_add)

    df_ext = pd.concat([df, adicional], ignore_index=True)
    # Garante exatamente target_rows
    df_ext = df_ext.sample(target_rows, random_state=SEED).reset_index(drop=True)
    return df_ext

def injetar_anomalias(df: pd.DataFrame,
                      n_missing_vendas: int = 4,
                      n_missing_margem: int = 4,
                      n_outliers_vendas: int = 2,
                      inserir_outliers_margem: bool = True,
                      clientes_errados: list[str] = None) -> pd.DataFrame:
    """Cria valores omissos, outliers e erros ortográficos simulados."""
    dfa = df.copy()

    # 1) Missing values
    if n_missing_vendas > 0:
        idx = random.sample(range(len(dfa)), n_missing_vendas)
        dfa.loc[idx, VENDAS_COL] = np.nan

    if n_missing_margem > 0:
        idx = random.sample(range(len(dfa)), n_missing_margem)
        dfa.loc[idx, MARGEM_PCT] = np.nan

    # 2) Outliers em vendas (exagerar vs. máximo atual)
    if n_outliers_vendas > 0:
        idx = random.sample(range(len(dfa)), n_outliers_vendas)
        fator = 50  # 50x o máximo atual
        dfa.loc[idx, VENDAS_COL] = dfa[VENDAS_COL].max() * fator

    # 3) Outliers em margem (fora do intervalo [0, 100])
    if inserir_outliers_margem:
        dfa.loc[random.randrange(len(dfa)), MARGEM_PCT] = -10   # negativo
        dfa.loc[random.randrange(len(dfa)), MARGEM_PCT] = 120   # acima de 100

    # 4) Erros ortográficos em clientes
    if not clientes_errados:
        clientes_errados = ["Kéro", "Shopritee", "Mercado Frescco"]
    for nome_errado in clientes_errados:
        dfa.loc[random.randrange(len(dfa)), "Cliente"] = nome_errado

    return dfa

# -------------------------------
# Pipeline
# -------------------------------
def main():
    # 0) Ler dados
    df = pd.read_excel(INPUT_PATH)
    validar_colunas(df)

    # 1) Remover exportação
    df_sem_export = remover_exportacao(df)
    df_sem_export.to_excel(SEM_EXPORT_PATH, index=False)

    # 2) Expandir para 500 linhas
    df_500 = expandir_para_500(df_sem_export, TARGET_ROWS)
    df_500.to_excel(FINAL_500_PATH, index=False)

    # 3) (Opcional) Anomalias
    df_500_anom = injetar_anomalias(
        df_500,
        n_missing_vendas=4,
        n_missing_margem=4,
        n_outliers_vendas=2,
        inserir_outliers_margem=True,
        clientes_errados=["Kéro", "Shopritee", "Mercado Frescco"]
    )
    df_500_anom.to_excel(FINAL_500_ANOM_PATH, index=False)

    # 4) Resumo rápido no terminal
    print("Linhas (sem exportação):", len(df_sem_export))
    print("Linhas (final 500):     ", len(df_500))
    print("Ficheiros gravados em:  ", OUTPUT_DIR.resolve())

if __name__ == "__main__":
    main()
