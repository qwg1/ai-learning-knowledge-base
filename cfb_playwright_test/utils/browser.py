#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - Playwright浏览器管理
功能: 浏览器启动、关闭、上下文管理
"""

import os
import sys
from typing import Optional, Dict
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.sync_api import Playwright, Browser, BrowserContext, Page
from playwright.sync_api import sync_playwright


class BrowserManager:
    """Playwright浏览器管理器"""
    
    def __init__(self, config: dict):
        """
        初始化浏览器管理器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.pages: Dict[str, Page] = {}
    
    def start(self) -> BrowserContext:
        """
        启动浏览器
        
        Returns:
            BrowserContext: 浏览器上下文
        """
        print("🚀 启动浏览器...")
        
        # 启动Playwright
        self.playwright = sync_playwright().start()
        
        # 选择浏览器
        browser_config = self.config.get("browser", {})
        browser_type = browser_config.get("type", "chromium")
        
        if browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(
                headless=browser_config.get("headless", False)
            )
        elif browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(
                headless=browser_config.get("headless", False)
            )
        elif browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(
                headless=browser_config.get("headless", False)
            )
        else:
            # 默认使用chromium
            self.browser = self.playwright.chromium.launch(
                headless=browser_config.get("headless", False)
            )
        
        # 创建浏览器上下文
        viewport = browser_config.get("viewport", {"width": 1920, "height": 1080})
        
        self.context = self.browser.new_context(
            viewport=viewport,
            locale=browser_config.get("locale", "zh-CN"),
            timezone_id=browser_config.get("timezone_id", "Asia/Shanghai"),
            # 保存认证状态
            storage_state=self._get_storage_state(),
            # User-Agent
            user_agent=browser_config.get("user_agent")
        )
        
        # 监听控制台消息
        self.context.on("console", lambda msg: self._handle_console(msg))
        
        # 监听页面错误
        self.context.on("pageerror", lambda error: self._handle_error(error))
        
        print("✅ 浏览器启动成功")
        return self.context
    
    def open_page(self, name: str, url: str) -> Page:
        """
        打开新页面
        
        Args:
            name: 页面名称
            url: URL地址
            
        Returns:
            Page: Playwright页面对象
        """
        if not self.context:
            raise Exception("浏览器未启动，请先调用 start()")
        
        # 关闭已存在的同名页面
        if name in self.pages:
            self.pages[name].close()
        
        # 打开新页面
        page = self.context.new_page()
        
        # 设置超时
        timeout = self.config.get("browser", {}).get("timeout", 30000)
        page.set_default_timeout(timeout)
        
        # 监听弹窗
        page.on("dialog", lambda dialog: self._handle_dialog(dialog))
        
        self.pages[name] = page
        print(f"📄 页面已打开: {name} - {url}")
        
        return page
    
    def get_page(self, name: str) -> Optional[Page]:
        """
        获取已打开的页面
        
        Args:
            name: 页面名称
            
        Returns:
            Page: 页面对象，如果不存在返回None
        """
        return self.pages.get(name)
    
    def close_page(self, name: str):
        """
        关闭页面
        
        Args:
            name: 页面名称
        """
        if name in self.pages:
            self.pages[name].close()
            del self.pages[name]
            print(f"📄 页面已关闭: {name}")
    
    def save_storage_state(self):
        """
        保存浏览器状态到文件
        """
        if self.context:
            storage_file = self._get_storage_state()
            os.makedirs(os.path.dirname(storage_file), exist_ok=True)
            self.context.storage_state(path=storage_file)
            print(f"💾 浏览器状态已保存: {storage_file}")
    
    def close(self):
        """
        关闭浏览器
        """
        # 保存状态
        self.save_storage_state()
        
        # 关闭所有页面
        for name, page in self.pages.items():
            try:
                page.close()
            except Exception:
                pass
        
        self.pages.clear()
        
        # 关闭浏览器
        if self.browser:
            self.browser.close()
            print("🔴 浏览器已关闭")
        
        # 停止Playwright
        if self.playwright:
            self.playwright.stop()
            print("🔴 Playwright已停止")
    
    def _get_storage_state(self) -> str:
        """
        获取存储状态文件路径
        """
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "storage_state.json"
        )
    
    def _handle_console(self, msg):
        """
        处理控制台消息
        """
        msg_type = msg.type
        if msg_type == "error":
            print(f"❌ 控制台错误: {msg.text}")
        elif msg_type == "warning":
            print(f"⚠️ 控制台警告: {msg.text}")
    
    def _handle_error(self, error):
        """
        处理页面错误
        """
        print(f"❌ 页面错误: {error}")
    
    def _handle_dialog(self, dialog):
        """
        处理弹窗
        """
        print(f"📦 弹窗: {dialog.message}")
        # 默认接受弹窗
        dialog.accept()


class PageHelper:
    """页面操作辅助工具"""
    
    def __init__(self, page: Page, config: dict):
        """
        初始化页面辅助工具
        
        Args:
            page: Playwright页面对象
            config: 配置字典
        """
        self.page = page
        self.config = config
    
    def wait_for_load(self):
        """等待页面完全加载"""
        wait_config = self.config.get("wait", {})
        self.page.wait_for_load_state(
            state=wait_config.get("load", "networkidle")
        )
    
    def wait_for_selector(self, locator: str, timeout: int = None):
        """
        等待元素出现
        
        Args:
            locator: 元素定位器
            timeout: 超时时间(ms)
        """
        timeout = timeout or self.config.get("browser", {}).get("timeout", 30000)
        self.page.wait_for_selector(locator, timeout=timeout)
    
    def click(self, locator: str, timeout: int = None):
        """
        点击元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间(ms)
        """
        timeout = timeout or self.config.get("wait", {}).get("click", 1000)
        self.wait_for_selector(locator, timeout)
        self.page.click(locator, timeout=timeout)
        self.page.wait_for_timeout(timeout)
    
    def fill(self, locator: str, value: str, timeout: int = None):
        """
        输入文本
        
        Args:
            locator: 元素定位器
            value: 输入的值
            timeout: 超时时间(ms)
        """
        timeout = timeout or self.config.get("wait", {}).get("input", 500)
        self.wait_for_selector(locator, timeout)
        self.page.fill(locator, value)
        self.page.wait_for_timeout(timeout)
    
    def select_option(self, locator: str, value: str, timeout: int = None):
        """
        选择下拉选项
        
        Args:
            locator: 元素定位器
            value: 选项值
            timeout: 超时时间(ms)
        """
        timeout = timeout or self.config.get("wait", {}).get("click", 1000)
        self.wait_for_selector(locator, timeout)
        self.page.select_option(locator, value)
        self.page.wait_for_timeout(timeout)
    
    def get_text(self, locator: str) -> str:
        """
        获取元素文本
        
        Args:
            locator: 元素定位器
            
        Returns:
            str: 元素文本
        """
        self.wait_for_selector(locator)
        return self.page.text_content(locator)
    
    def get_attribute(self, locator: str, attribute: str) -> str:
        """
        获取元素属性
        
        Args:
            locator: 元素定位器
            attribute: 属性名
            
        Returns:
            str: 属性值
        """
        self.wait_for_selector(locator)
        return self.page.get_attribute(locator, attribute)
    
    def is_visible(self, locator: str) -> bool:
        """
        检查元素是否可见
        
        Args:
            locator: 元素定位器
            
        Returns:
            bool: 是否可见
        """
        return self.page.is_visible(locator)
    
    def screenshot(self, path: str, full_page: bool = False):
        """
        截图
        
        Args:
            path: 保存路径
            full_page: 是否全页截图
        """
        self.page.screenshot(path=path, full_page=full_page)
        print(f"📸 截图已保存: {path}")


# ============== 便捷函数 ==============
def create_browser_manager(config_file: str = "./config/config.js") -> BrowserManager:
    """
    创建浏览器管理器（便捷函数）
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        BrowserManager: 浏览器管理器实例
    """
    import json
    
    config_path = os.path.join(os.path.dirname(config_file), "config.js")
    
    try:
        # 尝试读取JS配置文件
        import re
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取JSON部分
        match = re.search(r'const CONFIG = ({.*?});', content, re.DOTALL)
        if match:
            config_str = match.group(1)
            # 转换为Python格式
            config_str = config_str.replace('true', 'True')
            config_str = config_str.replace('false', 'False')
            config_str = config_str.replace('null', 'None')
            config = eval(f"{{{config_str}}}")
        else:
            raise Exception("无法解析配置文件")
            
    except Exception as e:
        print(f"⚠️ 配置加载失败: {e}")
        print("使用默认配置...")
        config = {
            "browser": {
                "type": "chromium",
                "headless": False,
                "timeout": 30000,
                "viewport": {"width": 1920, "height": 1080}
            },
            "wait": {
                "load": "networkidle",
                "click": 1000,
                "input": 500
            }
        }
    
    return BrowserManager(config)


if __name__ == "__main__":
    # 测试浏览器管理器
    print("=" * 60)
    print("CFB支付系统 - Playwright浏览器管理测试")
    print("=" * 60)
    
    browser = create_browser_manager()
    
    try:
        # 启动浏览器
        browser.start()
        
        # 打开测试页面
        page = browser.open_page("test", "https://test-admin.cfbaopay.com")
        
        # 等待加载
        page.wait_for_load_state("networkidle")
        
        print("✅ 浏览器测试成功")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        
    finally:
        # 关闭浏览器
        browser.close()
