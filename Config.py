import os.path
import sys

if getattr(sys, 'frozen', False):
    # Application is running as a bundle
    application_path = sys._MEIPASS
    patient_file_path = os.path.join(application_path, 'patient_files')
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    patient_file_path = os.path.join(application_path, 'patient_files')