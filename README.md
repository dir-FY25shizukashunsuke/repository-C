
# repository-C Project (Smart README)

**複数サブモジュール情報をもとに資料（README.md等）を自動生成・管理する専用リポジトリ**

このリポジトリは、複数のサブモジュール（`repository-A`、`repository-B`）の最新情報を自動取得し、AIによるREADME.md等の資料生成・自動更新を行うための専用リポジトリです。

---

## 🏗 ディレクトリ構成

```text
repository-C/
├── AGENTS.md                    # AI コンテキスト・設計思想
├── README.md                    # 本ファイル（自動生成）
├── .gitmodules                  # サブモジュール設定
├── 自動化説明資料.md            # GitHub Actions自動化の解説
├── repository-A/                # ユーザー登録API（サブモジュール）
│   ├── app.py                   # Flask 実装（ポート: 5000）
│   ├── server.js                # Node.js/Express 実装（ポート: 3000）
│   ├── db.js                    # SQLiteデータベース接続層
│   ├── requirements.txt         # Python 依存関係
│   ├── package.json             # Node.js 依存関係
│   └── test/                    # テスト関連
│       └── test.md
├── repository-B/                # FastAPI サーバー（サブモジュール）
│   ├── main.py                  # FastAPI アプリケーション本体
│   ├── requirements.txt         # Python 依存関係
│   └── test_api.py              # API テストファイル
└── .github/
    ├── workflows/               # ワークフロー定義
    └── skills/
        └── update README/
            └── SKILL.md         # Smart README Generator スキル定義
```

---

## 🚀 サブモジュール概要

### repository-A: ユーザー登録API

`repository-A` は、ユーザー登録機能を持つAPIサーバーで、**Flask** と **Node.js/Express** の2つの実装を提供しています。

#### Flask 実装（app.py）
- **ポート**: 5000
- **フレームワーク**: Flask + SQLAlchemy
- **データベース**: SQLite (`users.db`)

#### Node.js 実装（server.js + db.js）
- **ポート**: 3000
- **フレームワーク**: Express.js
- **データベース**: SQLite (`users.db`) + bcryptjs

#### API エンドポイント（両実装共通）

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/` | ホーム（API 確認用） | - | `{ "message": "ユーザー登録API へようこそ！" }` |
| `POST` | `/api/users/register` | ユーザー登録 | `{ "username", "email", "password", "passwordConfirm" }` | 201: `{ "message", "user" }` / 400: エラー |
| `PATCH` | `/api/users/<user_id>` | ユーザー情報更新 | `{ "username", "email" }` (任意) | 200: `{ "message", "user" }` / 404: Not Found |

#### セキュリティ機能
- パスワードハッシュ化（Flask: `werkzeug.security.generate_password_hash`、Node.js: `bcryptjs`）
- メールアドレス形式検証（正規表現）
- ユーザー名・メール重複チェック
- パスワード最小長（6文字以上）
- SQL インジェクション対策（Flask: SQLAlchemy ORM、Node.js: パラメータ化クエリ）

#### データモデル (`User`)
| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | Integer | 主キー（自動採番） |
| `username` | String(80) | ユーザー名（ユニーク） |
| `email` | String(120) | メールアドレス（ユニーク） |
| `password` | String(255) | ハッシュ化されたパスワード |
| `created_at` | DateTime | 登録日時（自動設定） |

---

### repository-B: FastAPI サーバー

`repository-B` は、FastAPIで構築されたシンプルなAPIサーバーです。

#### 実装情報
- **フレームワーク**: FastAPI
- **言語**: Python
- **説明**: 文字列操作と数値計算のAPIを提供

#### API エンドポイント

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| `GET` | `/hello` | Hello メッセージを返す | - | `{ "message": "HELLO" }` |
| `POST` | `/add` | 2つの数値の合計を返す | `{ "a": int, "b": int }` | `{ "result": int }` |
| `POST` | `/reverse` | 文字列を逆順にして返す | `{ "text": str }` | `{ "reversed": str }` |
| `POST` | `/length` | 文字列の長さを返す | `{ "text": str }` | `{ "length": int }` |

---

## 設計思想・拡張計画・サブモジュール管理方針

本リポジトリは、複数サブモジュールの情報を正確に取得し、AIによる資料（README.md等）の自動生成・自動更新・統合を標準化することを目的としています。

### 主な特徴
- **複数サブモジュール管理**: repository-A（ユーザー登録API）、repository-B（FastAPI）など、複数のサブモジュールを統合管理
- **2つの実装パターン**: repository-Aでは Flask と Node.js/Express の両方の実装を提供し、開発者が選択可能
- **自動化ワークフロー**: GitHub Actionsによるサブモジュール更新、Issue作成、AI資料生成の完全自動化
- **AI活用**: AGENTS.md と SKILL.md に基づき、AIが最新の実装状況を自動反映

### 今後の拡張例
- サブモジュールの多段管理
- 複数サブモジュール・複数リポジトリ横断の資料生成
- サブモジュールごとの個別資料と統合資料の自動生成
- 多言語対応
- CI/CDによる資料自動検証
- API仕様の自動抽出とOpenAPI形式でのエクスポート

---

## 📚 関連ドキュメント

- **[AGENTS.md](./AGENTS.md)**: AI コンテキスト・設計思想の詳細
- **[SKILL.md](./.github/skills/update%20README/SKILL.md)**: Smart README Generator の仕様
- **[自動化説明資料.md](./自動化説明資料.md)**: GitHub Actions 自動化ワークフローの詳細解説

---

## 🕒 最終更新

このREADMEは **Smart README Generator** により自動生成されました。  
**最終更新日時**: 2026-02-10 04:46:00 (UTC)

---

## 使用 AI モデル

**gpt-5.2-codex**
