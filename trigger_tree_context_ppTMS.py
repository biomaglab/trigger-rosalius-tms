#import os
#import sys

import time
import socketio
import threading

import keyboard
import serial
import random


target_status = False
create_navigation_marker = True
debug_arduino_ppTMS = False
number_of_stimuli = 10
ISI =  100 #Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option

def send_to_arduino(connection, msg):
    '''
    As mensagens para o Arduino seguem a seguinte lógica:
    1: Pulso simples
    2: Inibitório
    3: Excitatório
    '''
    msg = str(msg)
    connection.write(msg.encode())

# def ReadFromArduino(connection):
#     print(connection.readline())

# Try connection and send message
def arduino_connection():
    try:
        connection = serial.Serial("COM3", "115200", timeout=1)
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
        '''
        Define information for updating navigation information; characteristics of the object
        '''

        self.rc1 = RemoteControl('http://169.254.82.20:5000')  # Refers to the first pulse, the Conditioning Stimulus (CS)
        self.rc2 = RemoteControl('http://169.254.82.20:1000') # Refers to the second pulse, the Test Stimulus (TS)
        self.message = 'Coil at target' #Message that is going to be checked in the Buffer
        self.target_status_relay1 = None
        self.target_status_relay2 = None
        self.rc1.try_connect()
        self.rc2.try_connect()
        self.call_thread()

    def update_target_status(self):
        '''
        Check the message status in the Buffer that comes from the relay_server
        '''
        while True:
            self.buf1 = self.rc1.get_buffer()
            self.buf2 = self.rc2.get_buffer()

            if len(self.buf1) == 0:
                pass
            elif self.message in [d['topic'] for d in self.buf1]:
                for i in range(len(self.buf1)):
                    topic = [d['topic'] for d in self.buf1]
                    if topic[i] == self.message:
                        self.target_status_relay1 = self.buf1[i]["data"]["state"]

            if len(self.buf2) == 0:
                pass
            elif self.message in [d['topic'] for d in self.buf2]:
                for i in range(len(self.buf2)):
                    topic = [d['topic'] for d in self.buf2]
                    if topic[i] == self.message:
                        self.target_status_relay2 = self.buf2[i]["data"]["state"]

            #print(f'target 1 = {self.target_status_relay1} , target 2 = {self.target_status_relay2}')
            time.sleep(0.1)
            #return

    def call_thread(self):
        '''
        Call the update_target_status function as a thread, to run in parallel
        '''
        self.thread = threading.Thread(target=self.update_target_status, daemon=True)
        self.thread.start()

    # def get_navigation_status(self, msg):
    #     '''
    #     :param msg: put the message that you want to pull from the buffer. Ex: 'Coil at target'
    #     :param buff_number: choose which one of the buffers you want to acquire the information. Ex: 1 refers to rc1 = RemoteControl('http://127.0.0.1:5000')
    #     :return: the target status. OBS: some messages don't have the ["state"]
    #     '''
    #
    #     if len(buf) == 0:
    #         pass
    #     elif msg in [d['topic'] for d in buf]:
    #         for i in range(len(buf)):
    #             topic = [d['topic'] for d in buf]
    #             if topic[i] == msg:
    #                 print(i)
    #                 target_status = buf[i]["data"]["state"]
    #     return target_status

# def send_trigger_to_navigation(rc):
#     global create_navigation_marker
#     if create_navigation_marker:
#         topic = 'Create marker'
#         data = {}
#         rc.send_message(topic, data)


'''Connection to Arduino'''
arduino_connection = arduino_connection()
updator = UpdateNavigationInfo()

# if debug_arduino == False:
#     updator.rc1.try_connect()
#     updator.rc2.try_connect()

print("start sequence")
pulse_index = 0

start_sequence = True #Futuramente vai ser o botão

while True:

    #This one sends the pulses direclty to Arduino, without need of the navigation
    if debug_arduino_ppTMS == True:
        send_to_arduino(arduino_connection, 4)
        #ReadFromArduino(arduino_connection)
        time.sleep(5)

    if debug_arduino_ppTMS == False:
        if not arduino_connection:
            print("Arduino connection Error. Check the Port")
            break

        if start_sequence == True:
            while pulse_index < number_of_stimuli:  #Esse while vai mudar para algo do tipo delivering target on, para poder pausar a sequencia
                if updator.target_status_relay1 == True:
                    send_to_arduino(arduino_connection, 1)
                    print("disparando")
                time.sleep(random.uniform(4, 6))

                if updator.target_status_relay1 == True:
                    send_to_arduino(arduino_connection, 2) #Manda apenas um sinal, que já está associado ao pulso pareado
                    print("disparando")
                time.sleep(random.uniform(4, 6))

                if updator.target_status_relay1 == True:
                    send_to_arduino(arduino_connection, 3) #Manda apenas um sinal, que já está associado ao pulso pareado
                    print("disparando")

                time.sleep(random.uniform(4, 6))
                pulse_index += 1

        #hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= number_of_stimuli:
            break
        time.sleep(0.01)

