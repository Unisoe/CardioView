import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("PyQt messagebox example - pythonprogramminglanguage.com")

        pybutton = QPushButton('Show messagebox', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,64)
        pybutton.move(50, 50)

    def clickMethod(self):
        ret = QMessageBox.question(self, 'MessageBox', "Click a button",
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            print('Button QMessageBox.Yes clicked.')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )