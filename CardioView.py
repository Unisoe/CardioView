import os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5 import QtGui
import Config
from RunMainWindow import MainWindow
from UserSQLite import get_user
import sys
import qdarktheme
from StartCloseFunctions import on_close, on_startup

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardioView")
        self.setWindowIcon(QtGui.QIcon(os.path.join(Config.application_path, "Logo.png")))
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
        cancel_button.clicked.connect(self.closeEvent)
        stylesheet = "QWidget { font-size: 15px; }"
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
            self.password.clear()
            QMessageBox.about(self, "CardioView", "Incorrect username or password")

    def closeEvent(self, event):
        on_close() # remove gif files on close
        sys.exit(app.exec_())


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    on_startup()
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        app.exec()
        sys.exit(app.exec_())
    else:
        on_close()
        sys.exit(app.exec_())
