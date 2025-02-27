import yfinance as yf
print(yf.Ticker("NVDA").history(period="5d"))
print(yf.download("NVDA", period="5d"))
