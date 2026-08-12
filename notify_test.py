from notifier import send_notification
response = send_notification("宝宝正在哭！！！")
print(response.text)