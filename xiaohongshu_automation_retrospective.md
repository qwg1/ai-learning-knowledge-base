# 小红书自动化发布 - 经验总结

## 问题与解决方案

### 问题1: Profile参数被忽略
**症状**: 使用`--profile`参数时显示警告"daemon already running"
**原因**: agent-browser守护进程已在运行
**解决方案**:
```bash
agent-browser close && pkill -f agent-browser
sleep 2
agent-browser open "url" --profile "path"
```

### 问题2: 登录状态未生效
**症状**: 登录后再次打开仍要求登录
**原因**: 小红书使用多域名cookie系统
- xiaohongshu.com: 用户主站cookie
- creator.xiaohongshu.com: 创作者平台cookie
**解决方案**: 确保两个域名都有有效cookie

### 问题3: 多个相同文本元素
**症状**: `click "上传图文"` 返回strict mode violation
**原因**: 页面有3个"上传图文"元素
**解决方案**:
```javascript
document.querySelectorAll('span.title')[1].click()  // 第二个元素
```

### 问题4: 标题输入框无法定位
**症状**: `fill`命令失败
**原因**: 动态渲染页面，CSS选择器不稳定
**解决方案**:
```javascript
document.querySelector('input[placeholder="填写标题会有更多赞哦"]').value = '标题'
```

### 问题5: contenteditable元素无法设置
**症状**: textarea命令对div无效
**原因**: 正文使用 contenteditable div
**解决方案**:
```javascript
document.querySelector('[contenteditable]').innerText = '正文内容'
document.querySelector('[contenteditable]').innerHTML += '<br>#标签'
```

## 发布流程最佳实践

1. **启动浏览器**
   ```bash
   agent-browser close && sleep 2
   agent-browser open "https://creator.xiaohongshu.com/publish/publish?source=official_website" --profile ~/.xiaohongshu-profile
   ```

2. **等待页面加载**
   ```bash
   sleep 5
   agent-browser snapshot  # 检查页面元素
   ```

3. **切换到图文发布**
   ```javascript
   document.querySelectorAll('span.title')[1].click()
   ```

4. **上传图片**
   ```bash
   agent-browser upload @e1 "/path/to/image.jpg"
   ```

5. **填写内容**
   ```javascript
   // 标题
   document.querySelector('input[placeholder*="标题"]').value = '标题文本'
   
   // 正文
   document.querySelector('[contenteditable]').innerText = '正文内容'
   document.querySelector('[contenteditable]').innerHTML += '<br>#标签'
   ```

6. **发布**
   ```bash
   agent-browser click "发布"
   ```

## 常用JavaScript代码片段

### 获取元素
```javascript
document.querySelector('selector')  // 单个元素
document.querySelectorAll('selector')  // 所有元素
document.querySelectorAll('selector')[index]  // 指定索引
```

### 操作输入框
```javascript
element.value = '文本内容'
element.value = ''  // 清空
```

### 操作contenteditable
```javascript
element.innerText = '文本'
element.innerHTML = '<p>HTML内容</p>'
element.innerHTML += '<br>追加内容'
```

### 点击元素
```javascript
element.click()
```

### 获取元素文本
```javascript
element.innerText
element.textContent
```

## 注意事项

1. 每次操作后等待页面响应
2. 使用`agent-browser snapshot`检查页面状态
3. 复杂操作优先使用JavaScript
4. 保存登录状态到专用profile
5. 定期检查cookie有效期