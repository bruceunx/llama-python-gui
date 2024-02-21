from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ArchiveChats(QWidget):

    def __init__(self):
        super().__init__()
        self.addComponents()

    def addComponents(self):

        self.setLayout(QVBoxLayout())

        for _ in range(30):
            q_label = QLabel("chat")
            q_label.setFixedHeight(30)
            self.layout().addWidget(q_label)
