// 测试用例 - 调额
const LIMIT_TEST = [
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'商户管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入商户名称']", text: "测试商户001" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'搜索')]" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'额度')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='日限额']", text: "100000" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='单笔限额']", text: "10000" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='月限额']", text: "1000000" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认')]" } },
    { action: "screenshot", path: "./reports/limit.png" }
];
module.exports = LIMIT_TEST;
