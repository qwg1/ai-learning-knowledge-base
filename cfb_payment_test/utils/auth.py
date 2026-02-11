#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFB支付系统 - 认证模块
支持: Cookie认证、Token认证

功能:
1. 登录获取Cookie
2. Cookie管理（保存/加载）
3. Token刷新
"""

import json
import os
import time
import requests
from typing import Optional, Dict


class AuthManager:
    """认证管理器"""
    
    def __init__(self, config: dict):
        """
        初始化认证管理器
        
        Args:
            config: 配置字典，包含账户信息
        """
        self.config = config
        self.cookies_dir = "./config/cookies"
        self.session = requests.Session()
        
        # 确保cookie目录存在
        os.makedirs(self.cookies_dir, exist_ok=True)
    
    def login(self, system: str, username: str, password: str) -> Dict:
        """
        登录系统获取Cookie
        
        Args:
            system: 系统名称 (admin/agent/merch)
            username: 用户名
            password: 密码
            
        Returns:
            dict: 登录结果和Cookie
        """
        base_url = self.config["systems"][system]["url"]
        login_url = f"{base_url}/api/login"
        
        print(f"📤 登录 {self.config['systems'][system]['name']}...")
        
        try:
            # TODO: 根据实际登录接口修改
            login_data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(login_url, json=login_data, timeout=30)
            result = response.json()
            
            if result.get("code") == "0":
                print(f"✅ 登录成功")
                # 保存Cookie
                self._save_cookies(system, self.session.cookies.get_dict())
                return {"success": True, "cookies": self.session.cookies.get_dict()}
            else:
                print(f"❌ 登录失败: {result.get('msg')}")
                return {"success": False, "error": result.get('msg')}
                
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_cookies(self, system: str, cookies: Dict):
        """
        保存Cookie到文件
        
        Args:
            system: 系统名称
            cookies: Cookie字典
        """
        cookie_file = os.path.join(self.cookies_dir, f"{system}_cookies.json")
        
        cookie_data = {
            "system": system,
            "cookies": cookies,
            "save_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Cookie已保存: {cookie_file}")
    
    def load_cookies(self, system: str) -> Optional[Dict]:
        """
        从文件加载Cookie
        
        Args:
            system: 系统名称
            
        Returns:
            dict: Cookie字典，如果不存在返回None
        """
        cookie_file = os.path.join(self.cookies_dir, f"{system}_cookies.json")
        
        if not os.path.exists(cookie_file):
            print(f"⚠️ Cookie文件不存在: {cookie_file}")
            return None
        
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
        
        # 检查Cookie是否过期（简单判断：保存时间超过24小时）
        save_time = time.strptime(cookie_data["save_time"], "%Y-%m-%d %H:%M:%S")
        save_timestamp = time.mktime(save_time)
        
        if time.time() - save_timestamp > 24 * 3600:
            print(f"⚠️ Cookie已过期（超过24小时）")
            return None
        
        print(f"📂 Cookie已加载: {system}")
        return cookie_data["cookies"]
    
    def get_authenticated_session(self, system: str) -> Optional[requests.Session]:
        """
        获取已认证的Session
        
        Args:
            system: 系统名称
            
        Returns:
            Session: 已设置Cookie的Session，如果认证失败返回None
        """
        # 尝试加载已有Cookie
        cookies = self.load_cookies(system)
        
        if cookies:
            self.session.cookies.update(cookies)
            
            # 验证Cookie是否有效
            if self._verify_session(system):
                return self.session
        
        # 需要重新登录
        account_key = "admin" if system == "admin" else "merchant"
        account = self.config["accounts"][account_key]
        
        username_key = "username" if "username" in account else "id"
        username = account[username_key]
        password = account.get("password", "")
        
        result = self.login(system, username, password)
        
        if result["success"]:
            return self.session
        
        return None
    
    def _verify_session(self, system: str) -> bool:
        """
        验证Session是否有效
        
        Args:
            system: 系统名称
            
        Returns:
            bool: Session是否有效
        """
        base_url = self.config["systems"][system]["url"]
        verify_url = f"{base_url}/api/user/info"
        
        try:
            response = self.session.get(verify_url, timeout=10)
            result = response.json()
            
            if result.get("code") == "0":
                print(f"✅ Session验证成功")
                return True
            else:
                print(f"⚠️ Session验证失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"⚠️ Session验证异常: {e}")
            return False


class TokenAuth:
    """Token认证类（用于API调用）"""
    
    def __init__(self, config: dict):
        self.config = config
        self.token = None
        self.expire_time = None
    
    def get_token(self) -> Optional[str]:
        """
        获取Token
        
        Returns:
            str: Token字符串
        """
        # 检查Token是否过期
        if self.token and self.expire_time and time.time() < self.expire_time:
            return self.token
        
        # 重新获取Token
        return self._refresh_token()
    
    def _refresh_token(self) -> Optional[str]:
        """
        刷新Token
        
        Returns:
            str: 新Token
        """
        # TODO: 根据实际接口修改
        print("🔄 刷新Token...")
        
        merchant = self.config["accounts"]["merchant"]
        
        token_url = "https://api.cfbaopay.com/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": merchant["id"],
            "client_secret": merchant["api_key"]
        }
        
        try:
            response = requests.post(token_url, json=token_data, timeout=30)
            result = response.json()
            
            if result.get("code") == "0":
                self.token = result["data"]["access_token"]
                self.expire_time = time.time() + result["data"]["expires_in"]
                print(f"✅ Token获取成功")
                return self.token
            else:
                print(f"❌ Token获取失败: {result.get('msg')}")
                return None
                
        except Exception as e:
            print(f"❌ Token获取异常: {e}")
            return None
    
    def get_auth_headers(self) -> Dict:
        """
        获取认证头
        
        Returns:
            dict: 包含Authorization的请求头
        """
        token = self.get_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}


# ============== 便捷函数 ==============
def create_auth_manager(config_file: str = "./config/config.js") -> AuthManager:
    """
    创建认证管理器（便捷函数）
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        AuthManager: 认证管理器实例
    """
    # 加载配置
    import sys
    sys.path.insert(0, os.path.dirname(config_file))
    
    try:
        config_module = __import__("config")
        config = config_module.CONFIG
    except Exception as e:
        print(f"⚠️ 配置加载失败: {e}")
        print("使用默认配置...")
        config = {
            "systems": {
                "admin": {"url": "https://test-admin.cfbaopay.com"},
                "agent": {"url": "https://test-agent.cfbaopay.com"},
                "merch": {"url": "https://test-merch.cfbaopay.com"}
            },
            "accounts": {
                "admin": {"username": "admin", "password": ""},
                "merchant": {"id": "", "api_key": "", "md5_key": ""}
            }
        }
    
    return AuthManager(config)


if __name__ == "__main__":
    # 测试认证模块
    print("=" * 60)
    print("CFB支付系统 - 认证模块测试")
    print("=" * 60)
    
    auth = create_auth_manager()
    
    # 测试登录（需要配置真实账户）
    # result = auth.login("admin", "admin", "password")
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n✅ 认证模块加载成功")
    print("\n使用方法:")
    print("  auth = create_auth_manager()")
    print("  session = auth.get_authenticated_session('admin')")
