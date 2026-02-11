#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BS支付系统 - 回调处理示例

包含：
1. 回调验签
2. 订单状态处理
3. 数据库更新

作者: OpenClaw
日期: 2026-02-11
"""

import json
import hashlib
from typing import Dict, Any
from datetime import datetime


class CallbackHandler:
    """回调处理器"""
    
    def __init__(self, md5_key: str = "", rsa_public_key: str = ""):
        """
        初始化
        
        Args:
            md5_key: MD5密钥
            rsa_public_key: RSA公钥（平台公钥）
        """
        self.md5_key = md5_key
        self.rsa_public_key = rsa_public_key
    
    def verify_md5_sign(self, params: Dict, sign: str) -> bool:
        """
        MD5验签
        
        Args:
            params: 回调参数
            sign: 待验证签名
            
        Returns:
            验签结果
        """
        # 过滤sign参数
        sign_data = {k: v for k, v in params.items() if k != "sign"}
        
        # 排序
        sorted_keys = sorted(sign_data.keys())
        
        # 拼接
        sign_str = "&".join([f"{k}={sign_data[k]}" for k in sorted_keys])
        sign_str = f"{sign_str}&key={self.md5_key}"
        
        # MD5加密
        calculated = hashlib.md5(sign_str.encode()).hexdigest()
        
        return calculated == sign
    
    def verify_rsa_sign(self, params: Dict, sign: str) -> bool:
        """
        RSA验签
        
        Args:
            params: 回调参数
            sign: 待验证签名
            
        Returns:
            验签结果
        """
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.backends import default_backend
            import base64
            
            # 过滤sign参数
            sign_data = {k: v for k, v in params.items() if k != "sign"}
            
            # 排序
            sorted_keys = sorted(sign_data.keys())
            
            # 拼接
            sign_str = "&".join([f"{k}={sign_data[k]}" for k in sorted_keys])
            
            # RSA验签
            public_key = serialization.load_pem_public_key(
                self.rsa_public_key.encode(),
                backend=default_backend()
            )
            
            public_key.verify(
                base64.b64decode(sign),
                sign_str.encode(),
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            
            return True
            
        except Exception as e:
            print(f"RSA验签失败: {e}")
            return False
    
    def handle_collection_callback(self, data: Dict) -> Dict:
        """
        处理代收回调
        
        Args:
            data: 回调数据
            
        Returns:
            处理结果
        """
        print("\n" + "="*60)
        print("📥 收到代收回调")
        print("="*60)
        
        # 解析数据
        merchant_order_no = data.get("merchantOrderNo")
        amount = data.get("amount")
        pay_amount = data.get("payCoinAmount")
        status = data.get("status")
        supplement_state = data.get("supplementOrderState")
        
        print(f"   商户单号: {merchant_order_no}")
        print(f"   订单金额: {amount}")
        print(f"   支付金额: {pay_amount}")
        print(f"   订单状态: {status} (0=处理中, 1=成功, 2=失败)")
        print(f"   补单状态: {supplement_state}")
        
        # 验签
        sign = data.get("sign", "")
        verify_method = data.get("signType", "MD5")
        
        if verify_method == "RSA":
            is_valid = self.verify_rsa_sign(data, sign)
        else:
            is_valid = self.verify_md5_sign(data, sign)
        
        print(f"   签名验证: {'✅ 通过' if is_valid else '❌ 失败'}")
        
        if not is_valid:
            return {"code": "fail", "msg": "签名验证失败"}
        
        # 处理业务逻辑
        # TODO: 更新数据库订单状态
        
        status_map = {
            "0": "处理中",
            "1": "成功",
            "2": "失败"
        }
        
        print(f"   业务状态: {status_map.get(str(status), '未知')}")
        
        # 返回成功
        return {"code": "success"}
    
    def handle_remit_callback(self, data: Dict) -> Dict:
        """
        处理代付回调
        
        Args:
            data: 回调数据
            
        Returns:
            处理结果
        """
        print("\n" + "="*60)
        print("📥 收到代付回调")
        print("="*60)
        
        # 解析数据
        merchant_order_no = data.get("merchantOrderNo")
        amount = data.get("amount")
        remit_amount = data.get("remitCoinAmount")
        status = data.get("status")
        
        print(f"   商户单号: {merchant_order_no}")
        print(f"   订单金额: {amount}")
        print(f"   出币数量: {remit_amount}")
        print(f"   订单状态: {status} (0=处理中, 1=成功, 2=失败)")
        
        # 验签
        sign = data.get("sign", "")
        verify_method = data.get("signType", "MD5")
        
        if verify_method == "RSA":
            is_valid = self.verify_rsa_sign(data, sign)
        else:
            is_valid = self.verify_md5_sign(data, sign)
        
        print(f"   签名验证: {'✅ 通过' if is_valid else '❌ 失败'}")
        
        if not is_valid:
            return {"code": "fail", "msg": "签名验证失败"}
        
        # 处理业务逻辑
        # TODO: 更新数据库订单状态
        
        return {"code": "success"}
    
    def handle_quick_pay_callback(self, data: Dict) -> Dict:
        """
        处理闪付回调
        
        Args:
            data: 回调数据
            
        Returns:
            处理结果
        """
        print("\n" + "="*60)
        print("📥 收到闪付回调")
        print("="*60)
        
        # 解析数据
        order_no = data.get("orderNo")
        merchant_order_no = data.get("merchantOrderNo")
        pay_amount = data.get("payCoinAmount")
        status = data.get("status")
        quick_state = data.get("quickState")
        
        print(f"   平台单号: {order_no}")
        print(f"   商户单号: {merchant_order_no}")
        print(f"   支付金额: {pay_amount}")
        print(f"   订单状态: {status}")
        print(f"   闪付状态: {quick_state}")
        
        # 验签
        sign = data.get("sign", "")
        is_valid = self.verify_rsa_sign(data, sign)
        print(f"   签名验证: {'✅ 通过' if is_valid else '❌ 失败'}")
        
        if not is_valid:
            return {"code": "fail", "msg": "签名验证失败"}
        
        return {"code": "success"}


# ============== 示例 ==============
def example_callbacks():
    """回调示例"""
    
    handler = CallbackHandler()
    
    # 示例代收回调数据
    collection_callback = {
        "merchantOrderNo": "CZ123456789",
        "merchantId": "10216",
        "amount": "10",
        "coinType": "USDT_TRC20",
        "payCoinAmount": "10",
        "callbackCurrencyCode": "USDT",
        "callbackOrderAmount": "10",
        "supplementOrderState": "0",
        "supplementOrderRemark": "",
        "status": "1",
        "signType": "MD5",
        "sign": "xxx"
    }
    
    # 处理代收回调
    result = handler.handle_collection_callback(collection_callback)
    print(f"\n📤 响应: {json.dumps(result)}")
    
    # 示例代付回调数据
    remit_callback = {
        "merchantOrderNo": "DF123456789",
        "merchantId": "10216",
        "amount": "1",
        "coinType": "USDT_TRC20",
        "remitCoinAmount": "1.0000",
        "callbackCurrencyCode": "USDT",
        "callbackOrderAmount": "1",
        "status": "1",
        "signType": "MD5",
        "sign": "xxx"
    }
    
    # 处理代付回调
    result = handler.handle_remit_callback(remit_callback)
    print(f"\n📤 响应: {json.dumps(result)}")


if __name__ == "__main__":
    example_callbacks()
