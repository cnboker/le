import pyaudio
import wave

def record_wav():
  # Adjust parameters if necessary
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 44100  # Try 44100 if 16000 fails
    chunk = 8192
    record_secs = 5 
    dev_index = 0  # Make sure this matches your input device index
    wav_output_filename = './media/input.wav'

    audio = pyaudio.PyAudio()

    try:
        stream = audio.open(format=form_1, rate=samp_rate, channels=chans,
                            input_device_index=dev_index, input=True,
                            frames_per_buffer=chunk)
        print("Recording...")

        frames = []
        for _ in range(0, int(samp_rate / chunk * record_secs)):
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

        with wave.open(wav_output_filename, 'wb') as wf:
            wf.setnchannels(chans)
            wf.setsampwidth(audio.get_sample_size(form_1))
            wf.setframerate(samp_rate)
            wf.writeframes(b''.join(frames))
        print(f"Audio recorded and saved as {wav_output_filename}")

    return
