# CFB+BS 统一项目

## 合并说明

| 原项目 | 功能 | 状态 |
|--------|------|------|
| cfb_complete_test | 浏览器自动化 | ✅ 已合并 |
| bs_payment_test | API测试 | ✅ 已合并 |

## 项目结构

```
cfb_bs_unified/
├── config.js              # 统一配置（浏览器 + API）
├── locator.js             # 元素定位器
├── package.json           # Node.js依赖
├── requirements.txt       # Python依赖
├── README.md              # 文档
├── tests/                 # 浏览器测试
│   ├── admin_login.js     # admin登录
│   ├── merch_login.js     # merch登录
│   ├── collection.js      # 代收
│   └── payout.js          # 代付
├── api/                   # API测试
│   ├── bs_client.py       # API客户端
│   ├── quick_test.py      # 快速测试
│   └── README.md          # API文档
└── reports/               # 测试报告
```

## 使用方法

### 浏览器自动化

```bash
cd cfb_bs_unified
npm test merch_login
```

### API测试

```bash
cd cfb_bs_unified/api
python quick_test.py
```

## 密钥配置

| 密钥 | 配置位置 | 状态 |
|------|---------|------|
| 商户ID | config.js.api.merchant.id | ✅ |
| MD5密钥 | config.js.api.merchant.md5_key | ✅ |
| RSA私钥 | config.js.api.merchant.rsa_private_key | ❌ 需手动填写 |
| RSA公钥 | config.js.api.merchant.rsa_public_key | ❌ 需手动填写 |

## 验证码Key

| 系统 | 商户ID | TOTP种子 |
|------|--------|----------|
| admin | admin | `53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU` |
| merch | 10228 | `53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU` |

---

*合并时间: 2026-02-11*
