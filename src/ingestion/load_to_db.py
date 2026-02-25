import json
import os
from datetime import datetime

from src.db import get_connection

RAW_FOLDER = "data/raw"

def load_files():
    conn = get_connection()
    cur = conn.cursor()

    for file in os.listdir(RAW_FOLDER):
        if not file.endswith(".json"):
            continue   

        path = os.path.join(RAW_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for record in data:
            cur.execute("INSERT INTO raw_permits (fetched_at, raw_data, source_file) VALUES (%s, %s, %s)",
                        (datetime.now(), json.dumps(record), file)
                        )
        conn.commit()
        cur.close()
        conn.close()

        print("Loaded into database")

if __name__ == "__main__":
    load_files()