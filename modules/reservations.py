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
    nights = int(data["nights"])
    start_date = datetime.strptime(data["start_date"], "%d/%m/%y")
    end_date = start_date + timedelta(days=nights - 1)
    room = data["room"]

    if not name or len(name) > 50 or not name.replace(" ", "").isalnum():
        return jsonify({"error": "Invalid name"}), 400
    if not str(phone).isdigit():
        return jsonify({"error": "Invalid phone"}), 400

    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM reservations 
            WHERE room = ? 
            AND ((start_date <= ? AND DATE(start_date, '+' || nights || ' days') > ?) 
            OR (start_date BETWEEN ? AND ?))
        """, (room, start_date.strftime("%d/%m/%y"), start_date.strftime("%d/%m/%y"), start_date.strftime("%d/%m/%y"), end_date.strftime("%d/%m/%y")))

        existing_reservation = cursor.fetchone()

        if existing_reservation:
            return jsonify({"error": "Room is already booked for these dates"}), 400

        cursor.execute("""
            INSERT INTO reservations (room, name, phone, provider, start_date, nights) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (room, name, phone, data["provider"], start_date.strftime("%d/%m/%y"), nights))

        conn.commit()

    return jsonify({"message": "Reservation created successfully"}), 201

@bp.route("/api/get_reservations", methods=["GET"])
def get_reservations():
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT room, name, phone, start_date, nights FROM reservations")
        reservations = cursor.fetchall()

    reservations_list = []
    for res in reservations:
        reservations_list.append({
            "room": res[0],
            "name": res[1],
            "phone": res[2],
            "start_date": res[3],
            "nights": res[4]
        })

    return jsonify(reservations_list)
