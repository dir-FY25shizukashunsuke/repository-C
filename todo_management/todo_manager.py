from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Todo:
    """
    To-Do情報を表すクラス。
    Attributes:
        id (str): To-Do ID
        title (str): To-Doのタイトル
        completed (bool): 完了状態
        created_at (datetime): 作成日時
        updated_at (datetime): 更新日時
    """
    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class TodoManager:
    """
    To-Do管理クラス。
    - add_todo: To-Do追加
    - delete_todo: To-Do削除
    - get_todo_by_id: IDでTo-Do検索
    - get_all_todos: 全To-Do取得
    - get_todo_count: To-Do総数取得
    - update_todo: To-Do情報更新
    - toggle_todo: To-Doの完了状態を切り替え
    """

    def __init__(self):
        self.todos: List[Todo] = []

    def add_todo(self, todo: Todo) -> None:
        """
        To-Doを追加する。
        Args:
            todo (Todo): 追加するTo-Do
        Returns:
            None
        """
        self.todos.append(todo)

    def delete_todo(self, todo_id: str) -> bool:
        """
        To-DoをIDで削除する。
        Args:
            todo_id (str): 削除するTo-DoのID
        Returns:
            bool: 削除に成功した場合True、該当To-Doがない場合False
        """
        initial_length = len(self.todos)
        self.todos = [todo for todo in self.todos if todo.id != todo_id]
        return len(self.todos) < initial_length

    def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """
        To-DoをIDで検索する。
        Args:
            todo_id (str): 検索するTo-DoのID
        Returns:
            Optional[Todo]: To-Doが見つかった場合そのTo-Do、見つからない場合None
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def get_all_todos(self) -> List[Todo]:
        """
        全To-Doを取得する。
        Returns:
            List[Todo]: To-Do一覧
        """
        return self.todos.copy()

    def get_todo_count(self) -> int:
        """
        To-Do数を取得する。
        Returns:
            int: To-Doの総数
        """
        return len(self.todos)

    def update_todo(self, todo_id: str, title: Optional[str] = None) -> Optional[Todo]:
        """
        To-Do情報を更新する。
        Args:
            todo_id (str): 更新するTo-DoのID
            title (Optional[str]): 新しいタイトル
        Returns:
            Optional[Todo]: 更新されたTo-Do、見つからない場合None
        """
        todo = self.get_todo_by_id(todo_id)
        if todo is None:
            return None
        
        if title is not None:
            # イミュータブルなパターンに従い、新しいインスタンスを作成
            updated_todo = Todo(
                id=todo.id,
                title=title,
                completed=todo.completed,
                created_at=todo.created_at,
                updated_at=datetime.now()
            )
            # リスト内の要素を置き換え
            self.todos = [updated_todo if t.id == todo_id else t for t in self.todos]
            return updated_todo
        
        return todo

    def toggle_todo(self, todo_id: str) -> Optional[Todo]:
        """
        To-Doの完了状態を切り替える。
        Args:
            todo_id (str): 切り替えるTo-DoのID
        Returns:
            Optional[Todo]: 更新されたTo-Do、見つからない場合None
        """
        todo = self.get_todo_by_id(todo_id)
        if todo is None:
            return None
        
        # 完了状態を反転
        updated_todo = Todo(
            id=todo.id,
            title=todo.title,
            completed=not todo.completed,
            created_at=todo.created_at,
            updated_at=datetime.now()
        )
        # リスト内の要素を置き換え
        self.todos = [updated_todo if t.id == todo_id else t for t in self.todos]
        return updated_todo
