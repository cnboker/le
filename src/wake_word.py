import pvporcupine
import pyaudio
import struct
import vosk
import os
import json
import re
from config.settings import sample_rate,vosk_model


def listen_for_wake_word():
   
    audio = pyaudio.PyAudio()
    recognizer = vosk.KaldiRecognizer(vosk_model, sample_rate)

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=4096)
    stream.start_stream()

    print("Listening for '小乐'...")
    keywords=["小乐", "你好 小乐", "Hi 小乐"]
    # 将关键词组合为正则表达式模式
    pattern = re.compile("|".join(map(re.escape, keywords)))

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("wake:{0}",format(result))
                if pattern.search(result.get("text","")):
                    print("唤醒词检测到，开始录音...")
                    break
                    # 调用录音或其他功能
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        audio.terminate()



