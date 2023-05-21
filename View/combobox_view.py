from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QLabel, QButtonGroup, QRadioButton

from Common.common import probability_list
from View.a_common.HWidget import HWidget
from View.a_common.TextBox.FloatTextBox import FloatTextBox
from View.a_common.VWidget import VWidget


class ComboboxView(QWidget):
    def __init__(self, parent=None):
        super(ComboboxView, self).__init__(parent)
        self.probability_box = QComboBox()
        m_text = QLabel('Phân bố')
        for probability in probability_list:
            self.probability_box.addItem(probability)
        self.button_group = QButtonGroup()

        self.long_radio = QRadioButton("LONG")
        self.long_radio.setChecked(True)
        self.button_group.addButton(self.long_radio)
        self.short_radio = QRadioButton("SHORT")
        self.button_group.addButton(self.short_radio)

        self.m = HWidget(m_text, self.probability_box)
        self.margin_input = FloatTextBox('Margin', '')
        self.create_layout()

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.m)
        layout.addWidget(HWidget(self.long_radio, self.short_radio))
        layout.addWidget(VWidget(self.margin_input))
        self.setLayout(layout)
