# CFB支付系统 - agent-browser 自动化测试

> 使用 OpenClaw browser 工具
> 分析日期: 2026-02-11

---

## 📊 系统概述

### 三个系统

| 系统 | URL | 说明 |
|------|-----|------|
| **管理后台** | https://test-admin.cfbaopay.com | 商户管理、通道配置 |
| **代理系统** | https://test-agent.cfbaopay.com | 代理操作 |
| **商户系统** | https://test-merch.cfbaopay.com | 交易操作 |

---

## 📁 项目结构

```
cfb_agent_browser_test/
├── config/
│   └── config.js              # 配置文件
├── tests/
│   ├── __init__.py            # 测试命令
│   └── test_runner.py         # 测试运行器
├── pages/
│   ├── base_page.py           # 页面操作类
│   └── locator.py            # 元素定位器
├── README.md                  # 本文档
└── requirements.txt           # 依赖列表
```

---

## 🚀 快速使用

### 1. 配置

```javascript
// config/config.js
const CONFIG = {
    systems: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            username: "your_admin_username",
            password: "your_admin_password"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            username: "your_merchant_username",
            password: "your_merchant_password"
        }
    },
    test: {
        amounts: { min: "0.01", normal: "1" },
        addresses: {
            trc20: "TYourAddress",
            bep20: "0xYourAddress",
            erc20: "0xYourAddress"
        }
    }
};
```

### 2. 运行测试

在OpenClaw会话中直接使用：

```python
# 导入测试
import sys
sys.path.insert(0, 'cfb_agent_browser_test')
from tests import *

# 执行测试
steps = login_admin()      # 管理员登录
steps = create_merchant()  # 创建商户
steps = collection_cny()   # CNY代收
steps = payment_trc20()   # USDT-TRC20代付
steps = payment_bep20()    # USDT-BEP20代付
steps = payment_erc20()    # USDT-ERC20代付
```

### 3. 执行browser调用

每个测试函数会返回browser工具调用列表，例如：

```python
login_admin() 返回:
[
    {"action": "open", "targetUrl": "https://test-admin.cfbaopay.com/login"},
    {"action": "act", "request": {"kind": "wait", "ref": "username", "role": "textbox"}},
    {"action": "act", "request": {"kind": "type", "ref": "username", "role": "textbox", "text": "admin"}},
    {"action": "act", "request": {"kind": "type", "ref": "password", "role": "password", "text": "xxx"}},
    {"action": "act", "request": {"kind": "click", "selector": "//button[contains(text(),'登录')]"}},
]
```

然后在OpenClaw中逐个执行这些调用。

---

## 🎯 已实现功能

| 功能 | 系统 | 优先级 | 状态 |
|------|------|--------|------|
| **登录** | ALL | P0 | ✅ |
| **开新商户** | admin | P0 | ✅ |
| **代收** | merch | P0 | ✅ |
| **代付 TRC20** | merch | P0 | ✅ |
| **代付 BEP20** | merch | P0 | ✅ |
| **代付 ERC20** | merch | P0 | ✅ |
| 配置通道 | admin | P1 | ⏳ |
| 绑定通道 | merch | P1 | ⏳ |
| 补单 | admin | P0 | ⏳ |
| 退款 | admin | P0 | ⏳ |
| 调额 | admin | P1 | ⏳ |
| 商户互转 | admin | P2 | ⏳ |
| 手动归集 | merch | P2 | ⏳ |

---

## 📝 元素定位

### 定位器格式

```python
# ARIA ref定位（推荐）
{"ref": "username", "role": "textbox"}

# XPath定位
{"selector": "//button[contains(text(),'登录')]"}

# 组合使用
{"selector": "//span[contains(text(),'商户管理')]", "role": "link"}
```

### 常用定位

| 元素 | 定位器 |
|------|--------|
| 用户名输入框 | `{"ref": "username", "role": "textbox"}` |
| 密码输入框 | `{"ref": "password", "role": "password"}` |
| 登录按钮 | `{"selector": "//button[contains(text(),'登录')]"}` |
| 商户管理菜单 | `{"selector": "//span[contains(text(),'商户管理')]"}` |
| 新增商户按钮 | `{"selector": "//button[contains(text(),'新增商户')]"}` |
| 金额输入框 | `{"ref": "amount-input", "role": "textbox"}` |
| 币种选择 | `{"ref": "coin-type", "role": "combobox"}` |
| 链选择 | `{"ref": "chain-select", "role": "combobox"}` |
| 提交按钮 | `{"selector": "//button[contains(text(),'确认提交')]"}` |

---

## 🧪 测试命令

### 登录测试

```python
from cfb_agent_browser_test.tests import login_admin

# 执行登录
steps = login_admin()
# 返回browser调用列表
```

### 商户测试

```python
from cfb_agent_browser_test.tests import create_merchant

# 创建商户
steps = create_merchant(
    name="测试商户001",
    email="test@example.com",
    phone="13800138000"
)
```

### 代收测试

```python
from cfb_agent_browser_test.tests import collection_cny

# CNY代收
steps = collection_cny(amount="1")
```

### 代付测试

```python
from cfb_agent_browser_test.tests import payment_trc20, payment_bep20, payment_erc20

# TRC20代付
steps = payment_trc20(amount="1", address="TYourAddress")

# BEP20代付
steps = payment_bep20(amount="1", address="0xYourAddress")

# ERC20代付
steps = payment_erc20(amount="1", address="0xYourAddress")
```

---

## 📖 OpenClaw使用示例

```
OpenClaw会话:

1. 导入测试模块
> import sys
> sys.path.insert(0, 'cfb_agent_browser_test')
> from tests import *

2. 执行登录
> steps = login_admin()
> # 逐个执行browser调用
> browser(action="open", targetUrl="https://test-admin.cfbaopay.com/login")
> browser(action="act", request={"kind": "wait", "ref": "username", "role": "textbox"})
> ...

3. 执行创建商户
> steps = create_merchant()
> for step in steps:
>     browser(**step)

4. 截图验证
> browser(action="screenshot", path="reports/merchant_created.png")
```

---

## ⚠️ 注意事项

1. **配置敏感信息**
   - 不要提交 `config/config.js` 到Git
   - 使用环境变量管理密码

2. **测试环境**
   - 仅在 `test` 环境运行
   - 不要在生产环境测试

3. **元素定位**
   - 优先使用ARIA ref
   - XPath作为备选
   - 避免绝对XPath

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `browser_login_sop.md` | 浏览器登录SOP |
| `cfb_playwright_test/` | Playwright项目参考 |
| `cfb_payment_test/` | API测试项目 |

---

## 🔗 GitHub

- **仓库**: github.com/qwg1/ai-learning-knowledge-base
- **路径**: `cfb_agent_browser_test/`

---

*创建时间: 2026-02-11*
*使用 OpenClaw browser 工具*
