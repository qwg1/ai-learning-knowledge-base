# BS支付系统 - API测试项目

> 基于 https://doc.bs123.org/ API文档的完整测试项目

---

## 📋 功能支持

| 模块 | 功能 | 状态 |
|------|------|------|
| USDT代收 | 下单（接口模式） | ✅ |
| USDT代收 | 下单（收银台模式） | ✅ |
| USDT代收 | 订单查询 | ✅ |
| USDT代付 | 下单 | ✅ |
| USDT代付 | 订单查询 | ✅ |
| 余额查询 | USDT余额 | ✅ |
| 通道汇率 | 查询汇率 | ✅ |
| 闪付 | 获取用户地址 | ✅ |
| CNY代付 | 下单 | ✅ |
| CNY代付 | 订单查询 | ✅ |
| 签名 | MD5签名 | ✅ |
| 签名 | RSA签名 | ✅ |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd bs_payment_test
pip install requests cryptography
```

### 2. 配置商户信息

编辑 `config.js` 或直接修改 `bs_api_client.py` 中的配置：

```javascript
// config.js
module.exports = {
    env: "test",  // test 或 production
    
    merchant: {
        id: "10216",              // 商户ID
        md5_key: "",             // MD5密钥
        rsa_private_key: "",      // RSA私钥
        r ""        // RSA公sa_public_key:钥（平台公钥）
    },
    
    notify_url: "https://your-callback.com/callback"
};
```

### 3. 运行测试

```bash
# 全部测试
python bs_api_client.py

# 仅代收测试
python bs_api_client.py --test collection

# 仅代付测试
python bs_api_client.py --test remit

# 仅余额查询
python bs_api_client.py --test balance
```

---

## 📁 项目结构

```
bs_payment_test/
├── README.md              # 本文档
├── bs_api_client.py      # API客户端（主程序）
├── package.json          # Node.js配置
├── requirements.txt      # Python依赖
├── config.js             # 配置文件（可选）
└── docs/                # 文档
    └── API_SPEC.md      # API规范参考
```

---

## 💻 使用示例

### Python

```python
from bs_api_client import BSClient, BSTestCases

# 创建客户端
client = BSClient("test")

# USDT代收
result = client.create_collection_order(
    amount="10",
    coin_type="USDT_TRC20",
    callback_currency_code="USDT"
)
print(result)

# USDT代付
result = client.create_remit_order(
    amount="1",
    coin_type="USDT_TRC20",
    booking_address="TYourAddress",
    callback_currency_code="USDT"
)
print(result)

# 余额查询
result = client.query_balance("USDT")
print(result)
```

### 命令行

```bash
# 代收测试
python bs_api_client.py --test collection

# 代付测试
python bs_api_client.py --test remit

# 余额查询
python bs_api_client.py --test balance
```

---

## 📖 API文档

### 基础URL

| 环境 | URL |
|------|-----|
| 正式环境 | `https://gateway.bishengusdt.com` |
| 测试环境 | `https://test-gateway.cfbaopay.com` |

### USDT代收

```python
# 接口模式
client.create_collection_order(
    amount="10",
    coin_type="USDT_TRC20",      # 或 CNY
    callback_currency_code="USDT",  # 或 CNY
    notify_url="https://..."
)

# 收银台模式
client.create_collection_order_cashier(
    amount="10",
    coin_type="USDT_TRC20",
    callback_currency_code="USDT",
    language="zh"  # en, zh, jp, th, etc.
)
```

### USDT代付

```python
client.create_remit_order(
    amount="1",
    coin_type="USDT_TRC20",
    booking_address="TYourAddress",
    callback_currency_code="USDT"
)
```

### 订单查询

```python
# 代收订单查询
client.query_collection_order("CZ123456789")

# 代付订单查询
client.query_remit_order("DF123456789")
```

### 余额查询

```python
client.query_balance("USDT")
```

### 通道汇率

```python
client.query_channel_rate("USDT_TRC20")
```

---

## 🔧 签名规则

### MD5签名

```python
from bs_api_client import Signer

sign = Signer.md5_sign(
    params={"amount": "10", "merchantId": "10216"},
    secret_key="your_md5_key"
)
```

### RSA签名

```python
sign = Signer.rsa_sign(
    params={"amount": "10", "merchantId": "10216"},
    private_key="your_rsa_private_key"
)
```

---

## 📝 订单状态

### 代收订单状态

| status | 说明 |
|--------|------|
| 0 | 处理中 |
| 1 | 成功 |
| 2 | 失败 |

### 代付订单状态

| status | 说明 |
|--------|------|
| 0 | 处理中 |
| 1 | 成功 |
| 2 | 失败 |

---

## ⚠️ 注意事项

1. **商户配置**: 需在代码中配置正确的商户ID和密钥
2. **签名**: 请求需要正确的签名（MD5或RSA）
3. **回调**: 需配置有效的回调地址接收通知
4. **订单号**: 订单号长度8-30位，建议包含时间戳
5. **金额**: 最多支持两位小数

---

## 📚 相关链接

- API文档: https://doc.bs123.org/
- 密钥生成: https://www.bejson.com/enc/rsa/

---

*创建时间: 2026-02-11*
