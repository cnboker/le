import asyncio
import os
import threading
from src.gminigpt import chat_with_Gemin
from src.record import record_wav
from src.asr import speech_to_text
from src.coqui_tts import connect_to_server, text_to_speech
from src.voice_wake2 import monitor_voice
from src.voice_play import playsound

from config.settings import (
    voice_event,
    question_audio_file_path,
    reply_audio_file_path,
    hi_audio_file_path,
    wait_audio_file_path,
)


async def voice_reply():
    print("voice reply...")
    # Get WAV from microphone.
    record_wav()

    # Convert audio into text.
    question = speech_to_text(question_audio_file_path)
    print("Asking: {0}".format(question))

    if question == "":
        return
    gpt_response = chat_with_Gemin(question)
    print("Response: {0}".format(gpt_response))

    if gpt_response == "":
        return
    # Convert ChatGPT response into audio.
    text_to_speech(gpt_response)
    #playsound(reply_audio_file_path)


def prepare():
    if not os.path.exists(hi_audio_file_path):
        text_to_speech("在请讲", hi_audio_file_path)
    if not os.path.exists(wait_audio_file_path):
        text_to_speech("稍等", wait_audio_file_path)


async def main():
    prepare()
    while True:
        voice_event.wait()
        # 在现有的事件循环中运行协程
        print("voice replay....")
        await voice_reply()
        voice_event.clear()


if __name__ == "__main__":
    connect_to_server()
    # 启动语音监测线程
    voice_wake_thread = threading.Thread(target=monitor_voice, daemon=True)
    voice_wake_thread.start()

    asyncio.run(main())
   