from PySide6.QtWidgets import QApplication
from login import LoginWindow

if __name__ == "__main__":
    app = QApplication([])

    window = LoginWindow()
    window.show()

    app.exec()
