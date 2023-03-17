from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QLabel

from View.a_common.HWidget import HWidget
from View.a_common.TextBox.FloatTextBox import FloatTextBox
from common import probability_list_m, probability_list_n


class ComboboxView(QWidget):
    def __init__(self, parent=None):
        super(ComboboxView, self).__init__(parent)
        self.m_combobox = QComboBox()
        m_text = QLabel('Phân bố M')
        for probability in probability_list_m:
            self.m_combobox.addItem(probability)
        self.n_combobox = QComboBox()
        n_text = QLabel('Phân bố N')
        for probability in probability_list_n:
            self.n_combobox.addItem(probability)

        self.m = HWidget(m_text, self.m_combobox)
        self.n = HWidget(n_text, self.n_combobox)
        self.margin_input = FloatTextBox('Margin', '')
        self.create_layout()

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.m)
        layout.addWidget(self.n)
        layout.addWidget(self.margin_input)
        self.setLayout(layout)
