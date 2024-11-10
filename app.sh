#!/bin/bash


# 激活 Python 虚拟环境并运行脚本

cd /home/voice/le
source ./myvenv/bin/activate 
if [ $? -eq 0 ]; then
    echo "Python environment activated successfully" 
else
    echo "Failed to activate Python environment" 
fi

python ./main.py 
if [ $? -eq 0 ]; then
    echo "Python script executed successfully"
else
    echo "Failed to execute Python script" 
fi

# 记录脚本完成的时间
echo "Startup script completed at $(date)" 
