
# repository-C Project (Smart README)

**ユーザー管理機能を持つシステムのコアリポジトリ**

このリポジトリは、Flask による API プロトタイプ（`repository-A`）と、プロダクション品質のユーザー管理モジュール（`user_management`）を統合し、クリーンアーキテクチャに基づいた設計を実現しています。型安全性とセキュリティを重視し、Python と TypeScript の両方でユーザー管理機能を提供します。

---

## 🏗 ディレクトリ構成

```text
repository-C/
├── AGENTS.md                    # AI コンテキスト・設計思想
├── README.md                    # 本ファイル（自動生成）
├── README_OLD.md                # 旧バージョン
├── .gitmodules                  # サブモジュール設定
├── repository-A/                # Flask API プロトタイプ（サブモジュール）
│   ├── app.py                   # Flask アプリケーション本体
│   ├── server.js                # Node.js サーバー
│   ├── db.js                    # データベース接続
│   ├── requirements.txt         # Python 依存関係
│   ├── package.json             # Node.js 依存関係
│   └── test/                    # テスト関連
│       └── test.md
├── scripts/                     # ユーティリティスクリプト
│   ├── generate_readme.py       # README 生成スクリプト
│   └── agent_readme.py          # AI エージェント
├── user_management/             # ユーザー管理モジュール（Python & TypeScript）
│   ├── __init__.py              # Python パッケージ初期化
│   ├── user_manager.py          # Python ユーザー管理クラス
│   ├── example.py               # 使用例
│   ├── README.md                # モジュール説明
│   ├── package.json             # TypeScript プロジェクト設定
│   ├── tsconfig.json            # TypeScript コンパイラ設定
│   └── src/                     # TypeScript ソースコード
│       ├── index.ts             # エントリーポイント
│       ├── userManager.ts       # ユーザー管理クラス
│       └── types.ts             # 型定義
└── skills/                      # AI スキル定義
    └── update/
        └── skills/
            └── smart-readme/
                └── SKILL.md     # Smart README Generator スキル定義
```

---

## 🚀 API エンドポイント (repository-A)

### Flask 実装 (`repository-A/app.py`)
Flask を使用した Python API の実装。ポート 5000 で動作。

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/<user_id>` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message", "user" }` / 404: Not Found |

### Express 実装 (`repository-A/server.js` + `repository-A/db.js`)
Node.js + Express を使用した JavaScript API の実装。ポート 3000 で動作。

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/:id` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message" }` / 404: Not Found |

### セキュリティ機能

**Flask 実装:**
- パスワードハッシュ化（`werkzeug.security.generate_password_hash`）
- メールアドレス形式検証（正規表現）
- ユーザー名・メール重複チェック
- パスワード最小長（6文字以上）
- SQL インジェクション対策（SQLAlchemy ORM）

**Express 実装:**
- パスワードハッシュ化（`bcryptjs`）
- メールアドレス形式検証（正規表現）
- ユーザー名・メール重複チェック
- パスワード最小長（6文字以上）
- SQL インジェクション対策（パラメータ化クエリ）

### データモデル

**Flask `User` モデル (SQLAlchemy ORM):**
| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | Integer | 主キー（自動採番） |
| `username` | String(80) | ユーザー名（ユニーク） |
| `email` | String(120) | メールアドレス（ユニーク） |
| `password` | String(255) | ハッシュ化されたパスワード |
| `created_at` | DateTime | 登録日時（自動設定） |

**Express `users` テーブル (SQLite):**
| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | INTEGER | 主キー（自動採番） |
| `username` | TEXT | ユーザー名（ユニーク） |
| `email` | TEXT | メールアドレス（ユニーク） |
| `password` | TEXT | ハッシュ化されたパスワード |
| `created_at` | DATETIME | 登録日時（自動設定） |

---

## 🛠 モジュール機能 (user_management)

### Python 実装 (`user_management/user_manager.py`)

#### クラス: `User` (dataclass)
ユーザー情報を表すイミュータブルなデータクラス。

| 属性 | 型 | 説明 |
|-----|---|------|
| `id` | `str` | ユーザーID |
| `name` | `str` | ユーザー名 |
| `email` | `str` | メールアドレス |
| `created_at` | `datetime` | 登録日時 |

#### クラス: `UserManager`
ユーザー管理のビジネスロジックを提供するクラス。

| メソッド | 引数 | 戻り値 | 説明 |
|---------|-----|--------|------|
| `__init__()` | - | `None` | コンストラクタ。空のユーザーリストを初期化 |
| `add_user(user: User)` | `user: User` | `None` | ユーザーを追加 |
| `delete_user(user_id: str)` | `user_id: str` | `bool` | ユーザーを削除（成功: True / 失敗: False） |
| `get_user_by_id(user_id: str)` | `user_id: str` | `Optional[User]` | IDでユーザーを検索（見つからない場合: None） |
| `get_all_users()` | - | `List[User]` | 全ユーザーを取得（コピーを返却） |
| `get_user_count()` | - | `int` | ユーザー総数を取得 |

**設計原則:**
- イミュータブル返却（`get_all_users` はコピーを返す）
- 型ヒントの完全活用
- docstring による自己文書化

---

## 📝 TypeScript 型・クラス (user_management/src)

### 型定義 (`user_management/src/types.ts`)

#### インターフェース: `User`
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}
```

#### インターフェース: `UserDatabase`
```typescript
interface UserDatabase {
  users: User[];
}
```

### クラス: `UserManager` (`user_management/src/userManager.ts`)

| メソッド | 引数 | 戻り値 | 説明 |
|---------|-----|--------|------|
| `constructor(database: UserDatabase)` | `database: UserDatabase` | - | データベースオブジェクトを注入 |
| `addUser(user: User)` | `user: User` | `void` | ユーザーを追加 |
| `deleteUser(userId: string)` | `userId: string` | `boolean` | ユーザーを削除（成功: true / 失敗: false） |
| `getUserById(userId: string)` | `userId: string` | `User \| undefined` | IDでユーザーを検索 |
| `getAllUsers()` | - | `User[]` | 全ユーザーを取得（スプレッド演算子でコピー） |
| `getUserCount()` | - | `number` | ユーザー総数を取得 |

**設計原則:**
- 依存性注入（DI）パターン
- イミュータブル返却（配列のコピー）
- 完全な型安全性

---

## 🎯 設計思想

### クリーンアーキテクチャ
- **ビジネスロジック層** (`user_management`): インフラストラクチャに依存しない純粋なロジック
- **インフラ層** (`repository-A`): Flask API、データベース接続
- **明確な境界**: サブモジュールとモジュールの分離により、疎結合を実現

### 型安全性
- Python: `dataclass` + 型ヒント（`typing` モジュール）
- TypeScript: `interface` + 厳密な型チェック
- 両言語で一貫したデータモデル

### セキュリティ
- パスワードハッシュ化（`werkzeug.security`）
- SQL インジェクション対策（ORM 使用）
- 入力バリデーション（メール形式、パスワード長）
- ユニーク制約（ユーザー名・メールの重複防止）

### 副作用の最小化
- イミュータブル返却（リストや配列のコピー）
- 状態変更を伴うメソッドは明確に `bool` や `None` を返す

---

## 🚧 今後の拡張計画

- **OAuth 認証**: Google/GitHub 連携
- **ロール管理**: 管理者・一般ユーザーの権限分離
- **多言語対応**: i18n による国際化
- **API レスポンス型保証**: OpenAPI / JSON Schema
- **CI/CD**: GitHub Actions による自動テスト・デプロイ
- **検索機能拡張**: `search_users` メソッドの実装（名前・メール部分一致）
- **ユーザー更新機能**: `update_user` メソッドの実装（Python/TypeScript 両方）

---

## 📚 関連ドキュメント

- **[AGENTS.md](./AGENTS.md)**: AI コンテキスト・設計思想の詳細
- **[skills/SKILL.md](./skills/update/skills/smart-readme/SKILL.md)**: Smart README Generator の仕様
- **[user_management/README.md](./user_management/README.md)**: ユーザー管理モジュールの詳細

---

## 🕒 最終更新

このREADMEは **Smart README Generator** により自動生成されました。  
**最終更新日時**: 2026-02-10 01:24:00 (UTC)

---

## 使用 AI モデル

**gpt-5.2-codex**
