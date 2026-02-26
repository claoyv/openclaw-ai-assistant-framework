#!/usr/bin/env python3
"""
B站UP主视频分析爬虫 - 增强版
支持：关闭登录弹窗、滚动加载、动态内容获取
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json
import re
from datetime import datetime
import time


def analyze_up(uid_or_url, cookie_file=None):
    """分析B站UP主
    
    Args:
        uid_or_url: UID或B站空间链接
        cookie_file: Cookie文件路径（可选）
    """
    
    # 提取UID
    if 'bilibili.com' in uid_or_url:
        uid = re.search(r'space\.bilibili\.com/(\d+)', uid_or_url)
        uid = uid.group(1) if uid else uid_or_url
    else:
        uid = uid_or_url
    
    print(f"🎯 正在分析UP主: {uid}")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # 创建上下文（模拟真实用户）
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 如果有Cookie文件，加载Cookie
        if cookie_file and os.path.exists(cookie_file):
            print(f"🍪 正在加载Cookie: {cookie_file}")
            try:
                with open(cookie_file, 'r') as f:
                    cookie_str = f.read().strip()
                
                # 解析Cookie字符串
                cookies = []
                for item in cookie_str.split(';'):
                    if '=' in item:
                        name, value = item.strip().split('=', 1)
                        cookies.append({
                            'name': name,
                            'value': value,
                            'domain': '.bilibili.com',
                            'path': '/'
                        })
                
                # 添加Cookie到上下文
                context.add_cookies(cookies)
                print(f"  ✓ 已加载 {len(cookies)} 个Cookie")
            except Exception as e:
                print(f"  ⚠️ Cookie加载失败: {e}")
        
        page = context.new_page()
        
        try:
            # 访问UP主空间
            url = f"https://space.bilibili.com/{uid}"
            print(f"📍 访问: {url}")
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # 等待初始加载
            page.wait_for_timeout(3000)
            
            # ===== 关闭登录弹窗 =====
            print("🔧 尝试关闭登录弹窗...")
            try:
                # 方法1: 点击关闭按钮
                close_selectors = [
                    '.login-tip-close',
                    '.close-btn',
                    '.van-icon-close',
                    '[class*="close"]',
                    '.btn-close'
                ]
                for selector in close_selectors:
                    try:
                        close_btn = page.query_selector(selector)
                        if close_btn and close_btn.is_visible():
                            close_btn.click()
                            print(f"  ✓ 点击关闭按钮: {selector}")
                            page.wait_for_timeout(1000)
                            break
                    except:
                        continue
                
                # 方法2: 按ESC键关闭
                page.keyboard.press('Escape')
                page.wait_for_timeout(500)
                
                # 方法3: 点击空白处关闭
                page.mouse.click(100, 100)
                page.wait_for_timeout(500)
                
            except Exception as e:
                print(f"  ℹ️ 关闭弹窗过程: {e}")
            
            # ===== 获取基础信息 =====
            up_info = {
                "uid": uid,
                "analysis_time": datetime.now().isoformat(),
                "profile_url": url
            }
            
            # 提取昵称
            try:
                # 多种选择器尝试
                name_selectors = [
                    '.nickname-text',
                    '.h-name',
                    '[class*="nickname"]',
                    'h1.username'
                ]
                for selector in name_selectors:
                    elem = page.query_selector(selector)
                    if elem:
                        up_info['nickname'] = elem.inner_text().strip()
                        print(f"👤 昵称: {up_info['nickname']}")
                        break
            except Exception as e:
                print(f"  ℹ️ 获取昵称失败: {e}")
            
            # 提取粉丝数
            try:
                fans_selectors = [
                    '.followed-num',
                    '.fans-num',
                    '[class*="followed"]',
                    '.h-followed'
                ]
                for selector in fans_selectors:
                    elem = page.query_selector(selector)
                    if elem:
                        up_info['fans'] = elem.inner_text().strip()
                        print(f"👥 粉丝: {up_info['fans']}")
                        break
            except Exception as e:
                print(f"  ℹ️ 获取粉丝数失败: {e}")
            
            # 提取签名
            try:
                sign_selectors = [
                    '.description',
                    '.h-description',
                    '[class*="description"]',
                    '.sign-text'
                ]
                for selector in sign_selectors:
                    elem = page.query_selector(selector)
                    if elem:
                        up_info['signature'] = elem.inner_text().strip()
                        print(f"📝 签名: {up_info['signature'][:60]}...")
                        break
            except Exception as e:
                print(f"  ℹ️ 获取签名失败: {e}")
            
            # ===== 滚动加载视频列表 =====
            print("\n📹 开始滚动加载视频列表...")
            
            videos = []
            scroll_count = 0
            max_scrolls = 10  # 最多滚动10次
            last_video_count = 0
            no_change_count = 0
            
            while scroll_count < max_scrolls and no_change_count < 3:
                # 滚动页面
                page.evaluate("window.scrollBy(0, 800)")
                scroll_count += 1
                print(f"  滚动 {scroll_count}/{max_scrolls}...")
                
                # 等待内容加载
                page.wait_for_timeout(2000)
                
                # 检查是否有新视频
                current_videos = page.query_selector_all('.video-list-item, .small-item, [class*="video-list"] > div')
                if len(current_videos) > last_video_count:
                    print(f"    发现 {len(current_videos)} 个视频")
                    last_video_count = len(current_videos)
                    no_change_count = 0
                else:
                    no_change_count += 1
                
                # 如果已经获取足够多，提前结束
                if len(current_videos) >= 20:
                    print(f"    已获取足够视频，停止滚动")
                    break
            
            # ===== 提取视频信息 =====
            print(f"\n🎬 正在提取 {last_video_count} 个视频信息...")
            
            video_items = page.query_selector_all('.video-list-item, .small-item, [class*="video-list"] > div')
            
            for i, item in enumerate(video_items[:20], 1):  # 最多20个
                try:
                    video = {"index": i}
                    
                    # 标题
                    title_selectors = ['.title', '.name', 'a[title]', 'h3', '.video-title']
                    for sel in title_selectors:
                        title_elem = item.query_selector(sel)
                        if title_elem:
                            video['title'] = title_elem.get_attribute('title') or title_elem.inner_text().strip()
                            if video['title']:
                                break
                    
                    # 播放量
                    play_selectors = ['.play-text', '.play', '.view', '[class*="play"]']
                    for sel in play_selectors:
                        play_elem = item.query_selector(sel)
                        if play_elem:
                            video['play_count'] = play_elem.inner_text().strip()
                            break
                    
                    # 弹幕数
                    danmu_selectors = ['.danmu-text', '.danmu', '[class*="danmu"]']
                    for sel in danmu_selectors:
                        danmu_elem = item.query_selector(sel)
                        if danmu_elem:
                            video['danmu_count'] = danmu_elem.inner_text().strip()
                            break
                    
                    # 发布时间
                    time_selectors = ['.time', '.date', '[class*="time"]', '.pubdate']
                    for sel in time_selectors:
                        time_elem = item.query_selector(sel)
                        if time_elem:
                            video['pub_time'] = time_elem.inner_text().strip()
                            break
                    
                    # 视频链接
                    link_elem = item.query_selector('a[href*="BV"]')
                    if link_elem:
                        href = link_elem.get_attribute('href')
                        if href:
                            video['link'] = href if href.startswith('http') else f"https:{href}"
                    
                    # 只保留有标题的视频
                    if video.get('title'):
                        videos.append(video)
                        print(f"  {i}. {video['title'][:45]}...")
                        if video.get('play_count'):
                            print(f"     ▶️ {video['play_count']}  |  🕐 {video.get('pub_time', 'N/A')}")
                
                except Exception as e:
                    continue
            
            up_info['videos'] = videos
            up_info['video_count'] = len(videos)
            
            # ===== 截图保存 =====
            print("\n📸 正在保存截图...")
            screenshot_path = f"/home/zzyuzhangxing/.openclaw/workspace/qiuzhi_profile_{uid}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"  ✓ 截图已保存: {screenshot_path}")
            
            # ===== 保存JSON报告 =====
            report_path = f"/home/zzyuzhangxing/.openclaw/workspace/qiuzhi_analysis_{uid}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(up_info, f, ensure_ascii=False, indent=2)
            print(f"  ✓ 分析报告已保存: {report_path}")
            
            browser.close()
            return up_info
            
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            # 错误时也尝试截图
            try:
                error_screenshot = f"/home/zzyuzhangxing/.openclaw/workspace/error_{uid}.png"
                page.screenshot(path=error_screenshot)
                print(f"  错误截图已保存: {error_screenshot}")
            except:
                pass
            browser.close()
            return None


def main():
    """主函数"""
    import sys
    
    # 如果没有参数，使用示例
    if len(sys.argv) < 2:
        print("=" * 60)
        print("B站UP主视频分析爬虫 - 增强版")
        print("=" * 60)
        print("\n使用方法:")
        print("  python3 crawl-bilibili.py <UID或链接> [cookie文件]")
        print("\n示例:")
        print("  python3 crawl-bilibili.py 385670211")
        print("  python3 crawl-bilibili.py https://space.bilibili.com/385670211")
        print("  python3 crawl-bilibili.py 385670211 ~/.bilibili_cookie")
        print("\n功能:")
        print("  ✓ 自动关闭登录弹窗")
        print("  ✓ 支持Cookie登录（可选）")
        print("  ✓ 滚动加载视频列表")
        print("  ✓ 提取视频标题/播放量/时间")
        print("  ✓ 保存截图和JSON报告")
        print("\nCookie获取方法:")
        print("  1. 登录B站网页版")
        print("  2. F12 → Application → Cookies")
        print("  3. 复制 SESSDATA 的值")
        print("  4. 保存到文件: SESSDATA=xxx; bili_jct=yyy")
        return
    
    uid = sys.argv[1]
    cookie_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = analyze_up(uid, cookie_file)
    
    print("\n" + "=" * 60)
    if result:
        print("✅ 分析完成!")
        print(f"👤 UP主: {result.get('nickname', 'Unknown')}")
        print(f"👥 粉丝: {result.get('fans', 'N/A')}")
        print(f"🎬 视频: {result.get('video_count', 0)} 个")
    else:
        print("❌ 分析失败，请检查网络或UID")
    print("=" * 60)


if __name__ == "__main__":
    main()
