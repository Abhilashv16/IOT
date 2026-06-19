import serial
import csv
import os
import numpy as np
from utils import send_presence_alert
from collections import deque
from datetime import datetime

SERIAL_PORT = "COM4"
BAUD_RATE = 115200

ser = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    timeout=1
)

window_size = 20

buffer = deque(maxlen=window_size)

os.makedirs("logs", exist_ok=True)
csv_file = "logs/live_predict.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "timestamp",
            "rssi",
            "mean",
            "std",
            "max",
            "min",
            "prediction"
        ])

def classify(window):

    mean = np.mean(window)
    std = np.std(window)
    max_v = np.max(window)
    min_v = np.min(window)

    if std < 2:
        prediction = "OBJECT"
    else:
        prediction = "HUMAN"

    return prediction, mean, std, max_v, min_v

print("Listening to ESP32...")

while True:

    try:

        line = ser.readline().decode(
            errors="ignore"
        ).strip()

        if not line:
            continue

        try:
            rssi = float(line)

        except:
            continue

        buffer.append(rssi)

        if len(buffer) == window_size:

            prediction, mean, std, max_v, min_v = classify(
                list(buffer)
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print(
                f"{timestamp} |  {prediction}"
            )
            if prediction == "HUMAN":
                send_presence_alert()

        
            with open(csv_file, "a", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    timestamp,
                    rssi,
                    mean,
                    std,
                    max_v,
                    min_v,
                    prediction
                ])

    except KeyboardInterrupt:

        print("Stopped")

        break

    except Exception as e:

        print("ERROR:", e)