import torch
import numpy as np
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def calculate_reconstruction_errors(model: nn.Module, dataloader) -> np.ndarray:
    """
    3. Loop through dataloader, get reconstructed_x.
    4. Calculate MSE per sample (hint: set reduction='none' in MSELoss or compute it manually).
    5. Return all errors as a numpy array.
    """
    criterion = nn.MSELoss(reduction='none')
    model.eval()
    with torch.no_grad():
        all_errors = []
        for batch in dataloader:
            reconstructed_x = model(batch)
            all_errors.append( criterion(reconstructed_x, batch).mean(dim=1) )

    return torch.cat(all_errors).numpy()

def set_dynamic_threshold(train_errors: np.ndarray, k: float = 3.0) -> float:

    mean = np.mean(train_errors)
    std = np.std(train_errors)
    threshold = mean + (k * std)

    return threshold

def predict_anomalies(model: nn.Module, test_dataloader, threshold: float) -> np.ndarray:

    errors = calculate_reconstruction_errors(model, test_dataloader)
    return (errors > threshold).astype(int)

def evaluate_performance(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    
    print(f"Accuracy = {accuracy} \n Precision= {precision} \n Recall= {recall} \n F1= {f1}  \n\n")
    print(f"Confusion matrix = {cm} \n\n")