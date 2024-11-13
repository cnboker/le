import time
import pyaudio
import vosk
import json
from config.settings import sample_rate, voice_event, hi_audio_file_path
from config.audio_model import vosk_model
from src.voice_play import playsound
import numpy as np
from src.audio_util import detect_speaker_playback, noise_reduction


recognizer = vosk.KaldiRecognizer(vosk_model, sample_rate)


def monitor_voice():
    # 不能太小，太小获取不到数据
    chunk = 1024
    channels = 1
    keywords = ["小乐", "你好小乐", "Hi小乐"]

    audio = pyaudio.PyAudio()
    # 输入流（麦克风）
    input_stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
    )
    input_stream.start_stream()


    print("Listening for '小乐'...")

    output = ""
    task_finished = False
    duration = 5
    mic_signal = []

    try:
        while not task_finished:
            #audio_playing = detect_speaker_playback()
            audio_playing = False #取消噪音过滤，功能不工作
            print("audio_playing", audio_playing)
            #audio_playing = False
            # 如果扬声器在播放做降噪处理
            if audio_playing == True:
                mic_signal = noise_reduction(duration)
            else:
                mic_frames = []
                for _ in range(0, int(sample_rate / chunk * duration)):
                    mic_data = input_stream.read(chunk)
                    mic_frames.append(mic_data)
                mic_signal = np.frombuffer(b"".join(mic_frames), dtype=np.int16)

            if recognizer.AcceptWaveform(mic_signal.tobytes()):
                result = json.loads(recognizer.Result())
                output = result.get("text", "")
            else:
                partial_result = recognizer.PartialResult()
                output = json.loads(partial_result).get("partial", "")

            print("output:", output)

            if any(keyword in output for keyword in keywords):
                print("唤醒词检测到，开始录音...")
                # 当用户呼叫时,语音回答"在呢"
                playsound(hi_audio_file_path)
                task_finished = True
                voice_event.set()

            time.sleep(0.5)  # 防止 CPU 占用过高
    finally:

        input_stream.stop_stream()
        input_stream.close()
        audio.terminate()
        # 重置清除音频缓冲
        recognizer.Reset()
        print("voice_wake stream stop")
