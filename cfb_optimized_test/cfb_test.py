#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 优化后的自动化测试

优化点：
1. 预装TOTP库，自动生成验证码
2. 使用XPath定位，解决ref失效问题
3. 显式等待页面加载
4. 合并项目结构，减少冗余
"""

import os
import sys
import time
import json

# ============== 配置 ==============
CONFIG = {
    "systems": {
        "admin": {
            "url": "https://test-admin.cfbaopay.com",
            "username": "admin",
            "password": "Aa849956973",
            "totp_secret": "53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU"
        },
        "merch": {
            "url": "https://test-merch.cfbaopay.com",
            "username": "merchant",
            "password": "xxx"
        }
    },
    
    "paths": {
        "reports": "./reports",
        "cookies": "./config/cookies"
    }
}

# ============== TOTP验证码 ==============
def get_totp_code(secret=None):
    """
    生成TOTP验证码
    
    优先使用pyotp库，如果没有安装则返回None
    
    Args:
        secret: 种子密钥
        
    Returns:
        str: 6位验证码，或None（如果pyotp未安装）
    """
    secret = secret or CONFIG["systems"]["admin"]["totp_secret"]
    
    try:
        import pyotp
        totp = pyotp.TOTP(secret)
        code = totp.now()
        print(f"✅ TOTP验证码: {code}")
        return code
    except ImportError:
        print("❌ pyotp未安装")
        print("💡 安装: pip install pyotp --user")
        return None

# ============== 等待工具 ==============
def wait_for_element(selector, timeout=10):
    """
    等待元素出现
    
    Args:
        selector: XPath选择器
        timeout: 超时时间（秒）
    """
    print(f"⏳ 等待元素: {selector}")
    # 实际使用时，调用browser工具的wait功能
    return True

# ============== 页面操作 ==============
class Page:
    """页面操作类"""
    
    def __init__(self):
        self.current_url = None
        self.actions = []
    
    def open(self, url):
        """打开URL"""
        self.current_url = url
        self.actions.append({
            "action": "open",
            "targetUrl": url
        })
        return {
            "action": "open",
            "targetUrl": url
        }
    
    def click(self, selector):
        """点击元素（XPath）"""
        self.actions.append({
            "action": "act",
            "request": {
                "kind": "click",
                "selector": selector
            }
        })
        return {
            "action": "act",
            "request": {
                "kind": "click",
                "selector": selector
            }
        }
    
    def type(self, selector, text):
        """输入文本"""
        self.actions.append({
            "action": "act",
            "request": {
                "kind": "type",
                "selector": selector,
                "text": text
            }
        })
        return {
            "action": "act",
            "request": {
                "kind": "type",
                "selector": selector,
                "text": text
            }
        }
    
    def wait(self, selector, time_ms=3000):
        """等待元素"""
        self.actions.append({
            "action": "act",
            "request": {
                "kind": "wait",
                "selector": selector,
                "timeMs": time_ms
            }
        })
        return {
            "action": "act",
            "request": {
                "kind": "wait",
                "selector": selector,
                "timeMs": time_ms
            }
        }
    
    def screenshot(self, name):
        """截图"""
        return {
            "action": "screenshot",
            "path": f"{CONFIG['paths']['reports']}/{name}.png"
        }
    
    def snapshot(self):
        """获取页面快照"""
        return {
            "action": "snapshot"
        }

# ============== 测试用例 ==============
class LoginTest:
    """登录测试"""
    
    def __init__(self):
        self.page = Page()
        self.config = CONFIG["systems"]["admin"]
    
    def run(self):
        """执行登录测试"""
        print("\n" + "="*60)
        print("📝 测试: 管理员登录")
        print("="*60)
        
        # 1. 打开登录页
        print("\n1️⃣ 打开登录页...")
        self.page.open(self.config["url"])
        
        # 2. 等待登录表单
        print("2️⃣ 等待登录表单...")
        self.page.wait("//input[@placeholder='登录账户']", 5000)
        
        # 3. 输入用户名
        print("3️⃣ 输入用户名...")
        self.page.type("//input[@placeholder='登录账户']", self.config["username"])
        
        # 4. 输入密码
        print("4️⃣ 输入密码...")
        self.page.type("//input[@placeholder='登录密码']", self.config["password"])
        
        # 5. 获取TOTP验证码
        print("5️⃣ 获取验证码...")
        totp_code = get_totp_code(self.config["totp_secret"])
        if totp_code:
            self.page.type("//input[@placeholder='谷歌验证码']", totp_code)
        else:
            print("⚠️ 手动输入验证码")
        
        # 6. 点击登录
        print("6️⃣ 点击登录...")
        self.page.click("//button[contains(text(),'登录')]")
        
        # 7. 等待首页加载
        print("7️⃣ 等待首页...")
        self.page.wait("//span[contains(text(),'商户管理')]", 5000)
        
        # 8. 截图验证
        print("8️⃣ 截图验证...")
        self.page.screenshot("login_success")
        
        return self.page.actions


class MerchantTest:
    """商户管理测试"""
    
    def __init__(self):
        self.page = Page()
        self.config = CONFIG["systems"]["admin"]
    
    def run(self):
        """执行商户管理测试"""
        print("\n" + "="*60)
        print("📝 测试: 商户管理")
        print("="*60)
        
        # 1. 进入商户管理
        print("1️⃣ 进入商户管理...")
        self.page.click("//span[contains(text(),'商户管理')]")
        
        # 2. 等待商户列表
        print("2️⃣ 等待商户列表...")
        self.page.wait("//table", 5000)
        
        # 3. 点击新增
        print("3️⃣ 点击新增商户...")
        self.page.click("//button[contains(text(),'新增商户')]")
        
        # 4. 填写商户信息
        import time
        merchant_no = str(int(time.time()))[-6:]
        print(f"4️⃣ 填写商户信息...")
        self.page.type("//input[@placeholder='商户名称']", f"测试商户{merchant_no}")
        self.page.type("//input[@placeholder='商户邮箱']", f"test{merchant_no}@example.com")
        self.page.type("//input[@placeholder='商户电话']", "13800138000")
        
        # 5. 提交
        print("5️⃣ 提交...")
        self.page.click("//button[contains(text(),'提交')]")
        
        return self.page.actions


class PaymentTest:
    """代付测试"""
    
    def __init__(self, chain="TRC20"):
        self.page = Page()
        self.config = CONFIG["systems"]["admin"]
        self.chain = chain
    
    def run(self):
        """执行代付测试"""
        print("\n" + "="*60)
        print(f"📝 测试: USDT-{self.chain}代付")
        print("="*60)
        
        # 1. 进入代付管理
        print("1️⃣ 进入代付管理...")
        self.page.click("//span[contains(text(),'代付管理')]")
        
        # 2. 点击创建
        print("2️⃣ 点击创建订单...")
        self.page.click("//button[contains(text(),'创建订单')]")
        
        # 3. 填写订单信息
        print("3️⃣ 填写订单信息...")
        self.page.type("//input[@placeholder='金额']", "1")
        
        # 4. 选择链类型
        print(f"4️⃣ 选择{self.chain}...")
        self.page.click("//input[@placeholder='请选择链类型']")
        self.page.click(f"//li[contains(text(),'USDT-{self.chain}')]")
        
        # 5. 填写地址
        print("5️⃣ 填写地址...")
        addresses = {
            "TRC20": "TYourAddress",
            "BEP20": "0xYourAddress",
            "ERC20": "0xYourAddress"
        }
        self.page.type("//input[@placeholder='请输入钱包地址']", addresses.get(self.chain, ""))
        
        # 6. 提交
        print("6️⃣ 提交...")
        self.page.click("//button[contains(text(),'确认提交')]")
        
        return self.page.actions


# ============== 主程序 ==============
def main():
    """主程序"""
    print("""
╔══════════════════════════════════════════════════════╗
║     CFB支付系统 - 优化后的自动化测试            ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # 检查TOTP
    print("\n🔍 检查TOTP验证码...")
    code = get_totp_code()
    if code:
        print(f"✅ TOTP可用: {code}")
    else:
        print("❌ TOTP不可用，需要手动安装")
    
    # 显示配置
    print(f"""
📋 配置信息:
   系统: {CONFIG['systems']['admin']['url']}
   用户: {CONFIG['systems']['admin']['username']}
   TOTP: {CONFIG['systems']['admin']['totp_secret'][:4]}...{CONFIG['systems']['admin']['totp_secret'][-4:]}
    """)
    
    # 测试选项
    print("""
📝 测试选项:
   1. 登录测试
   2. 商户管理测试
   3. 代付测试(TRC20)
   4. 代付测试(BEP20)
   5. 代付测试(ERC20)
   6. 全部测试
    """)
    
    # 显示生成的actions（供OpenClaw使用）
    print("\n📖 使用方法:")
    print("   1. 在OpenClaw中执行browser工具")
    print("   2. 按照actions列表顺序执行")
    print("   3. 每个action是一个browser调用")
    
    return {
        "status": "ready",
        "config": CONFIG,
        "totp_available": code is not None
    }


if __name__ == "__main__":
    main()
