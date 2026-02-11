// CFB支付系统 - 元素定位器
const LOCATOR = {
    login: {
        username: "//input[@placeholder='登录账户']",
        password: "//input[@placeholder='登录密码']",
        totp: "//input[@placeholder='谷歌验证码']",
        submit: "//button[contains(text(),'登录')]"
    },
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
    order: {
        search: "//button[contains(text(),'搜索')]",
        reset: "//button[contains(text(),'重置')]",
        export: "//button[contains(text(),'导出')]",
        supplement: "//button[contains(text(),'补单')]",
        refund: "//button[contains(text(),'退款')]"
    },
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
    payout: {
        create: "//button[contains(text(),'创建订单')]",
        amount: "//input[@placeholder='金额']",
        chain: "//input[@placeholder='请选择链类型']",
        address: "//input[@placeholder='请输入钱包地址']",
        confirm: "//button[contains(text(),'确认提交')]",
        remark: "//input[@placeholder='备注']"
    },
    supplement: {
        dialog: "//div[contains(text(),'补单')]",
        orderNo: "//input[@placeholder='请输入平台单号']",
        txHash: "//input[@placeholder='请输入交易哈希']",
        amount: "//input[@placeholder='请输入金额']",
        submit: "//button[contains(text(),'确认补单')]"
    },
    refund: {
        dialog: "//div[contains(text(),'退款')]",
        orderNo: "//input[@placeholder='请输入平台单号']",
        amount: "//input[@placeholder='请输入退款金额']",
        remark: "//input[@placeholder='请输入退款原因']",
        submit: "//button[contains(text(),'确认退款')]"
    },
    limit: {
        dialog: "//div[contains(text(),'额度')]",
        dailyLimit: "//input[@placeholder='日限额']",
        singleLimit: "//input[@placeholder='单笔限额']",
        monthlyLimit: "//input[@placeholder='月限额']",
        submit: "//button[contains(text(),'确认')]"
    },
    transfer: {
        dialog: "//div[contains(text(),'商户互转')]",
        fromMerchant: "//input[@placeholder='转出商户']",
        toMerchant: "//input[@placeholder='转入商户']",
        amount: "//input[@placeholder='金额']",
        chain: "//input[@placeholder='币种']",
        submit: "//button[contains(text(),'确认互转')]"
    },
    withdraw: {
        menu: "//span[contains(text(),'提现')]",
        amount: "//input[@placeholder='提现金额']",
        address: "//input[@placeholder='钱包地址']",
        chain: "//input[@placeholder='链类型']",
        confirm: "//button[contains(text(),'确认提现')]",
        balance: "//span[contains(text(),'可用余额')]"
    },
    collect: {
        menu: "//span[contains(text(),'归集')]",
        manual: "//button[contains(text(),'手动归集')]",
        auto: "//span[contains(text(),'自动归集')]",
        address: "//input[@placeholder='归集地址']",
        submit: "//button[contains(text(),'确认归集')]",
        threshold: "//input[@placeholder='归集阈值']",
        enable: "//button[contains(text(),'开启自动归集')]"
    },
    common: {
        ok: "//button[contains(text(),'确定')]",
        cancel: "//button[contains(text(),'取消')]",
        close: "//button[contains(text(),'关闭')]",
        table: "//table",
        dialog: "//div[contains(@class,'el-dialog')]"
    }
};
module.exports = LOCATOR;
