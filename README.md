# VoiceGPT

# pip freeze > requirements.txt

## pip install -r requirements.txt

# precise train

```bash
precise-train ./data/mycroft-precise/ --model mymodel.pb
```

# Record command

```shell
arecord -d 2 -f cd ./data/mycroft precise/positive/hi-2.wav
```

# Docker build 

```bash
sudo docker build -t myvoice:latest .
# attach host audio resource
sudo docker run --rm -it   --device /dev/snd   -e ALSA_CARD=0   -v /run/user/$(id -u)/pulse:/run/user/$(id -u)/pulse   -v ~/.config/pulse/cookie:/root/.config/pulse/cookie   myvoice:latest
```

# publish to respberry

```bash
scp -r config media piper src main voice@192.168.0.102:/home/voice/le
```

# reaspberry pi issue

``` bash
    # install audio driver
    sudo apt-get install alsa-utils pulseaudio
    sudo apt-get install pulseaudio
    pulseaudio --start

   # install pyAudio failure
    sudo apt-get install -y python3-pyaudio portaudio19-dev
    pip install PyAudio
    pip install -r requirements.txt
```

# 部署自启动程序

### 配置脚本自动运行： 将脚本放在 /etc/network/if-up.d/ 目录中会确保网络连接后自动运行。每次网络接口启动后，系统会自动执行该脚本。确保脚本内容和路径正确无误

``` bash
cp ./voice_startup.sh start_vpn.sh /etc/network/if-up.d/
chomd +x voice_startup.sh

# log view
sudo journalctl -u networking.service

```

# speaker test

```bash
speaker-test -c2
```