import threading
import pyaudio
import numpy as np
import adaptfilt as adf
from scipy.io.wavfile import write, read
from scipy.signal import butter, lfilter
import scipy.io.wavfile as wav
from scipy.fftpack import fft, ifft
import scipy.signal as signal



def record_both_signals(duration, sample_rate=22050):
    chunk = 2205  # 缓冲区大小
    channels = 1
    # 缓存麦克风信号和扬声器信号
    speaker_signal = []
    mic_signal = []

    # 录制麦克风信号
    def record_mic():
        nonlocal mic_signal

        _, mic_signal = read("./mic_signal.wav")

        mic_signal = np.frombuffer(mic_signal, dtype=np.int16)
        

    # 录制扬声器信号
    def record_speaker():
        nonlocal speaker_signal
        _, speaker_signal = read("./speaker_signal.wav")
        speaker_signal = np.frombuffer(speaker_signal, dtype=np.int16)
    

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


def noise_reduction():
    sample_rate = 22050  # 采样率

    filter_order = 16  # 自适应滤波器阶数
    step_size = 0.2  # 步长
    duration = 5  # 录音时长

    # 调用函数进行同步录制
    mic_signal, speaker_signal = record_both_signals(duration)
    min_length = min(len(mic_signal), len(speaker_signal))
    mic_signal = mic_signal[:min_length]
    speaker_signal = speaker_signal[:min_length]

    print("speaker_signal len:", len(speaker_signal))
    print("mic_signal len:", len(mic_signal))
    mic_signal = mic_signal.astype(np.float32)
    speaker_signal = speaker_signal.astype(np.float32)

    mic_signal = mic_signal / np.max(np.abs(mic_signal))
    #mic_signal = np.clip(mic_signal, -1.0, 1.0)  # 限制范围
    #mic_signal = (mic_signal * 32767).astype(np.int16)  # 转换为 int16

    speaker_signal = speaker_signal / np.max(np.abs(speaker_signal))
    #speaker_signal = speaker_signal[1000:]
    #speaker_signal = np.clip(speaker_signal, -1.0, 1.0)  # 限制范围
    #speaker_signal = (speaker_signal * 32767).astype(np.int16)  # 转换为 int16
    print(mic_signal[:50])
    print(speaker_signal[:50])
    #denoised_signal =   mic_signal -speaker_signal 
    
    #wav.write("denoised_audio.wav", sample_rate, denoised_signal)
    # # 对结果进行适当增益控制
    # gain_factor = 0.8  # 设置增益因子，避免幅度过大或失真
    # audio_data = audio_data * gain_factor
    # # 如果 audio_data 是 float 数组，确保其在 -1.0 到 1.0 之间并转换为 int16
    # audio_data = np.clip(audio_data, -1.0, 1.0)  # 限制范围
    # audio_data = (audio_data * 32767).astype(np.int16)  # 转换为 int16
    # write("test.wav", sample_rate, output_signal)
    # 保存降噪后的音频
    # wav.write("denoised_audio.wav", sample_rate, denoised_signal)
    # mic_signal = normalize_audio(mic_signal)
    # speaker_signal = normalize_audio(speaker_signal)

    # fs = 22050
    # lowcut = 100   # 带通滤波器的低频截止（背景音频段起点）
    # highcut = 1000 # 带通滤波器的高频截止（背景音频段终点）
    # mic_signal = apply_bandpass_filter(mic_signal, lowcut, highcut, fs)
    # speaker_signal = apply_bandpass_filter(speaker_signal, lowcut, highcut, fs)

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
    write("output.wav", sample_rate, output_audio)
    print("音频文件已保存为 output.wav")


# def test_get_audio_segment_after_n_seconds():
#      get_audio_segment_after_n_seconds(current_playing_file_path, 2000)


def test_noise_reduction():
    noise_reduction()
