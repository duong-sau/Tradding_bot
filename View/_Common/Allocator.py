from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from View._Common.Label.Label import AllocatorLabel
from View._Common.TextBox.AllocatorTextBox import AllocatorTextBox
from common import probability_list, auto_complete


class Allocator(QWidget):
    def __init__(self, title, placeholder, parent=None):
        super(Allocator, self).__init__(parent)

        # Create widgets
        self.allocation_select_list = QComboBox()
        for probability in probability_list:
            self.allocation_select_list.addItem(probability)

        self.allocation_textbox = AllocatorTextBox(title, placeholder)
        self.allocation_hint_label = AllocatorLabel('Tạm tính')

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.allocation_select_list)
        layout.addWidget(self.allocation_textbox)
        layout.addWidget(self.allocation_hint_label)
        self.setLayout(layout)

    def get_selected(self):
        current_text = self.allocation_select_list.currentText()
        return current_text

    def get_value(self):
        return self.allocation_hint_label.get_value()

    def update_hint_text(self, min_max_counter):
        min_val, max_val, counter = min_max_counter

        # counter
        if counter == 0:
            self.allocation_hint_label.set_value([])
            return

        # Get the current value of the allocation textbox
        allocation_input = self.allocation_textbox.get_value()
        # Get the current selected allocation
        math_type = self.allocation_select_list.currentText()
        # Call the appropriate allocation method to get the allocation result
        allocation_result = auto_complete(math_type, allocation_input, min_val, max_val, counter)

        # Update the hint label text
        self.allocation_hint_label.set_value(allocation_result)
