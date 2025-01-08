
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import sqlite3
from config import DB_PATH

dashboard = Blueprint('dashboard', __name__)

ROOMS = [
    "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)",
    "ΤΕΤΡΑΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ",
    "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
]

@dashboard.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    year = int(request.args.get('year', 2025))
    month = int(request.args.get('month', 1))
    dates = [(datetime(year, month, i)).strftime("%d/%m/%y") for i in range(1, 16)]
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        reservations = cursor.execute("SELECT room, arrival_date, departure_date, name, phone FROM reservations").fetchall()
    
    reservations_dict = {}
    for room, arrival_date, departure_date, name, phone in reservations:
        key = f"{room},{arrival_date}"  # Convert tuple to string
        reservations_dict[key] = {"name": name, "phone": phone}
    
    return jsonify({"rooms": ROOMS, "dates": dates, "reservations": reservations_dict})
