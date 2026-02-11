# BS支付系统 - API规范速查

> 基于 https://doc.bs123.org/ 文档

---

## 📋 目录

1. [签名规则](#1-签名规则)
2. [USDT代收](#2-usdt代收)
3. [USDT代付](#5-usdt代付)
4. [余额查询](#9-余额查询)
5. [状态码](#状态码)

---

## 1. 签名规则

### MD5签名

```python
# 1. 过滤空值
params = {k: v for k, v in params.items() if v}

# 2. 排序
sorted_keys = sorted(params.keys())

# 3. 拼接
sign_str = "&".join([f"{k}={params[k]}" for k in sorted_keys])
sign_str = f"{sign_str}&key={secret_key}"

# 4. MD5加密
sign = hashlib.md5(sign_str.encode()).hexdigest()
```

### RSA签名

```python
from cryptography libraries import *

# 1. 拼接参数
sign_str = "&".join([f"{k}={params[k]}" for k in sorted(params.keys())])

# 2. RSA私钥签名
signature = private_key.sign(
    sign_str.encode(),
    padding.PKCS1v15(),
    hashes.SHA1()
)

# 3. Base64编码
sign = base64.b64encode(signature).decode()
```

---

## 2. USDT代收

### 请求地址

| 环境 | URL |
|------|-----|
| 正式 | `https://gateway.bishengusdt.com/api/coin/payOrder/create` |
| 测试 | `https://test-gateway.cfbaopay.com/api/coin/payOrder/create` |

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| merchantId | ✅ | 商户ID |
| version | ✅ | 版本号（6.0.0） |
| merchantOrderNo | ✅ | 商户单号（8-30位） |
| amount | ✅ | 订单金额 |
| coinType | ✅ | 订单币种（USDT_TRC20, CNY） |
| callbackCurrencyCode | ✅ | 回调币种（USDT, CNY） |
| notifyUrl | ✅ | 回调通知地址 |
| signType | ❌ | 加密方式（RSA/MD5） |
| sign | ✅ | 签名 |

### 请求示例

```json
{
  "amount": "10",
  "callbackCurrencyCode": "USDT",
  "coinType": "USDT_TRC20",
  "merchantId": "10216",
  "merchantOrderNo": "CZ123456789",
  "notifyUrl": "https://your-callback.com",
  "sign": "xxx",
  "version": "6.0.0"
}
```

### 响应参数

| 参数 | 说明 |
|------|------|
| code | 0=成功，其他=失败 |
| msg | 响应信息 |
| orderNo | 平台单号 |
| bookingAddress | 收款地址 |
| payCoinAmount | 实际支付金额 |
| orderExpireDate | 订单过期时间 |

### 响应示例

```json
{
  "code": "0",
  "msg": "操作成功",
  "orderNo": "CZ202506241839391065350",
  "bookingAddress": "TWNn1GqsodkoyTrYKnc6YkS4TM4JFpy",
  "payCoinAmount": "10",
  "orderExpireDate": "2025-06-24 18:54:39"
}
```

---

## 3. USDT代收订单查询

### 请求地址

`/api/coin/payOrder/query`

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| merchantId | ✅ | 商户ID |
| version | ✅ | 6.0.0 |
| merchantOrderNo | ✅ | 商户单号 |
| submitTime | ✅ | 订单提交时间（yyyyMMddHHmmss） |

### 响应参数

| 参数 | 说明 |
|------|------|
| status | 订单状态（0=处理中,1=成功,2=失败） |
| supplementOrderState | 补单状态（0=未补单,1=待审核,2=审核通过,-1=拒绝） |

---

## 4. USDT代付

### 请求地址

`/api/coin/remitOrder/create`

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| merchantId | ✅ | 商户ID |
| merchantOrderNo | ✅ | 商户单号 |
| amount | ✅ | 订单金额 |
| coinType | ✅ | 订单币种 |
| bookingAddress | ✅ | 收款地址 |
| callbackCurrencyCode | ✅ | 回调币种 |
| notifyUrl | ✅ | 回调地址 |

### 请求示例

```json
{
  "amount": "1",
  "bookingAddress": "TYourAddress",
  "callbackCurrencyCode": "USDT",
  "coinType": "USDT_TRC20",
  "merchantId": "10216",
  "merchantOrderNo": "DF123456789",
  "notifyUrl": "https://your-callback.com",
  "sign": "xxx",
  "version": "6.0.0"
}
```

### 响应参数

| 参数 | 说明 |
|------|------|
| status | 0=处理中,1=成功,2=失败 |
| remitCoinAmount | 出币数量 |

---

## 5. 余额查询

### 请求地址

`/api/coin/balance/query`

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| merchantId | ✅ | 商户ID |
| coinType | ✅ | 币种（USDT） |
| requestTime | ✅ | 请求时间 |

### 响应参数

| 参数 | 说明 |
|------|------|
| availableAmount | 可用金额 |
| frozenAmount | 冻结金额 |
| unsettledAmount | 待结算金额 |

---

## 6. 通道汇率

### 请求地址

`/api/merchant/queryChannelRate`

### 响应参数

| 参数 | 说明 |
|------|------|
| collectionExchangeRate | 代收汇率 |
| paymentExchangeRate | 代付汇率 |

---

## 状态码

### 订单状态

| 值 | 说明 |
|------|------|
| 0 | 处理中 |
| 1 | 成功 |
| 2 | 失败 |

### 补单状态

| 值 | 说明 |
|------|------|
| 0 | 未补单 |
| 1 | 待审核 |
| 2 | 审核通过 |
| -1 | 审核拒绝 |

### API响应码

| 值 | 说明 |
|------|------|
| 0 | 成功 |
| 7 | 订单号已存在 |

---

## 币种

| 币种 | 说明 |
|------|------|
| USDT_TRC20 | TRC20链USDT |
| USDT_BEP20 | BEP20链USDT |
| USDT_ERC20 | ERC20链USDT |
| CNY | 人民币 |

---

*文档创建: 2026-02-11*
