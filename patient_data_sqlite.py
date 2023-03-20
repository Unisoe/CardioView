import sqlite3
import shutil
import os
from PyQt5.QtWidgets import QMessageBox
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Use password for key
hardcode = b"ALMR9716"
salt = b'0\xe3K\xb0Bf?\xebc{\xa7\xf5\x15\t\xa8\x05'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key2 = base64.urlsafe_b64encode(kdf.derive(hardcode))

# Initialize a new Fernet object with the key
f_patient = Fernet(key2)

def new_entry(m_file_path, name, number, date):
    # Connect to database (or create it if it doesn't exist)
    conn = sqlite3.connect('patient_data.db')

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Get file name from file path
    dir_name, file_name = os.path.split(m_file_path)
    # app_paths = AppDataPaths() # edithere this will be used when the application is saved in process file
    # base_path = app_paths.app_data_path.replace('\\', '/')
    base_path = r'C:\Users\krist\OneDrive\Documents\School\8SEM-W2023\BME700 (Capstone)'
    database_path = os.path.join(base_path, f'patient_database')

    # Create table 'entries'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            m_file_path TEXT,
            gif_path TEXT,
            name TEXT,
            number INTEGER PRIMARY KEY,
            date TEXT
        )
    ''')

    # If entry already exists return error
    cursor.execute('''
                    SELECT COUNT(*) FROM patients
                    WHERE number = ?
                ''', (number,))
    count = cursor.fetchone()[0]

    if not os.path.exists(database_path):
        os.mkdir(database_path)
    os.makedirs(database_path, exist_ok=True)

    if count == 1:
        from GUI_main_window import Ui_MainWindow
        ret = QMessageBox.question(Ui_MainWindow, 'Error', "Patient already exists in the database",
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            cursor.close()
            conn.close()

    # make paths for files (now that we know they don't already exist)
    new_m_file_path = os.path.join(database_path, f'{number}.m')
    gif_path = os.path.join(database_path, f'{number}.gif')

    # Move .m file to app location
    shutil.copyfile(m_file_path, new_m_file_path)

    # Set the file permissions of the subdirectory to read and execute only for the owner


    # Insert new entry into the table
    cursor.execute('''
        INSERT INTO patients (m_file_path, gif_path, name, number, date)
        VALUES (?,?,?,?,?)
    ''', (f_patient.encrypt(bytes(m_file_path, 'utf-8')), f_patient.encrypt(bytes(gif_path, 'utf-8')),
          f_patient.encrypt(bytes(name, 'utf-8')), number, f_patient.encrypt(bytes(date, 'utf-8'))))

    # Commit changes to the database
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()


def get_m_file(ser_name, num):
    # Connect to database
    conn = sqlite3.connect('patient_data.db')

    # Create cursor to execute SQL commands
    cursor = conn.cursor()

    # If entry does not exist return error
    cursor.execute('''
                        SELECT COUNT(*) FROM patients
                        WHERE number = ?
                    ''', (num,))
    count = cursor.fetchone()[0]

    if count == 0: # edithere
        popup_nopat_window = NoPat()
        popup_nopat_window.show()
        cursor.close()
        conn.close()
        return 0

    # Retrieve m_file for specified patient
    cursor.execute('''
        SELECT name, m_file_path, gif_path, date FROM patients
        WHERE number = ?
    ''', (num,))

    # Fetch tuple (there should only be one)
    name_e, m_file_path_e, gif_path_e, date_e = cursor.fetchone()
    name = f_patient.decrypt(name_e)
    m_file_path = f_patient.decrypt(m_file_path_e)
    gif_path = f_patient.decrypt(gif_path_e)
    date = f_patient.decrypt(date_e)

    if bytes(ser_name, 'utf-8') != name: # edithere
        popup_nopat_window = NoPat()
        popup_nopat_window.show()
        cursor.close()
        conn.close()
        return 0

    # Close cursor and connection
    cursor.close()
    conn.close()

    return m_file_path, gif_path, name, num, date

def get_gif_path(num):
    # Connect to database
    conn = sqlite3.connect('patient_data.db')

    # Create cursor to execute SQL commands
    cursor = conn.cursor()

    # Retrieve m_file for specified patient
    cursor.execute('''
        SELECT gif_path FROM patients
        WHERE number = ?
    ''', (num,))

    # Fetch tuple (there should only be one)
    gif_path_e = cursor.fetchone()[0]
    gif_path = f_patient.decrypt(gif_path_e)

    # Close cursor and connection
    cursor.close()
    conn.close()

    return gif_path
