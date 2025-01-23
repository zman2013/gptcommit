# GPTCommit

GPTCommit 是一个智能的 Git 提交消息生成工具，它使用 LLM (Large Language Model) 来自动生成符合 Conventional Commits 规范的提交消息。这个工具可以让你专注于编写代码，而不用花太多时间思考如何写提交消息。

## 特性

- 🤖 自动生成符合 Conventional Commits 规范的提交消息
- 🔒 安全的 API Key 管理（24小时缓存）
- 🎯 支持项目级别的开启/关闭配置
- 🌐 使用 DeepSeek API 生成高质量的提交消息
- 📝 支持中文提交消息（描述和正文部分）

## 安装

### 设置 API Key

方式1: macOS Keychain（最安全，推荐）
```bash
# 添加 API Key 到 Keychain
security add-generic-password -a deepseek-key -s deepseek-key -w 'your-api-key'

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

API Key 的获取优先级：
1. macOS Keychain
2. 环境变量
3. Git 配置

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

### 在仓库中启用/禁用 GPTCommit

```bash
# 启用 GPTCommit（会自动安装钩子）
gptcommit enable

# 禁用 GPTCommit（会移除钩子）
gptcommit disable
```

或者手动配置：
```bash
# 启用
git config gptcommit.enabled true
cp ~/.git-templates/hooks/prepare-commit-msg .git/hooks/
chmod +x .git/hooks/prepare-commit-msg

# 禁用
git config gptcommit.enabled false
rm .git/hooks/prepare-commit-msg
```

### 日常使用

启用后，只需要像平常一样使用 git commit 命令：

1. 暂存你的更改：
```bash
git add .
```

2. 提交更改：
```bash
git commit
```

GPTCommit 会自动生成一个符合 Conventional Commits 规范的提交消息。如果你对生成的消息不满意，可以在提交之前编辑它。

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

## 故障排除

1. 检查钩子是否正确安装：
```bash
ls -la .git/hooks/prepare-commit-msg
```

2. 确认 API Key 是否正确设置：
```bash
# 检查环境变量
echo $DEEPSEEK_API_KEY

# 或检查 git 配置
git config --get gptcommit.apikey
```

3. 检查 GPTCommit 是否已启用：
```bash
git config --get gptcommit.enabled
```

## 贡献

欢迎提交 Pull Requests 和 Issues！

## 许可证

MIT License
