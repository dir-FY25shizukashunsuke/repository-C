# Repository-C - User Management System

**repository-C** は、ユーザー管理機能を持つシステムのコアリポジトリです。Flask による本格的な REST API 実装（`repository-A`）と、軽量なビジネスロジック層（`user_management`）を統合し、CRUD 操作、バリデーション、統計情報の取得機能を提供します。

このプロジェクトは、**プロトタイプから本番への段階的な移行**を設計思想とし、初期のFlask実装を活かしながら、クリーンアーキテクチャを目指したモジュール設計を並行開発しています。

---

## 🏗 ディレクトリ構成

```text
repository-C/
├── AGENTS.md                        # AIエージェントへの設計コンテキスト提供
├── README.md                        # このファイル（自動生成）
├── .gitmodules                      # サブモジュール構成
├── repository-A/                    # 【Submodule】Flask REST APIプロトタイプ
│   ├── app.py                       # メインAPIエンドポイント（全CRUD実装）
│   ├── server.js                    # Node.js補助実装
│   ├── db.js                        # データベース接続補助
│   ├── requirements.txt             # Python依存関係（Flask, SQLAlchemy）
│   ├── package.json                 # Node.js依存関係
│   ├── README.md                    # repository-A固有のドキュメント
│   └── test/
│       └── test.md                  # テスト仕様書
├── scripts/                         # README自動生成・保守
│   ├── generate_readme.py           # README生成スクリプト
│   └── agent_readme.py              # GitHub Copilot SDK統合スクリプト
└── user_management/                 # 【本番品質】ユーザー管理モジュール
    ├── user_manager.py              # Pythonユーザー管理クラス（インメモリ）
    ├── example.py                   # 使用例デモ
    ├── __init__.py                  # Pythonパッケージ初期化
    ├── package.json                 # TypeScript依存関係
    ├── tsconfig.json                # TypeScript設定
    ├── README.md                    # モジュール固有のドキュメント
    └── src/                         # TypeScript実装（型安全な実装）
        ├── index.ts
        ├── userManager.ts
        └── types.ts
```

---

## 🚀 API エンドポイント (repository-A)

`repository-A/app.py` から自動抽出。**SQLite + Flask-SQLAlchemy** を使用した本格的なユーザー管理 REST API です。

### **エンドポイント一覧**

| メソッド | エンドポイント | 説明 | ステータスコード |
|---------|---------------|------|-----------------|
| `GET` | `/` | APIウェルカムメッセージ | 200 |
| `POST` | `/api/users/register` | ユーザー新規登録（バリデーション付き） | 201 / 400 |
| `GET` | `/api/users` | 全ユーザー一覧取得 | 200 |
| `GET` | `/api/users/<int:user_id>` | 特定ユーザー詳細取得 | 200 / 404 |
| `PATCH` | `/api/users/<int:user_id>` | ユーザー情報更新（名前・メールのみ） | 200 / 400 / 404 |
| `DELETE` | `/api/users/<int:user_id>` | ユーザー削除 | 200 / 404 |
| `GET` | `/api/users/stats` | ユーザー統計情報取得（総登録数） | 200 |
| `GET` | `/api/info` | API情報取得（バージョン、エンドポイント一覧） | 200 |

### **セキュリティ機能**
- ✅ **パスワードハッシュ化**: `werkzeug.security.generate_password_hash` による安全な保存
- ✅ **バリデーション**: 
  - メールアドレス形式検証（正規表現）
  - パスワード長チェック（6文字以上）
  - 重複ユーザー検出（username, email）
  - パスワード確認一致検証
- ✅ **エラーハンドリング**: 404/500エラーの統一的なJSON応答

### **技術スタック**
- **フレームワーク**: Flask 2.x
- **ORM**: Flask-SQLAlchemy
- **データベース**: SQLite（`users.db`）
- **日本語対応**: `JSON_AS_ASCII=False` により日本語メッセージをそのまま返却

### **データベーススキーマ**
```python
users テーブル:
  - id (INTEGER, PRIMARY KEY)
  - username (STRING(80), UNIQUE, NOT NULL)
  - email (STRING(120), UNIQUE, NOT NULL)
  - password (STRING(255), NOT NULL, HASHED)
  - created_at (DATETIME, DEFAULT: CURRENT_TIMESTAMP)
```

---

## 🛠 モジュール機能 (user_management)

`user_management/user_manager.py` から自動抽出。**インメモリ**でユーザーを管理する軽量クラスです。

### **設計意図**
Flask API がデータベース永続化を担当するのに対し、`UserManager` は以下のユースケースを想定しています：
- テスト環境での高速な動作検証
- プロトタイピング段階での軽量実装
- キャッシュ層やセッション管理の中間層
- TypeScript版への移植準備（型定義の基盤）

---

### **クラス: `User`**

```python
@dataclass
class User:
    id: str              # ユーザー識別子
    name: str            # ユーザー名
    email: str           # メールアドレス
    created_at: datetime # 作成日時
```

Pythonの `dataclass` によるシンプルなユーザー表現。イミュータブルな設計を意識しています。

---

### **クラス: `UserManager`**

ユーザーのCRUD操作を提供する管理クラス。

| メソッド | 説明 | 引数 | 戻り値 |
|---------|------|-----|--------|
| `add_user(user: User)` | ユーザーをリストに追加 | `user`: Userオブジェクト | `None` |
| `delete_user(user_id: str)` | IDでユーザーを削除 | `user_id`: ユーザーID | `bool`（成功時True） |
| `get_user_by_id(user_id: str)` | IDでユーザーを検索 | `user_id`: ユーザーID | `Optional[User]` |
| `get_all_users()` | 全ユーザーを取得（コピー） | なし | `List[User]` |
| `get_user_count()` | ユーザー総数を取得 | なし | `int` |

**実装の特徴**:
- ✅ リスト内包表記による効率的な削除処理
- ✅ `get_all_users()` がコピーを返すことで、外部からの不正な変更を防止
- ✅ docstringによる明確なAPI仕様記述

---

## 🔧 セットアップ & 実行

### **1. repository-A (Flask API)**

```bash
# サブモジュールの初期化（初回のみ）
git submodule update --init --recursive

# repository-Aに移動
cd repository-A

# Python依存関係のインストール
pip install -r requirements.txt

# APIサーバー起動
python app.py
```

→ `http://localhost:5000` でAPIが起動  
→ ブラウザまたは `curl http://localhost:5000` でウェルカムメッセージを確認

### **2. user_management (Python モジュール)**

```bash
cd user_management

# 使用例の実行
python example.py
```

### **3. user_management (TypeScript モジュール)**

```bash
cd user_management

# 依存関係のインストール
npm install

# TypeScriptコンパイル
npm run build

# 出力確認
node dist/index.js
```

---

## 📝 使用例

### **Flask API の使用例**

```bash
# ユーザー登録
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tanaka",
    "email": "tanaka@example.com",
    "password": "password123",
    "passwordConfirm": "password123"
  }'

# 全ユーザー取得
curl http://localhost:5000/api/users

# ユーザー統計
curl http://localhost:5000/api/users/stats
```

### **Python モジュールの使用例**

```python
from user_management.user_manager import UserManager, User
from datetime import datetime

# マネージャーの初期化
manager = UserManager()

# ユーザーの追加
user = User(
    id="001",
    name="田中太郎",
    email="tanaka@example.com",
    created_at=datetime.now()
)
manager.add_user(user)

# ユーザーの取得
found_user = manager.get_user_by_id("001")
print(f"Found: {found_user.name}")

# ユーザー数の取得
print(f"Total users: {manager.get_user_count()}")
```

---

## 🤖 README 自動生成について

このREADMEは **AI駆動のドキュメント自動生成**により維持されています。

### **再生成コマンド**
```bash
# Python標準スクリプト
python scripts/generate_readme.py

# GitHub Copilot SDK統合版
python scripts/agent_readme.py
```

### **設計ファイル**
- **`AGENTS.md`**: AIエージェントがプロジェクトの設計意図や歴史を理解するためのコンテキスト
- **`.github/skills/update README/SKILL.md`**: README生成時のフォーマット指示書とAIの思考ルール

実装が変更された際は、上記スクリプトを実行することで、最新のコード状況を反映したREADMEが自動生成されます。

---

## 📌 今後の拡張計画

- [ ] **JWT認証の実装** - トークンベースの認証機構
- [ ] **ユーザー権限管理** - Admin/User/Guestロール
- [ ] **パスワードリセット機能** - メール確認フロー
- [ ] **メール通知機能** - 登録完了、パスワード変更通知
- [ ] **TypeScript版APIクライアント** - 型安全なフロントエンド連携
- [ ] **PostgreSQL対応** - 本番環境用のデータベース移行
- [ ] **Docker Compose環境** - 開発環境の標準化

---

## 🕒 最終更新

このREADMEは自動生成されました。  
**最終更新日時**: 2026-02-05 08:33:44 (UTC)

---

## 📚 関連ドキュメント

- [repository-A/README.md](./repository-A/README.md) - Flask API詳細仕様
- [user_management/README.md](./user_management/README.md) - モジュールAPI仕様
- [AGENTS.md](./AGENTS.md) - AI向けプロジェクトコンテキスト

---

## 📄 ライセンス

このプロジェクトの詳細は各サブモジュールのライセンスを参照してください。