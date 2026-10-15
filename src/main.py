from kiteconnect import KiteConnect, KiteTicker

from brokers.kite.auth import KiteAuth
from brokers.kite.kitedatafeed import KiteDataFeed

API_KEY = "dummy_api_key"
RECONNECT_MAX_TRIES = 3
API_SECRET = "dummy_secret"
ACCESS_TOKEN = "dummy_access_token"

if __name__ == '__main__':
    auth = KiteAuth(api_key=API_KEY, api_secret=API_SECRET)
    ACCESS_TOKEN = auth.login()
    print(ACCESS_TOKEN)
    # once you have an access token for a day you can comment above and just re-run main function
    ticker = KiteTicker(api_key=API_KEY,access_token=ACCESS_TOKEN)
    # print(f"ACCES TOKEN {ACCESS_TOKEN}")
    # 256265 -> NIFTY 50 Index (NSE)
    # 738561 -> RELIANCE (NSE) - Replace with your required tokens
    # 969473 -> WIPRO
    tokens = [969473]
    #initialise the datafeed with your ticker and tokens
    base_data_feed = KiteDataFeed(ticker, "ticks","tcp://127.0.0.1:5555",tokens)
    base_data_feed.start_feed()
    exit(0)



