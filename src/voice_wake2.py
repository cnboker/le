import json
import os
import sys
import time
import sounddevice as sd
import numpy as np
from config.settings import sample_rate, voice_event, hi_audio_file_path
from config.audio_model import vosk_model
import vosk
from src.voice_play import playsound

# 加载模型
recognizer = vosk.KaldiRecognizer(vosk_model, sample_rate)

# 设置唤醒词

keywords = ["小乐","小鹿", "你好小乐", "Hi小乐", "小了", "小小了","小 了",]


# 录音回调函数
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    if recognizer.AcceptWaveform(indata.tobytes()):
        result = json.loads(recognizer.Result())
        print('result->',result)
        output = result.get("text", "")
        if any(keyword in output for keyword in keywords):
            print("唤醒词检测到，开始录音...")
            # 当用户呼叫时,语音回答"在呢"
            playsound(hi_audio_file_path)
            voice_event.set()


# 配置麦克风参数
channels = 1  # 单声道

def monitor_voice():
    # 启动录音
    with sd.InputStream(
        callback=callback, channels=channels, samplerate=sample_rate, dtype=np.int16
    ):
        print("等待唤醒词...")
        while True:
            time.sleep(0.5)  # 每 1 秒检查一次
