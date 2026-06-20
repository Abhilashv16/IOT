import requests

BOT_TOKEN = "8735540500:AAGjJIRgeKlLLOXlNmDTOJg-JxVaLkmTVdU"
CHAT_ID = " "

message = "PRESENCE DETECTED"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=data)

print(response.text)
