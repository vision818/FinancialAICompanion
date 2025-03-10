import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_portfolio_data(portfolio_type):
    """
    Fetch historical stock data for a given portfolio type.
    Returns a combined dataframe representing portfolio performance.
    """
    portfolios = {
        "Growth": ["AAPL", "NVDA", "GOOGL", "TSLA", "AMZN"],
        "Income": ["JNJ", "PG", "KO", "XOM", "PFE"],
        "Balanced": ["MSFT", "BRK-B", "V", "MA", "JPM"],
        "Tech-Focused": ["AMD", "META", "NFLX", "CRM", "ADBE"],
        "Sustainable": ["ENPH", "TSLA", "NEE", "PLUG", "SEDG"],
        "Custom": []  # Can be updated dynamically by user input
    }

    # Get stock list for the selected portfolio
    symbols = portfolios.get(portfolio_type, [])
    if not symbols:
        raise Exception(f"No stocks defined for portfolio type: {portfolio_type}")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Fetch historical data for all stocks in the portfolio
    portfolio_data = {}
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"⚠️ No data found for {symbol}")
                continue
            
            portfolio_data[symbol] = data["Close"]  # Store only closing prices

        except Exception as e:
            print(f"⚠️ Error fetching data for {symbol}: {str(e)}")

    if not portfolio_data:
        raise Exception("No valid stock data retrieved for this portfolio")

    # Combine stock data into a single DataFrame
    portfolio_df = pd.DataFrame(portfolio_data)

    # Calculate portfolio return (equal-weighted)
    portfolio_df["Portfolio Value"] = portfolio_df.mean(axis=1)

    print(f"✅ Portfolio data fetched for {portfolio_type}")
    print(portfolio_df.head())  # Debugging output

    return portfolio_df
