from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """
    ユーザー情報を表すクラス。
    Attributes:
        id (str): ユーザーID
        name (str): ユーザー名
        email (str): メールアドレス
        created_at (datetime): 登録日時
    """
    id: str
    name: str
    email: str
    created_at: datetime


class UserManager:
    """
    ユーザー管理クラス。
    - add_user: ユーザー追加
    - delete_user: ユーザー削除
    - get_user_by_id: IDでユーザー検索
    - get_all_users: 全ユーザー取得
    - get_user_count: ユーザー総数取得
    - update_user: ユーザー情報更新（拡張予定）
    - search_users: 条件検索（拡張予定）
    """

    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User) -> None:
        """
        ユーザーを追加する。
        Args:
            user (User): 追加するユーザー
        Returns:
            None
        """
        self.users.append(user)

    def delete_user(self, user_id: str) -> bool:
        """
        ユーザーをIDで削除する。
        Args:
            user_id (str): 削除するユーザーのID
        Returns:
            bool: 削除に成功した場合True、該当ユーザーがない場合False
        """
        initial_length = len(self.users)
        self.users = [user for user in self.users if user.id != user_id]
        return len(self.users) < initial_length

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        ユーザーをIDで検索する。
        Args:
            user_id (str): 検索するユーザーのID
        Returns:
            Optional[User]: ユーザーが見つかった場合そのユーザー、見つからない場合None
        """
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_all_users(self) -> List[User]:
        """
        全ユーザーを取得する。
        Returns:
            List[User]: ユーザー一覧
        """
        return self.users.copy()

    def get_user_count(self) -> int:
        """
        ユーザー数を取得する。
        Returns:
            int: ユーザーの総数
        """
        return len(self.users)
