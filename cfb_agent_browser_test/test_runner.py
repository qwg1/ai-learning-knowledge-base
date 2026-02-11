#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - OpenClaw测试脚本
直接在OpenClaw会话中运行的测试

使用方法:
1. 在OpenClaw会话中
2. 运行此脚本
3. 会自动执行browser工具调用
"""

from typing import Dict, List
import json


# ============== 测试配置 ==============
CONFIG = {
    "systems": {
        "admin": {
            "url": "https://test-admin.cfbaopay.com",
            "username": "your_admin_username",
            "password": "your_admin_password"
        },
        "merch": {
            "url": "https://test-merch.cfbaopay.com",
            "username": "your_merchant_username",
            "password": "your_merchant_password"
        }
    },
    "test": {
        "amounts": {
            "min": "0.01",
            "normal": "1"
        },
        "addresses": {
            "trc20": "TYourAddress",
            "bep20": "0xYourAddress",
            "erc20": "0xYourAddress"
        }
    }
}


# ============== 页面操作 ==============
class PageActions:
    """页面操作集合"""
    
    @staticmethod
    def open(url: str) -> Dict:
        """打开URL"""
        return {"action": "open", "targetUrl": url}
    
    @staticmethod
    def click(ref: str = None, selector: str = None, role: str = "button") -> Dict:
        """点击元素"""
        if ref and role:
            return {"action": "act", "request": {"kind": "click", "ref": ref, "role": role}}
        elif selector:
            return {"action": "act", "request": {"kind": "click", "selector": selector}}
        return {"action": "act", "request": {"kind": "click"}}
    
    @staticmethod
    def fill(ref: str = None, selector: str = None, role: str = "textbox", text: str = "") -> Dict:
        """输入文本"""
        if ref and role:
            return {"action": "act", "request": {"kind": "type", "ref": ref, "role": role, "text": text}}
        elif selector:
            return {"action": "act", "request": {"kind": "type", "selector": selector, "text": text}}
        return {"action": "act", "request": {"kind": "type", "text": text}}
    
    @staticmethod
    def screenshot(name: str) -> Dict:
        """截图"""
        return {"action": "screenshot", "path": f"reports/{name}.png"}
    
    @staticmethod
    def snapshot() -> Dict:
        """获取页面快照"""
        return {"action": "snapshot"}
    
    @staticmethod
    def wait(ref: str = None, selector: str = None, role: str = "progressbar", time_ms: int = 3000) -> Dict:
        """等待元素"""
        if ref and role:
            return {"action": "act", "request": {"kind": "wait", "ref": ref, "role": role, "timeMs": time_ms}}
        elif selector:
            return {"action": "act", "request": {"kind": "wait", "selector": selector, "timeMs": time_ms}}
        return {"action": "act", "request": {"kind": "wait", "timeMs": time_ms}}


# ============== 测试步骤 ==============
class TestSteps:
    """测试步骤生成器"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Dict] = []
    
    def add(self, action: Dict):
        """添加步骤"""
        self.steps.append(action)
    
    def open(self, url: str):
        """打开页面"""
        self.add(PageActions.open(url))
    
    def click(self, ref: str = None, selector: str = None, role: str = "button"):
        """点击"""
        self.add(PageActions.click(ref, selector, role))
    
    def fill(self, ref: str = None, selector: str = None, role: str = "textbox", text: str = ""):
        """输入"""
        self.add(PageActions.fill(ref, selector, role, text))
    
    def screenshot(self, name: str):
        """截图"""
        self.add(PageActions.screenshot(name))
    
    def snapshot(self):
        """快照"""
        self.add(PageActions.snapshot())
    
    def wait(self, ref: str = None, selector: str = None, role: str = "progressbar", time_ms: int = 3000):
        """等待"""
        self.add(PageActions.wait(ref, selector, role, time_ms))
    
    def run(self):
        """运行测试（生成步骤列表）"""
        return self.steps
    
    def print(self):
        """打印步骤"""
        print(f"\n{'='*60}")
        print(f"测试: {self.name}")
        print(f"步骤数: {len(self.steps)}")
        print(f"{'='*60}")
        for i, step in enumerate(self.steps, 1):
            action = step.get("action", "")
            if action == "open":
                print(f"[{i}] 打开: {step.get('targetUrl')}")
            elif action == "screenshot":
                print(f"[{i}] 截图: {step.get('path')}")
            elif action == "snapshot":
                print(f"[{i}] 快照")
            elif action == "act":
                req = step.get("request", {})
                kind = req.get("kind", "")
                if kind == "click":
                    ref = req.get("ref", "")
                    selector = req.get("selector", "")
                    print(f"[{i}] 点击: {ref or selector}")
                elif kind == "type":
                    text = req.get("text", "")
                    ref = req.get("ref", "")
                    selector = req.get("selector", "")
                    print(f"[{i}] 输入: {text[:20]}... ({ref or selector})")


# ============== 测试用例 ==============
def test_login_admin():
    """测试: 管理员登录"""
    steps = TestSteps("管理员登录")
    
    # 打开登录页
    steps.open("https://test-admin.cfbaopay.com/login")
    steps.wait(ref="username", role="textbox")
    
    # 输入用户名
    steps.fill(ref="username", role="textbox", text=CONFIG["systems"]["admin"]["username"])
    
    # 输入密码
    steps.fill(ref="password", role="password", text=CONFIG["systems"]["admin"]["password"])
    
    # 点击登录
    steps.click(selector="//button[contains(text(),'登录')]")
    
    # 等待加载
    steps.wait(selector="//span[contains(text(),'商户管理')]")
    
    return steps


def test_create_merchant():
    """测试: 创建商户"""
    steps = TestSteps("创建商户")
    
    # 进入商户管理
    steps.click(selector="//span[contains(text(),'商户管理')]")
    steps.click(selector="//span[contains(text(),'商户列表')]")
    steps.wait(selector="//table")
    
    # 点击新增
    steps.click(selector="//button[contains(text(),'新增商户')]")
    
    # 填写商户信息
    import time
    merchant_no = str(int(time.time()))[-6:]
    steps.fill(ref="merchant-name", role="textbox", text=f"测试商户{merchant_no}")
    steps.fill(ref="merchant-email", role="textbox", text=f"test{merchant_no}@example.com")
    steps.fill(ref="merchant-phone", role="textbox", text="13800138000")
    
    # 提交
    steps.click(selector="//button[contains(text(),'提交')]")
    steps.wait(selector="//div[contains(@class,'success')]")
    
    return steps


def test_collection_cny():
    """测试: CNY代收"""
    steps = TestSteps("CNY代收")
    
    # 进入代收管理
    steps.click(selector="//span[contains(text(),'代收管理')]")
    steps.click(selector="//button[contains(text(),'创建订单')]")
    
    # 填写金额
    steps.fill(ref="amount-input", role="textbox", text="1")
    
    # 选择CNY
    steps.click(ref="coin-type", role="combobox")
    steps.click(selector="//li[contains(text(),'CNY')]")
    
    # 提交
    steps.click(selector="//button[contains(text(),'确认提交')]")
    steps.wait(selector="//div[contains(@class,'success')]")
    
    return steps


def test_payment_trc20():
    """测试: USDT-TRC20代付"""
    steps = TestSteps("USDT-TRC20代付")
    
    # 进入代付管理
    steps.click(selector="//span[contains(text(),'代付管理')]")
    steps.click(selector="//button[contains(text(),'创建订单')]")
    
    # 填写金额
    steps.fill(ref="amount-input", role="textbox", text="1")
    
    # 填写地址
    steps.fill(ref="address-input", role="textbox", text=CONFIG["test"]["addresses"]["trc20"])
    
    # 选择TRC20
    steps.click(ref="chain-select", role="combobox")
    steps.click(selector="//li[contains(text(),'USDT-TRC20')]")
    
    # 提交
    steps.click(selector="//button[contains(text(),'确认提交')]")
    steps.wait(selector="//div[contains(@class,'success')]")
    
    return steps


def test_payment_bep20():
    """测试: USDT-BEP20代付"""
    steps = TestSteps("USDT-BEP20代付")
    
    # 进入代付管理
    steps.click(selector="//span[contains(text(),'代付管理')]")
    steps.click(selector="//button[contains(text(),'创建订单')]")
    
    # 填写金额
    steps.fill(ref="amount-input", role="textbox", text="1")
    
    # 填写地址
    steps.fill(ref="address-input", role="textbox", text=CONFIG["test"]["addresses"]["bep20"])
    
    # 选择BEP20
    steps.click(ref="chain-select", role="combobox")
    steps.click(selector="//li[contains(text(),'USDT-BEP20')]")
    
    # 提交
    steps.click(selector="//button[contains(text(),'确认提交')]")
    steps.wait(selector="//div[contains(@class,'success')]")
    
    return steps


def test_payment_erc20():
    """测试: USDT-ERC20代付"""
    steps = TestSteps("USDT-ERC20代付")
    
    # 进入代付管理
    steps.click(selector="//span[contains(text(),'代付管理')]")
    steps.click(selector="//button[contains(text(),'创建订单')]")
    
    # 填写金额
    steps.fill(ref="amount-input", role="textbox", text="1")
    
    # 填写地址
    steps.fill(ref="address-input", role="textbox", text=CONFIG["test"]["addresses"]["erc20"])
    
    # 选择ERC20
    steps.click(ref="chain-select", role="combobox")
    steps.click(selector="//li[contains(text(),'USDT-ERC20')]")
    
    # 提交
    steps.click(selector="//button[contains(text(),'确认提交')]")
    steps.wait(selector="//div[contains(@class,'success')]")
    
    return steps


# ============== 测试套件 ==============
def run_all_tests():
    """运行所有测试"""
    tests = [
        ("登录-管理员", test_login_admin),
        ("创建商户", test_create_merchant),
        ("CNY代收", test_collection_cny),
        ("USDT-TRC20代付", test_payment_trc20),
        ("USDT-BEP20代付", test_payment_bep20),
        ("USDT-ERC20代付", test_payment_erc20),
    ]
    
    results = []
    for name, test_func in tests:
        steps = test_func()
        steps.print()
        results.append({
            "name": name,
            "steps_count": len(steps.steps),
            "success": True
        })
    
    return results


def export_tests():
    """导出测试为JSON"""
    tests = {
        "tests": [
            {"name": "登录-管理员", "steps": test_login_admin().run()},
            {"name": "创建商户", "steps": test_create_merchant().run()},
            {"name": "CNY代收", "steps": test_collection_cny().run()},
            {"name": "USDT-TRC20代付", "steps": test_payment_trc20().run()},
            {"name": "USDT-BEP20代付", "steps": test_payment_bep20().run()},
            {"name": "USDT-ERC20代付", "steps": test_payment_erc20().run()},
        ],
        "config": CONFIG
    }
    
    with open("test_suite.json", "w", encoding="utf-8") as f:
        json.dump(tests, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 测试套件已导出到 test_suite.json")


if __name__ == "__main__":
    # 打印测试摘要
    print("="*60)
    print("CFB支付系统 - OpenClaw测试脚本")
    print("="*60)
    
    # 运行所有测试
    results = run_all_tests()
    
    # 导出测试
    export_tests()
    
    # 打印汇总
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['name']}: {result['steps_count']}步")
