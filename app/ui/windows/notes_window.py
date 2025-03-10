from app.ui.generated_ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from mysql.connector import connect

from app.core.di import Container

class NotesWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.container = Container()
        self.service = self.container.note_service
        self.selected_note_id = None
        # Подключаем кнопки
        self.btn_add.clicked.connect(self.add_note)
        self.btn_delete.clicked.connect(self.delete_note)

        # Подключаем выбор элемента в списке
        self.list_notes.itemSelectionChanged.connect(self.select_note)
        self.setup_timers()
        self.load_notes()

    def add_note(self):
        title = self.txt_title.text().strip()
        content = self.txt_content.toPlainText().strip()
        reminder = self.datetime_reminder.dateTime().toPython()

        if not title or not content:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        try:
            self.service.add_note(title, content, reminder)
            self.load_notes()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_note(self):
        if not self.selected_note_id:
            return

        try:
            self.service.delete_note(self.selected_note_id)
            self.load_notes()
            self.selected_note_id = None
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_notes(self):
        self.list_notes.clear()
        for note in self.service.get_all_notes():
            item = f"{note['id']}. {note['title']} - {note['content']}"
            if note['reminder']:
                item += f" ({note['reminder'].strftime('%d.%m.%Y %H:%M')})"
            self.list_notes.addItem(item)

    def select_note(self):
        selected = self.list_notes.currentItem()
        if selected:
            note_id = int(selected.text().split('.')[0])
            self.selected_note_id = note_id

    def clear_fields(self):
        self.txt_title.clear()
        self.txt_content.clear()
        self.datetime_reminder.setDateTime(Qt.DateTime.currentDateTime())

    def setup_timers(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_notes)
        self.timer.start(5000)  # Обновление списка каждые 5 секунд