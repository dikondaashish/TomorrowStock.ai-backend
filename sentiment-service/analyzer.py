import os
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables
load_dotenv()

# Load the sentiment analysis model
# This is done once at module import time to avoid reloading
nlp = pipeline(
    "sentiment-analysis",
    model="yjernite/finbert-tone",
    device=0 if os.getenv("USE_GPU", "0") == "1" else -1
)

def analyze_headlines(articles):
    """
    Analyze sentiment for a list of news headlines.
    
    Args:
        articles: List of article dictionaries from the News API
        
    Returns:
        List of dictionaries with article info and sentiment scores
    """
    if not articles:
        return []
    
    # Extract headline texts
    texts = [art["title"] for art in articles]
    
    # Perform sentiment analysis
    print(f"Analyzing sentiment for {len(texts)} headlines...")
    results = nlp(texts)
    
    # Combine article data with sentiment results
    output = []
    for art, res in zip(articles, results):
        # Convert score to positive or negative value based on label
        # POSITIVE → keep score as positive
        # NEGATIVE → make score negative
        score = res["score"] if res["label"] == "POSITIVE" else -res["score"]
        
        output.append({
            "title": art["title"],
            "url": art["url"],
            "publishedAt": art["publishedAt"],
            "score": float(score),
            "label": res["label"]
        })
    
    # Sort by absolute score (strongest sentiment first)
    output.sort(key=lambda x: abs(x["score"]), reverse=True)
    
    return output

if __name__ == "__main__":
    # Simple test to verify functionality
    from scraper import fetch_headlines
    import json
    
    test_symbol = "AAPL"
    articles = fetch_headlines(test_symbol, page_size=5)
    results = analyze_headlines(articles)
    
    print(f"\nSentiment Analysis Results for {test_symbol}:")
    for i, result in enumerate(results, 1):
        sentiment = "POSITIVE" if result["score"] > 0 else "NEGATIVE"
        magnitude = abs(result["score"])
        print(f"{i}. {result['title']}")
        print(f"   Sentiment: {sentiment} (score: {result['score']:.4f})")
        print()
