# Stock Sentiment Service

A microservice that analyzes sentiment from news headlines about stocks using the FinBERT model.

## Features

- Fetches stock-related news headlines from NewsAPI
- Analyzes sentiment using a specialized financial sentiment model (FinBERT)
- Caches results to improve performance and reduce API calls
- Provides a RESTful API with FastAPI

## Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:

```
NEWSAPI_KEY=your_newsapi_key_here
CACHE_TTL_SECONDS=3600
USE_GPU=0
```

## Usage

### Start the service

```bash
./run.sh  # Or: uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### API Endpoints

- `GET /` - Service information
- `GET /sentiment/{symbol}` - Get sentiment analysis for a stock symbol
  - Query parameters:
    - `limit`: Maximum number of results to return (default 10, max 50)
- `GET /cache/stats` - Get current cache statistics

### Example Request

```bash
curl -X GET "http://localhost:8001/sentiment/AAPL?limit=5"
```

### Example Response

```json
{
  "symbol": "AAPL",
  "timestamp": "2023-05-12T12:34:56.789Z",
  "results": [
    {
      "title": "Apple Stock Rises After Strong Earnings Report",
      "url": "https://example.com/news/article1",
      "publishedAt": "2023-05-12T10:30:00Z",
      "score": 0.92,
      "label": "POSITIVE"
    },
    ...
  ],
  "avg_score": 0.75,
  "sentiment_summary": "Positive"
}
```

## Architecture

- `main.py` - FastAPI application and endpoints
- `scraper.py` - News API client for fetching headlines
- `analyzer.py` - Sentiment analysis using Hugging Face transformers
- `cache.py` - Caching layer with TTL

## Dependencies

- fastapi
- uvicorn
- transformers
- newsapi-python
- python-dotenv
- cachetools 