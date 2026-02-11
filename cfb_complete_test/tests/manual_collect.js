// 测试用例 - 手动归集
const MANUAL_COLLECT_TEST = [
    { action: "open", targetUrl: "https://test-merch.cfbaopay.com" },
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'归集')]" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'手动归集')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='归集地址']", text: "TYourCollectAddress" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认归集')]" } },
    { action: "screenshot", path: "./reports/manual_collect.png" }
];
module.exports = MANUAL_COLLECT_TEST;
