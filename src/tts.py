from gtts import gTTS
from config.settings import reply_audio_file_path
import requests

def text_to_speech(text,save_file=reply_audio_file_path):
    # Language selection (e.g., 'en' for English)
    tts = gTTS(text=text, lang='zh-CN')

    # Save the audio file
    tts.save(save_file)
   
    return

def text_to_speech_piper(text,save_file=reply_audio_file_path):
    url = "http://localhost:5001/tts"
    data = {
        "text": text,
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        with open(save_file, "wb") as f:
            f.write(response.content)
    else:
        print("Error:", response.json())
