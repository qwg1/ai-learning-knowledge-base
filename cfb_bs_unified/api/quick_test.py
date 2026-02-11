#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BS API 快速测试
"""
import sys
import json
import hashlib
import requests
from datetime import datetime
sys.path.insert(0, '.')

from config import CONFIG

def md5_sign(params, secret_key):
    """MD5签名"""
    filtered = {k: v for k, v in params.items() if v}
    sorted_keys = sorted(filtered.keys())
    sign_str = '&'.join([f'{k}={filtered[k]}' for k in sorted_keys])
    sign_str = f'{sign_str}&key={secret_key}'
    return hashlib.md5(sign_str.encode()).hexdigest()

def test_balance():
    """余额查询"""
    merchant = CONFIG['api']['merchant']
    base_url = CONFIG['api']['test']['base_url']
    
    params = {
        'merchantId': merchant['id'],
        'coinType': 'USDT',
        'requestTime': datetime.now().strftime('%Y%m%d%H%M%S'),
        'version': '6.0.0'
    }
    params['sign'] = md5_sign(params, merchant['md5_key'])
    
    response = requests.post(
        f'{base_url}/api/coin/balance/query',
        json=params,
        headers={'Content-Type': 'application/json'}
    )
    
    result = response.json()
    print('余额查询结果:', json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get('code') == '0':
        print('✅ 余额:', result.get('data', {}).get('balance'))
    else:
        print('❌ 失败:', result.get('msg'))

if __name__ == '__main__':
    test_balance()
