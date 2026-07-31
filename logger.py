import sqlite3
from datetime import datetime

DB_PATH = "conversations.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            question TEXT,
            retrieved_context TEXT,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_conversation(question, retrieved_context, answer):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (timestamp, question, retrieved_context, answer) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), question, retrieved_context, answer)
    )
    conn.commit()
    conn.close()

# Create the table the first time this file is imported
init_db()