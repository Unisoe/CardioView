import os
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
import config
from user_sqlite import new_user
from PyQt5.QtGui import QPixmap, QIcon


class NewUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardioView")
        self.setWindowIcon(QIcon(os.path.join(config.application_path, "Logo.png")))
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.re_password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.re_password.setEchoMode(QLineEdit.Password)
        new_user_button = QPushButton("Create New User", self)
        cancel_button = QPushButton("Cancel", self)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Retype password:"))
        layout.addWidget(self.re_password)
        layout.addWidget(new_user_button)
        layout.addWidget(cancel_button)
        new_user_button.clicked.connect(self.new_authentication)
        cancel_button.clicked.connect(self.reject)
        stylesheet = "QWidget { font-size: 15px; }"
        self.setStyleSheet(stylesheet)

    def new_authentication(self):
        if self.username.text() == '' or self.password.text() == '' or self.re_password.text() == '':
            QMessageBox.about(self, "CardioView", "Please fill out all required fields")
            return
        username = self.username.text()
        password = self.password.text()
        re_password = self.re_password.text()
        accepted = new_user(username, password, re_password)
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(os.path.join(config.application_path, "Logo.png")))
        msg_box.setWindowTitle("CardioView")

        # Check database
        if accepted == 0:
            msg_box.setText("Error: Username already exists")
            msg_box.show()
        elif accepted == 1:
            msg_box.setText("Error: Passwords do not match")
            msg_box.show()
        elif accepted == 2:
            msg_box.setText("New User Created")
            msg_box.show()
            self.accept()
        else:
            msg_box.setText("Error: Unknown Error Occurred")


class ProcessingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CardioView")
        self.setWindowIcon(QIcon(os.path.join(config.application_path, "Logo.png")))
        # self.setFixedSize(300, 100)
        layout = QVBoxLayout(self)
        # layout.addWidget(QLabel(os.path.join(config.application_path, "loading-gif.gif")))
        layout.addWidget(QLabel("Please wait, patient data is being processed."))

        stylesheet = "QWidget { font-size: 15px; }"
        self.setStyleSheet(stylesheet)

    def close_dialog(self):
        self.accept()