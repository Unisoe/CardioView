import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from Databases.patient_data_sqlite import new_entry, get_m_file
from popup import NewUserDialog
import RunProcessing
import serial
import struct


class UiMainWindow(object):
    def __init__(self):
        # # Set the size of the window
        # self.setGeometry(0, 0, 2000, 1200)

        # Get the screen geometry
        screen_geometry = QDesktopWidget().availableGeometry()

        # Calculate the position of the window
        x = int(np.round((screen_geometry.width() - self.width()) / 2))
        y = int(np.round((screen_geometry.height() - self.height()) / 2))

        # Move the window to the calculated position
        self.move(x, y)

        self.send_to_mc = None
        self.new_user = None
        self.timer = None
        self.y_coord = None
        self.x_coord = None
        self.pat_matrix = None
        self.axis = None
        self.figure = None
        self.centralwidget = None
        self.connect_mc = None
        self.date = None
        self.disp_graph = None
        self.disp_patient = None
        self.disp_speed = None
        self.file_search = None
        self.gridLayout = None
        self.line = None
        self.line_2 = None
        self.date_txt = None
        self.pat_name1 = None
        self.pat_num_txt1 = None
        self.thresh_txt = None
        self.load_data_txt = None
        self.new_pat_data_title = None
        self.get_pat_data_title = None
        self.pat_name2 = None
        self.pat_num2 = None
        self.load_data = None
        self.menubar = None
        self.new_pat_name = None
        self.new_pat_num = None
        self.prog_database = None
        self.prog_mc = None
        self.ser_pat_name = None
        self.ser_pat_num = None
        self.statusbar = None
        self.thresh = None
        self.upload_database = None
        self.upload_mc = None
        self.view_data = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.ser_pat_name = QtWidgets.QLineEdit(self.centralwidget)
        self.ser_pat_name.setObjectName("ser_pat_name")
        self.gridLayout.addWidget(self.ser_pat_name, 10, 5, 1, 4)

        self.ser_pat_num = QtWidgets.QLineEdit(self.centralwidget)
        self.ser_pat_num.setObjectName("ser_pat_num")
        self.gridLayout.addWidget(self.ser_pat_num, 11, 5, 1, 4)

        self.thresh = QtWidgets.QLineEdit(self.centralwidget)
        self.thresh.setObjectName("thresh")
        self.gridLayout.addWidget(self.thresh, 12, 5, 1, 1)

        self.get_pat_data_title = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.get_pat_data_title.setFont(font)
        self.get_pat_data_title.setAlignment(QtCore.Qt.AlignCenter)
        self.get_pat_data_title.setReadOnly(True)
        self.get_pat_data_title.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.get_pat_data_title, 9, 3, 1, 6)

        self.thresh_txt = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresh_txt.sizePolicy().hasHeightForWidth())
        self.thresh_txt.setSizePolicy(sizePolicy)
        self.thresh_txt.setReadOnly(True)
        self.thresh_txt.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.thresh_txt, 12, 3, 1, 1)

        # View Data Button
        self.view_data = QtWidgets.QPushButton(self.centralwidget)
        self.view_data.setObjectName("view_data")
        self.view_data.clicked.connect(self.ser_pat_info)
        self.gridLayout.addWidget(self.view_data, 12, 7, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 16, 1, 1, 9)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 8, 3, 1, 6)

        self.disp_speed = QtWidgets.QSlider(self.centralwidget)
        self.disp_speed.setOrientation(QtCore.Qt.Horizontal)
        self.disp_speed.setObjectName("disp_speed")
        self.disp_speed.setRange(1, 100)
        self.disp_speed.setValue(50)
        self.disp_speed.valueChanged.connect(self.slider_value_changed)
        self.gridLayout.addWidget(self.disp_speed, 10, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(17, 88, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 2, 4, 1)

        self.pat_num_txt1 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_num_txt1.sizePolicy().hasHeightForWidth())
        self.pat_num_txt1.setSizePolicy(sizePolicy)
        self.pat_num_txt1.setReadOnly(True)
        self.pat_num_txt1.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.pat_num_txt1, 11, 3, 1, 1)

        self.disp_patient = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.disp_patient.setObjectName("disp_patient")
        self.disp_patient.setReadOnly(True)
        self.gridLayout.addWidget(self.disp_patient, 11, 1, 3, 1)

        self.pat_name1 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_name1.sizePolicy().hasHeightForWidth())
        self.pat_name1.setSizePolicy(sizePolicy)
        self.pat_name1.setReadOnly(True)
        self.pat_name1.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.pat_name1, 10, 3, 1, 1)

        self.upload_mc = QtWidgets.QPushButton(self.centralwidget) #edithere maybe remove this button, have connection/send same button
        self.upload_mc.setObjectName("upload_mc")
        self.gridLayout.addWidget(self.upload_mc, 13, 8, 1, 1)

        self.connect_mc = QtWidgets.QPushButton(self.centralwidget) #edithere this might be the only button for connection
        self.connect_mc.setObjectName("connect_mc")
        self.connect_mc.clicked.connect(self.connect_to_model)
        self.gridLayout.addWidget(self.connect_mc, 12, 8, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(20, 127, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 10, 4, 3, 1)

        # upload to database button
        self.upload_database = QtWidgets.QPushButton(self.centralwidget)
        self.upload_database.setObjectName("upload_database")
        self.upload_database.clicked.connect(self.new_pat_info)
        self.gridLayout.addWidget(self.upload_database, 7, 8, 1, 1)

        spacerItem3 = QtWidgets.QSpacerItem(808, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 0, 1, 10)

        spacerItem4 = QtWidgets.QSpacerItem(20, 356, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 1, 0, 13, 1)

        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 1, 2, 9, 1)

        self.new_pat_data_title = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.new_pat_data_title.setFont(font)
        self.new_pat_data_title.setAlignment(QtCore.Qt.AlignCenter)
        self.new_pat_data_title.setReadOnly(True)
        self.new_pat_data_title.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.new_pat_data_title, 1, 3, 1, 6)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 3, 1, 6)

        self.load_data_txt = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_data_txt.sizePolicy().hasHeightForWidth())
        self.load_data_txt.setSizePolicy(sizePolicy)
        self.load_data_txt.setReadOnly(True)
        self.load_data_txt.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.load_data_txt, 3, 3, 1, 1)

        spacerItem6 = QtWidgets.QSpacerItem(20, 88, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 3, 4, 4, 1)

        self.load_data = QtWidgets.QLineEdit(self.centralwidget)
        self.load_data.setObjectName("load_data")
        self.gridLayout.addWidget(self.load_data, 3, 5, 1, 3)

        # New user button
        self.new_user = QtWidgets.QPushButton(self.centralwidget) # edithere
        self.new_user.setObjectName("new_user")
        self.new_user.clicked.connect(self.new_user_window)
        self.gridLayout.addWidget(self.new_user, 1, 1, 1, 1)

        # Create a figure and axis
        self.disp_graph = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph.setMinimumSize(QtCore.QSize(400, 400))
        self.disp_graph.setBaseSize(QtCore.QSize(400, 400))
        self.disp_graph.setObjectName("disp_graph")
        self.gridLayout.addWidget(self.disp_graph, 2, 1, 8, 1)

        spacerItem7 = QtWidgets.QSpacerItem(20, 356, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 1, 9, 13, 1)

        self.pat_name2 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_name2.sizePolicy().hasHeightForWidth())
        self.pat_name2.setSizePolicy(sizePolicy)
        self.pat_name2.setReadOnly(True)
        self.pat_name2.setObjectName("lineEdit_8")
        self.gridLayout.addWidget(self.pat_name2, 4, 3, 1, 1)

        # new patient name
        self.new_pat_name = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pat_name.setObjectName("new_pat_name")
        self.gridLayout.addWidget(self.new_pat_name, 4, 5, 1, 4)

        self.pat_num2 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_num2.sizePolicy().hasHeightForWidth())
        self.pat_num2.setSizePolicy(sizePolicy)
        self.pat_num2.setReadOnly(True)
        self.pat_num2.setObjectName("lineEdit_9")
        self.gridLayout.addWidget(self.pat_num2, 5, 3, 1, 1)

        # new patient number
        self.new_pat_num = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pat_num.setObjectName("new_pat_num")
        self.gridLayout.addWidget(self.new_pat_num, 5, 5, 1, 4)

        self.date_txt = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.date_txt.sizePolicy().hasHeightForWidth())
        self.date_txt.setSizePolicy(sizePolicy)
        self.date_txt.setReadOnly(True)
        self.date_txt.setObjectName("lineEdit_1")
        self.gridLayout.addWidget(self.date_txt, 6, 3, 1, 1)

        self.date = QtWidgets.QDateEdit(self.centralwidget)
        self.date.setObjectName("date")
        self.gridLayout.addWidget(self.date, 6, 5, 1, 4)

        # File Search Button
        self.file_search = QtWidgets.QPushButton(self.centralwidget)
        self.file_search.setObjectName("file_search")
        self.file_search.clicked.connect(self.openFileNameDialog)
        self.gridLayout.addWidget(self.file_search, 3, 8, 1, 1)

        self.prog_database = QtWidgets.QProgressBar(self.centralwidget)
        self.prog_database.setProperty("value", 24)
        self.prog_database.setObjectName("prog_database")
        self.gridLayout.addWidget(self.prog_database, 7, 3, 1, 5)

        self.prog_mc = QtWidgets.QProgressBar(self.centralwidget)
        self.prog_mc.setProperty("value", 24)
        self.prog_mc.setObjectName("prog_mc")
        self.gridLayout.addWidget(self.prog_mc, 13, 3, 1, 5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 889, 22))

        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.load_data.insert(fileName)

    def new_pat_info(self):
        # User input
        load_data = str(self.load_data.text())
        new_pat_name = str(self.new_pat_name.text())
        new_pat_num = int(self.new_pat_num.text())
        new_pat_date = str(self.date.text())
        new_entry(load_data, new_pat_name, new_pat_num, new_pat_date)

    def new_user_window(self):

        self.popup_user_window = NewUserDialog()
        self.popup_user_window.show()
        
    def no_pat_window(self):
        QMessageBox.about(self, "Error", "This patient does not exist.")

    def connect_to_model(self):
        ser = serial.Serial('COM3', 9600)  # Replace with the appropriate serial port
        matrix = self.send_to_mc

        data = struct.pack('<112i', *sum(matrix, []))

        ser.write(data)
        ser.close()

    def ser_pat_info(self):
        # User input
        ser_pat_name = str(self.ser_pat_name.text())
        ser_pat_num = int(self.ser_pat_num.text())
        thresh = str(self.thresh.text())

        # Pull patient info
        m_file, gif_file, pat_name, pat_num, date = get_m_file(ser_pat_name, ser_pat_num)

        # Run Processing
        self.send_to_mc = RunProcessing.run_processing(m_file, thresh, pat_num)

        # Display gif
        movie = QtGui.QMovie(gif_file)
        self.disp_graph.setMovie(movie)
        movie.start
        os.remove(gif_file) #edithere - may need to remove gif file later, not sure if it is stored in memory

        # Display patient info edithere
        text = f"Patient Name = {pat_name}\nPatient Number = {pat_num}\nData Entry Date = {date}"
        self.disp_patient.setPlainText(text)

    def slider_value_changed(self, value): #edithere
        # Set the speed of the GIF based on the value of the slider
        self.movie.setSpeed(value)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.new_user.setText(_translate("MainWindow", "New User"))
        self.get_pat_data_title.setText(_translate("MainWindow", "GET PATIENT DATA"))
        self.thresh_txt.setText(_translate("MainWindow", "Threshold:"))
        self.view_data.setText(_translate("MainWindow", "View Data"))
        self.pat_num_txt1.setText(_translate("MainWindow", "Patient Number:"))
        self.pat_name1.setText(_translate("MainWindow", "Patient Name:"))
        self.upload_mc.setText(_translate("MainWindow", "Upload to Model"))
        self.connect_mc.setText(_translate("MainWindow", "Connect to Model"))
        self.upload_database.setText(_translate("MainWindow", "Upload to Database"))
        self.new_pat_data_title.setText(_translate("MainWindow", "NEW PATIENT DATA"))
        self.load_data_txt.setText(_translate("MainWindow", "Load Data:"))
        self.pat_name2.setText(_translate("MainWindow", "Patient Name:"))
        self.pat_num2.setText(_translate("MainWindow", "Patient Number:"))
        self.date_txt.setText(_translate("MainWindow", "Date:"))
        self.file_search.setText(_translate("MainWindow", "File Search"))
