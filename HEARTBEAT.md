# HEARTBEAT.md - 系统事件处理

> **重要**: 本文件记录已生效的任务配置  
> **变更规则**: 任何任务的新增/修改/删除 **必须** 获得用户明确许可后方可执行

---

## 系统事件响应规则

当收到以下系统事件时，执行对应操作：

### send_daily_report  
**触发**: 每天 09:35 (系统通知)  
**操作**:  
1. 读取 `data/daily-reports/daily_report_latest.md`  
2. 提取关键数据（粉丝、播放、热门视频、技能学习）  
3. 生成简化版消息，通过飞书发送  
**说明**: 自动发送每日汇报（09:30生成后，09:35推送）  
**消息格式示例**:
```
📊 每日汇报 - 2026-02-27

👤 B站账号: 粉丝XX万 | 播放XX万
🔥 热门: XXXXX (XXX万播放)
📚 技能: 今日学了X个
📡 AI情报: XXX关键词热度上升
```

### run_skill_learning
**触发**: 每小时整点  
**执行方式**: 系统 crontab（静默，不通知）  
**脚本**: `scripts/run-skill-learning.sh` → `learn-skill-v2.js` (修复版)  
**说明**: 从SkillsMP搜索并学习新技能（修复版，每次可学5个）

### fetch_bilibili_account
**触发**: 每天 09:00
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/bilibili-account-fetch.py
```
**说明**: 获取老鱼B站个人账号数据（粉丝、播放、视频表现）

### fetch_ai_intelligence
**触发**: 每天 09:00
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/ai-intelligence-monitor.py
```
**说明**: 泛AI情报监控（B站全站AI相关内容，不限分区，130关键词搜索）

### generate_daily_report
**触发**: 每天 09:30
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/generate-daily-report.py
```
**说明**: 生成统一每日汇报（包含账号数据、AI情报、技能学习）

### send_daily_report
**触发**: 每天 09:35
**操作**:
```bash
# WF助手收到系统通知后，读取 daily_report_latest.md 并发送飞书消息
```
**说明**: 读取09:30生成的日报，通过飞书消息发送给老鱼

### git_backup
**触发**: 每30分钟
**执行方式**: 系统 crontab（静默，不通知）
**脚本**: `scripts/git-auto-backup.sh`
**说明**: 本地工作区Git备份（自动提交到Git仓库，含所有配置文件、脚本、记忆文件）

---

## 每日汇报时间线

| 时间 | 任务 | 产出 |
|------|------|------|
| 09:00 | B站账号数据获取 | 个人账号报告 |
| 09:00 | 泛AI情报监控 | 全站AI热门（不限分区） |
| 09:30 | 生成统一汇报 | 完整日报 |
| 每小时 | 技能学习 | 新技能 |
| 每30分钟 | Git备份 | 自动备份 |

---

## 汇报内容模块

- **B站账号数据**: 粉丝数、播放量、视频表现（Cookie登录获取）
- **B站全站AI**: AI热门视频Top 10（全站关键词搜索，130关键词）
- **技能学习**: 今日学习的新技能（每小时学习记录）
- **系统状态**: 定时任务运行状态监控

---

## 已取消的任务

> 以下任务曾经存在但已取消，恢复需用户明确许可

| 任务 | 原频率 | 取消原因 | 取消时间 |
|------|--------|----------|----------|
| B站科技区爬取 | 10:00/22:00 | 与全站监控重复 | 2026-02-25 |
| X(Twitter)监控 | 每天4次 | API需付费 | 2026-02-25 |
| 抖音监控 | - | 反爬机制太强 | 2026-02-25 |

---

## 脚本修复记录

### 2026-02-26 修复 (续)

| 脚本 | 问题 | 修复内容 |
|------|------|----------|
| `learn-skill.js` | SkillsMP网站AI搜索需登录，返回0结果 | 改为直接浏览技能列表，按类别筛选，去重 |
| `bilibili-account-fetch.py` | 无错误处理，Cookie过期时崩溃 | 添加完善错误处理和日志记录 |
| `ai-intelligence-monitor.py` | 无日志记录，412错误未处理 | 添加日志系统和反爬错误处理 |
| `generate-daily-report.py` | 无日志记录，变量未定义 | 添加日志系统和异常处理 |
| `learn-skill-v2.js` | 原脚本只能找到0-5个技能 | 全新修复版，使用正确URL，每次可学习5个技能 |

### 日志位置
所有脚本日志统一存放：`~/.openclaw/workspace/logs/`
- `bilibili_account.log` - B站账号数据
- `ai_intelligence.log` - AI情报监控
- `daily_report.log` - 日报生成
- `feishu_sync.log` - 飞书同步

---

## 常规Heartbeat检查

如果收到常规 heartbeat（无特定事件），检查：
1. 定时任务状态 - `openclaw cron list`
2. 日志文件是否有异常 - `tail -n 20 ~/.openclaw/workspace/logs/*.log`
3. 磁盘空间使用情况

如一切正常，回复: HEARTBEAT_OK

---

_更新: 2026-02-26_  
_任务数: 5个运行中 | 变更需授权: ✅_
