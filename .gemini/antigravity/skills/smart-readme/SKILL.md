# Skill: Smart README Generator

このリポジトリの実装状況を解析し、最新の情報を反映した `README.md` を生成・維持するためのスキルです。

## 概要

ソースコード（Python, Flask等）からAPIエンドポイント、クラス、メソッド、およびディレクトリ構造を抽出し、一貫性のあるドキュメントを生成します。

## トリガー

- 「READMEを更新して」
- 「現在の実装状況をREADMEに反映して」
- 「実装が変わったのでドキュメントを同期して」

## 手順

### 1. 情報の抽出
以下のソースをスキャンして情報を収集します：
- **APIルート**: `repository-A/app.py`（Flaskの `@app.route`）
- **モジュール機能**: `user_management/user_manager.py`（クラスとパブリックメソッド）
- **構成**: リポジトリ全体のディレクトリ構造（`.git`, `node_modules` 等は除外）

### 2. スクリプトの実行
`scripts/generate_readme.py` を使用して、抽出された情報を整形し、ルートの `README.md` を生成します。

```powershell
python scripts/generate_readme.py
```

### 3. 内容の検証
生成された `README.md` が最新の `app.py` や `user_manager.py` の実装（新しいメソッドや削除されたルートなど）と一致しているか、AIとしてダブルチェックします。

## 推奨される README フォーマット

以下は `README.md` の標準テンプレートです。抽出された情報は各セクションに埋め込まれます。

```markdown
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

## 🕒 最終更新
このREADMEは自動生成されました。
最終更新日時: [日時]
```

## 注意事項

- サブリポジトリ `repository-A` 内のファイルは読み取り専用とし、書き換えは行わないこと。
- 書き換え対象はルートディレクトリの `README.md` のみ。
- 自動生成されたセクションには「最終更新日時」を含めること。
