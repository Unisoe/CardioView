# import serial
# import time
# import bluetooth
#
# # Find available serial ports
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
# # User selects serial port
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
#
# # Wired Connection
# portNames = get_available_ports()
# selectedPort = select_port(portNames)
# ser_usb = serial.Serial(selectedPort, 9600)
#
# # Wireless Connection
# address = "00:22:04:01:0B:00" # need to put MAC address of the HC05 module
# bluetooth_port_offset = 1
# bluetooth_port = int(selectedPort.split('COM')[1]) + bluetooth_port_offset
# matrix_str = 112 + "\n"
#
# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# sock.connect((address, bluetooth_port))
#
# while True:
#     # Send matrix data over USB
#     ser_usb.write(b's') # start reading matrix
#     matrix_usb = ser_usb.readline().decode().strip() # read matrix from Arduino
#     print(f"USB: {matrix_usb}") # Print wired matrix data
#
#     # Send matrix data over Bluetooth
#     sock.send(matrix_str.encode('ascii')) # string over Bluetooth
#     matrix_bluetooth = sock.recv(1024).decode().strip()
#     print(f"Bluetooth: {matrix_bluetooth}")  # Print wireless matrix data
#
#     time.sleep(1)
#
# sock.close()
# ser_usb.close()



# import csv
# import PyBluez-updated
# import bluetooth
#
# # the address of the Bluetooth device
# bd_addr = "00:22:04:01:0B:00"
#
# # the data to send
# with open("C:/Users/krist/Downloads/vt_sample.csv", 'r') as file:
#     reader = csv.reader(file)
#
#     # read the first (and only) row of the CSV file into a list
#     row = next(reader)
#     data = [int(float(i.strip())) for i in row]
# # convert the data to a byte array
# byte_data = bytearray(data)
#
# # create a Bluetooth socket
# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#
# # connect to the Bluetooth device
# sock.connect((bd_addr, 1))
#
# # send the data
# sock.send(byte_data)
#
# # close the socket
# sock.close()


import serial
ser = serial.Serial('COM10', 9600)  # Replace 'COM3' with the name of your serial port

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
data = ','.join([str(item) for row in matrix for item in row]) + '\n'
ser.write_timeout = 1
ser.write(data.encode())
ser.flush()
ser.close()