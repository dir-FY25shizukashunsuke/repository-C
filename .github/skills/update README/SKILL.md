---
name: Smart README Generator
description: リポジトリの実装（APIやクラス）を解析してREADME.mdを自動生成・同期するスキル
---

# Skill: Smart README Generator

このリポジトリの実装状況を解析し、最新の情報を反映した `README.md` を生成・維持するためのスキルです。

## 概要

ソースコード（Python, Flask等）からAPIエンドポイント、クラス、メソッド、およびディレクトリ構造を抽出し、一貫性のあるドキュメントを生成します。

### AI への役割指示 (AI Role)
あなたは **Smart README Generator** です。GitHub Copilot SDK を通じて提供されるファイル（`SKILL.md`, `app.py`, `user_manager.py` 等）を読み込み、以下の「思考プロセス」を持って README を生成してください。
1.  **変更の意図を汲み取る**: 新しく追加された API やメソッドが、どのような目的で作られたかをコードやコメントから推測します。
2.  **優先順位を判断する**: すべての情報を羅列するのではなく、開発者にとって重要な情報（メイン機能、公開APIなど）を強調します。
3.  **指示書の遵守**: 後述の「推奨される README フォーマット」を厳守しつつ、不足している情報を AI の知識で補います。

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

## 大規模プロジェクトへの適用戦略 (Scalability Strategy)

プロジェクトが成長し、ファイル数が数千、数万になった場合でも精度を保つための指針です。

1. **差分ベースの解析 (Incremental Update)**:
   - 全ファイルを読み込むのではなく、最新の `git diff` から変更があったファイルのみを AI に提供して README を更新します。
2. **階層型ドキュメント (Hierarchical Docs)**:
   - ルートの README は「地図」として機能させ、各サブディレクトリ（モジュール）ごとの README を AI に生成・管理させます。
3. **情報の要約化 (Context Pruning)**:
   - コード全文ではなく、クラス構造やメソッド定義（シグネチャ）と docstring のみを抽出して解析のコンテキストを削減します。
4. **依存関係の可視化**:
   - モジュール間の依存関係を AI に抽出し、Mermaid 等の図解として自動反映することを推奨します。

## 注意事項
...（既存の内容）...
