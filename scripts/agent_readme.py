import os
import sys
import asyncio
import shutil
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
    
    # プロジェクト概要（Agents.md）があれば読み込む
    agents_path = os.path.join(root_dir, 'Agents.md')
    if not os.path.exists(agents_path):
        agents_path = os.path.join(root_dir, '.gemini', 'antigravity', 'Agents.md')
    context['agents'] = read_file(agents_path)
    
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

async def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Copilot CLI のバイナリパスを探す (npm install だと copilot-cli の場合がある)
    copilot_bin = shutil.which("copilot") or shutil.which("copilot-cli")
    
    if not copilot_bin:
        print("Error: 'copilot' or 'copilot-cli' binary not found. Please ensure GitHub Copilot CLI is installed.")
        sys.exit(1)
        
    print(f"Using Copilot CLI binary at: {copilot_bin}")
    
    # CopilotClient は環境変数から認証情報を読み込みます
    # CLI バイナリはインストール済みで PATH に通っているため、引数なしで初期化します
    client = CopilotClient()
    context = get_repo_context(root_dir)
    
    prompt = f"""
あなたはリポジトリのドキュメント作成エキスパートです。
以下の指示書(SKILL)とリポジトリの実装状況に基づき、最高の README.md を生成してください。
単なる情報の抽出だけでなく、コードの変更意図を汲み取った説明を心がけてください。

【指示書 (SKILL.md)】
{context['skill']}

【プロジェクト概要 (Agents.md)】
{context['agents'] if context['agents'] else '（ファイル未作成）'}

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

    print("Generating README with GitHub Copilot AI Agent (Async Lifecycle Mode)...")
    try:
        # CopilotClient のライフサイクル管理 (start/stop)
        await client.start()
        try:
            # セッションの作成（このバージョンの SDK では session はコンテキストマネージャではない）
            session = await client.create_session()
            # タイムアウトを180秒に延長
            response = await session.send_and_wait({"prompt": prompt}, timeout=180)
            
            output_path = os.path.join(root_dir, 'README.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                # response の形式を確認し、SessionEvent等のラップを除去
                if hasattr(response, 'content') and response.content:
                    content = response.content
                elif hasattr(response, 'text') and response.text:
                    content = response.text
                else:
                    content = str(response)

                # SessionEvent(...content='...') のような文字列から content のみ抽出
                if isinstance(content, str) and content.startswith('SessionEvent') and ", content='" in content:
                    import re
                    # content='...' の部分を非貪欲で抽出（改行・クォート・エスケープも考慮）
                    m = re.search(r"content='((?:[^']|''|\\')*)'", content, re.DOTALL)
                    if m:
                        # Pythonのシングルクォートエスケープ(''や\')を元に戻す
                        extracted = m.group(1)
                        extracted = extracted.replace("''", "'").replace("\\'", "'")
                        content = extracted

                # contentが```markdown ... ```で囲まれている場合、その中身だけを抽出
                if isinstance(content, str):
                    m = re.search(r"```markdown\\n(.*?)\\n```", content, re.DOTALL)
                    if m:
                        content = m.group(1).strip()

                # Copilot SDKのSessionEvent等でcontentがさらに辞書やオブジェクトの場合は再度抽出
                if isinstance(content, dict) and 'content' in content:
                    content = content['content']
                f.write(content)

        # --- 生成後のREADME.mdからSessionEventラップを除去し、Markdown本文だけにする後処理 ---
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                raw = f.read()
            import re
            # SessionEvent(...content='...') の中の ```markdown ... ``` だけを抽出
            m = re.search(r"```markdown\\n(.*?)\\n```", raw, re.DOTALL)
            if m:
                markdown = m.group(1).strip()
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown)
        except Exception as post_e:
            print(f"[WARN] README後処理でエラー: {post_e}")
        print(f"Successfully updated README.md using AI Agent at {datetime.now()}")
        
    except Exception as e:
        print(f"Error during AI generation: {e}")
        # 詳細なエラー情報を出すためにトレースバックを表示（デバッグ用）
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
