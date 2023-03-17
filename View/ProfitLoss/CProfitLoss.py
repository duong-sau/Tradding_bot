from PyQt6.QtWidgets import QHBoxLayout, QWidget

from View._Common.TextBox.FloatTextBox import FloatTextBox
from View._Common.TextBox.IntTextBox import IntTextBox


class CProfitLoss(QWidget):
    def __init__(self, parent=None):
        super(CProfitLoss, self).__init__(parent)
        self.future_textbox = None
        self.stop_loss_textbox = None
        self.profit_textbox = None

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.stop_loss_textbox = FloatTextBox('Stop loss', 'Nhập stop loss')
        self.profit_textbox = FloatTextBox('Take Profit', 'Nhập take profit')
        self.future_textbox = IntTextBox('X bao nhiêu', 'Nhập giá trị X bao nhiêu')

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.stop_loss_textbox)
        layout.addWidget(self.profit_textbox)
        layout.addWidget(self.future_textbox)
        self.setLayout(layout)

    def get_value(self):
        return self.stop_loss_textbox.get_value(), self.profit_textbox.get_value(), self.future_textbox.get_value()
