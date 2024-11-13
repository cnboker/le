import wave
from config.audio_model import detect_model
import json
from vosk import KaldiRecognizer


def speech_to_text(speech_file):
     # Open the audio file
    wf = wave.open(speech_file, "rb")
    vosk_model = detect_model(speech_file)
    # Create a recognizer with the model
    recognizer = KaldiRecognizer(vosk_model, wf.getframerate())
  
    # Read audio data and recognize speech
    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print("speech_to_text", result)
            text = json.loads(result).get("text", "")
        # else:
        #     partial_result = recognizer.PartialResult()
        #     print(partial_result)

    return text