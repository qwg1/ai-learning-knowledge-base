#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BS支付系统 - API测试项目

基于 https://doc.bs123.org/ API文档

支持:
1. USDT代收（下单、查询）
2. USDT代付（下单、查询）
3. 余额查询
4. 通道汇率查询
5. 签名验证

作者: OpenClaw
日期: 2026-02-11
"""

import os
import sys
import json
import time
import hashlib
import requests
from urllib.parse import urlencode, quote
from typing import Dict, Any, Optional, List
from datetime import datetime

# ============== 配置 ==============
CONFIG = {
    # 正式环境
    "production": {
        "base_url": "https://gateway.bishengusdt.com",
        "gateway": "https://gateway.bishengusdt.com"
    },
    
    # 测试环境
    "test": {
        "base_url": "https://test-gateway.cfbaopay.com",
        "gateway": "https://test-gateway.cfbaopay.com"
    },
    
    # 当前环境
    "current_env": "test",
    
    # 商户配置（示例）
    "merchant": {
        "id": "10216",  # 商户ID
        "md5_key": "",  # MD5密钥
        "rsa_private_key": "",  # RSA私钥
        "rsa_public_key": ""   # RSA公钥（平台公钥）
    },
    
    # 回调地址
    "notify_url": "https://your-callback-url.com/callback",
    
    # 请求超时
    "timeout": 30
}

# ============== 签名工具 ==============
class Signer:
    """签名工具类"""
    
    @staticmethod
    def md5_sign(params: Dict, secret_key: str) -> str:
        """
        MD5签名
        
        Args:
            params: 参数字典
            secret_key: 商户密钥
            
        Returns:
            签名字符串
        """
        # 1. 过滤空值参数
        filtered = {k: v for k, v in params.items() if v is not None and v != ""}
        
        # 2. 按键名ASCII排序
        sorted_keys = sorted(filtered.keys())
        
        # 3. 拼接键值对
        sign_str = "&".join([f"{k}={filtered[k]}" for k in sorted_keys])
        
        # 4. 追加密钥
        sign_str = f"{sign_str}&key={secret_key}"
        
        # 5. MD5加密（32位小写）
        return hashlib.md5(sign_str.encode()).hexdigest()
    
    @staticmethod
    def rsa_sign(params: Dict, private_key: str) -> str:
        """
        RSA签名（SHA1withRSA）
        
        Args:
            params: 参数字典
            private_key: RSA私钥
            
        Returns:
            签名字符串
        """
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.backends import default_backend
            
            # 1. 过滤空值参数
            filtered = {k: v for k, v in params.items() if v is not None and v != ""}
            
            # 2. 按键值+数值的ASCII编码顺序拼接
            sign_str = "&".join([f"{k}={filtered[k]}" for k in sorted(filtered.keys())])
            
            # 3. RSA私钥签名
            private_key_obj = serialization.load_pem_private_key(
                private_key.encode(),
                password=None,
                backend=default_backend()
            )
            
            signature = private_key_obj.sign(
                sign_str.encode(),
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            
            # 4. Base64编码
            import base64
            return base64.b64encode(signature).decode()
            
        except ImportError:
            print("❌ 需要安装cryptography库: pip install cryptography")
            return ""
    
    @staticmethod
    def rsa_verify(params: Dict, sign: str, public_key: str) -> bool:
        """
        RSA验签
        
        Args:
            params: 参数字典
            sign: 待验证签名
            public_key: RSA公钥
            
        Returns:
            验签结果
        """
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.backends import default_backend
            import base64
            
            # 1. 过滤空值参数
            filtered = {k: v for k, v in params.items() if v is not None and v != ""}
            
            # 2. 按键值+数值的ASCII编码顺序拼接
            sign_str = "&".join([f"{k}={filtered[k]}" for k in sorted(filtered.keys())])
            
            # 3. RSA公钥验签
            public_key_obj = serialization.load_pem_public_key(
                public_key.encode(),
                backend=default_backend()
            )
            
            public_key_obj.verify(
                base64.b64decode(sign),
                sign_str.encode(),
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            
            return True
            
        except Exception as e:
            print(f"❌ RSA验签失败: {e}")
            return False


# ============== API客户端 ==============
class BSClient:
    """BS支付API客户端"""
    
    def __init__(self, env: str = "test"):
        """
        初始化客户端
        
        Args:
            env: 环境（test/production）
        """
        self.base_url = CONFIG[env]["base_url"]
        self.config = CONFIG["merchant"]
        self.signer = Signer()
        
        print(f"\n🌐 初始化BS支付API客户端")
        print(f"   环境: {env}")
        print(f"   基础URL: {self.base_url}")
        print(f"   商户ID: {self.config['id']}")
    
    # ============== 辅助方法 ==============
    def _generate_order_no(self, prefix: str = "") -> str:
        """生成订单号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        import random
        random_suffix = str(random.randint(1000, 9999))
        return f"{prefix}{timestamp}{random_suffix}"
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    def _build_params(self, params: Dict, sign_type: str = "RSA") -> Dict:
        """
        构建请求参数（包含签名）
        
        Args:
            params: 原始参数
            sign_type: 签名类型（RSA/MD5）
            
        Returns:
            包含签名的完整参数
        """
        params["version"] = "6.0.0"
        params["merchantId"] = self.config["id"]
        
        # 生成签名
        if sign_type == "RSA":
            params["signType"] = "RSA"
            if self.config["rsa_private_key"]:
                params["sign"] = self.signer.rsa_sign(params, self.config["rsa_private_key"])
            else:
                print("⚠️ 未配置RSA私钥，跳过签名")
        else:
            params["signType"] = "MD5"
            if self.config["md5_key"]:
                params["sign"] = self.signer.md5_sign(params, self.config["md5_key"])
            else:
                print("⚠️ 未配置MD5密钥，跳过签名")
        
        return params
    
    def _request(self, endpoint: str, params: Dict, sign_type: str = "RSA") -> Dict:
        """
        发起HTTP请求
        
        Args:
            endpoint: API端点
            params: 请求参数
            sign_type: 签名类型
            
        Returns:
            响应结果
        """
        url = f"{self.base_url}{endpoint}"
        data = self._build_params(params, sign_type)
        
        print(f"\n📤 请求: {endpoint}")
        print(f"   URL: {url}")
        print(f"   参数: {json.dumps(data, ensure_ascii=False)}")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            response = requests.post(
                url,
                data=json.dumps(data),
                headers=headers,
                timeout=CONFIG["timeout"]
            )
            
            result = response.json()
            
            print(f"\n📥 响应:")
            print(f"   状态码: {response.status_code}")
            print(f"   响应体: {json.dumps(result, ensure_ascii=False)}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 请求失败: {e}")
            return {"code": -1, "msg": str(e)}
    
    # ============== USDT代收 ==============
    def create_collection_order(
        self,
        amount: str,
        coin_type: str,
        callback_currency_code: str,
        merchant_order_no: str = None,
        notify_url: str = None,
        rate: str = None
    ) -> Dict:
        """
        USDT代收下单（接口模式）
        
        Docs: https://doc.bs123.org/#2-usdt代收接口模式
        
        Args:
            amount: 订单金额
            coin_type: 订单币种（USDT_TRC20, CNY）
            callback_currency_code: 回调币种（USDT, CNY）
            merchant_order_no: 商户订单号（可选，自动生成）
            notify_url: 回调通知地址
            rate: 汇率（可选，仅CNY有效）
            
        Returns:
            API响应
        """
        if merchant_order_no is None:
            merchant_order_no = self._generate_order_no("CZ")
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "amount": amount,
            "coinType": coin_type,
            "callbackCurrencyCode": callback_currency_code,
            "notifyUrl": notify_url or CONFIG["notify_url"],
            "rate": rate
        }
        
        return self._request("/api/coin/payOrder/create", params)
    
    def create_collection_order_cashier(
        self,
        amount: str,
        coin_type: str,
        callback_currency_code: str,
        language: str = "zh",
        merchant_order_no: str = None,
        notify_url: str = None,
        return_url: str = None,
        rate: str = None
    ) -> Dict:
        """
        USDT代收下单（收银台模式）
        
        Docs: https://doc.bs123.org/#3-usdt代收收银台模式
        
        Args:
            amount: 订单金额
            coin_type: 订单币种
            callback_currency_code: 回调币种
            language: 收银台语言
            merchant_order_no: 商户订单号
            notify_url: 回调通知地址
            return_url: 支付成功后跳转地址
            rate: 汇率
            
        Returns:
            API响应（包含payUrl）
        """
        if merchant_order_no is None:
            merchant_order_no = self._generate_order_no("CZ")
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "amount": amount,
            "coinType": coin_type,
            "callbackCurrencyCode": callback_currency_code,
            "language": language,
            "notifyUrl": notify_url or CONFIG["notify_url"],
            "returnUrl": return_url,
            "rate": rate
        }
        
        return self._request("/api/coin/payOrder/createCashier", params)
    
    def query_collection_order(
        self,
        merchant_order_no: str,
        submit_time: str = None
    ) -> Dict:
        """
        USDT代收订单查询
        
        Docs: https://doc.bs123.org/#4-usdt代收订单查询
        
        Args:
            merchant_order_no: 商户订单号
            submit_time: 订单提交时间（格式: yyyyMMddHHmmss）
            
        Returns:
            API响应
        """
        if submit_time is None:
            submit_time = self._get_timestamp()
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "submitTime": submit_time
        }
        
        return self._request("/api/coin/payOrder/query", params)
    
    # ============== USDT代付 ==============
    def create_remit_order(
        self,
        amount: str,
        coin_type: str,
        booking_address: str,
        callback_currency_code: str,
        merchant_order_no: str = None,
        notify_url: str = None,
        remark: str = None,
        rate: str = None
    ) -> Dict:
        """
        USDT代付下单
        
        Docs: https://doc.bs123.org/#5-usdt代付下单
        
        Args:
            amount: 订单金额
            coin_type: 订单币种（USDT_TRC20, CNY）
            booking_address: 收款地址
            callback_currency_code: 回调币种
            merchant_order_no: 商户订单号
            notify_url: 回调通知地址
            remark: 备注
            rate: 汇率
            
        Returns:
            API响应
        """
        if merchant_order_no is None:
            merchant_order_no = self._generate_order_no("DF")
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "amount": amount,
            "coinType": coin_type,
            "bookingAddress": booking_address,
            "callbackCurrencyCode": callback_currency_code,
            "notifyUrl": notify_url or CONFIG["notify_url"],
            "remark": remark,
            "rate": rate
        }
        
        return self._request("/api/coin/remitOrder/create", params)
    
    def query_remit_order(
        self,
        merchant_order_no: str,
        submit_time: str = None
    ) -> Dict:
        """
        USDT代付订单查询
        
        Docs: https://doc.bs123.org/#6-usdt代付订单查询
        
        Args:
            merchant_order_no: 商户订单号
            submit_time: 订单提交时间
            
        Returns:
            API响应
        """
        if submit_time is None:
            submit_time = self._get_timestamp()
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "submitTime": submit_time
        }
        
        return self._request("/api/coin/remitOrder/query", params)
    
    # ============== 余额查询 ==============
    def query_balance(self, coin_type: str = "USDT") -> Dict:
        """
        余额查询
        
        Docs: https://doc.bs123.org/#9-余额查询
        
        Args:
            coin_type: 币种（USDT）
            
        Returns:
            API响应
        """
        params = {
            "coinType": coin_type,
            "requestTime": self._get_timestamp()
        }
        
        return self._request("/api/coin/balance/query", params)
    
    # ============== 通道汇率 ==============
    def query_channel_rate(self, coin_type: str) -> Dict:
        """
        商户通道汇率查询
        
        Docs: https://doc.bs123.org/#13-商户通道汇率获取
        
        Args:
            coin_type: 币种类型（USDT_TRC20, CNY）
            
        Returns:
            API响应
        """
        params = {
            "coinType": coin_type
        }
        
        return self._request("/api/merchant/queryChannelRate", params)
    
    # ============== 闪付 ==============
    def quick_query_address(
        self,
        member_no: str,
        coin_type: str = "USDT_TRC20"
    ) -> Dict:
        """
        闪付获取用户币地址
        
        Docs: https://doc.bs123.org/#11-闪付获取查询用户币地址
        
        Args:
            member_no: 用户唯一标识
            coin_type: 币种
            
        Returns:
            API响应
        """
        params = {
            "memberNo": member_no,
            "coinType": coin_type
        }
        
        return self._request("/api/coin/quick/queryAddress", params)
    
    # ============== CNY代付 ==============
    def create_cny_remit_order(
        self,
        amount: str,
        bank_code: str,
        bankcard_account_no: str,
        bankcard_account_name: str,
        merchant_order_no: str = None,
        member_no: str = None,
        notify_url: str = None
    ) -> Dict:
        """
        CNY-API代付下单
        
        Docs: https://doc.bs123.org/#14-cny-api代付下单
        
        Args:
            amount: 金额（元）
            bank_code: 银行编码
            bankcard_account_no: 银行卡号
            bankcard_account_name: 持卡人姓名
            merchant_order_no: 商户订单号
            member_no: 会员ID
            notify_url: 回调地址
            
        Returns:
            API响应
        """
        if merchant_order_no is None:
            merchant_order_no = self._generate_order_no("DF")
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "amount": amount,
            "bankCode": bank_code,
            "bankcardAccountNo": bankcard_account_no,
            "bankcardAccountName": bankcard_account_name,
            "memberNo": member_no,
            "notifyUrl": notify_url or CONFIG["notify_url"]
        }
        
        return self._request("/api/remitMatchOrder/create", params)
    
    def query_cny_remit_order(
        self,
        merchant_order_no: str,
        submit_time: str = None
    ) -> Dict:
        """
        CNY-API代付订单查询
        
        Docs: https://doc.bs123.org/#15-cny-api代付订单查询
        
        Args:
            merchant_order_no: 商户订单号
            submit_time: 订单提交时间
            
        Returns:
            API响应
        """
        if submit_time is None:
            submit_time = self._get_timestamp()
        
        params = {
            "merchantOrderNo": merchant_order_no,
            "submitTime": submit_time
        }
        
        return self._request("/api/remitMatchOrder/query", params)


# ============== 测试用例 ==============
class BSTestCases:
    """BS支付测试用例"""
    
    def __init__(self, env: str = "test"):
        """
        初始化测试
        
        Args:
            env: 环境
        """
        self.client = BSClient(env)
        self.results = []
    
    def log_result(self, name: str, success: bool, response: Dict = None):
        """记录测试结果"""
        self.results.append({
            "name": name,
            "success": success,
            "response": response
        })
        
        status = "✅ 通过" if success else "❌ 失败"
        print(f"\n{status} {name}")
    
    def test_collection_trc20(self) -> str:
        """
        测试USDT代收（TRC20）
        
        Returns:
            商户订单号
        """
        print("\n" + "="*60)
        print("🧪 测试: USDT代收（TRC20）")
        print("="*60)
        
        # 查询汇率
        rate_result = self.client.query_channel_rate("USDT_TRC20")
        print(f"\n📊 查询汇率: {rate_result}")
        
        # 下单
        result = self.client.create_collection_order(
            amount="10",
            coin_type="USDT_TRC20",
            callback_currency_code="USDT"
        )
        
        order_no = result.get("data", {}).get("merchantOrderNo") if result.get("code") == "0" else None
        
        self.log_result("USDT代收-TRC20", result.get("code") == "0", result)
        
        if order_no:
            # 查询订单
            query_result = self.client.query_collection_order(order_no)
            self.log_result("USDT代收查询", query_result.get("code") == "0", query_result)
        
        return order_no
    
    def test_collection_cny(self) -> str:
        """
        测试USDT代收（CNY）
        
        Returns:
            商户订单号
        """
        print("\n" + "="*60)
        print("🧪 测试: USDT代收（CNY）")
        print("="*60)
        
        result = self.client.create_collection_order(
            amount="100",
            coin_type="CNY",
            callback_currency_code="CNY",
            rate="8"  # 可选指定汇率
        )
        
        order_no = result.get("data", {}).get("merchantOrderNo") if result.get("code") == "0" else None
        
        self.log_result("USDT代收-CNY", result.get("code") == "0", result)
        
        return order_no
    
    def test_remit_trc20(self) -> str:
        """
        测试USDT代付（TRC20）
        
        Returns:
            商户订单号
        """
        print("\n" + "="*60)
        print("🧪 测试: USDT代付（TRC20）")
        print("="*60)
        
        result = self.client.create_remit_order(
            amount="1",
            coin_type="USDT_TRC20",
            booking_address="TYourAddress",
            callback_currency_code="USDT"
        )
        
        order_no = result.get("data", {}).get("merchantOrderNo") if result.get("code") == "0" else None
        
        self.log_result("USDT代付-TRC20", result.get("code") == "0", result)
        
        if order_no:
            # 查询订单
            time.sleep(2)  # 等待
            query_result = self.client.query_remit_order(order_no)
            self.log_result("USDT代付查询", query_result.get("code") == "0", query_result)
        
        return order_no
    
    def test_balance(self) -> Dict:
        """
        测试余额查询
        """
        print("\n" + "="*60)
        print("🧪 测试: 余额查询")
        print("="*60)
        
        result = self.client.query_balance("USDT")
        self.log_result("余额查询", result.get("code") == "0", result)
        
        return result
    
    def test_channel_rate(self) -> Dict:
        """
        测试通道汇率查询
        """
        print("\n" + "="*60)
        print("🧪 测试: 通道汇率查询")
        print("="*60)
        
        result = self.client.query_channel_rate("USDT_TRC20")
        self.log_result("通道汇率查询", result.get("code") == "0", result)
        
        return result
    
    def test_all(self) -> List[Dict]:
        """
        执行全部测试
        
        Returns:
            测试结果列表
        """
        print("\n" + "="*80)
        print("🚀 BS支付系统 - API自动化测试")
        print("="*80)
        print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 环境: {self.client.base_url}")
        print("="*80)
        
        # 依次执行测试
        self.test_channel_rate()
        self.test_balance()
        self.test_collection_trc20()
        self.test_collection_cny()
        self.test_remit_trc20()
        
        # 汇总结果
        print("\n" + "="*80)
        print("📊 测试结果汇总")
        print("="*80)
        
        passed = sum(1 for r in self.results if r["success"])
        failed = sum(1 for r in self.results if not r["success"])
        total = len(self.results)
        
        print(f"✅ 通过: {passed}")
        print(f"❌ 失败: {failed}")
        print(f"📝 总计: {total}")
        print(f"📈 通过率: {passed/total*100:.1f}%" if total > 0 else "📈 通过率: N/A")
        
        # 列出失败项
        if failed > 0:
            print("\n❌ 失败项:")
            for r in self.results:
                if not r["success"]:
                    print(f"   - {r['name']}: {r['response']}")
        
        return self.results


# ============== 主程序 ==============
def main():
    """主程序入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BS支付系统API测试")
    parser.add_argument("--env", "-e", choices=["test", "production"], 
                       default="test", help="环境配置")
    parser.add_argument("--test", "-t", choices=["all", "collection", "remit", "balance"],
                       default="all", help="测试类型")
    
    args = parser.parse_args()
    
    # 创建测试实例
    test_cases = BSTestCases(args.env)
    
    # 执行测试
    if args.test == "all":
        test_cases.test_all()
    elif args.test == "collection":
        test_cases.test_collection_trc20()
        test_cases.test_collection_cny()
    elif args.test == "remit":
        test_cases.test_remit_trc20()
    elif args.test == "balance":
        test_cases.test_balance()


if __name__ == "__main__":
    main()
