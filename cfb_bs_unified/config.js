// CFB+BS 统一配置
const CONFIG = {
    // ============== CFB 浏览器自动化 ==============
    browser: {
        admin: {
            url: "https://test-admin.cfbaopay.com",
            username: "admin",
            password: "Aa849956973",
            totp_secret: "53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU"
        },
        merch: {
            url: "https://test-merch.cfbaopay.com",
            username: "10228",
            password: "Aa849956973",
            totp_secret: "53JNRCHHK5TSO4LDNBSGKQLXHNUGLKRN"
        },
        agent: {
            url: "https://test-admin.cfbaopay.com",
            username: "actingregory",
            password: "Aa849956973",
            totp_secret: "S4JW5BTMJNFWYPBZM4GGZDFPOKHBMZYB"
        }
    },
    
    // ============== BS API 测试 ==============
    api: {
        test: {
            base_url: "https://test-gateway.cfbaopay.com",
            gateway: "https://test-gateway.cfbaopay.com"
        },
        production: {
            base_url: "https://gateway.bishengusdt.com",
            gateway: "https://gateway.bishengusdt.com"
        },
        current_env: "test",
        
        // ✅ 已获取的密钥
        merchant: {
            id: "10228",
            md5_key: "d7fdce63f5c74621a1877d6c7e3d43a2",
            // RSA密钥需要手动从后台复制
            rsa_private_key: "",
            rsa_public_key: ""
        },
        
        notify_url: "https://your-callback-url.com/callback"
    },
    
    // ============== 测试数据 ==============
    testData: {
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
        }
    },
    
    waits: {
        page: 5000,
        element: 3000
    }
};

module.exports = CONFIG;
