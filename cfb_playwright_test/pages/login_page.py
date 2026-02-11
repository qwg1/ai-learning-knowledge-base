#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 登录页面
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.base_page import AuthPage
from utils.locator import (
    LoginLocators,
    DashboardLocators,
    BaseLocators
)


class LoginPage(AuthPage):
    """登录页面"""
    
    def __init__(self, page, config: dict, base_url: str):
        """
        初始化登录页面
        
        Args:
            page: Playwright页面对象
            config: 配置字典
            base_url: 系统基础URL
        """
        super().__init__(page, config)
        self.base_url = base_url.rstrip("/")
    
    def navigate_to_login(self):
        """导航到登录页"""
        self.navigate(f"{self.base_url}/login")
    
    def login(self, username: str, password: str) -> bool:
        """
        登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            bool: 是否登录成功
        """
        print(f"📝 登录中: {username}")
        
        # 导航到登录页
        self.navigate_to_login()
        
        # 等待页面加载
        self.wait_for_load()
        
        # 输入用户名
        self.fill(LoginLocators.USERNAME, username)
        
        # 输入密码
        self.fill(LoginLocators.PASSWORD, password)
        
        # 点击登录按钮
        self.click(LoginLocators.LOGIN_BUTTON)
        
        # 等待登录结果
        self.wait_for_load()
        
        # 检查是否登录成功（检查是否跳转到首页）
        if self.is_visible(DashboardLocators.WELCOME):
            print(f"✅ 登录成功")
            return True
        
        # 检查是否有错误消息
        error_msg = self.get_error_message()
        if error_msg:
            print(f"❌ 登录失败: {error_msg}")
        
        return False
    
    def login_with_verify_code(self, username: str, password: str, verify_code: str) -> bool:
        """
        带验证码登录
        
        Args:
            username: 用户名
            password: 密码
            verify_code: 验证码
            
        Returns:
            bool: 是否登录成功
        """
        print(f"📝 登录中（验证码）: {username}")
        
        # 导航到登录页
        self.navigate_to_login()
        
        # 等待页面加载
        self.wait_for_load()
        
        # 输入用户名
        self.fill(LoginLocators.USERNAME, username)
        
        # 输入密码
        self.fill(LoginLocators.PASSWORD, password)
        
        # 输入验证码
        self.fill(LoginLocators.VERIFY_CODE, verify_code)
        
        # 点击登录按钮
        self.click(LoginLocators.LOGIN_BUTTON)
        
        # 等待登录结果
        self.wait_for_load()
        
        # 检查是否登录成功
        if self.is_visible(DashboardLocators.WELCOME):
            print(f"✅ 登录成功")
            return True
        
        return False
    
    def is_logged_out(self) -> bool:
        """
        检查是否已退出登录
        
        Returns:
            bool: 是否已退出
        """
        return self.is_visible(LoginLocators.LOGIN_BUTTON)
    
    def get_error_message(self) -> Optional[str]:
        """
        获取错误消息
        
        Returns:
            str: 错误消息文本
        """
        if self.is_visible(LoginLocators.ERROR_MESSAGE):
            return self.get_text(LoginLocators.ERROR_MESSAGE)
        return super().get_error_message()


class LogoutMixin:
    """退出登录混入类"""
    
    def logout(self):
        """退出登录"""
        # 点击用户菜单
        self.click(DashboardLocators.USER_MENU)
        
        # 点击退出
        self.click(DashboardLocators.LOGOUT)
        
        # 确认退出
        self.accept_dialog()
        
        # 等待返回登录页
        self.wait_for_load()
        
        print("✅ 已退出登录")
