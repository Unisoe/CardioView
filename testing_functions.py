from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # create a QMovie object from your GIF file
        self.movie = QMovie("C:/Users/krist/PycharmProjects/capscone_sigprocessing_v1/patient_files/123456789.gif")

        # create a QLabel to display the movie frames
        self.label = QLabel(self)

        # create a vertical layout and add the label to it
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        # connect the QMovie's frameChanged() signal to a slot that updates the label
        self.movie.frameChanged.connect(self.update_label)

        # start the movie playing
        self.movie.start()

        # set a boolean flag to keep track of whether the window is being resized by the user or not
        self.resizing = False

    def resizeEvent(self, event):
        if self.resizing:
            # if the window is being resized by the user, update the size of the label and set the resizing flag to False
            size = self.size()
            self.label.setFixedSize(size.width(), size.height())
            self.resizing = False
        else:
            # if the window is being resized programmatically, set the resizing flag to True and do not update the label
            self.resizing = True

    def update_label(self):
        # get the current pixmap from the movie
        pixmap = self.movie.currentPixmap()

        # create a QTransform to scale the pixmap to the size of the label
        size = self.label.size()
        transform = QTransform().scale(size.width() / pixmap.width(), size.height() / pixmap.height())
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

        # set the pixmap on the label
        self.label.setPixmap(pixmap)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


