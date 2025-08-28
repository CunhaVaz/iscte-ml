from pathlib import Path
import sys
import numpy as np
import pandas as pd
import sweetviz as sv

ROOT = Path(".").resolve()
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "raw" / "dataset_biagio.xlsx"

REPORTS = ROOT / "reports"; REPORTS.mkdir(parents=True, exist_ok=True)
XLSX_OUT = REPORTS / "eda_raw_outputs.xlsx"
TXT_OUT  = REPORTS / "eda_raw_summary.txt"
HTML_OUT = REPORTS / "eda_raw_sweetviz.html"

def z_outliers_count(s: pd.Series, z=3.0) -> int:
    if not np.issubdtype(s.dtype, np.number):
        return 0
    m, sd = s.mean(), s.std()
    if pd.isna(sd) or sd == 0:
        return 0
    return int(((s - m).abs() > z * sd).sum())

def main():
    if not DATA.exists():
        raise FileNotFoundError(f"❌ Não encontrei o dataset original: {DATA}")
    df = pd.read_excel(DATA)
    n, p = df.shape

    tipos = df.dtypes.rename("Tipo").to_frame()
    missing = df.isna().sum().rename("Omissos").to_frame()
    duplicados = int(df.duplicated().sum())
    stats = df.describe(include="all").transpose()

    out_counts = pd.Series(
        {c: z_outliers_count(df[c]) for c in df.select_dtypes(include="number").columns},
        name="N_outliers(|z|>3)"
    ).to_frame()

    corr = df.corr(numeric_only=True)

    tops = {}
    if "Cliente" in df.columns:
        tops["top_clientes"] = (df["Cliente"].astype(str).value_counts(dropna=False)
                                .rename_axis("Cliente").rename("freq").reset_index().head(10))
    if "Produto" in df.columns:
        tops["top_produtos"] = (df["Produto"].astype(str).value_counts(dropna=False)
                                .rename_axis("Produto").rename("freq").reset_index().head(10))

    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as w:
        pd.DataFrame({"Fonte":[str(DATA.resolve())],"Linhas":[n],"Colunas":[p]}).to_excel(w,"meta",index=False)
        df.head(20).to_excel(w,"primeiras_20",index=False)
        tipos.to_excel(w,"tipos")
        stats.to_excel(w,"estatisticas")
        missing.reset_index().rename(columns={"index":"Coluna"}).to_excel(w,"omissos",index=False)
        pd.DataFrame({"Duplicados_totais":[duplicados]}).to_excel(w,"duplicados",index=False)
        if not out_counts.empty:
            out_counts.reset_index().rename(columns={"index":"Coluna"}).to_excel(w,"outliers_z3",index=False)
        if corr is not None and not corr.empty:
            corr.to_excel(w,"correlacoes")
        for name, dft in tops.items():
            dft.to_excel(w, name, index=False)

    resumo = [
        "=== EDA (dados ORIGINAIS) ===",
        f"Fonte: {DATA}",
        f"Dimensão: {n} linhas × {p} colunas",
        f"Omissos totais: {int(missing['Omissos'].sum())}",
        f"Duplicados: {duplicados}",
        "Outliers (|z|>3) por coluna numérica:",
    ]
    if not out_counts.empty:
        resumo.append(out_counts.sort_values("N_outliers(|z|>3)", ascending=False).head(10).to_string())
    TXT_OUT.write_text("\n".join(resumo), encoding="utf-8")

    try:
        sv.analyze(df).show_html(str(HTML_OUT), open_browser=False)
    except Exception as e:
        with TXT_OUT.open("a", encoding="utf-8") as f:
            f.write(f"\n⚠️ Sweetviz não gerado: {e}\n")

    print("\n".join(resumo))
    print(f"\n✅ Excel EDA (raw): {XLSX_OUT}")
    print(f"✅ Summary TXT (raw): {TXT_OUT}")
    print(f"✅ Sweetviz HTML (raw): {HTML_OUT if HTML_OUT.exists() else '(não gerado)'}")

if __name__ == "__main__":
    main()

   # src/eda_raw.py

from pathlib import Path
import pandas as pd
import sweetviz as sv

# Caminho para os dados brutos
DATA = Path("data/raw/dataset_biagio.xlsx")
XLSX_OUT = Path("reports/eda_raw_outputs.xlsx")
TXT_OUT = Path("reports/eda_raw_summary.txt")
HTML_OUT = Path("reports/eda_raw_sweetviz.html")

def main():
    # Carregar dataset original
    df = pd.read_excel(DATA)

    resumo = []
    resumo.append(f"Dimensão: {df.shape[0]} linhas x {df.shape[1]} colunas")
    resumo.append(f"Colunas: {list(df.columns)}")
    resumo.append(f"Valores omissos:\n{df.isna().sum()}")
    resumo.append(f"Duplicados: {df.duplicated().sum()}")

    # Guardar resumo em TXT
    TXT_OUT.write_text("\n".join(resumo), encoding="utf-8")

    # Guardar estatísticas descritivas em Excel
    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as writer:
        df.describe(include="all").T.to_excel(writer, sheet_name="estatisticas")
        df.head(20).to_excel(writer, sheet_name="primeiras_20", index=False)

    # Gerar relatório Sweetviz
    try:
        report = sv.analyze(df)
        report.show_html(str(HTML_OUT), open_browser=False)
    except Exception as e:
        TXT_OUT.write_text(f"\n⚠️ Sweetviz não gerado: {e}\n", encoding="utf-8")

    print("\n".join(resumo))
    print(f"\n✅ Excel EDA (raw): {XLSX_OUT}")
    print(f"✅ Summary TXT (raw): {TXT_OUT}")
    print(f"✅ Sweetviz HTML (raw): {HTML_OUT if HTML_OUT.exists() else '(não gerado)'}")

if __name__ == "__main__":
    main() 
    