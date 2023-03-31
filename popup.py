from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from user_sqlite import new_user

class NewUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardioView")
        self.setIcon("Logo.png")
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
        username = self.username.text()
        password = self.password.text()
        re_password = self.re_password.text()
        accepted = new_user(username, password, re_password)
        msg_box = QMessageBox()
        msg_box.setIcon("Logo.png")
        msg_box.setWindowTitle("CardioView")

        # Check database
        if accepted == 0:
            msg_box.setText("Error: Username already exists")
        elif accepted == 1:
            msg_box.setText("Error: Username already exists")
        elif accepted == 2:
            msg_box.setText("New User Created")
            self.accept()
        else:
            msg_box.setText("Error: Unknown Error Occurred")
