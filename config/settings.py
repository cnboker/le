import vosk
import os

api_key = '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'

sample_rate = 44100
vosk_model = vosk.Model(os.path.expanduser("~") + "/code/voice_chatgpt/.venv/vosk-model-cn-0.22")
