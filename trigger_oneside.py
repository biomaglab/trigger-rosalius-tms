import threading
import os
import time
import socketio
import threading

import keyboard
import serial
import numpy as np
import random

# Publisher messages from invesalius
PUB_MESSAGES = [
    'Coil at target',
    'Marker label',
]

# File to register sequences
file_name = 'markers_label_sequence.txt'

target_status = False
create_navigation_marker = True
delete_marker=False
unset_marker=False
debug_arduino = False
number_of_stimuli = 3
ISI =  100 #Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option

def SendoToArduino(connection, msg):
    '''
    As mensagens para o Arduino seguem a seguinte lógica:
    1: Pulso simples
    2: Pulso pareado inibitório
    3: Pulso pareado excitatório
    '''
    msg = str(msg)
    connection.write(msg.encode())

# def ReadFromArduino(connection):
#     print(connection.readline())

# Try connection and send message
def ArduinoConnection():
    try:
        connection = serial.Serial("COM3", "9600", timeout=1)
        print("Connection Established")
        return connection
        #time.sleep(1.0)
        #ser.write(message.encode())
        #ser.close()
    except serial.SerialException:
        print("Connection Error. Check the Port")
        return None

class RemoteControl:
    def __init__(self, remote_host):
        self.__buffer = []
        self.__remote_host = remote_host
        self.__connected = False
        self.__sio = socketio.Client()

        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('to_robot', self.__on_message_receive)

        self.__lock = threading.Lock()

    def __on_connect(self):
        print("Connected to {}".format(self.__remote_host))
        self.__connected = True

    def __on_disconnect(self):
        print("Disconnected")
        self.__connected = False

    def __on_message_receive(self, msg):
        self.__lock.acquire()
        self.__buffer.append(msg)
        self.__lock.release()

    def get_buffer(self):
        self.__lock.acquire()
        res = self.__buffer.copy()
        self.__buffer = []
        self.__lock.release()
        return res

    def try_connect(self):
        self.__sio.connect(self.__remote_host, wait_timeout = 1)

        while not self.__connected:
            print("Connecting...")
            time.sleep(1.0)

    def send_message(self, topic, data={}):
        self.__sio.emit('from_robot', {'topic' : topic, 'data' : data})

class UpdateNavigationInfo:
    def __init__(self):
        ''' Define information for updating navigation information; characteristics of the object
        '''

        self.rc1 = RemoteControl('http://192.168.200.202:5000')  # Refers to the first pulse, the Conditioning Stimulus (CS)
        #self.rc1 = RemoteControl('http://127.0.0.1:5000')  # Refers to the first pulse, the Conditioning Stimulus (CS)
        #self.rc2 = RemoteControl('http://127.0.0.1:1000') # Refers to the second pulse, the Test Stimulus (TS)
        self.message = 'Coil at target' #Message that is going to be checked in the Buffer
        self.message2 = 'Marker label'
        self.target_status_relay1 = None
        #self.target_status_relay2 = None
        self.marker_label = None
        self.rc1.try_connect()
        #self.rc2.try_connect()
        self.call_thread()

    # def get_buffer_msg(self,rc,message, output_name):
    #
    #     while True:
    #         buf = rc.get_buffer()
    #         #self.buf2 = self.rc2.get_buffer()
    #
    #         if len(buf) == 0:
    #             pass
    #         elif message in [d['topic'] for d in buf]:
    #             for i in range(len(buf)):
    #                 topic = [d['topic'] for d in buf]
    #                 if topic[i] == message:
    #                     output_name = buf[i]["data"]["state"]
    def update_target_status(self):
        '''
        Check the message status in the Buffer that comes from the relay_server
        '''

        while True:
            self.buf1 = self.rc1.get_buffer()
            #self.buf2 = self.rc2.get_buffer()

            if len(self.buf1) == 0:
                pass
            elif any(item in [d['topic'] for d in self.buf1] for item in PUB_MESSAGES):
                for i in range(len(self.buf1)):
                    topic = [d['topic'] for d in self.buf1]
                    if topic[i] == self.message:
                        self.target_status_relay1 = self.buf1[i]["data"]["state"]
                    elif topic[i] == self.message2:
                        self.marker_label = self.buf1[i]["data"]["state"]


            # elif self.message in [d['topic'] for d in self.buf1]:
            #     for i in range(len(self.buf1)):
            #         topic = [d['topic'] for d in self.buf1]
            #         if topic[i] == self.message:
            #             self.target_status_relay1 = self.buf1[i]["data"]["state"]

            #print(f'target 1 = {self.target_status_relay1}')
            time.sleep(0.2)


    def call_thread(self):
        '''
        Call the update_target_status function as a thread
        '''
        self.thread = threading.Thread(target=self.update_target_status, daemon=True)
        self.thread.start()

    def get_marker_label(self):

        #self.buf1 = self.rc1.get_buffer()
        #self.buf2 = self.rc2.get_buffer()

        if len(self.buf1) == 0:
            pass
        elif self.message2 in [d['topic'] for d in self.buf1]:
            for i in range(len(self.buf1)):
                topic = [d['topic'] for d in self.buf1]
                if topic[i] == self.message2:
                    self.marker_label = self.buf1[i]["data"]["state"]

        print(f'MARKER LABEL = {self.marker_label}')


def send_trigger_to_navigation(rc):
    global create_navigation_marker
    if create_navigation_marker:
        topic = 'Create marker'
        data = {}
        rc.send_message(topic, data)

def send_to_navigation_delete_marker(rc):
    global delete_marker
    if delete_marker:
        topic = 'Delete marker'
        data = {'Enabled':'True'}
        rc.send_message(topic, data)
def send_to_navigation_unset_marker(rc):
    global unset_marker
    if unset_marker:
        topic = 'Unset marker'
        data = {'Enabled':'False'}
        rc.send_message(topic, data)




'''Connection to Arduino'''
arduino_connection = ArduinoConnection()
updator = UpdateNavigationInfo()

print("start sequence")
pulse_index = 0

start_sequence = False #Futuramente vai ser o botão
#rc1 = UpdateNavigationInfo()
#rc2 = UpdateNavigationInfo()

# File configs
dir = 'Markers-sequence/' + file_name
if os.path.exists(dir):
    mode = 'a'
else:
    mode = 'w'
file = open(dir, mode)
file.write('---------------------------\n')

while True:

    # if keyboard.is_pressed('d'):
    #     send_to_navigation_delete_marker(rc1.rc1)
    #     time.sleep(2)
    #     print('delete marker')
    #
    # if keyboard.is_pressed('u'):
    #     send_to_navigation_unset_marker(rc1.rc1)
    #     time.sleep(2)
    #     print('unset marker')
    # if keyboard.is_pressed('c'):
    #     send_trigger_to_navigation(rc1.rc1)
    #     time.sleep(2)
    #     print('create marker')


    #This one sends the pulses direclty to Arduino, without need of the navigation
    if debug_arduino:
        SendoToArduino(arduino_connection, 4)
        #ReadFromArduino(arduino_connection)
        time.sleep(5)
    else:
        if not arduino_connection:
            print("Arduino connection Error. Check the Port")
            break

        if start_sequence or keyboard.is_pressed('s'):
            while pulse_index < number_of_stimuli:  #Esse while vai mudar para algo do tipo delivering target on, para poder pausar a sequencia
                print(updator.target_status_relay1)
                if updator.target_status_relay1:
                    SendoToArduino(arduino_connection, 1) #A mensagem se mofifica a partir da escolha do tipo de pulso (Simples, pareado, etc)
                    file.write(f'{updator.marker_label}\n')
                    #send_trigger_to_navigation(rc1.rc1)
                    #send_to_navigation_delete_marker(rc1)
                    print("disparando")
                    time.sleep(random.uniform(7, 10))
                    pulse_index += 1

            file.close()
        #hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= number_of_stimuli:
            break
        time.sleep(0.01)

