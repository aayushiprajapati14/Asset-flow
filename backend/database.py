import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "assetflow.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH), timeout=15)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn