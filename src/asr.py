import vosk
import wave
from config.settings import sample_rate,vosk_model
import json


def speech_to_text(speech_file):
    rec = vosk.KaldiRecognizer(vosk_model, sample_rate)

    wf = wave.open(speech_file,"rb")
      # To store the full result
    full_result = []

    while True:
        data = wf.readframes(4000)
        if not data:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())  # Full result in JSON format
            full_result.append(result.get("text", ""))
     # Add any remaining partial result (for last incomplete phrase)
    final_result = json.loads(rec.FinalResult()).get("text", "")
    full_result.append(final_result)
    # close the audio file
    wf.close()

    print("full_result:{0}",format(full_result))
     # Return the combined results as a single string
    return " ".join(full_result)
