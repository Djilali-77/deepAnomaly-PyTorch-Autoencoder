import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, average_precision_score,
)


def calculate_reconstruction_errors(model: nn.Module, dataloader) -> np.ndarray:
    # reduction="none" gives one error per row, so every flow gets its own score
    criterion = nn.MSELoss(reduction="none")
    model.eval()
    all_errors = []
    with torch.no_grad():
        for batch in dataloader:
            reconstructed_x = model(batch)
            all_errors.append(criterion(reconstructed_x, batch).mean(dim=1))
    return torch.cat(all_errors).numpy()


def set_percentile_threshold(normal_errors: np.ndarray, percentile: float = 95.0) -> float:
    # Anything above what 95% of normal traffic reaches is called an anomaly
    return float(np.percentile(normal_errors, percentile))


def evaluate_scores(y_true, errors: np.ndarray) -> dict:
    # These two do not depend on the threshold, so they show if the model itself works
    roc_auc = roc_auc_score(y_true, errors)
    pr_auc = average_precision_score(y_true, errors)
    print(f"ROC-AUC = {roc_auc:.4f}")
    print(f"PR-AUC = {pr_auc:.4f}\n")
    return {"roc_auc": float(roc_auc), "pr_auc": float(pr_auc)}


def evaluate_performance(y_true, y_pred) -> dict:
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    # False positive rate: how many normal flows we wrongly flagged as attacks
    fpr = fp / (fp + tn)

    print(f"Accuracy = {accuracy:.4f}")
    print(f"Precision = {precision:.4f}")
    print(f"Recall = {recall:.4f}")
    print(f"F1 = {f1:.4f}")
    print(f"False positive rate = {fpr:.4f}")
    print(f"Confusion matrix:\n[[{tn} {fp}]\n [{fn} {tp}]]\n")

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "fpr": float(fpr),
    }