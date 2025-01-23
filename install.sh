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

echo "GPTCommit已安装完成！"
echo -e "\n首先需要设置 DeepSeek API Key，可以选择以下任一方式："
echo "1. 设置 macOS Keychain（最安全，推荐）："
echo "   security add-generic-password -s deepseek-key -w 'your-api-key'"
echo "2. 设置环境变量："
echo "   export DEEPSEEK_API_KEY='your-api-key'"
echo "3. 设置git配置："
echo "   git config --global gptcommit.apikey 'your-api-key'"

echo -e "\n使用方法："
echo "1. 自动生成提交消息："
echo "   gptcommit"
echo "2. 使用指定的提交消息："
echo "   gptcommit \"your commit message\""