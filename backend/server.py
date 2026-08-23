from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Smart Patient Monitoring Backend is Running"


@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid JSON"
        }), 400

    print("\n========== SENSOR DATA ==========")

    print("Temperature:", data.get("temperature"))
    print("Heart Rate:", data.get("heart_rate"))
    print("SpO2:", data.get("spo2"))
    print("Fall:", data.get("fall"))

    print("=================================")

    return jsonify({
        "status": "success",
        "message": "Sensor data received"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )