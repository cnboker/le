
from openai import OpenAI
import os
from config.settings import api_key
# Set your OpenAI API key
print(api_key)
client = OpenAI(api_key=api_key)
def chat_with_gpt(prompt, conversation_history=None):
    if conversation_history is None:
        conversation_history = []
    
    # Append the user's prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    
    try:
        # Make a call to the ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        # Extract and add the response to the conversation history
        gpt_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": gpt_response})
        
        return gpt_response, conversation_history
    
    except Exception as e:
        return f"An error occurred: {e}", ""

def hello():
    return "hello!"
