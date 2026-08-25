from flask import Flask, request, jsonify
import os

from .data_handler import (
    save_sensor_data,
    get_sensor_history
)

from .alerts import check_patient_status


app = Flask(__name__)


# ============================================================
# LATEST DATA
# ============================================================

latest_data = {
    "temperature": 0,
    "heart_rate": 0,
    "spo2": 0,
    "fall": False,
    "mode": "WAITING",
    "status": "WAITING",
    "alerts": []
}


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return (
        "CareMatrix Smart Patient Monitoring Backend is Running"
    )


# ============================================================
# SENSOR DATA
# ============================================================

@app.route(
    "/sensor-data",
    methods=["POST"]
)
def receive_sensor_data():

    global latest_data

    data = request.get_json(
        silent=True
    )

    if not isinstance(data, dict):

        return jsonify({
            "status": "error",
            "message": "Invalid JSON"
        }), 400


    # --------------------------------------------------------
    # GET VALUES
    # --------------------------------------------------------

    try:

        temperature = float(
            data.get(
                "temperature",
                0
            )
        )

        heart_rate = int(
            data.get(
                "heart_rate",
                0
            )
        )

        spo2 = int(
            data.get(
                "spo2",
                0
            )
        )

        fall = bool(
            data.get(
                "fall",
                False
            )
        )

    except (
        ValueError,
        TypeError
    ):

        return jsonify({
            "status": "error",
            "message": "Invalid sensor values"
        }), 400


    # --------------------------------------------------------
    # MODE FROM ESP32
    # --------------------------------------------------------

    mode = str(
        data.get(
            "mode",
            "NORMAL"
        )
    ).upper()

    if mode not in [
        "NORMAL",
        "ABNORMAL"
    ]:
        mode = "NORMAL"


    # --------------------------------------------------------
    # CHECK VITAL SIGNS
    # --------------------------------------------------------

    result = check_patient_status(
        temperature,
        heart_rate,
        spo2,
        fall
    )

    alerts = result["alerts"]


    # --------------------------------------------------------
    # PATIENT STATUS
    # --------------------------------------------------------

    if mode == "ABNORMAL" or alerts:

        patient_status = "ABNORMAL"

    else:

        patient_status = "NORMAL"


    # --------------------------------------------------------
    # LATEST DATA
    # --------------------------------------------------------

    latest_data = {

        "temperature": temperature,

        "heart_rate": heart_rate,

        "spo2": spo2,

        "fall": fall,

        "mode": mode,

        "status": patient_status,

        "alerts": alerts
    }


    # --------------------------------------------------------
    # PRINT
    # --------------------------------------------------------

    print(
        "\n========== CAREMATRIX SENSOR DATA =========="
    )

    print(
        "Temperature:",
        temperature
    )

    print(
        "Heart Rate:",
        heart_rate
    )

    print(
        "SpO2:",
        spo2
    )

    print(
        "Fall:",
        fall
    )

    print(
        "Mode:",
        mode
    )

    print(
        "Status:",
        patient_status
    )

    print(
        "Alerts:",
        alerts
    )

    print(
        "============================================"
    )


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    save_sensor_data(
        temperature,
        heart_rate,
        spo2,
        fall,
        mode
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "status": "success",

        "message":
            "Sensor data received",

        "mode":
            mode,

        "patient_status":
            patient_status,

        "alerts":
            alerts

    }), 200


# ============================================================
# LATEST
# ============================================================

@app.route(
    "/latest",
    methods=["GET"]
)
def latest():

    return jsonify(
        latest_data
    )


# ============================================================
# HISTORY
# ============================================================

@app.route(
    "/history",
    methods=["GET"]
)
def get_history():

    return jsonify(
        get_sensor_history()
    )


# ============================================================
# HEALTH
# ============================================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({
        "status": "ok",
        "service": "CareMatrix Backend"
    })


# ============================================================
# RUN
# ============================================================

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