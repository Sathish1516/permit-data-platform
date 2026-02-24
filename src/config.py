import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LIMIT = int(os.getenv("LIMIT", 10))
TIMEOUT = int(os.getenv("TIMEOUT", 30))