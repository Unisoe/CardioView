import glob
import os
import sqlite3
import config
from user_sqlite import new_user

def on_startup():

    # Connect to user database (or create it if it doesn't exist)
    user_database_path = os.path.join(config.application_path, 'user_database.db')
    conn_user = sqlite3.connect(user_database_path)

    # Create cursor to execute SQL commands
    cursor_user = conn_user.cursor()

    # Create table 'entries'
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
    patient_database_path = os.path.join(config.application_path, 'patient_database.db')
    conn_pat = sqlite3.connect(patient_database_path)

    # Create a cursor to execute SQL commands
    cursor_pat = conn_pat.cursor()

    # Create table 'entries'
    cursor_pat.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    m_file_path TEXT,
                    gif_path TEXT,
                    name TEXT,
                    number INTEGER PRIMARY KEY,
                    date TEXT
                )
            ''')

    cursor_pat.close()
    conn_pat.close()


def on_close():
    # Remove the .gif files created
    patient_file_path = os.path.join(config.application_path, 'patient_files')
    for gifpath in glob.iglob(os.path.join(patient_file_path, '*.gif')):
        os.remove(gifpath)