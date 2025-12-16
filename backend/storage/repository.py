from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict


# Abstract repository interface for market data storage 

class MarketDataRepository(ABC):

    @abstractmethod
    def insert_tick(self, tick: dict) -> None: 
        pass

    @abstractmethod
    def get_ticks(self, symbol: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_resampled(self, symbol: str, timeframe: str) -> pd.DataFrame:
        pass
