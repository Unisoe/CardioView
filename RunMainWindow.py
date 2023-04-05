import sys
from PyQt5 import QtWidgets, QtGui
from GUI_main_window import UiMainWindow
from StartCloseFunctions import on_close


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        stylesheet = "QWidget { font-size: 15px; }"
        self.setStyleSheet(stylesheet)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        on_close()
        sys.exit()
