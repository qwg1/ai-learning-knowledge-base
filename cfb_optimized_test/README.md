# CFB支付系统 - 优化后的自动化测试

> 优化点：TOTP自动生成、XPath定位、显式等待

---

## 📊 优化内容

| 优化项 | 优化前 | 优化后 |
|--------|--------|---------|
| TOTP验证码 | 手动/临时安装 | 预装pyotp库 |
| 元素定位 | ref（易失效） | XPath（稳定） |
| 等待方式 | 无等待 | 显式等待 |
| 项目结构 | 19个文件 | 5个文件 |
| 测试时间 | ~5分钟 | ~30秒 |

---

## 📁 文件结构（5个文件）

```
cfb_optimized_test/
├── config.js              # 配置文件
├── totp.py               # TOTP验证码生成器（预装）
├── cfb_test.py            # 自动化测试主程序
├── requirements.txt       # 依赖列表
└── README.md              # 本文档
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pyotp --user
```

### 2. 生成验证码

```bash
python totp.py

# 输出:
# 🔐 种子: 53JN...TXU
# 📟 当前验证码: 347186
# ⏰ 剩余时间: 25秒
```

### 3. 运行测试

```bash
python cfb_test.py
```

---

## 📖 使用方法

### 方法1：命令行生成验证码

```bash
python totp.py
# 输出验证码，直接使用
```

### 方法2：在OpenClaw中执行

```python
# 1. 生成验证码
python totp.py

# 2. 执行登录
browser(action="open", targetUrl="https://test-admin.cfbaopay.com")
browser(action="act", request={"kind": "wait", "selector": "//input[@placeholder='登录账户']", "timeMs": 5000})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='登录账户']", "text": "admin"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='登录密码']", "text": "Aa849956973"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='谷歌验证码']", "text": "验证码"})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'登录')]"})
```

---

## 📋 元素定位（XPath）

### 登录页面

| 元素 | XPath |
|------|-------|
| 用户名输入框 | `//input[@placeholder='登录账户']` |
| 密码输入框 | `//input[@placeholder='登录密码']` |
| 验证码输入框 | `//input[@placeholder='谷歌验证码']` |
| 登录按钮 | `//button[contains(text(),'登录')]` |

### 商户管理页面

| 元素 | XPath |
|------|-------|
| 商户管理菜单 | `//span[contains(text(),'商户管理')]` |
| 新增商户按钮 | `//button[contains(text(),'新增商户')]` |
| 商户名称 | `//input[@placeholder='商户名称']` |
| 商户邮箱 | `//input[@placeholder='商户邮箱']` |
| 商户电话 | `//input[@placeholder='商户电话']` |
| 提交按钮 | `//button[contains(text(),'提交')]` |

### 代付页面

| 元素 | XPath |
|------|-------|
| 代付管理菜单 | `//span[contains(text(),'代付管理')]` |
| 创建订单按钮 | `//button[contains(text(),'创建订单')]` |
| 金额输入框 | `//input[@placeholder='金额']` |
| 链类型选择 | `//input[@placeholder='请选择链类型']` |
| 地址输入框 | `//input[@placeholder='请输入钱包地址']` |
| 确认提交按钮 | `//button[contains(text(),'确认提交')]` |

---

## 🧪 测试用例

### 测试1：登录

```python
browser(action="open", targetUrl="https://test-admin.cfbaopay.com")
browser(action="act", request={"kind": "wait", "selector": "//input[@placeholder='登录账户']", "timeMs": 5000})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='登录账户']", "text": "admin"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='登录密码']", "text": "Aa849956973"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='谷歌验证码']", "text": totp_code()})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'登录')]"})
browser(action="act", request={"kind": "wait", "selector": "//span[contains(text(),'商户管理')]", "timeMs": 5000})
browser(action="screenshot", path="reports/login_success.png")
```

### 测试2：创建商户

```python
browser(action="act", request={"kind": "click", "selector": "//span[contains(text(),'商户管理')]"})
browser(action="act", request={"kind": "wait", "selector": "//table", "timeMs": 5000})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'新增商户')]"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='商户名称']", "text": "测试商户001"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='商户邮箱']", "text": "test@example.com"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='商户电话']", "text": "13800138000"})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'提交')]"})
```

### 测试3：TRC20代付

```python
browser(action="act", request={"kind": "click", "selector": "//span[contains(text(),'代付管理')]"})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'创建订单')]"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='金额']", "text": "1"})
browser(action="act", request={"kind": "click", "selector": "//input[@placeholder='请选择链类型']"})
browser(action="act", request={"kind": "click", "selector": "//li[contains(text(),'USDT-TRC20')]"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='请输入钱包地址']", "text": "TYourAddress"})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'确认提交')]"})
```

---

## 💡 优化要点

### 1. TOTP预装

```python
# 预装pyotp库
pip install pyotp --user

# 使用
python totp.py
# 直接输出验证码
```

### 2. XPath定位

```python
# ✅ 好的方式（稳定）
browser(action="act", request={
    "kind": "click",
    "selector": "//button[contains(text(),'登录')]"
})

# ❌ 避免的方式（易失效）
browser(action="act", request={
    "kind": "click",
    "ref": "e20"
})
```

### 3. 显式等待

```python
# ✅ 好的方式
browser(action="act", request={
    "kind": "wait",
    "selector": "//button[contains(text(),'登录')]",
    "timeMs": 5000
})

# ❌ 避免的方式（没有等待）
browser(action="act", request={"kind": "click", "ref": "e20"})
```

---

## 📦 依赖

```txt
pyotp>=1.6.0
```

---

## 📚 相关文档

- `cfb_agent_browser_test/` - 原始项目（已废弃）
- `cfb_playwright_test/` - Playwright版本（已废弃）

---

*优化时间: 2026-02-11*
