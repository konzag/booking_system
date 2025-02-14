from flask import Flask, send_file, jsonify
import os
import sqlite3
from modules import dashboard, reservations

app = Flask(__name__)

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Register Blueprints
app.register_blueprint(dashboard.bp)
app.register_blueprint(reservations.bp)

# Serve the index.html from the root directory
@app.route("/")
def serve_index():
    return send_file("index.html")

# API route to clear database
@app.route("/api/clear", methods=["DELETE"])
def clear_database():
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservations")
        conn.commit()
    return jsonify({"message": "Η βάση δεδομένων καθαρίστηκε επιτυχώς!"})

def init_db():
    with sqlite3.connect("reservations.db") as conn:
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

# Κάλεσμα της init_db() όταν ξεκινά η εφαρμογή
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
