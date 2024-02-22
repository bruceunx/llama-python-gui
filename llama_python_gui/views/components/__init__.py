from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

from llama_python_gui.assets import resource  # noqa


class ArchiveChats(QWidget):

    def __init__(self):
        super().__init__()
        self.addComponents()
        self.addStyle()

    def addComponents(self):

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5, 2, 5, 2)
        self.layout().setSpacing(1)

        for _ in range(30):
            q_label = SingleChat("chat")
            q_label.setObjectName("chat")
            self.layout().addWidget(q_label)

    def addStyle(self):
        self.setStyleSheet("#chat{border: 1px solid #fff; padding:2px;}")


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
        self.setFixedSize(170, 37)
        self.addComponents()
        self.addStyle()
        self.addConnections()

    def addComponents(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.content = QLabel(self.content)
        self.content.setFixedWidth(100)
        self.layout().addWidget(self.content)

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(QPixmap(":/icons/edit.svg"))
        self.layout().addWidget(self.edit_btn)

        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QPixmap(":/icons/trash-2.svg"))
        self.layout().addWidget(self.delete_btn)

    def addStyle(self):
        self.setStyleSheet("QLabel, QPushButton{border: none;}")

    def addConnections(self):
        pass

    def mousePressEvent(self, event):
        self.clicked.emit()
        print("clicked")
