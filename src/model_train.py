from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score

ROOT = Path(".")
DATA = ROOT / "data" / "processed" / "dataset_biagio_clean.xlsx"
OUT  = ROOT / "reports" / "model_results.xlsx"

TARGET = "Vendas"

def split_temporal(df: pd.DataFrame, target: str):
    """Split temporal 80/20 se houver Ano+Mês; caso contrário usa aleatório."""
    if {"Ano","Mês"}.issubset(df.columns):
        df = df.sort_values(["Ano","Mês"])
        split_idx = int(len(df) * 0.8)
        train_df, test_df = df.iloc[:split_idx], df.iloc[split_idx:]
        X_train, y_train = train_df.drop(columns=[target]), train_df[target]
        X_test,  y_test  = test_df.drop(columns=[target]),  test_df[target]
        return X_train, X_test, y_train, y_test, df
    else:
        X = df.drop(columns=[target])
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test, df

def evaluate(model, X_train, y_train, X_test, y_test):
    """Calcula RMSE, MAPE e R2 no treino e teste."""
    pred_train = model.predict(X_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, pred_train))
    mape_train = mean_absolute_percentage_error(y_train, pred_train)
    r2_train = r2_score(y_train, pred_train)

    pred_test = model.predict(X_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, pred_test))
    mape_test = mean_absolute_percentage_error(y_test, pred_test)
    r2_test = r2_score(y_test, pred_test)

    return rmse_train, mape_train, r2_train, rmse_test, mape_test, r2_test

def evaluate_global(model, df: pd.DataFrame, target: str):
    """Calcula métricas no dataset completo (100%)."""
    X_all = df.drop(columns=[target])
    y_all = df[target]
    pred_all = model.predict(X_all)
    rmse_all = np.sqrt(mean_squared_error(y_all, pred_all))
    mape_all = mean_absolute_percentage_error(y_all, pred_all)
    r2_all = r2_score(y_all, pred_all)
    return rmse_all, mape_all, r2_all

def main():
    df = pd.read_excel(DATA)
    assert TARGET in df.columns, f"Coluna alvo '{TARGET}' não encontrada. Colunas: {list(df.columns)}"

    X_train, X_test, y_train, y_test, df_all = split_temporal(df, TARGET)

    num_cols = X_train.select_dtypes(include=np.number).columns.tolist()
    cat_cols = [c for c in X_train.columns if c not in num_cols]

    preproc = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    rows_tt = []
    rows_all = []

    # Modelo 1: Regressão Linear
    lr = Pipeline(steps=[("prep", preproc), ("model", LinearRegression())])
    lr.fit(X_train, y_train)
    res_lr_tt = evaluate(lr, X_train, y_train, X_test, y_test)
    res_lr_all = evaluate_global(lr, df_all, TARGET)
    rows_tt.append(["Linear Regression"] + list(res_lr_tt))
    rows_all.append(["Linear Regression"] + list(res_lr_all))

    # Modelo 2: Random Forest
    rf = Pipeline(steps=[("prep", preproc),
                         ("model", RandomForestRegressor(n_estimators=300,
                                                        random_state=42,
                                                        n_jobs=-1))])
    rf.fit(X_train, y_train)
    res_rf_tt = evaluate(rf, X_train, y_train, X_test, y_test)
    res_rf_all = evaluate_global(rf, df_all, TARGET)
    rows_tt.append(["Random Forest"] + list(res_rf_tt))
    rows_all.append(["Random Forest"] + list(res_rf_all))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols_tt = ["Modelo", "RMSE_Treino", "MAPE_Treino", "R2_Treino",
               "RMSE_Teste", "MAPE_Teste", "R2_Teste"]
    cols_all = ["Modelo", "RMSE_Global", "MAPE_Global", "R2_Global"]

    df_tt = pd.DataFrame(rows_tt, columns=cols_tt)
    df_all = pd.DataFrame(rows_all, columns=cols_all)

    with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
        df_tt.to_excel(writer, sheet_name="comparacao_modelos", index=False)
        df_all.to_excel(writer, sheet_name="global", index=False)

    print("✅ Split concluído.")
    print("Treino:", X_train.shape, "| Teste:", X_test.shape)
    print("\n=== Comparação (Treino/Teste) ===")
    print(df_tt)
    print("\n=== Métricas Global (100%) ===")
    print(df_all)
    print("\n✅ Resultados salvos em:", OUT)

if __name__ == "__main__":
    main()