
import logging
import webbrowser
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def launch_browser():
    logging.info("Launching the default web browser...")
    try:
        time.sleep(1)  # Ensure the server starts before opening the browser
        webbrowser.open('http://127.0.0.1:5000')
        logging.info("Browser launched successfully.")
    except Exception as e:
        logging.error(f"Failed to launch browser: {e}")
