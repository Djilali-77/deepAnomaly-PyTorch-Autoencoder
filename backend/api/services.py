import json
import sys

import joblib
import pandas as pd
import torch
import torch.nn as nn

sys.path.append("../src")
from model import DeepAnomalyAE
from utils import apply_log_transform
from schemas import TrafficInput, PredictionOutput

print("Loading model, scaler and preprocessing info...")
scaler = joblib.load("../weights/scaler.pkl")
info = joblib.load("../weights/preprocessing_info.pkl")
with open("../weights/metrics.json") as f:
    metrics = json.load(f)

COLUMNS = info["columns"]
LOG_COLUMNS = info["log_columns"]
MEDIANS = info["medians"]
# The threshold comes from training, so the API and the training always agree
THRESHOLD = metrics["threshold"]

model = DeepAnomalyAE(len(COLUMNS))
model.load_state_dict(torch.load("../weights/autoencoder_model.pth"))
model.eval()


def predict_traffic(data: TrafficInput) -> PredictionOutput:
    # Start from a normal flow, then overwrite it with the 5 values the user typed
    row = MEDIANS.copy()
    row["sttl"] = data.sttl
    row["ct_state_ttl"] = data.ct_state_ttl
    row["sbytes"] = data.sbytes
    row["dbytes"] = data.dbytes
    row["smean"] = data.smean

    # Same steps as training: same column order, log transform, then scaling
    df_input = pd.DataFrame([row], columns=COLUMNS)
    df_input = apply_log_transform(df_input, LOG_COLUMNS)
    scaled_features = scaler.transform(df_input)
    tensor_features = torch.FloatTensor(scaled_features)

    with torch.no_grad():
        reconstructed = model(tensor_features)
        mse_loss = nn.MSELoss()(reconstructed, tensor_features).item()

    return PredictionOutput(
        is_anomaly=bool(mse_loss > THRESHOLD),
        anomaly_score=mse_loss,
        threshold=THRESHOLD,
    )