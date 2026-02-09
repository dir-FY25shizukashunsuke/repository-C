
# repository-C Project (Smart README)

**ユーザー管理機能を持つシステムのコアリポジトリ**

このリポジトリは、Flask/Express による API プロトタイプ（`repository-A` サブモジュール）と、プロダクション品質のユーザー管理モジュール（`user_management`）を統合し、クリーンアーキテクチャに基づいた設計を実現しています。型安全性とセキュリティを重視し、Python と TypeScript の両方でユーザー管理機能を提供します。

---

## 🏗 ディレクトリ構成

```text
repository-C/
├── AGENTS.md                    # AI コンテキスト・設計思想
├── README.md                    # 本ファイル（自動生成）
├── README_OLD.md                # 旧バージョン
├── .gitmodules                  # サブモジュール設定
├── 自動化説明資料.md             # 自動化の説明資料
├── repository-A/                # API プロトタイプ（サブモジュール）
│   ├── app.py                   # Flask アプリケーション本体
│   ├── server.js                # Express (Node.js) サーバー
│   ├── db.js                    # データベース層 (Node.js/SQLite)
│   ├── requirements.txt         # Python 依存関係
│   ├── package.json             # Node.js 依存関係
│   └── test/                    # テスト関連
│       └── test.md
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
└── .github/
    └── skills/
        └── update README/
            └── SKILL.md         # Smart README Generator スキル定義
```

---

## 🚀 API エンドポイント (repository-A)

### Flask 実装 (`repository-A/app.py`)

Python/Flask による RESTful API 実装。SQLAlchemy ORM を使用。

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/<user_id>` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message", "user" }` / 404: Not Found |

**Flask 実装の特徴:**
- **SQLAlchemy ORM**: SQL インジェクション対策
- **パスワードハッシュ化**: `werkzeug.security.generate_password_hash`
- **バリデーション**: メール形式、パスワード長（6文字以上）、重複チェック
- **エラーハンドリング**: 404, 500 エラーのカスタムハンドラー

#### データモデル (`User`)
| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | Integer | 主キー（自動採番） |
| `username` | String(80) | ユーザー名（ユニーク） |
| `email` | String(120) | メールアドレス（ユニーク） |
| `password` | String(255) | ハッシュ化されたパスワード |
| `created_at` | DateTime | 登録日時（自動設定） |

---

### Express 実装 (`repository-A/server.js` + `db.js`)

Node.js/Express による RESTful API 実装。SQLite3 ドライバーを直接使用。

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/:id` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message" }` / 404: Not Found |

**Express 実装の特徴:**
- **データベース層分離** (`db.js`): ビジネスロジックとDB操作を分離
- **パスワードハッシュ化**: `bcryptjs` ライブラリ使用
- **プリペアドステートメント**: SQL インジェクション対策
- **グレースフルシャットダウン**: SIGINT ハンドリング

#### データベース層 (`db.js`) 提供メソッド
| メソッド | 説明 |
|---------|------|
| `initializeDatabase()` | users テーブル作成 |
| `registerUser(username, email, password, callback)` | ユーザー登録（パスワードハッシュ化含む） |
| `getUserByUsername(username, callback)` | ユーザー名で検索 |
| `getUserById(id, callback)` | IDで検索 |
| `getAllUsers(callback)` | 全ユーザー取得 |
| `updateUser(id, updates, callback)` | ユーザー情報更新 |
| `deleteUserById(id, callback)` | ユーザー削除 |
| `getUserStats(callback)` | ユーザー統計取得 |
| `verifyPassword(plain, hashed, callback)` | パスワード検証 |
| `closeDatabase()` | DB接続クローズ |

---

### セキュリティ機能（共通）
- ✅ **パスワードハッシュ化**: Flask は `werkzeug.security`、Express は `bcryptjs`
- ✅ **SQL インジェクション対策**: Flask は SQLAlchemy ORM、Express はプリペアドステートメント
- ✅ **入力バリデーション**: メール形式、パスワード長（6文字以上）、必須フィールドチェック
- ✅ **ユニーク制約**: ユーザー名・メールの重複防止

---

## 🛠 モジュール機能 (user_management)

ビジネスロジック層として、インフラストラクチャに依存しないユーザー管理機能を提供。

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
- ✅ **イミュータブル返却**: `get_all_users` はコピーを返し、内部状態を保護
- ✅ **型ヒントの完全活用**: `typing` モジュールで型安全性を確保
- ✅ **docstring**: 自己文書化されたコード

---

### TypeScript 実装 (`user_management/src`)

#### 型定義 (`user_management/src/types.ts`)

```typescript
export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export interface UserDatabase {
  users: User[];
}
```

#### クラス: `UserManager` (`user_management/src/userManager.ts`)

| メソッド | 引数 | 戻り値 | 説明 |
|---------|-----|--------|------|
| `constructor(database: UserDatabase)` | `database: UserDatabase` | - | データベースオブジェクトを注入 |
| `addUser(user: User)` | `user: User` | `void` | ユーザーを追加 |
| `deleteUser(userId: string)` | `userId: string` | `boolean` | ユーザーを削除（成功: true / 失敗: false） |
| `getUserById(userId: string)` | `userId: string` | `User \| undefined` | IDでユーザーを検索 |
| `getAllUsers()` | - | `User[]` | 全ユーザーを取得（スプレッド演算子でコピー） |
| `getUserCount()` | - | `number` | ユーザー総数を取得 |

**設計原則:**
- ✅ **依存性注入（DI）パターン**: コンストラクタでデータベースを注入
- ✅ **イミュータブル返却**: スプレッド演算子 `[...]` で配列をコピー
- ✅ **完全な型安全性**: TypeScript の厳密な型チェック

---

## 🎯 設計思想

### クリーンアーキテクチャ
このプロジェクトは、ビジネスロジックとインフラストラクチャを明確に分離しています。

```
┌─────────────────────────────────────────┐
│  ビジネスロジック層 (user_management)   │
│  - インフラに依存しない純粋なロジック   │
│  - Python & TypeScript で同一設計        │
└─────────────────────────────────────────┘
                    ↑
                    │ 依存方向
                    │
┌─────────────────────────────────────────┐
│  インフラ層 (repository-A)              │
│  - Flask API (Python)                   │
│  - Express API (Node.js)                │
│  - データベース接続 (SQLite)             │
└─────────────────────────────────────────┘
```

### 型安全性
- **Python**: `@dataclass` + `typing` モジュール（型ヒント）
- **TypeScript**: `interface` + 厳密な型チェック（`tsconfig.json`）
- 両言語で一貫したデータモデル（`User`, `UserManager`）

### セキュリティ
- **パスワードハッシュ化**: Flask は `werkzeug.security`、Express は `bcryptjs`
- **SQL インジェクション対策**: ORM/プリペアドステートメント使用
- **入力バリデーション**: メール形式、パスワード長、必須フィールド
- **ユニーク制約**: データベースレベルでの重複防止

### 副作用の最小化
- **イミュータブル返却**: リストや配列のコピーを返す
- **明確な戻り値**: 状態変更メソッドは `bool` や `None` を返す
- **参照透過性**: 純粋関数の原則に従った設計

---

## 🚧 今後の拡張計画

- **OAuth 認証**: Google/GitHub 連携
- **ロール管理**: 管理者・一般ユーザーの権限分離
- **多言語対応**: i18n による国際化
- **API レスポンス型保証**: OpenAPI / JSON Schema による型定義
- **CI/CD**: GitHub Actions による自動テスト・デプロイ
- **検索機能拡張**: `search_users` メソッド（名前・メール部分一致）
- **ユーザー更新機能**: `update_user` メソッド（Python/TypeScript 両方）

---

## 📚 関連ドキュメント

- **[AGENTS.md](./AGENTS.md)**: AI コンテキスト・設計思想の詳細
- **[.github/skills/update README/SKILL.md](./.github/skills/update%20README/SKILL.md)**: Smart README Generator の仕様
- **[user_management/README.md](./user_management/README.md)**: ユーザー管理モジュールの詳細
- **[自動化説明資料.md](./自動化説明資料.md)**: 自動化の説明資料

---

## 🕒 最終更新

このREADMEは **Smart README Generator** により自動生成されました。  
**最終更新日時**: 2026-02-09 07:17:32 (UTC)

**生成に使用したAIモデル**: Claude Sonnet 4.5
