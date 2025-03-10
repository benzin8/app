from typing import List, Dict

from app.core.abstraction import INoteRepository
from datetime import datetime
import mysql.connector

class MySQLNoteRepository(INoteRepository):
    def __init__(self, host:str, user:str, password:str, database:str):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("✅ Успешное подключение к базе данных")
            self._create_table()
        except Exception as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            raise
    def _create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    reminder DATETIME
                )
            """)
            self.conn.commit()

    def create_note(self, title:str, content:str, reminder: datetime = None) -> int:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO notes (title, content, reminder) VALUES (%s, %s, %s)",
                    (title, content, reminder)
                )
                self.conn.commit()
                print(f"✅ Заметка сохранена: {title}")
                return cursor.lastrowid
        except Exception as e:
            print(f"❌ Ошибка сохранения заметки: {e}")
            self.conn.rollback()
            raise

    def get_notes(self) -> List[Dict]:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM notes")
            return cursor.fetchall()

    def delete_notes(self, note_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM notes WHERE id = %s",
                           (note_id,)
                           )
            self.conn.commit()
            return cursor.rowcount > 0