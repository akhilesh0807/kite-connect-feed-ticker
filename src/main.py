from kiteconnect import KiteConnect, KiteTicker

from brokers.kite.auth import KiteAuth
from brokers.kite.kitedatafeed import KiteDataFeed

API_KEY = "dummy"
API_SECRET = "dummy"
ACCESS_TOKEN = "dummy"

if __name__ == '__main__':
    auth = KiteAuth(api_key=API_KEY, api_secret=API_SECRET)
    ACCESS_TOKEN = auth.login()
    kite= KiteConnect(api_key=API_KEY)
    ticker = KiteTicker(api_key=API_KEY,access_token=ACCESS_TOKEN)
    # 256265 -> NIFTY 50 Index (NSE)
    # 738561 -> RELIANCE (NSE) - Replace with your required tokens
    # 969473 -> WIPRO
    tokens = [969473]
    # initialise the datafeed with your ticker and tokens
    base_data_feed = KiteDataFeed(ticker, "ticks","tcp://127.0.0.1:5555",tokens)
    base_data_feed.start_feed()
