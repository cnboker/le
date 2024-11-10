FROM python:3.12.3

# 更新包管理器并安装 python3-pyaudio 和其他依赖
# RUN apt-get update && \
#     apt-get install -y python3-pyaudio && \
#     rm -rf /var/lib/apt/lists/*

# 安装必要的系统工具
RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio

WORKDIR /app
COPY src /app/src
COPY data /app/data
COPY media /app/media
COPY piper /app/piper
COPY config /app/config
COPY main.py /app
COPY requirements.txt /app

# 更新 pip
RUN pip install --no-cache-dir --upgrade pip

# 创建并激活虚拟环境
RUN python -m venv venv

# 安装依赖
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

#run app
CMD ["venv/bin/python", "main.py"]

