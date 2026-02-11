// 测试用例 - 商户登录 (10228)
const { CONFIG } = require('../config');

const MERCH_LOGIN_TEST = [
    { action: "open", targetUrl: `${CONFIG.browser.merch.url}/#/login?redirect=%2FkeyManage` },
    { action: "act", request: { kind: "wait", selector: "//input[@placeholder='登录账户']", timeMs: 5000 } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录账户']", text: CONFIG.browser.merch.username } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='登录密码']", text: CONFIG.browser.merch.password } },
    // 验证码: 使用 totp.py 生成
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='谷歌验证码']", text: "验证码" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'登录')]" } },
    { action: "act", request: { kind: "wait", selector: "//span[contains(text(),'密钥')]", timeMs: 5000 } },
    { action: "screenshot", path: "./reports/merch_login.png" }
];
module.exports = MERCH_LOGIN_TEST;
