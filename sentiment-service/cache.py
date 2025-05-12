import os
from dotenv import load_dotenv
from cachetools import TTLCache, cached
from datetime import datetime

# Load environment variables
load_dotenv()

# Create a time-to-live cache
# maxsize: maximum number of items to store
# ttl: time-to-live in seconds before cache invalidation
cache_ttl = int(os.getenv("CACHE_TTL_SECONDS", 3600))
cache = TTLCache(maxsize=1000, ttl=cache_ttl)

@cached(cache)
def get_cached_sentiment(symbol: str):
    """
    Get sentiment analysis for a stock symbol, with caching.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        
    Returns:
        List of dictionaries with headline info and sentiment scores
    """
    # Import here to avoid circular imports
    from scraper import fetch_headlines
    from analyzer import analyze_headlines
    
    print(f"Cache miss for {symbol} at {datetime.now().isoformat()}")
    print(f"Fetching fresh sentiment data (TTL: {cache_ttl}s)...")
    
    # Fetch headlines and analyze sentiment
    articles = fetch_headlines(symbol)
    results = analyze_headlines(articles)
    
    return results

def get_cache_stats():
    """Get information about the current cache state."""
    return {
        "size": len(cache),
        "maxsize": cache.maxsize,
        "ttl": cache.ttl,
        "currsize": cache.currsize,
        "keys": list(cache.keys())
    }

if __name__ == "__main__":
    # Simple test to verify caching functionality
    test_symbol = "AAPL"
    
    # First call should hit the API
    print(f"First call for {test_symbol}:")
    results1 = get_cached_sentiment(test_symbol)
    print(f"Got {len(results1)} results")
    
    # Second call should use the cache
    print(f"\nSecond call for {test_symbol}:")
    results2 = get_cached_sentiment(test_symbol)
    print(f"Got {len(results2)} results")
    
    # Show cache stats
    print("\nCache stats:", get_cache_stats())
