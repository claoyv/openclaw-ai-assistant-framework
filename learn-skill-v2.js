#!/usr/bin/env node
/**
 * 每小时技能学习脚本 - ClawHub版
 * 从 ClawHub (https://clawhub.ai) 网站爬取并学习新技能
 */

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

puppeteer.use(StealthPlugin());

// 配置
const CONFIG = {
  baseUrl: 'https://clawhub.ai',
  skillsPerRun: 5,  // 每次学习几个技能
  maxRetries: 3,
  timeout: 30000,
};

// 技能分类关键词
const CATEGORY_KEYWORDS = {
  video_image: ['video', 'image', 'frame', 'camera', 'photo', 'picture', 'visual', 'comfyui', 'generate', 'ai', 'animation', 'render', 'ffmpeg', 'prompt', 'editing', 'graphics', '3d', 'blender', 'stable-diffusion', 'midjourney'],
  content: ['summarize', 'content', 'write', 'blog', 'social', 'media', 'article', 'text', 'copy', 'tweet', 'chinese', 'writer', 'storytelling', 'marketing'],
  automation: ['github', 'coding', 'agent', 'script', 'automate', 'workflow', 'bot', 'cron', 'activecampaign', 'netsuite', 'googlephotos', 'integration'],
  data: ['analysis', 'log', 'usage', 'data', 'google', 'workspace', 'excel', 'sheet', 'csv', 'polars', 'eda', 'gh-issues', 'session-logs', 'database', 'sql'],
  dev: ['python', 'javascript', 'typescript', 'rust', 'go', 'docker', 'kubernetes', 'terraform', 'aws', 'testing', 'debug', 'lint']
};

// 获取已学习技能
function getLearnedSkills() {
  const logPath = path.join(process.env.HOME, '.openclaw/workspace/skills-learning-log.json');
  if (fs.existsSync(logPath)) {
    try {
      const logs = JSON.parse(fs.readFileSync(logPath, 'utf8'));
      const learned = new Set();
      logs.forEach(log => {
        const name = log.skillLearned?.name;
        if (name && name !== '搜索中' && name !== '搜索中...' && name !== '未找到新技能') {
          learned.add(name.toLowerCase());
          learned.add(name.toLowerCase().replace(/\.md$/, '').replace(/\s+/g, '-'));
        }
      });
      return learned;
    } catch (e) {
      console.error('读取学习记录失败:', e.message);
    }
  }
  return new Set();
}

// 分类技能
function categorizeSkill(name, desc = '') {
  const text = (name + ' ' + desc).toLowerCase();
  for (const [cat, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (keywords.some(kw => text.includes(kw))) return cat;
  }
  return 'other';
}

// 提取技能数据
async function extractSkillsFromPage(page) {
  return await page.evaluate(() => {
    const skills = [];
    
    // 方法1: 查找技能卡片
    const cards = document.querySelectorAll('[data-skill], .skill-card, [class*="skill"], article, .card');
    cards.forEach(card => {
      const link = card.querySelector('a[href*="/skills/"]') || card.closest('a[href*="/skills/"]');
      const nameEl = card.querySelector('h3, h2, .title, [class*="name"]') || card;
      const descEl = card.querySelector('p, .description, [class*="desc"]');
      const starsEl = card.querySelector('[class*="star"], [class*="rating"], [class*="count"]');
      
      if (link && nameEl) {
        skills.push({
          name: nameEl.innerText?.trim() || '',
          href: link.href || link.getAttribute('href') || '',
          description: descEl?.innerText?.trim() || '',
          stars: starsEl?.innerText?.trim() || ''
        });
      }
    });
    
    // 方法2: 查找所有技能链接
    if (skills.length === 0) {
      document.querySelectorAll('a[href*="/skills/"]').forEach(a => {
        const container = a.closest('article, .card, div[class*="skill"], li') || a.parentElement;
        const name = a.innerText?.trim() || a.querySelector('h3, h2, .title')?.innerText?.trim() || '';
        const desc = container?.querySelector('p, .description')?.innerText?.trim() || '';
        const stars = container?.querySelector('[class*="star"], [class*="rating"]')?.innerText?.trim() || '';
        
        if (name && name.length > 2) {
          skills.push({ name, href: a.href, description: desc, stars });
        }
      });
    }
    
    return skills;
  });
}

// 主函数
async function learnSkills() {
  const now = new Date();
  const hour = now.getHours();
  console.log(`\n[${now.toLocaleString('zh-CN')}] 📚 开始技能学习...`);
  
  let browser;
  const learnedSkills = getLearnedSkills();
  console.log(`  → 已学习技能: ${learnedSkills.size} 个`);
  
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // 尝试多个URL获取技能
    const urlsToTry = [
      `${CONFIG.baseUrl}/skills`,
      `${CONFIG.baseUrl}/zh`,
      CONFIG.baseUrl,
      `${CONFIG.baseUrl}/?page=1`,
      `${CONFIG.baseUrl}/skills?page=1`
    ];
    
    let allSkills = [];
    
    for (const url of urlsToTry) {
      if (allSkills.length >= 20) break;
      
      try {
        console.log(`  → 尝试访问: ${url}`);
        const response = await page.goto(url, { waitUntil: 'networkidle2', timeout: CONFIG.timeout });
        
        if (response.status() === 200) {
          await new Promise(r => setTimeout(r, 3000));
          
          // 滚动加载
          for (let i = 0; i < 5; i++) {
            await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
            await new Promise(r => setTimeout(r, 2000));
          }
          
          const skills = await extractSkillsFromPage(page);
          console.log(`    找到 ${skills.length} 个技能`);
          allSkills = allSkills.concat(skills);
        }
      } catch (e) {
        console.log(`    访问失败: ${e.message}`);
      }
    }
    
    // 去重
    const uniqueSkills = [];
    const seen = new Set();
    for (const s of allSkills) {
      if (!seen.has(s.name)) {
        seen.add(s.name);
        uniqueSkills.push(s);
      }
    }
    
    console.log(`  → 去重后共 ${uniqueSkills.length} 个技能`);
    
    // 过滤已学习的
    const newSkills = uniqueSkills.filter(s => {
      const key = s.name.toLowerCase().replace(/\.md$/, '').replace(/\s+/g, '-');
      return !learnedSkills.has(s.name.toLowerCase()) && !learnedSkills.has(key);
    });
    
    console.log(`  → 未学习的新技能: ${newSkills.length} 个`);
    
    // 按热度排序
    newSkills.sort((a, b) => {
      const getStars = s => {
        const m = s.stars?.match(/([\d.]+)k?/i);
        return m ? parseFloat(m[1]) * (s.stars.includes('k') ? 1000 : 1) : 0;
      };
      return getStars(b) - getStars(a);
    });
    
    // 选择要学习的技能
    const skillsToLearn = newSkills.slice(0, CONFIG.skillsPerRun);
    
    if (skillsToLearn.length === 0) {
      console.log('  ⚠️ 没有新技能可学习');
      return;
    }
    
    // 学习每个技能
    for (const skill of skillsToLearn) {
      console.log(`\n  📖 学习: ${skill.name}`);
      
      try {
        // 访问详情页
        await page.goto(skill.href, { waitUntil: 'networkidle2', timeout: CONFIG.timeout });
        await new Promise(r => setTimeout(r, 3000));
        
        // 获取详情
        const details = await page.evaluate(() => {
          const title = document.querySelector('h1')?.innerText?.trim() || '';
          let content = '';
          
          // 尝试多个选择器
          const selectors = ['article', '.prose', '[class*="content"]', 'main', '.description'];
          for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el && el.innerText.length > content.length) {
              content = el.innerText;
            }
          }
          
          return { title, content: content.substring(0, 2000) };
        });
        
        // 记录学习
        const category = categorizeSkill(skill.name, details.content);
        const logEntry = {
          timestamp: new Date().toISOString(),
          hour,
          category,
          skillLearned: {
            name: skill.name,
            stars: skill.stars,
            link: skill.href,
            description: details.content.substring(0, 500)
          }
        };
        
        // 保存到日志
        const logPath = path.join(process.env.HOME, '.openclaw/workspace/skills-learning-log.json');
        let logs = fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, 'utf8')) : [];
        logs.push(logEntry);
        fs.writeFileSync(logPath, JSON.stringify(logs, null, 2));
        
        console.log(`    ✅ 已记录: ${skill.name} (${category})`);
        
      } catch (e) {
        console.log(`    ❌ 学习失败: ${e.message}`);
      }
    }
    
  } catch (error) {
    console.error('执行错误:', error.message);
  } finally {
    if (browser) await browser.close();
  }
  
  console.log(`\n[${new Date().toLocaleString('zh-CN')}] ✅ 学习完成\n`);
}

// 运行
learnSkills().catch(console.error);
