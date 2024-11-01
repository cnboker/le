import pyaudio
import wave
from config.settings import sample_rate,question_audio_file_path

def record_wav():
  # Adjust parameters if necessary
    chans = 1
    chunk = 8192
    record_secs = 5 

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, rate=sample_rate, channels=chans,
                             input=True,
                            frames_per_buffer=chunk)
    try:
      
        print("Recording...")

        frames = []
        for _ in range(0, int(sample_rate / chunk * record_secs)):
            data = stream.read(chunk)
            frames.append(data)

        print("Finished recording.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Cleanup
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(question_audio_file_path, 'wb') as wf:
            wf.setnchannels(chans)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        print(f"Audio recorded and saved as {question_audio_file_path}")

    return
