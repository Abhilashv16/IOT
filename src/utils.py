def print_dataset_info(X, y):
    print("Total samples:", len(X))
    print("Feature length:", len(X[0]))
    print("Labels:", set(y))
    
    
    
import requests

from datetime import datetime
BOT_TOKEN = "8735540500:AAGjJIRgeKlLLOXlNmDTOJg-JxVaLkmTVdU"
CHAT_ID = "7133167053"

last_alert_time = 0
ALERT_COOLDOWN = 30


def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    return response.json()


def send_presence_alert(confidence=None):

    global last_alert_time

    current_time = datetime.now().timestamp()

    
    if current_time - last_alert_time < ALERT_COOLDOWN:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        " HUMAN PRESENCE DETECTED\n\n"
        f"Time: {timestamp}\n"
    )

    if confidence is not None:
        message += f"Confidence: {confidence:.2f}%"

    send_telegram_alert(message)

    last_alert_time = current_time