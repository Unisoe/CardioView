import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
import Config
from PyQt5.QtGui import QIcon

class WaitDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardioView")
        self.setWindowIcon(QIcon(os.path.join(Config.application_path, "Logo.png")))
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Please wait, patient send_to_mc is being processed."))
        stylesheet = "QWidget { font-size: 15px; }"
        self.setStyleSheet(stylesheet)
