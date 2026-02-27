#!/usr/bin/env python3
"""
L2层网页抓取工具 - Playwright有头浏览器
用途: 处理需要JavaScript渲染的动态页面
能力层级: L2 (有头浏览器)
"""

import sys
import json
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def fetch_with_browser(url, wait_for=None, timeout=30000, headless=True):
    """
    使用Playwright抓取网页内容
    
    参数:
        url: 目标URL
        wait_for: 等待选择器 (如 "#content" 或等待网络空闲 "networkidle")
        timeout: 超时时间(毫秒)
        headless: 是否无头模式
    
    返回:
        dict: {success, title, content, url, error}
    """
    result = {
        'success': False,
        'title': '',
        'content': '',
        'url': url,
        'error': None
    }
    
    try:
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            # 设置超时
            page.set_default_timeout(timeout)
            
            # 导航到页面
            print(f"🌐 正在访问: {url}", file=sys.stderr)
            response = page.goto(url, wait_until='domcontentloaded')
            
            if not response:
                result['error'] = '页面加载失败'
                browser.close()
                return result
            
            # 等待指定元素或网络空闲
            if wait_for:
                try:
                    if wait_for == 'networkidle':
                        page.wait_for_load_state('networkidle', timeout=timeout)
                    else:
                        page.wait_for_selector(wait_for, timeout=timeout)
                    print(f"✅ 等待条件满足: {wait_for}", file=sys.stderr)
                except PlaywrightTimeout:
                    print(f"⚠️ 等待超时，继续处理: {wait_for}", file=sys.stderr)
            
            # 获取页面信息
            result['title'] = page.title()
            result['content'] = page.content()
            result['success'] = True
            
            print(f"✅ 抓取成功: {result['title'][:50]}...", file=sys.stderr)
            
            browser.close()
            
    except Exception as e:
        result['error'] = str(e)
        print(f"❌ 抓取失败: {e}", file=sys.stderr)
    
    return result

def main():
    parser = argparse.ArgumentParser(description='L2层网页抓取工具 (Playwright)')
    parser.add_argument('url', help='目标URL')
    parser.add_argument('--wait-for', '-w', help='等待选择器或networkidle')
    parser.add_argument('--timeout', '-t', type=int, default=30000, help='超时时间(毫秒)')
    parser.add_argument('--visible', '-v', action='store_true', help='显示浏览器窗口(非无头模式)')
    parser.add_argument('--json', '-j', action='store_true', help='输出JSON格式')
    parser.add_argument('--text-only', action='store_true', help='只输出文本内容')
    
    args = parser.parse_args()
    
    # 执行抓取
    result = fetch_with_browser(
        url=args.url,
        wait_for=args.wait_for,
        timeout=args.timeout,
        headless=not args.visible
    )
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    elif args.text_only:
        if result['success']:
            # 简单提取文本
            import re
            text = re.sub(r'<[^>]+>', ' ', result['content'])
            text = re.sub(r'\s+', ' ', text).strip()
            print(text[:5000])  # 限制长度
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    else:
        # 标准输出
        if result['success']:
            print(f"标题: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"内容长度: {len(result['content'])} 字符")
            print("-" * 50)
            print(result['content'][:3000])  # 限制预览长度
        else:
            print(f"抓取失败: {result['error']}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
