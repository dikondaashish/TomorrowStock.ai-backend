from pydantic import BaseModel
from typing import Optional, List

class PredictRequest(BaseModel):
    symbol: str

class PredictResponse(BaseModel):
    direction: str        # "Up" / "Down" / "Neutral"
    confidence: float     # 0.0–1.0
    lower_range: Optional[float]
    upper_range: Optional[float]

class Headline(BaseModel):
    title: str
    url: str

class SentimentResponse(BaseModel):
    score: float          # e.g. -1.0 to +1.0
    headlines: List[Headline]

class HistoryRecord(BaseModel):
    date: str             # ISO date
    predicted: str
    actual: str 