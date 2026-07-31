import sqlite3

conn = sqlite3.connect("conversations.db")
rows = conn.execute(
    "SELECT question, retrieved_context FROM conversations WHERE question LIKE '%used product%' OR question LIKE '%third-party%' ORDER BY id DESC LIMIT 2"
).fetchall()

for q, ctx in rows:
    print(q, "->", ctx[:200])
    print()