#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 代收代付测试
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
from pages.trade_page import CollectionPage, PaymentPage


class TestCollection:
    """代收测试类"""
    
    @pytest.fixture
    def merch_logged_in(self):
        """商户登录"""
        browser = create_browser_manager()
        browser.start()
        
        try:
            config = browser.config
            account = config["systems"]["merch"]
            
            page = browser.open_page("merch", account["url"])
            login_page = LoginPage(page, config, account["url"])
            
            success = login_page.login(account["username"], account["password"])
            assert success, "商户登录失败"
            
            collection_page = CollectionPage(page, config, account["url"])
            
            yield collection_page, browser
            
        finally:
            browser.close()
    
    def test_collection_cny(self, merch_logged_in):
        """
        测试用例: CNY代收
        优先级: P0
        
        步骤:
        1. 商户登录
        2. 进入代收页面
        3. 创建CNY代收订单
        4. 填写金额
        5. 确认
        
        预期: 订单创建成功
        """
        print("\n" + "=" * 60)
        print("📝 测试: CNY代收")
        print("=" * 60)
        
        collection_page, browser = merch_logged_in
        
        # 获取配置
        test_amount = browser.config["test"]["amounts"]["normal"]
        
        order_info = {
            "amount": test_amount,
            "coin_type": "CNY"
        }
        
        print(f"📤 订单信息: {order_info}")
        
        # 创建订单
        success = collection_page.create_order(order_info)
        
        # 验证结果
        assert success, "CNY代收订单创建失败"
        
        print("✅ CNY代收测试通过")
    
    def test_collection_usdt(self, merch_logged_in):
        """
        测试用例: USDT代收
        优先级: P0
        
        步骤:
        1. 商户登录
        2. 进入代收页面
        3. 创建USDT代收订单
        4. 选择链类型
        
        预期: 订单创建成功
        """
        print("\n" + "=" * 60)
        print("📝 测试: USDT代收")
        print("=" * 60)
        
        collection_page, browser = merch_logged_in
        
        # 获取配置
        test_amount = browser.config["test"]["amounts"]["normal"]
        
        order_info = {
            "amount": test_amount,
            "coin_type": "USDT"
        }
        
        print(f"📤 订单信息: {order_info}")
        
        # 创建订单
        success = collection_page.create_order(order_info)
        
        # 验证结果
        assert success, "USDT代收订单创建失败"
        
        print("✅ USDT代收测试通过")


class TestPayment:
    """代付测试类"""
    
    @pytest.fixture
    def merch_logged_in(self):
        """商户登录"""
        browser = create_browser_manager()
        browser.start()
        
        try:
            config = browser.config
            account = config["systems"]["merch"]
            
            page = browser.open_page("merch", account["url"])
            login_page = LoginPage(page, config, account["url"])
            
            success = login_page.login(account["username"], account["password"])
            assert success, "商户登录失败"
            
            payment_page = PaymentPage(page, config, account["url"])
            
            yield payment_page, browser
            
        finally:
            browser.close()
    
    def test_payment_trc20(self, merch_logged_in):
        """
        测试用例: USDT-TRC20代付
        优先级: P0
        
        步骤:
        1. 商户登录
        2. 进入代付页面
        3. 创建TRC20代付订单
        4. 填写地址（T开头）
        5. 确认
        
        预期: 订单创建成功
        """
        print("\n" + "=" * 60)
        print("📝 测试: USDT-TRC20代付")
        print("=" * 60)
        
        payment_page, browser = merch_logged_in
        
        # 获取配置
        test_amount = browser.config["test"]["amounts"]["normal"]
        test_address = browser.config["test"]["addresses"]["trc20"]
        
        order_info = {
            "amount": test_amount,
            "chain": "TRC20",
            "address": test_address
        }
        
        print(f"📤 订单信息: {order_info}")
        
        # 创建订单
        success = payment_page.create_order(order_info)
        
        # 验证结果
        assert success, "TRC20代付订单创建失败"
        
        print("✅ USDT-TRC20代付测试通过")
    
    def test_payment_bep20(self, merch_logged_in):
        """
        测试用例: USDT-BEP20代付
        优先级: P0
        
        步骤:
        1. 商户登录
        2. 进入代付页面
        3. 创建BEP20代付订单
        4. 填写地址（0x开头）
        5. 确认
        
        预期: 订单创建成功
        """
        print("\n" + "=" * 60)
        print("📝 测试: USDT-BEP20代付")
        print("=" * 60)
        
        payment_page, browser = merch_logged_in
        
        # 获取配置
        test_amount = browser.config["test"]["amounts"]["normal"]
        test_address = browser.config["test"]["addresses"]["bep20"]
        
        order_info = {
            "amount": test_amount,
            "chain": "BEP20",
            "address": test_address
        }
        
        print(f"📤 订单信息: {order_info}")
        
        # 创建订单
        success = payment_page.create_order(order_info)
        
        # 验证结果
        assert success, "BEP20代付订单创建失败"
        
        print("✅ USDT-BEP20代付测试通过")
    
    def test_payment_erc20(self, merch_logged_in):
        """
        测试用例: USDT-ERC20代付
        优先级: P0
        
        步骤:
        1. 商户登录
        2. 进入代付页面
        3. 创建ERC20代付订单
        4. 填写地址（0x开头）
        5. 确认
        
        预期: 订单创建成功
        """
        print("\n" + "=" * 60)
        print("📝 测试: USDT-ERC20代付")
        print("=" * 60)
        
        payment_page, browser = merch_logged_in
        
        # 获取配置
        test_amount = browser.config["test"]["amounts"]["normal"]
        test_address = browser.config["test"]["addresses"]["erc20"]
        
        order_info = {
            "amount": test_amount,
            "chain": "ERC20",
            "address": test_address
        }
        
        print(f"📤 订单信息: {order_info}")
        
        # 创建订单
        success = payment_page.create_order(order_info)
        
        # 验证结果
        assert success, "ERC20代付订单创建失败"
        
        print("✅ USDT-ERC20代付测试通过")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
