import requests
import json

# 定义API URL
url = "http://localhost:5000/api/chat"

def chat_with_Gemin(text):
    # 定义要发送的数据
    data = {
        "input_text": text
    }

    # 发送POST请求
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # 打印响应内容
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response.text.replace("*","")