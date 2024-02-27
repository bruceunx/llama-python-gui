import uuid

from PySide6.QtCore import QMetaObject, QSize, QThread, Signal, Slot
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QPushButton, QScrollArea, QTextEdit, QWidget, QVBoxLayout, QLabel

from llama_python_gui.views.components import ArchiveChats

from llama_python_gui.views.components.contentview import ChatContainer, Introduction
from llama_python_gui.workers import LlamaWorker  # noqa

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
#prompt_frame QTextEdit{
    padding: 10px;
    font-size: 16pt;
    border: 1px solid #424242;
    border-radius: 10px;
}
#prompt_frame QPushButton{
    padding: 5px;
}
"""


class MainView(QWidget):

    chat_uid = Signal(str)
    del_uid = Signal(str)

    chat_info = Signal(str, str)
    start_singnal = Signal()
    init_signal = Signal()

    def __init__(self):
        super().__init__()
        self.resize(1200, 700)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowTitle("Llama-chat")
        self.addComponents()
        self.addStyle()
        self.addWorkers()
        self.addConnections()
        self.afterInit()

        self.current_chat_id = ""
        self.start_chat = True

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

        # set right frame layout
        right_frame.setLayout(QVBoxLayout())
        self.chat_content = QScrollArea()
        prompt_frame = QFrame()
        prompt_frame.setLayout(QHBoxLayout())
        self.prompt_input = QTextEdit()
        prompt_frame.layout().addWidget(self.prompt_input)
        self.chat_button = QPushButton()
        self.chat_button.setIcon(QPixmap(":/icons/send.svg"))
        self.chat_button.setIconSize(QSize(30, 30))
        self.chat_button.setObjectName("send_chat")
        prompt_frame.layout().addWidget(self.chat_button)
        right_frame.layout().addWidget(self.chat_content)
        right_frame.layout().addWidget(prompt_frame, 0,
                                       Qt.AlignmentFlag.AlignBottom)
        right_frame.layout().setContentsMargins(0, 0, 0, 0)
        right_frame.layout().setSpacing(1)

        prompt_frame.layout().setContentsMargins(30, 10, 30, 10)
        prompt_frame.layout().setSpacing(5)
        prompt_frame.setObjectName("prompt_frame")
        prompt_frame.setFixedHeight(100)

        self.chat_content.setWidget(Introduction())
        self.chat_content.setWidgetResizable(True)
        self.chat_content.verticalScrollBar().rangeChanged.connect(
            self.scroll_down)

        QMetaObject.connectSlotsByName(self)

    def addStyle(self):
        self.setStyleSheet(MainStyle)

    def addWorkers(self):
        self.worker = LlamaWorker()
        self.thread_worker = QThread()
        self.worker.moveToThread(self.thread_worker)

    def addConnections(self):
        self.achive_chats.chat_uid.connect(self.reload_chat)
        self.achive_chats.del_uid.connect(self.delete_chat)
        self.worker.chats.connect(self.achive_chats.load_chats)
        self.del_uid.connect(self.worker.delete_chat)
        self.chat_info.connect(self.achive_chats.add_new_chat)
        self.chat_info.connect(self.worker.start_new_chat)
        self.start_singnal.connect(self.worker.handle_reset)
        self.init_signal.connect(self.worker.get_all_chats)

    def afterInit(self):
        self.thread_worker.start()
        self.init_signal.emit()

    @Slot()
    def on_new_chat_clicked(self):
        self.chat_content.setWidget(Introduction())
        self.start_chat = True

    @Slot(int, int)
    def scroll_down(self, min: int, max: int):
        self.chat_content.verticalScrollBar().setValue(max)

    @Slot()
    def on_send_chat_clicked(self):
        if self.start_chat:
            self.chat_content.setWidget(ChatContainer())
        prompt = self.prompt_input.toPlainText().strip()
        if prompt == "":
            return

        if self.start_chat:
            chat_uid = str(uuid.uuid4())
            self.current_chat_id = chat_uid
            self.chat_info.emit(prompt, chat_uid)

        self.start_chat = False
        self.chat_content.widget().add_chat(prompt)
        self.prompt_input.clear()

    @Slot(str)
    def reload_chat(self, chat_uid: str):
        self.current_chat_id = chat_uid
        self.chat_uid.disconnect()
        self.chat_content.setWidget(ChatContainer())
        self.chat_uid.connect(self.chat_content.widget().reload_chat)
        self.chat_uid.emit(chat_uid)
        self.start_chat = False

    @Slot(str)
    def delete_chat(self, chat_uid: str):
        if chat_uid == self.current_chat_id:
            self.chat_content.setWidget(Introduction())
        self.del_uid.emit(chat_uid)

    def closeEvent(self, event):
        self.thread_worker.quit()
        self.thread_worker.wait()
        event.accept()
