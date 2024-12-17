
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = 'database.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL,
                source TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/bookings', methods=['GET', 'POST', 'PUT', 'DELETE'])
def bookings():
    if request.method == 'GET':
        start_date = request.args.get('start', '01/01')
        end_date = request.args.get('end', '15/01')
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM bookings
                WHERE check_in <= ? AND check_out >= ?
            ''', (end_date, start_date))
            results = cursor.fetchall()
        return jsonify([
            {
                "id": row[0],
                "room": row[1],
                "name": row[2],
                "phone": row[3],
                "check_in": row[4],
                "check_out": row[5],
                "source": row[6]
            } for row in results])

    elif request.method == 'POST':
        data = request.json
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Check for conflicts
            cursor.execute('''
                SELECT * FROM bookings
                WHERE room = ? AND check_in <= ? AND check_out >= ?
            ''', (data['room'], data['check_out'], data['check_in']))
            conflict = cursor.fetchone()
            if conflict:
                return jsonify({"status": "error", "message": "Η κράτηση συγκρούεται με υπάρχουσα κράτηση."}), 400
            cursor.execute('''
                INSERT INTO bookings (room, name, phone, check_in, check_out, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['room'], data['name'], data['phone'], data['check_in'], data['check_out'], data['source']))
            conn.commit()
        return jsonify({"status": "success"})

    elif request.method == 'PUT':
        data = request.json
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bookings
                SET name = ?, phone = ?, check_in = ?, check_out = ?, source = ?
                WHERE id = ?
            ''', (data['name'], data['phone'], data['check_in'], data['check_out'], data['source'], data['id']))
            conn.commit()
        return jsonify({"status": "updated"})

    elif request.method == 'DELETE':
        data = request.json
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookings WHERE id = ?', (data['id'],))
            conn.commit()
        return jsonify({"status": "deleted"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
