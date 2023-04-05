import sys
import threading
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow

import RunProcessing


class ProcessingThread(QObject, threading.Thread):
    finished = pyqtSignal(int)

    def __init__(self, m_file, gif_file, thresh, pat_num):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.m_file = m_file
        self.gif_file = gif_file
        self.thresh = thresh
        self.pat_num = pat_num

    def run(self):
        # create a message box and show it
        msgBox = QMessageBox()
        msgBox.setText("Function is running...")
        msgBox.exec_()

        # call processing func function and emit the result
        result = RunProcessing.run_processing(self.m_file, self.gif_file, self.thresh, self.pat_num)
        self.finished.emit(result)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.myresult = None
        self.initUI()

    def initUI(self):
        # create a button to start the worker thread
        btn = QPushButton("Run Function", self)
        btn.setGeometry(10, 10, 100, 30)
        btn.clicked.connect(self.run_worker_thread)
        self.run_worker_thread()

        # show the main window
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Main Window")
        self.show()

    def run_worker_thread(self):
        # create a new worker thread and connect to its finished signal
        thread = WorkerThread(1, 2, 3, 4)
        thread.finished.connect(self.update_result)

        # start the thread
        thread.start()

    def update_result(self, result):
        # update the myresult attribute and show the result to the user
        self.myresult = result
        resultBox = QMessageBox()
        resultBox.setText(f"The result is: {self.myresult}")
        resultBox.exec_()


if __name__ == "__main__":
    # create the application and run it
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
