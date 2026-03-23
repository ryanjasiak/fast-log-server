import json
import asyncio
import websockets
import os

from .streamer import BinanceStreamer, CoinbaseStreamer
from .sink import FileSink



# --- 4. Execution ---
if __name__ == "__main__":
    streamer = CoinbaseStreamer("btcusdt")

    # Easily toggle what you want to do with the data here:
    streamer.add_sink(FileSink("log/trades.log"))
    # streamer.add_sink(UDSSink("/tmp/trading_logs.sock"))

    try:
        asyncio.run(streamer.start())
    except KeyboardInterrupt:
        pass