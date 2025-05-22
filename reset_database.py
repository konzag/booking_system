import sqlite3
from config import DB_PATH

def reset_database():
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Delete all data from the reservations table
        cursor.execute("DELETE FROM reservations")
        
        # Optional: Reset auto-increment counter (if used)
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='reservations'")
        
        conn.commit()
        print("✅ All database entries have been successfully deleted.")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    confirmation = input("⚠️ Are you sure you want to delete all database entries? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        reset_database()
    else:
        print("❎ Operation canceled.")
