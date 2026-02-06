"""
To-Do管理APIアプリケーション
Flask を使用した RESTful API
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import sys
import os

# todo_managementモジュールをインポートするためにパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from todo_management.todo_manager import Todo, TodoManager

app = Flask(__name__)
todo_manager = TodoManager()


@app.route('/', methods=['GET'])
def home():
    """
    ホームエンドポイント - API確認用
    """
    return jsonify({
        'message': 'To-Do管理API へようこそ！',
        'endpoints': {
            'GET /api/todos': 'すべてのTo-Doを取得',
            'POST /api/todos': 'To-Doを作成',
            'GET /api/todos/<todo_id>': '特定のTo-Doを取得',
            'PATCH /api/todos/<todo_id>': 'To-Doを更新',
            'DELETE /api/todos/<todo_id>': 'To-Doを削除',
            'POST /api/todos/<todo_id>/toggle': 'To-Doの完了状態を切り替え',
            'GET /api/todos/stats': 'To-Doの統計情報を取得'
        }
    }), 200


@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    """
    すべてのTo-Doを取得
    """
    todos = todo_manager.get_all_todos()
    todos_dict = [
        {
            'id': todo.id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo.created_at.isoformat(),
            'updated_at': todo.updated_at.isoformat()
        }
        for todo in todos
    ]
    return jsonify({'todos': todos_dict}), 200


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    To-Doを作成
    リクエストボディ: { "title": "タイトル" }
    """
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'タイトルは必須です'}), 400
    
    title = data.get('title', '').strip()
    
    if not title:
        return jsonify({'error': 'タイトルを入力してください'}), 400
    
    # 新しいTo-Doを作成
    now = datetime.now()
    new_todo = Todo(
        id=str(uuid.uuid4()),
        title=title,
        completed=False,
        created_at=now,
        updated_at=now
    )
    
    todo_manager.add_todo(new_todo)
    
    return jsonify({
        'message': 'To-Doが作成されました',
        'todo': {
            'id': new_todo.id,
            'title': new_todo.title,
            'completed': new_todo.completed,
            'created_at': new_todo.created_at.isoformat(),
            'updated_at': new_todo.updated_at.isoformat()
        }
    }), 201


@app.route('/api/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """
    特定のTo-Doを取得
    """
    todo = todo_manager.get_todo_by_id(todo_id)
    
    if todo is None:
        return jsonify({'error': 'To-Doが見つかりません'}), 404
    
    return jsonify({
        'todo': {
            'id': todo.id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo.created_at.isoformat(),
            'updated_at': todo.updated_at.isoformat()
        }
    }), 200


@app.route('/api/todos/<todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    """
    To-Doを更新
    リクエストボディ: { "title": "新しいタイトル" } (オプション)
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'リクエストボディが必要です'}), 400
    
    title = data.get('title')
    
    if title is not None:
        title = title.strip()
        if not title:
            return jsonify({'error': 'タイトルを入力してください'}), 400
    
    updated_todo = todo_manager.update_todo(todo_id, title=title)
    
    if updated_todo is None:
        return jsonify({'error': 'To-Doが見つかりません'}), 404
    
    return jsonify({
        'message': 'To-Doが更新されました',
        'todo': {
            'id': updated_todo.id,
            'title': updated_todo.title,
            'completed': updated_todo.completed,
            'created_at': updated_todo.created_at.isoformat(),
            'updated_at': updated_todo.updated_at.isoformat()
        }
    }), 200


@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    To-Doを削除
    """
    success = todo_manager.delete_todo(todo_id)
    
    if not success:
        return jsonify({'error': 'To-Doが見つかりません'}), 404
    
    return jsonify({
        'message': 'To-Doが削除されました',
        'id': todo_id
    }), 200


@app.route('/api/todos/<todo_id>/toggle', methods=['POST'])
def toggle_todo(todo_id):
    """
    To-Doの完了状態を切り替え
    """
    updated_todo = todo_manager.toggle_todo(todo_id)
    
    if updated_todo is None:
        return jsonify({'error': 'To-Doが見つかりません'}), 404
    
    return jsonify({
        'message': 'To-Doの状態が更新されました',
        'todo': {
            'id': updated_todo.id,
            'title': updated_todo.title,
            'completed': updated_todo.completed,
            'created_at': updated_todo.created_at.isoformat(),
            'updated_at': updated_todo.updated_at.isoformat()
        }
    }), 200


@app.route('/api/todos/stats', methods=['GET'])
def get_todo_stats():
    """
    To-Doの統計情報を取得
    """
    all_todos = todo_manager.get_all_todos()
    total_count = len(all_todos)
    completed_count = sum(1 for todo in all_todos if todo.completed)
    pending_count = total_count - completed_count
    
    return jsonify({
        'total_todos': total_count,
        'completed_todos': completed_count,
        'pending_todos': pending_count
    }), 200


if __name__ == '__main__':
    # 開発用サーバーを起動
    app.run(debug=True, host='0.0.0.0', port=5000)
