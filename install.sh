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
echo "1. 设置 macOS Keychain（最安全，推荐）："
echo "   security add-generic-password -s deepseek-key -w 'your-api-key'"
echo "2. 设置环境变量："
echo "   export DEEPSEEK_API_KEY='your-api-key'"
echo "3. 设置git配置："
echo "   git config --global gptcommit.apikey 'your-api-key'"

echo -e "\n要在git仓库中启用GPTCommit，只需运行："
echo "   gptcommit enable"

echo -e "\n要禁用GPTCommit，运行："
echo "   gptcommit disable"

# 如果当前目录是git仓库，提示用户是否要启用
if [ -d ".git" ]; then
    echo -e "\n检测到当前目录是git仓库，你可以运行以下命令启用GPTCommit："
    echo "   gptcommit enable"
fi