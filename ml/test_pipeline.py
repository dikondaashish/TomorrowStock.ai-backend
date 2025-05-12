"""
Test script for the stock prediction pipeline.
This script tests components of the pipeline without 
requiring the full model to be trained.
"""

import os
import pandas as pd
import sys
import json
from datetime import datetime

# Ensure data directories exist
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/sentiment', exist_ok=True)
os.makedirs('models', exist_ok=True)

def check_data_quality(symbol):
    """Check if we have proper feature data for the symbol"""
    features_path = f'data/processed/{symbol}_features.csv'
    
    if not os.path.exists(features_path):
        print(f"Error: Features file not found at {features_path}")
        print("Please run the feature engineering script first.")
        return False
    
    try:
        df = pd.read_csv(features_path, index_col='Date', parse_dates=True)
        print(f"Successfully loaded feature data for {symbol}")
        print(f"Data shape: {df.shape}")
        print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")
        
        # Check for common technical indicators
        expected_columns = ['rsi14', 'sma20', 'ema20', 'macd']
        missing = [col for col in expected_columns if col not in df.columns]
        
        if missing:
            print(f"Warning: Missing expected columns: {missing}")
        else:
            print("All expected technical indicators are present.")
            
        return True
    except Exception as e:
        print(f"Error reading feature data: {e}")
        return False

def simulate_prediction(symbol):
    """Simulate a prediction without a real model"""
    features_path = f'data/processed/{symbol}_features.csv'
    
    if not os.path.exists(features_path):
        return {
            "error": f"Features file not found at {features_path}",
            "direction": None,
            "confidence": None
        }
    
    try:
        # Load the features
        df = pd.read_csv(features_path, index_col='Date', parse_dates=True)
        
        # Get the most recent data point
        latest = df.iloc[-1]
        
        # Simple rule-based prediction (just for testing)
        rsi = latest.get('rsi14', 50)  # Default to neutral if not available
        
        # Very simple rule: if RSI > 50, predict Up, otherwise Down
        direction = "Up" if rsi > 50 else "Down"
        
        # Calculate simple confidence (0.5 = neutral, 1.0 = max confidence)
        # Normalize RSI to 0-1 range centered around 0.5
        confidence = abs(rsi - 50) / 50
        
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "direction": direction,
            "confidence": float(confidence),
            "rsi": float(rsi),
            "note": "This is a simulated prediction for testing purposes."
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "direction": None,
            "confidence": None
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <SYMBOL>")
        sys.exit(1)
        
    symbol = sys.argv[1]
    
    # Check data quality
    if check_data_quality(symbol):
        print("\nGenerating simulated prediction...")
        result = simulate_prediction(symbol)
        print(json.dumps(result, indent=2))
    else:
        print("Data quality check failed. Please fix issues before proceeding.") 