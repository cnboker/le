#!/bin/bash

# 定义日志文件
LOG_FILE="/var/log/startup_script.log"

# 写入脚本开始执行的时间
echo "Starting startup script at $(date)" 

# 配置 DNS
echo "Setting DNS..."
nmcli con mod preconfigured ipv4.dns "8.8.8.8 8.8.4.4" 
if [ $? -eq 0 ]; then
    echo "DNS set successfully"
else
    echo "Failed to set DNS" 
fi

# 开启 VPN 连接
echo "Starting VPN connection..."
echo "c myvpn" | /var/run/xl2tpd/l2tp-control 
if [ $? -eq 0 ]; then
    echo "VPN connection started"
else
    echo "Failed to start VPN or timed out" 
fi
echo "Wait 3 seconds" 
sleep 3

# 添加路由
echo "Adding routes..." 
# 等待 VPN 连接成功
if [ -f /var/run/xl2tpd/l2tp-control ]; then
    route add 192.168.0.102 gw 192.168.0.1
    route add 112.90.60.254 gw 192.168.0.1
    route add default dev ppp0
else
    echo "VPN connection not established, skipping route add" 
fi
# 检查 IPsec 状态并连接
echo "Starting IPsec connection..." 
ipsec up myvpn
if [ $? -eq 0 ]; then
    echo "IPsec started successfully" 
else
    echo "Failed to start IPsec" 
fi
