
import sqlite3
import logging
from flask import Blueprint, request, jsonify

reservations = Blueprint('reservations', __name__)
DB_PATH = "database.db"  # Adjust the path to your database

# Configure logging for better debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@reservations.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    logging.debug(f"Received data for reservation: {data}")

    # Validate input data
    required_fields = ['room', 'date', 'name', 'phone', 'provider']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logging.warning(f"Missing fields in reservation data: {missing_fields}")
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        logging.debug("Connected to the database.")

        # Insert the reservation into the database
        cursor.execute("""
            INSERT INTO reservations (room, date, name, phone, provider)
            VALUES (?, ?, ?, ?, ?)
        """, (data['room'], data['date'], data['name'], data['phone'], data['provider']))

        conn.commit()
        logging.info(f"Reservation for room {data['room']} on {data['date']} saved successfully.")
        conn.close()
        return jsonify({"status": "success"}), 200

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
