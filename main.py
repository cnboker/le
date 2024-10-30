import json
import os
import sys
from src.chatgpt import chat_with_gpt
from src.record import record_wav
from src.stt import speech_to_text
from src.tts import text_to_speech

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./src")))

def main():
    while True:
        print("begin....")
        # Get WAV from microphone.
        record_wav()

        # Convert audio into text.
        question = speech_to_text("./media/input.wav")
        # Send text to ChatGPT.
        print("Asking: {0}".format(question))
        qd = json.loads(question)
        if qd.get("text","") == "":
            continue
        gpt_response,_ = chat_with_gpt(question)
        print("Response: {0}".format(gpt_response))

        if gpt_response == "":
            continue
        # Convert ChatGPT response into audio.
        text_to_speech(gpt_response)

        # Play audio of reponse.
        os.system("aplay ./media/result.wav")
    

if __name__ == "__main__":
    main()
