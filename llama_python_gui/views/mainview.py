from PySide6.QtCore import QMetaObject, Slot
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QPushButton, QScrollArea, QWidget, QVBoxLayout, QLabel

from llama_python_gui.views.components import ArchiveChats

from llama_python_gui.assets import resource  # noqa

MainStyle = """
*{
    background-color: #212121;
    color:#fff;
    font-size: 12pt;
}
#left_frame *{
    background-color: #303030;
}
#top_frame QLabel{
    font-size: 26pt;
}
#top_frame QComboBox{
    padding: 10px;
    border: 1px solid #424242;
    font-size: 16pt;
}
#new_chat_frame *{
    font-size: 16pt;
    background-color: transparent;
}
#new_chat{
    background-color: #424242;
    padding: 5px;
    margin: 10 0 10 0;
}
#new_chat:hover{
    background-color: #303030;
}
#right_frame{
    background-color: #2c2c2c;
    color:#fff;
}
"""


class MainView(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1200, 700)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowTitle("Llama-chat")
        self.addComponents()
        self.addStyle()
        self.addWorkers()
        self.afterInit()

    def addComponents(self):
        self.setLayout(QVBoxLayout())
        top_frame = QFrame()
        top_frame.setFixedHeight(70)
        top_frame.setObjectName("top_frame")

        content_frame = QFrame()
        content_frame.setObjectName("content_frame")

        footer_frame = QFrame()
        footer_frame.setFixedHeight(30)
        footer_frame.setObjectName("footer_frame")

        self.layout().addWidget(top_frame)
        self.layout().addWidget(content_frame)
        self.layout().addWidget(footer_frame)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(1)

        top_frame.setLayout(QHBoxLayout())
        top_frame.layout().addWidget(
            QLabel("Llama-chat"), 0,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        top_model = QFrame()
        top_frame.layout().addWidget(top_model, 0,
                                     Qt.AlignmentFlag.AlignCenter)
        top_model.setLayout(QHBoxLayout())
        model_switch = QComboBox()
        model_switch.setFixedWidth(200)
        model_switch.setObjectName("model_switch")
        model_switch.addItems(["通用模型4-6G", "小模型<1G"])

        model_label = QLabel()
        model_label.setObjectName("model_label")
        model_label.setPixmap(QPixmap(":/icons/server.svg"))

        top_model.layout().addWidget(model_label)
        top_model.layout().addWidget(model_switch)

        top_frame.layout().addWidget(QLabel(""))
        top_frame.layout().setContentsMargins(10, 0, 10, 0)
        content_frame.setLayout(QHBoxLayout())
        left_frame = QFrame()
        left_frame.setFixedWidth(200)
        left_frame.setObjectName("left_frame")

        right_frame = QFrame()
        right_frame.setObjectName("right_frame")
        content_frame.layout().addWidget(left_frame)
        content_frame.layout().addWidget(right_frame)

        content_frame.layout().setContentsMargins(0, 0, 0, 0)
        content_frame.layout().setSpacing(1)

        left_frame.setLayout(QVBoxLayout())
        left_frame.layout().setContentsMargins(0, 0, 0, 0)
        left_frame.layout().setSpacing(1)

        new_chat_frame = QFrame()
        new_chat_frame.setObjectName("new_chat_frame")

        left_frame.layout().addWidget(new_chat_frame)
        new_chat_frame.setLayout(QHBoxLayout())
        new_chat_frame.layout().setContentsMargins(0, 0, 0, 0)
        new_chat_frame.setFixedHeight(50)

        new_chat_frame.layout().addWidget(QLabel("聊天"))

        new_chat = QPushButton("+ 新建聊天")
        new_chat.setObjectName("new_chat")

        new_chat.setIcon(QPixmap(":/icons/layers.svg"))

        new_chat_frame.layout().addWidget(new_chat, 0,
                                          Qt.AlignmentFlag.AlignRight)

        new_chat_frame.layout().setContentsMargins(10, 0, 0, 0)

        topic_group = QScrollArea()
        topic_group.setLayout(QVBoxLayout())
        left_frame.layout().addWidget(topic_group)

        self.achive_chats = ArchiveChats()

        topic_group.setWidget(self.achive_chats)

        QMetaObject.connectSlotsByName(self)

    def addStyle(self):
        self.setStyleSheet(MainStyle)

    def addWorkers(self):
        pass

    def afterInit(self):
        pass

    @Slot()
    def on_new_chat_clicked(self):
        print("new chat")
