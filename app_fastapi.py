from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn
import os

# Configuration
MODEL_PATH = "fraud_model_xgboost.pkl"
METADATA_PATH = "model_metadata.pkl"

app = FastAPI(title="Fraud Detection API", version="1.0")

# Load Model and Metadata
try:
    model = joblib.load(MODEL_PATH)
    metadata = joblib.load(METADATA_PATH)
    THRESHOLD = metadata.get('threshold', 0.5)
    print(f"Model loaded. Threshold set to {THRESHOLD}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    metadata = {}

class TransactionInput(BaseModel):
    transaction_hour: int
    day_of_week: int
    age: int
    gender: str
    home_country: str
    transaction_country: str
    merchant_category: str
    merchant_base_risk: float
    transaction_type: str
    card_type: str
    device: str
    amount: float
    avg_30d_amount: float
    previous_transactions_24h: int
    last_hour_transactions: int
    balance: float
    ip_risk_score: float
    is_foreign: int
    device_mismatch: int
    location_change: int
    amount_anomaly: float
    hour_anomaly: int
    # Add other fields if necessary based on training data

@app.get("/health")
def health_check():
    return {"status": "active", "model_loaded": model is not None}

@app.post("/predict")
def predict(transaction: TransactionInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input to DataFrame
        data = transaction.dict()
        df = pd.DataFrame([data])
        
        # Predict probability
        proba = model.predict_proba(df)[0][1]
        
        # Determine fraud status based on threshold
        is_fraud = bool(proba >= THRESHOLD)
        
        return {
            "fraud_probability": float(proba),
            "is_fraud": is_fraud,
            "threshold_used": float(THRESHOLD),
            "risk_level": "High" if proba > 0.8 else "Medium" if proba > 0.4 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
