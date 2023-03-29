from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QGridLayout
from patient_data_sqlite import new_entry, get_m_file
from popup import NewUserDialog
import RunProcessing
import serial
import struct

class UiMainWindow(object):
    def __init__(self):
        super().__init__()
        self.popup_user_window = None
        self.movie = None
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
        self.disp_graph_gif = None
        self.disp_patient = None
        self.disp_speed = None
        self.file_search = None
        self.outerLayout = None
        self.line_get = None
        self.line_new = None
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
        self.outerLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.outerLayout.setObjectName("outerLayout")

        stylesheet = "QWidget { font-size: 15px; }"
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
        self.connect_mc = QtWidgets.QPushButton(self.centralwidget) #edithere this might be the only button for connection
        self.connect_mc.setObjectName("connect_mc")
        self.connect_mc.clicked.connect(self.connect_to_model)
        self.rightLayout.addWidget(self.connect_mc, 10, 5, 1, 1)

        self.get_pat_data_title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.get_pat_data_title.setFont(font)
        self.get_pat_data_title.setAlignment(QtCore.Qt.AlignCenter)
        self.get_pat_data_title.setObjectName("Get Patient Data Title")
        self.rightLayout.addWidget(self.get_pat_data_title, 7, 2, 1, 4)

        self.thresh_txt = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresh_txt.sizePolicy().hasHeightForWidth())
        self.thresh_txt.setSizePolicy(sizePolicy)
        self.thresh_txt.setObjectName("Thresh Label")
        self.rightLayout.addWidget(self.thresh_txt, 10, 2, 1, 1)

        self.line_get = QtWidgets.QFrame(self.centralwidget)
        self.line_get.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_get.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_get.setObjectName("line_get")
        self.rightLayout.addWidget(self.line_get, 6, 2, 1, 4)

        self.pat_num_txt1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_num_txt1.sizePolicy().hasHeightForWidth())
        self.pat_num_txt1.setSizePolicy(sizePolicy)
        self.pat_num_txt1.setObjectName("New Pat Num Label")
        self.rightLayout.addWidget(self.pat_num_txt1, 4, 2, 1, 1)

        self.pat_name_get = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_name_get.sizePolicy().hasHeightForWidth())
        self.pat_name_get.setSizePolicy(sizePolicy)
        self.pat_name_get.setObjectName("Get Patient Label")
        self.rightLayout.addWidget(self.pat_name_get, 8, 2, 1, 1)

        # upload to database button
        self.upload_database = QtWidgets.QPushButton(self.centralwidget)
        self.upload_database.setObjectName("upload_database")
        self.upload_database.clicked.connect(self.new_pat_info)
        self.rightLayout.addWidget(self.upload_database, 5, 5, 1, 1)  # edithere

        self.new_pat_data_title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.new_pat_data_title.setFont(font)
        self.new_pat_data_title.setAlignment(QtCore.Qt.AlignCenter)
        self.new_pat_data_title.setObjectName("lineEdit_6")
        self.rightLayout.addWidget(self.new_pat_data_title, 1, 2, 1, 4)

        self.load_data_txt = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_data_txt.sizePolicy().hasHeightForWidth())
        self.load_data_txt.setSizePolicy(sizePolicy)
        self.load_data_txt.setObjectName("lineEdit_5")
        self.rightLayout.addWidget(self.load_data_txt, 2, 2, 1, 1)

        self.load_data = QtWidgets.QLineEdit(self.centralwidget)
        self.load_data.setObjectName("load_data")
        self.rightLayout.addWidget(self.load_data, 2, 3, 1, 2)

        self.new_pat_name_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_pat_name_label.sizePolicy().hasHeightForWidth())
        self.new_pat_name_label.setSizePolicy(sizePolicy)
        self.new_pat_name_label.setObjectName("lineEdit_8")
        self.rightLayout.addWidget(self.new_pat_name_label, 3, 2, 1, 1)

        # new patient name
        self.new_pat_name = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pat_name.setObjectName("new_pat_name")
        self.rightLayout.addWidget(self.new_pat_name, 3, 3, 1, 3)

        self.pat_num2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pat_num2.sizePolicy().hasHeightForWidth())
        self.pat_num2.setSizePolicy(sizePolicy)
        self.pat_num2.setObjectName("lineEdit_9")
        self.rightLayout.addWidget(self.pat_num2, 9, 2, 1, 1)

        # new patient number
        self.new_pat_num = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pat_num.setObjectName("new_pat_num")
        self.rightLayout.addWidget(self.new_pat_num, 4, 3, 1, 3)

        self.date_txt = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.date_txt.sizePolicy().hasHeightForWidth())
        self.date_txt.setSizePolicy(sizePolicy)
        self.date_txt.setObjectName("lineEdit_1")
        self.rightLayout.addWidget(self.date_txt, 5, 2, 1, 1)

        self.date = QtWidgets.QDateEdit(self.centralwidget)
        self.date.setObjectName("date")
        self.rightLayout.addWidget(self.date, 5, 3, 1, 2) #edithere

        # File Search Button
        self.file_search = QtWidgets.QPushButton(self.centralwidget)
        self.file_search.setObjectName("file_search")
        self.file_search.clicked.connect(self.openFileNameDialog)
        self.rightLayout.addWidget(self.file_search, 2, 5, 1, 1)

        # Speed toggle slider
        self.disp_speed = QtWidgets.QSlider(self.centralwidget)
        self.disp_speed.setOrientation(QtCore.Qt.Horizontal)
        self.disp_speed.setObjectName("Disp Speed Slider")
        self.disp_speed.setRange(0, 10)
        self.disp_speed.setValue(5)
        self.disp_speed.setEnabled(False)
        self.disp_speed.valueChanged.connect(self.slider_value_changed)
        self.leftLayout.addWidget(self.disp_speed, 3, 1, 1, 1)

        # Patient info display
        self.disp_patient = QtWidgets.QLabel(self.centralwidget)
        self.disp_patient.setObjectName("disp_patient")
        self.leftLayout.addWidget(self.disp_patient, 7, 1, 1, 1)

        # New user button
        self.new_user = QtWidgets.QPushButton(self.centralwidget)  # edithere
        self.new_user.setObjectName("new_user")
        self.new_user.clicked.connect(self.new_user_window)
        self.leftLayout.addWidget(self.new_user, 1, 1, 1, 1)

        # Create a figure and axis for the gif
        self.disp_graph_gif = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_gif.setMinimumSize(QtCore.QSize(200, 200))
        self.disp_graph_gif.setBaseSize(QtCore.QSize(200, 200))
        self.disp_graph_gif.setObjectName("disp_graph_gif")
        self.leftLayout.addWidget(self.disp_graph_gif, 2, 1, 1, 1)

        # Create a figure and axis for
        self.disp_graph_1 = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_1.setMinimumSize(QtCore.QSize(200, 200))
        self.disp_graph_1.setBaseSize(QtCore.QSize(200, 200))
        self.disp_graph_1.setObjectName("disp_graph_1")
        self.leftLayout.addWidget(self.disp_graph_1, 4, 1, 1, 1)

        # Create a figure and axis
        self.disp_graph_2 = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_2.setMinimumSize(QtCore.QSize(200, 200))
        self.disp_graph_2.setBaseSize(QtCore.QSize(200, 200))
        self.disp_graph_2.setObjectName("disp_graph_2")
        self.leftLayout.addWidget(self.disp_graph_2, 5, 1, 1, 1)

        # Create a figure and axis
        self.disp_graph_3 = QtWidgets.QLabel(self.centralwidget)
        self.disp_graph_3.setMinimumSize(QtCore.QSize(200, 200))
        self.disp_graph_3.setBaseSize(QtCore.QSize(200, 200))
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
        self.setLayout(self.outerLayout)

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
        t_file = get_m_file(ser_pat_name, ser_pat_num)
        if t_file is None:
            return
        else:
            m_file, gif_file, pat_name, pat_num, date = t_file
        # Run Processing
        self.send_to_mc = RunProcessing.run_processing(m_file, thresh, pat_num)

        # Display patient info edithere
        text = f"Patient Name = {pat_name}\nPatient Number = {pat_num}\nData Entry Date = {date}"
        self.disp_patient.setText(text)

        # Display gif
        gif = QtGui.QMovie(gif_file)
        self.disp_graph_gif.setMovie(gif)
        gif_size = QPixmap(gif_file).size()
        self.disp_graph_gif.resize(gif_size) #resize the gif
        gif.start()
        self.movie.started.connect(lambda: self.disp_speed.setEnabled(True))
        self.movie.finished.connect(lambda: self.disp_speed.setEnabled(False))

    def slider_value_changed(self, value): #edithere
        # Set the speed of the GIF based on the value of the slider
        self.gif.setSpeed(value*10)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.new_user.setText(_translate("MainWindow", "New User"))
        self.get_pat_data_title.setText(_translate("MainWindow", "GET PATIENT DATA"))
        self.thresh_txt.setText(_translate("MainWindow", "Threshold:"))
        self.view_data.setText(_translate("MainWindow", "View Data"))
        self.pat_num_txt1.setText(_translate("MainWindow", "Patient Number:"))
        self.pat_name_get.setText(_translate("MainWindow", "Patient Name:"))
        # self.upload_mc.setText(_translate("MainWindow", "Upload to Model"))
        self.connect_mc.setText(_translate("MainWindow", "Connect to Model"))
        self.upload_database.setText(_translate("MainWindow", "Upload to Database"))
        self.new_pat_data_title.setText(_translate("MainWindow", "NEW PATIENT DATA"))
        self.load_data_txt.setText(_translate("MainWindow", "Load Data:"))
        self.new_pat_name_label.setText(_translate("MainWindow", "Patient Name:"))
        self.pat_num2.setText(_translate("MainWindow", "Patient Number:"))
        self.date_txt.setText(_translate("MainWindow", "Date:"))
        self.file_search.setText(_translate("MainWindow", "File Search"))
