import duckdb
import pandas as pd
from typing import Dict
from datetime import datetime
from .repository import MarketDataRepository

#duckDB to store market data ticks
class DuckDbStore(MarketDataRepository):
    def __init__(self, path = "data/market_data.duckdb"):
        self.con = duckdb.connect(path)
        self._init_tables()

    def _init_tables(self) -> None:
        self.con.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            timestamp TIMESTAMP,
            symbol VARCHAR,
            price DOUBLE,
            size DOUBLE
        )
        """)

    def insert_tick(self, tick: Dict) -> None:  # Insert a market data tick
        self.con.execute(
            "INSERT INTO ticks(timestamp, symbol, price, size) VALUES (?, ?, ?, ?)",
            (tick['timestamp'], tick['symbol'], tick['price'], tick['size'])
        )

    def get_ticks(self, symbol: str) -> pd.DataFrame:  # Retrieve raw ticks for a symbol
        query = f"SELECT * FROM ticks WHERE symbol = '{symbol}' ORDER BY timestamp"
        return self.con.execute(query).df()
    
    def get_resampled(self, symbol: str, timeframe: str) -> pd.DataFrame:   # Resample ticks into specified timeframe
        bucket_map = {
            "1s" : "1 second",
            "1m" : "1 minute",
            "5m" : "5 minutes"
        }

        if timeframe not in bucket_map:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        interval = bucket_map[timeframe]
        
        query = f"""
        SELECT
            time_bucket(INTERVAL '{interval}', timestamp) AS ts,
            AVG(price) AS price,
            SUM(size) AS volume
        FROM ticks
        WHERE symbol = '{symbol}'
        GROUP BY ts
        ORDER BY ts
        """
        return self.con.execute(query).df()