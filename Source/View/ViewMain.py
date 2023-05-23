import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from Source.View.MainView import MainWindow


def handle_exception(exc_type, exc_value, exc_traceback):
    print(f"{exc_type} || {exc_value} || {exc_traceback}")


sys.excepthook = handle_exception

if __name__ == '__main__':
    app = QApplication(sys.argv)
    extra = {
        # Font
        'font_family': 'Consolas',
        'font_size': 20
    }

    apply_stylesheet(app, theme='dark_yellow.xml', invert_secondary=True, extra=extra)
    mainWindow = MainWindow()
    mainWindow.show()
    error = app.exec()
    sys.exit(0)
