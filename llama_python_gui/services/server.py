from typing import Dict, List
import pickle

from llama_python_gui._config import base_path


class ChatServer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ChatServer,
                                  cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.chat_base = base_path / "data"

    def get_chats(self) -> List[Dict[str, str]]:
        chats = []
        for chat in self.chat_base.iterdir():
            with open(chat, "rb") as f:
                data = pickle.load(f)
                chats.append({"uuid": chat, "name": data["name"]})
        return chats
