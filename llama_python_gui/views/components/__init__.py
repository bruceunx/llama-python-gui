from typing import List, Dict

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

from llama_python_gui.assets import resource  # noqa


class ChangeTitle(QDialog):

    def __init__(self, title: str):
        super().__init__()
        self._title = title
        self.setFixedSize(270, 150)
        self.setWindowTitle("修改标题")
        self.addComponents()
        self.addStyle()

    def addComponents(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("修改标题"))
        self.title_input = QLineEdit()
        self.title_input.setText(self._title)
        self.layout().addWidget(self.title_input)

        foot_frame = QFrame()
        self.layout().addWidget(foot_frame, 0, Qt.AlignmentFlag.AlignBottom)
        self.save_btn = QPushButton("保存")
        self.cancel_btn = QPushButton("取消")
        foot_frame.setLayout(QHBoxLayout())
        foot_frame.layout().addWidget(self.save_btn)
        foot_frame.layout().addWidget(self.cancel_btn)

        self.cancel_btn.clicked.connect(self.close)
        self.save_btn.clicked.connect(self.accept)

    def addStyle(self):
        self.setStyleSheet(
            "QLabel{font-size: 18pt;} QLineEdit{padding:5px;} QPushButton{padding:7px;}"
        )


class ArchiveChats(QWidget):
    chat_uid = Signal(str)
    del_uid = Signal(str)

    def __init__(self):
        super().__init__()
        self.addComponents()

    def addComponents(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5, 2, 5, 2)
        self.layout().setSpacing(1)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop
                                   | Qt.AlignmentFlag.AlignHCenter)

        self.chats = []

    @Slot(str)
    def delete_chat(self, chat_uid: str):
        for chat in self.chats:
            if chat.uid == chat_uid:
                self.chats.remove(chat)
                self.layout().removeWidget(chat)
                self.del_uid.emit(chat_uid)
                chat.deleteLater()
                break

    @Slot(list)
    def load_chats(self, chats: List[Dict[str, str]]):
        # self.setStyleSheet("background-color: #f5f5f5;")
        for chat in chats:
            q_label = SingleChat(chat["name"], chat["uuid"])
            q_label.del_chat.connect(self.delete_chat)
            q_label.chat_uid.connect(self.send_chat_uid)
            self.chats.append(q_label)
            self.layout().addWidget(q_label)

    @Slot(str)
    def send_chat_uid(self, chat_uid):
        self.chat_uid.emit(chat_uid)

    @Slot(str, str)
    def add_new_chat(self, prompt: str, chat_uid: str) -> None:
        q_label = SingleChat(prompt, chat_uid)
        q_label.del_chat.connect(self.delete_chat)
        q_label.chat_uid.connect(self.send_chat_uid)
        self.chats.append(q_label)
        self.layout().insertWidget(0, q_label)  # type: ignore
        # self.layout().addWidget(q_label)  # type: ignore


class ClickLable(QLabel):

    clicked = Signal()

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def mousePressEvent(self, event):
        self.clicked.emit()


class SingleChat(QWidget):

    clicked = Signal()
    del_chat = Signal(str)

    chat_uid = Signal(str)

    def __init__(self, content: str, uid: str):
        super().__init__()
        self.uid = uid
        self.content = content
        self.setFixedSize(170, 37)
        self.addComponents()
        self.addStyle()
        self.addConnections()

        self.afterInit()

    def addComponents(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.content_label = ClickLable(self.content)
        self.layout().addWidget(self.content_label)

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(QPixmap(":/icons/edit.svg"))
        self.layout().addWidget(self.edit_btn)

        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QPixmap(":/icons/trash-2.svg"))
        self.layout().addWidget(self.delete_btn)

        self.content_label.clicked.connect(
            lambda: self.chat_uid.emit(self.uid))

    def addStyle(self):
        self.setStyleSheet("")

    def addConnections(self):
        pass

    def afterInit(self):
        self.edit_btn.clicked.connect(self.on_edit)
        self.delete_btn.clicked.connect(lambda: self.del_chat.emit(self.uid))
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)

    def on_edit(self):
        change_title = ChangeTitle(self.content)
        if change_title.exec() == QDialog.Accepted:
            self.content_label.setText(change_title.title_input.text())

    def enterEvent(self, event):
        self.edit_btn.setVisible(True)
        self.delete_btn.setVisible(True)

    def leaveEvent(self, event):
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)
