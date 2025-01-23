#!/opt/homebrew/anaconda3/envs/deepseek/bin/python3
import os
import sys
import subprocess
import argparse
from pathlib import Path
from openai import OpenAI

class GPTCommit:
    def __init__(self, lang='zh'):
        self.config_dir = os.path.expanduser("~/.config/gptcommit")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.lang = lang

    def get_keychain_api_key(self):
        """从 macOS Keychain 获取 API key"""
        try:
            cmd = ['security', 'find-generic-password', '-s', 'deepseek-key', '-w']
            api_key = subprocess.check_output(cmd, encoding='utf-8').strip()
            return api_key if api_key else None
        except subprocess.CalledProcessError:
            return None

    def get_api_key(self):
        """获取API key，按优先级：Keychain > 环境变量 > git配置"""
        # 从 Keychain 获取
        api_key = self.get_keychain_api_key()
        if api_key:
            return api_key

        # 从环境变量获取
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        if api_key:
            return api_key

        # 从git配置获取
        try:
            api_key = subprocess.check_output(
                ['git', 'config', '--get', 'gptcommit.apikey'],
                encoding='utf-8'
            ).strip()
            if api_key:
                return api_key
        except subprocess.CalledProcessError:
            pass

        print("错误: 未找到 DeepSeek API Key")
        print("请通过以下方式之一设置 API Key:")
        print("1. 设置 macOS Keychain: security add-generic-password -s deepseek-key -w 'your-api-key'")
        print("2. 设置环境变量: export DEEPSEEK_API_KEY='your-api-key'")
        print("3. 设置git配置: git config gptcommit.apikey 'your-api-key'")
        sys.exit(1)

    def get_git_diff(self):
        """获取git diff信息"""
        # 获取暂存区的更改
        staged_diff = subprocess.check_output(
            ['git', 'diff', '--cached'],
            encoding='utf-8'
        )
        return staged_diff

    def generate_commit_message(self, diff):
        """使用LLM生成提交信息"""
        client = OpenAI(
            api_key=self.get_api_key(),
            base_url="https://api.deepseek.com"
        )

        if self.lang == 'zh':
            prompt = f"""作为一个Git提交消息生成助手，请根据以下git diff生成一个符合 Conventional Commits 的中文 commit message:
            - type 和 scope 使用英文
            - description、body 和 footer 使用中文
            - 保持简洁明了

            Git Diff:
            {diff}

请直接返回 commit message，不要使用 ``` 包围，不要返回任何其他内容。
            """
        else:
            prompt = f"""As a Git commit message generator, please generate a commit message following the Conventional Commits standard based on the following git diff:
            - Keep the message concise and clear
            - Follow the format: <type>[optional scope]: <description>
            - Add body and footer if necessary

            Git Diff:
            {diff}

Please return only the commit message, without any ``` or additional content.
            """

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的Git提交消息生成助手，严格遵循 commit convention"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        return response.choices[0].message.content

    def commit(self, message=None):
        """执行git commit"""
        if message:
            subprocess.run(['git', 'commit', '-m', message], check=True)
        else:
            # 如果没有提供消息，则使用生成的消息
            diff = self.get_git_diff()
            if not diff:
                print("没有要提交的更改")
                sys.exit(1)

            commit_message = self.generate_commit_message(diff)
            print("\n生成的提交消息:")
            print("---")
            print(commit_message)
            print("---")

            # 询问用户是否接受这个提交消息
            response = input("\n是否接受这个提交消息？[Y/n] ").strip().lower()
            if response in ['', 'y', 'yes']:
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                print("提交成功！")
            else:
                print("提交已取消")
                sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='GPTCommit - AI-powered Git commit message generator')
    parser.add_argument('message', nargs='?', help='Optional commit message')
    parser.add_argument('-l', '--lang', choices=['zh', 'en'], default='zh',
                      help='Language for commit message (zh: Chinese, en: English)')

    args = parser.parse_args()

    # 检查当前目录是否是git仓库
    if not os.path.isdir('.git'):
        print("错误: 当前目录不是git仓库")
        sys.exit(1)

    gpt_commit = GPTCommit(lang=args.lang)
    gpt_commit.commit(args.message)

if __name__ == "__main__":
    main()