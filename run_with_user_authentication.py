from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, \
    QDesktopWidget
from RunUI_main_window import MainWindow
from user_sqlite import get_user
import sys
import numpy as np
import qdarktheme

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        # # Set the size of the window
        # self.setGeometry(0, 0, 400, 300)
        #
        # # Get the screen geometry
        # screen_geometry = QDesktopWidget().availableGeometry()
        #
        # # Calculate the position of the window
        # x = np.round((screen_geometry.width() - self.width()) / 2)
        # y = np.round((screen_geometry.height() - self.height()) / 2)
        #
        # # Move the window to the calculated position
        # self.move(x, y)

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
            QMessageBox.about(self, "Error", "Incorrect username or password")


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        app.exec()
        sys.exit(app.exec_()) #edithere
    else:
        sys.exit(app.exec_())
    sys.exit(app.exec_())
