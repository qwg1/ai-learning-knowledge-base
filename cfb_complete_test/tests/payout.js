// 测试用例 - 代付
const PAYOUT_TEST = {
    TRC20: [
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'TRC订单管理')]" } },
        { action: "act", request: { kind: "wait", selector: "//table", timeMs: 5000 } },
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'代付管理')]" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-TRC20')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "TYourAddress" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        { action: "screenshot", path: "./reports/payout_trc20.png" }
    ],
    BEP20: [
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'BEP订单管理')]" } },
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'代付管理')]" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-BEP20')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "0xYourAddress" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        { action: "screenshot", path: "./reports/payout_bep20.png" }
    ],
    ERC20: [
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'BEP订单管理')]" } },
        { action: "act", request: { kind: "click", selector: "//span[contains(text(),'代付管理')]" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'创建订单')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='金额']", text: "1" } },
        { action: "act", request: { kind: "click", selector: "//input[@placeholder='请选择链类型']" } },
        { action: "act", request: { kind: "click", selector: "//li[contains(text(),'USDT-ERC20')]" } },
        { action: "act", request: { kind: "type", selector: "//input[@placeholder='请输入钱包地址']", text: "0xYourAddress" } },
        { action: "act", request: { kind: "click", selector: "//button[contains(text(),'确认提交')]" } },
        { action: "screenshot", path: "./reports/payout_erc20.png" }
    ]
};
module.exports = PAYOUT_TEST;
