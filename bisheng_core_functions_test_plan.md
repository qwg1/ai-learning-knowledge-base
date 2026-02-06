# 币圣系统核心功能自动化测试方案

## 概述
基于币圣系统API文档，制定针对拉单、TRC/BEP、代收/代付、补单、调额、商户互转、商户后台提现等核心功能的自动化测试方案。

## 测试功能列表

### 1. USDT代收功能测试（接口模式和收银台模式）
- **TRC20代收**：测试USDT_TRC20代收功能
- **BEP20代收**：如系统支持，测试BEP20代收功能
- **法币代收**：测试CNY等法币通过汇率转换为USDT代收
- **订单查询**：验证代收订单查询功能
- **回调通知**：验证代收回调功能

### 2. USDT代付功能测试
- **TRC20代付**：测试USDT_TRC20代付功能
- **BEP20代付**：如系统支持，测试BEP20代付功能
- **法币代付**：测试CNY等法币代付功能
- **代付查询**：验证代付订单查询功能
- **代付回调**：验证代付认调功能

### 3. 拉单功能测试
- **批量订单查询**：测试大量订单数据拉取
- **分页拉单**：验证分页拉取功能
- **实时拉单**：测试实时订单获取功能

### 4. 补单功能测试
- **补单状态验证**：测试补单状态（0未补单、1待审核、2审核通过、-1审核拒绝）
- **补单金额验证**：验证补单金额准确性
- **补单审核流程**：测试补单审核流程

### 5. 调额功能测试
- **余额查询**：测试余额查询功能（可用金额、冻结金额、待结算金额）
- **额度调整**：如系统支持，测试额度调整功能

### 6. 商户互转功能测试
- **转账功能**：测试商户间资金转移功能
- **转账记录查询**：验证转账记录查询功能

### 7. 商户后台提现功能测试
- **CNY-API代付**：测试银行卡代付功能
- **银行编码验证**：验证不同银行编码的处理
- **代付订单查询**：验证CNY代付订单查询功能

## 详细测试用例

### USDT代收功能测试

#### 代收下单（接口模式）
```javascript
// 测试用例：TRC20代收下单
async function testTRC20PayOrder() {
  const params = {
    merchantId: "10216",
    version: "6.0.0",
    merchantOrderNo: `CZ${Date.now()}`,
    amount: "10",
    coinType: "USDT_TRC20",
    callbackCurrencyCode: "USDT",
    notifyUrl: "https://test-callback.example.com",
    signType: "RSA"
  };
  
  // 添加签名逻辑
  const signedParams = addSign(params);
  
  const response = await post('/api/coin/payOrder/create', signedParams);
  
  // 验证响应
  assert(response.code === "0");
  assert(response.bookingAddress);
  assert(response.orderExpireDate);
  
  return response;
}
```

#### 代收下单（收银台模式）
```javascript
// 测试用例：收银台模式代收
async function testCashierPayOrder() {
  const params = {
    merchantId: "10216",
    version: "6.0.0",
    merchantOrderNo: `CZ${Date.now()}`,
    amount: "10",
    coinType: "USDT_TRC20",
    callbackCurrencyCode: "USDT",
    notifyUrl: "https://test-callback.example.com",
    language: "en",
    signType: "RSA"
  };
  
  const signedParams = addSign(params);
  
  const response = await post('/api/coin/cashier/create', signedParams);
  
  // 验证响应
  assert(response.code === "0");
  assert(response.payUrl);
  
  return response;
}
```

### USDT代付功能测试

#### 代付下单
```javascript
// 测试用例：TRC20代付下单
async function testTRC20RemitOrder() {
  const params = {
    merchantId: "10216",
    version: "6.0.0",
    merchantOrderNo: `DF${Date.now()}`,
    amount: "5",
    coinType: "USDT_TRC20",
    bookingAddress: "TBCwRrYLeBi9GZqDdeAiDToXzx12345678",
    callbackCurrencyCode: "USDT",
    notifyUrl: "https://test-callback.example.com",
    signType: "RSA"
  };
  
  const signedParams = addSign(params);
  
  const response = await post('/api/coin/remitOrder/create', signedParams);
  
  // 验证响应
  assert(response.code === "0");
  assert(response.status === "0"); // 0为处理中
  
  return response;
}
```

### 拉单功能测试

#### 批量订单查询
```javascript
// 测试用例：批量拉取代收订单
async function testPullPayOrders() {
  // 查询最近的多个订单
  const orders = [];
  for(let i = 0; i < 10; i++) {
    const params = {
      merchantId: "10216",
      version: "6.0.0",
      merchantOrderNo: `CZ${Date.now()}-${i}`,
      submitTime: formatDate(new Date(), 'yyyyMMddHHmmss'),
      signType: "RSA"
    };
    
    const signedParams = addSign(params);
    const response = await post('/api/coin/payOrder/query', signedParams);
    orders.push(response);
  }
  
  return orders;
}
```

### 余额查询功能测试

#### 余额查询
```javascript
// 测试用例：余额查询
async function testBalanceQuery() {
  const params = {
    merchantId: "80008",
    version: "6.0.0",
    requestTime: formatDate(new Date(), 'yyyyMMddHHmmss'),
    coinType: "USDT",
    signType: "RSA"
  };
  
  const signedParams = addSign(params);
  
  const response = await post('/api/coin/balance/query', signedParams);
  
  // 验证响应
  assert(response.code === "0");
  assert(typeof response.availableAmount !== 'undefined');
  assert(typeof response.frozenAmount !== 'undefined');
  assert(typeof response.unsettledAmount !== 'undefined');
  
  return response;
}
```

### CNY代付功能测试

#### CNY代付下单
```javascript
// 测试用例：CNY银行卡代付
async function testCNYRemitOrder() {
  const params = {
    merchantId: "10117",
    version: "1.0.0",
    merchantOrderNo: `test${Date.now()}`,
    amount: "100.00",
    bankCode: "ABC",  // 农业银行
    bankcardAccountNo: "6289990729793741",
    bankcardAccountName: "测试用户",
    memberNo: `user_${Date.now()}`,
    notifyUrl: "https://test-callback.example.com"
  };
  
  const signedParams = addSign(params);
  
  const response = await post('/api/remitMatchOrder/create', signedParams);
  
  // 验证响应
  assert(response.code === "0");
  assert(response.status === "0"); // 0为处理中
  
  return response;
}
```

## 签名算法实现

### RSA签名
```javascript
// RSA签名函数
function generateRSASign(data, privateKey) {
  // 按字典序排列参数
  const sortedKeys = Object.keys(data).filter(key => data[key] !== '').sort();
  let signData = '';
  for (let i = 0; i < sortedKeys.length; i++) {
    const key = sortedKeys[i];
    if (i > 0) signData += '&';
    signData += `${key}=${data[key]}`;
  }
  
  // 使用RSA私钥进行SHA1withRSA签名
  const sign = rsaSignWithSHA1(signData, privateKey);
  return sign;
}
```

### MD5签名
```javascript
// MD5签名函数
function generateMD5Sign(data, secretKey) {
  // 按字典序排列参数
  const sortedKeys = Object.keys(data).filter(key => data[key] !== '').sort();
  let signData = '';
  for (let i = 0; i < sortedKeys.length; i++) {
    const key = sortedKeys[i];
    if (i > 0) signData += '&';
    signData += `${key}=${data[key]}`;
  }
  
  // 添加商户密钥并进行MD5加密
  signData += `&key=${secretKey}`;
  return md5(signData).toLowerCase();
}
```

## 回调验证测试

### 代收回调验证
```javascript
// 测试用例：验证代收回调
async function testPayCallbackVerification(callbackData, publicKey) {
  const receivedSign = callbackData.sign;
  delete callbackData.sign;
  
  // 重新计算签名
  const calculatedSign = verifyRSASign(callbackData, publicKey);
  
  // 验证签名
  assert(calculatedSign === receivedSign);
  
  // 返回success确认
  return "success";
}
```

## 测试执行框架

### 测试初始化
```javascript
class BishengAPITester {
  constructor(config) {
    this.merchantId = config.merchantId;
    this.md5Key = config.md5Key;
    this.rsaPrivateKey = config.rsaPrivateKey;
    this.rsaPublicKey = config.rsaPublicKey;
    this.baseURL = config.baseURL || 'https://gateway.bishengusdt.com';
  }
  
  async runAllTests() {
    console.log('开始执行币圣系统API测试...');
    
    // 执行各项测试
    await this.testPayFunctions();      // 代收功能
    await this.testRemitFunctions();    // 代付功能
    await this.testQueryFunctions();    // 查询功能
    await this.testBalanceFunction();   // 余额功能
    await this.testCNYPayments();       // CNY代付功能
    
    console.log('币圣系统API测试完成');
  }
  
  // 实现各个测试方法...
}
```

## 测试数据管理

### 测试数据生成
```javascript
// 生成测试数据
const testDataGenerator = {
  generateMerchantOrderNo: () => `TEST${Date.now()}`,
  generateAmount: (min = 1, max = 100) => (Math.random() * (max - min) + min).toFixed(2),
  getRandomAddress: (type = 'TRC20') => {
    if (type === 'TRC20') {
      return 'T' + Math.random().toString(36).substring(2, 34).padEnd(33, 'x').substring(0, 33);
    }
    // 其他类型地址生成
  }
};
```

## 异常情况测试

### 错误处理测试
```javascript
// 测试异常情况
async function testErrorCases() {
  // 1. 重复订单号测试
  await testDuplicateOrderNo();
  
  // 2. 无效签名测试
  await testInvalidSignature();
  
  // 3. 缺少必填参数测试
  await testMissingRequiredParams();
  
  // 4. 超额金额测试
  await testOverAmount();
  
  // 5. 无效地址测试
  await testInvalidAddress();
}
```

## 性能测试

### 并发测试
```javascript
// 并发下单测试
async function testConcurrentOrders(concurrentCount = 10) {
  const promises = [];
  
  for (let i = 0; i < concurrentCount; i++) {
    promises.push(createSingleOrder());
  }
  
  const results = await Promise.all(promises);
  
  // 验证结果
  const successCount = results.filter(r => r.code === "0").length;
  console.log(`并发测试结果: ${successCount}/${concurrentCount} 成功`);
  
  return results;
}
```

## 安全性测试

### 安全验证测试
```javascript
// 安全性测试
async function testSecurity() {
  // 1. IP白名单测试（如果有）
  // 2. 签名校验测试
  // 3. 重放攻击防护测试
  // 4. 数据加密验证
}
```

## 测试报告

### 生成测试报告
```javascript
// 生成测试报告
function generateTestReport(results) {
  const report = {
    summary: {
      total: results.length,
      passed: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      successRate: (results.filter(r => r.success).length / results.length * 100).toFixed(2) + '%'
    },
    details: results,
    timestamp: new Date().toISOString()
  };
  
  return report;
}
```

## 自动化测试执行流程

1. **环境准备**：配置商户ID、密钥等信息
2. **基础功能测试**：逐一测试各项核心功能
3. **集成测试**：测试功能间的相互作用
4. **异常测试**：测试错误处理能力
5. **性能测试**：测试高并发下的表现
6. **安全测试**：验证安全机制的有效性
7. **报告生成**：生成详细的测试报告

## 注意事项

1. **测试环境**：确保在测试环境中执行，避免影响生产数据
2. **测试数据**：使用模拟数据，避免使用真实敏感信息
3. **频率控制**：控制API调用频率，避免触发限流
4. **回调验证**：确保回调地址可访问且能正确处理回调
5. **签名验证**：确保签名算法正确实现，避免验签失败