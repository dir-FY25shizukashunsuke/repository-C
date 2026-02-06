# To-Do Management Module

To-Do管理機能を提供するPythonモジュールです。クリーンアーキテクチャに基づいた設計で、型安全性とイミュータブル性を重視しています。

## 機能

- To-Doの追加、削除、検索、更新
- To-Doの完了状態の切り替え
- To-Do一覧の取得
- 統計情報の取得

## クラス

### `Todo` (dataclass)

To-Do情報を表すイミュータブルなデータクラス。

| 属性 | 型 | 説明 |
|-----|---|------|
| `id` | `str` | To-Do ID |
| `title` | `str` | To-Doのタイトル |
| `completed` | `bool` | 完了状態 |
| `created_at` | `datetime` | 作成日時 |
| `updated_at` | `datetime` | 更新日時 |

### `TodoManager`

To-Do管理のビジネスロジックを提供するクラス。

| メソッド | 引数 | 戻り値 | 説明 |
|---------|-----|--------|------|
| `__init__()` | - | `None` | コンストラクタ。空のTo-Doリストを初期化 |
| `add_todo(todo: Todo)` | `todo: Todo` | `None` | To-Doを追加 |
| `delete_todo(todo_id: str)` | `todo_id: str` | `bool` | To-Doを削除（成功: True / 失敗: False） |
| `get_todo_by_id(todo_id: str)` | `todo_id: str` | `Optional[Todo]` | IDでTo-Doを検索（見つからない場合: None） |
| `get_all_todos()` | - | `List[Todo]` | 全To-Doを取得（コピーを返却） |
| `get_todo_count()` | - | `int` | To-Do総数を取得 |
| `update_todo(todo_id: str, title: Optional[str])` | `todo_id: str`, `title: Optional[str]` | `Optional[Todo]` | To-Do情報を更新 |
| `toggle_todo(todo_id: str)` | `todo_id: str` | `Optional[Todo]` | To-Doの完了状態を切り替え |

## 使用例

```python
from todo_management.todo_manager import TodoManager, Todo
from datetime import datetime

# マネージャーを初期化
manager = TodoManager()

# To-Doを追加
todo1 = Todo(
    id='todo_1',
    title='Pythonの勉強',
    completed=False,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
manager.add_todo(todo1)

# To-Doを検索
todo = manager.get_todo_by_id('todo_1')
print(todo)

# To-Doを更新
updated = manager.update_todo('todo_1', title='Flaskの勉強')

# 完了状態を切り替え
toggled = manager.toggle_todo('todo_1')

# To-Doを削除
deleted = manager.delete_todo('todo_1')
```

## 設計原則

- **イミュータブル返却**: `get_all_todos` はコピーを返す
- **型ヒントの完全活用**: すべての関数に型注釈を付与
- **docstringによる自己文書化**: すべてのクラスとメソッドにドキュメントを記載
- **副作用の最小化**: 状態変更を伴うメソッドは明確に `bool` や `None` を返す
