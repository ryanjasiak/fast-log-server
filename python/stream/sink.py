import os
from abc import ABC, abstractmethod
import asyncio

class DataSink(ABC):
    """Base class for anything that wants to consume Binance data."""
    @abstractmethod
    async def send(self, data: str):
        pass

class UDSSink(DataSink):
    def __init__(self, path):
        self.path = path
        self.writer = None

    async def send(self, data: str):
        print(f'sending data: {type(data)}, {len(data)}')
        try:
            if not self.writer:
                _, self.writer = await asyncio.open_unix_connection(self.path)
            
            self.writer.write((data + "\n").encode())
            await self.writer.drain()
        except Exception as e:
            print(f"UDS Error: {e}")
            self.writer = None

class FileSink(DataSink):
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    async def send(self, data: str):
        if self.file is None:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            self.file = open(self.filename, "a", buffering=1)

        self.file.write(data + "\n")

class PrintSink(DataSink):
    async def send(self, data: str):
        print(f"Received: {data[:50]}...")
