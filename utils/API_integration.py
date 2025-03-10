import requests

def get_bitcoin_data():
    """
    Fetch the latest Bitcoin price and market data from CoinGecko API.
    """
    url_price = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    url_news = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"
    
    try:
        # Get Bitcoin price
        price_response = requests.get(url_price)
        price_data = price_response.json()
        bitcoin_price = price_data['bitcoin']['usd']
        
        # Get Bitcoin market chart data (price movement over the last day)
        news_response = requests.get(url_news)
        news_data = news_response.json()
        
        # Return both the price and the market chart data
        return bitcoin_price, news_data
    
    except Exception as e:
        return f"Error fetching data: {e}"

def get_bitcoin_news():
    """
    Fetch the latest news about Bitcoin from CryptoPanic API.
    """
    url_news = "https://cryptopanic.com/api/v1/posts/?auth_token=06fb77df0418216cf54dc006fa336c9944fbb8fe&filters=currencies"
    
    try:
        response = requests.get(url_news)
        news_data = response.json()
        
        # Extract news related to Bitcoin
        bitcoin_news = []
        for post in news_data['results']:
            if 'bitcoin' in post['title'].lower():
                bitcoin_news.append(post['title'])
        
        return bitcoin_news
    
    except Exception as e:
        return f"Error fetching news: {e}"

