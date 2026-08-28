from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RENDER_URL = "https://smart-patient-monitoring.onrender.com/sensor-data"


@app.route("/")
def home():
    return "CareMatrix Local Bridge is Running"


@app.route("/sensor-data", methods=["POST"])
def sensor_data():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid JSON"
        }), 400

    print()
    print("=================================")
    print("CAREMATRIX LOCAL BRIDGE")
    print("Received from Wokwi:")
    print(data)

    try:

        response = requests.post(
            RENDER_URL,
            json=data,
            timeout=20
        )

        print("Render HTTP status:", response.status_code)
        print("Render response:", response.text)
        print("=================================")

        return (
            response.text,
            response.status_code,
            {
                "Content-Type": "application/json"
            }
        )

    except requests.RequestException as e:

        print("ERROR connecting to Render:")
        print(e)

        return jsonify({
            "status": "error",
            "message": "Could not connect to Render",
            "error": str(e)
        }), 502


if __name__ == "__main__":

    print()
    print("=================================")
    print(" CAREMATRIX LOCAL HTTP BRIDGE")
    print("=================================")
    print()
    print("Listening on:")
    print("http://0.0.0.0:5001")
    print()
    print("Wokwi should use:")
    print("http://host.wokwi.internal:5001/sensor-data")
    print()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )