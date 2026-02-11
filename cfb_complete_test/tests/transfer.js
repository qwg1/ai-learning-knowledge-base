// 测试用例 - 商户互转
const TRANSFER_TEST = [
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC钱包管理')]" } },
    { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'商户互转')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='转出商户']", text: "M1001" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='转入商户']", text: "M1002" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
    { action: "act", request: { kind: "click", selector: "//input[@placeholder='币种']" } },
    { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT')]" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认互转')]" } },
    { action: "screenshot", path: "./reports/transfer.png" }
];
module.exports = TRANSFER_TEST;
