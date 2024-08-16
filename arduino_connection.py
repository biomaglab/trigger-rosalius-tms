import serial
import constants as consts

class ArduinoConnection():
    def __init__(self):
        self.device = None
        self.arduino_connected = False

    def connect(self, port, baudrate):
        try:
            self.device = serial.Serial(port, baudrate, timeout=1)
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

    def send_to_arduino(self, msg):
        '''
        As mensagens para o Arduino seguem a seguinte lógica:
        1: Pulso simples
        2: Pulso pareado inibitório
        3: Pulso pareado excitatório
        '''
        msg = str(msg)
        self.device.write(msg.encode())

    def read_from_arduino(self):
        print(self.device.readline())