"""
todo_managementモジュールの使用例
"""

from todo_manager import TodoManager, Todo
from datetime import datetime


def main():
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
    todo2 = Todo(
        id='todo_2',
        title='買い物に行く',
        completed=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    todo3 = Todo(
        id='todo_3',
        title='レポートを書く',
        completed=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    manager.add_todo(todo1)
    manager.add_todo(todo2)
    manager.add_todo(todo3)

    print(f"To-Do数: {manager.get_todo_count()}")  # 3
    print(f"すべてのTo-Do: {manager.get_all_todos()}\n")

    # To-Doを検索
    todo = manager.get_todo_by_id('todo_1')
    print(f"todo_1を検索: {todo}\n")

    # To-Doを更新
    print("todo_1のタイトルを更新します")
    updated = manager.update_todo('todo_1', title='Flaskの勉強')
    print(f"更新されたTo-Do: {updated}\n")

    # To-Doの完了状態を切り替え
    print("todo_2の完了状態を切り替えます")
    toggled = manager.toggle_todo('todo_2')
    print(f"切り替え後のTo-Do: {toggled}")
    print(f"完了状態: {toggled.completed}\n")

    # To-Doを削除
    print("todo_1を削除します")
    deleted = manager.delete_todo('todo_1')
    print(f"削除成功: {deleted}")
    print(f"To-Do数: {manager.get_todo_count()}")  # 2

    # 存在しないTo-Doを削除
    print(f"\ntodo_999を削除します")
    deleted = manager.delete_todo('todo_999')
    print(f"削除成功: {deleted}")  # False
    print(f"To-Do数: {manager.get_todo_count()}")  # 2

    # 統計情報
    all_todos = manager.get_all_todos()
    completed = sum(1 for t in all_todos if t.completed)
    pending = len(all_todos) - completed
    print(f"\n統計情報:")
    print(f"  総To-Do数: {len(all_todos)}")
    print(f"  完了: {completed}")
    print(f"  未完了: {pending}")


if __name__ == '__main__':
    main()
