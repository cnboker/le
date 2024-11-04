import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg', 'GTK3Agg'
import matplotlib.pyplot as plt
import wave

# 读取 WAV 文件
def read_wav(file_path):
    with wave.open(file_path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)

    # 将音频数据转换为 NumPy 数组
    audio_data = np.frombuffer(audio_data, dtype=np.int16)
    return audio_data, framerate

# 进行傅里叶变换
def perform_fourier_transform(audio_data):
    N = len(audio_data)
    fourier_transform = np.fft.fft(audio_data)
    frequency = np.fft.fftfreq(N, d=1/N)  # Frequency bins
    return fourier_transform, frequency

# 绘制频谱
# 绘制频谱
def plot_combined_spectrum(fourier_transform1, frequency_mic, fourier_transform2, frequency_speaker, framerate,N):
    plt.figure(figsize=(12, 6))
    N = len(audio_data)
    # 第一个音频信号的频谱
    plt.subplot(1, 2, 1)
    plt.plot(frequency_mic[:N//2], np.abs(fourier_transform1)[:N//2])
    plt.title("Mic Signal Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 0.5 * framerate)  # Adjust the limit according to your sampling rate
    plt.grid()

    # 第二个音频信号的频谱
    plt.subplot(1, 2, 2)
    plt.plot(frequency_speaker[:N//2], np.abs(fourier_transform2)[:N//2])
    plt.title("Speaker Signal Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 0.5 * framerate)  # Adjust the limit according to your sampling rate
    plt.grid()

    plt.tight_layout()  # Adjust subplots to fit into figure area.
    plt.show()

# 主程序
if __name__ == "__main__":
    print("start")
    #audio_file = "./mic_signal.wav"
    audio_file = "./media/file3-1.wav"
    audio_data, framerate = read_wav(audio_file)
    fourier_transform_mic, frequency_mic = perform_fourier_transform(audio_data)
    #plot_spectrum(fourier_transform, frequency)

    audio_file = "./speaker_signal.wav"
    #audio_file = "./media/mixed_output1-1.wav"
    audio_data, framerate = read_wav(audio_file)
    fourier_transform_speaker, frequency_speaker = perform_fourier_transform(audio_data)
    #plot_spectrum(fourier_transform, frequency)
    # 绘制合并频谱
    plot_combined_spectrum(fourier_transform_mic, frequency_mic, fourier_transform_speaker, frequency_speaker, framerate, len(audio_data))