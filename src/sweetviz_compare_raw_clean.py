import pandas as pd
import sweetviz as sv
from pathlib import Path

print("🚀 Sweetviz Raw vs Clean a arrancar…")

RAW = Path("data/raw/dataset_biagio.xlsx")
CLEAN = Path("data/processed/dataset_biagio_clean.xlsx")
REPORTS = Path("reports"); REPORTS.mkdir(exist_ok=True)
OUT_HTML = REPORTS / "sweetviz_raw_vs_clean.html"

def main():
    # Carregar datasets
    df_raw = pd.read_excel(RAW)
    df_clean = pd.read_excel(CLEAN)

    print(f"📊 Dataset bruto: {df_raw.shape} | Dataset limpo: {df_clean.shape}")

    # Comparar Raw vs Clean
    report = sv.compare([df_raw, "Raw"], [df_clean, "Clean"])
    report.show_html(str(OUT_HTML), open_browser=False)

    print(f"✅ Relatório Sweetviz gerado em: {OUT_HTML.resolve()}")

if __name__ == "__main__":
    main()