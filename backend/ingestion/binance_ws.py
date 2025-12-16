import json
import asyncio
import websockets
from datetime import datetime
from .base_source import MarketDataSource
from typing import List

class BinanceWebSocket(MarketDataSource):
    def __init__(self, symbols):
        self.symbols = [s.lower() for s in symbols]
        self.sockets = []
        self._running = False

    async def connect(self) -> None:  # Connect to Binance WebSocket streams
        for symbol in self.symbols:
            url = f"wss://stream.binance.com/ws/{symbol}@trade"
            ws = await websockets.connect(url)
            self.sockets.append(ws)
        self._running = True

    async def stream(self): # Stream market data asynchronously
        if not self._running:
            raise Exception("WebSocket not connected.")
        
        while self._running:
            for ws in self.sockets:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)

                    if(data.get("e") != "trade"):
                        continue

                    yield{
                        "symbol": data["s"],
                        "timestamp": datetime.fromtimestamp(data["T"] / 1000),
                        "price": float(data["p"]),
                        "size": float(data["q"])
                    }
                except Exception as e:
                    continue
            
            await asyncio.sleep(0)
            
    async def close(self) -> None:  # Close all WebSocket connections
        self._running = False
        for ws in self.sockets:
            try:
                await ws.close()
            except Exception:
                pass
