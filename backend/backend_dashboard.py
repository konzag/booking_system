
import sqlite3
import logging
from flask import Blueprint, jsonify

dashboard = Blueprint('dashboard', __name__)
DB_PATH = "database.db"  # Adjust the path to your database

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@dashboard.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    logging.debug("Received request to fetch dashboard data.")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        logging.debug("Connected to the database.")

        # Fetch all reservations
        cursor.execute("SELECT room, date, name, phone, provider FROM reservations")
        reservations = cursor.fetchall()
        logging.debug(f"Fetched {len(reservations)} reservations from the database.")

        # Structure the data
        reservations_dict = {}
        for room, date, name, phone, provider in reservations:
            reservations_dict[f"{room}-{date}"] = {
                "name": name,
                "phone": phone,
                "provider": provider
            }
            logging.debug(f"Processed reservation: Room={room}, Date={date}, Name={name}, Phone={phone}, Provider={provider}")

        # Sample rooms and dates for demonstration
        rooms = [
            "ΟΝΤΑΣ", "ΜΠΑΛΚΟΝΙ", "ΜΗΤΣΟΣ (ΤΖΑΚΙ)", "ΜΗΤΣΟΣ (ΔΙΠΛΑ)",
            "ΤΕΤΡΑΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ", "ΤΡΙΚΛΙΝΟ ΜΕ ΑΥΛΙ",
            "ΔΙΚΛΙΝΟ ΔΙΠΛΑ ΤΡΙΚ", "ΔΙΚΛΙΝΟ ΜΠΑΛΚΟΝΙ", "ΤΡΙΚΛΙΝΟ ΠΑΝΩ ΑΠΟ ΣΑΛΑ"
        ]
        dates = [f"{str(day).zfill(2)}/01/25" for day in range(1, 16)]  # Example dates for January 1-15

        conn.close()
        logging.debug("Database connection closed.")

        return jsonify({"rooms": rooms, "dates": dates, "reservations": reservations_dict}), 200

    except sqlite3.Error as e:
        logging.error(f"Database error while fetching dashboard: {e}")
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while fetching dashboard: {e}")
        return jsonify({"error": "Unexpected error"}), 500
