from flask import Flask, jsonify
import os, random, time

app = Flask(__name__)
DEVICE_ID = os.getenv("DEVICE_ID", "device-001")

@app.route("/")
def index():
    return jsonify({
        "device_id": DEVICE_ID,
        "model": "ThermoX-100",
        "firmware": "v1.2.3",
        "uptime": int(time.time())
    })

@app.route("/status")
def status():
    return jsonify({
        "device_id": DEVICE_ID,
        "temperature": round(18 + random.random()*10, 2),
        "humidity": round(30 + random.random()*40, 1),
        "online": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
