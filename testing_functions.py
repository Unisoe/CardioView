import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt


class LoadingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Loading Window")
        # self.setFixedSize(700, 700)

        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap("Logo.png")
        label.setPixmap(pixmap)

        # movie = QMovie("loading-gif.gif")
        # label.setMovie(movie)
        #
        # movie.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_window = LoadingWindow()
    loading_window.show()
    sys.exit(app.exec_())