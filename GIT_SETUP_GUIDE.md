# Git仓库初始化指南

## 初始化本地仓库

1. 在项目目录中初始化仓库:
```bash
git init
```

2. 添加所有文件:
```bash
git add .
```

3. 创建初始提交:
```bash
git commit -m "Initial commit: AI Agent skills and daily learning summaries"
```

## 连接远程仓库

1. 在GitHub上创建新仓库后，添加远程仓库地址:
```bash
git remote add origin <your-github-repository-url>
```

2. 推送到GitHub:
```bash
git branch -M master          # 使用master分支
git push -u origin master     # 推送到master
```

## ⚠️ 重要提醒

- **只使用 master 分支**
- **不要创建 main 分支**
- **操作前先读知识库文档**
- **发现文档错误要及时更新**

## 已准备的文件

当前目录已包含以下文件:
- xiaohongshu_auto_publisher_skill.md (小红书自动发布技能)
- 2026-02-06_daily_learning_summary.md (每日学习总结)
- README.md (仓库说明文件)