from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

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

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
    
    return jsonify([{
        "id": row[0], "room": row[1], "name": row[2], "phone": row[3],
        "provider": row[4], "start_date": row[5], "nights": row[6]
    } for row in reservations])

@app.route("/api/reserve", methods=["POST"])
def create_reservation():
    data = request.json
    if not all(k in data for k in ("room", "name", "phone", "provider", "start_date", "nights")):
        return jsonify({"error": "Missing data"}), 400
    
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservations (room, name, phone, provider, start_date, nights) VALUES (?, ?, ?, ?, ?, ?)",
                       (data["room"], data["name"], data["phone"], data["provider"], data["start_date"], data["nights"]))
        conn.commit()
    
    return jsonify({"message": "Reservation created successfully"}), 201

from flask import send_from_directory

@app.route('/frontend/<path:filename>')
def serve_frontend(filename):
    return send_from_directory('../frontend', filename)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
