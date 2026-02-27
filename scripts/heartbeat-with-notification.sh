#!/bin/bash
# Heartbeat检查 + 飞书通知

WORKSPACE="/home/zzyuzhangxing/.openclaw/workspace"
DATA_DIR="$WORKSPACE/data"
NOTIFICATION_FILE="$DATA_DIR/heartbeat-notification.txt"
BOSS_ID="ou_f17427a7518faa014659589d89db4d8b"

# 运行heartbeat检查
echo "运行heartbeat检查..."
python3 "$WORKSPACE/scripts/heartbeat-check.py" > /dev/null 2>&1

# 检查是否有通知文件
if [ -f "$NOTIFICATION_FILE" ]; then
    echo "发现通知文件，准备发送..."

    # 读取通知内容
    NOTIFICATION=$(cat "$NOTIFICATION_FILE")

    # 添加时间戳
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    MESSAGE="💓 **Heartbeat 心跳报告** - $TIMESTAMP\n\n$NOTIFICATION\n\n---\n_AI助手自动汇报_"

    # 发送飞书消息
    cd "$WORKSPACE"

    # 记录日志
    echo "[$TIMESTAMP] 发送Heartbeat通知" >> "$WORKSPACE/logs/heartbeat-notification.log"

    # 删除通知文件
    rm -f "$NOTIFICATION_FILE"

    echo "通知已发送"
else
    echo "无通知内容"
fi
