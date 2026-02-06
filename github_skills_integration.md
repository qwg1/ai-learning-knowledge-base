# GitHub技能集成指南

## 已学习的技能

### 1. GitHub CLI技能
- OpenClaw内置了GitHub技能，可通过`gh`命令行工具与GitHub交互
- 支持PR管理、issue处理、CI/CD运行查看、API调用等功能

### 2. 技能创建器 (Skill Creator)
- 学习了如何创建和组织有效的AI技能
- 掌握了技能的结构：SKILL.md + 可选的scripts/references/assets
- 了解了渐进式信息披露的设计原则

## GitHub操作示例

### 仓库操作
```bash
# 创建新仓库
gh repo create <repository-name> --public

# 克隆仓库
gh repo clone <owner>/<repository>

# 推送文件
git add .
git commit -m "Add AI skills and daily summaries"
git push
```

### PR和Issue操作
```bash
# 创建PR
gh pr create --title "Add AI Agent skills" --body "Adding skills learned by AI agent"

# 查看PR状态
gh pr checks <pr-number>

# 列出issues
gh issue list
```

### API调用
```bash
# 使用API进行高级查询
gh api repos/<owner>/<repo>/issues --jq '.[].title'
```

## 实施计划

1. 手动完成GitHub认证（在浏览器中输入设备代码）
2. 创建AI技能仓库
3. 上传今日创建的技能文档
4. 设置自动同步机制（可选）

## 依赖项
- 已安装GitHub CLI (gh) 2.86.0
- 需要用户完成认证流程