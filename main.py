import sys

from PySide6.QtWidgets import QApplication
from app.ui.windows.notes_window import NotesWindow

if __name__ == "__main__":
    app =QApplication(sys.argv)
    window = NotesWindow()
    window.setWindowTitle("Заметки")
    window.show()
    sys.exit(app.exec())