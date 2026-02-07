# 小红书自动化发布脚本

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random

def post_xiaohongshu_note(driver, title, content, image_paths, tags):
    """
    自动发布小红书笔记
    :param driver: WebDriver实例
    :param title: 笔记标题
    :param content: 笔记正文
    :param image_paths: 图片路径列表
    :param tags: 标签列表
    """
    try:
        # 打开发布页面
        driver.get("https://creator.xiaohongshu.com/publish/publish?source=official_website")
        time.sleep(3)
        
        # 等待编辑区域加载
        editor_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "note-editor"))
        )
        
        # 输入标题
        title_input = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='请输入标题']")
        title_input.clear()
        title_input.send_keys(title)
        
        # 输入内容
        content_textarea = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        content_textarea.clear()
        content_textarea.send_keys(content)
        
        # 上传图片
        upload_button = driver.find_element(By.CSS_SELECTOR, "div.upload-btn")
        for img_path in image_paths:
            upload_button.send_keys(img_path)
            time.sleep(1)  # 等待图片上传
        
        # 添加标签
        for tag in tags:
            tag_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='#话题']")
            tag_input.send_keys(tag)
            time.sleep(0.5)
            # 选择第一个推荐的话题
            tag_suggestion = driver.find_elements(By.CSS_SELECTOR, "div.tag-suggestion-item")
            if tag_suggestion:
                tag_suggestion[0].click()
        
        # 发布按钮
        publish_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.publish-btn"))
        )
        publish_button.click()
        
        print(f"笔记发布成功: {title}")
        return True
        
    except Exception as e:
        print(f"发布失败: {str(e)}")
        return False

def get_random_iphone_case_content():
    """
    获取随机的iPhone壳内容模板
    """
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
        },
        {
            "title": "iPhone壳避雷实录｜这些千万别买！",
            "content": "血泪教训！分享几个iPhone壳购买避雷指南\n\n❌ 雷区1：劣质透明壳\n- 问题：一个月就发黄、粘手汗\n- 避雷：选择品牌透明壳，有抗黄认证\n\n❌ 雷区2：过薄保护壳\n- 问题：轻微跌落就裂开\n- 避雷：选择四角加厚防摔款\n\n❌ 雷区3：材质刺鼻的壳\n- 问题：可能含有有害物质\n- 避雷：闻到刺鼻味道立即退货\n\n✅ 好物推荐：\n- 品牌：OtterBox、UAG、Apple官方\n- 材质：TPU软胶、PC硬壳、硅胶\n- 功能：MagSafe兼容、无线充电友好",
            "tags": ["#手机壳避雷", "#iPhone配件", "#购物指南", "#防踩坑"]
        }
    ]
    
    return random.choice(templates)

# 使用示例
if __name__ == "__main__":
    # 初始化WebDriver
    driver = webdriver.Chrome()  # 需要安装ChromeDriver
    
    try:
        # 获取随机内容
        content_data = get_random_iphone_case_content()
        
        # 发布笔记
        success = post_xiaohongshu_note(
            driver=driver,
            title=content_data['title'],
            content=content_data['content'],
            image_paths=[],  # 图片路径列表
            tags=content_data['tags']
        )
        
        if success:
            print("发布成功！")
        else:
            print("发布失败！")
            
    finally:
        driver.quit()