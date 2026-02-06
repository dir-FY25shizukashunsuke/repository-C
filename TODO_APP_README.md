# To-Do アプリケーション

FlaskベースのRESTful API によるTo-Do管理アプリケーションです。

## 概要

このTo-Doアプリケーションは、以下の機能を提供します：

- ✅ To-Doの作成、表示、更新、削除（CRUD操作）
- ✅ To-Doの完了状態の切り替え
- ✅ To-Do統計情報の取得
- ✅ クリーンアーキテクチャに基づいた設計
- ✅ 型安全性（dataclass + 型ヒント）
- ✅ 完全なAPI ドキュメント

## プロジェクト構造

```
repository-C/
├── app.py                      # Flask API アプリケーション
├── requirements.txt             # Python依存関係
├── API_DOCUMENTATION.md         # API完全ドキュメント
├── todo_management/            # To-Do管理モジュール
│   ├── __init__.py             # パッケージ初期化
│   ├── todo_manager.py         # ビジネスロジック
│   ├── example.py              # 使用例
│   └── README.md               # モジュール説明
└── AGENTS.md                   # AIコンテキスト・設計思想
```

## クイックスタート

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. サーバーの起動

```bash
# 本番モード（デフォルト、推奨）
python app.py

# 開発モード（デバッグ有効）
FLASK_DEBUG=true python app.py
```

サーバーは `http://localhost:5000` で起動します。

### 3. APIを試す

```bash
# ホーム画面（エンドポイント一覧）
curl http://localhost:5000/

# To-Doを作成
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Pythonの勉強"}'

# すべてのTo-Doを取得
curl http://localhost:5000/api/todos

# 統計情報を取得
curl http://localhost:5000/api/todos/stats
```

## API エンドポイント

| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| `GET` | `/` | API情報とエンドポイント一覧 |
| `GET` | `/api/todos` | すべてのTo-Doを取得 |
| `POST` | `/api/todos` | To-Doを作成 |
| `GET` | `/api/todos/<id>` | 特定のTo-Doを取得 |
| `PATCH` | `/api/todos/<id>` | To-Doを更新 |
| `DELETE` | `/api/todos/<id>` | To-Doを削除 |
| `POST` | `/api/todos/<id>/toggle` | 完了状態を切り替え |
| `GET` | `/api/todos/stats` | 統計情報を取得 |

詳細なAPIドキュメントは [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) をご覧ください。

## 使用例

### Python モジュールとしての使用

```python
from todo_management.todo_manager import TodoManager, Todo
from datetime import datetime

# マネージャーを初期化
manager = TodoManager()

# To-Doを追加
todo = Todo(
    id='todo_1',
    title='Pythonの勉強',
    completed=False,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
manager.add_todo(todo)

# To-Doを取得
all_todos = manager.get_all_todos()
print(f"To-Do数: {len(all_todos)}")

# 完了状態を切り替え
manager.toggle_todo('todo_1')
```

詳細な使用例は `todo_management/example.py` をご覧ください。

## 設計思想

### クリーンアーキテクチャ

- **ビジネスロジック層** (`todo_management/`): インフラに依存しない純粋なロジック
- **インフラ層** (`app.py`): Flask API、HTTPリクエスト処理
- **明確な境界**: モジュール分離による疎結合

### 型安全性

- Python dataclass + 型ヒント (`typing` モジュール)
- すべての関数に型注釈
- IDEの型チェック対応

### イミュータブル性

- `get_all_todos()` はリストのコピーを返す
- 更新操作は新しいインスタンスを作成
- 副作用を最小化

### セキュリティ

- デバッグモードはデフォルトで無効
- 環境変数 `FLASK_DEBUG` で制御
- 入力バリデーション（タイトル必須チェック）

## テスト

モジュールのテスト:

```bash
cd todo_management
python example.py
```

APIのテスト:

```bash
# サーバーを起動（別ターミナル）
python app.py

# APIエンドポイントをテスト
curl http://localhost:5000/
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "テスト"}'
```

## 今後の拡張予定

- [ ] ユーザー認証とTo-Doの関連付け
- [ ] To-Doの期限設定機能
- [ ] To-Doの優先度設定
- [ ] To-Doのカテゴリ分類
- [ ] データベース永続化（SQLite / PostgreSQL）
- [ ] フロントエンド（React / Vue.js）
- [ ] TypeScript実装の追加

## セキュリティに関する注意

⚠️ **重要**: 本番環境では以下に注意してください：

1. **デバッグモード**: デフォルトで無効ですが、`FLASK_DEBUG=true` は開発時のみ使用
2. **WSGIサーバー**: 本番環境では Gunicorn や uWSGI を使用
3. **HTTPS**: 本番環境では必ず HTTPS を使用
4. **認証**: 実際の運用では認証機能の実装が必要

## ライセンス

このプロジェクトは ISC ライセンスの下で公開されています。

## 関連ドキュメント

- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - 完全なAPIリファレンス
- [todo_management/README.md](./todo_management/README.md) - モジュール詳細
- [AGENTS.md](./AGENTS.md) - 設計思想とAIコンテキスト
