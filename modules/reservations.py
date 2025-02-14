from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime, timedelta

bp = Blueprint('reservations', __name__)

def get_db_connection():
    return sqlite3.connect("reservations.db")

@bp.route("/api/check_availability", methods=["GET"])
def check_availability():
    date = request.args.get("date")
    room = request.args.get("room")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations WHERE room = ? AND start_date <= ? AND DATE(start_date, '+' || nights || ' days') > ?", (room, date, date))
    reservation = cur.fetchone()
    conn.close()
    
    if reservation:
        return jsonify({
            "status": "booked",
            "name": reservation[2],
            "phone": reservation[3]
        })
    else:
        return jsonify({"status": "available"})

@bp.route("/api/reserve", methods=["POST"])
def create_reservation():
    data = request.json
    if not all(k in data for k in ("room", "name", "phone", "provider", "start_date", "nights")):
        return jsonify({"error": "Missing data"}), 400
    
    name = data["name"]
    phone = data["phone"]
    nights = data["nights"]
    start_date = data["start_date"]
    
    if not name or len(name) > 50 or not name.replace(" ", "").isalnum():
        return jsonify({"error": "Invalid name"}), 400
    if not str(nights).isdigit():
        return jsonify({"error": "Invalid nights"}), 400
    if not str(phone).isdigit():
        return jsonify({"error": "Invalid phone"}), 400
    
    end_date = datetime.strptime(start_date, "%d/%m/%y") + timedelta(days=int(nights) - 1)
    
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservations (room, name, phone, provider, start_date, nights) VALUES (?, ?, ?, ?, ?, ?)",
                       (data["room"], name, phone, data["provider"], start_date, nights))
        conn.commit()
    
    return jsonify({"message": "Reservation created successfully"}), 201
