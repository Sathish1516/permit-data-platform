import requests
from datetime import datetime
import json
import os

URL = "https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$limit=10"

def fetch_raw():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    os.makedirs("data/raw", exist_ok=True)

    filename = f"data/raw/permits_{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Saved file:", filename)

if __name__ == "__main__":
    fetch_raw()