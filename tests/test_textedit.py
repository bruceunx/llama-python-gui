from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget


class ExpandingTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_scroll_bar = self.verticalScrollBar()
        self.setReadOnly(True)
        self.vertical_scroll_bar.rangeChanged.connect(self.update_scrollbar)

    def update_scrollbar(self, min, max):
        w, h = self.width(), self.height()
        self.resize(w, h + max)

    def add_message(self, message: str) -> None:
        self.setPlainText(self.toPlainText() + "\n" + message)


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 500)
        self.setLayout(QVBoxLayout())

        self.textEdit = ExpandingTextEdit()
        self.textEdit.setPlainText(
            "This is some sample text.")  # Add some content
        self.layout().addWidget(self.textEdit, 0, Qt.AlignmentFlag.AlignTop)

        # self.textEdit.vertical_scroll_bar.rangeChanged.connect(
        #     self.update_scrollbar)

        self.add_chat = QPushButton("Add Chat")
        self.add_chat.clicked.connect(
            lambda: self.textEdit.add_message("This is some sample text."))
        self.layout().addWidget(self.add_chat)

    # def update_scrollbar(self, min, max):
    #     w, h = self.textEdit.width(), self.textEdit.height()
    #     self.textEdit.resize(w, h + max)


if __name__ == "__main__":
    import sys
    app = QApplication([])
    main = MainWidget()
    main.show()
    sys.exit(app.exec())
