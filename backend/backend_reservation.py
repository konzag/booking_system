# backend_reservation.py
from flask import Blueprint, request, jsonify

reservation = Blueprint('reservation', __name__)

@reservation.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    # Validate required fields
    required_fields = ["room", "date", "name", "phone", "provider", "nights"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Simulate successful reservation
    # Ideally, you would save this to your database
    print("Reservation received:", data)
    return jsonify({"status": "success"})
