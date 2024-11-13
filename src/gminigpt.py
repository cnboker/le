from config.settings import ssr_server
import requests
import time

# 假设我们要调用Google Gemini LLMs或类似服务的API
def chat_with_Gemin(input_text):
    payload = {"input_text": input_text}
    response = requests.post(f"{ssr_server}/start_chat", json=payload)
    response_text = ""    
    task_id = response.json().get("task_id")
    print("taskid->",task_id)
    while True:
        status_response = requests.get(f"{ssr_server}/chat/{task_id}")
        json = status_response.json()
        status = json.get("status")
        print("task status ->", status)
        if status == "complete":
            response_text = json.get("payload")
            break
        else:
            print("task is still in progress ...")
        time.sleep(1)
    return response_text