// 测试用例 - 商户后台提现
const WITHDRAW_TEST = [
    { action: "open", targetUrl: "https://test-merch.cfbaopay.com" },
    { action: "act", request: { kind: "wait", selector: "//input[@placeholder='登录账户']", timeMs: 5000 } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录账户']", text: "merchant" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录密码']", text: "xxx" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='谷歌验证码']", text: "验证码" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'登录')]" } },
    { action: "act", request: { kind: "wait", selector: "//span[contains(text(),'首页')]", timeMs: 5000 } },
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'提现')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='提现金额']", text: "1" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='钱包地址']", text: "TYourAddress" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提现')]" } },
    { action: "screenshot", path: "./reports/withdraw.png" }
];
module.exports = WITHDRAW_TEST;
