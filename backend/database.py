import sqlite3
import os

# Define the database file path
DB_PATH = "seshat_bible.db"

def initialize_db():
    """Creates the tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Table For Characters
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS characters (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT UNIQUE,
                   description TEXT,
                   first_seen_in TEXT)
                   ''')
    
    #Table for Places
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS places (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        location_type TEXT)
                   ''')
    
    #Table for Ebents (The 'Significance')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sentence TEXT,
                        action TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                    ''')
    
    conn.commit()
    conn.close()

def save_entity(category, name):
     """Saves a character or place it it's new."""
     conn = sqlite3.connect(DB_PATH)
     cursor = conn.cursor()
     table = "characters" if category == "person" else "places"

     try:
        cursor.execute(f"INSERT OR IGNORE INTO {table} (name) VALUES (?)", (name,))
        conn.commit()
     except Exception as e:
        print(f"DB Error: {e}")
     finally:
        conn.close()

def save_event(sentence, action):
    """Saves a plot event to the history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO events (sentence, action) VALUES (?, ?)", (sentence, action))
        conn.commit()
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        conn.close()

# Initialize the DB when this script is run
if __name__ == "__main__":
    initialize_db()
    print("Seshat Database Initialized.")