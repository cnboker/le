import sounddevice as sd
from scipy.io.wavfile import write

from src.tts import text_to_speech_piper


# 设置录音参数
duration = 5  # 录音时间（秒）
sample_rate = 22050  # 采样率

def record_audio(duration, sample_rate, filename="output.wav"):
    print("Recording...")

    # 录制音频
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()  # 等待录音完成

    # 将录音保存为 WAV 文件
    write(filename, sample_rate, audio_data)
    print(f"Recording saved as {filename}")



def test_tts():
    text_to_speech_piper("郑州骑共享单车到开封”这个梗源于2024年6月18日，四位女生为了品尝开封的灌汤包，从郑州骑行50多公里到达开'封的事件。她们晚上7点出发，经过3个多小时的骑行，终于到达目的地，享受了美味的灌汤包。")

