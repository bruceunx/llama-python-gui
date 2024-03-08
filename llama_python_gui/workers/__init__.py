from typing import List
import os
import pickle
import time

from PySide6.QtCore import QThread, Slot, Signal

from jinja2.sandbox import ImmutableSandboxedEnvironment
from llama_cpp import Llama
from llama_cpp.llama_types import ChatCompletionRequestMessage

from llama_python_gui._config import MODEL_PATH, base_path
from llama_python_gui._utils import check_gpu_availability

DEFAULT_TEMP = "{% for message in messages %}{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}"


class LlamaWorker(QThread):

    chats = Signal(list)
    stream_msg = Signal(str)
    chat_msg = Signal(str)
    prompt_end = Signal()

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
                         verbose=False,
                         n_ctx=2048)
        self.name: str | None = None
        self.chat_id: str | None = None

        self.stop_chat = False

        self.stop = False
        self.prompt: str | None = None

        if "tokenizer.chat_template" not in self.llm.metadata:
            chat_temp = DEFAULT_TEMP
        else:
            chat_temp = self.llm.metadata["tokenizer.chat_template"].strip()

        _env = ImmutableSandboxedEnvironment(trim_blocks=True,
                                             lstrip_blocks=True)
        self.temp_eng = _env.from_string(chat_temp)

    def run(self) -> None:
        while not self.stop:
            if self.prompt is not None:
                self.messages.append({"role": "user", "content": self.prompt})
                self.chat_msg.emit("问题 -> &nbsp;" + self.prompt)
                prompts = self.temp_eng.render(messages=self.messages[-3:],
                                               add_generation_prompt=True)
                output = self.llm.create_completion(
                    prompt=prompts,
                    temperature=0.7,
                    stream=True,
                    max_tokens=1024,
                )
                self.chat_msg.emit("AI -> ")
                res = ""
                for result in output:
                    if self.stop_chat:
                        break
                    content = result["choices"][0]['text']  # type: ignore
                    self.stream_msg.emit(content)  # type: ignore
                    res += content
                self.messages.append({"role": "assistant", "content": res})
                self.prompt_end.emit()
                # save chat at any step
                self.save_chat()

                self.prompt = None
            self.stop_chat = False
            time.sleep(0.5)

    @Slot(str)
    def switch_model(self, model: str):
        if model not in MODEL_PATH:
            raise ValueError(f"Model {model} not found")
        self.llm = Llama(model_path=MODEL_PATH[model],
                         n_gpu_layers=self.n_gpu_layers,
                         verbose=False)

        if "tokenizer.chat_template" not in self.llm.metadata:
            chat_temp = DEFAULT_TEMP
        else:
            chat_temp = self.llm.metadata["tokenizer.chat_template"].strip()
        _env = ImmutableSandboxedEnvironment(trim_blocks=True,
                                             lstrip_blocks=True)
        self.temp_eng = _env.from_string(chat_temp)

    @Slot(str)
    def handle_chat(self, prompt: str) -> None:
        self.prompt = prompt

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
        # self.messages.clear()
        self.load_chat(chat_id)
        for message in self.messages[1:]:
            if message["role"] == "assistant":
                self.chat_msg.emit("AI -> &nbsp;" +  # type: ignore
                                   message["content"])  # type: ignore
            else:
                self.chat_msg.emit("问题 -> &nbsp;" +  # type: ignore
                                   message["content"])  # type: ignore

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
            self.chat_id = chat_id

    @Slot(str)
    def delete_chat(self, chat_id: str):
        os.remove(base_path / "data" / chat_id)

    @Slot()
    def stop_handle(self):
        self.stop_chat = True

    def quit(self):
        self.stop = True
        super().quit()
