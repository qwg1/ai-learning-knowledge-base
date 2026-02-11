#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - OpenClaw会话测试脚本

直接在OpenClaw会话中运行的测试
用法: 在OpenClaw中执行此脚本，会自动调用browser工具

示例:
> 打开管理后台
> 输入用户名 admin
> 输入密码 xxx
> 点击登录
"""

# ============== 快捷命令 ==============
# 这些命令可以直接在OpenClaw会话中使用

def login_admin():
    """
    管理员登录
    """
    print("""
📝 执行: 管理员登录

步骤:
1. 打开登录页
2. 输入用户名
3. 输入密码
4. 点击登录
""")
    
    # 生成的browser调用
    return [
        {"action": "open", "targetUrl": "https://test-admin.cfbaopay.com/login"},
        {"action": "act", "request": {"kind": "wait", "ref": "username", "role": "textbox"}},
        {"action": "act", "request": {"kind": "type", "ref": "username", "role": "textbox", "text": "your_admin_username"}},
        {"action": "act", "request": {"kind": "type", "ref": "password", "role": "password", "text": "your_admin_password"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'登录')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//span[contains(text(),'商户管理')]"}},
    ]


def create_merchant(name=None, email=None, phone=None):
    """
    创建商户
    """
    import time
    name = name or f"测试商户{int(time.time())[-6:]}"
    email = email or f"test{int(time.time())[-6:]}@example.com"
    phone = phone or "13800138000"
    
    print(f"""
📝 执行: 创建商户
名称: {name}
邮箱: {email}
电话: {phone}

步骤:
1. 进入商户管理
2. 点击新增
3. 填写信息
4. 提交
""")
    
    return [
        # 进入商户管理
        {"action": "act", "request": {"kind": "click", "selector": "//span[contains(text(),'商户管理')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//span[contains(text(),'商户列表')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//table"}},
        
        # 点击新增
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'新增商户')]"}},
        
        # 填写信息
        {"action": "act", "request": {"kind": "type", "ref": "merchant-name", "role": "textbox", "text": name}},
        {"action": "act", "request": {"kind": "type", "ref": "merchant-email", "role": "textbox", "text": email}},
        {"action": "act", "request": {"kind": "type", "ref": "merchant-phone", "role": "textbox", "text": phone}},
        
        # 提交
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'提交')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//div[contains(@class,'success')]"}},
    ]


def collection_cny(amount="1"):
    """
    CNY代收
    """
    print(f"""
📝 执行: CNY代收
金额: {amount}

步骤:
1. 进入代收管理
2. 创建订单
3. 填写金额
4. 选择CNY
5. 提交
""")
    
    return [
        {"action": "act", "request": {"kind": "click", "selector": "//span[contains(text(),'代收管理')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'创建订单')]"}},
        {"action": "act", "request": {"kind": "type", "ref": "amount-input", "role": "textbox", "text": amount}},
        {"action": "act", "request": {"kind": "click", "ref": "coin-type", "role": "combobox"}},
        {"action": "act", "request": {"kind": "click", "selector": "//li[contains(text(),'CNY')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'确认提交')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//div[contains(@class,'success')]"}},
    ]


def payment_trc20(amount="1", address="TYourAddress"):
    """
    USDT-TRC20代付
    """
    print(f"""
📝 执行: USDT-TRC20代付
金额: {amount}
地址: {address}

步骤:
1. 进入代付管理
2. 创建订单
3. 填写金额
4. 填写地址
5. 选择TRC20
6. 提交
""")
    
    return [
        {"action": "act", "request": {"kind": "click", "selector": "//span[contains(text(),'代付管理')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'创建订单')]"}},
        {"action": "act", "request": {"kind": "type", "ref": "amount-input", "role": "textbox", "text": amount}},
        {"action": "act", "request": {"kind": "type", "ref": "address-input", "role": "textbox", "text": address}},
        {"action": "act", "request": {"kind": "click", "ref": "chain-select", "role": "combobox"}},
        {"action": "act", "request": {"kind": "click", "selector": "//li[contains(text(),'USDT-TRC20')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'确认提交')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//div[contains(@class,'success')]"}},
    ]


def payment_bep20(amount="1", address="0xYourAddress"):
    """
    USDT-BEP20代付
    """
    print(f"""
📝 执行: USDT-BEP20代付
金额: {amount}
地址: {address}

步骤:
1. 进入代付管理
2. 创建订单
3. 填写金额
4. 填写地址
5. 选择BEP20
6. 提交
""")
    
    return [
        {"action": "act", "request": {"kind": "click", "selector": "//span[contains(text(),'代付管理')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'创建订单')]"}},
        {"action": "act", "request": {"kind": "type", "ref": "amount-input", "role": "textbox", "text": amount}},
        {"action": "act", "request": {"kind": "type", "ref": "address-input", "role": "textbox", "text": address}},
        {"action": "act", "request": {"kind": "click", "ref": "chain-select", "role": "combobox"}},
        {"action": "act", "request": {"kind": "click", "selector": "//li[contains(text(),'USDT-BEP20')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'确认提交')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//div[contains(@class,'success')]"}},
    ]


def payment_erc20(amount="1", address="0xYourAddress"):
    """
    USDT-ERC20代付
    """
    print(f"""
📝 执行: USDT-ERC20代付
金额: {amount}
地址: {address}

步骤:
1. 进入代付管理
2. 创建订单
3. 填写金额
4. 填写地址
5. 选择ERC20
6. 提交
""")
    
    return [
        {"action": "act", "request": {"kind": "click", "selector": "//span[contains(text(),'代付管理')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'创建订单')]"}},
        {"action": "act", "request": {"kind": "type", "ref": "amount-input", "role": "textbox", "text": amount}},
        {"action": "act", "request": {"kind": "type", "ref": "address-input", "role": "textbox", "text": address}},
        {"action": "act", "request": {"kind": "click", "ref": "chain-select", "role": "combobox"}},
        {"action": "act", "request": {"kind": "click", "selector": "//li[contains(text(),'USDT-ERC20')]"}},
        {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'确认提交')]"}},
        {"action": "act", "request": {"kind": "wait", "selector": "//div[contains(@class,'success')]"}},
    ]


# ============== 完整测试流程 ==============
FULL_TEST_FLOW = """
╔══════════════════════════════════════════════════════╗
║       CFB支付系统 - 完整测试流程                       ║
╚══════════════════════════════════════════════════════╝

📋 测试流程:

1️⃣  管理员登录
    > login_admin()

2️⃣  创建商户
    > create_merchant()

3️⃣  CNY代收
    > collection_cny()

4️⃣  USDT-TRC20代付
    > payment_trc20()

5️⃣  USDT-BEP20代付
    > payment_bep20()

6️⃣  USDT-ERC20代付
    > payment_erc20()

📖 使用方法:
    1. 在OpenClaw会话中
    2. 导入此脚本: import cfb_agent_browser_test.tests as tests
    3. 调用测试函数: tests.login_admin()
    4. 会返回browser工具调用列表
    5. 逐个执行或批量执行
"""


def print_guide():
    """打印使用指南"""
    print(FULL_TEST_FLOW)


# ============== 导出 ==============
__all__ = [
    "login_admin",
    "create_merchant",
    "collection_cny",
    "payment_trc20",
    "payment_bep20",
    "payment_erc20",
    "print_guide",
]

if __name__ == "__main__":
    print_guide()
