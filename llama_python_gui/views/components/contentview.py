from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QTextEdit, QWidget, QVBoxLayout, QLabel

import markdown

from llama_python_gui._config import code_style

INTRODUCTION = """
1. 本软件是一个基于Qt的聊天软件
2. 本软件支持用户离线AI聊天功能
3. 本软件支持小内存笔记本使用
```python
import os
os.system("echo hello")
def hello():
    return "world"
```

```ts
let a = "hello world"
console.log(a)
```
| Item         | Price     | # In stock |
|--------------|-----------|------------|
| Juicy Apples | 1.99      | *7*        |
| Bananas      | **1.89**  | 5234       |
"""

# background-color: #272822;
Style = """
QLabel {
    font-size: 27pt;
    font-weight: bold;
}
QTextEdit {
    font-size: 18pt;
    border: none;
    background-color: #272822;
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
        html = code_style
        html += markdown.markdown(
            INTRODUCTION, extensions=["fenced_code", "codehilite", "tables"])
        introduction.setHtml(html)
        introduction.setReadOnly(True)
        introduction.setFixedSize(500, 200)

        self.setStyleSheet(Style)

        content.layout().setSpacing(10)


class ExpandingTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFixedHeight(30)
        self.vertical_scroll_bar = self.verticalScrollBar()
        self.vertical_scroll_bar.rangeChanged.connect(self.update_scrollbar)

    def update_scrollbar(self, min, max):
        w, h = self.width(), self.height()
        self.resize(w, h + max)

    def add_message(self, message: str) -> None:
        self.content += message
        self.refresh()

    def init_message(self, message: str) -> None:
        self.content = message
        self.refresh()

    def refresh(self) -> None:
        html = code_style
        html += markdown.markdown(
            self.content, extensions=["fenced_code", "codehilite", "tables"])
        self.setHtml(html)


class ChatContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(20, 5, 20, 5)
        self.layout().setSpacing(2)
        self.lastchat = None

        self.setStyleSheet(
            "*{border: none;} QTextEdit{font-size:17pt; border:none; background-color: #272822; color: #f8f8f2;}"
        )

    @Slot(str)
    def add_chat(self, message: str):
        chat = ExpandingTextEdit()
        chat.init_message(message)
        self.lastchat = chat
        self.layout().addWidget(chat, 0,
                                Qt.AlignmentFlag.AlignTop)  # type: ignore
        # self.layout().insertWidget(0, chat)  # type: ignore

    @Slot(str)
    def update_message(self, message: str):
        if self.lastchat is not None:
            self.lastchat.add_message(message)
