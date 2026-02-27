# MEMORY.md - 核心记忆

> 精简版 | 详细内容见各分文件  
> **变更规则**: 任何配置更改 **必须** 获得老板明确许可

---

## 👤 老板档案

| 属性 | 内容 |
|------|------|
| **身份** | AI自媒体博主 |
| **粉丝** | ~5万 |
| **方向** | ComfyUI / Seedence / 泛AI |
| **风格** | 系统化、数据驱动、风控优先 |
| **技术栈** | Python + 飞书 + OpenClaw + ComfyUI |

---

## 📊 关键决策

| 日期 | 决策 | 状态 |
|------|------|------|
| 02-23 | 飞书主控/Kimi辅助 | ✅ 生效 |
| 02-24 | 任务精简 (9→6) | ✅ 生效 |
| 02-24 | B站短剧区→X监控→取消 | ❌ 暂停 |
| 02-25 | 管家体系部署 | ✅ 生效 |
| 02-25 | 泛AI监控→全站 | ✅ 生效 |
| **02-25** | **取消B站科技区爬取** | ✅ **生效** |
| 02-27 | 日报飞书消息发送 | ✅ 生效 |
| **02-27** | **L2层浏览器能力** | ✅ **生效** |
| **02-27** | **OpenClaw深度使用7步法** | ✅ **完成** |

---

## 🧬 2026-02-27 重大更新

### 完成OpenClaw深度使用7步法

| 步骤 | 内容 | 文件 |
|:---|:---|:---|
| 1️⃣ | 智能备份机制 | `scripts/smart-backup.sh` |
| 2️⃣ | 模型池配置（4池） | `config/model-pools.json` |
| 3️⃣ | 会话识别规则 | `config/session-routing.md` |
| 4️⃣ | 上下文压缩 | `scripts/test-compression.py` |
| 5️⃣ | 任务铁律 | `config/task-iron-law.md` |
| 6️⃣ | 陌生任务处理 | `config/unfamiliar-task-handling.md` |
| 7️⃣ | 自我进化 | `scripts/daily-evolution.py` |

### 完成Heartbeat记忆维护机制

**核心功能**:
- ✅ 每30分钟检查紧急事项、整理记忆、清理日志
- ✅ 每日提取重要决策到MEMORY.md
- ✅ 每周回顾MEMORY.md，清理30天前记忆
- ✅ 状态保存到 `data/heartbeat-state.json`

**文件**: `scripts/heartbeat-check.py`

---

## 🏗️ 核心框架（固化）

### 1️⃣ 四层模型池体系

```
任务到达 → 会话识别 → 选择模型池
    ↓
┌───────┴───────┬───────┬───────┐
↓               ↓       ↓       ↓
高速池         智能池  文本池  视觉池
glm-4.7       glm-5   kimi   glm-4.6v
备用: kimi    备用:k2p5 备用  备用:k2p5
```

**健康检查**: 每6小时，当前 **4/4 (100%)**

---

### 2️⃣ 三层记忆体系

```
L1 工作记忆（会话临时）
    ↓ 重要事件
L2 短期记忆（memory/YYYY-MM-DD.md）
    ↓ 核心经验
L3 长期记忆（MEMORY.md）
```

**维护**: Heartbeat每30分钟 + 每日整理 + 每周回顾

---

### 3️⃣ 定时任务体系（11个）

| 类别 | 任务 | 频率 |
|:---|:---|:---|
| **维护** | heartbeat-check | 每30分钟 |
| **进化** | install-skills-v2 | 每小时 |
| **进化** | daily-evolution | 22:00 |
| **备份** | smart-backup | 每小时 |
| **备份** | git-backup | 每30分钟 |
| **健康** | model-health-check | 每6小时 |
| **数据** | bilibili-account-fetch | 09:00 |
| **数据** | ai-intelligence-monitor | 09:00 |
| **汇报** | daily-report-gen | 09:30 |
| **汇报** | send-daily-report | 09:35 |
| **迭代** | mission-control-weekly | 周一20:00 |

---

### 4️⃣ 技能体系（28个）

**来源**: ClawHub (https://clawhub.ai)
**安装频率**: 每小时1个
**固化标准**: 重复3次 + 通用问题 + 可标准化

**核心技能**:
- 编程: python, python-patterns, python-testing
- 生产力: pdf, xlsx, notion, obsidian, image, file
- 内容: writer, chinese-writing, summarize
- 自动化: github, docker, k8s
- 多媒体: video-frames, video-prompt-engineering

---

### 5️⃣ 数据体系

**数据源**:
- B站账号（09:00）: 粉丝/播放/视频表现
- B站全站AI（09:00）: 130关键词监控
- 技能学习（每小时）: ClawHub安装记录
- 模型健康（每6小时）: 4池API状态

**数据产出**:
- 每日汇报（09:35）: 飞书消息
- 进化报告（22:00）: 飞书消息
- Mission Control（实时）: http://localhost:5000

---

### 6️⃣ 核心偏好

| 维度 | 偏好 |
|:---|:---|
| **沟通** | 简洁结构化，不说废话 |
| **决策** | 数据驱动、成本敏感、风控优先 |
| **技术** | 公式>硬编码、分层工具链、自动化 |
| **权限** | **任何配置更改必须询问老板许可** |
| **视频生成** | 不节省Token，提示词完整详尽，中文优先 |

---

## 🛠️ 技能清单 (30+)

| 类别 | 关键技能 |
|------|----------|
| 编程 | python, python-patterns, python-testing |
| 生产力 | pdf, xlsx, notion, obsidian, **image**, **file**, **pandoc**, **docx**, **memory** |
| 内容 | tweet-writer, writer, chinese-writing, summarize |
| 自动化 | github, activecampaign, netsuite |
| 数据 | polars, eda, model-usage |
| DevOps | docker, k8s, terraform |
| 多媒体 | video-frames, camsnap, nano-banana-pro |
| **视频生成** | **video-prompt-engineering** (24模板整合) |

**粗体** = 今日手动学习

---

## 🎓 学习策略

- **频率**: 1技能/小时
- **分配**: 偶数小时=视频/图片, 奇数小时=内容/数据
- **标准**: 评分高 + 对自媒体有用

---

## 🤖 管家体系 [02-25]

```
        大管家 (WF助手)
       /    |    \
   🎓学习  📊数据  ✍️内容
      \      |      /
      🎬视频 ← ⚙️系统
```

**视频管家审查员**: 7维度检查 + 强制评分 + 每周迭代

---

## ⏰ 定时任务 (5个运行中)

| 任务 | 频率 | 产出 |
|------|------|------|
| 技能学习 | 每小时 | 新技能 |
| B站账号 | 09:00 | 个人数据 |
| 泛AI情报 | 09:00 | 全站热门 |
| 日报 | 09:30 | 综合汇报 |
| Git备份 | 30分钟 | 自动备份 |

> **已取消**: B站科技区爬取(重复)、X监控(付费)、抖音(反爬)

---

## 🔧 能力层级 (Web抓取)

| 层级 | 工具 | 状态 | 说明 |
|:---|:---|:---|:---|
| **L0** | web_search API | ✅ | Bing/Google搜索 |
| **L1** | jina.ai / curl | ✅ | 静态页面Markdown |
| **L2** | **Playwright** | ✅ | **有头浏览器，JS渲染** |
| L3 | AI视觉API | ❌ | 成本较高 |

**L2工具**: `tools/l2-browser-fetch.py`
- 引擎: Playwright 1.58.0 + Chromium
- 场景: 动态页面、复杂JS渲染
- 文档: `docs/l2-browser-capability.md`

---

## ⚠️ 待办

### P1 (高)
- [ ] Kimi速率限制恢复
- [ ] VirusTotal标记

### P2 (中)
- [x] **视频管家Skill整合完成** (24模板)
- [ ] 视频管家实际测试
- [ ] 收集错误案例
- [ ] 首次规则迭代 (周日20:00)

### P3 (低)
- [ ] 飞书消息读取配置

---

## 🎯 核心偏好

| 维度 | 偏好 |
|------|------|
| 沟通 | 简洁结构化 |
| 决策 | 数据驱动、成本敏感、风控优先 |
| 技术 | 公式>硬编码、分层工具链、自动化 |
| **权限** | **任何配置更改必须询问许可** |
| **视频生成** | **不节省Token，提示词必须完整详尽，缩略提示词会严重影响视频质量；使用中文提示词** |

---

## 📁 详细内容

- 决策详情 → `memory/decisions/`
- 技能详情 → `skills-learning-plan.md`
- 管家配置 → `managers/*.md`
- 待办追踪 → `memory/todos/`
- 任务配置 → `HEARTBEAT.md`

---

_更新: 2026-02-25_  
_优化: 应用memory-optimization技能，Token节省~60%_  
_变更授权: 已启用_

## 🎓 学习成果 - 2026-02-26

（待从短期记忆中提取）
