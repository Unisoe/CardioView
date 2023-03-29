import sqlite3
import shutil
import os
from PyQt5.QtWidgets import QMessageBox
import base64
import config
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
    patient_database_path = os.path.join(config.application_path, 'patient_database.db')
    conn = sqlite3.connect(patient_database_path)

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Create database path for .m, .gif, and .png files
    patient_file_path = os.path.join(config.application_path, 'patient_files')

    # If entry already exists return error
    cursor.execute('''
                    SELECT COUNT(*) FROM patients
                    WHERE number = ?
                ''', (number,))
    count = cursor.fetchone()[0]

    if not os.path.exists(patient_file_path):
        os.mkdir(patient_file_path)
    os.makedirs(patient_file_path, exist_ok=True)

    if count == 1:
        popup_val = check_overwrite(cursor, conn)
        if popup_val == 0:
            return

    # make paths for files (now that we know they don't already exist)
    new_m_file_path = os.path.join(patient_file_path, f'{number}.m')
    gif_path = os.path.join(patient_file_path, f'{number}.gif')

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
    error_popup("Patient file created.")

    # Close cursor and connection
    cursor.close()
    conn.close()


def get_m_file(ser_name, num):
    # Connect to database (or create it if it doesn't exist)
    patient_database_path = os.path.join(config.application_path, 'patient_database.db')
    conn = sqlite3.connect(patient_database_path)

    # Create cursor to execute SQL commands
    cursor = conn.cursor()

    # If entry does not exist return error
    cursor.execute('''
                        SELECT COUNT(*) FROM patients
                        WHERE number = ?
                    ''', (num,))
    count = cursor.fetchone()[0]

    if count == 0:
        error_popup("This patient does not exist.")
        cursor.close()
        conn.close()
        return

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

    if ser_name != name.decode('utf-8'):
        error_popup("This patient does not exist.")
        cursor.close()
        conn.close()
        return

    # Close cursor and connection
    cursor.close()
    conn.close()

    return m_file_path.decode('utf-8'), gif_path.decode('utf-8'), name.decode('utf-8'), num, date.decode('utf-8')

def get_gif_path(num):
    # Connect to database (or create it if it doesn't exist)
    patient_database_path = os.path.join(config.application_path, 'patient_database.db')
    conn = sqlite3.connect(patient_database_path)

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Retrieve m_file for specified patient
    cursor.execute('''
        SELECT gif_path FROM patients
        WHERE number = ?
    ''', (num,))

    # Fetch tuple (there should only be one)
    gif_path_e = cursor.fetchone()[0]
    gif_path = bytes.decode(f_patient.decrypt(gif_path_e), 'utf-8')

    # Close cursor and connection
    cursor.close()
    conn.close()

    return gif_path

def error_popup(text):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Attention") #maybe replace with our brand name edithere
    msg_box.setText(text)
    stylesheet = "QWidget { font-size: 15px; }"
    msg_box.setStyleSheet(stylesheet)
    msg_box.exec_()

def check_overwrite(cursor, conn):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowTitle("Existing Patient")
    msg_box.setText("Data for this patient number already exists in the database. \n\nWould you like to overwrite it?")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.Cancel)
    response = msg_box.exec_()
    if response == QMessageBox.Yes:
        # Code to execute if the user clicked "Ok"
        return 1
    else:
        # Code to execute if the user clicked "Cancel"
        cursor.close()
        conn.close()
        return 0