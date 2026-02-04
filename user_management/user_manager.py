from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """ユーザー情報を表すクラス"""
    id: str
    name: str
    email: str
    created_at: datetime


class UserManager:
    """ユーザー管理クラス"""

    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User) -> None:
        """
        ユーザーを追加する

        Args:
            user: 追加するユーザー
        """
        self.users.append(user)

    def delete_user(self, user_id: str) -> bool:
        """
        ユーザーをIDで削除する

        Args:
            user_id: 削除するユーザーのID

        Returns:
            削除に成功した場合True、該当ユーザーがない場合False
        """
        initial_length = len(self.users)
        self.users = [user for user in self.users if user.id != user_id]
        return len(self.users) < initial_length

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        ユーザーをIDで検索する

        Args:
            user_id: 検索するユーザーのID

        Returns:
            ユーザーが見つかった場合そのユーザー、見つからない場合None
        """
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_all_users(self) -> List[User]:
        """
        すべてのユーザーを取得する

        Returns:
            ユーザーのリスト
        """
        return self.users.copy()

    def get_user_count(self) -> int:
        """
        ユーザー数を取得する

        Returns:
            ユーザーの総数
        """
        return len(self.users)
