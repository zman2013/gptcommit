# GPTCommit

GPTCommit 是一个智能的 Git 提交消息生成工具，它使用 LLM (Large Language Model) 来自动生成符合 Conventional Commits 规范的提交消息。这个工具可以让你专注于编写代码，而不用花太多时间思考如何写提交消息。

## 特性

- 🤖 自动生成符合 Conventional Commits 规范的提交消息
- 🔒 安全的 API Key 管理
- 🌐 使用 DeepSeek API 生成高质量的提交消息
- 📝 支持中文提交消息（描述和正文部分）
- ✨ 简单直观的命令行界面

## 安装

### 设置 API Key

方式1: macOS Keychain（最安全，推荐）
```bash
# 添加 API Key 到 Keychain
security add-generic-password -s deepseek-key -w 'your-api-key'

# 验证是否添加成功
security find-generic-password -s deepseek-key -w
```

方式2: 环境变量
```bash
export DEEPSEEK_API_KEY='your-api-key'
```

方式3: Git 配置
```bash
git config --global gptcommit.apikey 'your-api-key'
```

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/gptcommit.git
cd gptcommit
```

2. 运行安装脚本：
```bash
chmod +x install.sh
./install.sh
```

## 使用方法

### 自动生成提交消息

在 git 仓库中运行：
```bash
git add .  # 暂存你的更改
gptcommit   # 自动生成并提交
```

工具会显示生成的提交消息，并询问你是否接受。输入 Y 确认提交，输入 N 取消提交。

### 使用指定的提交消息

如果你想使用自己的提交消息：
```bash
gptcommit "your commit message"
```

## 提交消息格式

GPTCommit 生成的提交消息遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范，格式如下：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

其中：
- type 和 scope 使用英文
- description、body 和 footer 使用中文
- type 可以是：feat、fix、docs、style、refactor、perf、test、chore 等

示例：
```
feat(auth): 添加用户认证功能

- 实现基于 JWT 的身份验证
- 添加登录和注册接口
- 创建用户模型和数据迁移
```

## 贡献

欢迎提交 Pull Requests 和 Issues！

## 许可证

MIT License
