import os
import wave
import vosk


sample_rate = 44100

def speech_to_text(speech_file):
    model = vosk.Model(os.path.expanduser("~") + "/code/voice_chatgpt/.venv/vosk-model-small-cn-0.22")
    rec = vosk.KaldiRecognizer(model, sample_rate)

    wf = wave.open(speech_file,"rb")
    while True:
        data = wf.readframes(4000)
        if not data:
            break;
        if rec.AcceptWaveform(data):
            print(rec.Reset())
        # else:
        #     print(rec.PartialResult())
    #print(rec.FinalResult());
    return rec.FinalResult()
