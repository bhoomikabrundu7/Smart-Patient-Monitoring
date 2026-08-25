from flask import Flask, request, jsonify
import os

from data_handler import save_sensor_data

app = Flask(__name__)

# Latest sensor reading
latest_data = {
    "temperature": 0,
    "heart_rate": 0,
    "spo2": 0,
    "fall": False
}

# Sensor history for dashboard
history = []


@app.route("/")
def home():
    return "Smart Patient Monitoring Backend is Running"


@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():

    global latest_data

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid JSON"
        }), 400

    # Receive sensor values
    latest_data = {
        "temperature": data.get("temperature", 0),
        "heart_rate": data.get("heart_rate", 0),
        "spo2": data.get("spo2", 0),
        "fall": data.get("fall", False)
    }

    # Keep history
    history.append(latest_data.copy())

    # Keep maximum 100 readings
    if len(history) > 100:
        history.pop(0)

    # Print received data
    print("\n========== SENSOR DATA ==========")
    print("Temperature:", latest_data["temperature"])
    print("Heart Rate:", latest_data["heart_rate"])
    print("SpO2:", latest_data["spo2"])
    print("Fall:", latest_data["fall"])
    print("=================================")

    # Save to CSV
    save_sensor_data(
        latest_data["temperature"],
        latest_data["heart_rate"],
        latest_data["spo2"],
        latest_data["fall"]
    )

    return jsonify({
        "status": "success",
        "message": "Sensor data received"
    }), 200


# ==========================================
# LATEST SENSOR DATA
# ==========================================

@app.route("/latest", methods=["GET"])
def latest():

    return jsonify(latest_data)


# ==========================================
# SENSOR HISTORY
# ==========================================

@app.route("/history", methods=["GET"])
def get_history():

    return jsonify(history)


# ==========================================
# START SERVER
# ==========================================

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