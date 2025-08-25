from pathlib import Path
import sys
import pandas as pd
import numpy as np
from scipy.stats import zscore

ROOT = Path(".").resolve()
# Permite passar o caminho do excel por argumento:
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "raw" / "dataset_biagio.xlsx"

OUT_DIR = ROOT / "data" / "processed"; OUT_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR = ROOT / "reports"; REP_DIR.mkdir(parents=True, exist_ok=True)

OUT_XLSX = OUT_DIR / "dataset_biagio_clean.xlsx"
SUMMARY = REP_DIR / "cleaning_summary.txt"

def ordenar_temporalmente(df: pd.DataFrame) -> pd.DataFrame:
    cols = set(df.columns.map(str))
    if "Data" in cols:
        return df.sort_values("Data")
    # aceita "Mês" ou "Mes"
    if {"Ano","Mês"}.issubset(cols) or {"Ano","Mes"}.issubset(cols):
        if "Mes" in cols and "Mês" not in cols:
            df = df.rename(columns={"Mes": "Mês"})
        # mapear nomes de mês, se necessário
        if df["Mês"].dtype == object:
            mapa = {"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,
                    "jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}
            df["Mês"] = (df["Mês"].astype(str).str.lower()
                         .map(mapa).fillna(pd.to_numeric(df["Mês"], errors="coerce")))
        return df.sort_values(["Ano","Mês"], kind="mergesort")
    return df  # se não houver colunas temporais

def main():
    if not RAW.exists():
        raise FileNotFoundError(f"❌ Não encontrei o ficheiro de origem: {RAW}")

    df = pd.read_excel(RAW)
    orig_n, orig_p = df.shape

    # 1) Ordenação temporal
    df = ordenar_temporalmente(df)

    # 2) Imputação de omissos (mediana) em Vendas e Margem_%
    imput = {}
    for c in ["Vendas", "Margem_%"]:
        if c in df.columns:
            n_before = int(df[c].isna().sum())
            if n_before:
                df[c] = df[c].fillna(df[c].median())
            imput[c] = n_before

    # 3) Remoção de outliers (|z|>3) em QUALQUER coluna numérica
    removed = 0
    num = df.select_dtypes(include="number")
    if not num.empty:
        Z = num.apply(zscore)
        mask_ok = (Z.abs() <= 3).all(axis=1)
        removed = int((~mask_ok).sum())
        df = df[mask_ok].copy()

    # 4) Correções de ortografia em 'Cliente'
    corr = {"Mercado Frescco": "Mercado Fresco", "Kéro": "Kero", "Shopritee": "Shoprite"}
    corr_counts = {}
    if "Cliente" in df.columns:
        for k, v in corr.items():
            corr_counts[k] = int((df["Cliente"] == k).sum())
        df["Cliente"] = df["Cliente"].replace(corr)

    # 5) Duplicados
    dups = int(df.duplicated().sum())
    if dups:
        df = df.drop_duplicates()

    # 6) Guardar e escrever resumo
    df.to_excel(OUT_XLSX, index=False)

    lines = []
    lines += [
        "=== LIMPEZA DO DATASET ===",
        f"Origem: {RAW}",
        f"Dimensão original: {orig_n} linhas × {orig_p} colunas",
        f"Dimensão final   : {len(df)} linhas × {df.shape[1]} colunas",
        "",
        "— Omissos imputados (mediana):"
    ]
    for c in ["Vendas", "Margem_%"]:
        if c in imput:
            lines.append(f"  • {c}: {imput[c]} → 0")

    lines += [
        "",
        f"— Outliers removidos (|z|>3): {removed} linhas",
        "",
        f"— Duplicados removidos: {dups}",
        "",
        "— Ortografia (Cliente) corrigida:"
    ]
    if corr_counts:
        for k, v in corr_counts.items():
            lines.append(f"  • {k} → {corr[k]} : {v} ocorrências")
    else:
        lines.append("  • coluna 'Cliente' não existe; não aplicável.")

    SUMMARY.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n✅ Ficheiro limpo: {OUT_XLSX}")

if __name__ == "__main__":
    main()
