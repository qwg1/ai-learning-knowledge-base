# CFB支付系统 - Playwright浏览器自动化测试

> 基于 Playwright 的浏览器自动化测试项目

---

## 📊 系统概述

### 三个系统

| 系统 | URL | 说明 |
|------|-----|------|
| **管理后台** | https://test-admin.cfbaopay.com | 商户管理、通道配置 |
| **代理系统** | https://test-agent.cfbaopay.com | 代理操作 |
| **商户系统** | https://test-merch.cfbaopay.com | 交易操作 |

### 支持的功能

| 功能 | 系统 | 优先级 | 状态 |
|------|------|--------|------|
| **登录** | ALL | P0 | ✅ |
| **开新商户** | admin | P0 | ✅ |
| **配置通道** | admin | P1 | ✅ |
| **绑定通道** | merch | P1 | ✅ |
| **代收** | merch | P0 | ✅ |
| **代付** | merch | P0 | ✅ |
| **补单** | admin | P0 | ⏳ |
| **退款** | admin | P0 | ⏳ |
| **调额** | admin | P1 | ⏳ |
| **商户互转** | admin | P2 | ⏳ |
| **手动归集** | merch | P2 | ⏳ |
| **首页提现** | merch | P2 | ⏳ |

---

## 📁 项目结构

```
cfb_playwright_test/
├── config/
│   └── config.js              # ⭐ 配置文件（敏感）
├── tests/
│   ├── test_login.py          # 登录测试
│   ├── test_merchant.py       # 商户管理测试
│   └── test_trade.py          # 代收代付测试
├── pages/
│   ├── base_page.py           # 页面基类
│   ├── login_page.py          # 登录页面
│   ├── merchant_page.py       # 商户管理页面
│   └── trade_page.py          # 交易管理页面
├── utils/
│   ├── browser.py             # 浏览器管理
│   ├── locator.py             # 元素定位器
│   └── wait.py                # 等待工具
├── docs/
│   └── ANALYSIS.md            # 详细分析
├── .gitignore
├── README.md                  # 本文档
└── requirements.txt           # 依赖列表
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置

```bash
# 编辑配置文件
vim config/config.js

# 填写配置
const CONFIG = {
    systems: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            username: "admin",
            password: "xxx"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            username: "merchant",
            password: "xxx"
        }
    }
};
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个测试
pytest tests/test_login.py -v
pytest tests/test_merchant.py::TestMerchant::test_create_merchant -v
pytest tests/test_trade.py::TestPayment::test_payment_trc20 -v

# 生成HTML报告
pytest tests/ --html=reports/report.html
```

---

## 🎨 元素定位器设计

### 定位器类型

| 类型 | 用法 | 示例 |
|------|------|------|
| ARIA | `page.get_by_aria_label()` | `[ARIA, "username-input"]` |
| Role | `page.get_by_role()` | `[ROLE, "button"]` |
| Text | `page.get_by_text()` | `[TEXT, "登录"]` |
| XPath | `page.locator()` | `[XPATH, "//table//tr"]` |

### 使用示例

```python
from utils.locator import LoginLocators, LocatorFactory

# 点击登录按钮
LocatorFactory.click(page, LoginLocators.LOGIN_BUTTON)

# 输入用户名
LocatorFactory.fill(page, LoginLocators.USERNAME, "admin")

# 获取文本
text = LocatorFactory.text(page, LoginLocators.USERNAME)
```

---

## 🧪 测试用例

### 登录测试

```python
def test_admin_login():
    """
    测试管理员登录
    """
    browser = create_browser_manager()
    browser.start()
    
    page = browser.open_page("admin", "https://test-admin.cfbaopay.com")
    login_page = LoginPage(page, config, url)
    
    success = login_page.login("admin", "password")
    assert success
```

### 商户管理测试

```python
def test_create_merchant():
    """
    测试创建商户
    """
    merchant_info = {
        "name": "测试商户001",
        "email": "test@example.com",
        "phone": "13800138000"
    }
    
    success = merchant_page.create_merchant(merchant_info)
    assert success
```

### 代付测试

```python
def test_payment_trc20():
    """
    测试TRC20代付
    """
    order_info = {
        "amount": "1",
        "chain": "TRC20",
        "address": "TYourAddress"
    }
    
    success = payment_page.create_order(order_info)
    assert success
```

---

## ⚠️ 注意事项

1. **敏感信息**
   - 不要提交 `config/config.js` 到Git
   - 使用环境变量管理密钥

2. **浏览器状态**
   - 自动保存登录状态到 `config/storage_state.json`
   - 状态文件也在`.gitignore`中

3. **测试环境**
   - 仅在 `test` 环境运行
   - 不要在生产环境测试

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `docs/ANALYSIS.md` | 详细分析文档 |
| `cfb_payment_test/` | API测试项目 |

---

## 🔗 GitHub

- **仓库**: github.com/qwg1/ai-learning-knowledge-base
- **路径**: `cfb_playwright_test/`

---

*创建时间: 2026-02-11*
