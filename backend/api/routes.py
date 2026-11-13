from fastapi import APIRouter
from schemas import TrafficInput, PredictionOutput
from services import predict_traffic, metrics

router = APIRouter()


@router.post("/predict", response_model=PredictionOutput)
def predict_anomaly(data: TrafficInput):
    return predict_traffic(data)


@router.get("/metrics")
def get_metrics():
    return metrics