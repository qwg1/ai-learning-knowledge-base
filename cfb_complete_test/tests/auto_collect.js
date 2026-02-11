// 测试用例 - 自动归集
const AUTO_COLLECT_TEST = [
    { action: "open", targetUrl: "https://test-merch.cfbaopay.com" },
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'归集')]" } },
    { action: "act", request: { kind: "click", selector: "//span[contains(text(),'自动归集')]" } },
    { action: "act", request: { kind: "type", selector: "//input[@placeholder='归集阈值']", text: "1" } },
    { action: "act", request: { kind: "click", selector: "//button[contains(text(),'开启自动归集')]" } },
    { action: "screenshot", path: "./reports/auto_collect.png" }
];
module.exports = AUTO_COLLECT_TEST;
