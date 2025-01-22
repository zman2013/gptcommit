#!/bin/bash

# 复制gptcommit.py到用户bin目录
mkdir -p ~/.local/bin
cp gptcommit.py ~/.local/bin/gptcommit
chmod +x ~/.local/bin/gptcommit

# 添加~/.local/bin到PATH（如果还没有）
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"
fi

# 创建git hook模板
HOOK_TEMPLATE_DIR=~/.git-templates/hooks
mkdir -p "$HOOK_TEMPLATE_DIR"

# 创建prepare-commit-msg钩子
cat > "$HOOK_TEMPLATE_DIR/prepare-commit-msg" << 'EOF'
#!/bin/sh
gptcommit "$1"
EOF

chmod +x "$HOOK_TEMPLATE_DIR/prepare-commit-msg"

# 设置git使用这个模板目录
git config --global init.templateDir ~/.git-templates

echo "GPTCommit已安装完成！"
echo -e "\n首先需要设置 DeepSeek API Key，可以选择以下任一方式："
echo "1. 设置环境变量（推荐）："
echo "   export DEEPSEEK_API_KEY='your-api-key'"
echo "2. 设置git配置："
echo "   git config --global gptcommit.apikey 'your-api-key'"

echo -e "\n要在现有的git仓库中启用GPTCommit，请按以下步骤操作："
echo "1. 运行以下命令启用GPTCommit："
echo "   git config gptcommit.enabled true"
echo "2. 复制钩子到当前仓库："
echo "   cp ~/.git-templates/hooks/prepare-commit-msg .git/hooks/"
echo "   chmod +x .git/hooks/prepare-commit-msg"

# 验证钩子是否生效
echo -e "\n验证钩子是否生效:"
echo "1. 在git仓库中运行 'ls -la .git/hooks' 检查prepare-commit-msg钩子是否存在"
echo "2. 确认钩子文件有执行权限(应显示-rwxr-xr-x)"
echo "3. 尝试进行一次git commit，如果看到生成的commit message则说明钩子生效"

# 如果当前目录是git仓库，自动安装钩子
if [ -d ".git" ]; then
    echo -e "\n检测到当前目录是git仓库，正在自动安装钩子..."
    cp ~/.git-templates/hooks/prepare-commit-msg .git/hooks/
    chmod +x .git/hooks/prepare-commit-msg
    echo "钩子已安装到当前仓库"
fi