from typing import List, Dict
from app.core.abstraction import INoteService, INoteRepository, INotifier
from datetime import datetime

class NoteService(INoteService):
    def __init__(self, note_repo: INoteRepository, notifier: INotifier):
        self.repo = note_repo
        self.notifier = notifier

    def add_note(self, title:str, content:str, reminder: datetime = None) -> None:
        note_id = self.repo.create_note(title, content, reminder)
        if reminder:
            self.notifier.reminder(
                note_id,
                reminder,
                f"Напоминание:{title}\n{content}"
            )

    def get_all_notes(self) -> List[Dict]:
        return self.repo.get_notes()

    def delete_note(self, note_id:int) -> None:
        if not self.repo.delete_notes(note_id):
            raise ValueError("Note not found")