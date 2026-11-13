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

print("Loading model, scaler, and column map...")
scaler = joblib.load("../weights/scaler.pkl")
expected_columns = joblib.load("../weights/expected_columns.pkl") # Load columns

model = DeepAnomalyAE(INPUT_DIM)
model.load_state_dict(torch.load("../weights/autoencoder_model.pth"))
model.eval()

def predict_traffic(data: TrafficInput) -> PredictionOutput:
    # 1. Create a zeroed dictionary for all 65 features
    feature_dict = {col: 0.0 for col in expected_columns}
    
    # 2. Inject user data into the exact correct keys
    feature_dict['sttl'] = data.sttl
    feature_dict['ct_state_ttl'] = data.ct_state_ttl
    feature_dict['sbytes'] = data.sbytes
    feature_dict['dbytes'] = data.dbytes
    feature_dict['smean'] = data.smean
    
    # 3. Convert to 1D array in the exact order the scaler expects
    ordered_features = np.array([[feature_dict[col] for col in expected_columns]])
    
    # 4. Scale and predict
    scaled_features = scaler.transform(ordered_features)
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