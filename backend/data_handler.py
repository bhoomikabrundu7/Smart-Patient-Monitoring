import csv
import os
from datetime import datetime

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "patient_data.csv"
)


def save_sensor_data(
    temperature,
    heart_rate,
    spo2,
    fall
):
    file_exists = os.path.exists(DATA_FILE)

    with open(
        DATA_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "temperature",
                "heart_rate",
                "spo2",
                "fall"
            ])

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            temperature,
            heart_rate,
            spo2,
            fall
        ])


def get_sensor_history():
    if not os.path.exists(DATA_FILE):
        return []

    with open(
        DATA_FILE,
        "r"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)
