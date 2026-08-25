from flask import Flask, request, jsonify
import os

from backend.data_handler import save_sensor_data

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

    temperature = data.get("temperature")
    heart_rate = data.get("heart_rate")
    spo2 = data.get("spo2")
    fall = data.get("fall", False)

    print("\n========== SENSOR DATA ==========")

    print("Temperature:", temperature)
    print("Heart Rate:", heart_rate)
    print("SpO2:", spo2)
    print("Fall:", fall)

    print("=================================")

    # Save reading to CSV
    save_sensor_data(
        temperature,
        heart_rate,
        spo2,
        fall
    )

    return jsonify({
        "status": "success",
        "message": "Sensor data received"
    }), 200


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )