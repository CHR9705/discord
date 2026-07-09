import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
raw_id = os.getenv("auth_id", "")
RECIPIENT_IDS = [int(x.strip()) for x in raw_id.split(",")] if raw_id else []

DB_PATH = "your_database.db"
TABLE_NAME = "your_table"
KEY_COLUMN = "id"