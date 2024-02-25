from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QTextEdit, QWidget, QVBoxLayout, QLabel

INTRODUCTION = """
1. 本软件是一个基于Qt的聊天软件
2. 本软件支持用户离线AI聊天功能
3. 本软件支持小内存笔记本使用
"""

Style = """
QLabel {
    font-size: 20pt;
}
QTextEdit {
    border: none;
}
"""


class Introduction(QWidget):

    def __init__(self):
        super().__init__()

        content = QFrame()
        content.setLayout(QVBoxLayout())
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(content, 0, Qt.AlignmentFlag.AlignCenter)

        content.layout().addWidget(
            QLabel("LLama-chat"), 0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        introduction = QTextEdit()
        content.layout().addWidget(
            introduction, 1,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        introduction.setMarkdown(INTRODUCTION)
        introduction.setReadOnly(True)
        introduction.setFixedSize(400, 200)

        self.setStyleSheet(Style)

        content.layout().setSpacing(10)
