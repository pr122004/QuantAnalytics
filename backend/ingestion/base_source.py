from abc import ABC, abstractmethod

# ABC (Abstract Base Class) defines a common interface that all market data providers must implement.

class MarketDataSource(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def stream(self):
        pass

    @abstractmethod
    async def close(self):
        pass