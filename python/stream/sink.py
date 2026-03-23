import os
from abc import ABC, abstractmethod

# --- 1. Define the Interface ---
class DataSink(ABC):
    """Base class for anything that wants to consume Binance data."""
    @abstractmethod
    async def send(self, data: str):
        pass

# --- 2. Create Concrete Handlers ---
class UDSSink(DataSink):
    def __init__(self, path):
        self.path = path
        self.writer = None

    async def send(self, data: str):
        try:
            if not self.writer:
                _, self.writer = await asyncio.open_unix_connection(self.path)
            
            self.writer.write((data + "\n").encode())
            await self.writer.drain()
        except Exception as e:
            print(f"UDS Error: {e}")
            self.writer = None # Reset for reconnection

class FileSink(DataSink):
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    async def send(self, data: str):
        # Open the file only once if it's not open
        if self.file is None:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            self.file = open(self.filename, "a", buffering=1) # Line buffering

        self.file.write(data + "\n")
        # We don't 'await' here because standard file objects aren't awaitable,
        # but opening/closing every time was the real performance killer.

class PrintSink(DataSink):
    async def send(self, data: str):
        print(f"Received: {data[:50]}...")
