
from flask import Flask, render_template
from routes.dashboard import dashboard
from routes.reservations import reservations
from routes.reset import reset
import webbrowser
import threading
from browser_launcher import launch_browser
from cache_cleaner import clear_cache

app = Flask(__name__)

# Clear cache before starting
clear_cache()

# Register Blueprints
app.register_blueprint(dashboard)
app.register_blueprint(reservations)
app.register_blueprint(reset)

# Default route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Timer(1.0, launch_browser).start()
    app.run(debug=True)
