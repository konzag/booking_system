
# backend_dashboard.py
from flask import Blueprint, jsonify
from config import DB_PATH
import sqlite3

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservations")
    reservations = cursor.fetchall()
    conn.close()

    # Mock data for simplicity
    data = {
        "rooms": [
            "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)",
            "ΤΕΤΡΑΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ",
            "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
        ],
        "dates": [f"{day:02d}/01/25" for day in range(1, 16)],
        "reservations": {}
    }
    return jsonify(data)
