#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 商户管理测试
"""

import pytest
import time
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.sync_api import Page
from utils.browser import create_browser_manager
from pages.login_page import LoginPage
from pages.merchant_page import MerchantPage


class TestMerchant:
    """商户管理测试类"""
    
    @pytest.fixture
    def admin_logged_in(self):
        """管理员登录"""
        browser = create_browser_manager()
        browser.start()
        
        try:
            config = browser.config
            account = config["systems"]["admin"]
            
            page = browser.open_page("admin", account["url"])
            login_page = LoginPage(page, config, account["url"])
            
            success = login_page.login(account["username"], account["password"])
            assert success, "管理员登录失败"
            
            merchant_page = MerchantPage(page, config, account["url"])
            
            yield merchant_page, browser
            
        finally:
            browser.close()
    
    def test_create_merchant(self, admin_logged_in):
        """
        测试用例: 创建新商户
        优先级: P0
        
        步骤:
        1. 管理员登录
        2. 进入商户管理
        3. 点击新增商户
        4. 填写商户信息
        5. 提交
        
        预期: 商户创建成功
        """
        print("\n" + "=" * 60)
        print("📝 测试: 创建新商户")
        print("=" * 60)
        
        merchant_page, browser = admin_logged_in
        
        # 生成唯一的商户信息
        merchant_no = int(time.time())
        merchant_info = {
            "name": f"测试商户{merchant_no}",
            "email": f"test{merchant_no}@example.com",
            "phone": f"138{random.randint(10000000, 99999999)}"
        }
        
        print(f"📤 商户信息: {merchant_info}")
        
        # 创建商户
        success = merchant_page.create_merchant(merchant_info)
        
        # 验证结果
        assert success, "商户创建失败"
        
        # 验证商户存在
        exists = merchant_page.is_merchant_exists(merchant_info["name"])
        assert exists, "商户不存在"
        
        print("✅ 商户创建测试通过")
    
    def test_search_merchant(self, admin_logged_in):
        """
        测试用例: 搜索商户
        优先级: P1
        
        步骤:
        1. 管理员登录
        2. 进入商户管理
        3. 输入商户名称搜索
        
        预期: 显示搜索结果
        """
        print("\n" + "=" * 60)
        print("📝 测试: 搜索商户")
        print("=" * 60)
        
        merchant_page, browser = admin_logged_in
        
        # 先创建商户
        merchant_no = int(time.time())
        merchant_info = {
            "name": f"搜索测试商户{merchant_no}",
            "email": f"search{merchant_no}@example.com",
            "phone": f"138{random.randint(10000000, 99999999)}"
        }
        
        success = merchant_page.create_merchant(merchant_info)
        assert success, "商户创建失败"
        
        # 搜索商户
        print(f"🔍 搜索商户: {merchant_info['name']}")
        merchant_page.search_merchant(name=merchant_info["name"])
        
        # 验证结果
        merchants = merchant_page.get_merchant_list()
        
        found = False
        for merchant in merchants:
            if merchant_info["name"] in merchant["name"]:
                found = True
                print(f"✅ 找到商户: {merchant}")
                break
        
        assert found, "未找到搜索的商户"
        print("✅ 商户搜索测试通过")
    
    def test_freeze_merchant(self, admin_logged_in):
        """
        测试用例: 冻结商户
        优先级: P1
        
        步骤:
        1. 管理员登录
        2. 进入商户管理
        3. 选择商户
        4. 点击冻结
        
        预期: 商户状态变为冻结
        """
        print("\n" + "=" * 60)
        print("📝 测试: 冻结商户")
        print("=" * 60)
        
        merchant_page, browser = admin_logged_in
        
        # 先创建商户
        merchant_no = int(time.time())
        merchant_info = {
            "name": f"冻结测试商户{merchant_no}",
            "email": f"freeze{merchant_no}@example.com",
            "phone": f"138{random.randint(10000000, 99999999)}"
        }
        
        success = merchant_page.create_merchant(merchant_info)
        assert success, "商户创建失败"
        
        # 冻结商户
        success = merchant_page.freeze_merchant(merchant_info["name"])
        assert success, "商户冻结失败"
        
        print("✅ 商户冻结测试通过")
    
    def test_unfreeze_merchant(self, admin_logged_in):
        """
        测试用例: 解冻商户
        优先级: P1
        
        步骤:
        1. 管理员登录
        2. 进入商户管理
        3. 选择已冻结商户
        4. 点击解冻
        
        预期: 商户状态变为已激活
        """
        print("\n" + "=" * 60)
        print("📝 测试: 解冻商户")
        print("=" * 60)
        
        merchant_page, browser = admin_logged_in
        
        # 先冻结商户
        merchant_no = int(time.time())
        merchant_info = {
            "name": f"解冻测试商户{merchant_no}",
            "email": f"unfreeze{merchant_no}@example.com",
            "phone": f"138{random.randint(10000000, 99999999)}"
        }
        
        success = merchant_page.create_merchant(merchant_info)
        assert success, "商户创建失败"
        
        # 冻结
        success = merchant_page.freeze_merchant(merchant_info["name"])
        assert success, "商户冻结失败"
        
        # 解冻
        success = merchant_page.unfreeze_merchant(merchant_info["name"])
        assert success, "商户解冻失败"
        
        print("✅ 商户解冻测试通过")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
