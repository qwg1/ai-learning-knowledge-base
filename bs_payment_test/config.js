// BS支付系统 - 配置文件
module.exports = {
    // 环境配置
    env: "test",  // test 或 production
    
    // 正式环境
    production: {
        base_url: "https://gateway.bishengusdt.com"
    },
    
    // 测试环境
    test: {
        base_url: "https://test-gateway.cfbaopay.com"
    },
    
    // 商户配置（需要替换为实际值）
    merchant: {
        id: "10216",              // 商户ID
        md5_key: "",             // MD5密钥
        rsa_private_key: "",     // RSA私钥
        rsa_public_key: ""       // RSA公钥（平台公钥）
    },
    
    // 回调配置
    notify_url: "https://your-callback-url.com/callback",
    
    // 回调IP
    callback_ip: "8.217.236.95",
    
    // 超时配置（秒）
    timeout: 30
};
