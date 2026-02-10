
# repository-C Project (Smart README)

**サブモジュール情報をもとに資料（README.md等）を自動生成・管理する専用リポジトリ**

このリポジトリは、サブモジュール（`repository-A`）の最新情報を自動取得し、AIによるREADME.md等の資料生成・自動更新を行うための専用リポジトリです。

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
└── .github/
  ├── workflows/               # ワークフロー定義
  └── skills/
    └── update README/
      └── SKILL.md         # Smart README Generator スキル定義
└── skills/                      # AI スキル定義
    └── update/
        └── skills/
            └── smart-readme/
                └── SKILL.md     # Smart README Generator スキル定義
```

---

## 🚀 API エンドポイント (repository-A)

`repository-A/app.py` から自動抽出された Flask API エンドポイント一覧。

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `GET` | `/api/users` | ユーザー一覧取得 | - | 200: `{ "users": [...] }` |
| `GET` | `/api/users/<user_id>` | ユーザー一件取得 | - | 200: `{ "user": {...} }` / 404: Not Found |
| `PATCH` | `/api/users/<user_id>` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message", "user" }` / 404: Not Found |
| `DELETE` | `/api/users/<user_id>` | ユーザー削除 | - | 200: `{ "message", "user" }` / 404: Not Found |
| `GET` | `/api/users/stats` | ユーザー統計取得 | - | 200: `{ "total_users": N }` |

### セキュリティ機能
- パスワードハッシュ化（`werkzeug.security.generate_password_hash`）
- メールアドレス形式検証（正規表現）
- ユーザー名・メール重複チェック
- パスワード最小長（6文字以上）
- SQL インジェクション対策（SQLAlchemy ORM）

### データモデル (`User`)
| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | Integer | 主キー（自動採番） |
| `username` | String(80) | ユーザー名（ユニーク） |
| `email` | String(120) | メールアドレス（ユニーク） |
| `password` | String(255) | ハッシュ化されたパスワード |
| `created_at` | DateTime | 登録日時（自動設定） |

---



## 設計思想・拡張計画・サブモジュール管理方針

本リポジトリは、サブモジュールの情報を正確に取得し、AIによる資料（README.md等）の自動生成・自動更新を標準化することを目的としています。

今後の拡張例：
- サブモジュールの多段管理
- 複数リポジトリ横断の資料生成
- 多言語対応
- CI/CDによる資料自動検証

---

## 📚 関連ドキュメント

- **[AGENTS.md](./AGENTS.md)**: AI コンテキスト・設計思想の詳細
- **[skills/SKILL.md](./skills/update/skills/smart-readme/SKILL.md)**: Smart README Generator の仕様


---

## 🕒 最終更新

このREADMEは **Smart README Generator** により自動生成されました。  
**最終更新日時**: 2026-02-06 04:36:18 (UTC)
