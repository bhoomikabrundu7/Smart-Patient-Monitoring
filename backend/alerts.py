from .config import (
    MIN_HEART_RATE,
    MAX_HEART_RATE,
    MIN_SPO2,
    MAX_TEMPERATURE
)


# ============================================================
# CHECK PATIENT CONDITION
# ============================================================

def check_patient_status(
    temperature,
    heart_rate,
    spo2,
    fall
):

    alerts = []


    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    if temperature >= MAX_TEMPERATURE:

        alerts.append(
            "High temperature detected"
        )


    # --------------------------------------------------------
    # HEART RATE
    # --------------------------------------------------------

    if heart_rate > MAX_HEART_RATE:

        alerts.append(
            "High heart rate detected"
        )

    elif heart_rate < MIN_HEART_RATE:

        alerts.append(
            "Low heart rate detected"
        )


    # --------------------------------------------------------
    # SPO2
    # --------------------------------------------------------

    if spo2 < MIN_SPO2:

        alerts.append(
            "Low SpO2 detected"
        )


    # --------------------------------------------------------
    # FALL
    # --------------------------------------------------------

    if fall:

        alerts.append(
            "Fall detected"
        )


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if alerts:

        return {
            "status": "ABNORMAL",
            "alerts": alerts
        }


    return {
        "status": "NORMAL",
        "alerts": []
    }


# ============================================================
# SIMPLE BOOLEAN CHECK
# ============================================================

def is_abnormal(
    temperature,
    heart_rate,
    spo2,
    fall
):

    result = check_patient_status(
        temperature,
        heart_rate,
        spo2,
        fall
    )

    return result["status"] == "ABNORMAL"
