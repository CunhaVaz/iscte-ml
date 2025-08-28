from pathlib import Path
import pandas as pd
import sweetviz as sv

# Paths
ROOT = Path(".").resolve()
DATA = ROOT / "data" / "processed" / "dataset_biagio_clean.xlsx"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

XLSX_OUT = REPORTS / "eda_clean_outputs.xlsx"
TXT_OUT = REPORTS / "eda_clean_summary.txt"
HTML_OUT = REPORTS / "eda_sweetviz_clean.html"

def main():
    # Read cleaned dataset
    df = pd.read_excel(DATA)

    # Descriptive statistics
    resumo = []
    resumo.append(f"Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
    resumo.append("\nColumns:")
    resumo.extend([f"- {c} ({df[c].dtype})" for c in df.columns])

    resumo.append("\nStatistical summary:")
    resumo.append(str(df.describe(include="all").transpose()))

    resumo.append("\nMissing values per column:")
    resumo.append(str(df.isna().sum()))

    # Save TXT
    TXT_OUT.write_text("\n".join(resumo), encoding="utf-8")

    # Save Excel
    with pd.ExcelWriter(XLSX_OUT, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="data", index=False)
        df.describe().to_excel(writer, sheet_name="statistics")

    # Generate Sweetviz report
    try:
        report = sv.analyze(df)
        report.show_html(str(HTML_OUT), open_browser=False)
    except Exception as e:
        print(f"Sweetviz error: {e}")

    print("\n".join(resumo))
    print(f"\n✅ Excel EDA (clean): {XLSX_OUT}")
    print(f"✅ Summary TXT (clean): {TXT_OUT}")
    print(f"✅ Sweetviz HTML (clean): {HTML_OUT}")

if __name__ == "__main__":
    main()