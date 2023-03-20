import sys
from PyQt5 import QtWidgets, QtGui
from GUI_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        stylesheet = "QWidget { font-size: 30px; }"
        self.setStyleSheet(stylesheet)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        sys.exit()
