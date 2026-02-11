#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 页面操作类
为 OpenClaw browser 工具设计的页面操作封装

使用方式:
1. 在 OpenClaw 会话中使用
2. 调用 page.xxx() 方法会自动生成 browser 工具请求
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """操作类型"""
    OPEN = "open"
    SCREENSHOT = "screenshot"
    SNAPSHOT = "snapshot"
    CLICK = "click"
    TYPE = "type"
    SELECT = "select"
    WAIT = "wait"
    EVALUATE = "evaluate"
    NAVIGATE = "navigate"


@dataclass
class BrowserRequest:
    """浏览器请求"""
    action: str
    targetUrl: Optional[str] = None
    request: Optional[Dict] = None
    path: Optional[str] = None
    targetId: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        result = {"action": self.action}
        if self.targetUrl:
            result["targetUrl"] = self.targetUrl
        if self.request:
            result["request"] = self.request
        if self.path:
            result["path"] = self.path
        if self.targetId:
            result["targetId"] = self.targetId
        return result


class Page:
    """页面操作类"""
    
    def __init__(self, name: str = "page"):
        """
        初始化页面
        
        Args:
            name: 页面名称
        """
        self.name = name
        self.current_url = None
        self.requests: List[BrowserRequest] = []
    
    def open(self, url: str) -> BrowserRequest:
        """
        打开URL
        
        Args:
            url: 目标URL
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        request = BrowserRequest(
            action=ActionType.OPEN.value,
            targetUrl=url
        )
        self.current_url = url
        self.requests.append(request)
        return request
    
    def navigate(self, url: str) -> BrowserRequest:
        """
        导航到URL
        
        Args:
            url: 目标URL
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        request = BrowserRequest(
            action=ActionType.NAVIGATE.value,
            targetUrl=url
        )
        self.current_url = url
        self.requests.append(request)
        return request
    
    def screenshot(self, name: str = None) -> BrowserRequest:
        """
        截图
        
        Args:
            name: 截图名称
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        path = f"reports/{name or self.name}.png"
        request = BrowserRequest(
            action=ActionType.SCREENSHOT.value,
            path=path
        )
        self.requests.append(request)
        return request
    
    def snapshot(self) -> BrowserRequest:
        """
        获取页面快照
        
        Returns:
            BrowserRequest: 浏览器请求
        """
        request = BrowserRequest(
            action=ActionType.SNAPSHOT.value
        )
        self.requests.append(request)
        return request
    
    def click(self, ref: str = None, selector: str = None, role: str = "button") -> BrowserRequest:
        """
        点击元素
        
        Args:
            ref: ARIA ref
            selector: XPath选择器
            role: 元素角色
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        locator = self._build_locator(ref, selector, role)
        request = BrowserRequest(
            action=ActionType.CLICK.value,
            request={
                "kind": "click",
                **locator
            }
        )
        self.requests.append(request)
        return request
    
    def fill(self, ref: str = None, selector: str = None, role: str = "textbox", text: str = "") -> BrowserRequest:
        """
        输入文本
        
        Args:
            ref: ARIA ref
            selector: XPath选择器
            role: 元素角色
            text: 输入的文本
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        locator = self._build_locator(ref, selector, role)
        request = BrowserRequest(
            action=ActionType.CLICK.value,
            request={
                "kind": "type",
                "text": text,
                **locator
            }
        )
        self.requests.append(request)
        return request
    
    def select(self, ref: str = None, selector: str = None, role: str = "combobox", value: str = "") -> BrowserRequest:
        """
        选择选项
        
        Args:
            ref: ARIA ref
            selector: XPath选择器
            role: 元素角色
            value: 选项值
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        locator = self._build_locator(ref, selector, role)
        request = BrowserRequest(
            action=ActionType.CLICK.value,
            request={
                "kind": "select",
                "value": value,
                **locator
            }
        )
        self.requests.append(request)
        return request
    
    def wait(self, ref: str = None, selector: str = None, role: str = "progressbar") -> BrowserRequest:
        """
        等待元素
        
        Args:
            ref: ARIA ref
            selector: XPath选择器
            role: 元素角色
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        locator = self._build_locator(ref, selector, role)
        request = BrowserRequest(
            action=ActionType.CLICK.value,
            request={
                "kind": "wait",
                **locator
            }
        )
        self.requests.append(request)
        return request
    
    def evaluate(self, script: str) -> BrowserRequest:
        """
        执行JavaScript
        
        Args:
            script: JavaScript代码
            
        Returns:
            BrowserRequest: 浏览器请求
        """
        request = BrowserRequest(
            action=ActionType.EVALUATE.value,
            request={
                "fn": script
            }
        )
        self.requests.append(request)
        return request
    
    def _build_locator(self, ref: str = None, selector: str = None, role: str = None) -> Dict:
        """
        构建定位器
        
        Args:
            ref: ARIA ref
            selector: XPath选择器
            role: 元素角色
            
        Returns:
            Dict: 定位器字典
        """
        if ref and role:
            return {"ref": ref, "role": role}
        elif selector:
            return {"selector": selector}
        elif ref:
            return {"ref": ref}
        elif selector and role:
            return {"selector": selector, "role": role}
        else:
            raise ValueError("必须提供 ref 或 selector")
    
    def get_requests(self) -> List[Dict]:
        """
        获取所有请求
        
        Returns:
            List[Dict]: 请求字典列表
        """
        return [r.to_dict() for r in self.requests]
    
    def clear_requests(self):
        """清空请求队列"""
        self.requests.clear()
    
    def print_requests(self):
        """打印请求队列"""
        for i, req in enumerate(self.requests):
            print(f"[{i+1}] {req.action}: {req.request if req.request else req.targetUrl or ''}")


class TestCase:
    """测试用例基类"""
    
    def __init__(self, name: str, priority: str = "P2"):
        """
        初始化测试用例
        
        Args:
            name: 测试名称
            priority: 优先级
        """
        self.name = name
        self.priority = priority
        self.steps: List[str] = []
        self.page = Page(name)
    
    def setup(self):
        """测试前置操作"""
        pass
    
    def test(self):
        """测试主体"""
        raise NotImplementedError
    
    def teardown(self):
        """测试后置操作"""
        pass
    
    def run(self) -> Dict:
        """
        运行测试
        
        Returns:
            Dict: 测试结果
        """
        try:
            self.setup()
            self.test()
            self.teardown()
            return {
                "success": True,
                "name": self.name,
                "priority": self.priority,
                "requests": self.page.get_requests()
            }
        except Exception as e:
            return {
                "success": False,
                "name": self.name,
                "priority": self.priority,
                "error": str(e),
                "requests": self.page.get_requests()
            }
    
    def print_summary(self):
        """打印测试摘要"""
        print(f"\n{'='*60}")
        print(f"测试用例: {self.name}")
        print(f"优先级: {self.priority}")
        print(f"操作数: {len(self.page.requests)}")
        print(f"{'='*60}")
        self.page.print_requests()


class LoginTest(TestCase):
    """登录测试用例"""
    
    def __init__(self, system: str, username: str, password: str):
        """
        初始化
        
        Args:
            system: 系统名称
            username: 用户名
            password: 密码
        """
        super().__init__(f"登录-{system}", "P0")
        self.system = system
        self.username = username
        self.password = password
    
    def test(self):
        """测试主体"""
        # 打开登录页
        self.page.open(f"https://test-{self.system}.cfbaopay.com/login")
        self.page.wait(ref="username", role="textbox")
        
        # 输入用户名
        self.page.fill(ref="username", role="textbox", text=self.username)
        
        # 输入密码
        self.page.fill(ref="password", role="password", text=self.password)
        
        # 点击登录
        self.page.click(selector="//button[contains(text(),'登录')]")
        
        # 等待加载
        self.page.wait(ref="dashboard", role="main")


class CreateMerchantTest(TestCase):
    """创建商户测试用例"""
    
    def __init__(self, merchant_info: Dict):
        super().__init__("创建商户", "P0")
        self.merchant_info = merchant_info
    
    def test(self):
        """测试主体"""
        # 进入商户管理
        self.page.click(selector="//span[contains(text(),'商户管理')]")
        self.page.click(selector="//span[contains(text(),'商户列表')]")
        
        # 点击新增
        self.page.click(selector="//button[contains(text(),'新增商户')]")
        
        # 填写信息
        self.page.fill(ref="merchant-name", role="textbox", text=self.merchant_info["name"])
        self.page.fill(ref="merchant-email", role="textbox", text=self.merchant_info["email"])
        self.page.fill(ref="merchant-phone", role="textbox", text=self.merchant_info["phone"])
        
        # 提交
        self.page.click(selector="//button[contains(text(),'提交')]")


class PaymentTest(TestCase):
    """代付测试用例"""
    
    def __init__(self, chain: str, amount: str, address: str):
        super().__init__(f"代付-{chain}", "P0")
        self.chain = chain
        self.amount = amount
        self.address = address
    
    def test(self):
        """测试主体"""
        # 进入代付管理
        self.page.click(selector="//span[contains(text(),'代付管理')]")
        self.page.click(selector="//button[contains(text(),'创建订单')]")
        
        # 填写金额
        self.page.fill(ref="amount-input", role="textbox", text=self.amount)
        
        # 填写地址
        self.page.fill(ref="address-input", role="textbox", text=self.address)
        
        # 选择链类型
        self.page.click(ref="chain-select", role="combobox")
        if self.chain == "TRC20":
            self.page.click(selector="//li[contains(text(),'USDT-TRC20')]")
        elif self.chain == "BEP20":
            self.page.click(selector="//li[contains(text(),'USDT-BEP20')]")
        elif self.chain == "ERC20":
            self.page.click(selector="//li[contains(text(),'USDT-ERC20')]")
        
        # 提交
        self.page.click(selector="//button[contains(text(),'确认提交')]")


# 导出
__all__ = ["Page", "TestCase", "LoginTest", "CreateMerchantTest", "PaymentTest"]
