import sqlite3

DB_FILE = "seen.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS seen (url TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()

def is_seen(url: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    cur = conn.execute("SELECT 1 FROM seen WHERE url = ?", (url,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def mark_seen(url: str):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT OR IGNORE INTO seen VALUES (?)", (url,))
    conn.commit()
    conn.close()