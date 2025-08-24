import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Your LINE channel access token
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
# The user ID, group ID, or room ID
TO = os.getenv("USER_ID")

def send_line_message(message: str):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": TO,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    send_line_message("Hello! This is a test message from Python 🚀")
