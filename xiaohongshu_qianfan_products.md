# 小红书千帆商品数据获取系统

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│           小红书千帆商品数据获取系统                  │
├─────────────────────────────────────────────────────┤
│  1. 登录认证模块                                    │
│     - 千帆API认证                                    │
│     - Token管理                                      │
│     - 刷新机制                                       │
├─────────────────────────────────────────────────────┤
│  2. 商品数据获取模块                                 │
│     - 商品列表API                                     │
│     - 商品详情API                                     │
│     - 库存状态API                                    │
├─────────────────────────────────────────────────────┤
│  3. 数据处理模块                                     │
│     - JSON解析                                       │
│     - 数据清洗                                        │
│     - 状态筛选                                        │
├─────────────────────────────────────────────────────┤
│  4. 数据存储模块                                     │
│     - 本地JSON文件                                   │
│     - 数据库存储                                      │
│     - 定时更新                                        │
├─────────────────────────────────────────────────────┤
│  5. 发布集成模块                                     │
│     - 商品选择策略                                    │
│     - 自动关联                                        │
│     - 日志记录                                        │
└─────────────────────────────────────────────────────┘
```

## 配置文件 (config.json)

```json
{
  "qianfan": {
    "api_base": "https://gw.xiaohongshu.com",
    "app_key": "YOUR_APP_KEY",
    "app_secret": "YOUR_APP_SECRET"
  },
  "product_filter": {
    "status": "on_sale",  // on_sale: 在售中, all: 全部
    "fields": [
      "product_id",
      "title",
      "price",
      "stock",
      "status"
    ]
  },
  "storage": {
    "type": "json",  // json 或 database
    "path": "./data/products.json"
  },
  "update_interval": 3600  // 定时更新间隔（秒）
}
```

## 核心脚本

### 1. 认证模块 (auth.py)

```python
import requests
import time
from typing import Dict, Optional

class QianFanAuth:
    def __init__(self, config: Dict):
        self.config = config
        self.access_token = None
        self.refresh_token = None
        self.token_expire = 0
    
    def get_access_token(self) -> Optional[str]:
        """获取访问令牌"""
        if self.access_token and time.time() < self.token_expire:
            return self.access_token
        
        url = f"{self.config['api_base']}/auth/token"
        data = {
            "grant_type": "app_auth_code",
            "app_key": self.config['app_key'],
            "app_secret": self.config['app_secret']
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.access_token = result.get('access_token')
            self.refresh_token = result.get('refresh_token')
            self.token_expire = time.time() + result.get('expires_in', 7200)
            return self.access_token
        return None
    
    def refresh_access_token(self):
        """刷新访问令牌"""
        url = f"{self.config['api_base']}/auth/token/refresh"
        data = {
            "grant_type": "refresh_token",
            "app_key": self.config['app_key'],
            "app_secret": self.config['app_secret'],
            "refresh_token": self.refresh_token
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.access_token = result.get('access_token')
            self.refresh_token = result.get('refresh_token')
            self.token_expire = time.time() + result.get('expires_in', 7200)
```

### 2. 商品获取模块 (products.py)

```python
import requests
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class QianFanProducts:
    def __init__(self, auth: QianFanAuth, config: Dict):
        self.auth = auth
        self.config = config
        self.api_base = config['api_base']
    
    def get_product_list(
        self,
        page: int = 1,
        page_size: int = 50,
        status: str = None
    ) -> Dict:
        """获取商品列表"""
        url = f"{self.api_base}/product/list"
        
        headers = {
            "Authorization": f"Bearer {self.auth.get_access_token()}",
            "Content-Type": "application/json"
        }
        
        params = {
            "page_no": page,
            "page_size": page_size,
            "app_key": self.auth.config['app_key']
        }
        
        if status:
            params["status"] = status
        
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def get_all_products(
        self,
        status: str = "on_sale"
    ) -> List[Dict]:
        """获取所有商品（分页获取）"""
        all_products = []
        page = 1
        
        while True:
            result = self.get_product_list(page=page, status=status)
            
            if result.get('code') != 0:
                break
            
            products = result.get('data', {}).get('products', [])
            if not products:
                break
            
            all_products.extend(products)
            
            # 检查是否还有更多
            total = result.get('data', {}).get('total', 0)
            if len(all_products) >= total:
                break
            
            page += 1
        
        return all_products
    
    def filter_on_sale(self, products: List[Dict]) -> List[Dict]:
        """筛选在售中的商品"""
        return [
            p for p in products
            if p.get('status') == 'ON_SALE'
        ]
```

### 3. 数据存储模块 (storage.py)

```python
import json
import os
from typing import List, Dict
from datetime import datetime

class ProductStorage:
    def __init__(self, config: Dict):
        self.config = config
        self.storage_type = config.get('type', 'json')
        self.storage_path = config.get('path', './data/products.json')
    
    def save_products(self, products: List[Dict]):
        """保存商品数据"""
        if self.storage_type == 'json':
            self._save_to_json(products)
        else:
            # 可以扩展为数据库存储
            self._save_to_json(products)
    
    def _save_to_json(self, products: List[Dict]):
        """保存为JSON文件"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        
        data = {
            "updated_at": datetime.now().isoformat(),
            "total_count": len(products),
            "products": products
        }
        
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_products(self) -> List[Dict]:
        """加载商品数据"""
        if not os.path.exists(self.storage_path):
            return []
        
        with open(self.storage_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('products', [])
    
    def get_on_sale_products(self) -> List[Dict]:
        """获取在售商品"""
        products = self.load_products()
        return [p for p in products if p.get('status') == 'ON_SALE']
```

### 4. 主程序 (main.py)

```python
#!/usr/bin/env python3

import json
import argparse
from auth import QianFanAuth
from products import QianFanProducts
from storage import ProductStorage

def main():
    parser = argparse.ArgumentParser(description='小红书千帆商品数据获取')
    parser.add_argument('--config', default='config.json', help='配置文件路径')
    parser.add_argument('--status', default='on_sale', choices=['all', 'on_sale', 'off_sale'], help='商品状态筛选')
    parser.add_argument('--output', default='./data/products.json', help='输出文件路径')
    args = parser.parse_args()
    
    # 加载配置
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    # 初始化模块
    auth = QianFanAuth(config['qianfan'])
    products = QianFanProducts(auth, config['qianfan'])
    storage = ProductStorage(config['storage'])
    
    # 获取商品数据
    print("正在获取商品列表...")
    all_products = products.get_all_products(status=args.status if args.status != 'all' else None)
    
    # 筛选在售商品（如果需要）
    if args.status == 'on_sale':
        filtered = products.filter_on_sale(all_products)
    else:
        filtered = all_products
    
    # 保存数据
    storage.save_products(filtered)
    
    print(f"✅ 获取完成！共 {len(filtered)} 个商品")
    print(f"📁 数据已保存到: {args.output}")
    
    # 打印前5个商品
    print("\n📦 商品预览：")
    for i, p in enumerate(filtered[:5]):
        print(f"  {i+1}. {p.get('title', 'N/A')} - ¥{p.get('price', 'N/A')} - {p.get('status', 'N/A')}")

if __name__ == '__main__':
    main()
```

## 使用方法

### 1. 准备工作

```bash
# 创建项目目录
mkdir xiaohongshu-products
cd xiaohongshu-products

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install requests

# 创建配置文件
cp config.example.json config.json
# 编辑config.json填入你的API密钥
```

### 2. 配置API密钥

编辑 `config.json`：

```json
{
  "qianfan": {
    "api_base": "https://gw.xiaohongshu.com",
    "app_key": "你的AppKey",
    "app_secret": "你的AppSecret"
  },
  "product_filter": {
    "status": "on_sale"
  },
  "storage": {
    "type": "json",
    "path": "./data/products.json"
  },
  "update_interval": 3600
}
```

### 3. 获取商品数据

```bash
# 获取所有在售商品
python main.py --status on_sale

# 获取所有商品
python main.py --status all
```

### 4. 定时更新（使用cron）

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天凌晨2点更新）
0 2 * * * /path/to/venv/bin/python /path/to/main.py --status on_sale >> /var/log/xiaohongshu_products.log 2>&1
```

## 输出示例

```json
{
  "updated_at": "2026-02-08T15:30:00",
  "total_count": 25,
  "products": [
    {
      "product_id": "67e9396615a1180015b5240d",
      "title": "塔下 韩系简约波点苹果16手机壳",
      "price": 13.00,
      "stock": 100,
      "status": "ON_SALE",
      "specifications": [
        {
          "spec_id": "xxx",
          "name": "哑光银 迷你小粉波/13"
        }
      ]
    }
  ]
}
```

## 注意事项

1. **API权限**：需要申请小红书千帆API权限
2. **Token管理**：Access Token有效期约2小时，需自动刷新
3. **频率限制**：注意API调用频率限制
4. **数据安全**：妥善保管API密钥，不要提交到版本控制

## 后续扩展

- [ ] 数据库存储支持（MySQL/PostgreSQL）
- [ ] Web管理界面
- [ ] 发布时自动选择商品
- [ ] 库存不足预警
- [ ] 数据分析报表