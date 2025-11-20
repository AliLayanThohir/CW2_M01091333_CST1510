#Libraries needed for this python program
import sqlite3
from pathlib import Path


#Sets path where database is present in
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR /  "DATA"
DB_PATH = DATA_DIR / "intelligence_platform.db"

#Function where it returns the database which will be interacted with
def connect_database(db_path=DB_PATH):
    return sqlite3.connect(str(db_path))