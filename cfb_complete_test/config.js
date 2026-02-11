// CFB支付系统 - 配置文件
const CONFIG = {
    systems: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            username: "admin",
            password: "Aa849956973",
            totp_secret: "53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            username: "merchant",
            password: "xxx"
        }
    },
    testData: {
        merchant: {
            id: "M1001",
            name: "测试商户001",
            email: "test@example.com",
            phone: "13800138000"
        },
        amounts: {
            collection: "100",
            payout: "1",
            min: "0.01",
            normal: "1",
            max: "10000"
        },
        addresses: {
            trc20: "TYourTRC20Address",
            bep20: "0xYourBEP20Address",
            erc20: "0xYourERC20Address"
        },
        chains: ["TRC20", "BEP20", "ERC20"]
    },
    waits: {
        page: 5000,
        element: 3000,
        dialog: 1000
    }
};
module.exports = CONFIG;
