// 测试用例 - 登录
const LOGIN_TEST = [
    { action: "open", targetUrl: "https://test-admin.cfbaopay.com" },
    { action: "act", request: { kind: "wait", selector: "//input[@placeholder='登录账户']", timeMs: 5000 } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录账户']", text: "admin" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录密码']", text: "Aa849956973" } },
    // 生成验证码: ./totp.sh
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='谷歌验证码']", text: "验证码" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'登录')]" } },
    { action: "act", request: { kind: "wait", selector: "//span[contains(text(),'商户管理')]", timeMs: 5000 } },
    { action: "screenshot", path: "./reports/login_success.png" }
];
module.exports = LOGIN_TEST;
