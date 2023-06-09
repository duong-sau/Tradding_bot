from PyQt5.QtWidgets import QWidget, QVBoxLayout


class VWidget(QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        for arg in args:
            self.layout.addWidget(arg)
        self.setLayout(self.layout)


