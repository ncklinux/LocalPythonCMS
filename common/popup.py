from PyQt6.QtWidgets import QApplication, QDialog, QLabel


class PopUp(QDialog):
    def __init__(self, title: str, text: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.text = text

        self.setWindowTitle(self.title)
        self.label = QLabel(self.text, self)
        self.label.move(125, 50)

        self.center_dialog()

    def center_dialog(self):
        parent_widget = self.parentWidget()
        if parent_widget is not None:
            parent_geometry = parent_widget.frameGeometry()
            dialog_geometry = self.frameGeometry()
            center_point = parent_geometry.center()
        else:
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            dialog_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
        dialog_geometry.moveCenter(center_point)
        self.move(dialog_geometry.topLeft())
