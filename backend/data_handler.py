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
    fall,
    mode="NORMAL"
):

    os.makedirs(
        os.path.dirname(DATA_FILE),
        exist_ok=True
    )

    file_exists = os.path.exists(DATA_FILE)

    with open(
        DATA_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "temperature",
                "heart_rate",
                "spo2",
                "fall",
                "mode"
            ])

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            float(temperature),
            int(heart_rate),
            int(spo2),
            bool(fall),
            mode
        ])


def get_sensor_history():

    if not os.path.exists(DATA_FILE):
        return []

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            history = []

            for row in reader:

                try:

                    history.append({
                        "timestamp": row.get(
                            "timestamp",
                            ""
                        ),

                        "temperature": float(
                            row.get(
                                "temperature",
                                0
                            )
                        ),

                        "heart_rate": int(
                            row.get(
                                "heart_rate",
                                0
                            )
                        ),

                        "spo2": int(
                            row.get(
                                "spo2",
                                0
                            )
                        ),

                        "fall": (
                            row.get(
                                "fall",
                                "False"
                            ).lower()
                            == "true"
                        ),

                        "mode": row.get(
                            "mode",
                            "NORMAL"
                        )
                    })

                except (
                    ValueError,
                    TypeError
                ):
                    continue

            return history

    except (
        FileNotFoundError,
        OSError
    ):
        return []