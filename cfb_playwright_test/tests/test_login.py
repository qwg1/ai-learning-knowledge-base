#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 登录测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.sync_api import Page
from utils.browser import create_browser_manager
from pages.login_page import LoginPage
from pages.merchant_page import MerchantPage


class TestLogin:
    """登录测试类"""
    
    @pytest.fixture
    def browser(self):
        """创建浏览器"""
        browser = create_browser_manager()
        browser.start()
        yield browser
        browser.close()
    
    @pytest.fixture
    def admin_login(self, browser):
        """管理员登录"""
        config = browser.config
        account = config["systems"]["admin"]
        
        page = browser.open_page("admin", account["url"])
        login_page = LoginPage(page, config, account["url"])
        
        success = login_page.login(account["username"], account["password"])
        assert success, "管理员登录失败"
        
        yield login_page, page
    
    @pytest.fixture
    def merch_login(self, browser):
        """商户登录"""
        config = browser.config
        account = config["systems"]["merch"]
        
        page = browser.open_page("merch", account["url"])
        login_page = LoginPage(page, config, account["url"])
        
        success = login_page.login(account["username"], account["password"])
        assert success, "商户登录失败"
        
        yield login_page, page
    
    def test_admin_login(self, browser):
        """
        测试用例: 管理员登录
        优先级: P0
        
        步骤:
        1. 打开管理后台
        2. 输入用户名和密码
        3. 点击登录
        
        预期: 登录成功，进入首页
        """
        print("\n" + "=" * 60)
        print("📝 测试: 管理员登录")
        print("=" * 60)
        
        config = browser.config
        account = config["systems"]["admin"]
        
        # 打开页面
        page = browser.open_page("admin_login", account["url"])
        
        # 创建登录页面
        login_page = LoginPage(page, config, account["url"])
        
        # 执行登录
        success = login_page.login(account["username"], account["password"])
        
        # 验证结果
        assert success, "管理员登录失败"
        
        print("✅ 管理员登录测试通过")
    
    def test_merchant_login(self, browser):
        """
        测试用例: 商户登录
        优先级: P0
        
        步骤:
        1. 打开商户后台
        2. 输入用户名和密码
        3. 点击登录
        
        预期: 登录成功，进入首页
        """
        print("\n" + "=" * 60)
        print("📝 测试: 商户登录")
        print("=" * 60)
        
        config = browser.config
        account = config["systems"]["merch"]
        
        # 打开页面
        page = browser.open_page("merch_login", account["url"])
        
        # 创建登录页面
        login_page = LoginPage(page, config, account["url"])
        
        # 执行登录
        success = login_page.login(account["username"], account["password"])
        
        # 验证结果
        assert success, "商户登录失败"
        
        print("✅ 商户登录测试通过")
    
    def test_login_failure(self, browser):
        """
        测试用例: 登录失败
        优先级: P2
        
        步骤:
        1. 打开登录页
        2. 输入错误的密码
        3. 点击登录
        
        预期: 显示错误信息
        """
        print("\n" + "=" * 60)
        print("📝 测试: 登录失败")
        print("=" * 60)
        
        config = browser.config
        account = config["systems"]["admin"]
        
        # 打开页面
        page = browser.open_page("login_failure", account["url"])
        
        # 创建登录页面
        login_page = LoginPage(page, config, account["url"])
        
        # 输入错误的密码
        success = login_page.login(account["username"], "wrong_password")
        
        # 验证结果
        assert not success, "登录应该失败"
        
        # 检查错误消息
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "应该显示错误消息"
        
        print(f"✅ 登录失败测试通过，错误消息: {error_msg}")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
