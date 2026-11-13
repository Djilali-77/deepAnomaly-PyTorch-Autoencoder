from pydantic import BaseModel

class TrafficInput(BaseModel):

    sttl : int
    ct_state_ttl : int
    sbytes : int
    dbytes : int
    smean : int

class PredictionOutput(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    threshold: float