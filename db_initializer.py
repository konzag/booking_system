
import sqlite3

DB_PATH = 'database.db'

def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                provider TEXT NOT NULL,
                arrival_date TEXT NOT NULL,
                departure_date TEXT NOT NULL
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    initialize_db()
    print("Database initialized successfully.")
