import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox
import Config
import asyncio
from bleak import BleakClient
from bleak import BleakScanner
import serial

class ConnectionDialog(QDialog):
    def __init__(self, send_to_mc):
        super().__init__()
        self.send_to_mc = send_to_mc
        self.setWindowTitle("CardioView")
        self.setWindowIcon(QIcon(os.path.join(Config.application_path, "Logo.png")))

        layout = QVBoxLayout(self)
        stylesheet = "QWidget { font-size: 15px; }"
        self.setStyleSheet(stylesheet)

        wireless_button = QPushButton("Wireless Connection", self)
        layout.addWidget(wireless_button)
        wireless_button.clicked.connect(self.wireless_connection(self.send_to_mc))

        wired_button = QPushButton("Wired Connection", self)
        layout.addWidget(wired_button)
        wired_button.clicked.connect(self.wired_connection(self.send_to_mc))

        cancel_button = QPushButton("Cancel", self)
        layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.reject)

    @staticmethod
    def wireless_connection(send_to_mc):
        write_characteristic = "00002A3D-0000-1000-8000-00805f9b34fb"
        read_characteristic = "00002A58-0000-1000-8000-00805f9b34fb"

        num = len(send_to_mc)

        def wireless_run():
            async def run(matrix_1):
                print('ProtoStax Arduino Nano BLE LED Peripheral Central Service')
                print('Looking for Arduino Nano 33 BLE Sense Peripheral Device...')
                found = False
                devices = await BleakScanner.discover()
                for d in devices:
                    # if "40C93D13-9572-020B-37A1-C30CBA580D16" == str(d.address): #use MAC address if needed
                    if 'Heart' == str(d.name):  # use MAC address if needed
                        print('Found Arduino Nano 33 BLE Sense Peripheral')
                        found = True
                        async with BleakClient(d.address) as client:
                            print(f'Connected to {d.address}')

                            input_str_1 = matrix_1

                            bytes_to_send_1 = bytearray(map(ord, input_str_1))

                            await client.write_gatt_char(write_characteristic, bytes_to_send_1)

                            # print(f"Sent: {input_str_1}")

                            val = await client.read_gatt_char(read_characteristic)
                            val_ = int.from_bytes(val, "big")

            # Run the function
            for i in range(num):
                matrix = send_to_mc[i]

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(run(matrix))
                except KeyboardInterrupt:
                    print('\nReceived Keyboard Interrupt')
                finally:
                    print('Program finished')
        wireless_run()
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(os.path.join(Config.application_path, "Logo.png")))
        msg_box.setWindowTitle("CardioView")
        msg_box.setText("Send Successful.")
        msg_box.exec_()

    @staticmethod
    def wired_connection():
        def wired_run():
            port = '/dev/cu.usbmodem14101'
            arduinoData = serial.Serial(port, 115200)

            while True:
                cmd = input('Enter your command: ')
                cmd = cmd + '\r'
                arduinoData.write(cmd.encode())
        wired_run()
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon(os.path.join(Config.application_path, "Logo.png")))
        msg_box.setWindowTitle("CardioView")
        msg_box.setText("Send Successful.")
        msg_box.exec_()