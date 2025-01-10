
import logging
from flask import Flask, render_template
from backend.backend_dashboard import dashboard
from backend.backend_reservation import reservations

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.register_blueprint(dashboard)
app.register_blueprint(reservations)

@app.route('/')
def home():
    logging.info("Serving the homepage (index.html).")
    return render_template('index.html')

if __name__ == '__main__':
    logging.info("Starting Flask application...")
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Application encountered an error: {e}")
