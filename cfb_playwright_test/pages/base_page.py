#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 页面基类
所有页面的父类，封装通用操作
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List
from playwright.sync_api import Page

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.locator import LocatorFactory, BaseLocators


class BasePage:
    """页面基类"""
    
    def __init__(self, page: Page, config: dict):
        """
        初始化页面
        
        Args:
            page: Playwright页面对象
            config: 配置字典
        """
        self.page = page
        self.config = config
        self.wait_config = config.get("wait", {})
    
    # ============== 页面导航 ==============
    
    def navigate(self, url: str):
        """
        导航到URL
        
        Args:
            url: 目标URL
        """
        self.page.goto(url)
        self.wait_for_load()
    
    def wait_for_load(self):
        """等待页面完全加载"""
        self.page.wait_for_load_state(
            state=self.wait_config.get("load", "networkidle")
        )
    
    def refresh(self):
        """刷新页面"""
        self.page.reload()
        self.wait_for_load()
    
    # ============== 元素操作 ==============
    
    def click(self, locator: List, timeout: int = None):
        """
        点击元素
        
        Args:
            locator: 定位器
            timeout: 超时时间
        """
        timeout = timeout or self.wait_config.get("click", 1000)
        LocatorFactory.click(self.page, locator, timeout)
    
    def fill(self, locator: List, value: str, timeout: int = None):
        """
        输入文本
        
        Args:
            locator: 定位器
            value: 输入的值
            timeout: 超时时间
        """
        timeout = timeout or self.wait_config.get("input", 500)
        LocatorFactory.fill(self.page, locator, value, timeout)
    
    def select(self, locator: List, value: str, timeout: int = None):
        """
        选择下拉选项
        
        Args:
            locator: 定位器
            value: 选项值
            timeout: 超时时间
        """
        timeout = timeout or self.wait_config.get("click", 1000)
        LocatorFactory.select_option(self.page, locator, value, timeout)
    
    def get_text(self, locator: List) -> str:
        """
        获取文本
        
        Args:
            locator: 定位器
            
        Returns:
            str: 元素文本
        """
        return LocatorFactory.text(self.page, locator)
    
    def is_visible(self, locator: List) -> bool:
        """
        检查是否可见
        
        Args:
            locator: 定位器
            
        Returns:
            bool: 是否可见
        """
        return LocatorFactory.is_visible(self.page, locator)
    
    # ============== 等待 ==============
    
    def wait_for_selector(self, locator: List, timeout: int = None):
        """
        等待元素出现
        
        Args:
            locator: 定位器
            timeout: 超时时间
        """
        timeout = timeout or self.config.get("browser", {}).get("timeout", 30000)
        element = LocatorFactory.get(self.page, locator)
        element.wait_for(timeout=timeout)
    
    def wait_for_timeout(self, milliseconds: int):
        """
        等待指定时间
        
        Args:
            milliseconds: 毫秒数
        """
        self.page.wait_for_timeout(milliseconds)
    
    # ============== 弹窗处理 ==============
    
    def accept_dialog(self):
        """接受弹窗"""
        self.page.on("dialog", lambda dialog: dialog.accept())
    
    def dismiss_dialog(self):
        """拒绝弹窗"""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
    
    # ============== 截图 ==============
    
    def screenshot(self, name: str, full_page: bool = False):
        """
        截图
        
        Args:
            name: 文件名
            full_page: 是否全页截图
        """
        report_dir = self.config.get("report", {}).get("dir", "./reports")
        import os
        os.makedirs(report_dir, exist_ok=True)
        
        path = f"{report_dir}/{name}.png"
        self.page.screenshot(path=path, full_page=full_page)
        print(f"📸 截图: {path}")
    
    # ============== 表格操作 ==============
    
    def get_table_rows(self, table_locator: List) -> List:
        """
        获取表格行
        
        Args:
            table_locator: 表格定位器
            
        Returns:
            List: 行元素列表
        """
        table = LocatorFactory.get(self.page, table_locator)
        return table.locator("tr").all()
    
    def get_cell_text(self, table_locator: List, row: int, column: int) -> str:
        """
        获取单元格文本
        
        Args:
            table_locator: 表格定位器
            row: 行号（从0开始）
            column: 列号（从0开始）
            
        Returns:
            str: 单元格文本
        """
        table = LocatorFactory.get(self.page, table_locator)
        cell = table.locator("tr").nth(row).locator("td,th").nth(column)
        return cell.text_content()
    
    # ============== 消息处理 ==============
    
    def get_success_message(self) -> str:
        """
        获取成功消息
        
        Returns:
            str: 成功消息文本
        """
        if self.is_visible(BaseLocators.SUCCESS_TOAST):
            return self.get_text(BaseLocators.SUCCESS_TOAST)
        return ""
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            str: 错误消息文本
        """
        if self.is_visible(BaseLocators.ERROR_TOAST):
            return self.get_text(BaseLocators.ERROR_TOAST)
        return ""
    
    # ============== 通用操作 ==============
    
    def click_confirm(self):
        """点击确认"""
        self.click(BaseLocators.CONFIRM_BUTTON)
    
    def click_cancel(self):
        """点击取消"""
        self.click(BaseLocators.CANCEL_BUTTON)
    
    def close(self):
        """关闭页面"""
        self.page.close()


class AuthPage(BasePage):
    """认证页面基类"""
    
    def login(self, username: str, password: str) -> bool:
        """
        登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            bool: 是否登录成功
        """
        raise NotImplementedError


class LoggedInPage(BasePage):
    """已登录页面基类"""
    
    def logout(self):
        """退出登录"""
        raise NotImplementedError
