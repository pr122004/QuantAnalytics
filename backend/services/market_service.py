import asyncio
import threading
from typing import List

from backend.ingestion.binance_ws import BinanceWebSocket
from backend.storage.duckdb_store import DuckDbStore


class MarketService:
    
    #Central orchestration layer.
    #Manages ingestion lifecycle and exposes data access to frontend.
    

    def __init__(self, symbols: List[str] = None):
        if symbols is None:
            symbols = ["btcusdt", "ethusdt"]

        self.symbols = symbols
        self.store = DuckDbStore()
        self.source = BinanceWebSocket(symbols)

        self._running = False
        self._thread = None

    async def _ingest_loop(self): # Internal async ingestion loop
       
        await self.source.connect()
        self._running = True

        async for tick in self.source.stream():
            if not self._running:
                break
            self.store.insert_tick(tick)

    def start_ingestion(self):  # Start ingestion in background thread

        if self._thread and self._thread.is_alive():
            return  # since already running

        def runner():
            asyncio.run(self._ingest_loop())

        self._thread = threading.Thread(
            target=runner, daemon=True
        )
        self._thread.start()

    def stop_ingestion(self): # Stop ingestion
        
        self._running = False 


    def get_resampled_data(self, symbol: str, timeframe: str):
        return self.store.get_resampled(symbol, timeframe)

    def get_raw_ticks(self, symbol: str):
        return self.store.get_ticks(symbol)
