#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 签名模块
支持: MD5签名、RSA签名

功能:
1. MD5签名（常用）
2. RSA签名（更安全）
3. 签名验证
"""

import hashlib
import json
import time
import random
from typing import Dict, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


class SignatureManager:
    """签名管理器"""
    
    def __init__(self, config: dict):
        """
        初始化签名管理器
        
        Args:
            config: 配置字典，包含签名密钥
        """
        self.config = config
        self.sign_type = config.get("sign", {}).get("type", "MD5")
        self.version = config.get("sign", {}).get("version", "6.0.0")
    
    def md5_sign(self, params: Dict, api_key: str) -> str:
        """
        MD5签名
        
        Args:
            params: 请求参数字典
            api_key: 签名密钥
            
        Returns:
            str: 签名结果
        """
        # 1. 过滤空值和None
        filtered = {k: v for k, v in params.items() 
                   if v is not None and str(v).strip() != ""}
        
        # 2. 排序（按key字母顺序）
        sorted_items = sorted(filtered.items(), key=lambda x: x[0])
        
        # 3. 拼接签名串
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_items])
        sign_str += f"&key={api_key}"
        
        # 4. MD5加密并转小写
        sign_result = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()
        
        return sign_result
    
    def rsa_sign(self, params: Dict, private_key: str) -> str:
        """
        RSA签名
        
        Args:
            params: 请求参数字典
            private_key: RSA私钥
            
        Returns:
            str: 签名结果（Base64编码）
        """
        # 1. 过滤空值
        filtered = {k: v for k, v in params.items() 
                   if v is not None and str(v).strip() != ""}
        
        # 2. 排序
        sorted_items = sorted(filtered.items(), key=lambda x: x[0])
        
        # 3. 拼接签名串
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_items])
        
        # 4. 加载私钥
        private_key_obj = serialization.load_pem_private_key(
            private_key.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        
        # 5. RSA签名
        signature = private_key_obj.sign(
            sign_str.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        # 6. Base64编码
        import base64
        return base64.b64encode(signature).decode('utf-8')
    
    def rsa_verify(self, params: Dict, signature: str, public_key: str) -> bool:
        """
        RSA签名验证
        
        Args:
            params: 请求参数字典
            signature: 待验证的签名
            public_key: RSA公钥
            
        Returns:
            bool: 签名是否有效
        """
        # 1. 过滤空值
        filtered = {k: v for k, v in params.items() 
                   if v is not None and str(v).strip() != ""}
        
        # 2. 排序
        sorted_items = sorted(filtered.items(), key=lambda x: x[0])
        
        # 3. 拼接签名串
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_items])
        
        # 4. 加载公钥
        public_key_obj = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            backend=default_backend()
        )
        
        # 5. Base64解码签名
        import base64
        signature_bytes = base64.b64decode(signature)
        
        try:
            # 6. 验证签名
            public_key_obj.verify(
                signature_bytes,
                sign_str.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def generate_signature_params(self, 
                                 params: Dict, 
                                 api_key: str,
                                 timestamp: Optional[str] = None,
                                 nonce: Optional[str] = None) -> Dict:
        """
        生成带签名的完整参数
        
        Args:
            params: 原始参数
            api_key: 签名密钥
            timestamp: 时间戳（可选，自动生成）
            nonce: 随机数（可选，自动生成）
            
        Returns:
            dict: 包含签名的完整参数
        """
        # 添加公共参数
        full_params = {
            "version": self.version,
            "timestamp": timestamp or self._generate_timestamp(),
            "nonce": nonce or self._generate_nonce(),
            **params
        }
        
        # 计算签名
        sign = self.md5_sign(full_params, api_key) if self.sign_type == "MD5" \
               else self.rsa_sign(full_params, self.config.get("accounts", {}).get("merchant", {}).get("rsa_private_key", ""))
        
        # 添加签名
        full_params["sign"] = sign
        full_params["signType"] = self.sign_type
        
        return full_params
    
    def _generate_timestamp(self) -> str:
        """生成时间戳"""
        return str(int(time.time()))
    
    def _generate_nonce(self) -> str:
        """生成随机数"""
        return str(int(random.random() * 1000000))


class RequestBuilder:
    """请求构建器"""
    
    def __init__(self, config: dict, endpoint: str):
        """
        初始化请求构建器
        
        Args:
            config: 配置字典
            endpoint: API端点
        """
        self.config = config
        self.endpoint = endpoint
        self.sign_manager = SignatureManager(config)
    
    def build_params(self,
                     method: str,
                     data: Dict,
                     timestamp: Optional[str] = None,
                     nonce: Optional[str] = None) -> Dict:
        """
        构建请求参数
        
        Args:
            method: 请求方法
            data: 请求数据
            timestamp: 时间戳
            nonce: 随机数
            
        Returns:
            dict: 完整请求参数
        """
        params = {
            "method": method,
            "bizContent": json.dumps(data, ensure_ascii=False),
            "timestamp": timestamp or self.sign_manager._generate_timestamp(),
            "nonce": nonce or self.sign_manager._generate_nonce()
        }
        
        # 获取API密钥
        api_key = self.config.get("accounts", {}).get("merchant", {}).get("md5_key", "")
        
        # 生成签名
        params["sign"] = self.sign_manager.md5_sign(params, api_key)
        params["signType"] = "MD5"
        
        return params


# ============== 便捷函数 ==============
def create_signature_manager(config_file: str = "./config/config.js") -> SignatureManager:
    """
    创建签名管理器（便捷函数）
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        SignatureManager: 签名管理器实例
    """
    import sys
    import os
    sys.path.insert(0, os.path.dirname(config_file))
    
    try:
        config_module = __import__("config")
        config = config_module.CONFIG
    except Exception as e:
        print(f"⚠️ 配置加载失败: {e}")
        config = {
            "sign": {"type": "MD5", "version": "6.0.0"},
            "accounts": {"merchant": {"md5_key": "your_md5_key"}}
        }
    
    return SignatureManager(config)


if __name__ == "__main__":
    # 测试签名模块
    print("=" * 60)
    print("CFB支付系统 - 签名模块测试")
    print("=" * 60)
    
    # 创建签名管理器
    sign_manager = create_signature_manager()
    
    # 测试MD5签名
    test_params = {
        "merchantId": "test_merchant_001",
        "orderNo": "ORDER123456",
        "amount": "100",
        "coinType": "USDT_TRC20"
    }
    
    api_key = "your_md5_key"
    sign = sign_manager.md5_sign(test_params, api_key)
    
    print(f"\n原始参数: {json.dumps(test_params, ensure_ascii=False, indent=2)}")
    print(f"\n签名结果: {sign}")
    
    # 验证签名
    sign_manager2 = create_signature_manager()
    verify_sign = sign_manager2.md5_sign(test_params, api_key)
    print(f"\n验证签名: {'✅ 成功' if sign == verify_sign else '❌ 失败'}")
    
    print("\n✅ 签名模块测试完成")
