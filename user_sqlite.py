import sqlite3
import base64
import os
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Use password for key
hardcode = b"AZBF6223"
salt = b'\xee\xd8\xf3V\xc6!\xee\xf5\x9cF\x11"L\xaa\xed\xa5'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key1 = base64.urlsafe_b64encode(kdf.derive(hardcode))

# Initialize a new Fernet object with the key
f_user = Fernet(key1)

def new_user(username, password, re_password):
    # Convert to byte type
    byte_username = bytes(username, 'utf-8')

    # Connect to database (or create it if it doesn't exist)
    conn = sqlite3.connect('user_database.db')

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Create table 'entries'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username BLOB PRIMARY KEY COLLATE BINARY,
            password BLOB COLLATE BINARY
        )
    ''')

    # Check if the specified username exists in the database
    cursor.execute('''
        SELECT COUNT(*) FROM users
        WHERE username = ?
            ''', (byte_username,))

    count = cursor.fetchone()[0]

    if count == 1:
        # Close cursor and connection
        cursor.close()
        conn.close()
        return 0

    # Check if passwords match
    if password != re_password:
        cursor.close()
        conn.close()
        return 1

    # Convert password to byte type
    byte_password = bytes(password, 'utf-8')

    # Insert new entry into the table
    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?,?)
    ''', (byte_username, f_user.encrypt(byte_password)))

    # Commit changes to the database
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()
    return 2


def get_user(username, user_password):
    # Convert to byte type
    byte_username = bytes(username, 'utf-8')
    byte_password = bytes(user_password, 'utf-8')

    # Connect to database
    conn = sqlite3.connect('user_database.db')

    # Create cursor to execute SQL commands
    cursor = conn.cursor()

    # Check if the specified username exists in the database
    cursor.execute('''
            SELECT COUNT(*) FROM users
            WHERE username = ?
        ''', (byte_username,))
    count = cursor.fetchone()[0]

    if count == 0:
        # Close cursor and connection
        cursor.close()
        conn.close()
        return 0

    # Retrieve password for specified patient
    cursor.execute('''
        SELECT password FROM users
        WHERE username = ?
    ''', (byte_username,))

    # Fetch password as a string
    password = cursor.fetchone()[0]
    decrypted_password = f_user.decrypt(password)

    if byte_password == bytes(decrypted_password):
        # Close cursor and connection
        cursor.close()
        conn.close()
        return 1
    else:
        # Close cursor and connection
        cursor.close()
        conn.close()
        return 0
