#!/bin/bash

# 复制gptcommit.py到用户bin目录
mkdir -p ~/.local/bin
cp gptcommit.py ~/.local/bin/gptcommit
chmod +x ~/.local/bin/gptcommit

# 添加~/.local/bin到PATH
# 为 bash 添加 PATH
if [ -f ~/.bashrc ]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

# 为 zsh 添加 PATH
if [ -f ~/.zshrc ]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
fi

# 为 fish 添加配置
if [ -f ~/.config/fish/config.fish ]; then
    echo -e "\n# GPTCommit PATH configuration" >> ~/.config/fish/config.fish
    echo 'if test -d ~/.local/bin' >> ~/.config/fish/config.fish
    echo '    fish_add_path ~/.local/bin' >> ~/.config/fish/config.fish
    echo 'end' >> ~/.config/fish/config.fish
fi

# 立即更新当前会话的 PATH
export PATH="$HOME/.local/bin:$PATH"

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
echo "3. 制定语言："
echo "   gptcommit -l en"

# 提示用户重新加载 shell 配置
echo -e "\n请运行以下命令之一来使PATH更改生效："
echo "- Bash: source ~/.bashrc"
echo "- Zsh:  source ~/.zshrc"
echo "- Fish: exec fish"