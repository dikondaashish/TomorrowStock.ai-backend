import requests
import logging
from app.core.config import settings
from datetime import datetime, timedelta

class NewsApiClient:
    """Client for accessing the News API securely using the stored API key."""
    
    BASE_URL = "https://newsapi.org/v2"
    
    @classmethod
    def get_stock_news(cls, symbol, days_back=7, max_articles=10):
        """
        Get recent news articles about a stock.
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            days_back (int): How many days to look back
            max_articles (int): Maximum number of articles to return
            
        Returns:
            list: List of news articles with title, description, url, etc.
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Format dates for API
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')
        
        # Define company names for better results
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
        
        # Build the query - use company name if available
        company = company_names.get(symbol, symbol)
        query = f"{company} stock OR {symbol} stock"
        
        try:
            # Make request to News API
            response = requests.get(
                f"{cls.BASE_URL}/everything",
                params={
                    'q': query,
                    'from': from_date,
                    'to': to_date,
                    'language': 'en',
                    'sortBy': 'relevancy',
                    'pageSize': max_articles,
                    'apiKey': settings.NEWSAPI_KEY
                },
                timeout=10
            )
            
            # Check for successful response
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                logging.error(f"News API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logging.error(f"Failed to fetch news data: {e}")
            return []
    
    @classmethod
    def get_market_news(cls, max_articles=10):
        """
        Get general market news.
        
        Args:
            max_articles (int): Maximum number of articles to return
            
        Returns:
            list: List of news articles
        """
        try:
            # Make request to News API
            response = requests.get(
                f"{cls.BASE_URL}/top-headlines",
                params={
                    'category': 'business',
                    'language': 'en',
                    'pageSize': max_articles,
                    'apiKey': settings.NEWSAPI_KEY
                },
                timeout=10
            )
            
            # Check for successful response
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                logging.error(f"News API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logging.error(f"Failed to fetch news data: {e}")
            return [] 