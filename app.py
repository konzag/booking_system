from flask import Flask, send_file, send_from_directory, jsonify
import os
import sqlite3
from modules import dashboard, reservations

app = Flask(__name__)

# Ensure browser does not cache static files
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

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

# Call init_db() when app starts
init_db()

# Browser use the most recent static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path, cache_timeout=0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
