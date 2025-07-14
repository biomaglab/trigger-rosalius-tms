import serial
import serial.tools.list_ports as lp

available_ports = [port.description for port in lp.comports()]
print(available_ports)

class ArduinoConnection():
    def __init__(self):
        self.device = None
        self.arduino_connected = False

    def connect(self, port, baudrate):
        try:
            self.device = serial.Serial(port, str(baudrate), timeout=1)
            self.arduino_connected = True
            print("Arduino Connection Established")
        except serial.SerialException:
            print("Arduino Connection Error. Check the USB Port")
            self.arduino_connected = False
            self.device = None

    def disconnect(self):
        if self.arduino_connected:
            self.device.close()
            self.arduino_connected = False
            print("Arduino Disconnected")
        else:
            print("Arduino is not connected")

    def send_to_arduino(self, message):
        if self.arduino_connected:
            self.device.write((str(message) + '\n').encode())

    def read_from_arduino(self):
        read = self.device.readline()
        read = read.decode('utf-8')
        read = read.strip()

        try:
            read = int(read)  # converte a string para um número inteiro
            #print(read)  # exibe o número
            return read
        except ValueError:
            print("Não foi possível converter para número:", read)
        #print(self.device.readline())
        #return read
