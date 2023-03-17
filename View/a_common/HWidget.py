from PyQt5.QtWidgets import QHBoxLayout, QWidget


class HWidget(QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        self.layout = QHBoxLayout()
        for arg in args:
            self.layout.addWidget(arg)
        self.setLayout(self.layout)
