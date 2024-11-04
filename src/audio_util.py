import threading
import pygame
import pyaudio
import wave
import numpy as np
import adaptfilt as adf
from scipy.io.wavfile import write, read
from config.settings import sample_rate, current_playing_file_path
from pydub import AudioSegment
from pydub.utils import get_array_type

# 检测扬声器是否正在播放
def detect_speaker_playback(threshold=5000, duration=1):
    return pygame.mixer.music.get_busy()


# 要使用 pygame.mixer.music 播放 mp3 文件并获取当前播放位置后的 n 秒数据
def get_audio_segment_after_n_seconds(audiofile, duration=2):
     # 获取当前播放位置
    current_position = pygame.mixer.music.get_pos()  # 毫秒
    audio = AudioSegment.from_mp3(audiofile)
    end_pos_ms = min(len(audio), current_position + duration * 1000)  # 防止超出音频长度
    audio_segment = audio[current_position:end_pos_ms]
    # 获取正确的 NumPy 数据类型
    array_type = get_array_type(audio_segment.sample_width * 8)
    audio_array = np.array(audio_segment.get_array_of_samples(), dtype=array_type)
    
    # 如果是立体声，重新调整为 2 列
    if audio_segment.channels == 2:
        audio_array = audio_array.reshape((-1, 2))
    return audio_array



# 要使用 pygame.mixer.music 播放 WAV 文件并获取当前播放位置后的 n 秒数据
def playing_audio_after_n_seconds_data(audiofile,seconds):

    # 获取 WAV 文件的参数
    with wave.open(audiofile, "rb") as wf:
        framerate = wf.getframerate()
        n_channels = wf.getnchannels()
        n_samples = wf.getnframes()
    print('framerate',framerate)
    # 获取当前播放位置
    current_position = pygame.mixer.music.get_pos()  # 毫秒
    if current_position < 0 or current_position > (n_samples / framerate * 1000):
        print("当前播放位置无效或超出范围。")
        return None
    
    print("Current position (ms):", current_position)

    # 计算后 2 秒的位置
    target_position = current_position + seconds * 1000  # 后 n 秒
    max_position_ms = (n_samples / framerate) * 1000  # 文件的总时长（毫秒）
    print('max_position_ms',max_position_ms)
    # 确保目标位置不超过音频长度
    if target_position > max_position_ms:  # 转换为毫秒
        target_position = max_position_ms

    # 读取音频数据
    start_sample = int(current_position * framerate / 1000)
    end_sample = int(target_position * framerate / 1000)

    # 读取指定的音频片段
    with wave.open(audiofile, "rb") as wf:
        wf.setpos(start_sample)  # 移动到开始位置
        frames = wf.readframes(end_sample - start_sample)  # 读取指定的帧数

    # 将读取的帧数据转换为 numpy 数组
    audio_data = np.frombuffer(
        frames, dtype=np.int16
    )  # 根据你的 WAV 文件数据类型选择合适的 dtype
    print("Extracted audio data shape:", audio_data.shape)

    # 你可以在这里处理或保存 audio_data
    return audio_data


def record_both_signals(duration, sample_rate=22050):
    chunk = 1024  # 缓冲区大小
    channels = 1
    # 缓存麦克风信号和扬声器信号
    speaker_signal = []
    mic_signal = []
    # 初始化 PyAudio
    audio = pyaudio.PyAudio()

    # 打开麦克风输入流
    input_stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
    )
    input_stream.start_stream()

    # 录制麦克风信号
    def record_mic():
        nonlocal mic_signal
        mic_frames = []
        for _ in range(0, int(sample_rate / chunk * duration)):
            mic_data = input_stream.read(chunk)
            mic_frames.append(mic_data)

        # Join the list of byte objects into a single byte string, then convert to a NumPy array
        mic_signal = np.frombuffer(b"".join(mic_frames), dtype=np.int16)
        
        write("mic_signal.wav", sample_rate, mic_signal)
        input_stream.stop_stream()
        input_stream.close()

    # 获取当前播放文件后　duration　数据
    def record_speaker():
        nonlocal speaker_signal
        speaker_signal = playing_audio_after_n_seconds_data(current_playing_file_path, duration)
        write("speaker_signal.wav", sample_rate, speaker_signal)
        
    # 启动两个线程同步录制
    mic_thread = threading.Thread(target=record_mic)
    speaker_thread = threading.Thread(target=record_speaker)

    speaker_thread.start()
    mic_thread.start()
    # 等待线程结束
    mic_thread.join()
    speaker_thread.join()
    print("thread end")
    return mic_signal, speaker_signal


# 噪音抑制
def noise_reduction(duration=2):
    filter_order = 64  # 自适应滤波器阶数
    step_size = 0.5  # 步长
    # 调用函数进行同步录制
    mic_signal, speaker_signal = record_both_signals(duration)

    print("speaker_signal len:", len(speaker_signal))
    print("mic_signal len:", len(mic_signal))
    if len(speaker_signal) < len(mic_signal):
        return mic_signal.astype(np.float32)
    
    mic_signal = mic_signal.astype(np.float32)
    speaker_signal = speaker_signal.astype(np.float32)

    # 使用自适应滤波器处理信号
    _, error_signal, _ = adf.nlms(
        d=speaker_signal,  # 输入信号：扬声器音频
        u=mic_signal,  # 期望信号：麦克风音频
        M=filter_order,  # 滤波器阶数
        step=step_size,  # 步长
        returnCoeffs=True,
    )
    print("adf.nlms run completed.")
    # 检查 error_signal 是否有效
    print("error_signal min:", np.min(error_signal), "max:", np.max(error_signal))

    # 如果 error_signal 过小，可以尝试增益
    error_signal *= 2  # 放大信号，放大倍数可以调整
    # 归一化并转换 error_signal 以适合音频格式
    max_val = np.max(np.abs(error_signal))
    if max_val > 0:
        error_signal_normalized = error_signal / max_val  # 归一化到 -1 到 1 范围
        output_audio = np.int16(error_signal_normalized * 32767)  # 转换为 int16
    else:
        output_audio = np.zeros_like(error_signal, dtype=np.int16)

    # 保存处理后的误差信号为 WAV 文件
    write("noise_audio.wav", sample_rate, output_audio)
    print("音频文件已保存为 noise_audio.wav")
    output_audio = np.array(output_audio, dtype=np.int16)
    return output_audio.astype(np.float32)

# 2个音频文件混音，２个文件需要rate_sample一致
def mix_audio(file1, file2):
    # Load the two audio files
    rate1, audio1 = read(file1)
    rate2, audio2 = read(file2)

    # Ensure both files have the same sample rate
    assert rate1 == rate2, "Sample rates should match for mixing."

    # Convert both audio signals to mono if they are stereo
    if len(audio1.shape) > 1:  # If audio1 is stereo
        audio1 = np.mean(audio1, axis=1)  # Average the channels to make it mono
    if len(audio2.shape) > 1:  # If audio2 is stereo
        audio2 = np.mean(audio2, axis=1)  # Average the channels to make it mono

    # Ensure both files have the same length
    length = min(len(audio1), len(audio2))
    audio1 = audio1[:length]
    audio2 = audio2[:length]

    # Normalize to avoid clipping during mixing
    audio1 = audio1 / np.max(np.abs(audio1))
    audio2 = audio2 / np.max(np.abs(audio2))

    # Mix the audio by adding the arrays (reduce volume if needed)
    mixed_audio = (audio1 + audio2) / 2
    mixed_audio = np.int16(
        mixed_audio / np.max(np.abs(mixed_audio)) * 32767
    )  # Convert back to int16

    # Save the mixed audio to a new file
    write("mixed_output.wav", rate1, mixed_audio)
