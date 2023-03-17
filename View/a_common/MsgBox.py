from PyQt5.QtWidgets import QMessageBox


def msg_box(message, title='Lỗi'):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(str(message))
    msg.exec_()
