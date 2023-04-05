import glob
import os
import sqlite3
import Config
from UserSQLite import new_user

def on_startup():

    # Connect to user database (or create it if it doesn't exist)
    user_database_path = os.path.join(Config.application_path, 'user_database.db')
    conn_user = sqlite3.connect(user_database_path)

    # Create cursor to execute SQL commands
    cursor_user = conn_user.cursor()

    # Create table 'user'
    cursor_user.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username BLOB PRIMARY KEY COLLATE BINARY,
                password BLOB COLLATE BINARY
            )
        ''')

    # Check if the database is empty
    cursor_user.execute('''
            SELECT COUNT(*) FROM users
                ''')

    count = cursor_user.fetchone()[0]

    if count == 0:
        new_user('admin', 'admin', 'admin')

    cursor_user.close()
    conn_user.close()

    # Connect to patient database (or create it if it doesn't exist)
    patient_database_path = os.path.join(Config.application_path, 'patient_database.db')
    conn_pat = sqlite3.connect(patient_database_path)

    # Create database path for .m, .gif, and .png files
    patient_file_path = os.path.join(Config.application_path, 'patient_files')
    if not os.path.exists(patient_file_path):
        os.makedirs(patient_file_path, exist_ok=True)

    # Create a cursor to execute SQL commands
    cursor_pat = conn_pat.cursor()

    # Create table 'patients'
    cursor_pat.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    name TEXT,
                    number INTEGER PRIMARY KEY,
                    date TEXT
                )
            ''')

    cursor_pat.close()
    conn_pat.close()


def on_close():
    # Remove the .gif files created
    path = os.listdir(Config.patient_file_path)
    for images in path:
        if images.endswith(".png") or images.endswith(".gif"):
            os.remove(os.path.join(Config.patient_file_path, images))