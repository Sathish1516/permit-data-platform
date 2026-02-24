import requests
from datetime import datetime
import json
import os

from src.config import BASE_URL, LIMIT, TIMEOUT
from src.logger import logger

def fetch_raw():
    url = f"{BASE_URL}?$limit={LIMIT}"
    logger.info(f"Starting ingestion from {url}")

    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        os.makedirs("data/raw", exist_ok=True)
        filename = f"data/raw/permits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w",encoding="utf-8") as f:
            json.dump(data,f,indent=2)

        logger.info(f"Saved {len(data)} records to {filename}")
        print("Success:", filename)
    
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        print("FAILED - check logs/run.log")

if __name__ == "__main__":
    fetch_raw()