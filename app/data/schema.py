#Libaries needed for program
import sqlite3

#Function that creates the users table in a database, along with its variables and format of them
def create_users_table(conn):
    #Cursor allows for execution of SQL statements
    cursor = conn.cursor()
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    #Create users table with its variables and variables formats
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Users table created successfully!")

#Function to create cyber_incidents table
def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    cyber_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT DEFAULT 'Open',
    decription TEXT,
    reported_by TEXT NOT NULL,
    created_at TIMESTAMP DEAFULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(cyber_table_sql)
    conn.commit
    print("✅ Cyber incidents table created successfully!")

#Function to create datasets_metadata table 
def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    create_metadata_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT NOT NULL,
    category TEXT,
    source TEXT,
    last_updated TEXT NOT NULL,
    record_count INTEGER,
    file_size_mb REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_metadata_sql)
    conn.commit
    print("✅ Datasets metadata table created successfully!")

#Function to create it tickets table
def create_it_tickets_table(conn):
    cursor = conn.cursor()
    create_it_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL UNIQUE,
    priority TEXT,
    status TEXT DEFAULT 'Open',
    category TEXT,
    subject TEXT NOT NULL,
    description TEXT,
    created_date TEXT,
    resolved_date TEXT,
    assigned_to TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_it_sql)
    conn.commit
    print("✅ IT tickets table created successfully!")

#Function that runs everything
def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)