#!/opt/homebrew/anaconda3/envs/deepseek/bin/python3
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
from openai import OpenAI

class GPTCommit:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/gptcommit")
        self.cache_file = os.path.join(self.config_dir, "api_key_cache.json")
        self.ensure_config_dir()

    def ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def get_keychain_api_key(self):
        """从 macOS Keychain 获取 API key"""
        try:
            cmd = ['security', 'find-generic-password', '-s', 'deepseek-key', '-w']
            api_key = subprocess.check_output(cmd, encoding='utf-8').strip()
            return api_key if api_key else None
        except subprocess.CalledProcessError:
            return None

    def get_cached_api_key(self):
        """从缓存中获取API key"""
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
                expiry_time = datetime.fromisoformat(cache_data['expiry'])
                if datetime.now() < expiry_time:
                    return cache_data['api_key']
        except:
            return None
        return None

    def cache_api_key(self, api_key):
        """缓存API key，24小时有效"""
        expiry_time = datetime.now() + timedelta(hours=24)
        cache_data = {
            'api_key': api_key,
            'expiry': expiry_time.isoformat()
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)

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

        prompt = f"""作为一个Git提交消息生成助手，请根据以下git diff生成一个符合 Conventional Commits 的中文 commit message: type 和 scope 为英文，description 和 body 和 footer 为中文。

Conventional Commits 1.0.0
Summary
The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with SemVer, by describing the features, fixes, and breaking changes made in commit messages.

The commit message should be structured as follows:

<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
The commit contains the following structural elements, to communicate intent to the consumers of your library:

fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
types other than fix: and feat: are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
footers other than BREAKING CHANGE: <description> may be provided and follow a convention similar to git trailer format.
Additional types are not mandated by the Conventional Commits specification, and have no implicit effect in Semantic Versioning (unless they include a BREAKING CHANGE). A scope may be provided to a commit's type, to provide additional contextual information and is contained within parenthesis, e.g., feat(parser): add ability to parse arrays.

Examples
Commit message with description and breaking change footer
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
Commit message with ! to draw attention to breaking change
feat!: send an email to the customer when a product is shipped
Commit message with scope and ! to draw attention to breaking change
feat(api)!: send an email to the customer when a product is shipped
Commit message with both ! and BREAKING CHANGE footer
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
Commit message with no body
docs: correct spelling of CHANGELOG
Commit message with scope
feat(lang): add Polish language
Commit message with multi-paragraph body and multiple footers
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123

        Git Diff:
        {diff}

请直接返回 commit message，不要使用 ``` 包围，不要返回任何其他内容。
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

    def is_enabled_for_repo(self):
        """检查当前仓库是否启用了gptcommit"""
        try:
            result = subprocess.check_output(
                ['git', 'config', '--get', 'gptcommit.enabled'],
                encoding='utf-8'
            ).strip()
            return result.lower() == 'true'
        except subprocess.CalledProcessError:
            return False

def enable_gptcommit():
    """启用 GPTCommit"""
    try:
        # 检查当前目录是否是 git 仓库
        if not os.path.isdir('.git'):
            print("错误: 当前目录不是 git 仓库")
            sys.exit(1)

        # 启用 GPTCommit
        subprocess.run(['git', 'config', 'gptcommit.enabled', 'true'], check=True)

        # 确保 hooks 目录存在
        hooks_dir = Path('.git/hooks')
        hooks_dir.mkdir(exist_ok=True)

        # 复制 prepare-commit-msg 钩子
        template_hook = Path('~/.git-templates/hooks/prepare-commit-msg').expanduser()
        if not template_hook.exists():
            print("错误: 钩子模板文件不存在，请先运行安装脚本")
            sys.exit(1)

        target_hook = hooks_dir / 'prepare-commit-msg'
        subprocess.run(['cp', str(template_hook), str(target_hook)], check=True)
        subprocess.run(['chmod', '+x', str(target_hook)], check=True)

        print("GPTCommit 已成功启用")
        print("- 已设置 gptcommit.enabled=true")
        print("- 已安装 prepare-commit-msg 钩子")

    except subprocess.CalledProcessError as e:
        print(f"错误: 启用 GPTCommit 失败: {e}")
        sys.exit(1)

def disable_gptcommit():
    """禁用 GPTCommit"""
    try:
        # 检查当前目录是否是 git 仓库
        if not os.path.isdir('.git'):
            print("错误: 当前目录不是 git 仓库")
            sys.exit(1)

        # 禁用 GPTCommit
        subprocess.run(['git', 'config', 'gptcommit.enabled', 'false'], check=True)

        # 移除 prepare-commit-msg 钩子
        hook_path = Path('.git/hooks/prepare-commit-msg')
        if hook_path.exists():
            hook_path.unlink()
            print("- 已移除 prepare-commit-msg 钩子")

        print("GPTCommit 已成功禁用")
        print("- 已设置 gptcommit.enabled=false")

    except subprocess.CalledProcessError as e:
        print(f"错误: 禁用 GPTCommit 失败: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'enable':
        enable_gptcommit()
        return
    elif len(sys.argv) == 2 and sys.argv[1] == 'disable':
        disable_gptcommit()
        return
    elif len(sys.argv) != 2:
        print("Usage: gptcommit <commit-msg-file>")
        print("   or: gptcommit enable")
        print("   or: gptcommit disable")
        sys.exit(1)

    commit_msg_file = sys.argv[1]
    gpt_commit = GPTCommit()

    # 检查是否启用
    if not gpt_commit.is_enabled_for_repo():
        sys.exit(0)

    # 获取git diff
    diff = gpt_commit.get_git_diff()
    if not diff:
        print("No changes to commit")
        sys.exit(0)

    # 生成提交消息
    commit_message = gpt_commit.generate_commit_message(diff)

    # 写入提交消息文件
    with open(commit_msg_file, 'w') as f:
        f.write(commit_message)

if __name__ == "__main__":
    main()