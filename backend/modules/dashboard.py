from flask import Blueprint, jsonify
import sqlite3

bp = Blueprint('dashboard', __name__)

@bp.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    with sqlite3.connect("reservations.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
    
    return jsonify([{
        "id": row[0], "room": row[1], "name": row[2], "phone": row[3],
        "provider": row[4], "start_date": row[5], "nights": row[6]
    } for row in reservations])
