import sqlite3
import shutil
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
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
    if not os.path.exists(patient_file_path):
        os.makedirs(patient_file_path, exist_ok=True)
    # If entry already exists return error
    cursor.execute('''
                    SELECT COUNT(*) FROM patients
                    WHERE number = ?
                ''', (number,))
    count = cursor.fetchone()[0]

    if count == 1:
        popup_val = check_overwrite(cursor, conn)
        if popup_val == 0:
            return

    # make paths for files (now that we know they don't already exist)
    new_m_file_path = os.path.join(patient_file_path, f'{number}.m')

    # Move .m file to app location
    shutil.copyfile(m_file_path, new_m_file_path)

    # Insert new entry into the table
    cursor.execute('''
        INSERT INTO patients (name, number, date)
        VALUES (?,?,?)
    ''', (f_patient.encrypt(bytes(name, 'utf-8')), number, f_patient.encrypt(bytes(date, 'utf-8'))))

    # Commit changes to the database
    conn.commit()
    error_popup("Patient file created.")

    # Close cursor and connection
    cursor.close()
    conn.close()


def get_patient(ser_name, num):
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

    # Retrieve name and date for specified patient
    cursor.execute('''
        SELECT name, date FROM patients
        WHERE number = ?
    ''', (num,))

    # Fetch tuple (there should only be one)
    name_e, date_e = cursor.fetchone()
    name = f_patient.decrypt(name_e)
    date = f_patient.decrypt(date_e)

    if ser_name != name.decode('utf-8'):
        error_popup("This patient does not exist.")
        cursor.close()
        conn.close()
        return

    # Close cursor and connection
    cursor.close()
    conn.close()

    return name.decode('utf-8'), num, date.decode('utf-8')

def error_popup(text):
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(os.path.join(config.application_path, "Logo.png")))
    msg_box.setWindowTitle("CardioView")
    msg_box.setText(text)
    msg_box.exec_()

def check_overwrite(cursor, conn):
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(os.path.join(config.application_path, "Logo.png")))
    msg_box.setWindowTitle("CardioView")
    msg_box.setText("Data for this patient number already exists in the database. \n\nWould you like to overwrite it?")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.Cancel)
    response = msg_box.exec_()
    if response == QMessageBox.Yes:
        # Code to execute if the user clicked "Ok"
        return 1
    else:
        # Code to execute if the user clicked "Cancel" or closed the window
        cursor.close()
        conn.close()
        return 0