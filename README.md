
# repository-C Project (Smart README)

**サブモジュール情報をもとに資料（README.md等）を自動生成・管理する専用リポジトリ**

このリポジトリは、サブモジュール（`repository-A`）の最新情報を自動取得し、AIによるREADME.md等の資料生成・自動更新を行うための専用リポジトリです。

---

## 🏗 ディレクトリ構成

```text
repository-C/
├── AGENTS.md                    # AI コンテキスト・設計思想
├── README.md                    # 本ファイル（自動生成）
├── 自動化説明資料.md             # GitHub Actions自動化の説明
├── .gitmodules                  # サブモジュール設定
├── repository-A/                # ユーザー登録APIプロトタイプ（サブモジュール）
│   ├── app.py                   # Flask アプリケーション（ポート5000）
│   ├── server.js                # Express サーバー（ポート3000）
│   ├── db.js                    # SQLiteデータベース接続（Node.js）
│   ├── requirements.txt         # Python 依存関係
│   ├── package.json             # Node.js 依存関係
│   ├── README.md                # repository-Aのドキュメント
│   └── test/                    # テスト関連
└── .github/
    ├── workflows/               # GitHub Actions ワークフロー定義
    └── skills/
        └── update README/
            └── SKILL.md         # Smart README Generator スキル定義
```

---

## 🚀 API エンドポイント (repository-A)

`repository-A` には **Flask (Python)** と **Express (Node.js)** の2つの実装があり、同一のAPIを提供します。

### Flask実装（app.py - ポート5000）

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/<user_id>` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message", "user" }` / 404: Not Found |

### Express実装（server.js + db.js - ポート3000）

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/:id` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message" }` / 404: Not Found |

### セキュリティ機能
- **パスワードハッシュ化**
  - Flask: `werkzeug.security.generate_password_hash`
  - Express: `bcryptjs`
- **メールアドレス形式検証**（正規表現）
- **ユーザー名・メール重複チェック**
- **パスワード最小長**（6文字以上）
- **SQL インジェクション対策**
  - Flask: SQLAlchemy ORM
  - Express: パラメータ化クエリ（sqlite3）

### データモデル (`User`)
| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | Integer | 主キー（自動採番） |
| `username` | String(80) | ユーザー名（ユニーク） |
| `email` | String(120) | メールアドレス（ユニーク） |
| `password` | String(255) | ハッシュ化されたパスワード |
| `created_at` | DateTime | 登録日時（自動設定） |

### 使用技術

**Flask実装**
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Werkzeug 3.0.1
- SQLite

**Express実装**
- Express 4.18.2
- sqlite3 5.1.6
- bcryptjs 2.4.3
- body-parser 1.20.2

---

## 設計思想・拡張計画・サブモジュール管理方針

本リポジトリは、サブモジュールの情報を正確に取得し、AIによる資料（README.md等）の自動生成・自動更新を標準化することを目的としています。

### 主要な設計方針
- **サブモジュール情報の自動取得**: `git submodule update --init` による最新情報の取得
- **AI自動生成**: AGENTS.mdとSKILL.mdに基づいたREADME自動更新
- **GitHub Actions連携**: 開発リポジトリの更新を自動検知しドキュメント更新

### 今後の拡張例
- サブモジュールの多段管理
- 複数リポジトリ横断の資料生成
- 多言語対応
- CI/CDによる資料自動検証

---

## 📚 関連ドキュメント

- **[AGENTS.md](./AGENTS.md)**: AI コンテキスト・設計思想の詳細
- **[自動化説明資料.md](./自動化説明資料.md)**: GitHub Actionsによる自動化の説明
- **[.github/skills/update README/SKILL.md](./.github/skills/update%20README/SKILL.md)**: Smart README Generator の仕様
- **[repository-A/README.md](./repository-A/README.md)**: サブモジュールの詳細ドキュメント

---

## 🕒 最終更新

このREADMEは **Smart README Generator** により自動生成されました。  
**最終更新日時**: 2026-02-10 03:02:00 (UTC)

---

## 使用 AI モデル

**gpt-5.2-codex**
