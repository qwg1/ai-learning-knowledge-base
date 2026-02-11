# API测试

## 使用方法

```bash
cd cfb_bs_unified/api

# 安装依赖
pip install requests cryptography

# 运行测试
python quick_test.py
```

## 密钥配置

编辑 `config.py` 中的 `merchant` 配置：

```python
"merchant": {
    "id": "10228",
    "md5_key": "d7fdce63f5c74621a1877d6c7e3d43a2",  # 从商户后台获取
    "rsa_private_key": "-----BEGIN RSA PRIVATE KEY-----...",  # 手动填写
    "rsa_public_key": "-----BEGIN PUBLIC KEY-----..."  # 手动填写
}
```

## 测试功能

| 功能 | 状态 |
|------|------|
| 余额查询 | ✅ |
| 代收下单 | ⏳ |
| 代付下单 | ⏳ |
| 订单查询 | ⏳ |
