import os
import re
from datetime import datetime

def read_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def extract_flask_routes(file_path):
    content = read_file(file_path)
    # Match @app.route('/path', methods=['GET', 'POST'])
    routes = re.findall(r"@app\.route\(['\"](.+?)['\"].*?(?:methods=\[(.+?)\])?\)", content)
    formatted_routes = []
    for path, methods in routes:
        methods = methods.replace("'", "").replace('"', "") if methods else "GET"
        formatted_routes.append(f"- `{methods}` `{path}`")
    return "\n".join(formatted_routes) if formatted_routes else "エンドポイントが見つかりませんでした。"

def extract_python_classes_and_methods(file_path):
    content = read_file(file_path)
    lines = content.split('\n')
    results = []
    current_class = None
    
    for line in lines:
        class_match = re.match(r"^class\s+(\w+)", line)
        if class_match:
            current_class = class_match.group(1)
            results.append(f"#### Class: `{current_class}`")
            continue
            
        method_match = re.match(r"^\s+def\s+(\w+)\(self", line)
        if method_match and current_class:
            method_name = method_match.group(1)
            if not method_name.startswith('__'):
                results.append(f"- Method: `{method_name}`")
                
    return "\n".join(results) if results else "クラス・メソッドが見つかりませんでした。"

def get_directory_structure(root_path):
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.github', '.gemini'}
    tree = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        level = root.replace(root_path, '').count(os.sep)
        indent = '  ' * level
        tree.append(f"{indent}- {os.path.basename(root)}/")
        sub_indent = '  ' * (level + 1)
        for f in files:
            tree.append(f"{sub_indent}- {f}")
    return "\n".join(tree)

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # paths
    repo_a_app_path = os.path.join(root_dir, 'repository-A', 'app.py')
    user_mgmt_path = os.path.join(root_dir, 'user_management', 'user_manager.py')
    output_readme_path = os.path.join(root_dir, 'README.md')
    
    # extraction
    repo_a_routes = extract_flask_routes(repo_a_app_path)
    user_mgmt_details = extract_python_classes_and_methods(user_mgmt_path)
    dir_structure = get_directory_structure(root_dir)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    readme_template = f"""# Repository-C Project (Smart README)

本体プロジェクトとサブモジュールの情報を、ソースコードから自動抽出して管理しています。

---

## 🏗 ディレクトリ構成
```text
{dir_structure}
```

---

## 🚀 API エンドポイント (repository-A)
`repository-A/app.py` から自動抽出されたルート一覧です。

{repo_a_routes}

---

## 🛠 モジュール機能 (user_management)
`user_management/user_manager.py` から自動抽出された機能一覧です。

{user_mgmt_details}

---

## 🕒 最終更新
このREADMEは自動生成されました。ソースコードの変更を検知して自動で更新されます。
最終更新日時: {now}
"""

    with open(output_readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_template)
    
    print(f"Successfully updated README.md at {now}")

if __name__ == "__main__":
    main()
