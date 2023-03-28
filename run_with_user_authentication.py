from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from RunUI_main_window import MainWindow
from user_sqlite import get_user
import sys
import qdarktheme
from start_close import on_close, on_startup

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
    # print(f'Application path {config.application_path}')
    '''
        TODO:
        1. Move creating databases for patient database and user database here (pre-startup)
        2. Add a user with admin/admin username/pass if it doesn't exist here (pre-startup)
        3. Remove base path
        4. Replace database_path to use config.application_path as the root folder
           (i.e. database_path = path.join(config.application_path, patient_data.db).
           Should probably also make it patient_database_path.
        5. Do similar for user database (make a user_database_path variable).
    '''
    qdarktheme.setup_theme("auto")
    on_startup()
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        app.exec()
        on_close() # remove gif files on close
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec_())
    sys.exit(app.exec_())
