# CFB支付系统 - agent-browser 自动化测试

> 使用 OpenClaw browser 工具
> 分析日期: 2026-02-11

---

## 🎯 系统概述

### 三个系统

| 系统 | URL | 说明 |
|------|-----|------|
| **管理后台** | https://test-admin.cfbaopay.com | 商户管理、通道配置 |
| **代理系统** | https://test-agent.cfbaopay.com | 代理操作 |
| **商户系统** | https://test-merch.cfbaopay.com | 交易操作 |

---

## 📊 功能清单

| 功能 | 系统 | 优先级 | 状态 |
|------|------|--------|------|
| **登录** | ALL | P0 | ✅ |
| **开新商户** | admin | P0 | ✅ |
| **配置通道** | admin | P1 | ⏳ |
| **绑定通道** | merch | P1 | ⏳ |
| **代收** | merch | P0 | ✅ |
| **代付** | merch | P0 | ✅ |
| **补单** | admin | P0 | ⏳ |
| **退款** | admin | P0 | ⏳ |
| **调额** | admin | P1 | ⏳ |
| **商户互转** | admin | P2 | ⏳ |
| **手动归集** | merch | P2 | ⏳ |

---

## 🔧 OpenClaw browser 工具使用

### 可用操作

| 操作 | 说明 | 示例 |
|------|------|------|
| `open` | 打开URL | `{"action":"open","targetUrl":"..."}` |
| `screenshot` | 截图 | `{"action":"screenshot"}` |
| `snapshot` | 获取页面快照 | `{"action":"snapshot"}` |
| `act` | 执行操作 | `{"action":"act","request":{"kind":"click","ref":"..."}}` |
| `navigate` | 导航 | `{"action":"navigate","targetUrl":"..."}` |

### 元素定位

| 类型 | 用法 | 示例 |
|------|------|------|
| ARIA | `{"ref":"...","role":"button"}` | `{"ref":"login-btn","role":"button"}` |
| Text | `{"ref":"...","role":"textbox"}` | `{"ref":"username","role":"textbox"}` |
| XPath | `{"selector":"..."}` | `{"selector":"//button[text()='登录']"}` |

---

## 📁 项目结构

```
cfb_agent_browser_test/
├── config/
│   └── config.js              # 配置文件
├── tests/
│   ├── test_login.py         # 登录测试
│   ├── test_merchant.py      # 商户管理测试
│   ├── test_trade.py         # 代收代付测试
│   └── conftest.py           # pytest配置
├── pages/
│   ├── base_page.py          # 页面基类
│   ├── login_page.py          # 登录页面
│   ├── admin_page.py          # 管理后台
│   └── merch_page.py          # 商户系统
├── utils/
│   ├── browser.py            # 浏览器封装
│   └── config.py              # 配置管理
├── README.md
└── requirements.txt
```

---

## 🎨 元素定位设计

### 登录页面

```python
LOGIN = {
    "username": {"ref": "username", "role": "textbox"},
    "password": {"ref": "password", "role": "textbox"},
    "login_btn": {"ref": "login-btn", "role": "button"}
}
```

### 商户管理页面

```python
MERCHANT = {
    "menu": {"ref": "merchant-menu", "role": "link"},
    "create_btn": {"ref": "create-merchant", "role": "button"},
    "name_input": {"ref": "merchant-name", "role": "textbox"},
    "submit_btn": {"ref": "submit", "role": "button"}
}
```

### 代收页面

```python
COLLECTION = {
    "menu": {"ref": "collection", "role": "link"},
    "amount": {"ref": "amount-input", "role": "textbox"},
    "coin_type": {"ref": "coin-type", "role": "combobox"},
    "submit": {"ref": "submit-order", "role": "button"}
}
```

---

## 🧪 测试用例设计

### Test Login

```python
def test_login_admin():
    """
    测试: 管理员登录
    优先级: P0
    
    步骤:
    1. 打开管理后台
    2. 输入用户名/密码
    3. 点击登录
    4. 验证登录成功
    """
```

### Test Create Merchant

```python
def test_create_merchant():
    """
    测试: 创建新商户
    优先级: P0
    
    步骤:
    1. 管理员登录
    2. 进入商户管理
    3. 点击新增商户
    4. 填写商户信息
    5. 提交
    6. 验证创建成功
    """
```

### Test Collection CNY

```python
def test_collection_cny():
    """
    测试: CNY代收
    优先级: P0
    
    步骤:
    1. 商户登录
    2. 进入代收页面
    3. 创建代收订单
    4. 填写金额(CNY)
    5. 确认
    """
```

### Test Payment TRC20

```python
def test_payment_trc20():
    """
    测试: USDT-TRC20代付
    优先级: P0
    
    步骤:
    1. 商户登录
    2. 进入代付页面
    3. 选择TRC20链
    4. 填写收款地址(T开头)
    5. 填写金额
    6. 确认提交
    """
```

### Test Payment BEP20

```python
def test_payment_bep20():
    """
    测试: USDT-BEP20代付
    优先级: P0
    
    步骤:
    1. 商户登录
    2. 进入代付页面
    3. 选择BEP20链
    4. 填写收款地址(0x开头)
    5. 填写金额
    6. 确认提交
    """
```

---

## 🚀 快速开始

### 1. 配置

```javascript
// config/config.js
const CONFIG = {
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
    test: {
        amounts: {
            min: "0.01",
            normal: "1"
        },
        addresses: {
            trc20: "TYourAddress",
            bep20: "0xYourAddress",
            erc20: "0xYourAddress"
        }
    }
};
```

### 2. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个测试
pytest tests/test_login.py -v
pytest tests/test_merchant.py::test_create_merchant -v
```

---

## 📝 页面操作封装

### Browser工具封装

```python
class BrowserHelper:
    """OpenClaw browser工具封装"""
    
    def __init__(self):
        self.context = None
    
    def open(self, url: str):
        """打开URL"""
        browser(action="open", targetUrl=url)
    
    def click(self, ref: str, role: str = "button"):
        """点击元素"""
        browser(
            action="act",
            request={
                "kind": "click",
                "ref": ref,
                "role": role
            }
        )
    
    def fill(self, ref: str, value: str, role: str = "textbox"):
        """输入文本"""
        browser(
            action="act",
            request={
                "kind": "type",
                "ref": ref,
                "role": role,
                "text": value
            }
        )
    
    def screenshot(self, name: str):
        """截图"""
        browser(action="screenshot", path=f"reports/{name}.png")
    
    def snapshot(self):
        """获取页面快照"""
        browser(action="snapshot")
```

---

## ⚠️ 注意事项

### 1. 元素定位

```python
# 使用ARIA ref定位（推荐）
{"ref": "login-btn", "role": "button"}

# 使用文字内容定位
{"selector": "//button[contains(text(),'登录')]"}

# 使用XPath
{"selector": "//input[@name='username']"}
```

### 2. 等待

```python
# 等待元素出现
browser(action="act", request={"kind": "wait", "ref": "..."})

# 等待时间
import time
time.sleep(1)
```

### 3. 截图和日志

```python
# 失败截图
if test.failed:
    browser(action="screenshot", path=f"reports/{test.name}.png")

# 获取页面快照
browser(action="snapshot")
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `browser_login_sop.md` | 浏览器登录SOP |
| `cfb_playwright_test/` | Playwright项目参考 |

---

*创建时间: 2026-02-11*
*使用 OpenClaw browser 工具*
