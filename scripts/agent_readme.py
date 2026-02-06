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
    
    # 指示書（SKILL.md）
    skill_path = os.path.join(root_dir, '.github', 'skills', 'update README', 'SKILL.md')
    context['skill'] = read_file(skill_path)
    if not context['skill']:
        print(f"Error: SKILL.mdが見つからないか内容が空です。パス: {skill_path}")
        sys.exit(1)
    
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
あなたは Smart README Generator です。
必ずリポジトリ内の実装（app.py, user_manager.py, src/配下のTypeScriptファイルなど）を詳細に分析し、
SKILL.md・Agents.mdの指示と設計思想を反映し、実際のコード・API・クラス・メソッド・型定義・ディレクトリ構成を正確にREADMEにまとめてください。

【指示書 (SKILL.md)】
{context['skill']}

【プロジェクト概要 (Agents.md)】
{context['agents'] if context['agents'] else '（ファイル未作成）'}

【ディレクトリ構成】
{context['structure']}

【API実装 (repository-A/app.py)】
{context['app_py']}

【ユーザーモジュール (user_management/user_manager.py)】
{context['user_manager_py']}

【TypeScript実装 (user_management/src/)】
{read_file(os.path.join(root_dir, 'user_management', 'src', 'userManager.ts'))}
{read_file(os.path.join(root_dir, 'user_management', 'src', 'types.ts'))}

【最終更新日時】
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

必ず以下の「推奨されるREADMEフォーマット例」に従い、各セクションを詳細に埋めてください：

---
# [リポジトリ名] Project (Smart README)
[概要説明]
---
## 🏗 ディレクトリ構成
```text
[ここに自動抽出されたディレクトリツリー]
```
---
## 🚀 API エンドポイント (repository-A)
`repository-A/app.py` から自動抽出。
[ここに自動抽出されたルート一覧]
---
## 🛠 モジュール機能 (user_management)
`user_management/user_manager.py` から自動抽出。
[ここに自動抽出されたクラス・メソッド一覧]
---
## 📝 TypeScript型・クラス (user_management/src)
`user_management/src/userManager.ts` と `types.ts` から自動抽出。
[ここに自動抽出された型・クラス・メソッド一覧]
---
## 🕒 最終更新
このREADMEは自動生成されました。
最終更新日時: [日時]
---

出力はREADME.mdの中身（Markdown）のみとします。
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
        finally:
            await client.stop()
    except Exception as e:
        print(f"Error during AI generation: {e}")
        # 詳細なエラー情報を出すためにトレースバックを表示（デバッグ用）
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
