from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from user_sqlite import new_user

class NewUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New User")
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
        stylesheet = "QWidget { font-size: 30px; }"
        self.setStyleSheet(stylesheet)

    def new_authentication(self):
        username = self.username.text()
        password = self.password.text()
        re_password = self.re_password.text()
        accepted = new_user(username, password, re_password)

        # Check database
        if accepted == 0:
            QMessageBox.about(self, "Error", "Username already exists")
        elif accepted == 1:
            QMessageBox.about(self, "Error", "Passwords do not match")
        elif accepted == 2:
            self.accept()
        else:
            # display error message
            QMessageBox.about(self, "Error", "Unknown Error")
