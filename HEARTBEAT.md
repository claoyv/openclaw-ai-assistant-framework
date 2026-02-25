# HEARTBEAT.md - 系统事件处理

## 系统事件响应规则

当收到以下系统事件时，执行对应操作：

### run_skill_learning
**触发**: 每小时整点
**操作**: 
```bash
cd ~/.openclaw/workspace && node learn-skill.js >> learn-cron.log 2>&1
```
**说明**: 从SkillsMP搜索并学习一个新技能

### fetch_bilibili_tech
**触发**: 每天 10:00 和 22:00
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/bilibili-tech-fetch.py
```
**说明**: 爬取B站科技区AI视频数据

### generate_daily_report
**触发**: 每天 09:00
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/generate-daily-report.py
```
**说明**: 生成每日汇报并发送给用户

### git_backup
**触发**: 每30分钟
**操作**:
```bash
cd ~/.openclaw/workspace && git add . && git commit -m "auto: $(date +%Y-%m-%d-%H:%M) backup" && git push origin main 2>/dev/null || true
```
**说明**: 自动备份工作区到Git

## 常规Heartbeat检查

如果收到常规 heartbeat（无特定事件），检查：
1. 定时任务状态 - `openclaw cron list`
2. 磁盘空间使用情况
3. 最近的错误日志

如一切正常，回复: HEARTBEAT_OK
