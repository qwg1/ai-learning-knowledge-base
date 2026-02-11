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
        channel: "//span[contains(text(),'通道管理')]",
        keyManage: "//span[contains(text(),'密钥管理')]"
    },
    collection: {
        create: "//button[contains(text(),'创建订单')]",
        amount: "//input[@placeholder='金额']",
        chainTRC20: "//li[contains(text(),'USDT-TRC20')]",
        address: "//input[@placeholder='请输入钱包地址']",
        confirm: "//button[contains(text(),'确认提交')]"
    },
    payout: {
        create: "//button[contains(text(),'创建订单')]",
        amount: "//input[@placeholder='金额']",
        address: "//input[@placeholder='请输入钱包地址']",
        confirm: "//button[contains(text(),'确认提交')]"
    }
};
module.exports = LOCATOR;
