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
**脚本**: `scripts/run-skill-learning.sh` → `learn-skill-cli.js` (ClawHub CLI版)  
**说明**: 
- 使用 ClawHub CLI 直接安装技能
- 从推荐列表中选择未安装的技能
- 每小时安装5个新技能
- 自动跳过已安装的技能
**技能来源**: ClawHub (https://clawhub.ai)
**推荐技能**: python, writer, summarize, image, video-frames, github, docker等30+
**当前进度**: 持续增长中

### install_next_skill_infinite
**触发**: 每小时整点
**执行方式**: 系统 cron
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/install-skills-infinite.py
```
**说明**: 
- **无限学习模式** - 从ClawHub持续安装新技能
- 自动跳过已安装的技能
- 每小时安装1个新技能
- 永不停止，持续学习
**技能来源**: ClawHub (https://clawhub.ai)
**已安装**: 28个（持续增长）
**目标**: 无限学习，持续进化

### fetch_bilibili_account
**触发**: 每天 09:00
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/bilibili-account-fetch.py
```
**说明**: 获取老板B站个人账号数据（粉丝、播放、视频表现）

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
**说明**: 读取09:30生成的日报，通过飞书消息发送给老板

### git_backup
**触发**: 每30分钟
**执行方式**: 系统 crontab（静默，不通知）
**脚本**: `scripts/git-auto-backup.sh`
**说明**: 本地工作区Git备份（自动提交到Git仓库，含所有配置文件、脚本、记忆文件）

### mission_control_iteration
**触发**: 每周一 20:00
**操作**:
1. 读取 `mission-control/ITERATION_PLAN.md`
2. 回顾上周使用情况
3. 分析数据（访问次数、功能使用率）
4. 确定本周优化项
5. 发送飞书消息提醒老板
**说明**: Mission Control每周迭代会议
**迭代周期**: 每周一 20:00
**下次迭代**: 2026-03-02 20:00

### smart_backup_check
**触发**: 每小时整点
**操作**:
```bash
bash ~/.openclaw/workspace/scripts/smart-backup.sh
```
**说明**: 
- 智能备份：24小时或10K变化触发
- 本地备份：7天轮换（周一~周日）
- 云端同步：iCloud（可选）
**备份文件**: MEMORY.md, USER.md, IDENTITY.md, SOUL.md, AGENTS.md, HEARTBEAT.md, TOOLS.md, openclaw.json
**恢复方式**: `bash scripts/auto-restore.sh` 或查看 `docs/backup-restore-guide.md`

### model_health_check
**触发**: 每6小时
**操作**:
```bash
python3 scripts/model-health-check.py
```
**说明**: 
- 检查模型池健康程度
- 检查API可达性、Token余额、Rate Limit
- 记录健康状态到 `data/model-health-status.json`
**模型池**: 高速池、智能池、文本池、视觉池

### heartbeat_check
**触发**: 每30分钟
**操作**:
```bash
python3 scripts/heartbeat-check.py
```
**说明**: 
- **让记忆"活"起来**的维护机制
- 检查紧急事项（邮件/日历）
- 整理短期记忆到长期记忆
- 清理过期日志（7天前）
- 检查需要提醒用户的事
**状态保存**: `data/heartbeat-state.json`
**输出**: 发现问题时返回非0状态码（触发通知）

**维护任务**:

#### 每日执行
- ✅ 检查过去24小时的memory文件
- ✅ 提取重要决策/偏好 → 更新MEMORY.md
- ✅ 删除已处理的临时信息

#### 每周执行（周日）
- ✅ 回顾本周MEMORY.md，补充遗漏
- ✅ 更新项目状态
- ✅ 清理超过30天的daily memory

---
**触发**: 每天 22:00
**操作**:
```bash
cd ~/.openclaw/workspace && python3 scripts/daily-evolution.py
```
**说明**:
- **回顾今日会话历史**
- **分析学习成果**（包含今日安装的技能）
- **分析错误和解决方案**
- **生成进化报告**
- **提议可固化的技能**
- **保存报告**到 `data/evolution-reports/`
- **通过飞书发送报告**
**进化指标**: 
- 学习技能: 1个/天（自动统计今日安装）
- 固化技能: 1个/周
- 错误减少: 50%/月
- 效率提升: 20%/月
**整合功能**: 
- ✅ 技能学习统计（从`.skill-install-status-v2.json`读取）
- ✅ 会话分析（从`memory/YYYY-MM-DD.md`读取）
- ✅ 错误总结（从会话历史提取）
- ✅ 固化建议（基于重复使用次数）

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
