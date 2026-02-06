# 币圣系统自动化测试实现方案

## 实现概述

基于币圣系统API文档，我们将使用OpenClaw的工具集来实现自动化测试，主要涉及API调用、签名算法实现、测试数据管理和结果验证。

## 技术栈和工具

### 主要工具
- OpenClaw exec工具 - 执行shell命令
- OpenClaw web_fetch工具 - API调用
- OpenClaw write/read工具 - 配置文件管理
- Node.js环境 - 实现API调用和签名算法

## 实现步骤

### 1. 环境准备

首先，我们需要创建测试配置文件：

```bash
# 创建测试配置文件
cat > /Users/qin/.openclaw/workspace/test_config.json << EOF
{
  "merchantId": "YOUR_MERCHANT_ID",
  "md5Key": "YOUR_MD5_KEY",
  "rsaPrivateKey": "YOUR_RSA_PRIVATE_KEY",
  "rsaPublicKey": "YOUR_RSA_PUBLIC_KEY",
  "baseURL": "https://gateway.bishengusdt.com",
  "testCallbacks": {
    "payNotifyUrl": "https://test-callback.yourdomain.com/pay_notify",
    "remitNotifyUrl": "https://test-callback.yourdomain.com/remit_notify"
  }
}
EOF
```

### 2. 实现API调用脚本

创建一个Node.js脚本来实现API调用和签名功能：

```javascript
// bisheng_api_client.js
const crypto = require('crypto');

class BishengAPIClient {
  constructor(config) {
    this.config = config;
  }

  // RSA签名算法
  generateRSASign(data) {
    // 按字典序排列参数
    const sortedKeys = Object.keys(data)
      .filter(key => data[key] !== '' && data[key] !== null && data[key] !== undefined)
      .sort();
    
    let signData = sortedKeys.map(key => `${key}=${data[key]}`).join('&');
    
    // 使用RSA私钥进行签名
    const sign = crypto.createSign('RSA-SHA1');
    sign.update(signData);
    const signature = sign.sign(this.config.rsaPrivateKey, 'base64');
    
    return {
      signData,
      signature
    };
  }

  // MD5签名算法
  generateMD5Sign(data) {
    const sortedKeys = Object.keys(data)
      .filter(key => data[key] !== '' && data[key] !== null && data[key] !== undefined)
      .sort();
    
    let signData = sortedKeys.map(key => `${key}=${data[key]}`).join('&');
    signData += `&key=${this.config.md5Key}`;
    
    return crypto.createHash('md5').update(signData).digest('hex').toLowerCase();
  }

  // 生成带签名的请求参数
  signRequest(params, signType = 'RSA') {
    const paramsCopy = {...params};
    
    if (signType === 'RSA') {
      const {signature} = this.generateRSASign(paramsCopy);
      paramsCopy.sign = signature;
      paramsCopy.signType = 'RSA';
    } else if (signType === 'MD5') {
      paramsCopy.sign = this.generateMD5Sign(paramsCopy);
      paramsCopy.signType = 'MD5';
    }
    
    return paramsCopy;
  }

  // 发起API请求
  async makeRequest(endpoint, params, method = 'POST') {
    const url = `${this.config.baseURL}${endpoint}`;
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params)
    });
    
    return await response.json();
  }

  // USDT代收下单
  async createPayOrder(orderParams) {
    const params = {
      merchantId: this.config.merchantId,
      version: '6.0.0',
      merchantOrderNo: orderParams.merchantOrderNo || `CZ${Date.now()}`,
      amount: orderParams.amount,
      coinType: orderParams.coinType || 'USDT_TRC20',
      callbackCurrencyCode: orderParams.callbackCurrencyCode || 'USDT',
      notifyUrl: orderParams.notifyUrl || this.config.testCallbacks.payNotifyUrl,
      ...orderParams
    };

    const signedParams = this.signRequest(params, orderParams.signType || 'RSA');
    return await this.makeRequest('/api/coin/payOrder/create', signedParams);
  }

  // USDT代付下单
  async createRemitOrder(orderParams) {
    const params = {
      merchantId: this.config.merchantId,
      version: '6.0.0',
      merchantOrderNo: orderParams.merchantOrderNo || `DF${Date.now()}`,
      amount: orderParams.amount,
      coinType: orderParams.coinType || 'USDT_TRC20',
      bookingAddress: orderParams.bookingAddress,
      callbackCurrencyCode: orderParams.callbackCurrencyCode || 'USDT',
      notifyUrl: orderParams.notifyUrl || this.config.testCallbacks.remitNotifyUrl,
      ...orderParams
    };

    const signedParams = this.signRequest(params, orderParams.signType || 'RSA');
    return await this.makeRequest('/api/coin/remitOrder/create', signedParams);
  }

  // 订单查询
  async queryOrder(merchantOrderNo, endpoint = '/api/coin/payOrder/query') {
    const params = {
      merchantId: this.config.merchantId,
      version: '6.0.0',
      merchantOrderNo: merchantOrderNo,
      submitTime: new Date().toISOString().replace(/[-:]/g, '').replace(/\..+/, '').substring(0, 14)
    };

    const signedParams = this.signRequest(params);
    return await this.makeRequest(endpoint, signedParams);
  }

  // 余额查询
  async queryBalance(coinType = 'USDT') {
    const params = {
      merchantId: this.config.merchantId,
      version: '6.0.0',
      requestTime: new Date().toISOString().replace(/[-:]/g, '').replace(/\..+/, '').substring(0, 14),
      coinType: coinType
    };

    const signedParams = this.signRequest(params);
    return await this.makeRequest('/api/coin/balance/query', signedParams);
  }
}

module.exports = BishengAPIClient;
```

### 3. 创建测试执行脚本

```javascript
// test_runner.js
const BishengAPIClient = require('./bisheng_api_client');
const config = require('../test_config.json');

class TestRunner {
  constructor() {
    this.client = new BishengAPIClient(config);
    this.results = [];
  }

  async runPayTest() {
    console.log('开始执行代收测试...');
    
    try {
      const orderResult = await this.client.createPayOrder({
        amount: '10.00',
        coinType: 'USDT_TRC20',
        callbackCurrencyCode: 'USDT'
      });
      
      console.log('代收下单结果:', orderResult);
      
      // 记录测试结果
      this.results.push({
        testName: 'USDT代收下单',
        result: orderResult,
        success: orderResult.code === '0',
        timestamp: new Date().toISOString()
      });
      
      return orderResult;
    } catch (error) {
      console.error('代收测试失败:', error);
      this.results.push({
        testName: 'USDT代收下单',
        error: error.message,
        success: false,
        timestamp: new Date().toISOString()
      });
    }
  }

  async runRemitTest() {
    console.log('开始执行代付测试...');
    
    try {
      const orderResult = await this.client.createRemitOrder({
        amount: '5.00',
        coinType: 'USDT_TRC20',
        bookingAddress: 'TBCwRrYLeBi9GZqDdeAiDToXzx12345678', // 示例地址
        callbackCurrencyCode: 'USDT'
      });
      
      console.log('代付下单结果:', orderResult);
      
      // 记录测试结果
      this.results.push({
        testName: 'USDT代付下单',
        result: orderResult,
        success: orderResult.code === '0',
        timestamp: new Date().toISOString()
      });
      
      return orderResult;
    } catch (error) {
      console.error('代付测试失败:', error);
      this.results.push({
        testName: 'USDT代付下单',
        error: error.message,
        success: false,
        timestamp: new Date().toISOString()
      });
    }
  }

  async runBalanceTest() {
    console.log('开始执行余额查询测试...');
    
    try {
      const balanceResult = await this.client.queryBalance('USDT');
      
      console.log('余额查询结果:', balanceResult);
      
      // 记录测试结果
      this.results.push({
        testName: '余额查询',
        result: balanceResult,
        success: balanceResult.code === '0',
        timestamp: new Date().toISOString()
      });
      
      return balanceResult;
    } catch (error) {
      console.error('余额查询测试失败:', error);
      this.results.push({
        testName: '余额查询',
        error: error.message,
        success: false,
        timestamp: new Date().toISOString()
      });
    }
  }

  async runAllTests() {
    console.log('开始执行全部测试...');
    
    await this.runPayTest();
    await this.runRemitTest();
    await this.runBalanceTest();
    
    // 生成测试报告
    await this.generateReport();
    
    return this.results;
  }

  async generateReport() {
    const report = {
      summary: {
        total: this.results.length,
        passed: this.results.filter(r => r.success).length,
        failed: this.results.filter(r => !r.success).length,
        successRate: (this.results.filter(r => r.success).length / this.results.length * 100).toFixed(2) + '%'
      },
      details: this.results,
      timestamp: new Date().toISOString()
    };
    
    // 保存测试报告
    const fs = require('fs');
    fs.writeFileSync(`/Users/qin/.openclaw/workspace/test_report_${Date.now()}.json`, JSON.stringify(report, null, 2));
    
    console.log('测试报告已生成:', `/Users/qin/.openclaw/workspace/test_report_${Date.now()}.json`);
    return report;
  }
}

// 执行测试
(async () => {
  const runner = new TestRunner();
  await runner.runAllTests();
})();
```

### 4. 在OpenClaw中执行测试

现在我们可以使用OpenClaw的exec工具来运行这些测试脚本：

```bash
# 创建测试执行脚本
cat > /Users/qin/.openclaw/workspace/run_bisheng_tests.sh << 'EOF'
#!/bin/bash

# 设置工作目录
cd /Users/qin/.openclaw/workspace

# 安装依赖（如果需要）
# npm install

# 运行测试
node test_runner.js

echo "测试执行完成"
EOF

chmod +x /Users/qin/.openclaw/workspace/run_bisheng_tests.sh
```

### 5. 实际执行步骤

1. **配置测试参数**：首先需要将真实的商户ID、密钥等信息填入配置文件

2. **运行测试**：
```bash
# 在OpenClaw中执行
exec("bash /Users/qin/.openclaw/workspace/run_bisheng_tests.sh")
```

3. **验证结果**：检查生成的测试报告文件

4. **调试和优化**：根据测试结果调整参数和修复问题

### 6. 安全注意事项

- 将敏感信息（如密钥）存储在安全的配置文件中
- 不要在代码或日志中明文输出敏感信息
- 使用测试环境而不是生产环境进行测试
- 控制API调用频率，避免触发限流

### 7. 定时执行

还可以设置定时任务来定期执行测试：

```javascript
// 设置每日执行测试
cron({
  action: "add",
  job: {
    name: "Daily Bisheng API Tests",
    schedule: { kind: "every", everyMs: 24 * 60 * 60 * 1000 }, // 每天执行
    payload: { 
      kind: "systemEvent", 
      text: "Running daily Bisheng API tests..." 
    },
    sessionTarget: "main"
  }
})
```

这就是实现币圣系统自动化测试的完整方案。通过这种方式，我们可以系统地测试所有核心功能，并生成详细的测试报告。