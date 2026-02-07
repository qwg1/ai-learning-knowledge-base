# 小红书配置管理系统

import json
import os
from datetime import datetime, timedelta
import pickle
import requests

class XiaoHongShuCrawlerConfig:
    def __init__(self, config_file="xiaohongshu_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.default_config()
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def default_config(self):
        """默认配置"""
        return {
            "login_info": {
                "username": "",
                "password": "",  # 加密存储
                "cookies": [],
                "login_time": None,
                "is_logged_in": False
            },
            "automation_settings": {
                "auto_login": True,
                "post_interval": 300,  # 发帖间隔时间（秒）
                "max_daily_posts": 10,
                "use_proxy": False,
                "proxy_settings": {}
            },
            "content_settings": {
                "default_tags": [
                    "#iPhone配件", 
                    "#手机壳推荐", 
                    "#苹果配件", 
                    "#开箱分享",
                    "#手机壳搭配",
                    "#生活美学"
                ],
                "content_templates": {
                    "iphone_case_review": {
                        "title_pattern": "「绝了」这些iPhone壳真的太好看了！",
                        "content_structure": [
                            "开头引入",
                            "产品介绍", 
                            "使用体验",
                            "推荐理由"
                        ]
                    }
                }
            },
            "user_profile": {
                "user_id": "",
                "nickname": "",
                "avatar_url": "",
                "followers_count": 0,
                "following_count": 0
            }
        }
    
    def update_login_info(self, username, cookies, user_profile=None):
        """更新登录信息"""
        self.config['login_info']['username'] = username
        self.config['login_info']['cookies'] = cookies
        self.config['login_info']['login_time'] = datetime.now().isoformat()
        self.config['login_info']['is_logged_in'] = True
        
        if user_profile:
            self.config['user_profile'].update(user_profile)
        
        self.save_config()
    
    def get_cookies(self):
        """获取cookies"""
        return self.config['login_info']['cookies']
    
    def is_logged_in(self):
        """检查是否已登录"""
        login_info = self.config['login_info']
        if not login_info['is_logged_in']:
            return False
            
        # 检查登录时间是否超过7天
        if login_info['login_time']:
            login_time = datetime.fromisoformat(login_info['login_time'])
            if datetime.now() - login_time > timedelta(days=7):
                return False
                
        return len(login_info['cookies']) > 0
    
    def clear_login_info(self):
        """清除登录信息"""
        self.config['login_info']['cookies'] = []
        self.config['login_info']['login_time'] = None
        self.config['login_info']['is_logged_in'] = False
        self.config['user_profile'] = {}
        self.save_config()

# Cookie管理器
class CookieManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def save_cookies(self, cookies, filename="xiaohongshu_cookies.pkl"):
        """保存cookies到文件"""
        with open(filename, 'wb') as f:
            pickle.dump(cookies, f)
    
    def load_cookies(self, filename="xiaohongshu_cookies.pkl"):
        """从文件加载cookies"""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        return []
    
    def validate_cookies(self, cookies):
        """验证cookies是否有效"""
        # 这里可以实现一个简单的验证方法，比如访问一个需要登录的页面
        # 由于不能直接发起网络请求，这里只做基本格式验证
        return isinstance(cookies, list) and len(cookies) > 0

# 使用示例
if __name__ == "__main__":
    # 创建配置管理器
    config_manager = XiaoHongShuCrawlerConfig()
    
    # 创建Cookie管理器
    cookie_manager = CookieManager(config_manager)
    
    print("小红书配置管理系统初始化完成")
    print(f"当前登录状态: {'已登录' if config_manager.is_logged_in() else '未登录'}")