from PySide6.QtCore import QObject, Slot


class LlamaServer(QObject):

    def __init__(self):
        super().__init__()

    @Slot(str)
    def send_message(self, message: str):
        pass

