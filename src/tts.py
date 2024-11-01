from gtts import gTTS
from config.settings import reply_audio_file_path

def text_to_speech(text,save_file=reply_audio_file_path):
    # Language selection (e.g., 'en' for English)
    tts = gTTS(text=text, lang='zh-CN')

    # Save the audio file
    tts.save(save_file)
   
    return
