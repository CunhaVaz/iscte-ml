from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Paths
ROOT = Path(".").resolve()
DATA = ROOT / "data" / "processed" / "dataset_biagio_clean.xlsx"
OUT_XLSX = ROOT / "reports" / "feature_importance.xlsx"
OUT_PNG  = ROOT / "reports" / "feature_importance.png"

TARGET = "Vendas"

def main():
    # 1) Load cleaned dataset
    df = pd.read_excel(DATA)
    assert TARGET in df.columns, f"Target column '{TARGET}' not found. Columns: {list(df.columns)}"

    X = df.drop(columns=[TARGET])
    y = df[TARGET].astype(float)

    # 2) Separate types
    num_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]

    # 3) Preprocessing: numeric passthrough, categorical one-hot
    preproc = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ],
        remainder="drop"
    )

    # 4) Pipeline: preproc + RandomForest
    rf = Pipeline(steps=[
        ("prep", preproc),
        ("model", RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=-1))
    ])

    rf.fit(X, y)

    # 5) Feature names after one-hot
    if cat_cols:
        ohe = rf.named_steps["prep"].named_transformers_["cat"]
        cat_names = ohe.get_feature_names_out(cat_cols)
    else:
        cat_names = np.array([])

    feature_names = num_cols + cat_names.tolist()
    importances = rf.named_steps["model"].feature_importances_

    imp_df = (pd.DataFrame({"feature": feature_names, "importance": importances})
                .sort_values("importance", ascending=False))

    # 6) Export Excel
    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    imp_df.to_excel(OUT_XLSX, index=False)

    print("✅ Top most relevant variables:")
    print(imp_df.head(15))
    print(f"\n📂 Ranking saved at: {OUT_XLSX}")

    # 7) (Optional) PNG plot
    try:
        import matplotlib.pyplot as plt
        topN = 15
        top_imp = imp_df.head(topN).iloc[::-1]  # inverted for horizontal bar top-down
        plt.figure(figsize=(9, 6))
        plt.barh(top_imp["feature"], top_imp["importance"], color="#4e79a7")
        plt.title("Feature Importance (Random Forest)")
        plt.xlabel("importance")
        plt.tight_layout()
        plt.savefig(OUT_PNG, dpi=150)
        plt.close()
        print(f"🖼️ Plot saved at: {OUT_PNG}")
    except Exception as e:
        print("⚠️ Could not generate plot:", e)

if __name__ == "__main__":
    main()