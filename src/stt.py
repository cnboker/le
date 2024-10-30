import vosk
import wave
from config.settings import sample_rate,vosk_model



def speech_to_text(speech_file):
    rec = vosk.KaldiRecognizer(vosk_model, sample_rate)

    wf = wave.open(speech_file,"rb")
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            print(rec.Reset())
        # else:
        #     print(rec.PartialResult())
    #print(rec.FinalResult());
    return rec.FinalResult()
