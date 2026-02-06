# To-Do管理API ドキュメント

Flask を使用した RESTful API による To-Do 管理システムです。

## ベースURL

```
http://localhost:5000
```

## エンドポイント一覧

### 1. ホーム (API確認)

**GET** `/`

APIの動作確認と利用可能なエンドポイント一覧を取得します。

**レスポンス例:**
```json
{
  "message": "To-Do管理API へようこそ！",
  "endpoints": {
    "GET /api/todos": "すべてのTo-Doを取得",
    "POST /api/todos": "To-Doを作成",
    "GET /api/todos/<todo_id>": "特定のTo-Doを取得",
    "PATCH /api/todos/<todo_id>": "To-Doを更新",
    "DELETE /api/todos/<todo_id>": "To-Doを削除",
    "POST /api/todos/<todo_id>/toggle": "To-Doの完了状態を切り替え",
    "GET /api/todos/stats": "To-Doの統計情報を取得"
  }
}
```

---

### 2. すべてのTo-Doを取得

**GET** `/api/todos`

すべてのTo-Doを取得します。

**レスポンス例:**
```json
{
  "todos": [
    {
      "id": "3ca31f3f-900e-47eb-992e-d79b6c95b24d",
      "title": "Pythonの勉強",
      "completed": false,
      "created_at": "2026-02-06T04:30:41.995195",
      "updated_at": "2026-02-06T04:30:41.995195"
    }
  ]
}
```

---

### 3. To-Doを作成

**POST** `/api/todos`

新しいTo-Doを作成します。

**リクエストボディ:**
```json
{
  "title": "買い物に行く"
}
```

**バリデーション:**
- `title`: 必須、空でない文字列

**レスポンス (201 Created):**
```json
{
  "message": "To-Doが作成されました",
  "todo": {
    "id": "3b40610a-6a93-4f61-b9ed-20e289fe0658",
    "title": "買い物に行く",
    "completed": false,
    "created_at": "2026-02-06T04:30:42.029092",
    "updated_at": "2026-02-06T04:30:42.029092"
  }
}
```

**エラーレスポンス (400 Bad Request):**
```json
{
  "error": "タイトルは必須です"
}
```

---

### 4. 特定のTo-Doを取得

**GET** `/api/todos/<todo_id>`

指定されたIDのTo-Doを取得します。

**パスパラメータ:**
- `todo_id`: To-DoのID (UUID形式)

**レスポンス (200 OK):**
```json
{
  "todo": {
    "id": "3ca31f3f-900e-47eb-992e-d79b6c95b24d",
    "title": "Pythonの勉強",
    "completed": false,
    "created_at": "2026-02-06T04:30:41.995195",
    "updated_at": "2026-02-06T04:30:41.995195"
  }
}
```

**エラーレスポンス (404 Not Found):**
```json
{
  "error": "To-Doが見つかりません"
}
```

---

### 5. To-Doを更新

**PATCH** `/api/todos/<todo_id>`

指定されたIDのTo-Doのタイトルを更新します。

**パスパラメータ:**
- `todo_id`: To-DoのID (UUID形式)

**リクエストボディ:**
```json
{
  "title": "スーパーで買い物"
}
```

**バリデーション:**
- `title`: 任意、空でない文字列

**レスポンス (200 OK):**
```json
{
  "message": "To-Doが更新されました",
  "todo": {
    "id": "3b40610a-6a93-4f61-b9ed-20e289fe0658",
    "title": "スーパーで買い物",
    "completed": false,
    "created_at": "2026-02-06T04:30:42.029092",
    "updated_at": "2026-02-06T04:30:42.161938"
  }
}
```

**エラーレスポンス (404 Not Found):**
```json
{
  "error": "To-Doが見つかりません"
}
```

---

### 6. To-Doを削除

**DELETE** `/api/todos/<todo_id>`

指定されたIDのTo-Doを削除します。

**パスパラメータ:**
- `todo_id`: To-DoのID (UUID形式)

**レスポンス (200 OK):**
```json
{
  "message": "To-Doが削除されました",
  "id": "3b40610a-6a93-4f61-b9ed-20e289fe0658"
}
```

**エラーレスポンス (404 Not Found):**
```json
{
  "error": "To-Doが見つかりません"
}
```

---

### 7. To-Doの完了状態を切り替え

**POST** `/api/todos/<todo_id>/toggle`

指定されたIDのTo-Doの完了状態を切り替えます（未完了→完了、完了→未完了）。

**パスパラメータ:**
- `todo_id`: To-DoのID (UUID形式)

**レスポンス (200 OK):**
```json
{
  "message": "To-Doの状態が更新されました",
  "todo": {
    "id": "3b40610a-6a93-4f61-b9ed-20e289fe0658",
    "title": "スーパーで買い物",
    "completed": true,
    "created_at": "2026-02-06T04:30:42.029092",
    "updated_at": "2026-02-06T04:30:42.195315"
  }
}
```

**エラーレスポンス (404 Not Found):**
```json
{
  "error": "To-Doが見つかりません"
}
```

---

### 8. To-Doの統計情報を取得

**GET** `/api/todos/stats`

To-Doの統計情報（総数、完了数、未完了数）を取得します。

**レスポンス (200 OK):**
```json
{
  "total_todos": 2,
  "completed_todos": 1,
  "pending_todos": 1
}
```

---

## データモデル

### Todo

| フィールド | 型 | 説明 |
|-----------|---|------|
| `id` | `string` (UUID) | To-DoのユニークID |
| `title` | `string` | To-Doのタイトル |
| `completed` | `boolean` | 完了状態 (true: 完了, false: 未完了) |
| `created_at` | `string` (ISO 8601) | 作成日時 |
| `updated_at` | `string` (ISO 8601) | 更新日時 |

---

## 使用例

### cURLを使った例

```bash
# To-Doを作成
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Pythonの勉強"}'

# すべてのTo-Doを取得
curl http://localhost:5000/api/todos

# To-Doを更新
curl -X PATCH http://localhost:5000/api/todos/<todo_id> \
  -H "Content-Type: application/json" \
  -d '{"title": "Flaskの勉強"}'

# To-Doの完了状態を切り替え
curl -X POST http://localhost:5000/api/todos/<todo_id>/toggle

# To-Doを削除
curl -X DELETE http://localhost:5000/api/todos/<todo_id>

# 統計情報を取得
curl http://localhost:5000/api/todos/stats
```

---

## サーバーの起動

```bash
# 依存関係をインストール
pip install -r requirements.txt

# サーバーを起動
python app.py
```

サーバーは `http://localhost:5000` でリッスンします。
