import json
import asyncio
import websockets
import os

from .streamer import CoinbaseStreamer
from .sink import FileSink, UDSSink



if __name__ == "__main__":
    streamer = CoinbaseStreamer("btcusdt")

    # streamer.add_sink(FileSink("log/trades.log"))
    streamer.add_sink(UDSSink(os.getenv('UDS_SOCKET')))

    try:
        asyncio.run(streamer.start())
    except KeyboardInterrupt:
        pass