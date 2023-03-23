from PyQt5.QtWidgets import QWidget, QHBoxLayout

from View.a_common.Button.Button import Button


class ControlView(QWidget):
    def __init__(self, parent=None):
        super(ControlView, self).__init__(parent)
        self.long_button = Button(" LONG ", '#00FF00')
        self.short_button = Button(" SHORT ", '#FF0000')
        self.create_layout()

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.long_button)
        layout.addWidget(self.short_button)
        self.setLayout(layout)
