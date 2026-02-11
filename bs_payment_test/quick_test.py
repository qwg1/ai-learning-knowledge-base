#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BS支付系统 - 快速测试脚本

使用示例：
    python quick_test.py
    python quick_test.py --env test --test collection
    python quick_test.py --env production --test remit
"""

import sys
import time
from datetime import datetime

# 导入API客户端
from bs_api_client import BSClient, BSTestCases

# ============== 测试配置 ==============
QUICK_CONFIG = {
    "test": {
        "代收": {
            "trc20": {
                "amount": "10",
                "coin_type": "USDT_TRC20",
                "callback_currency_code": "USDT"
            },
            "cny": {
                "amount": "100",
                "coin_type": "CNY",
                "callback_currency_code": "CNY",
                "rate": "8"
            }
        },
        "代付": {
            "trc20": {
                "amount": "1",
                "coin_type": "USDT_TRC20",
                "booking_address": "TYourTRC20Address",
                "callback_currency_code": "USDT"
            },
            "bep20": {
                "amount": "1",
                "coin_type": "USDT_BEP20",
                "booking_address": "0xYourBEP20Address",
                "callback_currency_code": "USDT"
            }
        }
    },
    
    "production": {
        # 正式环境配置
    }
}


def print_header(title):
    """打印标题"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_step(step, message):
    """打印步骤"""
    print(f"\n{step}. {message}")


def test_collection(client, chain="TRC20"):
    """测试代收"""
    print_header(f"🧪 测试USDT代收（{chain}）")
    
    # 查询汇率
    print_step(1, "查询通道汇率...")
    rate_result = client.query_channel_rate(f"USDT_{chain}")
    print(f"   汇率查询: {'✅ 成功' if rate_result.get('code') == '0' else '❌ 失败'}")
    if rate_result.get("code") == "0":
        data = rate_result.get("data", {})
        print(f"   代收汇率: {data.get('collectionExchangeRate', 'N/A')}")
        print(f"   代付汇率: {data.get('paymentExchangeRate', 'N/A')}")
    
    # 下单
    print_step(2, "创建代收订单...")
    coin_type = f"USDT_{chain}" if chain != "CNY" else "CNY"
    callback_cc = "USDT" if chain != "CNY" else "CNY"
    
    result = client.create_collection_order(
        amount="10" if chain != "CNY" else "100",
        coin_type=coin_type,
        callback_currency_code=callback_cc
    )
    
    success = result.get("code") == "0"
    print(f"   下单结果: {'✅ 成功' if success else '❌ 失败'}")
    
    if success:
        data = result.get("data", {})
        order_no = data.get("merchantOrderNo")
        pay_address = data.get("bookingAddress")
        amount = data.get("payCoinAmount")
        expire = data.get("orderExpireDate")
        
        print(f"   商户单号: {order_no}")
        print(f"   收款地址: {pay_address}")
        print(f"   支付金额: {amount}")
        print(f"   过期时间: {expire}")
        
        # 查询订单
        print_step(3, "查询订单...")
        time.sleep(1)
        query_result = client.query_collection_order(order_no)
        print(f"   查询结果: {'✅ 成功' if query_result.get('code') == '0' else '❌ 失败'}")
        
        return order_no
    else:
        print(f"   错误信息: {result.get('msg')}")
        return None


def test_remit(client, chain="TRC20"):
    """测试代付"""
    print_header(f"🧪 测试USDT代付（{chain}）")
    
    # 下单
    print_step(1, "创建代付订单...")
    coin_type = f"USDT_{chain}"
    
    addresses = {
        "TRC20": "TYourTRC20Address",
        "BEP20": "0xYourBEP20Address",
        "ERC20": "0xYourERC20Address"
    }
    
    result = client.create_remit_order(
        amount="1",
        coin_type=coin_type,
        booking_address=addresses.get(chain, addresses["TRC20"]),
        callback_currency_code="USDT"
    )
    
    success = result.get("code") == "0"
    print(f"   下单结果: {'✅ 成功' if success else '❌ 失败'}")
    
    if success:
        data = result.get("data", {})
        order_no = data.get("merchantOrderNo")
        amount = data.get("amount")
        remit_amount = data.get("remitCoinAmount")
        status = data.get("status")
        
        print(f"   商户单号: {order_no}")
        print(f"   订单金额: {amount}")
        print(f"   出币数量: {remit_amount}")
        print(f"   状态: {status}")
        
        # 查询订单
        print_step(2, "查询订单...")
        time.sleep(2)
        query_result = client.query_remit_order(order_no)
        print(f"   查询结果: {'✅ 成功' if query_result.get('code') == '0' else '❌ 失败'}")
        
        if query_result.get("code") == "0":
            q_data = query_result.get("data", {})
            print(f"   订单状态: {q_data.get('status')}")
        
        return order_no
    else:
        print(f"   错误信息: {result.get('msg')}")
        return None


def test_balance(client):
    """测试余额查询"""
    print_header("🧪 测试余额查询")
    
    result = client.query_balance("USDT")
    success = result.get("code") == "0"
    print(f"\n   查询结果: {'✅ 成功' if success else '❌ 失败'}")
    
    if success:
        data = result.get("data", {})
        print(f"   可用余额: {data.get('availableAmount', 'N/A')} USDT")
        print(f"   冻结余额: {data.get('frozenAmount', 'N/A')} USDT")
        print(f"   待结算: {data.get('unsettledAmount', 'N/A')} USDT")
    
    return success


def run_tests(env="test", test_type="all"):
    """
    运行测试
    
    Args:
        env: 环境（test/production）
        test_type: 测试类型（all/collection/remit/balance）
    """
    print_header("🚀 BS支付系统 - API快速测试")
    print(f"\n📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 环境: {env}")
    print(f"🔧 测试: {test_type}")
    
    # 创建客户端
    client = BSClient(env)
    
    results = {}
    
    if test_type in ["all", "balance"]:
        results["balance"] = test_balance(client)
    
    if test_type in ["all", "collection"]:
        results["collection_trc20"] = test_collection(client, "TRC20")
        results["collection_cny"] = test_collection(client, "CNY")
    
    if test_type in ["all", "remit"]:
        results["remit_trc20"] = test_remit(client, "TRC20")
    
    # 汇总
    print_header("📊 测试结果汇总")
    
    for name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {name}: {status}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n📈 通过率: {passed}/{total} ({passed/total*100:.1f}%)" if total > 0 else "\n📈 无测试数据")
    
    return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BS支付系统 - API快速测试")
    parser.add_argument("--env", "-e", choices=["test", "production"],
                       default="test", help="环境")
    parser.add_argument("--test", "-t", 
                       choices=["all", "collection", "remit", "balance"],
                       default="all", help="测试类型")
    
    args = parser.parse_args()
    
    run_tests(args.env, args.test)


if __name__ == "__main__":
    main()
