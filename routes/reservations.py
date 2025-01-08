
from flask import Blueprint, request, jsonify
import sqlite3
from config import DB_PATH
from datetime import datetime, timedelta

reservations = Blueprint('reservations', __name__)

@reservations.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    room = data.get('room')
    name = data.get('name')
    phone = data.get('phone')
    provider = data.get('provider')
    arrival_date = data.get('arrival_date')
    nights = int(data.get('nights'))
    
    arrival = datetime.strptime(arrival_date, "%d/%m/%y")
    departure = arrival + timedelta(days=nights)
    departure_date = departure.strftime("%d/%m/%y")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reservations (room, name, phone, provider, arrival_date, departure_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (room, name, phone, provider, arrival_date, departure_date))
        conn.commit()
    
    return jsonify({"message": "Reservation created successfully"})
