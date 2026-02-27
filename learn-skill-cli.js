#!/usr/bin/env node
/**
 * 每小时技能学习脚本 - ClawHub CLI版
 * 使用 clawhub CLI 安装新技能
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const LOG_FILE = path.join(WORKSPACE, 'learn-cron.log');
const STATUS_FILE = path.join(WORKSPACE, '.skill-install-status-v2.json');

function log(msg) {
  const timestamp = new Date().toLocaleString('zh-CN');
  const logMsg = `[${timestamp}] ${msg}`;
  console.log(logMsg);
  fs.appendFileSync(LOG_FILE, logMsg + '\n');
}

function getInstalledSkills() {
  const skillsDir = path.join(WORKSPACE, 'skills');
  if (!fs.existsSync(skillsDir)) return new Set();
  
  const skills = fs.readdirSync(skillsDir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
  
  return new Set(skills);
}

function getStatus() {
  if (fs.existsSync(STATUS_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(STATUS_FILE, 'utf8'));
    } catch (e) {
      return { installed: [], current_index: 0 };
    }
  }
  return { installed: [], current_index: 0 };
}

function saveStatus(status) {
  fs.writeFileSync(STATUS_FILE, JSON.stringify(status, null, 2));
}

function searchClawhubSkills() {
  try {
    // 尝试搜索热门技能
    const result = execSync('clawhub search --json 2>/dev/null || echo "[]"', {
      cwd: WORKSPACE,
      encoding: 'utf8',
      timeout: 30000
    });
    
    try {
      return JSON.parse(result);
    } catch {
      return [];
    }
  } catch (e) {
    log(`⚠️ 搜索失败: ${e.message}`);
    return [];
  }
}

function installSkill(skillName, retryCount = 0) {
  try {
    log(`📦 安装: ${skillName}`);
    
    const result = execSync(`clawhub install ${skillName} 2>&1`, {
      cwd: WORKSPACE,
      encoding: 'utf8',
      timeout: 60000
    });
    
    log(`✅ 安装成功: ${skillName}`);
    return { success: true, output: result };
  } catch (e) {
    const errorMsg = e.message || '';
    
    // Rate limit - 重试
    if (errorMsg.includes('Rate limit') && retryCount < 3) {
      log(`⏳ Rate limit，等待30秒后重试... (${retryCount + 1}/3)`);
      execSync('sleep 30');
      return installSkill(skillName, retryCount + 1);
    }
    
    // 已安装
    if (errorMsg.includes('already installed') || errorMsg.includes('已存在')) {
      log(`⚠️ 已安装: ${skillName}`);
      return { success: true, alreadyInstalled: true };
    }
    
    // 技能不存在
    if (errorMsg.includes('not found') || errorMsg.includes('Skill not found')) {
      log(`⚠️ 技能不存在: ${skillName}`);
      return { success: false, notFound: true };
    }
    
    // 安全标记
    if (errorMsg.includes('VirusTotal') || errorMsg.includes('suspicious')) {
      log(`⚠️ 安全标记跳过: ${skillName}`);
      return { success: false, securityFlag: true };
    }
    
    log(`❌ 安装失败: ${skillName} - ${errorMsg.substring(0, 100)}`);
    return { success: false, error: errorMsg };
  }
}

// 推荐技能列表（从ClawHub实际存在的技能）
const RECOMMENDED_SKILLS = [
  'agent-browser', 'automation-workflows', 'bird-twitter',
  'brave-search', 'calendar', 'find-skills',
  'github', 'gmail', 'gog', 'home-assistant',
  'image', 'mcp-skill', 'notion', 'obsidian',
  'planning-with-files', 'proactive-agent', 'remotion',
  'self-improving-agent', 'skill-creator', 'skill-vetter',
  'spotify', 'tavily-search', 'twitter-post',
  'video-prompt-engineering', 'x-twitter',
  // 开发相关
  'docker', 'k8s', 'terraform', 'aws',
  // 数据处理
  'polars', 'eda', 'model-usage',
  // 内容创作
  'tweet-writer', 'chinese-writing', 'summarize'
];

async function main() {
  log('');
  log('============================================================');
  log('🚀 技能学习 - ClawHub CLI版');
  log('============================================================');
  
  const installed = getInstalledSkills();
  const status = getStatus();
  
  log(`📊 当前已安装: ${installed.size} 个技能`);
  
  // 找出未安装的技能
  const toInstall = RECOMMENDED_SKILLS.filter(s => !installed.has(s));
  
  if (toInstall.length === 0) {
    log('✅ 所有推荐技能已安装完毕！');
    log('🎉 技能库已满，停止学习。');
    return;
  }
  
  log(`📚 待安装技能: ${toInstall.length} 个`);
  
  // 安装前5个
  const batch = toInstall.slice(0, 5);
  let successCount = 0;
  
  for (const skill of batch) {
    const result = installSkill(skill);
    if (result.success) {
      successCount++;
      status.installed.push({
        name: skill,
        time: new Date().toISOString(),
        note: result.alreadyInstalled ? '已存在' : '新安装'
      });
    }
    
    // 间隔5秒，避免rate limit
    await new Promise(r => setTimeout(r, 5000));
  }
  
  status.current_index += batch.length;
  saveStatus(status);
  
  log('');
  log('============================================================');
  log(`✅ 完成! 成功安装: ${successCount}/${batch.length}`);
  log(`📊 总计: ${installed.size + successCount} 个技能`);
  log('============================================================');
}

main().catch(e => {
  log(`❌ 错误: ${e.message}`);
  process.exit(1);
});
