from notifier import send_notification
response = send_notification("宝宝正在哭！！！")
if response is None:
    print("发送提示失败")
else:
    print(response.text)
    