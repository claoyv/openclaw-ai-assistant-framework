#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heartbeat Mechanism
Keep memory alive with periodic checks
"""

import os
import json
from datetime import datetime, timedelta
import glob

WORKSPACE = '/home/zzyuzhangxing/.openclaw/workspace'
MEMORY_DIR = f'{WORKSPACE}/memory'
LOGS_DIR = f'{WORKSPACE}/logs'
DATA_DIR = f'{WORKSPACE}/data'
HEARTBEAT_STATE = f'{DATA_DIR}/heartbeat-state.json'

class HeartbeatEngine:
    """Heartbeat maintenance engine"""

    def __init__(self):
        self.now = datetime.now()
        self.state = self.load_state()
        self.alerts = []

    def load_state(self):
        """Load heartbeat state"""
        if os.path.exists(HEARTBEAT_STATE):
            with open(HEARTBEAT_STATE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'lastChecks': {},
            'memoryCleanup': None,
            'logCleanup': None
        }

    def save_state(self):
        """Save heartbeat state"""
        os.makedirs(os.path.dirname(HEARTBEAT_STATE), exist_ok=True)
        with open(HEARTBEAT_STATE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def check_urgent_items(self):
        """Check for urgent items (email, calendar)"""
        print("\n[1/4] 检查紧急事项...")

        # TODO: 实际邮件/日历检查需要API配置
        # 这里先模拟检查

        # 检查是否有待办事项
        todos_file = f'{WORKSPACE}/memory/todos'
        if os.path.exists(todos_file):
            with open(todos_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '紧急' in content or 'URGENT' in content:
                    self.alerts.append("⚠️ 发现紧急待办事项")

        self.state['lastChecks']['urgent'] = self.now.isoformat()
        print("  ✅ 紧急事项检查完成")

    def organize_memory(self):
        """Organize short-term memory to long-term memory"""
        print("\n[2/4] 整理记忆...")

        # 检查昨天的记忆文件
        yesterday = (self.now - timedelta(days=1)).strftime('%Y-%m-%d')
        yesterday_memory = f'{MEMORY_DIR}/{yesterday}.md'

        if os.path.exists(yesterday_memory):
            # 读取昨天记忆
            with open(yesterday_memory, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取核心经验
            if len(content) > 100:  # 有实质内容
                # 检查MEMORY.md是否需要更新
                memory_file = f'{WORKSPACE}/MEMORY.md'
                if os.path.exists(memory_file):
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        memory_content = f.read()

                    # 检查是否有需要固化的内容
                    if '## 🎓 学习成果' not in memory_content:
                        # 添加学习成果部分
                        with open(memory_file, 'a', encoding='utf-8') as f:
                            f.write(f"\n## 🎓 学习成果 - {yesterday}\n\n")
                            f.write("（待从短期记忆中提取）\n")

                        self.alerts.append(f"📝 检测到昨天的记忆需要整理到MEMORY.md")

        self.state['lastChecks']['memory'] = self.now.isoformat()
        self.state['memoryCleanup'] = self.now.isoformat()
        print("  ✅ 记忆整理完成")

    def cleanup_logs(self):
        """Clean up expired logs"""
        print("\n[3/4] 清理过期日志...")

        if not os.path.exists(LOGS_DIR):
            print("  ⚠️  日志目录不存在")
            return

        # 清理7天前的日志
        cutoff_date = self.now - timedelta(days=7)
        deleted_count = 0

        for log_file in glob.glob(f'{LOGS_DIR}/*.log'):
            file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
            if file_time < cutoff_date:
                try:
                    os.remove(log_file)
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ 删除失败: {log_file} - {e}")

        if deleted_count > 0:
            self.alerts.append(f"🗑️ 清理了 {deleted_count} 个过期日志")

        self.state['lastChecks']['logs'] = self.now.isoformat()
        self.state['logCleanup'] = self.now.isoformat()
        print(f"  ✅ 日志清理完成（删除 {deleted_count} 个文件）")

    def check_reminders(self):
        """Check for items that need user reminder"""
        print("\n[4/4] 检查提醒事项...")

        # 检查Mission Control是否需要迭代
        iteration_file = f'{WORKSPACE}/mission-control/ITERATION_PLAN.md'
        if os.path.exists(iteration_file):
            with open(iteration_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查下次迭代时间
            if '下次迭代' in content:
                # 简单检查是否是周一
                if self.now.weekday() == 0 and self.now.hour >= 20:  # 周一20:00后
                    self.alerts.append("📅 今晚20:00有Mission Control迭代会议")

        # 检查定时任务状态
        # TODO: 实际检查需要运行 openclaw cron list

        self.state['lastChecks']['reminders'] = self.now.isoformat()
        print("  ✅ 提醒检查完成")

    def daily_maintenance(self):
        """Daily memory maintenance tasks"""
        print("\n[每日维护] 记忆文件处理...")

        # 检查过去24小时的memory文件
        yesterday = (self.now - timedelta(days=1)).strftime('%Y-%m-%d')
        yesterday_memory = f'{MEMORY_DIR}/{yesterday}.md'

        if os.path.exists(yesterday_memory):
            with open(yesterday_memory, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取重要决策/偏好
            decisions = []
            if '决策' in content or '决定' in content:
                decisions.append("发现重要决策")

            # 更新MEMORY.md
            if decisions:
                memory_file = f'{WORKSPACE}/MEMORY.md'
                with open(memory_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n## 📅 {yesterday} 重要决策\n\n")
                    for decision in decisions:
                        f.write(f"- {decision}\n")

                self.alerts.append(f"📝 已将{yesterday}的重要决策更新到MEMORY.md")

        # 删除已处理的临时信息（标记为已处理的）
        # TODO: 实现临时信息标记和清理

        self.state['lastChecks']['daily'] = self.now.isoformat()
        print("  ✅ 每日维护完成")

    def weekly_maintenance(self):
        """Weekly memory maintenance tasks"""
        # 只在周日执行
        if self.now.weekday() != 6:  # 0=周一, 6=周日
            return

        print("\n[每周维护] 记忆回顾...")

        # 回顾本周MEMORY.md
        memory_file = f'{WORKSPACE}/MEMORY.md'
        if os.path.exists(memory_file):
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否需要补充
            if len(content) < 1000:  # 内容太少
                self.alerts.append("⚠️ MEMORY.md内容较少，建议补充本周重要信息")

        # 清理超过30天的daily memory
        cutoff_date = self.now - timedelta(days=30)
        deleted_files = 0

        for memory_file in glob.glob(f'{MEMORY_DIR}/*.md'):
            # 提取文件名中的日期
            filename = os.path.basename(memory_file)
            date_str = filename.replace('.md', '')

            try:
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                if file_date < cutoff_date:
                    os.remove(memory_file)
                    deleted_files += 1
            except:
                pass

        if deleted_files > 0:
            self.alerts.append(f"🗑️ 清理了 {deleted_files} 个30天前的记忆文件")

        self.state['lastChecks']['weekly'] = self.now.isoformat()
        print(f"  ✅ 每周维护完成（清理 {deleted_files} 个文件）")

    def run(self):
        """Run heartbeat check"""
        print("=" * 60)
        print("💓 Heartbeat 心跳检查")
        print(f"时间: {self.now.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # 执行基础检查
        self.check_urgent_items()
        self.organize_memory()
        self.cleanup_logs()
        self.check_reminders()

        # 执行维护任务
        self.daily_maintenance()
        self.weekly_maintenance()

        # 保存状态
        self.save_state()

        # 输出报告
        print("\n" + "=" * 60)
        print("💓 Heartbeat 报告")
        print("=" * 60)

        if self.alerts:
            print("\n⚠️ 需要注意:")
            for alert in self.alerts:
                print(f"  {alert}")
        else:
            print("\n✅ 一切正常")

        print("\n" + "=" * 60)

        return self.alerts

def send_feishu_notification(alerts):
    """发送飞书通知"""
    if not alerts:
        return

    try:
        import subprocess
        import json

        # 构建消息
        message = "💓 Heartbeat 报告\n\n"
        message += "⚠️ 需要注意:\n"
        for alert in alerts:
            message += f"  {alert}\n"

        # 使用openclaw发送消息
        subprocess.run([
            'openclaw', 'message', 'send',
            '--to', 'ou_f17427a7518faa014659589d89db4d8b',
            '--message', message
        ], capture_output=True, timeout=30)

        print("📤 已发送飞书通知")
    except Exception as e:
        print(f"⚠️ 发送通知失败: {e}")

def main():
    """Main function"""
    engine = HeartbeatEngine()
    alerts = engine.run()
    
    # 发送飞书通知
    send_feishu_notification(alerts)
    
    # 如果有警报，返回非0状态码（用于通知）
    if alerts:
        print("\n🔔 有事项需要注意！")
        return 1
    else:
        print("\n💤 HEARTBEAT_OK")
        return 0

if __name__ == '__main__':
    exit(main())
