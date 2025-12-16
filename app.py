import asyncio
import threading
from backend.services.market_service import MarketService
from frontend.dashboard import run_dashboard

def start_ingestion(service):
    service.start_ingestion()  


if __name__ == "__main__":
    service = MarketService()

    t = threading.Thread(target=start_ingestion, args=(service,), daemon=True) #threading is used to run the ingestion in the background
    t.start()

    run_dashboard(service)
    