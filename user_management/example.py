"""
user_managementモジュールの使用例
"""

from user_manager import UserManager, User
from datetime import datetime


def main():
    # マネージャーを初期化
    manager = UserManager()

    # ユーザーを追加
    user1 = User(
        id='user_1',
        name='Alice',
        email='alice@example.com',
        created_at=datetime.now()
    )
    user2 = User(
        id='user_2',
        name='Bob',
        email='bob@example.com',
        created_at=datetime.now()
    )

    manager.add_user(user1)
    manager.add_user(user2)

    print(f"ユーザー数: {manager.get_user_count()}")  # 2
    print(f"すべてのユーザー: {manager.get_all_users()}")

    # ユーザーを検索
    user = manager.get_user_by_id('user_1')
    print(f"user_1を検索: {user}")

    # ユーザーを削除
    print(f"\nuser_1を削除します")
    deleted = manager.delete_user('user_1')
    print(f"削除成功: {deleted}")
    print(f"ユーザー数: {manager.get_user_count()}")  # 1

    # 存在しないユーザーを削除
    print(f"\nuser_999を削除します")
    deleted = manager.delete_user('user_999')
    print(f"削除成功: {deleted}")  # False
    print(f"ユーザー数: {manager.get_user_count()}")  # 1


if __name__ == '__main__':
    main()
