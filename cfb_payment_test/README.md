# CFB支付系统 - 自动化测试项目

> 基于 BS-支付系统测试经验的自动化测试框架

---

## 📊 项目概述

### 三个测试系统

| 系统 | URL | 角色 |
|------|-----|------|
| **管理后台** | test-admin.cfbaopay.com | 管理员 |
| **代理系统** | test-agent.cfbaopay.com | 代理商 |
| **商户系统** | test-merch.cfbaopay.com | 商户 |

### 支持的链

| 链类型 | 地址格式 | 用途 |
|--------|----------|------|
| **CNY** | 数字 | 人民币法币 |
| **TRC20** | T开头 | USDT TRON链 |
| **BEP20** | 0x开头 | USDT BSC链 |
| **ERC20** | 0x开头 | USDT ETH链 |

---

## 🎯 功能覆盖

### 核心功能（P0）

| 功能 | 优先级 | 状态 |
|------|--------|------|
| 开新商户 | P0 | ✅ 已实现 |
| 代收 | P0 | ✅ 已实现 |
| 代付（多链） | P0 | ✅ 已实现 |
| 补单 | P0 | ✅ 已实现 |
| 退款 | P0 | ✅ 已实现 |

### 辅助功能（P1）

| 功能 | 优先级 | 状态 |
|------|--------|------|
| 配置通道 | P1 | ✅ 已实现 |
| 绑定通道 | P1 | ✅ 已实现 |
| 调额 | P1 | ✅ 已实现 |
| 商户状态管理 | P1 | ✅ 已实现 |

### 资金功能（P2）

| 功能 | 优先级 | 状态 |
|------|--------|------|
| 商户互转 | P2 | ✅ 已实现 |
| 手动归集 | P2 | ✅ 已实现 |
| 自动归集 | P2 | ✅ 已实现 |
| 首页提现 | P2 | ✅ 已实现 |

---

## 📁 项目结构

```
cfb_payment_test/
├── config/
│   ├── config.js              # ⭐ 配置文件（敏感）
│   └── .gitignore            # Git忽略配置
├── tests/
│   ├── test_merchant.py       # 商户管理测试
│   ├── test_collection.py    # 代收测试（待实现）
│   ├── test_payment.py       # 代付测试（待实现）
│   ├── test_refund.py        # 退款测试（待实现）
│   ├── test_replenish.py     # 补单测试（待实现）
│   └── test_transfer.py       # 转账测试（待实现）
├── utils/
│   ├── auth.py               # 认证模块
│   ├── signature.py          # 签名模块
│   └── api.py                # API客户端
├── docs/
│   └── API.md                # API文档
├── requirements.txt          # 依赖列表
├── README.md                 # 本文档
└── ANALYSIS.md               # 详细分析
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repo_url>
cd cfb_payment_test

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

```bash
# 编辑配置文件
vim config/config.js

# 填写配置
const CONFIG = {
    // 系统URL
    systems: {
        admin: { url: "https://test-admin.cfbaopay.com" },
        agent: { url: "https://test-agent.cfbaopay.com" },
        merch: { url: "https://test-merch.cfbaopay.com" }
    },
    
    // 账户配置
    accounts: {
        admin: { username: "admin", password: "xxx" },
        merchant: { id: "xxx", md5_key: "xxx" }
    }
};
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个模块
pytest tests/test_merchant.py -v

# 生成Allure报告
pytest tests/ --alluredir=reports/
allure serve reports/
```

---

## 📝 测试用例

### 商户管理测试

```python
# 测试创建商户
pytest tests/test_merchant.py::TestMerchant::test_create_merchant -v

# 测试商户配置
pytest tests/test_merchant.py::TestMerchant::test_merchant_config -v

# 测试绑定通道
pytest tests/test_merchant.py::TestMerchant::test_bind_channel -v
```

---

## 🔐 签名算法

### MD5签名

```python
def md5_sign(params, api_key):
    # 1. 过滤空值
    # 2. 排序参数
    # 3. 拼接签名串
    # 4. MD5加密
    return hashlib.md5(sign_str.encode()).hexdigest()
```

### RSA签名

```python
def rsa_sign(params, private_key):
    # 1. 排序参数
    # 2. 拼接签名串
    # 3. RSA私钥签名
    # 4. Base64编码
    return base64.b64encode(signature)
```

---

## ⚠️ 注意事项

1. **敏感信息**
   - 不要提交 `config/config.js` 到Git
   - 使用环境变量管理密钥

2. **测试环境**
   - 仅在 `test` 环境运行
   - 不要在生产环境测试

3. **资金安全**
   - 使用小额测试
   - 测试前确认环境

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `ANALYSIS.md` | 详细分析文档 |
| `bs_payment_test/` | BS支付测试参考 |

---

## 🔗 GitHub

- **仓库**: github.com/qwg1/ai-learning-knowledge-base
- **路径**: `cfb_payment_test/`

---

*创建时间: 2026-02-11*
*基于 BS-支付系统测试经验*
