from fastapi import APIRouter
from schemas import TrafficInput, PredictionOutput
from services import predict_traffic

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
def predict_anomaly(data: TrafficInput):

    result = predict_traffic(data)
    return result