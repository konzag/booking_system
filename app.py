from flask import Flask, send_file, send_from_directory, jsonify
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import os
from .modules import dashboard, reservations, database

app = Flask(__name__)

# Ensure browser does not cache static files
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Register Blueprints
app.register_blueprint(dashboard.bp)
app.register_blueprint(reservations.bp)

# Serve the index.html from the root directory
@app.route("/")
def serve_index():
    return send_file("index.html")

# API route to clear database
@app.route("/api/clear", methods=["DELETE"])
def clear_database():
    database.clear_reservations()
    return jsonify({"message": "Database cleared successfully!"})

# Initialize database
if __name__ == "__main__":
    database.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
