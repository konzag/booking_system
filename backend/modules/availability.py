from flask import Blueprint, request, jsonify
import sqlite3

bp = Blueprint('availability', __name__)

def check_room_availability(room, date):
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE room = ? AND start_date <= ? AND DATE(start_date, '+' || nights || ' days') > ?", (room, date, date))
        reservation = cursor.fetchone()
    
    if reservation:
        return {"status": "booked", "name": reservation[2], "phone": reservation[3]}
    else:
        return {"status": "available"}

@bp.route("/api/check_availability", methods=["GET"])
def check_availability():
    date = request.args.get("date")
    room = request.args.get("room")
    return jsonify(check_room_availability(room, date))
