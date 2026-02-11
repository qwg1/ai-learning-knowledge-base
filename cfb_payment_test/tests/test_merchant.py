#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 商户管理测试
功能: 开新商户、商户配置、商户状态管理
"""

import json
import time
import random
import pytest
from typing import Optional, Dict


class TestMerchant:
    """商户管理测试类"""
    
    def __init__(self, config: dict, auth_manager, api_client):
        """
        初始化商户测试类
        
        Args:
            config: 配置字典
            auth_manager: 认证管理器
            api_client: API客户端
        """
        self.config = config
        self.auth = auth_manager
        self.api = api_client
    
    def test_create_merchant(self):
        """
        测试用例: 创建新商户
        用例编号: MERCHANT-001
        优先级: P0
        
        前置条件:
        1. 登录管理员账户
        
        测试步骤:
        1. 进入商户管理页面
        2. 点击新增商户
        3. 填写商户信息
        4. 提交审核
        5. 审核通过
        6. 激活商户
        
        预期结果:
        1. 商户创建成功
        2. 商户状态为"已激活"
        """
        print("\n" + "=" * 60)
        print("📝 测试创建新商户")
        print("=" * 60)
        
        # 获取管理员Session
        session = self.auth.get_authenticated_session("admin")
        if not session:
            pytest.skip("管理员登录失败")
        
        # 生成测试商户信息
        merchant_no = self._generate_merchant_no()
        merchant_info = {
            "merchantName": f"测试商户{merchant_no}",
            "merchantEmail": f"test{merchant_no}@example.com",
            "merchantPhone": f"138{random.randint(10000000, 99999999)}",
            "status": "PENDING"  # 待审核
        }
        
        # Step 1: 创建商户
        print("\n📤 Step 1: 创建商户...")
        result = self.api.create_merchant(session, merchant_info)
        
        if not result.get("success"):
            print(f"❌ 商户创建失败: {result.get('message')}")
            return {"success": False, "error": result.get('message')}
        
        print(f"✅ 商户创建成功: {result.get('merchantNo')}")
        
        # Step 2: 审核商户
        print("\n📤 Step 2: 审核商户...")
        approve_result = self.api.approve_merchant(session, result.get('merchantNo'))
        
        if not approve_result.get("success"):
            print(f"❌ 审核失败: {approve_result.get('message')}")
            return {"success": False, "error": approve_result.get('message')}
        
        print(f"✅ 审核通过")
        
        # Step 3: 验证商户状态
        print("\n📤 Step 3: 验证商户状态...")
        status_result = self.api.get_merchant_status(session, result.get('merchantNo'))
        
        if status_result.get("status") != "ACTIVE":
            print(f"❌ 商户状态异常: {status_result.get('status')}")
            return {"success": False, "error": f"商户状态为 {status_result.get('status')}"}
        
        print(f"✅ 商户已激活: {status_result.get('status')}")
        
        return {
            "success": True,
            "merchantNo": result.get('merchantNo'),
            "status": "ACTIVE"
        }
    
    def test_merchant_config(self):
        """
        测试用例: 商户配置
        用例编号: MERCHANT-002
        优先级: P1
        
        测试步骤:
        1. 登录商户
        2. 进入商户配置页面
        3. 配置API密钥
        4. 配置限额
        5. 绑定支付通道
        """
        print("\n" + "=" * 60)
        print("⚙️ 测试商户配置")
        print("=" * 60)
        
        session = self.auth.get_authenticated_session("merch")
        if not session:
            pytest.skip("商户登录失败")
        
        # 配置信息
        config_data = {
            "md5Key": self.config["accounts"]["merchant"]["md5_key"],
            "dailyLimit": "10000",
            "singleLimit": "1000",
            "callbackUrl": "https://your-domain.com/callback"
        }
        
        print("\n📤 配置商户...")
        result = self.api.update_merchant_config(session, config_data)
        
        if result.get("success"):
            print(f"✅ 配置更新成功")
            return {"success": True}
        else:
            print(f"❌ 配置失败: {result.get('message')}")
            return {"success": False, "error": result.get('message')}
    
    def test_bind_channel(self):
        """
        测试用例: 绑定支付通道
        用例编号: MERCHANT-003
        优先级: P1
        
        测试步骤:
        1. 查询可用通道
        2. 选择通道
        3. 绑定通道
        """
        print("\n" + "=" * 60)
        print("🔗 测试绑定通道")
        print("=" * 60)
        
        session = self.auth.get_authenticated_session("merch")
        if not session:
            pytest.skip("商户登录失败")
        
        # Step 1: 查询可用通道
        print("\n📤 查询可用通道...")
        channels = self.api.query_available_channels(session)
        
        if not channels:
            print("❌ 没有可用通道")
            return {"success": False, "error": "没有可用通道"}
        
        print(f"✅ 找到 {len(channels)} 个可用通道")
        
        # Step 2: 绑定通道
        channel_id = channels[0]["channelId"]
        print(f"\n📤 绑定通道: {channel_id}")
        
        bind_result = self.api.bind_channel(session, channel_id)
        
        if bind_result.get("success"):
            print(f"✅ 通道绑定成功")
            return {"success": True, "channelId": channel_id}
        else:
            print(f"❌ 绑定失败: {bind_result.get('message')}")
            return {"success": False, "error": bind_result.get('message')}
    
    def test_merchant_status_change(self):
        """
        测试用例: 商户状态变更
        用例编号: MERCHANT-004
        优先级: P1
        
        测试步骤:
        1. 冻结商户
        2. 解冻商户
        3. 禁用商户
        """
        print("\n" + "=" * 60)
        print("🔄 测试商户状态变更")
        print("=" * 60)
        
        session = self.auth.get_authenticated_session("admin")
        if not session:
            pytest.skip("管理员登录失败")
        
        merchant_no = self.config["test"]["merchant_info"]["name"].replace("测试商户", "")[-6:]
        
        # 测试冻结
        print("\n📤 冻结商户...")
        freeze_result = self.api.freeze_merchant(session, merchant_no)
        
        if not freeze_result.get("success"):
            print(f"❌ 冻结失败: {freeze_result.get('message')}")
        
        # 测试解冻
        print("\n📤 解冻商户...")
        unfreeze_result = self.api.unfreeze_merchant(session, merchant_no)
        
        if unfreeze_result.get("success"):
            print(f"✅ 解冻成功")
            return {"success": True}
        else:
            print(f"❌ 解冻失败: {unfreeze_result.get('message')}")
            return {"success": False, "error": unfreeze_result.get('message')}
    
    def test_query_merchant_list(self):
        """
        测试用例: 查询商户列表
        用例编号: MERCHANT-005
        优先级: P2
        
        测试步骤:
        1. 查询全部商户
        2. 按状态筛选
        3. 按名称搜索
        """
        print("\n" + "=" * 60)
        print("🔍 测试查询商户列表")
        print("=" * 60)
        
        session = self.auth.get_authenticated_session("admin")
        if not session:
            pytest.skip("管理员登录失败")
        
        # 查询全部
        print("\n📤 查询全部商户...")
        all_merchants = self.api.query_merchant_list(session, {})
        
        if all_merchants:
            print(f"✅ 找到 {len(all_merchants)} 个商户")
        else:
            print("❌ 查询失败或没有商户")
        
        # 按状态筛选
        print("\n📤 按状态筛选（ACTIVE）...")
        active_merchants = self.api.query_merchant_list(session, {"status": "ACTIVE"})
        print(f"✅ 找到 {len(active_merchants)} 个已激活商户")
        
        return {
            "success": True,
            "total": len(all_merchants),
            "active": len(active_merchants)
        }
    
    def _generate_merchant_no(self) -> str:
        """生成商户号"""
        return f"M{int(time.time())}{random.randint(1000, 9999)}"


# ============== 便捷函数 ==============
def run_merchant_tests(config_file: str = "./config/config.js"):
    """
    运行所有商户测试（便捷函数）
    
    Args:
        config_file: 配置文件路径
    """
    import sys
    import os
    sys.path.insert(0, os.path.dirname(config_file))
    sys.path.insert(0, os.path.dirname(os.path.dirname(config_file)))
    
    from config import CONFIG
    from auth import create_auth_manager
    from api import create_api_client
    
    # 创建认证管理器和API客户端
    auth = create_auth_manager(config_file)
    api = create_api_client(config_file)
    
    # 创建测试类
    test = TestMerchant(CONFIG, auth, api)
    
    # 运行测试
    tests = [
        ("创建商户", test.test_create_merchant),
        ("商户配置", test.test_merchant_config),
        ("绑定通道", test.test_bind_channel),
        ("状态变更", test.test_merchant_status_change),
        ("查询列表", test.test_query_merchant_list)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🚀 运行测试: {name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            results.append((name, "✅ 通过" if result.get("success") else "❌ 失败", result))
        except Exception as e:
            print(f"\n❌ 测试异常: {e}")
            results.append((name, "❌ 异常", str(e)))
    
    # 打印结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for name, status, result in results:
        print(f"{status} {name}")
    
    return results


if __name__ == "__main__":
    # 直接运行测试
    run_merchant_tests()
