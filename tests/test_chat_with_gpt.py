import os
import sys
from src.chatgpt import chat_with_gpt,hello

# 添加 src 目录到 Python 路径
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_chat_with_gpt():
     user_input = "What are some interesting facts about the ocean?"
     response, _ = chat_with_gpt(user_input)
     print("ChatGPT:", response)
     assert response == "ok"

def test_hello():
     assert hello() == "hello!"

