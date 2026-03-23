import json
import asyncio
import websockets

from .sink import DataSink

class BinanceStreamer:
    def __init__(self, symbol):
        # 1. Switch to aggTrade (usually more reliable/consistent)
        self.symbol = symbol.lower()
        self.url = f"wss://stream.binance.us:9443/ws/{self.symbol}@aggTrade"
        self.sinks = []

    def add_sink(self, sink: DataSink):
        self.sinks.append(sink)

    async def start(self):
        # 2. Add ping_interval to keep the connection "hot"
        async with websockets.connect(self.url, ping_interval=20, ping_timeout=20) as ws:
            print(f"Streaming {self.symbol} aggTrades...")
            async for message in ws:
                # 3. Print a timestamp to see exactly when messages arrive
                from datetime import datetime
                print(f"[{datetime.now().strftime('%H:%M:%S')}] New Data Received")
                
                await asyncio.gather(*(sink.send(message) for sink in self.sinks))


##
# This is the primary streamer we will use!
#
class CoinbaseStreamer:
    def __init__(self, symbol):
        # Coinbase uses uppercase and hyphens (e.g., BTC-USD)
        self.symbol = symbol.upper().replace("USDT", "-USD")
        self.url = "wss://advanced-trade-ws.coinbase.com"
        self.sinks = []

    def add_sink(self, sink: DataSink):
        self.sinks.append(sink)

    async def start(self):
        async with websockets.connect(self.url) as ws:
            # Coinbase requires an explicit subscribe message after connecting
            subscribe_msg = {
                "type": "subscribe",
                "product_ids": [self.symbol],
                "channel": "ticker"
            }
            await ws.send(json.dumps(subscribe_msg))
            print(f"Streaming {self.symbol} from Coinbase...")

            async for message in ws:
                await asyncio.gather(*(sink.send(message) for sink in self.sinks))

class PythStreamer:
    def __init__(self, symbol_id):
        # Pyth uses Hex IDs for assets. 
        # BTC/USD is: e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43
        self.symbol_id = symbol_id
        self.url = "wss://hermes.pyth.network/ws"
        self.sinks = []

    def add_sink(self, sink: DataSink):
        self.sinks.append(sink)

    async def start(self):
        async with websockets.connect(self.url) as ws:
            subscribe_msg = {
                "type": "subscribe",
                "ids": [self.symbol_id]
            }
            await ws.send(json.dumps(subscribe_msg))
            print("Streaming from Pyth Network...")

            async for message in ws:
                # Pyth sends binary/json updates constantly
                await asyncio.gather(*(sink.send(message) for sink in self.sinks))