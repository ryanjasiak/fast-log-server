import json
import asyncio
import websockets
import os

from .streamer import CoinbaseStreamer
from .sink import FileSink



if __name__ == "__main__":
    streamer = CoinbaseStreamer("btcusdt")

    streamer.add_sink(FileSink("log/trades.log"))

    try:
        asyncio.run(streamer.start())
    except KeyboardInterrupt:
        pass