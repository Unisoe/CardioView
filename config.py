import os.path
import sys

if getattr(sys, 'frozen', False):
    # Application is running as a bundle
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))