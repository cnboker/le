import time
import wave
import pygame
from src.voice_play import playsound
def test_file(seconds=2):
    file = "./media/reply.wav"
    with wave.open(file, "rb") as wf:
        framerate = wf.getframerate()
        n_channels = wf.getnchannels()
        n_samples = wf.getnframes()
    print('framerate',framerate)
    # 获取当前播放位置
    playsound(file)
    time.sleep(5)  # 防止 CPU 占用过高
    current_position = pygame.mixer.music.get_pos()  # 毫秒
    print('current_position',current_position)
    if current_position < 0 or current_position > (n_samples / framerate * 1000):
        print("当前播放位置无效或超出范围。")
        return None
    
    print("Current position (ms):", current_position)

    # 计算后 2 秒的位置
    target_position = current_position + seconds * 1000  # 后 n 秒
    max_position_ms = (n_samples / framerate) * 1000  # 文件的总时长（毫秒）
    print('max_position_ms',max_position_ms)