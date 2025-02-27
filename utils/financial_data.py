import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        print(f"Fetching data for {symbol} from {start_date} to {end_date}")
        print(data.head())  # Print the first few rows for debugging
        
        if data.empty:
            raise Exception("No data found for this symbol")
            
        return data
    except Exception as e:
        raise Exception(f"Error fetching stock data: {str(e)}")
