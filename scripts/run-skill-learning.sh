#!/bin/bash
# 技能学习定时任务脚本 - ClawHub CLI版

cd /home/zzyuzhangxing/.openclaw/workspace || exit 1

# 记录开始时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始技能学习..." >> learn-cron.log

# 执行学习脚本（使用CLI版）
node learn-skill-cli.js >> learn-cron.log 2>&1

# 记录结束
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 技能学习完成" >> learn-cron.log
echo "---" >> learn-cron.log
