import sqlite3
import os

# Define the database file path
DB_PATH = "seshat_bible.db"

def initialize_db():
    """Creates the tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Table For Characters
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            first_seen_in TEXT)
    ''')
    
    # 2. Table for Places
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            location_type TEXT)
    ''')
    
    # 3. Table for Events (The 'Significance')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')

    # 4. NEW: Table for Custom Lore (The Galbark Fix)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_lore (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            entity_type TEXT)
    ''')
    
    conn.commit()
    conn.close()

def save_entity(category, name):
    """Saves a character or place if it's new."""
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

def get_all_lore():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM characters")
    chars = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT name FROM places")
    places = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT sentence, action FROM events ORDER BY timestamp DESC LIMIT 10")
    events = [{"context": row[0], "main_action": row[1]} for row in cursor.fetchall()]
    conn.close()
    return {"characters": chars, "places": places, "events": events}

def add_custom_lore(name, entity_type):
    """Teaches Seshat a new irregular name (The Galbark Fix)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO custom_lore (name, entity_type) VALUES (?, ?)", (name, entity_type))
        conn.commit()
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        conn.close()

# Initialize the DB when this script is run
if __name__ == "__main__":
    initialize_db()
    print("Seshat Database Initialized.")