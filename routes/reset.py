
from flask import Blueprint, request, jsonify
import sqlite3
from config import DB_PATH

reset = Blueprint('reset', __name__)

@reset.route('/api/reset-db', methods=['POST'])
def reset_db():
    data = request.json
    if data.get('pin') == '123':
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservations")
            conn.commit()
        return jsonify({"message": "Database reset successfully"}), 200
    else:
        return jsonify({"error": "Invalid PIN"}), 403
