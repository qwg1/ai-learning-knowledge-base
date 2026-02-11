#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - API客户端
封装所有API调用
"""

import json
import time
import requests
from typing import Optional, Dict, List


class APIClient:
    """API客户端"""
    
    def __init__(self, config: dict, auth_manager):
        """
        初始化API客户端
        
        Args:
            config: 配置字典
            auth_manager: 认证管理器
        """
        self.config = config
        self.auth = auth_manager
        self.session = requests.Session()
    
    def _request(self, 
                 method: str, 
                 endpoint: str, 
                 data: Dict = None,
                 use_auth: bool = True) -> Dict:
        """
        发起API请求
        
        Args:
            method: 请求方法
            endpoint: API端点
            data: 请求数据
            use_auth: 是否使用认证
            
        Returns:
            dict: 响应结果
        """
        url = endpoint
        
        # 如果需要认证，获取已认证的Session
        if use_auth:
            # 根据endpoint判断使用哪个系统
            if "/admin/" in endpoint:
                self.session = self.auth.get_authenticated_session("admin")
            elif "/agent/" in endpoint:
                self.session = self.auth.get_authenticated_session("agent")
            else:
                self.session = self.auth.get_authenticated_session("merch")
            
            if not self.session:
                return {"success": False, "error": "认证失败"}
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=data, timeout=30)
            else:
                response = self.session.post(url, json=data, timeout=30)
            
            return response.json()
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============== 商户管理API ==============
    
    def create_merchant(self, session, data: Dict) -> Dict:
        """创建商户"""
        # TODO: 根据实际接口修改
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/create"
        return self._request("POST", endpoint, data)
    
    def query_merchant_list(self, session, params: Dict = None) -> List:
        """查询商户列表"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/list"
        return self._request("POST", endpoint, params)
    
    def get_merchant_status(self, session, merchant_no: str) -> Dict:
        """查询商户状态"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/status"
        return self._request("POST", endpoint, {"merchantNo": merchant_no})
    
    def approve_merchant(self, session, merchant_no: str) -> Dict:
        """审核商户"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/approve"
        return self._request("POST", endpoint, {"merchantNo": merchant_no, "action": "APPROVE"})
    
    def freeze_merchant(self, session, merchant_no: str) -> Dict:
        """冻结商户"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/freeze"
        return self._request("POST", endpoint, {"merchantNo": merchant_no})
    
    def unfreeze_merchant(self, session, merchant_no: str) -> Dict:
        """解冻商户"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/unfreeze"
        return self._request("POST", endpoint, {"merchantNo": merchant_no})
    
    def update_merchant_config(self, session, config: Dict) -> Dict:
        """更新商户配置"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/merchant/config"
        return self._request("POST", endpoint, config)
    
    # ============== 通道管理API ==============
    
    def query_available_channels(self, session) -> List:
        """查询可用通道"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/channel/list"
        return self._request("POST", endpoint, {})
    
    def bind_channel(self, session, channel_id: str) -> Dict:
        """绑定通道"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/channel/bind"
        return self._request("POST", endpoint, {"channelId": channel_id})
    
    def query_channel_config(self, session) -> List:
        """查询通道配置"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/channel/config"
        return self._request("POST", endpoint, {})
    
    def update_channel_config(self, session, config: Dict) -> Dict:
        """更新通道配置"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/channel/config"
        return self._request("POST", endpoint, config)
    
    # ============== 交易API - 代收 ==============
    
    def create_collection_order(self, session, data: Dict) -> Dict:
        """创建代收订单"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/order/collection/create"
        return self._request("POST", endpoint, data)
    
    def query_collection_order(self, session, order_no: str) -> Dict:
        """查询代收订单"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/order/collection/query"
        return self._request("POST", endpoint, {"orderNo": order_no})
    
    # ============== 交易API - 代付 ==============
    
    def create_payment_order(self, session, data: Dict) -> Dict:
        """创建代付订单"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/order/payment/create"
        return self._request("POST", endpoint, data)
    
    def query_payment_order(self, session, order_no: str) -> Dict:
        """查询代付订单"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/order/payment/query"
        return self._request("POST", endpoint, {"orderNo": order_no})
    
    # ============== 退款API ==============
    
    def create_refund_order(self, session, data: Dict) -> Dict:
        """创建退款订单"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/order/refund/create"
        return self._request("POST", endpoint, data)
    
    def query_refund_order(self, session, order_no: str) -> Dict:
        """查询退款订单"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/order/refund/query"
        return self._request("POST", endpoint, {"orderNo": order_no})
    
    # ============== 补单API ==============
    
    def create_replenish_order(self, session, data: Dict) -> Dict:
        """创建补单"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/order/replenish/create"
        return self._request("POST", endpoint, data)
    
    def query_replenish_order(self, session, order_no: str) -> Dict:
        """查询补单"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/order/replenish/query"
        return self._request("POST", endpoint, {"orderNo": order_no})
    
    # ============== 调额API ==============
    
    def adjust_limit(self, session, data: Dict) -> Dict:
        """调整限额"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/merchant/limit/adjust"
        return self._request("POST", endpoint, data)
    
    def query_limit(self, session, merchant_no: str = None) -> Dict:
        """查询限额"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/merchant/limit/query"
        params = {"merchantNo": merchant_no} if merchant_no else {}
        return self._request("POST", endpoint, params)
    
    # ============== 转账API ==============
    
    def merchant_transfer(self, session, data: Dict) -> Dict:
        """商户间转账"""
        endpoint = f"{self.config['systems']['admin']['url']}/api/transfer/merchant"
        return self._request("POST", endpoint, data)
    
    # ============== 归集API ==============
    
    def manual_collection(self, session, data: Dict) -> Dict:
        """手动归集"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/collection/manual"
        return self._request("POST", endpoint, data)
    
    def auto_collection_status(self, session) -> Dict:
        """查询自动归集状态"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/collection/auto/status"
        return self._request("POST", endpoint, {})
    
    # ============== 账户API ==============
    
    def get_balance(self, session, coin_type: str = None) -> Dict:
        """查询余额"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/account/balance"
        params = {"coinType": coin_type} if coin_type else {}
        return self._request("POST", endpoint, params)
    
    def get_transaction_history(self, session, params: Dict = None) -> List:
        """查询交易历史"""
        endpoint = f"{self.config['systems']['merch']['url']}/api/account/history"
        return self._request("POST", endpoint, params or {})


# ============== 便捷函数 ==============
def create_api_client(config_file: str = "./config/config.js") -> APIClient:
    """
    创建API客户端（便捷函数）
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        APIClient: API客户端实例
    """
    import sys
    import os
    sys.path.insert(0, os.path.dirname(config_file))
    sys.path.insert(0, os.path.dirname(os.path.dirname(config_file)))
    
    from config import CONFIG
    from auth import create_auth_manager
    
    auth = create_auth_manager(config_file)
    return APIClient(CONFIG, auth)


if __name__ == "__main__":
    # 测试API客户端
    print("=" * 60)
    print("CFB支付系统 - API客户端测试")
    print("=" * 60)
    
    api = create_api_client()
    print("✅ API客户端初始化成功")
    
    print("\n可用的API方法:")
    methods = [method for method in dir(api) if not method.startswith('_')]
    for method in methods:
        print(f"  - {method}")
