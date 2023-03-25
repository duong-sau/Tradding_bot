import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QPushButton
from PyQt5.QtGui import QFont


class PNLView(QWidget):
    def __init__(self, test, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Window")

        # Tạo QPlainTextEdit để hiển thị console log
        layout = QVBoxLayout(self)
        self.log_console = QPlainTextEdit(self)
        self.log_console.setReadOnly(True)
        layout.addWidget(self.log_console)

        # Tạo nút "Clear Log" để xóa nội dung trong QPlainTextEdit
        self.clear_button = QPushButton("Test")
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(test)

        # Thiết lập font chữ và cỡ chữ cho QPlainTextEdit
        font = QFont("Consolas", 20)
        self.log_console.setFont(font)

        # Thiết lập màu sắc cho QPlainTextEdit
        stylesheet = """
            QPlainTextEdit {
                background-color: black;
                color: white;
                font-family: Consolas;
                font-size: 10pt;
            }
        """
        self.log_console.setStyleSheet(stylesheet)

        # Cấu hình logging để ghi log vào QPlainTextEdit
        # logging.basicConfig(level=logging.DEBUG, stream=self)
        # self.logger = logging.getLogger()
        # self.logger.addHandler(logging.StreamHandler(self))

    def write(self, message):
        # Ghi log vào QPlainTextEdit
        self.log_console.insertPlainText(message)

    def clear_log(self):
        # Xóa nội dung trong QPlainTextEdit
        self.log_console.clear()

    def set_text(self, long, short, rx, pnl, spnl, sl, tp1, tp2):
        self.clear_log()
        message = \
            f'''
Giá thanh lý           LONG     : {long}
                       SHORT    : {short}\
                       
Margin đề xuất         RX       : {rx}
                       PNL      : {pnl} 
                       SPNL     : {spnl}
----------------------------------------------------------\n'''
        message = message + f"""STOP LOSS     (%) : {sl}  \n"""
        message = message + f"""T___ P__1     (%) : {tp1} \n"""
        message = message + f"""T___ P__2     (%) : {tp2} \n"""
        self.write(message=message)

    def log_cant_cal(self):
        self.clear_log()
        self.write('Chưa thể tính toán')
