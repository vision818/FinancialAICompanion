import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol):
    """
    Fetch stock data using yfinance
    """
    try:
        # Get data for the last year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            raise Exception("No data found for this symbol")
            
        return data
    except Exception as e:
        raise Exception(f"Error fetching stock data: {str(e)}")
