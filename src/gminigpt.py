from config.settings import ssr_server
import requests


# 假设我们要调用Google Gemini LLMs或类似服务的API
async def chat_with_Gemin(input_text):
    payload = {"input_text": input_text}
    response = requests.post(f"{ssr_server}/chat", json=payload)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("response_text", "这个问题无法回复")
    else:
        return f"错误:{response.text}"
