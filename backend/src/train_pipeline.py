import json
import os
import joblib
import torch
from sklearn.model_selection import train_test_split

from utils import load_and_clean_data, separate_normal_traffic, preprocess_features
from dataset import create_dataloader
from model import DeepAnomalyAE
from train import train_autoencoder
from evaluate import (
    calculate_reconstruction_errors,
    set_percentile_threshold,
    evaluate_performance,
    evaluate_scores,
)


def main():
    TRAIN_PATH = "../data/UNSW_NB15_training-set.csv"
    TEST_PATH = "../data/UNSW_NB15_testing-set.csv"
    BATCH_SIZE = 64
    EPOCHS = 50
    LEARNING_RATE = 0.001
    # The threshold is the 95th percentile of the errors on normal validation traffic
    THRESHOLD_PERCENTILE = 95

    print("1. Loading and cleaning data...")
    df_train = load_and_clean_data(TRAIN_PATH)
    df_test = load_and_clean_data(TEST_PATH)
    y_true = df_test["label"].values

    print("2. Keeping only normal traffic for training...")
    df_train_normal = separate_normal_traffic(df_train)
    df_test_features = df_test.drop(columns=["attack_cat", "label"])

    print("3. Preprocessing features...")
    X_train_scaled, X_test_scaled, scaler, info = preprocess_features(df_train_normal, df_test_features)

    # Keep 10% of the normal rows aside, only to choose the threshold
    X_fit, X_val = train_test_split(X_train_scaled, test_size=0.1, random_state=42)

    print("4. Creating DataLoaders...")
    train_loader = create_dataloader(X_fit, BATCH_SIZE, shuffle=True)
    # No shuffling for these two: the errors must stay in the same order as y_true
    val_loader = create_dataloader(X_val, BATCH_SIZE, shuffle=False)
    test_loader = create_dataloader(X_test_scaled, BATCH_SIZE, shuffle=False)

    print("5. Initializing model...")
    model = DeepAnomalyAE(X_fit.shape[1])

    print("6. Training autoencoder...")
    trained_model = train_autoencoder(model, train_loader, EPOCHS, LEARNING_RATE)

    print("7. Choosing the threshold on normal validation traffic...")
    val_errors = calculate_reconstruction_errors(trained_model, val_loader)
    threshold = set_percentile_threshold(val_errors, THRESHOLD_PERCENTILE)
    print(f"Threshold: {threshold:.6f}\n")

    print("8. Scoring the test set...")
    test_errors = calculate_reconstruction_errors(trained_model, test_loader)
    predictions = (test_errors > threshold).astype(int)

    print("9. Evaluating...")
    metrics = evaluate_performance(y_true, predictions)
    metrics.update(evaluate_scores(y_true, test_errors))
    metrics["threshold"] = threshold
    metrics["threshold_percentile"] = THRESHOLD_PERCENTILE

    print("10. Saving everything the API needs...")
    os.makedirs("../weights", exist_ok=True)
    torch.save(trained_model.state_dict(), "../weights/autoencoder_model.pth")
    joblib.dump(scaler, "../weights/scaler.pkl")
    joblib.dump(info, "../weights/preprocessing_info.pkl")
    with open("../weights/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("Done!")


if __name__ == "__main__":
    main()