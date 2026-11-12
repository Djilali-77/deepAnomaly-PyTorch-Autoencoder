import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_clean_data(filepath: str) -> pd.DataFrame:

    df = pd.read_csv(filepath)
    df.drop(columns="id", inplace=True)
    return df
    

def separate_normal_traffic(df: pd.DataFrame) -> pd.DataFrame:

    df = df[df['label'] == 0].copy()
    df.drop(columns=["attack_cat", "label"], inplace=True)

    return df

def preprocess_features(df_train: pd.DataFrame, df_test: pd.DataFrame):

    cat_cols_train = df_train.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    encoded_df_train = pd.get_dummies(df_train, columns=cat_cols_train)
    cat_cols_test = df_test.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    encoded_df_test = pd.get_dummies(df_test, columns=cat_cols_test)

    X_train, X_test = encoded_df_train.align(encoded_df_test, join='left', axis=1, fill_value=0)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    return X_train_scaled, X_test_scaled, scaler