// CFB支付系统测试 - 配置文件
// ⚠️ 敏感信息，请勿提交到公开仓库

const CONFIG = {
    // ========== 系统配置 ==========
    systems: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            name: "管理后台",
            username: "your_admin_username",
            password: "your_admin_password"
        },
        agent: {
            url: "https://test-agent.cfbaopay.com",
            name: "代理系统",
            username: "your_agent_username",
            password: "your_agent_password"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            name: "商户系统",
            username: "your_merchant_username",
            password: "your_merchant_password"
        }
    },

    // ========== 测试配置 ==========
    test: {
        // 测试商户信息
        merchant_info: {
            name: "测试商户001",
            email: "test001@example.com",
            phone: "13800138000"
        },

        // 测试金额
        amounts: {
            min: "0.01",
            normal: "1",
            max: "10000"
        },

        // 测试地址
        addresses: {
            trc20: "TYourTrc20Address",
            bep20: "0xYourBep20Address",
            erc20: "0xYourErc20Address"
        },

        // 链类型
        chains: {
            cny: "CNY",
            trc20: "USDT-TRC20",
            bep20: "USDT-BEP20",
            erc20: "USDT-ERC20"
        }
    },

    // ========== 等待配置 ==========
    wait: {
        page_load: 5000,      // 页面加载(ms)
        element: 3000,         // 元素等待(ms)
        dialog: 1000           // 弹窗等待(ms)
    }
};

module.exports = { CONFIG };
