from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel
from RunUI_main_window import MainWindow
from user_sqlite import get_user
import sys


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login", self)
        cancel_button = QPushButton("Cancel", self)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        layout.addWidget(cancel_button)
        login_button.clicked.connect(self.login)
        cancel_button.clicked.connect(self.reject)
        stylesheet = "QWidget { font-size: 30px; }"
        self.setStyleSheet(stylesheet)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        accepted = get_user(username, password)
        # check if username and password are correct
        if accepted == 1:
            self.accept()
        else:
            # display error message
            error_label = QLabel("Incorrect username or password", self)
            layout = self.layout()
            layout.addWidget(error_label)
            self.resize(self.sizeHint())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        app.exec()
        sys.exit(app.exec_()) #edithere
    sys.exit(app.exec_())
