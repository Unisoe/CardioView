import os
import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import Config
import RunProcessing


class ProcessingThread(threading.Thread):
    def __init__(self, m_file, gif_file, thresh, pat_num):
        threading.Thread.__init__(self)
        self.m_file = m_file
        self.gif_file = gif_file
        self.thresh = thresh
        self.pat_num = pat_num
        self.result = None

    def run(self):
        print("the thread has run")
        self.result = "hello this does in fact work"
        print("self.result exists")
        return
        # self.result = RunProcessing.run_processing(self.m_file, self.gif_file, self.thresh, self.pat_num)

    def get_result(self):
        return self.result


class MsgBoxThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.msg_box = None

    def run(self):
        self.msg_box = QMessageBox()
        self.msg_box.setWindowIcon(QIcon(os.path.join(Config.application_path, "Logo.png")))
        self.msg_box.setWindowTitle("CardioView")
        self.msg_box.setText("Please wait. Patient data is being processed.")
        self.msg_box.setStandardButtons(QMessageBox.NoButton)
        self.msg_box.exec_()
        a=1
        
    def closemsg(self):
        self.msg_box.close()