from utils import load_and_clean_data, separate_normal_traffic, preprocess_features
from dataset import create_dataloader
from model import DeepAnomalyAE
from train import train_autoencoder
from evaluate import calculate_reconstruction_errors, set_dynamic_threshold, predict_anomalies, evaluate_performance
import torch
import joblib

def main():
    TRAIN_PATH = "../data/UNSW_NB15_training-set.csv"
    TEST_PATH = "../data/UNSW_NB15_testing-set.csv"
    BATCH_SIZE = 64
    EPOCHS = 50
    LEARNING_RATE = 0.001
    K_THRESHOLD = 0.5

    print("1. Loading and cleaning data...")
    df_train = load_and_clean_data(TRAIN_PATH)
    
    df_test = load_and_clean_data(TEST_PATH)
    y_true = df_test['label'].values

    print("2. Separating normal traffic for training...")
    df_train_normal = separate_normal_traffic(df_train)
    df_test.drop(columns=["attack_cat", "label"], inplace=True)
    df_test.dropna(subset=['label'], inplace=True)

    print("3. Preprocessing features...")
    X_train_scaled, X_test_scaled, scaler = preprocess_features(df_train_normal, df_test)

    print("4. Creating DataLoaders...")
    train_loader = create_dataloader(X_train_scaled, BATCH_SIZE)
    test_loader = create_dataloader(X_test_scaled, BATCH_SIZE)

    print("5. Initializing Model...")
    input_dim = X_train_scaled.shape[1]
    model = DeepAnomalyAE(input_dim)

    print("6. Training Autoencoder...")
    trained_model = train_autoencoder(model, train_loader, EPOCHS, LEARNING_RATE)

    print("7. Evaluating and Setting Threshold...")
    train_errors = calculate_reconstruction_errors(trained_model, train_loader)
    threshold = set_dynamic_threshold(train_errors, K_THRESHOLD)
    print(f"Dynamic Threshold set to: {threshold:.4f}")

    print("8. Predicting Anomalies on Test Set...")
    predictions = predict_anomalies(trained_model, test_loader, threshold)

    print("9. Evaluating Final Performance...")
    evaluate_performance(y_true, predictions)
    
    print("Done! The maestro has finished the symphony.")

    print("10. Saving Artifacts for API...")
    torch.save(trained_model.state_dict(), "../weights/autoencoder_model.pth")
    joblib.dump(scaler, "../weights/scaler.pkl")
    
if __name__ == "__main__":
    main()




# Accuracy = 0.49436428120293446 
# Precision= 0.5502361178961082 
# Recall= 0.44723374216888734 
# F1= 0.4934167295383193  