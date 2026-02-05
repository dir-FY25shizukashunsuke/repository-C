import os
import sys
from datetime import datetime
try:
    from copilot import CopilotClient
except ImportError:
    print("Error: github-copilot-sdk is not installed. Please run 'pip install github-copilot-sdk'")
    sys.exit(1)

def read_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def get_repo_context(root_dir):
    context = {}
    
    # 指示書
    context['skill'] = read_file(os.path.join(root_dir, '.gemini', 'antigravity', 'skills', 'smart-readme', 'SKILL.md'))
    
    # 実装ファイル
    context['app_py'] = read_file(os.path.join(root_dir, 'repository-A', 'app.py'))
    context['user_manager_py'] = read_file(os.path.join(root_dir, 'user_management', 'user_manager.py'))
    
    # ディレクトリ構成
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.github', '.gemini'}
    tree = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        level = root.replace(root_dir, '').count(os.sep)
        indent = '  ' * level
        tree.append(f"{indent}- {os.path.basename(root) or root}/")
        for f in files:
            tree.append(f"{'  ' * (level + 1)}- {f}")
    context['structure'] = "\n".join(tree)
    
    return context

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    token = os.environ.get("COPILOT_TOKEN")
    
    # CopilotClient は引数なしで初期化し、環境変数（COPILOT_GITHUB_TOKEN 等）から認証情報を読み込みます
    client = CopilotClient()
    context = get_repo_context(root_dir)
    
    prompt = f"""
あなたはリポジトリのドキュメント作成エキスパートです。
以下の指示書(SKILL)とリポジトリの実装状況に基づき、最高の README.md を生成してください。
単なる情報の抽出だけでなく、コードの変更意図を汲み取った説明を心がけてください。

【指示書 (SKILL.md)】
{context['skill']}

【ディレクトリ構成】
{context['structure']}

【実装プロトタイプ (repository-A/app.py)】
{context['app_py']}

【モジュール機能 (user_management/user_manager.py)】
{context['user_manager_py']}

【最終更新日時】
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

指示書にある「推奨される README フォーマット」をベースにしつつ、AIとしての洞察を加えて内容を充実させてください。
出力は README.md の中身（Markdown）のみとしてください。
"""

    print("Generating README with GitHub Copilot AI Agent...")
    try:
        # Copilot SDK は Session を通じて操作する
        with client.create_session() as session:
            response = session.send_and_wait(prompt)
            
            output_path = os.path.join(root_dir, 'README.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                # response の属性名は SDK の仕様に合わせる（text または content）
                f.write(response.text if hasattr(response, 'text') else str(response))
            
        print(f"Successfully updated README.md using AI Agent at {datetime.now()}")
        
    except Exception as e:
        print(f"Error during AI generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
