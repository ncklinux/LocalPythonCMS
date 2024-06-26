from PyQt6.QtWidgets import QDialog, QLabel


class PopUp(QDialog):
    def __init__(self, title: str, text: str):
        super().__init__()
        self.title = title
        self.text = text

        self.setWindowTitle(self.title)
        self.label = QLabel(self.text, self)
        self.label.move(125, 50)
