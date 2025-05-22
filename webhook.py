from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    if data and "ref" in data and data["ref"] == "refs/heads/main":
        subprocess.Popen(["/bin/bash", "/opt/booking_system/deploy.sh"])
        return "Deployment started", 200
    return "Ignored", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
