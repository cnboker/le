import threading
from time import sleep
import time
import numpy as np
import socketio
from scipy.io.wavfile import read
import socketio.exceptions
import sounddevice as sd
from config.settings import tts_server
from datetime import datetime

# Initialize an empty list for incoming audio data
audio_buffer = []
is_playing = False  # Track if audio is currently playing
# Initialize the Socket.IO client
sio = socketio.Client()


def play_audio():
    global audio_buffer, is_playing
    while True:
        # 仅当audio_buffer有数据且当前没有播放时，才开始播放
        if audio_buffer and not is_playing:
            # 将所有缓冲区中的音频数据拼接成一个数组用于播放
            audio_data_to_play = np.concatenate(audio_buffer)
            
            # 启动非阻塞播放
            is_playing = True  # 设置正在播放标志
            sd.play(audio_data_to_play, samplerate=22050)

            # 清空已播放的数据缓冲区
            audio_buffer.clear()
            
            # 等待播放完成，重置 `is_playing` 状态
            sd.wait()  # 等待当前播放完成
            is_playing = False  # 重置播放状态

        # 稍作延时，以减少资源占用
        time.sleep(0.01)

# 启动音频播放线程
play_thread = threading.Thread(target=play_audio, daemon=True)
play_thread.start()

@sio.event
def text_to_speech(text):
     sio.emit('start_tts', {'text': text})

@sio.event
def connect():
    print("Connected to server")
    #sio.emit('start_tts', {'text': "根据2023年1月联合国世界人口展望，very good中国的人口估计为 14.26 亿, Hello, 这是一个测试。This is a test."})

def print_time():
    # 获取当前时间
    current_time = datetime.now()

    # 格式化时间到毫秒
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S') + f'.{current_time.microsecond // 1000:03d}'

    print(formatted_time)

# 音频播放线程：创建一个独立的线程 play_thread，持续检查 audio_buffer 并播放其中的数据，这样 play_audio() 会自动在 audio_buffer 中有数据且 is_playing=False 时开始播放。
# 缓冲区管理：如果 is_playing=True 时有新数据进来，add_audio_data(new_data) 函数会继续将新数据添加到 audio_buffer，确保不会丢失数据。
# 非阻塞播放：sd.play() 启动非阻塞播放后，sd.wait() 会等待播放结束并重置 is_playing 状态，以便新的音频数据可以及时播放。

@sio.on('audio_chunk')
def handle_audio_chunk(data):
    print("receive data:", len(data))
    print_time()
    global audio_buffer
    # Convert the byte data to a NumPy array
    audio_chunk = np.frombuffer(data, dtype=np.int16)

    # Append the new chunk to the buffer
    audio_buffer.append(audio_chunk)


@sio.event
def disconnect():
    print("Disconnected from server")
    # Attempt to reconnect if disconnected
    connect_to_server()


def connect_to_server():
    try:
        # Connect to the WebSocket server         
        sio.connect(tts_server)
        print("connected successfully")            
    except socketio.exceptions.ConnectionError as e:
        print("Connection failured:{e}")
       
    except Exception as e:
        print("error occured:{e}")
      
       

connect_to_server()

