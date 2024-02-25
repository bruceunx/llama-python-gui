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
