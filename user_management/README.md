# User Management Module

ユーザー管理モジュールです。。

## 機能

- **ユーザー追加**: 新しいユーザーをデータベースへ追加
- **ユーザー削除**: 指定されたIDのユーザーを削除
- **ユーザー検索**: IDでユーザーを検索
- **一覧取得**: すべてのユーザーを取得

## 使用例

```python
from user_manager import UserManager, User
from datetime import datetime

manager = UserManager()

# ユーザーを追加
user = User(
    id='1',
    name='John Doe',
    email='john@example.com',
    created_at=datetime.now()
)
manager.add_user(user)

# ユーザーを削除
deleted = manager.delete_user('1')
print(deleted)  # True

# ユーザーを削除（存在しない場合）
deleted = manager.delete_user('999')
print(deleted)  # False
```

## API

### UserManager

#### `delete_user(user_id: str) -> bool`

指定されたIDのユーザーを削除します。

- **パラメータ**: `user_id` - 削除するユーザーのID
- **戻り値**: `bool` - 削除に成功した場合True、該当ユーザーがない場合False

#### `add_user(user: User) -> None`

ユーザーを追加します。

#### `get_user_by_id(user_id: str) -> Optional[User]`

IDでユーザーを検索します。

#### `get_all_users() -> List[User]`

すべてのユーザーを取得します。

#### `get_user_count() -> int`

ユーザー数を取得します。
