import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
import Config

class ConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CardioView")
        self.setWindowIcon(QIcon(os.path.join(Config.application_path, "Logo.png")))

        layout = QVBoxLayout(self)
        stylesheet = "QWidget { font-size: 15px; }"
        self.setStyleSheet(stylesheet)

        wireless_button = QPushButton("Wireless Connection", self)
        layout.addWidget(wireless_button)
        wireless_button.clicked.connect(self.wireless_connection)

        wired_button = QPushButton("Wired Connection", self)
        layout.addWidget(wired_button)
        wired_button.clicked.connect(self.wired_connection)

        cancel_button = QPushButton("Cancel", self)
        layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.reject)

    @staticmethod
    def wireless_connection():
        pass

    @staticmethod
    def wired_connection():
        pass

    # @staticmethod #EDITHERE THIS IS V1
    # def wired_connection(): #edithere
    #     ser = serial.Serial()  # initialize serial communication
    #     ser.baudrate = 9600
    #     ser.port = None
    #     ser.timeout = 1
    #
    #     print("Searching for available ports...")
    #     time.sleep(1)
    #
    #     portNames = []  # find available serial ports
    #     portCount = 0
    #     while True:
    #         line = ser.readline().decode().strip()
    #         if line.startswith("COM"):
    #             portNames.append(line.split(":")[0])
    #             print(str(portCount) + ". " + portNames[portCount])
    #             portCount += 1
    #         if not ser.inWaiting():
    #             break
    #
    #     selectedPort = -1  # ask user to select a port
    #     while selectedPort < 0 or selectedPort >= portCount:
    #         selectedPort = int(input("Select a port number (0-" + str(portCount - 1) + "): "))
    #
    #     ser.port = portNames[selectedPort]  # connect to the selected port
    #     ser.open()
    #
    #     print("Connected to " + ser.port)
    #
    #     import GUI_main_window
    #     matrix = GUI_main_window.UiMainWindow.send_to_mc,  # single line array
    #     ser.write(matrix)
    #     ser.close()



#     @staticmethod
#     def wireless_connection():
#         address = "00:22:04:01:0B:00"  # need to put MAC address of the HC05 module
#         bluetooth_port_offset = 1
#         bluetooth_port = int(selectedPort.split('COM')[1]) + bluetooth_port_offset
#         matrix_str = 112 + "\n"
#
#         sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#         sock.connect((address, bluetooth_port))
#
#     @staticmethod
#     def wired_connection():
#         portNames = get_available_ports()
#         selectedPort = select_port(portNames)
#         ser_usb = serial.Serial(selectedPort, 9600)
#
# def get_available_ports():
#     available_ports = []
#     for i in range(256):
#         try:
#             ser = serial.Serial(i)
#             available_ports.append(ser.name)
#             ser.close()
#         except serial.SerialException:
#             pass
#     return available_ports
#
# def select_port(portNames):
#     print("Available ports:")
#     for i, portName in enumerate(portNames):
#         print(f"{i}. {portName}")
#     selectedPort = None
#     while selectedPort is None:
#         try:
#             portIndex = int(input("Select a port number: "))
#             selectedPort = portNames[portIndex]
#         except (ValueError, IndexError):
#             print("Invalid selection, please try again.")
#     return selectedPort
