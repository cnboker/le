
import pyaudio
import vosk
import json
import re
import time
from config.settings import sample_rate,vosk_model,voice_event,hi_audio_file_path
from src.voice_play import playsound


recognizer = vosk.KaldiRecognizer(vosk_model, sample_rate)

def monitor_voice():   
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=4096)
    stream.start_stream()

    print("Listening for '小乐'...")
    keywords=["小乐", "你好 小乐", "Hi 小乐"]
    # 将关键词组合为正则表达式模式
    pattern = re.compile("|".join(map(re.escape, keywords)))
    output = ""
    task_finished = False
    try:
        while not task_finished:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                output = result.get("text","")          
            else:
                partial_result = recognizer.PartialResult()
                output = json.loads(partial_result).get("partial", "") 
            
            print("output:", output)
        
            if pattern.search(output):
                print("唤醒词检测到，开始录音...")                         
                # 当用户呼叫时,语音回答"在呢"
                playsound(hi_audio_file_path)
                task_finished = True
            time.sleep(0.5) # 防止 CPU 占用过高
    finally:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        audio.terminate()
