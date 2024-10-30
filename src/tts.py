from gtts import gTTS

def text_to_speech(text):
    # Language selection (e.g., 'en' for English)
    tts = gTTS(text=text, lang='en')

    # Save the audio file
    tts.save("./media/result.mp4")
   
    return
