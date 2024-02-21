from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ArchiveChats(QWidget):

    def __init__(self):
        super().__init__()
        self.addComponents()

    def addComponents(self):

        self.setLayout(QVBoxLayout())

        for _ in range(30):
            q_label = ClickLable("chat")
            q_label.setFixedHeight(30)
            self.layout().addWidget(q_label)


class ClickLable(QLabel):

    clicked = Signal()

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def mousePressEvent(self, event):
        self.clicked.emit()
        print("clicked")
