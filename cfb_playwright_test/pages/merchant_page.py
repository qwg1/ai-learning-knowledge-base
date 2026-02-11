#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 商户管理页面
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.base_page import LoggedInPage
from utils.locator import (
    MerchantLocators,
    BaseLocators
)


class MerchantPage(LoggedInPage):
    """商户管理页面"""
    
    def __init__(self, page, config: dict, base_url: str):
        """
        初始化商户管理页面
        
        Args:
            page: Playwright页面对象
            config: 配置字典
            base_url: 系统基础URL
        """
        super().__init__(page, config)
        self.base_url = base_url.rstrip("/")
    
    def navigate_to_merchant(self):
        """导航到商户管理"""
        self.navigate(f"{self.base_url}/merchant")
        self.wait_for_load()
    
    def navigate_to_create(self):
        """导航到创建商户页"""
        self.navigate(f"{self.base_url}/merchant/create")
        self.wait_for_load()
    
    # ============== 商户列表 ==============
    
    def search_merchant(self, name: str = None, status: str = None):
        """
        搜索商户
        
        Args:
            name: 商户名称（模糊搜索）
            status: 商户状态
        """
        if name:
            self.fill(MerchantLocators.SEARCH_INPUT, name)
        
        if status:
            self.select(MerchantLocators.MERCHANT_STATUS_SELECT, status)
        
        # 点击搜索
        self.click(MerchantLocators.SEARCH_BUTTON)
        
        # 等待结果
        self.wait_for_load()
    
    def get_merchant_list(self) -> List[Dict]:
        """
        获取商户列表
        
        Returns:
            List[Dict]: 商户信息列表
        """
        merchants = []
        
        # 获取所有行
        rows = self.get_table_rows(MerchantLocators.MERCHANT_TABLE)
        
        for row in rows[1:]:  # 跳过表头
            cells = row.locator("td,th").all()
            
            if len(cells) >= 3:
                merchant = {
                    "name": cells[0].text_content().strip(),
                    "status": cells[1].text_content().strip(),
                    "actions": cells[2].text_content().strip()
                }
                merchants.append(merchant)
        
        return merchants
    
    def is_merchant_exists(self, name: str) -> bool:
        """
        检查商户是否存在
        
        Args:
            name: 商户名称
            
        Returns:
            bool: 是否存在
        """
        self.search_merchant(name=name)
        
        merchants = self.get_merchant_list()
        for merchant in merchants:
            if name in merchant["name"]:
                return True
        
        return False
    
    # ============== 创建商户 ==============
    
    def create_merchant(self, merchant_info: Dict) -> bool:
        """
        创建商户
        
        Args:
            merchant_info: 商户信息字典
                {
                    "name": "商户名称",
                    "email": "邮箱",
                    "phone": "电话"
                }
                
        Returns:
            bool: 是否创建成功
        """
        print(f"📝 创建商户: {merchant_info.get('name')}")
        
        # 导航到创建页
        self.navigate_to_create()
        
        # 填写商户信息
        self.fill(MerchantLocators.MERCHANT_NAME_INPUT, merchant_info["name"])
        self.fill(MerchantLocators.MERCHANT_EMAIL_INPUT, merchant_info["email"])
        self.fill(MerchantLocators.MERCHANT_PHONE_INPUT, merchant_info["phone"])
        
        # 提交
        self.click(BaseLocators.CONFIRM_BUTTON)
        
        # 等待结果
        self.wait_for_load()
        
        # 检查是否创建成功
        success_msg = self.get_success_message()
        if success_msg:
            print(f"✅ 商户创建成功: {success_msg}")
            return True
        
        error_msg = self.get_error_message()
        if error_msg:
            print(f"❌ 商户创建失败: {error_msg}")
        
        return False
    
    # ============== 商户操作 ==============
    
    def view_merchant(self, name: str):
        """
        查看商户详情
        
        Args:
            name: 商户名称
        """
        self.search_merchant(name=name)
        
        # 点击查看
        # TODO: 根据实际定位器修改
        self.click([BaseLocators.XPATH, f"//td[contains(text(),'{name}')]//following-sibling::td//a[text()='查看']"])
    
    def freeze_merchant(self, name: str) -> bool:
        """
        冻结商户
        
        Args:
            name: 商户名称
            
        Returns:
            bool: 是否操作成功
        """
        print(f"🔴 冻结商户: {name}")
        
        self.search_merchant(name=name)
        
        # 点击冻结
        self.click([BaseLocators.XPATH, f"//td[contains(text(),'{name}')]//following-sibling::td//button[text()='冻结']"])
        
        # 确认操作
        self.accept_dialog()
        
        # 等待结果
        self.wait_for_timeout(1000)
        
        # 验证状态变化
        self.search_merchant(name=name)
        merchants = self.get_merchant_list()
        
        for merchant in merchants:
            if name in merchant["name"]:
                if "冻结" in merchant["status"]:
                    print(f"✅ 商户已冻结")
                    return True
        
        return False
    
    def unfreeze_merchant(self, name: str) -> bool:
        """
        解冻商户
        
        Args:
            name: 商户名称
            
        Returns:
            bool: 是否操作成功
        """
        print(f"🟢 解冻商户: {name}")
        
        self.search_merchant(name=name)
        
        # 点击解冻
        self.click([BaseLocators.XPATH, f"//td[contains(text(),'{name}')]//following-sibling::td//button[text()='解冻']"])
        
        # 确认操作
        self.accept_dialog()
        
        # 等待结果
        self.wait_for_timeout(1000)
        
        return True
    
    def set_merchant_status(self, name: str, status: str) -> bool:
        """
        设置商户状态
        
        Args:
            name: 商户名称
            status: 目标状态
            
        Returns:
            bool: 是否操作成功
        """
        if status == "冻结":
            return self.freeze_merchant(name)
        elif status == "已激活":
            return self.unfreeze_merchant(name)
        
        return False
