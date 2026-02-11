#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 页面元素定位器
专门为 OpenClaw browser 工具设计
"""

from typing import Dict, List, Union


class Locator:
    """元素定位器"""
    
    def __init__(self, name: str, locator: Dict):
        """
        初始化定位器
        
        Args:
            name: 定位器名称
            locator: 定位器字典
        """
        self.name = name
        self.locator = locator
    
    def click(self) -> Dict:
        """生成点击请求"""
        return {
            "kind": "click",
            **self.locator
        }
    
    def fill(self, value: str) -> Dict:
        """生成输入请求"""
        return {
            "kind": "type",
            "text": value,
            **self.locator
        }
    
    def select(self, value: str) -> Dict:
        """生成选择请求"""
        return {
            "kind": "select",
            "value": value,
            **self.locator
        }
    
    def wait(self) -> Dict:
        """生成等待请求"""
        return {
            "kind": "wait",
            **self.locator
        }
    
    def __str__(self) -> str:
        return f"{self.name}: {self.locator}"


class Locators:
    """页面元素定位器集合"""
    
    # ========== 通用定位器 ==========
    LOADING = Locator("loading", {"ref": "loading", "role": "progressbar"})
    SUCCESS_TOAST = Locator("success-toast", {"selector": "//div[contains(@class,'success')]"})
    ERROR_TOAST = Locator("error-toast", {"selector": "//div[contains(@class,'error')]"})
    CONFIRM = Locator("confirm", {"selector": "//button[contains(text(),'确定')]"})
    CANCEL = Locator("cancel", {"selector": "//button[contains(text(),'取消')]"})
    CLOSE = Locator("close", {"selector": "//button[contains(@class,'close')]"})
    
    # ========== 登录页面 ==========
    USERNAME = Locator("username", {"ref": "username", "role": "textbox"})
    PASSWORD = Locator("password", {"ref": "password", "role": "textbox"})
    VERIFY_CODE = Locator("verify-code", {"ref": "verify-code", "role": "textbox"})
    LOGIN_BTN = Locator("login-btn", {"selector": "//button[contains(text(),'登录')]"})
    LOGIN_ERROR = Locator("login-error", {"ref": "error-message", "role": "alert"})
    
    # ========== 商户管理页面 ==========
    MERCHANT_MENU = Locator("merchant-menu", {"selector": "//span[contains(text(),'商户管理')]"})
    MERCHANT_LIST = Locator("merchant-list", {"selector": "//span[contains(text(),'商户列表')]"})
    CREATE_MERCHANT = Locator("create-merchant", {"selector": "//button[contains(text(),'新增商户')]"})
    
    # 商户表单
    MERCHANT_NAME = Locator("merchant-name", {"ref": "merchant-name", "role": "textbox"})
    MERCHANT_EMAIL = Locator("merchant-email", {"ref": "merchant-email", "role": "textbox"})
    MERCHANT_PHONE = Locator("merchant-phone", {"ref": "merchant-phone", "role": "textbox"})
    MERCHANT_SUBMIT = Locator("merchant-submit", {"selector": "//button[contains(text(),'提交')]"})
    
    # 商户列表
    MERCHANT_TABLE = Locator("merchant-table", {"role": "table"})
    MERCHANT_ROWS = Locator("merchant-rows", {"selector": "//table//tr"})
    MERCHANT_STATUS = Locator("merchant-status", {"ref": "status", "role": "status"})
    
    # ========== 通道管理页面 ==========
    CHANNEL_MENU = Locator("channel-menu", {"selector": "//span[contains(text(),'通道管理')]"})
    CHANNEL_LIST = Locator("channel-list", {"selector": "//span[contains(text(),'通道列表')]"})
    CHANNEL_CONFIG = Locator("channel-config", {"selector": "//span[contains(text(),'通道配置')]"})
    BIND_CHANNEL = Locator("bind-channel", {"selector": "//button[contains(text(),'绑定通道')]"})
    
    # ========== 代收页面 ==========
    COLLECTION_MENU = Locator("collection-menu", {"selector": "//span[contains(text(),'代收管理')]"})
    COLLECTION_CREATE = Locator("collection-create", {"selector": "//button[contains(text(),'创建订单')]"})
    
    # 代收表单
    COLLECTION_AMOUNT = Locator("collection-amount", {"ref": "amount-input", "role": "textbox"})
    COIN_TYPE = Locator("coin-type", {"ref": "coin-type", "role": "combobox"})
    COIN_CNY = Locator("coin-cny", {"selector": "//li[contains(text(),'CNY')]"})
    COIN_USDT = Locator("coin-usdt", {"selector": "//li[contains(text(),'USDT')]"})
    COLLECTION_SUBMIT = Locator("collection-submit", {"selector": "//button[contains(text(),'确认提交')]"})
    
    # 代收列表
    ORDER_TABLE = Locator("order-table", {"role": "table"})
    ORDER_STATUS = Locator("order-status", {"ref": "order-status", "role": "status"})
    STATUS_PENDING = Locator("status-pending", {"selector": "//span[contains(text(),'待支付')]"})
    STATUS_SUCCESS = Locator("status-success", {"selector": "//span[contains(text(),'成功')]"})
    STATUS_FAILED = Locator("status-failed", {"selector": "//span[contains(text(),'失败')]"})
    
    # ========== 代付页面 ==========
    PAYMENT_MENU = Locator("payment-menu", {"selector": "//span[contains(text(),'代付管理')]"})
    PAYMENT_CREATE = Locator("payment-create", {"selector": "//button[contains(text(),'创建订单')]"})
    
    # 代付表单
    PAYMENT_AMOUNT = Locator("payment-amount", {"ref": "amount-input", "role": "textbox"})
    PAYMENT_ADDRESS = Locator("payment-address", {"ref": "address-input", "role": "textbox"})
    CHAIN_SELECT = Locator("chain-select", {"ref": "chain-select", "role": "combobox"})
    
    # 链类型
    CHAIN_TRC20 = Locator("chain-trc20", {"selector": "//li[contains(text(),'USDT-TRC20')]"})
    CHAIN_BEP20 = Locator("chain-bep20", {"selector": "//li[contains(text(),'USDT-BEP20')]"})
    CHAIN_ERC20 = Locator("chain-erc20", {"selector": "//li[contains(text(),'USDT-ERC20')]"})
    CHAIN_CNY = Locator("chain-cny", {"selector": "//li[contains(text(),'CNY')]"})
    
    PAYMENT_SUBMIT = Locator("payment-submit", {"selector": "//button[contains(text(),'确认提交')]"})
    
    # ========== 订单管理页面 ==========
    ORDER_MENU = Locator("order-menu", {"selector": "//span[contains(text(),'订单管理')]"})
    ALL_ORDERS = Locator("all-orders", {"selector": "//span[contains(text(),'全部订单')]"})
    
    ORDER_NO_INPUT = Locator("order-no-input", {"ref": "order-no-input", "role": "textbox"})
    QUERY_BTN = Locator("query-btn", {"selector": "//button[contains(text(),'查询')]"})
    
    # ========== 退款页面 ==========
    REFUND_MENU = Locator("refund-menu", {"selector": "//span[contains(text(),'退款管理')]"})
    REFUND_BTN = Locator("refund-btn", {"selector": "//button[contains(text(),'退款')]"})
    REFUND_CONFIRM = Locator("refund-confirm", {"selector": "//button[contains(text(),'确认退款')]"})
    
    # ========== 补单页面 ==========
    REPLENISH_MENU = Locator("replenish-menu", {"selector": "//span[contains(text(),'补单管理')]"})
    CREATE_REPLENISH = Locator("create-replenish", {"selector": "//button[contains(text(),'创建补单')]"})
    
    # ========== 调额页面 ==========
    LIMIT_MENU = Locator("limit-menu", {"selector": "//span[contains(text(),'限额管理')]"})
    DAILY_LIMIT = Locator("daily-limit", {"ref": "daily-limit", "role": "textbox"})
    SINGLE_LIMIT = Locator("single-limit", {"ref": "single-limit", "role": "textbox"})
    LIMIT_SAVE = Locator("limit-save", {"selector": "//button[contains(text(),'保存')]"})
    
    # ========== 转账页面 ==========
    TRANSFER_MENU = Locator("transfer-menu", {"selector": "//span[contains(text(),'转账管理')]"})
    MERCHANT_TRANSFER = Locator("merchant-transfer", {"selector": "//span[contains(text(),'商户互转')]"})
    MANUAL_COLLECTION = Locator("manual-collection", {"selector": "//span[contains(text(),'手动归集')]"})
    
    FROM_MERCHANT = Locator("from-merchant", {"ref": "from-merchant", "role": "combobox"})
    TO_MERCHANT = Locator("to-merchant", {"ref": "to-merchant", "role": "combobox"})
    TRANSFER_AMOUNT = Locator("transfer-amount", {"ref": "transfer-amount", "role": "textbox"})
    TRANSFER_BTN = Locator("transfer-btn", {"selector": "//button[contains(text(),'确认转账')]}")
    
    COLLECT_ADDRESS = Locator("collect-address", {"ref": "collect-address", "role": "textbox"})
    COLLECT_AMOUNT = Locator("collect-amount", {"ref": "collect-amount", "role": "textbox"})
    COLLECT_BTN = Locator("collect-btn", {"selector": "//button[contains(text(),'确认归集')]"})


class PageLocators:
    """页面定位器工厂"""
    
    @staticmethod
    def get_login() -> Dict[str, Locator]:
        return {
            "username": Locators.USERNAME,
            "password": Locators.PASSWORD,
            "verify_code": Locators.VERIFY_CODE,
            "login_btn": Locators.LOGIN_BTN,
            "error": Locators.LOGIN_ERROR
        }
    
    @staticmethod
    def get_merchant() -> Dict[str, Locator]:
        return {
            "menu": Locators.MERCHANT_MENU,
            "list": Locators.MERCHANT_LIST,
            "create": Locators.CREATE_MERCHANT,
            "name": Locators.MERCHANT_NAME,
            "email": Locators.MERCHANT_EMAIL,
            "phone": Locators.MERCHANT_PHONE,
            "submit": Locators.MERCHANT_SUBMIT,
            "table": Locators.MERCHANT_TABLE
        }
    
    @staticmethod
    def get_collection() -> Dict[str, Locator]:
        return {
            "menu": Locators.COLLECTION_MENU,
            "create": Locators.COLLECTION_CREATE,
            "amount": Locators.COLLECTION_AMOUNT,
            "coin_type": Locators.COIN_TYPE,
            "cny": Locators.COIN_CNY,
            "usdt": Locators.COIN_USDT,
            "submit": Locators.COLLECTION_SUBMIT,
            "table": Locators.ORDER_TABLE
        }
    
    @staticmethod
    def get_payment() -> Dict[str, Locator]:
        return {
            "menu": Locators.PAYMENT_MENU,
            "create": Locators.PAYMENT_CREATE,
            "amount": Locators.PAYMENT_AMOUNT,
            "address": Locators.PAYMENT_ADDRESS,
            "chain": Locators.CHAIN_SELECT,
            "trc20": Locators.CHAIN_TRC20,
            "bep20": Locators.CHAIN_BEP20,
            "erc20": Locators.CHAIN_ERC20,
            "cny": Locators.CHAIN_CNY,
            "submit": Locators.PAYMENT_SUBMIT
        }


# 导出
__all__ = ["Locator", "Locators", "PageLocators"]
