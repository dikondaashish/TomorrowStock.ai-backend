import yfinance as yf
import pandas as pd
import sys, os

def download(symbol, start="2015-01-01", end=None):
    """
    Download historical stock data for a specific symbol.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., 'AAPL')
        start (str): Start date in YYYY-MM-DD format
        end (str): End date in YYYY-MM-DD format, defaults to today
    
    Returns:
        None: Saves data to CSV file
    """
    # Download data
    data = yf.download(symbol, start=start, end=end or pd.Timestamp.today().strftime('%Y-%m-%d'))
    
    # Clean up the data frame
    df = data.copy()
    df.reset_index(inplace=True)  # Make Date a column
    
    # Make sure directory exists
    os.makedirs("data/raw", exist_ok=True)
    
    # Save to CSV
    df.to_csv(f"data/raw/{symbol}.csv", index=False)
    
    # Print summary
    print(f"Saved raw data for {symbol} --> data/raw/{symbol}.csv")
    print(f"Downloaded {len(df)} rows of data")
    print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    
    # Display basic statistics - use float conversion to avoid Series formatting issues
    print("\nBasic Statistics:")
    close_mean = float(df['Close'].mean())
    close_max = float(df['Close'].max()) 
    close_min = float(df['Close'].min())
    print(f"Average Close Price: ${close_mean:.2f}")
    print(f"Highest Close Price: ${close_max:.2f}")
    print(f"Lowest Close Price: ${close_min:.2f}")
    
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_data.py <SYMBOL> [START_DATE] [END_DATE]")
        sys.exit(1)
        
    symbol = sys.argv[1]
    start_date = sys.argv[2] if len(sys.argv) > 2 else "2015-01-01"
    end_date = sys.argv[3] if len(sys.argv) > 3 else None
    
    download(symbol, start=start_date, end=end_date)
