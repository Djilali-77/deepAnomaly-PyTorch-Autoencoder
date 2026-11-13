import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Columns whose biggest value is above this get a log transform
LOG_THRESHOLD = 100


def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df = df.drop(columns="id")
    return df


def separate_normal_traffic(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["label"] == 0].copy()
    df = df.drop(columns=["attack_cat", "label"])
    return df


def apply_log_transform(df: pd.DataFrame, log_columns: list) -> pd.DataFrame:
    # Columns like sbytes go up to millions. Without this, MinMaxScaler would
    # squeeze almost every row near 0 and the model could not tell them apart.
    df = df.copy()
    for col in log_columns:
        df[col] = np.log1p(df[col].clip(lower=0))
    return df


def preprocess_features(df_train: pd.DataFrame, df_test: pd.DataFrame):
    # One-hot encode the text columns (proto, service, state)
    cat_cols = df_train.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    train_encoded = pd.get_dummies(df_train, columns=cat_cols).astype(float)
    test_encoded = pd.get_dummies(df_test, columns=cat_cols)

    # The test set must have the same columns, in the same order, as train
    test_encoded = test_encoded.reindex(columns=train_encoded.columns, fill_value=0).astype(float)

    # A typical normal flow in raw units (before log and scaling).
    # The API uses it to fill every feature the user does not type in.
    normal_medians = train_encoded.median()
    for col in cat_cols:
        group = [c for c in train_encoded.columns if c.startswith(col + "_")]
        normal_medians[group] = 0.0
        # For text columns we keep the most common value in normal traffic
        normal_medians[train_encoded[group].mean().idxmax()] = 1.0

    log_columns = [c for c in train_encoded.columns if train_encoded[c].max() > LOG_THRESHOLD]
    train_encoded = apply_log_transform(train_encoded, log_columns)
    test_encoded = apply_log_transform(test_encoded, log_columns)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(train_encoded)
    X_test_scaled = scaler.transform(test_encoded)

    info = {
        "columns": train_encoded.columns.tolist(),
        "log_columns": log_columns,
        "medians": normal_medians,
    }
    return X_train_scaled, X_test_scaled, scaler, info