# CFB支付系统 - Playwright浏览器自动化测试

> 分析日期: 2026-02-11
> 工具: Playwright

---

## 🎯 系统概述

### 三个系统URL

| 系统 | URL | 说明 |
|------|-----|------|
| **管理后台** | https://test-admin.cfbaopay.com | 商户管理、通道配置 |
| **代理系统** | https://test-agent.cfbaopay.com | 代理操作 |
| **商户系统** | https://test-merch.cfbaopay.com | 交易操作 |

---

## 📊 需要自动化的功能

### 核心功能（P0）

| 功能 | 系统 | 优先级 | 操作类型 |
|------|------|--------|----------|
| **登录** | ALL | P0 | 输入+点击 |
| **开新商户** | admin | P0 | 表单填写 |
| **配置通道** | admin | P0 | 表单+选择 |
| **绑定通道** | merch | P0 | 选择+确认 |
| **拉单** | admin/merch | P0 | 查询+操作 |
| **代收** | merch | P0 | 表单+提交 |
| **代付** | merch | P0 | 表单+确认 |
| **补单** | admin | P0 | 查询+补录 |
| **退款** | admin | P0 | 查询+退款 |
| **调额** | admin | P0 | 输入+保存 |

### 辅助功能（P1）

| 功能 | 系统 | 操作类型 |
|------|------|----------|
| **商户互转** | admin | 表单+确认 |
| **首页提现** | merch | 点击+确认 |
| **手动归集** | merch | 选择+确认 |

---

## 🔧 技术方案

### 工具选择

| 工具 | 用途 | 优先级 |
|------|------|--------|
| **Playwright** | 浏览器自动化 | ⭐⭐⭐ |
| **agent-browser | 独立CLI管理 | ⭐⭐⭐ |

### 页面元素定位策略

| 方法 | 适用场景 | 优先级 |
|------|----------|--------|
| **ARIA** | 可访问元素 | ⭐⭐⭐ |
| **XPath** | 复杂元素 | ⭐⭐ |
| **CSS选择器** | 简单元素 | ⭐⭐ |
| **文字内容** | 按钮/链接 | ⭐⭐ |

### 操作类型

| 操作 | Playwright方法 |
|------|---------------|
| 点击 | `page.click()` |
| 输入 | `page.fill()` |
| 选择 | `page.select_option()` |
| 上传 | `page.set_input_files()` |
| 等待 | `page.wait_for_selector()` |
| 滚动 | `page.evaluate()` |

---

## 📁 项目结构

```
cfb_playwright_test/
├── config/
│   └── config.js              # 配置文件
├── tests/
│   ├── test_login.py         # 登录测试
│   ├── test_merchant.py       # 商户管理
│   ├── test_channel.py       # 通道配置
│   ├── test_collection.py    # 代收测试
│   ├── test_payment.py       # 代付测试
│   ├── test_order.py         # 订单管理
│   └── test_transfer.py      # 转账测试
├── pages/
│   ├── base_page.py          # 基类
│   ├── login_page.py          # 登录页面
│   ├── admin_page.py         # 管理后台
│   ├── agent_page.py         # 代理系统
│   └── merch_page.py          # 商户系统
├── utils/
│   ├── browser.py            # 浏览器管理
│   ├── locator.py            # 元素定位器
│   └── wait.py               # 等待工具
├── reports/
│   └── test_report.html      # 测试报告
├── README.md
└── requirements.txt
```

---

## 🎨 页面元素定位器设计

### 登录页面

```python
class LoginLocators:
    """登录页面元素定位器"""
    
    USERNAME = [ARIA, "username-input"]
    PASSWORD = [ARIA, "password-input"]
    LOGIN_BUTTON = [TEXT, "登录"]
    VERIFY_CODE = [ARIA, "verify-code"]
    REMEMBER = [ARIA, "remember-me"]
```

### 商户管理页面

```python
class MerchantLocators:
    """商户管理页面元素定位器"""
    
    # 菜单
    MERCHANT_MENU = [TEXT, "商户管理"]
    CREATE_BUTTON = [TEXT, "新增商户"]
    
    # 表单
    MERCHANT_NAME = [ARIA, "merchant-name"]
    MERCHANT_EMAIL = [ARIA, "merchant-email"]
    MERCHANT_PHONE = [ARIA, "merchant-phone"]
    SUBMIT_BUTTON = [TEXT, "提交"]
    CANCEL_BUTTON = [TEXT, "取消"]
    
    # 列表
    MERCHANT_TABLE = [ROLE, "table"]
    STATUS_COLUMN = [ARIA, "status"]
    ACTION_COLUMN = [ARIA, "actions"]
```

### 代收页面

```python
class CollectionLocators:
    """代收页面元素定位器"""
    
    COLLECTION_MENU = [TEXT, "代收管理"]
    CREATE_ORDER = [TEXT, "创建订单"]
    
    # 创建订单表单
    AMOUNT_INPUT = [ARIA, "amount"]
    COIN_TYPE = [ARIA, "coin-type"]
    CNY_OPTION = [TEXT, "CNY"]
    TRC20_OPTION = [TEXT, "USDT-TRC20"]
    BEP20_OPTION = [TEXT, "USDT-BEP20"]
    
    SUBMIT_BUTTON = [TEXT, "确认提交"]
    CANCEL_BUTTON = [TEXT, "取消"]
```

---

## 🧪 测试用例设计

### Test Login

```python
def test_login_admin():
    """
    测试用例: 管理员登录
    优先级: P0
    
    步骤:
    1. 打开管理后台
    2. 输入用户名/密码
    3. 点击登录
    4. 验证登录成功
    
    预期: 进入管理后台首页
    """
```

### Test Create Merchant

```python
def test_create_merchant():
    """
    测试用例: 创建新商户
    优先级: P0
    
    步骤:
    1. 管理员登录
    2. 进入商户管理
    3. 点击新增商户
    4. 填写商户信息
    5. 提交
    6. 验证创建成功
    
    预期: 商户列表显示新商户
    """
```

### Test Collection (CNY)

```python
def test_collection_cny():
    """
    测试用例: CNY代收
    优先级: P0
    
    步骤:
    1. 商户登录
    2. 进入代收页面
    3. 创建代收订单
    4. 填写金额（CNY）
    5. 确认支付
    6. 验证订单创建成功
    
    预期: 订单状态为"待支付"
    """
```

### Test Payment (TRC20)

```python
def test_payment_trc20():
    """
    测试用例: USDT-TRC20代付
    优先级: P0
    
    步骤:
    1. 商户登录
    2. 进入代付页面
    3. 创建代付订单
    4. 选择TRC20链
    5. 填写收款地址（T开头）
    6. 填写金额
    7. 确认提交
    8. 验证订单创建成功
    
    预期: 订单状态为"处理中"
    """
```

### Test Payment (BEP20)

```python
def test_payment_bep20():
    """
    测试用例: USDT-BEP20代付
    优先级: P0
    
    步骤:
    1. 商户登录
    2. 进入代付页面
    3. 创建代付订单
    4. 选择BEP20链
    5. 填写收款地址（0x开头）
    6. 填写金额
    7. 确认提交
    8. 验证订单创建成功
    
    预期: 订单状态为"处理中"
    """
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 配置

```bash
vim config/config.js
```

```javascript
const CONFIG = {
    // 系统配置
    systems: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            username: "admin",
            password: "xxx"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            username: "xxx",
            password: "xxx"
        }
    },
    
    // 浏览器配置
    browser: {
        headless: false,
        timeout: 30000,
        viewport: { width: 1920, height: 1080 }
    },
    
    // 等待配置
    wait: {
        load: 5000,
        click: 1000,
        input: 500
    }
};
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个测试
pytest tests/test_login.py -v

# 生成报告
pytest tests/ --html=reports/report.html
```

---

## ⚠️ 注意事项

### 1. 页面加载

```python
# 等待页面完全加载
page.goto(url)
page.wait_for_load_state("networkidle")

# 等待特定元素
page.wait_for_selector(locator)
```

### 2. iframe处理

```python
# 进入iframe
frame = page.frame_locator(locator)
frame.click(locator)

# 退出iframe
page.frame(None)
```

### 3. 弹窗处理

```python
# 接受弹窗
page.on("dialog", lambda dialog: dialog.accept())

# 拒绝弹窗
page.on("dialog", lambda dialog: dialog.dismiss())
```

### 4. 截图和日志

```python
# 失败截图
if test.failed:
    page.screenshot(path="reports/failed.png")

# 打印日志
page.on("console", lambda msg: print(msg.text))
```

---

## 📝 元素定位最佳实践

### 推荐顺序

```
1. ARIA labels (可访问性)
2. Test IDs (data-testid)
3. Role + name
4. XPath (最后手段)
```

### 避免

```
❌ 绝对 XPath
❌ 索引定位 ([1])
❌ 复杂表达式
❌ 动态ID
```

---

## 🔧 调试技巧

### 1. Playwright Inspector

```bash
playwright codegen https://test-admin.cfbaopay.com
```

### 2. 录制脚本

```bash
# 录制操作生成脚本
playwright codegen --output test.py URL
```

### 3. 截图调试

```python
page.screenshot(path="debug.png", full_page=True)
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `browser_login_sop.md` | 浏览器登录SOP |
| `cfb_payment_test/` | API测试项目 |

---

*创建时间: 2026-02-11*
