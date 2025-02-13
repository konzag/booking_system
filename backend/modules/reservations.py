from flask import Blueprint, request, jsonify
import sqlite3

bp = Blueprint('reservations', __name__)

@bp.route("/api/reserve", methods=["POST"])
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
