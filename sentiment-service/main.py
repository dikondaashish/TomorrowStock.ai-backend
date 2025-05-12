import os
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Import cache module
from cache import get_cached_sentiment, get_cache_stats

# Define Pydantic models for request/response validation
class SentimentItem(BaseModel):
    title: str
    url: str
    publishedAt: str
    score: float
    label: Optional[str] = None

class SentimentResponse(BaseModel):
    symbol: str
    timestamp: str
    results: List[SentimentItem]
    avg_score: float
    sentiment_summary: str
    
class CacheStatsResponse(BaseModel):
    size: int
    maxsize: int
    ttl: int
    currsize: int
    keys: List[str]

# Create FastAPI app
app = FastAPI(
    title="Stock Sentiment Service",
    description="API for sentiment analysis of stock-related news headlines",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define routes
@app.get("/")
async def root():
    return {
        "service": "Stock Sentiment Analysis API",
        "version": "1.0.0",
        "endpoints": [
            "/sentiment/{symbol}",
            "/cache/stats"
        ]
    }

@app.get("/sentiment/{symbol}", response_model=SentimentResponse)
async def sentiment(symbol: str, limit: int = Query(10, ge=1, le=50)):
    """
    Get sentiment analysis for news about a stock.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        limit: Maximum number of results to return (default 10, max 50)
    """
    try:
        # Get sentiment data with caching
        results = get_cached_sentiment(symbol.upper())
        
        # Limit the number of results
        results = results[:limit]
        
        # Calculate average sentiment score
        if results:
            avg_score = sum(item["score"] for item in results) / len(results)
        else:
            avg_score = 0.0
        
        # Generate a summary of sentiment
        sentiment_summary = get_sentiment_summary(avg_score)
        
        # Return formatted response
        return {
            "symbol": symbol.upper(),
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "avg_score": avg_score,
            "sentiment_summary": sentiment_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment fetch error: {str(e)}")

@app.get("/cache/stats", response_model=CacheStatsResponse)
async def cache_stats():
    """Get current cache statistics."""
    return get_cache_stats()

def get_sentiment_summary(score: float) -> str:
    """Generate a human-readable summary of sentiment score."""
    if score > 0.5:
        return "Strongly Positive"
    elif score > 0.2:
        return "Positive"
    elif score > 0.05:
        return "Slightly Positive"
    elif score > -0.05:
        return "Neutral"
    elif score > -0.2:
        return "Slightly Negative"
    elif score > -0.5:
        return "Negative"
    else:
        return "Strongly Negative"

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting sentiment service on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
