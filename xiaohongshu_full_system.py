# 小红书自动化运营系统 - 整合版

import json
import os
import pickle
from datetime import datetime, timedelta
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class XiaoHongShuAutomationSystem:
    def __init__(self, config_file="xiaohongshu_config.json"):
        self.config_file = config_file
        self.config_manager = XiaoHongShuCrawlerConfig(config_file)
        self.cookie_manager = CookieManager(self.config_manager)
        self.driver = None
        
    def initialize_driver(self):
        """初始化浏览器驱动"""
        chrome_options = Options()
        # 可以根据需要添加选项
        # chrome_options.add_argument("--headless")  # 无头模式
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # 如果有保存的cookies，加载它们
        if self.config_manager.is_logged_in():
            cookies = self.config_manager.get_cookies()
            if cookies:
                self.driver.get("https://www.xiaohongshu.com")
                self.load_cookies_to_driver(cookies)
                
    def load_cookies_to_driver(self, cookies):
        """将cookies加载到浏览器驱动"""
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                print(f"加载cookie失败: {e}")
    
    def save_current_cookies(self):
        """保存当前浏览器的cookies"""
        cookies = self.driver.get_cookies()
        self.config_manager.update_login_info(
            username=self.get_user_nickname(), 
            cookies=cookies
        )
        # 同时保存到专用cookie文件
        self.cookie_manager.save_cookies(cookies)
        
    def get_user_nickname(self):
        """获取当前用户的昵称"""
        try:
            # 这里需要根据实际页面结构调整
            self.driver.get("https://www.xiaohongshu.com/user/profile/me")
            time.sleep(2)
            # 查找用户名元素，根据实际情况调整选择器
            nickname_element = self.driver.find_element(By.CSS_SELECTOR, ".nickname")
            return nickname_element.text
        except:
            return "unknown_user"
    
    def check_login_status(self):
        """检查登录状态"""
        if self.config_manager.is_logged_in():
            # 验证cookies是否仍然有效
            self.driver.get("https://www.xiaohongshu.com")
            time.sleep(2)
            
            # 尝试访问需要登录的页面来验证登录状态
            self.driver.get("https://creator.xiaohongshu.com/")
            time.sleep(2)
            
            # 检查页面是否有登录后的元素（需要根据实际页面结构调整）
            try:
                profile_element = self.driver.find_element(By.CSS_SELECTOR, ".creator-profile")
                return True
            except:
                # 如果没有找到预期的登录元素，认为登录失效
                self.config_manager.clear_login_info()
                return False
        return False
    
    def login_if_needed(self):
        """如果需要则执行登录"""
        if not self.check_login_status():
            print("需要登录...")
            # 这里需要实现登录逻辑
            # 注意：实际密码输入需要安全处理
            return self.perform_login()
        else:
            print("已登录，无需重复登录")
            return True
    
    def perform_login(self):
        """执行登录操作"""
        print("请手动完成登录...")
        # 导航到登录页面
        self.driver.get("https://www.xiaohongshu.com/login")
        print("请在浏览器中完成登录操作...")
        print("登录完成后，请按回车键继续...")
        input()  # 等待用户手动登录
        
        # 登录后保存cookies
        self.save_current_cookies()
        print("登录信息已保存")
        return True
    
    def post_note(self, title, content, image_paths=None, tags=None):
        """发布笔记"""
        if not self.login_if_needed():
            print("登录失败，无法发布笔记")
            return False
            
        try:
            # 导航到发布页面
            self.driver.get("https://creator.xiaohongshu.com/publish/publish?source=official_website")
            time.sleep(3)
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='publish-title-input']"))
            )
            
            # 输入标题
            title_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='publish-title-input']")
            title_input.clear()
            title_input.send_keys(title)
            
            # 输入内容
            content_textarea = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='publish-content-textarea']")
            content_textarea.clear()
            content_textarea.send_keys(content)
            
            # 上传图片（如果提供）
            if image_paths:
                for img_path in image_paths:
                    upload_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file'][accept='image/*']")
                    upload_input.send_keys(img_path)
                    time.sleep(2)  # 等待图片上传
            
            # 添加标签
            if tags:
                for tag in tags[:5]:  # 最多添加5个标签
                    tag_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='publish-tag-input']")
                    tag_input.clear()
                    tag_input.send_keys(tag.replace('#', '').strip())
                    time.sleep(1)
                    
                    # 选择第一个匹配的标签
                    try:
                        first_tag_option = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='tag-option']:first-child")
                        first_tag_option.click()
                    except:
                        # 如果没有找到建议标签，手动添加
                        tag_input.send_keys(" ")  # 添加空格以确认标签
            
            # 发布笔记
            publish_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='publish-button']"))
            )
            publish_button.click()
            
            time.sleep(3)  # 等待发布完成
            
            print(f"笔记发布成功: {title}")
            return True
            
        except Exception as e:
            print(f"发布失败: {str(e)}")
            return False
    
    def get_iphone_case_content(self):
        """获取iPhone壳相关内容"""
        templates = [
            {
                "title": "「绝美手机壳分享」这些iPhone壳真的太好看了！",
                "content": "姐妹们！今天来分享几款我最近入手的超美iPhone壳～\n真的是颜值与保护性并存！\n\n🌟 透明清水壳\n- 质感：超薄手感，不发黄\n- 保护：四角加厚防摔\n- 颜值：简约百搭\n\n🌟 彩色磨砂壳\n- 质感：磨砂工艺，不易留指纹\n- 保护：抗刮耐磨\n- 颜值：马卡龙色系，少女心爆棚\n\n✨ 使用感受：\n用了这么久，最推荐透明清水壳！既保护手机又不掩盖原机颜值～",
                "tags": ["#iPhone配件", "#手机壳推荐", "#苹果配件", "#开箱分享"]
            },
            {
                "title": "iPhone壳搭配学｜不同风格这样选手机壳",
                "content": "姐妹们！手机壳也是穿搭的一部分哦～\n今天教大家如何根据不同风格选择手机壳！\n\n👗 甜美风穿搭\n→ 选择：珍珠装饰、蝴蝶结元素、马卡龙色系\n→ 推荐：粉色渐变、奶油白贝壳纹\n\n💼 职场精英风\n→ 选择：纯色、极简设计、金属质感\n→ 推荐：黑色磨砂、香槟金边框\n\n🎯 酷girl风穿搭\n→ 选择：透明壳、涂鸦设计、几何图案\n→ 推荐：透明带链条、黑边框设计\n\n💡 小贴士：\n手机壳也要呼应整体造型哦～\n记得定期清洁手机壳保持美观！",
                "tags": ["#手机壳搭配", "#iPhone配件", "#穿搭技巧", "#生活美学"]
            }
        ]
        
        return random.choice(templates)
    
    def run_auto_posting_campaign(self, num_posts=3, interval_minutes=30):
        """运行自动发布活动"""
        for i in range(num_posts):
            print(f"正在发布第 {i+1} 篇笔记...")
            
            # 获取内容
            content_data = self.get_iphone_case_content()
            
            # 发布笔记
            success = self.post_note(
                title=content_data['title'],
                content=content_data['content'],
                tags=content_data['tags']
            )
            
            if success:
                print(f"第 {i+1} 篇笔记发布成功")
            else:
                print(f"第 {i+1} 篇笔记发布失败")
            
            # 等待下一次发布
            if i < num_posts - 1:
                print(f"等待 {interval_minutes} 分钟后发布下一篇...")
                time.sleep(interval_minutes * 60)
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()


# 使用示例
if __name__ == "__main__":
    system = XiaoHongShuAutomationSystem()
    
    try:
        # 初始化浏览器
        system.initialize_driver()
        
        # 发布单篇笔记测试
        content_data = system.get_iphone_case_content()
        system.post_note(
            title=content_data['title'],
            content=content_data['content'],
            tags=content_data['tags']
        )
        
        # 或者运行自动发布活动
        # system.run_auto_posting_campaign(num_posts=2, interval_minutes=5)
        
    finally:
        system.close()