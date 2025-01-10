
import sqlite3

DB_PATH = "database.db"  # Adjust this path to your actual database file

def fix_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Add the 'date' column if it doesn't exist
        cursor.execute("ALTER TABLE reservations ADD COLUMN date TEXT")
        print("Column 'date' added successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'date' already exists.")
        else:
            print(f"Error: {e}")

    # Verify schema
    cursor.execute("PRAGMA table_info(reservations)")
    columns = cursor.fetchall()
    print("Table schema:")
    for column in columns:
        print(column)

    conn.close()

if __name__ == "__main__":
    fix_database()
