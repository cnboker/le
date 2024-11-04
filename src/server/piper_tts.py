from flask import Flask, request, jsonify, send_file
import subprocess
import sys
import os

app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def generate_speech():
    data = request.get_json()
    text = data.get("text")

    piper_path_base = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../piper")
    )
    piper_file = piper_path_base + "/piper"
    output_file = piper_path_base + "/output.wav"
    model_path = piper_path_base + "/zh_CN-huayan-medium.onnx"
    sample_rate = 22050  # 目标采样率

    command = [
        piper_file,
        "--model",
        model_path,
        "--output_file",
        output_file,
        '--sample_rate', str(sample_rate)  # 添加采样率参数
    ]
    print("command", command)
    p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    p2 = subprocess.run(command, stdin=p1.stdout, capture_output=True, text=True)
    p1.stdout.close()

    print(p2.stdout)
    print("p2.stderr->", p2.stderr)
    if p2.returncode != 0:
        return jsonify({"error": p2.stderr}), 500

    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
