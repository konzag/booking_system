import sqlite3

def get_db_connection():
    return sqlite3.connect("reservations.db")

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            room TEXT NOT NULL,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            provider TEXT NOT NULL,
                            start_date TEXT NOT NULL,
                            nights INTEGER NOT NULL
                          )''')
        conn.commit()

def clear_reservations():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservations")
        conn.commit()
