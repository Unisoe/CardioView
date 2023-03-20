from user_sqlite import new_user, get_user
from patient_data_sqlite import new_entry, get_m_file, get_gif_path
from popup import NewUserDialog
from PyQt5.QtWidgets import QDialog
# username = "admin"
# password = "admin"
# re_password = "admin"
# new_user(username, password, re_password)
#
# accepted = get_user(username, password)
# print(accepted)

m_file_path = 'C:/Users/krist/PycharmProjects/capscone_sigprocessing_v1/vt1_sample.mat'
name = 'admin'
number = '123456789'
date = '2000-01-01'

# new_entry(m_file_path, name, number, date)
# get_m_file(name, number)
# get_gif_path(number)
# NewUserDialog(QDialog)

# import os
# from appdata import AppDataPaths
#
# iv = os.urandom(16)
# print(iv)
#
# app_paths = AppDataPaths()
# database_path = app_paths.app_data_path.replace('\\', '/')
# print(app_paths)
# print(database_path)
#
# import os
# import sys
#
# # Get the path to the temporary directory created by PyInstaller
# base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
#
# # Create a subdirectory within the temporary directory
# subdir_path = os.path.join(base_path, 'my_secret_directory')
# os.makedirs(subdir_path, exist_ok=True)
#
# # Set the file permissions of the subdirectory to read and execute only for the owner
# os.chmod(subdir_path, 0o700)
#
# # Write some data to a file called "mydata.m" in the subdirectory
# data = "x = 1:10;\ny = sin(x);\nplot(x, y);\n"
# file_path = os.path.join(subdir_path, 'mydata.m')
# print(file_path)
# with open(file_path, 'w') as f_user:
#     f_user.write(data)