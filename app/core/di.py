from app.database.mysql_note_repository import MySQLNoteRepository
from app.notifications.notifications import NotifyPyNotifier
from app.logic.note_service import NoteService

class Container:
    def __init__(self):
        self.note_repo = MySQLNoteRepository(
            host="localhost",
            user="root",
            password="",
            database="notes_app"
        )
        self.notifier = NotifyPyNotifier()
        self.note_service = NoteService(self.note_repo, self.notifier)