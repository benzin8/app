from notifypy import Notify
from datetime import datetime
import threading
from app.core.abstraction import INotifier

class NotifyPyNotifier(INotifier):
    def reminder(self, note_id: int, reminder_time: datetime, message: str) -> None:
        delay = (reminder_time - datetime.now()).total_seconds()
        if delay > 0:
            threading.Timer(delay, self._show_notification, args=[message]).start()

    def _show_notification(self, message: str):
        notification = Notify()
        notification.title = "Напоминание о заметке"
        notification.message = message
        notification.send()
