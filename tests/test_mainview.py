from PySide6.QtWidgets import QApplication

from llama_python_gui.views.mainview import MainView

if __name__ == "__main__":
    import sys
    app = QApplication([])
    window = MainView()
    window.show()
    sys.exit(app.exec())
