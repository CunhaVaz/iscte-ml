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
        return X_train, X_test, y_train, y_test
    else:
        return train_test_split(
            df.drop(columns=[target]), df[target],
            test_size=0.2, random_state=42
        )

def evaluate(model, X_train, y_train, X_test, y_test):
    """Calcula RMSE, MAPE e R2 no treino e teste."""
    # treino
    pred_train = model.predict(X_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, pred_train))
    mape_train = mean_absolute_percentage_error(y_train, pred_train)
    r2_train = r2_score(y_train, pred_train)

    # teste
    pred_test = model.predict(X_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, pred_test))
    mape_test = mean_absolute_percentage_error(y_test, pred_test)
    r2_test = r2_score(y_test, pred_test)

    return rmse_train, mape_train, r2_train, rmse_test, mape_test, r2_test

def main():
    # 1) carregar
    df = pd.read_excel(DATA)
    assert TARGET in df.columns, f"Coluna alvo '{TARGET}' não encontrada. Colunas: {list(df.columns)}"

    # 2) split 80/20
    X_train, X_test, y_train, y_test = split_temporal(df, TARGET)

    # separar tipos
    num_cols = X_train.select_dtypes(include=np.number).columns.tolist()
    cat_cols = [c for c in X_train.columns if c not in num_cols]

    # pré-processamento
    preproc = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    results = []

    # 3) Modelo 1: Regressão Linear
    lr = Pipeline(steps=[("prep", preproc), ("model", LinearRegression())])
    lr.fit(X_train, y_train)
    res_lr = evaluate(lr, X_train, y_train, X_test, y_test)
    results.append(["Linear Regression"] + list(res_lr))

    # 4) Modelo 2: Random Forest
    rf = Pipeline(steps=[("prep", preproc),
                         ("model", RandomForestRegressor(n_estimators=300,
                                                        random_state=42,
                                                        n_jobs=-1))])
    rf.fit(X_train, y_train)
    res_rf = evaluate(rf, X_train, y_train, X_test, y_test)
    results.append(["Random Forest"] + list(res_rf))

    # 5) guardar resultados
    results_df = pd.DataFrame(
        results,
        columns=[
            "Modelo",
            "RMSE_Treino", "MAPE_Treino", "R2_Treino",
            "RMSE_Teste", "MAPE_Teste", "R2_Teste"
        ]
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_excel(OUT, index=False)

    print("✅ Split concluído.")
    print("Treino:", X_train.shape, "| Teste:", X_test.shape)
    print("\n✅ Métricas salvas em:", OUT)
    print(results_df)

if __name__ == "__main__":
    main()