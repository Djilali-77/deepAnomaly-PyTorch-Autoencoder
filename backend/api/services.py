import torch
import numpy as np
import joblib
import torch.nn as nn
import sys
sys.path.append('../src')
from model import DeepAnomalyAE
from schemas import TrafficInput, PredictionOutput

INPUT_DIM = 65
THRESHOLD = 0.073

print("Loading model and scaler...")
scaler = joblib.load("../weights/scaler.pkl")

model = DeepAnomalyAE(INPUT_DIM)
model.load_state_dict(torch.load("../weights/autoencoder_model.pth"))
model.eval()

def predict_traffic(data: TrafficInput) -> PredictionOutput:

    user_features = [data.sttl, data.ct_state_ttl, data.sbytes, data.dbytes, data.smean]
    
    full_features = np.zeros((1, INPUT_DIM))
    full_features[0, :5] = user_features
    
    scaled_features = scaler.transform(full_features)

    tensor_features = torch.FloatTensor(scaled_features)

    with torch.no_grad():
        reconstructed = model(tensor_features)
        loss_function = nn.MSELoss()
        mse_loss = loss_function(reconstructed, tensor_features).item()
    
    is_anomaly = (mse_loss > THRESHOLD)
    
    return PredictionOutput(
        is_anomaly=is_anomaly,
        anomaly_score=mse_loss
    )