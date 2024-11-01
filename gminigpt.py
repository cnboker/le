import os
import google.generativeai as genai
from flask import Flask, request, jsonify
import requests

os.environ['GOOGLE_API_KEY'] = "AIzaSyCKf7OmRz8qRZPB_q5VG-iGaVnh3OKOuqc"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

# 假设我们要调用Google Gemini LLMs或类似服务的API
def generate_content(input_text):
    response = model.generate_content(input_text)
    print(response.text)
    return response.text

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    input_text = data.get('input_text', '')
    if not input_text:
        return jsonify({"error": "No input text provided"}), 400

    # 调用服务API并返回结果
    result = generate_content(input_text)
    return result

if __name__ == '__main__':
    app.run(debug=True)