import os
import sys
import threading
from multiprocessing import Process
import time
from src.geminiClient import chat_with_Gemin
from src.record import record_wav
from src.stt import speech_to_text
from src.tts import text_to_speech
from src.voice_wake import  monitor_voice
from src.voice_play import playsound
from config.settings import voice_event,question_audio_file_path,reply_audio_file_path,hi_audio_file_path,wait_audio_file_path

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./src")))

def voice_reply():
    # Get WAV from microphone.
    record_wav()

    # Convert audio into text.
    question = speech_to_text(question_audio_file_path)
    # Send text to ChatGPT.
    print("Asking: {0}".format(question))
    
    if question == "":
        return
    gpt_response = chat_with_Gemin(question)
    print("Response: {0}".format(gpt_response))

    if gpt_response == "":
        return
    # Convert ChatGPT response into audio.
    text_to_speech(gpt_response)

    # Play audio of reponse.
    playsound(reply_audio_file_path)
    return


def perpare():
     if not os.path.exists(hi_audio_file_path):
        text_to_speech("来啦", hi_audio_file_path)
     if not os.path.exists(wait_audio_file_path):
        text_to_speech("稍等", wait_audio_file_path)


if __name__ == "__main__":
    #普通线程在程序中是非守护线程。主线程会等待所有非守护线程完成后再退出。
    #守护线程是一种特殊类型的线程，用于执行后台任务。它的生命周期依赖于主线程。
    # voice_wake_thread = threading.Thread(target=monitor_voice, daemon=True)    
    voice_reply_thread = Process(target=voice_reply, daemon=True) 
    perpare()
    while True:
        try:
            # voice_wake_thread.start()        
            # voice_event.wait()
            # voice_event.clear()        
            # #关闭唤醒线程重新开启
            # voice_wake_thread.join() 
            monitor_voice()
            print("得到小乐回应")
            time.sleep(2)
            if voice_reply_thread.is_alive():
                voice_reply_thread.terminate()
                voice_reply_thread.join()
                voice_reply_thread = Process(target=voice_reply)
            else:
                # 正常结束
                if voice_reply_thread.exitcode == 0:
                    voice_reply_thread = Process(target=voice_reply)
                    
            voice_reply_thread.start()  
           
            time.sleep(5)
            print('begin new voice_wake')
            # voice_wake_thread = threading.Thread(target=monitor_voice)
            # voice_wake_thread.start()
        except KeyboardInterrupt:
                print("app exit")
                sys.exit(0)
        finally:
            print("continue")
        
