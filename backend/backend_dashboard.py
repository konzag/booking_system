
# backend_dashboard.py
from flask import Blueprint, jsonify
from config import DB_PATH
import sqlite3

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch reservations from the database
    cursor.execute("SELECT room, date, name, phone, provider FROM reservations")
    reservations_data = cursor.fetchall()
    conn.close()

    # Build the reservations dictionary
    reservations = {}
    for room, date, name, phone, provider in reservations_data:
        reservation_key = f"{room}-{date}"
        reservations[reservation_key] = {
            "name": name,
            "phone": phone,
            "provider": provider
        }

    # Prepare the response data
    data = {
        "rooms": [
            "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)",
            "ΤΕΤΡΑΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ",
            "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
        ],
        "dates": [f"{day:02d}/01/25" for day in range(1, 16)],
        "reservations": reservations  # Include actual reservations
    }
    return jsonify(data)
