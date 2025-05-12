from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.schemas import PredictRequest, PredictResponse, SentimentResponse, HistoryRecord
from app.firebase_auth import get_current_user
from app.db import get_db, init_db
from app.predictor import Predictor
from app.sentiment import SentimentAnalyzer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Stock Predictor API",
    description="API for stock price prediction",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()                     # Create tables / connect to DB
    Predictor.load_model()        # Load ML model into memory

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Predictor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest, db=Depends(get_db), user=Depends(get_current_user)):
    result = Predictor.predict(req.symbol)
    if result is None:
        raise HTTPException(404, "Symbol not found")
    
    # Log prediction to database (optional)
    # db.log_prediction(user["uid"], req.symbol, result.direction, result.confidence)
    
    return result

@app.get("/sentiment", response_model=SentimentResponse)
def sentiment(symbol: str, db=Depends(get_db), user=Depends(get_current_user)):
    return SentimentAnalyzer.analyze(symbol)

@app.get("/history", response_model=List[HistoryRecord])
def history(db=Depends(get_db), user=Depends(get_current_user)):
    # Extract user ID from Firebase token
    user_id = user.get("uid")
    if not user_id:
        raise HTTPException(400, "Invalid user information")
    
    return db.get_prediction_history(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 