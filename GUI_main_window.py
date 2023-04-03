import os
import string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QGridLayout
import config
from patient_data_sqlite import new_entry, get_patient
from popup import NewUserDialog
import RunProcessing
import serial
import time


class UiMainWindow(object):
    def __init__(self):
        super().__init__()
        self.disp_patient_title = None
        self.line_disp = None
        self.msg_box = None
        self.pixmap3 = None
        self.pixmap2 = None
        self.pixmap1 = None
        self.disp_graph_3 = None
        self.disp_graph_2 = None
        self.disp_graph_1 = None
        self.rightLayout = None
        self.leftLayout = None
        self.resizing = None
        self.gif = None
        self.popup_user_window = None
        self.send_to_mc = None
        self.new_user = None
        self.centralwidget = None
        self.connect_mc = None
        self.date = None
        self.disp_graph_gif = None
        self.disp_patient = None
        self.disp_speed = None
        self.file_search = None
        self.outerLayout = None
        self.line_get = None
        self.date_txt = None
        self.pat_name_get = None
        self.pat_num_txt1 = None
        self.thresh_txt = None
        self.load_data_txt = None
        self.new_pat_data_title = None
        self.get_pat_data_title = None
        self.new_pat_name_label = None
        self.pat_num2 = None
        self.load_data = None
        self.menubar = None
        self.new_pat_name = None
        self.new_pat_num = None
        self.ser_pat_name = None
        self.ser_pat_num = None
        self.statusbar = None
        self.thresh = None
        self.upload_database = None
        self.upload_mc = None
        self.view_data = None


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.setWindowIcon(QtGui.QIcon('Logo.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.outerLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.outerLayout.setObjectName("outerLayout")

        stylesheet = "QWidget { font_title-size: 15px; }"
        self.centralwidget.setStyleSheet(stylesheet)
        self.leftLayout = QGridLayout()
        self.rightLayout = QGridLayout()

        self.ser_pat_name = QtWidgets.QLineEdit(self.centralwidget)
        self.ser_pat_name.setObjectName("ser_pat_name")
        self.rightLayout.addWidget(self.ser_pat_name, 8, 3, 1, 3)

        self.ser_pat_num = QtWidgets.QLineEdit(self.centralwidget)
        self.ser_pat_num.setObjectName("ser_pat_num")
        self.rightLayout.addWidget(self.ser_pat_num, 9, 3, 1, 3)

        self.thresh = QtWidgets.QLineEdit(self.centralwidget)
        self.thresh.setObjectName("thresh")
        self.rightLayout.addWidget(self.thresh, 10, 3, 1, 1)

        # View Data Button
        self.view_data = QtWidgets.QPushButton(self.centralwidget)
        self.view_data.setObjectName("view_data")
        self.view_data.clicked.connect(self.ser_pat_info)
        self.rightLayout.addWidget(self.view_data, 10, 4, 1, 1)

        # Connect to MC button
        self.connect_mc = QtWidgets.QPushButton(self.centralwidget)
        self.connect_mc.setObjectName("connect_mc")
        self.connect_mc.clicked.connect(self.connect_to_model)
        self.rightLayout.addWidget(self.connect_mc, 10, 5, 1, 1)

        self.get_pat_data_title = QtWidgets.QLabel(self.centralwidget)
        font_title = QtGui.QFont()
        font_title.setBold(True)
        font_title.setWeight(75)
        self.get_pat_data_title.setFont(font_title)
        self.get_pat_data_title.setAlignment(QtCore.Qt.AlignCenter)
        self.get_pat_data_title.setObjectName("Get Patient Data Title")
        self.rightLayout.addWidget(self.get_pat_data_title, 7, 2, 1, 4)

        self.thresh_txt = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.thresh_txt.setSizePolicy(sizePolicy)
        self.thresh_txt.setObjectName("Thresh Label")
        self.rightLayout.addWidget(self.thresh_txt, 10, 2, 1, 1)

        self.line_get = QtWidgets.QFrame(self.centralwidget)
        self.line_get.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_get.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_get.setObjectName("line_get")
        self.rightLayout.addWidget(self.line_get, 6, 2, 1, 4)

        self.line_disp = QtWidgets.QFrame(self.centralwidget)
        self.line_disp.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_disp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_disp.setObjectName("line_disp")
        self.rightLayout.addWidget(self.line_disp, 11, 2, 1, 4)

        self.pat_num_txt1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.pat_num_txt1.sizePolicy().hasHeightForWidth())
        self.pat_num_txt1.setSizePolicy(sizePolicy)
        self.pat_num_txt1.setObjectName("New Pat Num Label")
        self.rightLayout.addWidget(self.pat_num_txt1, 4, 2, 1, 1)

        self.pat_name_get = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.pat_name_get.sizePolicy().hasHeightForWidth())
        self.pat_name_get.setSizePolicy(sizePolicy)
        self.pat_name_get.setObjectName("Get Patient Label")
        self.rightLayout.addWidget(self.pat_name_get, 8, 2, 1, 1)

        # upload to database button
        self.upload_database = QtWidgets.QPushButton(self.centralwidget)
        self.upload_database.setObjectName("upload_database")
        self.upload_database.clicked.connect(self.new_pat_info)
        self.rightLayout.addWidget(self.upload_database, 5, 5, 1, 1)

        self.new_pat_data_title = QtWidgets.QLabel(self.centralwidget)
        self.new_pat_data_title.setFont(font_title)
        self.new_pat_data_title.setAlignment(QtCore.Qt.AlignCenter)
        self.new_pat_data_title.setObjectName("lineEdit_6")
        self.rightLayout.addWidget(self.new_pat_data_title, 1, 2, 1, 4)

        self.load_data_txt = QtWidgets.QLabel(self.centralwidget)
        self.load_data_txt.setSizePolicy(sizePolicy)
        self.load_data_txt.setObjectName("lineEdit_5")
        self.rightLayout.addWidget(self.load_data_txt, 2, 2, 1, 1)

        self.load_data = QtWidgets.QLineEdit(self.centralwidget)
        self.load_data.setObjectName("load_data")
        self.rightLayout.addWidget(self.load_data, 2, 3, 1, 2)

        self.new_pat_name_label = QtWidgets.QLabel(self.centralwidget)
        self.new_pat_name_label.setSizePolicy(sizePolicy)
        self.new_pat_name_label.setObjectName("lineEdit_8")
        self.rightLayout.addWidget(self.new_pat_name_label, 3, 2, 1, 1)

        # new patient name
        self.new_pat_name = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pat_name.setObjectName("new_pat_name")
        self.rightLayout.addWidget(self.new_pat_name, 3, 3, 1, 3)

        self.pat_num2 = QtWidgets.QLabel(self.centralwidget)
        self.pat_num2.setSizePolicy(sizePolicy)
        self.pat_num2.setObjectName("lineEdit_9")
        self.rightLayout.addWidget(self.pat_num2, 9, 2, 1, 1)

        # new patient number
        self.new_pat_num = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pat_num.setObjectName("new_pat_num")
        self.rightLayout.addWidget(self.new_pat_num, 4, 3, 1, 3)

        self.date_txt = QtWidgets.QLabel(self.centralwidget)
        self.date_txt.setSizePolicy(sizePolicy)
        self.date_txt.setObjectName("lineEdit_1")
        self.rightLayout.addWidget(self.date_txt, 5, 2, 1, 1)

        self.date = QtWidgets.QDateEdit(self.centralwidget)
        self.date.setDate(QDate.currentDate())
        self.date.setObjectName("date")
        self.rightLayout.addWidget(self.date, 5, 3, 1, 2)

        # File Search Button
        self.file_search = QtWidgets.QPushButton(self.centralwidget)
        self.file_search.setObjectName("file_search")
        self.file_search.clicked.connect(self.openFileNameDialog)
        self.rightLayout.addWidget(self.file_search, 2, 5, 1, 1)

        # Speed toggle slider
        self.disp_speed = QtWidgets.QSlider(self.centralwidget)
        self.disp_speed.setOrientation(QtCore.Qt.Horizontal)
        self.disp_speed.setObjectName("Disp Speed Slider")
        self.disp_speed.setRange(0, 200)
        self.disp_speed.setValue(100)
        self.disp_speed.setEnabled(False)
        self.disp_speed.valueChanged.connect(self.slider_value_changed)
        self.leftLayout.addWidget(self.disp_speed, 3, 1, 1, 1)

        # Patient info display
        self.disp_patient_title = QtWidgets.QLabel(self.centralwidget)
        self.disp_patient_title.setFont(font_title)
        self.disp_patient_title.setAlignment(QtCore.Qt.AlignCenter)
        self.disp_patient_title.setObjectName("disp_patient_title")
        self.rightLayout.addWidget(self.disp_patient_title, 12, 2, 1, 4)
        
        self.disp_patient = QtWidgets.QLabel(self.centralwidget)
        self.disp_patient.setObjectName("disp_patient")
        self.rightLayout.addWidget(self.disp_patient, 13, 1, 1, 4)

        # New user button
        self.new_user = QtWidgets.QPushButton(self.centralwidget)
        self.new_user.setObjectName("new_user")
        self.new_user.clicked.connect(self.new_user_window)
        self.leftLayout.addWidget(self.new_user, 1, 1, 1, 1)

        # Create a figure and axis for the gif
        self.disp_graph_gif = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_gif.setMinimumSize(QtCore.QSize(300,225))
        self.disp_graph_gif.setBaseSize(QtCore.QSize(300, 225))
        self.disp_graph_gif.setScaledContents(True)
        self.disp_graph_gif.setObjectName("disp_graph_gif")
        self.leftLayout.addWidget(self.disp_graph_gif, 2, 1, 1, 1)

        # Create a figure and axis for
        self.disp_graph_1 = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_1.setMinimumSize(QtCore.QSize(300,90))
        self.disp_graph_1.setBaseSize(QtCore.QSize(300,90))
        self.disp_graph_1.setScaledContents(True)
        self.disp_graph_1.setObjectName("disp_graph_1")
        self.leftLayout.addWidget(self.disp_graph_1, 4, 1, 1, 1)

        # Create a figure and axis
        self.disp_graph_2 = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_2.setMinimumSize(QtCore.QSize(300,90))
        self.disp_graph_2.setBaseSize(QtCore.QSize(300,90))
        self.disp_graph_2.setScaledContents(True)
        self.disp_graph_2.setObjectName("disp_graph_2")
        self.leftLayout.addWidget(self.disp_graph_2, 5, 1, 1, 1)

        # Create a figure and axis
        self.disp_graph_3 = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_3.setMinimumSize(QtCore.QSize(300,90))
        self.disp_graph_3.setBaseSize(QtCore.QSize(300,90))
        self.disp_graph_3.setScaledContents(True)
        self.disp_graph_3.setObjectName("disp_graph_3")
        self.leftLayout.addWidget(self.disp_graph_3, 6, 1, 1, 1)

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

        self.outerLayout.addLayout(self.leftLayout)
        self.outerLayout.addLayout(self.rightLayout)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.load_data.insert(fileName)

    def new_pat_info(self):
        # User input
        if str(self.load_data.text()) or str(self.new_pat_name.text()) or int(self.new_pat_num.text()) == '':
            QMessageBox.about(self, "CardioView", "Please provide all required patient information")
            return
        else:
            load_data = str(self.load_data.text())
            new_pat_name = str(self.new_pat_name.text())
            new_pat_num = int(self.new_pat_num.text())
            new_pat_date = str(self.date.text())
            new_entry(load_data, new_pat_name, new_pat_num, new_pat_date)

    def new_user_window(self):

        self.popup_user_window = NewUserDialog()
        self.popup_user_window.show()

    def connect_to_model(self): #edithere
        ser = serial.Serial()  # initialize serial communication
        ser.baudrate = 9600
        ser.port = None
        ser.timeout = 1

        print("Searching for available ports...") # edithere popup
        time.sleep(1)

        portNames = []  # find available serial ports
        portCount = 0
        while True:
            line = ser.readline().decode().strip()
            if line.startswith("COM"):
                portNames.append(line.split(":")[0])
                print(str(portCount) + ". " + portNames[portCount]) # edithere popup
                portCount += 1
            if not ser.inWaiting():
                break

        selectedPort = -1  # ask user to select a port
        while selectedPort < 0 or selectedPort >= portCount:
            selectedPort = int(input("Select a port number (0-" + str(portCount - 1) + "): ")) # edithere popup

        ser.port = portNames[selectedPort]  # connect to the selected port
        ser.open()

        print("Connected to " + ser.port) # edithere make this into a popup

        matrix = self.send_to_mc,  # single line array
        ser.write(matrix)
        ser.close()
    def ser_pat_info(self):
        # User input
        if str(self.ser_pat_name.text()) or str(self.ser_pat_name.text()) == '':
            QMessageBox.about(self, "CardioView", "Please fill out all required fields")
            return
        else:
            ser_pat_name = str(self.ser_pat_name.text())
            ser_pat_num = int(self.ser_pat_num.text())

        if self.thresh.text() != '':
            thresh = str(self.thresh.text())
        else:
            thresh = 1

        # Pull patient info
        t_file = get_patient(ser_pat_name, ser_pat_num)
        if t_file is None:
            return
        else:
            pat_name, pat_num, date = t_file
            m_file = os.path.join(config.patient_file_path, f'{pat_num}.m')
            gif_file = os.path.join(config.patient_file_path, f'{pat_num}.gif')

        # Run Processing
        msg_box = QMessageBox()
        msg_box.setText("Patient data is being processed, please wait.")
        msg_box.setWindowTitle("CardioView")
        msg_box.setIconPixmap(QPixmap("Logo.png"))
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.show()
        self.send_to_mc = RunProcessing.run_processing(m_file, gif_file, thresh, pat_num)
        msg_box.close()

        # Display patient info
        text = f"\t\tPatient Name:\t\t\t{string.capwords(pat_name)}\n\t\tPatient Number:\t\t\t{pat_num}\n\t\tDate of File Creation:\t\t{date}"
        self.disp_patient.setText(text)

        # Display gif
        self.gif = QtGui.QMovie(gif_file)
        self.disp_graph_gif.setMovie(self.gif)
        self.pixmap1 = QPixmap(os.path.join(config.patient_file_path, f'{pat_num}16.png'))
        self.disp_graph_1.setPixmap(self.pixmap1)
        self.pixmap2 = QPixmap(os.path.join(config.patient_file_path, f'{pat_num}50.png'))
        self.disp_graph_2.setPixmap(self.pixmap2)
        self.pixmap3 = QPixmap(os.path.join(config.patient_file_path, f'{pat_num}107.png'))
        self.disp_graph_3.setPixmap(self.pixmap3)
        self.gif.start()
        self.disp_speed.setEnabled(True)

    def slider_value_changed(self, value):
        # Set the speed of the GIF based on the value of the slider
        self.gif.setSpeed(value)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CardioView"))
        self.new_user.setText(_translate("MainWindow", "New User"))
        self.get_pat_data_title.setText(_translate("MainWindow", "GET PATIENT DATA"))
        self.thresh_txt.setText(_translate("MainWindow", "Threshold:"))
        self.view_data.setText(_translate("MainWindow", "View Data"))
        self.pat_num_txt1.setText(_translate("MainWindow", "Patient Number:"))
        self.pat_name_get.setText(_translate("MainWindow", "Patient Name:"))
        self.connect_mc.setText(_translate("MainWindow", "Connect to Model"))
        self.upload_database.setText(_translate("MainWindow", "Upload to Database"))
        self.new_pat_data_title.setText(_translate("MainWindow", "NEW PATIENT DATA"))
        self.load_data_txt.setText(_translate("MainWindow", "Load Data:"))
        self.new_pat_name_label.setText(_translate("MainWindow", "Patient Name:"))
        self.pat_num2.setText(_translate("MainWindow", "Patient Number:"))
        self.date_txt.setText(_translate("MainWindow", "Date:"))
        self.file_search.setText(_translate("MainWindow", "File Search"))
        self.disp_patient_title.setText(_translate("MainWindow", "DISPLAY INFORMATION"))
