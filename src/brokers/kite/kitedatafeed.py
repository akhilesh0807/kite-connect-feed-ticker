import logging
from datetime import datetime
from core.interfaces import BaseDataFeed
from messenger.zmq_publisher import ZMQPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

API_KEY = "dummy"
API_SECRET = "dummy"
ACCESS_TOKEN = "dummy"

TIMESTAMP_KEYS = {
    "exchange_timestamp",
    "last_trade_time",
}

class KiteDataFeed(BaseDataFeed):
    def __init__(self, kiteticker, topic, endpoint, tokens):
        self.kws = kiteticker
        self.tokens = tokens
        self.publisher = ZMQPublisher(endpoint)

        #Decorate the bound method using the initialized publisher.
        self.publish_tick = self.publisher.publishZMQtopic(
            topic
        )(self.publish_tick)

        self.topic = topic

        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self.kws.on_error = self.on_error

    def start_feed(self):
        self.kws.connect()

    def publish_tick(self, tick):
        normalized_tick = self.normalize_tick(tick)
        return normalized_tick

    def normalize_tick(self,tick):
        for key in TIMESTAMP_KEYS:
            value = tick.get(key)

            if isinstance(value, datetime):
                tick[key] = value.isoformat()

        return tick

    def on_ticks(self, ws, ticks):
        """Callback to catch incoming ticks (live data stream)."""
        for tick in ticks:
            self.publish_tick(tick)

    def on_connect(self, ws, response):
        """Callback called when connection is successfully established."""
        logger.log(logging.INFO,"Connected to Kite WebSocket successfully!")

        tokens = self.tokens

        # Subscribe to the tokens
        ws.subscribe(tokens)

        # Set the stream mode to FULL (gives complete market depth, OHLC, LTP)
        # Other modes: ws.MODE_LTP (only last price), ws.MODE_QUOTE (LTP + OHLC + volume)
        ws.set_mode(ws.MODE_FULL, tokens)

    def on_close(self, ws, code, reason):
        """Callback when connection is closed."""
        logger.log(logging.INFO, f"Connection closed: {code} - {reason}")

    def on_error(self, ws, code, reason):
        """Callback when an error occurs."""
        logger.log(logging.INFO, f"WebSocket error: {code} - {reason}")
