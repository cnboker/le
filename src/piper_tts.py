import subprocess


#output 输出文件名称
def text_to_speech(text,output_file):

    piper_file = "./piper/piper"   
    model_path = "./piper/zh_CN-huayan-medium.onnx"

    command = [
        piper_file,
        "--model",
        model_path,
        "--output_file",
        output_file,
        "--length-scale 1.2",  # 这个参数控制语音的整体时长或语速。默认值为 1.0。如果你想让语音变慢，可以设置大于 1.0 的值，比如 1.2；如果想让语速变快，可以设置小于 1.0 的值，比如 0.8。
        "--noise-scale 0.5"  # 这个参数控制生成语音时的音色随机性，影响语音的抑扬顿挫。默认值为 0.667。将此参数调高会增加语音的多样性，但可能会导致语音不稳定；调低则会使语音更加一致，但可能显得单调。
        "--noise-w 0.9",  # 控制每个音素的停顿与重音，默认为 0.8。增大此参数会让每个音素的重音更明显，有助于生成更有节奏感的声音；减小它会使声音更加平滑
        "--sample_rate 22050",      
    ]
    print("command", command)
    p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    p2 = subprocess.run(command, stdin=p1.stdout, capture_output=True, text=True)
    p1.stdout.close()

    print(p2.stdout)
    print("p2.stderr->", p2.stderr)
