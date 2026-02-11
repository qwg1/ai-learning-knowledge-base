# CFB支付系统 - 完整自动化测试方案

> 基于OpenClaw agent-browser，实现所有核心功能自动化

---

## 📋 功能清单

| 模块 | 功能 | 系统 | 优先级 |
|------|------|------|--------|
| 登录 | 管理员登录 | admin | P0 |
| 代收 | CNY代收 | admin/merch | P0 |
| 代收 | USDT-TRC20代收 | admin/merch | P0 |
| 代收 | USDT-BEP20代收 | admin/merch | P0 |
| 代付 | USDT-TRC20代付 | admin/merch | P0 |
| 代付 | USDT-BEP20代付 | admin/merch | P0 |
| 代付 | USDT-ERC20代付 | admin/merch | P0 |
| 补单 | 订单补单 | admin | P0 |
| 退款 | 订单退款 | admin | P0 |
| 调额 | 商户限额调整 | admin | P1 |
| 商户互转 | 商户间转账 | admin | P1 |
| 提现 | 商户后台提现 | merch | P1 |
| 手动归集 | 手动归集地址 | merch | P1 |
| 自动归集 | 自动归集配置 | admin | P1 |

---

## 📁 项目结构

```
cfb_complete_test/
├── config.js              # 配置文件
├── locator.js             # 元素定位器
├── actions.js             # 页面操作封装
├── totp.sh               # TOTP验证码生成
├── tests/
│   ├── login.js          # 登录
│   ├── collection.js      # 代收
│   ├── payout.js         # 代付
│   ├── supplement.js      # 补单
│   ├── refund.js         # 退款
│   ├── limit.js          # 调额
│   ├── transfer.js       # 商户互转
│   ├── withdraw.js       # 提现
│   ├── manual_collect.js # 手动归集
│   └── auto_collect.js  # 自动归集
└── README.md             # 本文档
```

---

## 🔧 配置文件 (config.js)

```javascript
const CONFIG = {
    // 系统配置
    systems: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            username: "admin",
            password: "Aa849956973",
            totp_secret: "53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            username: "merchant",
            password: "xxx"
        }
    },
    
    // 测试数据
    testData: {
        // 商户
        merchant: {
            id: "M1001",
            name: "测试商户001",
            email: "test@example.com",
            phone: "13800138000"
        },
        
        // 测试金额
        amounts: {
            collection: "100",      // 代收金额
            payout: "1",             // 代付金额
            min: "0.01",
            normal: "1",
            max: "10000"
        },
        
        // 测试地址
        addresses: {
            trc20: "TYourTRC20Address",
            bep20: "0xYourBEP20Address",
            erc20: "0xYourERC20Address"
        },
        
        // 链类型
        chains: ["TRC20", "BEP20", "ERC20"]
    },
    
    // 等待配置
    waits: {
        page: 5000,
        element: 3000,
        dialog: 1000
    }
};

module.exports = CONFIG;
```

---

## 📍 元素定位器 (locator.js)

```javascript
const LOCATOR = {
    // ========== 登录页面 ==========
    login: {
        username: "//input[@placeholder='登录账户']",
        password: "//input[@placeholder='登录密码']",
        totp: "//input[@placeholder='谷歌验证码']",
        submit: "//button[contains(text(),'登录')]"
    },
    
    // ========== 菜单 ==========
    menu: {
        home: "//span[contains(text(),'我的首页')]",
        merchant: "//span[contains(text(),'商户管理')]",
        trcOrder: "//span[contains(text(),'TRC订单管理')]",
        bepOrder: "//span[contains(text(),'BEP订单管理')]",
        channel: "//span[contains(text(),'通道管理')]",
        trcWallet: "//span[contains(text(),'TRC钱包管理')]",
        bepWallet: "//span[contains(text(),'BEP钱包管理')]",
        risk: "//span[contains(text(),'风控管理')]",
        config: "//span[contains(text(),'配置管理')]",
        statistics: "//span[contains(text(),'统计报表')]",
        agent: "//span[contains(text(),'代理管理')]",
        staff: "//span[contains(text(),'员工管理')]",
        system: "//span[contains(text(),'系统管理')]"
    },
    
    // ========== 商户管理 ==========
    merchant: {
        addButton: "//button[contains(text(),'新增商户')]",
        name: "//input[@placeholder='商户名称']",
        email: "//input[@placeholder='商户邮箱']",
        phone: "//input[@placeholder='商户电话']",
        submit: "//button[contains(text(),'提交')]",
        search: "//button[contains(text(),'搜索')]",
        edit: "//button[contains(text(),'编辑')]",
        limit: "//button[contains(text(),'额度')]"
    },
    
    // ========== 订单管理 ==========
    order: {
        search: "//button[contains(text(),'搜索')]",
        reset: "//button[contains(text(),'重置')]",
        export: "//button[contains(text(),'导出')]",
        supplement: "//button[contains(text(),'补单')]",
        refund: "//button[contains(text(),'退款')]"
    },
    
    // ========== 代收 ==========
    collection: {
        create: "//button[contains(text(),'创建订单')]",
        amount: "//input[@placeholder='金额']",
        chain: "//input[@placeholder='请选择链类型']",
        chainCNY: "//li[contains(text(),'CNY')]",
        chainTRC20: "//li[contains(text(),'USDT-TRC20')]",
        chainBEP20: "//li[contains(text(),'USDT-BEP20')]",
        chainERC20: "//li[contains(text(),'USDT-ERC20')]",
        address: "//input[@placeholder='请输入钱包地址']",
        confirm: "//button[contains(text(),'确认提交')]",
        cancel: "//button[contains(text(),'取消')]"
    },
    
    // ========== 代付 ==========
    payout: {
        create: "//button[contains(text(),'创建订单')]",
        amount: "//input[@placeholder='金额']",
        chain: "//input[@placeholder='请选择链类型')]",
        address: "//input[@placeholder='请输入钱包地址']",
        confirm: "//button[contains(text(),'确认提交')]",
        remark: "//input[@placeholder='备注')]"
    },
    
    // ========== 补单 ==========
    supplement: {
        dialog: "//div[contains(text(),'补单')]",
        orderNo: "//input[@placeholder='请输入平台单号')]",
        txHash: "//input[@placeholder='请输入交易哈希')]",
        amount: "//input[@placeholder='请输入金额')]",
        submit: "//button[contains(text(),'确认补单')]"
    },
    
    // ========== 退款 ==========
    refund: {
        dialog: "//div[contains(text(),'退款')]",
        orderNo: "//input[@placeholder='请输入平台单号')]",
        amount: "//input[@placeholder='请输入退款金额')]",
        remark: "//input[@placeholder='请输入退款原因')]",
        submit: "//button[contains(text(),'确认退款')]"
    },
    
    // ========== 调额 ==========
    limit: {
        dialog: "//div[contains(text(),'额度')]",
        dailyLimit: "//input[@placeholder='日限额')]",
        singleLimit: "//input[@placeholder='单笔限额')]",
        monthlyLimit: "//input[@placeholder='月限额')]",
        submit: "//button[contains(text(),'确认')]"
    },
    
    // ========== 商户互转 ==========
    transfer: {
        dialog: "//div[contains(text(),'商户互转')]",
        fromMerchant: "//input[@placeholder='转出商户')]",
        toMerchant: "//input[@placeholder='转入商户')]",
        amount: "//input[@placeholder='金额')]",
        chain: "//input[@placeholder='币种')]",
        submit: "//button[contains(text(),'确认互转')]"
    },
    
    // ========== 提现 ==========
    withdraw: {
        menu: "//span[contains(text(),'提现')]",
        amount: "//input[@placeholder='提现金额')]",
        address: "//input[@placeholder='钱包地址')]",
        chain: "//input[@placeholder='链类型')]",
        confirm: "//button[contains(text(),'确认提现')]",
        balance: "//span[contains(text(),'可用余额')]"
    },
    
    // ========== 归集 ==========
    collect: {
        menu: "//span[contains(text(),'归集')]",
        manual: "//button[contains(text(),'手动归集')]",
        auto: "//span[contains(text(),'自动归集')]",
        address: "//input[@placeholder='归集地址')]",
        submit: "//button[contains(text(),'确认归集')]",
        threshold: "//input[@placeholder='归集阈值')]",
        enable: "//button[contains(text(),'开启自动归集')]"
    },
    
    // ========== 通用 ==========
    common: {
        ok: "//button[contains(text(),'确定')]",
        cancel: "//button[contains(text(),'取消')]",
        close: "//button[contains(text(),'关闭')]",
        table: "//table",
        dialog: "//div[contains(@class,'el-dialog')]"
    }
};

module.exports = LOCATOR;
```

---

## 🧪 测试用例

### 1. 登录测试 (tests/login.js)

```javascript
const LOGIN_TEST = [
    // 1. 打开登录页
    { action: "open", targetUrl: "https://test-admin.cfbaopay.com" },
    
    // 2. 等待用户名输入框
    { action: "act", request: { kind: "wait", selector: "//input[@placeholder='登录账户']", timeMs: 5000 } },
    
    // 3. 输入用户名
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录账户']", text: "admin" } },
    
    // 4. 输入密码
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录密码']", text: "Aa849956973" } },
    
    // 5. 生成验证码
    // ./totp.sh -> 123456
    
    // 6. 输入验证码
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='谷歌验证码']", text: "验证码" } },
    
    // 7. 点击登录
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'登录')]" } },
    
    // 8. 等待首页
    { action: "act", request: { kind: "wait", selector: "//span[contains(text(),'商户管理')]", timeMs: 5000 } },
    
    // 9. 截图
    { action: "screenshot", path: "./reports/login_success.png" }
];

module.exports = LOGIN_TEST;
```

### 2. 代收测试 (tests/collection.js)

```javascript
const COLLECTION_TEST = {
    // CNY代收
    CNY: [
        // 1. 进入TRC订单管理
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
        { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
        
        // 2. 点击创建订单
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        
        // 3. 输入金额
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "100" } },
        
        // 4. 选择CNY
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'CNY')]" } },
        
        // 5. 输入商户名称
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入商户名称']", text: "测试商户001" } },
        
        // 6. 确认提交
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        
        // 7. 截图
        { action: "screenshot", path: "./reports/collection_cny.png" }
    ],
    
    // USDT-TRC20代收
    TRC20: [
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "10" } },
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-TRC20')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "TYourAddress" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        { action: "screenshot", path: "./reports/collection_trc20.png" }
    ],
    
    // USDT-BEP20代收
    BEP20: [
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'BEP订单管理')]" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "10" } },
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-BEP20')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "0xYourAddress" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        { action: "screenshot", path: "./reports/collection_bep20.png" }
    ]
};

module.exports = COLLECTION_TEST;
```

### 3. 代付测试 (tests/payout.js)

```javascript
const PAYOUT_TEST = {
    // USDT-TRC20代付
    TRC20: [
        // 1. 进入TRC订单管理
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
        { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
        
        // 2. 点击代付管理tab
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'代付管理')]" } },
        
        // 3. 点击创建订单
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        
        // 4. 输入金额
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
        
        // 5. 选择USDT-TRC20
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-TRC20')]" } },
        
        // 6. 输入钱包地址
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "TYourAddress" } },
        
        // 7. 确认提交
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        
        // 8. 截图
        { action: "screenshot", path: "./reports/payout_trc20.png" }
    ],
    
    // USDT-BEP20代付
    BEP20: [
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'BEP订单管理')]" } },
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'代付管理')]" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-BEP20')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "0xYourAddress" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        { action: "screenshot", path: "./reports/payout_bep20.png" }
    ],
    
    // USDT-ERC20代付
    ERC20: [
        // 流程同上，选择USDT-ERC20
    ]
};

module.exports = PAYOUT_TEST;
```

### 4. 补单测试 (tests/supplement.js)

```javascript
const SUPPLEMENT_TEST = [
    // 1. 进入订单列表
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    
    // 2. 搜索订单
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入平台单号']", text: "ORD123456" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'搜索')]" } },
    
    // 3. 点击补单
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'补单')]" } },
    
    // 4. 填写补单信息
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入交易哈希']", text: "txHash123" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入金额']", text: "1" } },
    
    // 5. 确认补单
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认补单')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/supplement.png" }
];

module.exports = SUPPLEMENT_TEST;
```

### 5. 退款测试 (tests/refund.js)

```javascript
const REFUND_TEST = [
    // 1. 进入订单列表
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    
    // 2. 搜索订单
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入平台单号']", text: "ORD123456" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'搜索')]" } },
    
    // 3. 点击退款
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'退款')]" } },
    
    // 4. 填写退款信息
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入退款金额']", text: "1" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入退款原因']", text: "测试退款" } },
    
    // 5. 确认退款
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认退款')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/refund.png" }
];

module.exports = REFUND_TEST;
```

### 6. 调额测试 (tests/limit.js)

```javascript
const LIMIT_TEST = [
    // 1. 进入商户管理
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'商户管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    
    // 2. 搜索商户
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入商户名称']", text: "测试商户001" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'搜索')]" } },
    
    // 3. 点击额度按钮
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'额度')]" } },
    
    // 4. 填写限额
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='日限额']", text: "100000" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='单笔限额']", text: "10000" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='月限额']", text: "1000000" } },
    
    // 5. 确认
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/limit.png" }
];

module.exports = LIMIT_TEST;
```

### 7. 商户互转测试 (tests/transfer.js)

```javascript
const TRANSFER_TEST = [
    // 1. 进入钱包管理
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC钱包管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    
    // 2. 点击商户互转
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'商户互转')]" } },
    
    // 3. 填写信息
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='转出商户']", text: "M1001" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='转入商户']", text: "M1002" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
    
    // 4. 选择币种
    { action: "act", request: { kind: "click", selector: "//input[@placeholder='币种']" } },
    { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT')]" } },
    
    // 5. 确认互转
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认互转')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/transfer.png" }
];

module.exports = TRANSFER_TEST;
```

### 8. 提现测试 (tests/withdraw.js)

```javascript
const WITHDRAW_TEST = [
    // 1. 打开商户系统
    { action: "open", targetUrl: "https://test-merch.cfbaopay.com" },
    { action: "act", request: { kind: "wait", selector: "//input[@placeholder='登录账户']", timeMs: 5000 } },
    
    // 2. 登录商户
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录账户']", text: "merchant" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录密码']", text: "xxx" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='谷歌验证码']", text: "验证码" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'登录')]" } },
    { action: "act", request: { kind: "wait", selector: "//span[contains(text(),'首页')]", timeMs: 5000 } },
    
    // 3. 进入提现
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'提现')]" } },
    
    // 4. 填写提现信息
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='提现金额']", text: "1" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='钱包地址']", text: "TYourAddress" } },
    
    // 5. 确认提现
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提现')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/withdraw.png" }
];

module.exports = WITHDRAW_TEST;
```

### 9. 手动归集测试 (tests/manual_collect.js)

```javascript
const MANUAL_COLLECT_TEST = [
    // 1. 打开商户系统
    { action: "open", targetUrl: "https://test-merch.cfbaopay.com" },
    
    // 2. 进入归集
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'归集')]" } },
    
    // 3. 点击手动归集
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'手动归集')]" } },
    
    // 4. 填写归集地址
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='归集地址']", text: "TYourCollectAddress" } },
    
    // 5. 确认归集
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认归集')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/manual_collect.png" }
];

module.exports = MANUAL_COLLECT_TEST;
```

### 10. 自动归集测试 (tests/auto_collect.js)

```javascript
const AUTO_COLLECT_TEST = [
    // 1. 进入商户系统
    { action: "open", targetUrl: "https://test-merch.cfbaopay.com" },
    
    // 2. 进入归集
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'归集')]" } },
    
    // 3. 进入自动归集tab
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'自动归集')]" } },
    
    // 4. 设置归集阈值
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='归集阈值']", text: "1" } },
    
    // 5. 开启自动归集
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'开启自动归集')]" } },
    
    // 6. 截图
    { action: "screenshot", path: "./reports/auto_collect.png" }
];

module.exports = AUTO_COLLECT_TEST;
```

---

## 📖 执行方式

### 方式1：逐个执行browser工具调用

在OpenClaw中直接输入：

```
# 登录
browser(action="open", targetUrl="https://test-admin.cfbaopay.com")
browser(action="act", request={"kind": "wait", "selector": "//input[@placeholder='登录账户']", "timeMs": 5000})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='登录账户']", "text": "admin"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='登录密码']", "text": "Aa849956973"})
browser(action="act", request={"kind": "type", "selector": "//input[@placeholder='谷歌验证码']", "text": "验证码"})
browser(action="act", request={"kind": "click", "selector": "//button[contains(text(),'登录')]"})
```

### 方式2：使用JavaScript注入获取TOTP

```javascript
// 在浏览器上下文中生成验证码
browser(action="act", request={
    kind: "evaluate",
    fn: "(() => { const secret = '53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU'; const base32chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'; let bits = ''; secret.toUpperCase().replace(/=+$/, '').split('').forEach(c => { bits += base32chars.indexOf(c).toString(2).padStart(5, '0'); }); let hex = ''; for (let i = 0; i + 4 <= bits.length; i += 4) { hex += parseInt(bits.substr(i, 4), 2).toString(16); } const time = Math.floor(Date.now() / 1000 / 30); const timeHex = time.toString(16).padStart(16, '0'); const crypto = window.crypto || window.msCrypto; const key = new Uint8Array(hex.match(/.{1,2}/g).map(b => parseInt(b, 16))); const data = new Uint8Array(timeHex.match(/.{1,2}/g).map(b => parseInt(b, 16))); crypto.subtle.importKey('raw', key, { name: 'HMAC', hash: 'SHA-1' }, false, ['sign']).then(k => crypto.subtle.sign('HMAC', k, data)).then(s => { const h = new Uint8Array(s); const o = h[h.length - 1] & 0x0f; const b = ((h[o] & 0x7f) << 24) | ((h[o + 1] & 0xff) << 16) | ((h[o + 2] & 0xff) << 8) | (h[o + 3] & 0xff); window.totpCode = (b % 1000000).toString().padStart(6, '0'); }); return 'generating...'; })()"
})

browser(action="act", request={
    kind: "evaluate",
    fn: "(() => { return window.totpCode || 'wait'; })()"
})
```

---

## 💡 最佳实践

| 场景 | 建议 |
|------|------|
| TOTP验证码 | 使用 `./totp.sh` 后台生成 |
| 元素定位 | 始终使用XPath |
| 页面等待 | 每个操作前添加显式等待 |
| 截图验证 | 每个关键步骤后截图 |
| 错误处理 | 使用try-catch捕获异常 |

---

## 🚨 常见问题

### 1. 验证码过期
**解决**：先生成验证码，再输入，避免超时

### 2. 元素找不到
**解决**：添加显式等待 `timeMs: 5000`

### 3. Dialog未关闭
**解决**：等待dialog消失后再进行下一步

---

*方案创建时间: 2026-02-11*
