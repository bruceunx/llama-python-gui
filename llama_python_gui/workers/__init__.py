from typing import List
import os
import pickle

from PySide6.QtCore import QObject, Slot, Signal

from llama_cpp import Llama
from llama_cpp.llama_types import ChatCompletionRequestMessage

from llama_python_gui._config import MODEL_PATH, base_path
from llama_python_gui._utils import check_gpu_availability


class LlamaWorker(QObject):

    chats = Signal(list)
    stream_msg = Signal(str)

    def __init__(self, model: str = "normal"):
        super().__init__()
        self.messages: List[ChatCompletionRequestMessage] = []

        if model not in MODEL_PATH:
            raise ValueError(f"Model {model} not found")

        if check_gpu_availability():
            self.n_gpu_layers = 20
        else:
            self.n_gpu_layers = 0

        sysinfo = os.uname()
        if sysinfo.sysname == "Darwin" and sysinfo.machine == "arm64":
            self.n_gpu_layers = 32

        self.llm = Llama(model_path=MODEL_PATH[model],
                         n_gpu_layers=self.n_gpu_layers,
                         chat_format="chatml",
                         verbose=False)
        self.name: str | None = None
        self.chat_id: str | None = None

    @Slot(str)
    def switch_model(self, model: str):
        if model not in MODEL_PATH:
            raise ValueError(f"Model {model} not found")
        self.llm = Llama(model_path=MODEL_PATH[model],
                         n_gpu_layers=self.n_gpu_layers,
                         chat_format="chatml",
                         verbose=False)

    @Slot(str)
    def handle_chat(self, prompt: str) -> None:
        self.messages.append({"role": "user", "content": prompt})
        output = self.llm.create_chat_completion(
            messages=self.messages[-7:],
            response_format={
                "type": "json_object",
            },
            temperature=0.7,
            stream=True,
        )
        res = ""
        for reselt in output:
            content = reselt["choices"][0]["delta"]  # type: ignore
            if "content" in content:
                self.stream_msg.emit(content["content"])  # type: ignore
                res += content["content"]  # type: ignore
        self.messages.append({"role": "assistant", "content": res})
        # save chat at any step
        self.save_chat()

    @Slot(str, str)
    def start_new_chat(self, prompt: str, chat_uid: str) -> None:
        if len(self.messages) > 1:
            self.save_chat()
        self.messages = [{
            "role": "system",
            "content": "You are a helpful assistant"
        }]
        self.name = prompt
        self.chat_id = chat_uid
        self.save_chat()

    @Slot(str)
    def handle_reset(self) -> None:
        if len(self.messages) == 1:
            return
        self.save_chat()
        self.messages.clear()
        self.chat_id = None
        self.name = None

    @Slot(str)
    def reload_messages(self, chat_id: str) -> None:
        self.load_chat(chat_id)
        for message in self.messages[1:]:
            self.stream_msg.emit(message["content"])

    @Slot(str)
    def set_name(self, name: str):
        self.name = name

    def save_chat(self):
        with open(base_path / "data" / self.chat_id, "wb") as f:
            if self.name is None:
                for message in self.messages:
                    if message["role"] == "user":
                        self.name = message["content"][:50]
                        break
            pickle.dump({"name": self.name, "messages": self.messages}, f)

    @Slot()
    def get_all_chats(self):
        chats = []
        for chat in os.listdir(base_path / "data"):
            # sort chat by timestamp from newer to older
            with open(base_path / "data" / chat, "rb") as f:
                data = pickle.load(f)
                chats.append({"uuid": chat, "name": data["name"]})
        self.chats.emit(chats)

    def load_chat(self, chat_id: str):
        with open(base_path / "data" / chat_id, "rb") as f:
            data = pickle.load(f)
            self.name = data["name"]
            self.messages = data["messages"]
        return self.name, self.messages

    @Slot(str)
    def delete_chat(self, chat_id: str):
        os.remove(base_path / "data" / chat_id)
