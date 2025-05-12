# ml/scripts/feature_engineering.py
import pandas as pd
import ta  # Technical Analysis library
import os, sys
import numpy as np

def featurize(symbol):
    """
    Generate technical indicators and features for a stock symbol.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        pd.DataFrame: DataFrame with calculated features
    """
    # Ensure raw data directory exists
    if not os.path.exists(f"data/raw/{symbol}.csv"):
        print(f"Error: Raw data file for {symbol} not found. Run ingest_data.py first.")
        return None
    
    # Read the raw data and fix data types
    try:
        raw = pd.read_csv(f"data/raw/{symbol}.csv")
        
        # Convert Date to datetime
        raw['Date'] = pd.to_datetime(raw['Date'])
        
        # Ensure price columns are numeric
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in raw.columns:
                raw[col] = pd.to_numeric(raw[col], errors='coerce')
        
        # Set Date as index
        raw.set_index('Date', inplace=True)
        
        print(f"Successfully loaded data for {symbol} with shape {raw.shape}")
    except Exception as e:
        print(f"Error processing data: {e}")
        return None
    
    df = raw.copy()
    
    # Calculate daily returns
    df['daily_return'] = df['Close'].pct_change()
    
    # Momentum Indicators
    # RSI (Relative Strength Index)
    df["rsi14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    
    # Moving Averages
    # SMA (Simple Moving Average)
    df["sma20"] = df["Close"].rolling(20).mean()
    df["sma50"] = df["Close"].rolling(50).mean()
    df["sma200"] = df["Close"].rolling(200).mean()
    
    # EMA (Exponential Moving Average)
    df["ema20"] = df["Close"].ewm(span=20, adjust=False).mean()
    
    # Trend Indicators
    # MACD (Moving Average Convergence Divergence)
    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["bb_high"] = bollinger.bollinger_hband()
    df["bb_low"] = bollinger.bollinger_lband()
    df["bb_mid"] = bollinger.bollinger_mavg()
    df["bb_width"] = (df["bb_high"] - df["bb_low"]) / df["bb_mid"]
    
    # Volatility Indicators
    # Average True Range (ATR)
    df["atr"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"], window=14).average_true_range()
    
    # Volume Indicators
    # On-Balance Volume (OBV)
    df["obv"] = ta.volume.OnBalanceVolumeIndicator(df["Close"], df["Volume"]).on_balance_volume()
    
    # Create target variable (next day's movement direction)
    df['target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    
    # Create directory for processed data if it doesn't exist
    os.makedirs("data/processed", exist_ok=True)
    
    # Drop rows with NaN values and save
    df_clean = df.dropna()
    df_clean.to_csv(f"data/processed/{symbol}_features.csv")
    
    # Print summary
    feature_count = len(df_clean.columns) - len(raw.columns) - 1  # Subtract original columns and target
    print(f"Features saved --> data/processed/{symbol}_features.csv")
    print(f"Created {feature_count} new features")
    print(f"Data shape: {df_clean.shape}")
    print(f"Target distribution: {df_clean['target'].value_counts(normalize=True).apply(lambda x: f'{x:.2%}')}")
    
    return df_clean

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python feature_engineering.py <SYMBOL>")
        sys.exit(1)
        
    symbol = sys.argv[1]
    featurize(symbol)
