from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout


class ArchiveChats(QWidget):

    def __init__(self):
        super().__init__()
        self.addComponents()

    def addComponents(self):

        self.setLayout(QVBoxLayout())

        for _ in range(30):
            q_label = SingleChat("chat")
            q_label.setFixedHeight(30)
            self.layout().addWidget(q_label)


class ClickLable(QLabel):

    clicked = Signal()

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QLabel("hello"))

    def mousePressEvent(self, event):
        self.clicked.emit()
        print("clicked")


class SingleChat(QWidget):

    clicked = Signal()

    def __init__(self, content: str):
        super().__init__()
        self.content = content
        self.setFixedHeight(50)
        self.addComponents()
        self.addStyle()
        self.addConnections()

    def addComponents(self):
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QLabel(self.content))

        self.layout().setContentsMargins(0, 0, 0, 0)

    def addStyle(self):
        self.setStyleSheet("*{border-bottom: 1px solid #424242;}")

    def addConnections(self):
        pass

    def mousePressEvent(self, event):
        self.clicked.emit()
        print("clicked")
