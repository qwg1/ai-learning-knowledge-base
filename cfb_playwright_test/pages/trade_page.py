#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 交易管理页面
代收、代付、订单查询
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.base_page import LoggedInPage
from utils.locator import (
    CollectionLocators,
    PaymentLocators,
    OrderLocators,
    BaseLocators
)


class CollectionPage(LoggedInPage):
    """代收管理页面"""
    
    def __init__(self, page, config: dict, base_url: str):
        super().__init__(page, config)
        self.base_url = base_url.rstrip("/")
    
    def navigate_to_collection(self):
        """导航到代收页面"""
        self.navigate(f"{self.base_url}/collection")
        self.wait_for_load()
    
    def create_order(self, order_info: Dict) -> bool:
        """
        创建代收订单
        
        Args:
            order_info: 订单信息
                {
                    "amount": "100",
                    "coin_type": "CNY"
                }
                
        Returns:
            bool: 是否创建成功
        """
        print(f"📝 创建代收订单: {order_info}")
        
        # 导航到代收页面
        self.navigate_to_collection()
        
        # 点击创建订单
        self.click(CollectionLocators.CREATE_COLLECTION)
        
        # 填写订单信息
        self.fill(CollectionLocators.AMOUNT_INPUT, order_info["amount"])
        
        # 选择币种
        if order_info.get("coin_type") == "CNY":
            self.select(CollectionLocators.COIN_TYPE_SELECT, "CNY")
        else:
            self.select(CollectionLocators.COIN_TYPE_SELECT, order_info.get("coin_type", "CNY"))
        
        # 提交
        self.click(CollectionLocators.SUBMIT_BUTTON)
        
        # 等待结果
        self.wait_for_load()
        
        # 检查是否成功
        success_msg = self.get_success_message()
        if success_msg:
            print(f"✅ 代收订单创建成功: {success_msg}")
            return True
        
        error_msg = self.get_error_message()
        if error_msg:
            print(f"❌ 代收订单创建失败: {error_msg}")
        
        return False
    
    def get_order_list(self) -> List[Dict]:
        """获取代收订单列表"""
        self.navigate_to_collection()
        
        orders = []
        rows = self.get_table_rows(CollectionLocators.ORDER_TABLE)
        
        for row in rows[1:]:  # 跳过表头
            cells = row.locator("td,th").all()
            
            if len(cells) >= 4:
                order = {
                    "order_no": cells[0].text_content().strip(),
                    "amount": cells[1].text_content().strip(),
                    "status": cells[2].text_content().strip(),
                    "time": cells[3].text_content().strip()
                }
                orders.append(order)
        
        return orders


class PaymentPage(LoggedInPage):
    """代付管理页面"""
    
    def __init__(self, page, config: dict, base_url: str):
        super().__init__(page, config)
        self.base_url = base_url.rstrip("/")
    
    def navigate_to_payment(self):
        """导航到代付页面"""
        self.navigate(f"{self.base_url}/payment")
        self.wait_for_load()
    
    def create_order(self, order_info: Dict) -> bool:
        """
        创建代付订单
        
        Args:
            order_info: 订单信息
                {
                    "amount": "10",
                    "chain": "TRC20",  # TRC20/BEP20/ERC20/CNY
                    "address": "Txxx"  # 收款地址
                }
                
        Returns:
            bool: 是否创建成功
        """
        print(f"📝 创建代付订单: {order_info}")
        
        # 导航到代付页面
        self.navigate_to_payment()
        
        # 点击创建订单
        self.click(PaymentLocators.CREATE_PAYMENT)
        
        # 填写订单信息
        self.fill(PaymentLocators.AMOUNT_INPUT, order_info["amount"])
        self.fill(PaymentLocators.ADDRESS_INPUT, order_info["address"])
        
        # 选择链类型
        chain = order_info.get("chain", "TRC20")
        if chain == "TRC20":
            self.click(PaymentLocators.CHAIN_TRC20)
        elif chain == "BEP20":
            self.click(PaymentLocators.CHAIN_BEP20)
        elif chain == "ERC20":
            self.click(PaymentLocators.CHAIN_ERC20)
        elif chain == "CNY":
            self.click(PaymentLocators.CHAIN_CNY)
        
        # 提交
        self.click(BaseLocators.CONFIRM_BUTTON)
        
        # 等待结果
        self.wait_for_load()
        
        # 检查是否成功
        success_msg = self.get_success_message()
        if success_msg:
            print(f"✅ 代付订单创建成功: {success_msg}")
            return True
        
        error_msg = self.get_error_message()
        if error_msg:
            print(f"❌ 代付订单创建失败: {error_msg}")
        
        return False
    
    def get_order_list(self) -> List[Dict]:
        """获取代付订单列表"""
        self.navigate_to_payment()
        
        orders = []
        rows = self.get_table_rows(PaymentLocators.PAYMENT_TABLE)
        
        for row in rows[1:]:
            cells = row.locator("td,th").all()
            
            if len(cells) >= 4:
                order = {
                    "order_no": cells[0].text_content().strip(),
                    "amount": cells[1].text_content().strip(),
                    "status": cells[2].text_content().strip(),
                    "chain": cells[3].text_content().strip()
                }
                orders.append(order)
        
        return orders


class OrderPage(LoggedInPage):
    """订单管理页面"""
    
    def __init__(self, page, config: dict, base_url: str):
        super().__init__(page, config)
        self.base_url = base_url.rstrip("/")
    
    def navigate_to_orders(self):
        """导航到订单页面"""
        self.navigate(f"{self.base_url}/orders")
        self.wait_for_load()
    
    def search_orders(self, order_no: str = None, status: str = None) -> List[Dict]:
        """
        搜索订单
        
        Args:
            order_no: 订单号
            status: 订单状态
            
        Returns:
            List[Dict]: 订单列表
        """
        self.navigate_to_orders()
        
        if order_no:
            self.fill(OrderLocators.ORDER_NO_INPUT, order_no)
        
        if status:
            self.select(OrderLocators.ORDER_STATUS_SELECT, status)
        
        # 点击查询
        self.click(OrderLocators.QUERY_BUTTON)
        
        # 等待结果
        self.wait_for_load()
        
        # 获取订单列表
        orders = []
        rows = self.get_table_rows(OrderLocators.ORDER_TABLE)
        
        for row in rows[1:]:
            cells = row.locator("td,th").all()
            
            if len(cells) >= 5:
                order = {
                    "order_no": cells[0].text_content().strip(),
                    "type": cells[1].text_content().strip(),
                    "amount": cells[2].text_content().strip(),
                    "status": cells[3].text_content().strip(),
                    "time": cells[4].text_content().strip()
                }
                orders.append(order)
        
        return orders
