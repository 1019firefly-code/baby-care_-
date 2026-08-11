import requests
from config import WEBHOOK_URL

def send_notification(message):
    payload = {
        "msgtype" : "text",
        "text" : {
            "content" : message
        }
    }
    response = requests.post(WEBHOOK_URL,json=payload)
    return response

response = send_notification("宝宝正在哭！！！")
print(response.text)