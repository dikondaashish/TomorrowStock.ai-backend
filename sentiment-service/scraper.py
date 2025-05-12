import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

# Load environment variables
load_dotenv()

# Initialize the News API client
api = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

def fetch_headlines(symbol: str, page_size: int = 50):
    """
    Fetch news headlines for a given stock symbol.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        page_size: Number of articles to fetch (max 100)
        
    Returns:
        List of article dictionaries with title, url, and publishedAt
    """
    # Construct search query - include company name for better results
    company_names = {
        'AAPL': 'Apple',
        'MSFT': 'Microsoft',
        'GOOGL': 'Google',
        'AMZN': 'Amazon',
        'META': 'Meta Facebook',
        'TSLA': 'Tesla',
        'NVDA': 'Nvidia',
        # Add more mappings as needed
    }
    
    # Use company name if available, otherwise just use the symbol
    company = company_names.get(symbol, symbol)
    query = f"{company} stock OR {symbol} stock"
    
    # Call News API to fetch articles
    resp = api.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",
        page_size=page_size
    )
    
    # Return list of article dictionaries
    return resp.get("articles", [])

if __name__ == "__main__":
    # Simple test to verify functionality
    import json
    
    test_symbol = "AAPL"
    articles = fetch_headlines(test_symbol, page_size=5)
    
    print(f"Fetched {len(articles)} headlines for {test_symbol}:")
    for i, article in enumerate(articles[:3], 1):  # Print first 3 for testing
        print(f"{i}. {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   Published: {article['publishedAt']}")
        print()
