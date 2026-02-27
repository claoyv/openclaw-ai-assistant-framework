#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能自动安装脚本 v3.0 - 无限学习版
每小时从ClawHub安装一个新技能，永不停止
"""

import json
import os
import subprocess
from datetime import datetime
import requests
import time

LOG_FILE = '/home/zzyuzhangxing/.openclaw/workspace/logs/skill-install.log'
STATUS_FILE = '/home/zzyuzhangxing/.openclaw/workspace/.skill-install-status-v3.json'
SKILLS_DIR = '/home/zzyuzhangxing/.openclaw/workspace/skills'
CLAWHUB_API = 'https://clawhub.ai/api/skills'

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def get_status():
    """获取安装状态"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 尝试从v2版本迁移
    v2_status_file = '/home/zzyuzhangxing/.openclaw/workspace/.skill-install-status-v2.json'
    if os.path.exists(v2_status_file):
        with open(v2_status_file, 'r', encoding='utf-8') as f:
            v2_status = json.load(f)
        
        # 提取已安装的技能名
        installed = []
        for skill_info in v2_status.get('installed', []):
            if isinstance(skill_info, dict):
                installed.append(skill_info.get('name'))
        
        log(f"📦 从v2迁移: {len(installed)} 个已安装技能")
        
        return {
            'installed_skills': installed,
            'total_installed': len(installed),
            'last_install_time': datetime.now().isoformat(),
            'current_page': 1,
            'failed_attempts': 0
        }
    
    return {
        'installed_skills': [],
        'total_installed': 0,
        'last_install_time': None,
        'current_page': 1,
        'failed_attempts': 0
    }

def save_status(status):
    """保存安装状态"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

def fetch_clawhub_skills(page=1, sort='downloads'):
    """从ClawHub获取技能列表"""
    try:
        # ClawHub API (模拟，实际需要真实API)
        url = f"https://clawhub.ai/skills?page={page}&sort={sort}"
        
        # 使用 clawhub CLI 搜索
        result = subprocess.run(
            ['clawhub', 'search', '--json', '--page', str(page)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return data.get('skills', [])
            except:
                return []
        else:
            # 如果CLI失败，使用默认技能列表
            return get_default_skills()
    
    except Exception as e:
        log(f"⚠️ 获取ClawHub技能失败: {e}")
        return get_default_skills()

def get_default_skills():
    """默认技能列表（ClawHub热门技能）"""
    return [
        'tavily-search', 'skill-creator', 'proactive-agent', 
        'automation-workflows', 'notion', 'obsidian', 
        'brave-search', 'agent-browser', 'find-skills',
        'self-improving-agent', 'skill-vetter', 'planning-with-files',
        'bird-twitter', 'x-twitter', 'gmail', 'calendar',
        'spotify', 'home-assistant', 'github', 'remotion',
        'mcp-skill', 'python', 'python-patterns', 'python-testing',
        'pdf', 'xlsx', 'writer', 'chinese-writing', 'summarize',
        'docker', 'k8s', 'terraform', 'video-frames', 'image',
        'polars', 'eda', 'model-usage', 'activecampaign', 'netsuite',
        'camsnap', 'nano-banana-pro', 'video-prompt-engineering',
        'memory', 'file', 'pandoc', 'docx', 'tweet-writer'
    ]

def install_skill(skill_name):
    """安装技能"""
    log(f"📦 正在安装: {skill_name}")
    
    try:
        # 使用 clawhub CLI 安装
        result = subprocess.run(
            ['clawhub', 'install', skill_name],
            capture_output=True,
            text=True,
            timeout=60,
            cwd='/home/zzyuzhangxing/.openclaw/workspace'
        )
        
        if result.returncode == 0:
            log(f"✅ 安装成功: {skill_name}")
            return True, "安装成功"
        else:
            error_msg = result.stderr[:100] if result.stderr else "未知错误"
            log(f"❌ 安装失败: {skill_name} - {error_msg}")
            return False, error_msg
    
    except subprocess.TimeoutExpired:
        log(f"⏱️ 安装超时: {skill_name}")
        return False, "安装超时"
    except Exception as e:
        log(f"❌ 安装异常: {skill_name} - {e}")
        return False, str(e)

def verify_installation(skill_name):
    """验证技能安装"""
    skill_path = os.path.join(SKILLS_DIR, skill_name)
    skill_md = os.path.join(skill_path, 'SKILL.md')
    
    if os.path.exists(skill_path) and os.path.exists(skill_md):
        return True
    return False

def get_next_skill(status):
    """获取下一个要安装的技能"""
    # 获取ClawHub技能列表
    skills = fetch_clawhub_skills(page=status.get('current_page', 1))
    
    # 过滤已安装的
    installed = set(status.get('installed_skills', []))
    
    for skill in skills:
        skill_name = skill if isinstance(skill, str) else skill.get('name')
        if skill_name not in installed:
            return skill_name
    
    # 如果当前页都安装完了，翻到下一页
    status['current_page'] = status.get('current_page', 1) + 1
    save_status(status)
    
    # 递归获取下一页的技能
    return get_next_skill(status)

def main():
    log("=" * 60)
    log("🚀 技能自动安装 v3.0 - 无限学习版")
    log("=" * 60)
    
    # 加载状态
    status = get_status()
    
    # 获取下一个技能
    next_skill = get_next_skill(status)
    
    if not next_skill:
        log("⚠️ 未找到新技能")
        return
    
    log(f"📌 下一个技能: {next_skill}")
    
    # 安装技能
    success, message = install_skill(next_skill)
    
    if success:
        # 验证安装
        if verify_installation(next_skill):
            status['installed_skills'].append(next_skill)
            status['total_installed'] += 1
            status['last_install_time'] = datetime.now().isoformat()
            status['failed_attempts'] = 0
            log(f"✅ 验证通过: {next_skill}")
        else:
            log(f"⚠️ 验证失败: {next_skill} (文件不存在)")
            status['failed_attempts'] += 1
    else:
        status['failed_attempts'] += 1
    
    # 保存状态
    save_status(status)
    
    # 输出统计
    log("=" * 60)
    log(f"📊 统计:")
    log(f"  已安装: {status['total_installed']} 个")
    log(f"  失败次数: {status['failed_attempts']}")
    log(f"  最后安装: {status['last_install_time']}")
    log("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"❌ 脚本异常: {e}")
        import traceback
        traceback.print_exc()
