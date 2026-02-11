#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 页面元素定位器
统一管理所有页面元素的定位方式
"""

from typing import List, Union
from playwright.sync_api import Page


class LocatorType:
    """定位器类型常量"""
    ARIA = "aria"
    ROLE = "role"
    TEXT = "text"
    XPATH = "xpath"
    CSS = "css"
    TEST_ID = "test-id"
    LABEL = "label"


class BaseLocators:
    """基础定位器（所有页面的公共元素）"""
    
    # 通用
    LOADING = [LocatorType.ARIA, "loading"]
    MESSAGE = [LocatorType.ARIA, "message"]
    SUCCESS_TOAST = [LocatorType.XPATH, "//div[contains(@class, 'success')]"]
    ERROR_TOAST = [LocatorType.XPATH, "//div[contains(@class, 'error')]"]
    CONFIRM_BUTTON = [LocatorType.TEXT, "确定"]
    CANCEL_BUTTON = [LocatorType.TEXT, "取消"]
    CLOSE_BUTTON = [LocatorType.XPATH, "//button[contains(@class,'close')]"]


class LoginLocators:
    """登录页面元素定位器"""
    
    USERNAME = [LocatorType.ARIA, "username"]
    PASSWORD = [LocatorType.ARIA, "password"]
    VERIFY_CODE = [LocatorType.ARIA, "verify-code"]
    LOGIN_BUTTON = [LocatorType.TEXT, "登录"]
    REMEMBER = [LocatorType.ARIA, "remember"]
    FORGOT_PASSWORD = [LocatorType.TEXT, "忘记密码"]
    ERROR_MESSAGE = [LocatorType.ARIA, "error-message"]


class DashboardLocators:
    """仪表板/首页元素定位器"""
    
    # 菜单
    SIDEBAR_MENU = [LocatorType.ROLE, "navigation"]
    USER_MENU = [LocatorType.ARIA, "user-menu"]
    LOGOUT = [LocatorType.TEXT, "退出登录"]
    
    # 首页卡片
    WELCOME = [LocatorType.ARIA, "welcome"]
    QUICK_ACTIONS = [LocatorType.ARIA, "quick-actions"]
    RECENT_ORDERS = [LocatorType.ARIA, "recent-orders"]
    BALANCE_CARD = [LocatorType.ARIA, "balance-card"]
    
    # 首页提现
    WITHDRAW_BUTTON = [LocatorType.TEXT, "提现"]


class MerchantLocators:
    """商户管理页面元素定位器"""
    
    # 菜单
    MERCHANT_MENU = [LocatorType.TEXT, "商户管理"]
    MERCHANT_LIST = [LocatorType.TEXT, "商户列表"]
    CREATE_MERCHANT = [LocatorType.TEXT, "新增商户"]
    
    # 商户列表
    MERCHANT_TABLE = [LocatorType.ROLE, "table"]
    MERCHANT_ROWS = [LocatorType.XPATH, "//table//tr"]
    MERCHANT_NAME_CELL = [LocatorType.ARIA, "merchant-name"]
    STATUS_CELL = [LocatorType.ARIA, "status"]
    ACTIONS_CELL = [LocatorType.ARIA, "actions"]
    
    # 商户表单
    MERCHANT_NAME_INPUT = [LocatorType.ARIA, "merchant-name-input"]
    MERCHANT_EMAIL_INPUT = [LocatorType.ARIA, "merchant-email-input"]
    MERCHANT_PHONE_INPUT = [LocatorType.ARIA, "merchant-phone-input"]
    MERCHANT_STATUS_SELECT = [LocatorType.ARIA, "merchant-status"]
    
    # 搜索
    SEARCH_INPUT = [LocatorType.ARIA, "search-input"]
    SEARCH_BUTTON = [LocatorType.TEXT, "搜索"]
    RESET_BUTTON = [LocatorType.TEXT, "重置"]


class ChannelLocators:
    """通道管理页面元素定位器"""
    
    # 菜单
    CHANNEL_MENU = [LocatorType.TEXT, "通道管理"]
    CHANNEL_LIST = [LocatorType.TEXT, "通道列表"]
    CHANNEL_CONFIG = [LocatorType.TEXT, "通道配置"]
    BIND_CHANNEL = [LocatorType.TEXT, "绑定通道"]
    
    # 通道列表
    CHANNEL_TABLE = [LocatorType.ROLE, "table"]
    CHANNEL_NAME = [LocatorType.ARIA, "channel-name"]
    CHANNEL_STATUS = [LocatorType.ARIA, "channel-status"]
    FEE_RATE = [LocatorType.ARIA, "fee-rate"]
    
    # 通道配置表单
    FEE_RATE_INPUT = [LocatorType.ARIA, "fee-rate-input"]
    MIN_AMOUNT_INPUT = [LocatorType.ARIA, "min-amount-input"]
    MAX_AMOUNT_INPUT = [LocatorType.ARIA, "max-amount-input"]
    
    # 绑定通道
    AVAILABLE_CHANNELS = [LocatorType.ARIA, "available-channels"]
    SELECTED_CHANNELS = [LocatorType.ARIA, "selected-channels"]
    BIND_BUTTON = [LocatorType.TEXT, "绑定"]
    UNBIND_BUTTON = [LocatorType.TEXT, "解绑"]


class CollectionLocators:
    """代收管理页面元素定位器"""
    
    # 菜单
    COLLECTION_MENU = [LocatorType.TEXT, "代收管理"]
    COLLECTION_ORDER = [LocatorType.TEXT, "代收订单"]
    CREATE_COLLECTION = [LocatorType.TEXT, "创建订单"]
    
    # 创建订单表单
    AMOUNT_INPUT = [LocatorType.ARIA, "amount-input"]
    COIN_TYPE_SELECT = [LocatorType.ARIA, "coin-type"]
    COIN_TYPE_CNY = [LocatorType.TEXT, "CNY"]
    COIN_TYPE_USDT = [LocatorType.TEXT, "USDT"]
    
    # 订单列表
    ORDER_TABLE = [LocatorType.ROLE, "table"]
    ORDER_NO = [LocatorType.ARIA, "order-no"]
    ORDER_STATUS = [LocatorType.ARIA, "order-status"]
    STATUS_PENDING = [LocatorType.TEXT, "待支付"]
    STATUS_SUCCESS = [LocatorType.TEXT, "成功"]
    STATUS_FAILED = [LocatorType.TEXT, "失败"]
    
    # 搜索
    ORDER_NO_INPUT = [LocatorType.ARIA, "order-no-input"]
    DATE_RANGE = [LocatorType.ARIA, "date-range"]


class PaymentLocators:
    """代付管理页面元素定位器"""
    
    # 菜单
    PAYMENT_MENU = [LocatorType.TEXT, "代付管理"]
    PAYMENT_ORDER = [LocatorType.TEXT, "代付订单"]
    CREATE_PAYMENT = [LocatorType.TEXT, "创建订单"]
    
    # 创建订单表单
    AMOUNT_INPUT = [LocatorType.ARIA, "amount-input"]
    ADDRESS_INPUT = [LocatorType.ARIA, "address-input"]
    CHAIN_SELECT = [LocatorType.ARIA, "chain-select"]
    
    # 链类型选择
    CHAIN_CNY = [LocatorType.TEXT, "CNY"]
    CHAIN_TRC20 = [LocatorType.TEXT, "USDT-TRC20"]
    CHAIN_BEP20 = [LocatorType.TEXT, "USDT-BEP20"]
    CHAIN_ERC20 = [LocatorType.TEXT, "USDT-ERC20"]
    
    # 订单列表
    PAYMENT_TABLE = [LocatorType.ROLE, "table"]
    PAYMENT_STATUS = [LocatorType.ARIA, "payment-status"]
    STATUS_PROCESSING = [LocatorType.TEXT, "处理中"]
    STATUS_COMPLETED = [LocatorType.TEXT, "已完成"]
    STATUS_FAILED = [LocatorType.TEXT, "失败"]


class OrderLocators:
    """订单管理页面元素定位器"""
    
    # 菜单
    ORDER_MENU = [LocatorType.TEXT, "订单管理"]
    ALL_ORDERS = [LocatorType.TEXT, "全部订单"]
    
    # 搜索筛选
    ORDER_NO_INPUT = [LocatorType.ARIA, "order-no-input"]
    ORDER_TYPE_SELECT = [LocatorType.ARIA, "order-type"]
    ORDER_STATUS_SELECT = [LocatorType.ARIA, "order-status"]
    DATE_PICKER = [LocatorType.ARIA, "date-picker"]
    QUERY_BUTTON = [LocatorType.TEXT, "查询"]
    RESET_BUTTON = [LocatorType.TEXT, "重置"]
    
    # 订单列表
    ORDER_TABLE = [LocatorType.ROLE, "table"]
    ORDER_ROWS = [LocatorType.XPATH, "//table//tr"]
    
    # 订单详情
    DETAIL_PANEL = [LocatorType.ARIA, "order-detail"]
    ORDER_INFO = [LocatorType.ARIA, "order-info"]


class RefundLocators:
    """退款管理页面元素定位器"""
    
    # 菜单
    REFUND_MENU = [LocatorType.TEXT, "退款管理"]
    REFUND_ORDER = [LocatorType.TEXT, "退款订单"]
    
    # 操作按钮
    REFUND_BUTTON = [LocatorType.TEXT, "退款"]
    REFUND_CONFIRM = [LocatorType.TEXT, "确认退款"]
    
    # 搜索
    ORDER_NO_INPUT = [LocatorType.ARIA, "order-no-input"]
    QUERY_BUTTON = [LocatorType.TEXT, "查询"]
    
    # 退款表单
    REFUND_AMOUNT = [LocatorType.ARIA, "refund-amount"]
    REFUND_REASON = [LocatorType.ARIA, "refund-reason"]


class ReplenishLocators:
    """补单管理页面元素定位器"""
    
    # 菜单
    REPLENISH_MENU = [LocatorType.TEXT, "补单管理"]
    CREATE_REPLENISH = [LocatorType.TEXT, "创建补单"]
    
    # 创建补单表单
    ORDER_NO_INPUT = [LocatorType.ARIA, "order-no-input"]
    AMOUNT_INPUT = [LocatorType.ARIA, "amount-input"]
    CHAIN_SELECT = [LocatorType.ARIA, "chain-select"]
    REMARK_INPUT = [LocatorType.ARIA, "remark-input"]
    
    # 操作
    CREATE_BUTTON = [LocatorType.TEXT, "创建"]
    CONFIRM_BUTTON = [LocatorType.TEXT, "确认"]


class LimitLocators:
    """限额管理页面元素定位器"""
    
    # 菜单
    LIMIT_MENU = [LocatorType.TEXT, "限额管理"]
    
    # 限额表单
    DAILY_LIMIT_INPUT = [LocatorType.ARIA, "daily-limit-input"]
    SINGLE_LIMIT_INPUT = [LocatorType.ARIA, "single-limit-input"]
    MONTHLY_LIMIT_INPUT = [LocatorType.ARIA, "monthly-limit-input"]
    
    # 操作
    SAVE_BUTTON = [LocatorType.TEXT, "保存"]
    EDIT_BUTTON = [LocatorType.TEXT, "编辑"]


class TransferLocators:
    """转账管理页面元素定位器"""
    
    # 菜单
    TRANSFER_MENU = [LocatorType.TEXT, "转账管理"]
    MERCHANT_TRANSFER = [LocatorType.TEXT, "商户互转"]
    MANUAL_COLLECTION = [LocatorType.TEXT, "手动归集"]
    
    # 商户互转表单
    FROM_MERCHANT = [LocatorType.ARIA, "from-merchant"]
    TO_MERCHANT = [LocatorType.ARIA, "to-merchant"]
    TRANSFER_AMOUNT = [LocatorType.ARIA, "transfer-amount"]
    TRANSFER_BUTTON = [LocatorType.TEXT, "确认转账"]
    
    # 手动归集
    COLLECT_ADDRESS = [LocatorType.ARIA, "collect-address"]
    COLLECT_AMOUNT = [LocatorType.ARIA, "collect-amount"]
    COLLECT_BUTTON = [LocatorType.TEXT, "确认归集"]


class LocatorFactory:
    """定位器工厂 - 将定位器数组转换为Playwright可用的定位器"""
    
    @staticmethod
    def get(page: Page, locator: List) -> object:
        """
        获取Playwright定位器
        
        Args:
            page: Playwright页面对象
            locator: 定位器数组 [类型, 标识]
            
        Returns:
            Playwright定位器对象
        """
        locator_type = locator[0]
        identifier = locator[1]
        
        if locator_type == LocatorType.ARIA:
            return page.get_by_aria_label(identifier)
        elif locator_type == LocatorType.ROLE:
            return page.get_by_role(identifier)
        elif locator_type == LocatorType.TEXT:
            return page.get_by_text(identifier)
        elif locator_type == LocatorType.XPATH:
            return page.locator(identifier)
        elif locator_type == LocatorType.CSS:
            return page.locator(identifier)
        elif locator_type == LocatorType.TEST_ID:
            return page.get_by_test_id(identifier)
        elif locator_type == LocatorType.LABEL:
            return page.get_by_label(identifier)
        else:
            return page.locator(identifier)
    
    @staticmethod
    def click(page: Page, locator: List, timeout: int = None):
        """
        点击元素
        
        Args:
            page: Playwright页面对象
            locator: 定位器
            timeout: 超时时间
        """
        element = LocatorFactory.get(page, locator)
        element.click(timeout=timeout)
    
    @staticmethod
    def fill(page: Page, locator: List, value: str, timeout: int = None):
        """
        输入文本
        
        Args:
            page: Playwright页面对象
            locator: 定位器
            value: 输入的值
            timeout: 超时时间
        """
        element = LocatorFactory.get(page, locator)
        element.fill(value, timeout=timeout)
    
    @staticmethod
    def text(page: Page, locator: List) -> str:
        """
        获取文本
        
        Args:
            page: Playwright页面对象
            locator: 定位器
            
        Returns:
            str: 元素文本
        """
        element = LocatorFactory.get(page, locator)
        return element.text_content()
    
    @staticmethod
    def is_visible(page: Page, locator: List) -> bool:
        """
        检查是否可见
        
        Args:
            page: Playwright页面对象
            locator: 定位器
            
        Returns:
            bool: 是否可见
        """
        element = LocatorFactory.get(page, locator)
        return element.is_visible()
    
    @staticmethod
    def select_option(page: Page, locator: List, value: str, timeout: int = None):
        """
        选择下拉选项
        
        Args:
            page: Playwright页面对象
            locator: 定位器
            value: 选项值
            timeout: 超时时间
        """
        element = LocatorFactory.get(page, locator)
        element.select_option(value, timeout=timeout)


# 导出
__all__ = [
    "LocatorType",
    "BaseLocators",
    "LoginLocators",
    "DashboardLocators",
    "MerchantLocators",
    "ChannelLocators",
    "CollectionLocators",
    "PaymentLocators",
    "OrderLocators",
    "RefundLocators",
    "ReplenishLocators",
    "LimitLocators",
    "TransferLocators",
    "LocatorFactory"
]
