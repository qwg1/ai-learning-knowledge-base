#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - TOTP验证码生成器（预装版）

使用说明：
1. 预装pyotp库，无需安装
2. 直接运行即可获取验证码
3. 验证码30秒内有效
"""

import sys

# 预装的TOTP密钥
SECRET = "53JNRCVNUC2ZZ2OV5TDT5DWWK3TM7TXU"

def get_totp_code(secret=None):
    """
    生成TOTP验证码
    
    Args:
        secret: 种子密钥
        
    Returns:
        str: 6位验证码
    """
    secret = secret or SECRET
    
    try:
        import pyotp
        totp = pyotp.TOTP(secret)
        code = totp.now()
        return code
    except ImportError:
        return None

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════╗
║     CFB支付系统 - TOTP验证码生成器            ║
╚══════════════════════════════════════════════════════╝
    """)
    
    print(f"🔐 种子: {SECRET[:4]}...{SECRET[-4:]}")
    print("="*40)
    
    code = get_totp_code()
    
    if code:
        import time
        epoch = int(time.time())
        remaining = 30 - (epoch % 30)
        
        print(f"\n📟 当前验证码: {code}")
        print(f"⏰ 剩余时间: {remaining}秒")
        print("="*40)
        
        # 保存到文件
        with open("totp_code.txt", "w") as f:
            f.write(code)
        print(f"💾 已保存到: totp_code.txt")
        
        return code
    else:
        print("\n❌ pyotp未安装")
        print("\n💡 安装方法:")
        print("   pip install pyotp --user")
        return None

if __name__ == "__main__":
    main()
