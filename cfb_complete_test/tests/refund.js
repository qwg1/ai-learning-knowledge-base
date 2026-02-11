// 测试用例 - 退款
const REFUND_TEST = [
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入平台单号']", text: "ORD123456" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'搜索')]" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'退款')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入退款金额']", text: "1" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入退款原因']", text: "测试退款" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认退款')]" } },
    { action: "screenshot", path: "./reports/refund.png" }
];
module.exports = REFUND_TEST;
