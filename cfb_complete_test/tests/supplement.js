// 测试用例 - 补单
const SUPPLEMENT_TEST = [
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入平台单号']", text: "ORD123456" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'搜索')]" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'补单')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入交易哈希']", text: "txHash123" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入金额']", text: "1" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认补单')]" } },
    { action: "screenshot", path: "./reports/supplement.png" }
];
module.exports = SUPPLEMENT_TEST;
