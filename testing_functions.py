# from PyQt5.QtCore import QSize
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#
#         self.setMinimumSize(QSize(300, 200))
#         self.setWindowTitle("PyQt messagebox example - pythonprogramminglanguage.com")
#
#         pybutton = QPushButton('Show messagebox', self)
#         pybutton.clicked.connect(self.clickMethod)
#         pybutton.resize(200,64)
#         pybutton.move(50, 50)
#
#     def clickMethod(self):
#         ret = QMessageBox.question(self, 'MessageBox', "Click a button",
#                                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
#
#         if ret == QMessageBox.Yes:
#             print('Button QMessageBox.Yes clicked.')
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     mainWin = MainWindow()
#     mainWin.show()
#     sys.exit( app.exec_() )

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt
import sys

from patient_data_sqlite import get_gif_path, get_m_file

app = QApplication(sys.argv)
window = QWidget()

m_file, gif_file, pat_name, pat_num, date = get_m_file('a',1)

gif_label = QLabel(window)
gif = QMovie(gif_file)
gif_label.setMovie(gif)
gif_size = QPixmap(gif_file).size()
gif_label.resize(gif_size)
gif.start()

window.setWindowTitle("Display GIF")
window.show()

sys.exit(app.exec_())

