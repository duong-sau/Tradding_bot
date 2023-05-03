from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from View.a_common.HWidget import HWidget
from View.a_common.TextBox.FloatTextBox import FloatTextBox


class AdvanceView(QWidget):
    def __init__(self, parent=None):
        super(AdvanceView, self).__init__(parent)
        self.stop_loss_textbox = FloatTextBox('Stop loss', 'giá')
        self.take_profit_textbox = FloatTextBox('Take profit', 'giá')
        self.is_stop_loss = QCheckBox("Đặt stop loss")
        self.is_stop_loss.setChecked(True)
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.is_stop_loss)
        layout.addWidget(HWidget(self.stop_loss_textbox))
        layout.addWidget(HWidget(self.take_profit_textbox))
        self.setLayout(layout)

    def check_stop_loss(self):
        if self.is_stop_loss.isChecked():
            self.stop_loss_textbox.setVisible(True)
        else:
            self.stop_loss_textbox.setVisible(False)

    def create_connection(self):
        self.is_stop_loss.clicked.connect(self.check_stop_loss)
