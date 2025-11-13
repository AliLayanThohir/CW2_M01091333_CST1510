#Libraries needed for this python program
import sqlite3
from pathlib import Path

#Sets path where database is present in
DB_PATH = Path("DATA") / "intelligence_platform.db"

#Function where it returns the database which will be interacted with
def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))