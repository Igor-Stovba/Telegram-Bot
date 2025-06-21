import sqlite3

from datetime import datetime
from typing import List, Optional

class TaskManager:
    def __init__(self, db_name: str = "tasks.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                deadline TEXT,
                important INTEGER CHECK (important IN (0, 1)),
                urgent INTEGER CHECK (urgent IN (0, 1)),
                completed INTEGER CHECK (completed IN (0, 1)),
                notify INTEGER CHECK (notify IN (0, 1))
            )
        ''')
        self.conn.commit()

    def disable_notification(self, task_id: int):
        self.cursor.execute('''
            UPDATE tasks SET notify = 0 WHERE id = ?
        ''', (task_id,))
        self.conn.commit()

    def get_all_users(self) -> List[int]:
        self.cursor.execute('SELECT DISTINCT user_id FROM tasks')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
    
    def add_task(self, user_id: int, description: str, deadline: Optional[str], important: bool, urgent: bool, notify: bool):
        self.cursor.execute('''
            INSERT INTO tasks (user_id, description, deadline, important, urgent, completed, notify)
            VALUES (?, ?, ?, ?, ?, 0, ?)
        ''', (user_id, description, deadline, int(important), int(urgent), int(notify)))
        self.conn.commit()
    
    def get_tasks(self, user_id: int) -> List[dict]:
        self.cursor.execute('''
            SELECT id, description, deadline, important, urgent, completed, notify FROM tasks WHERE user_id = ?
        ''', (user_id,))
        rows = self.cursor.fetchall()
        return [
            {
                "id": row[0],
                "description": row[1],
                "deadline": row[2],
                "important": bool(row[3]),
                "urgent": bool(row[4]),
                "completed": bool(row[5]),
                "notify": bool(row[6]),
            }
            for row in rows
        ]
    
    def mark_task_completed(self, task_id: int):
        self.cursor.execute('''
            UPDATE tasks SET completed = 1 WHERE id = ?
        ''', (task_id,))
        self.conn.commit()
    
    def delete_task(self, task_id: int):
        self.cursor.execute('''
            DELETE FROM tasks WHERE id = ?
        ''', (task_id,))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

class ChatManager:
    def __init__(self, db_name: str = "chats.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE NOT NULL
            )
        ''')
        self.conn.commit()

    def add_chat(self, chat_id: int):
        """Добавляет chat_id, если он ещё не был добавлен."""
        try:
            self.cursor.execute('''
                INSERT INTO chats (chat_id) VALUES (?)
            ''', (chat_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении chat_id: {e}")
    
    def get_all_chat_ids(self) -> List[int]:
        self.cursor.execute('SELECT chat_id FROM chats')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
    
    def close(self):
        self.conn.close()