import time
import keyboard
import random
import numpy as np
from Components.arduino_connection import ArduinoConnection
from Components.constants import STIMULI_NUMBER
from Components.update_navigation import UpdateNavigationInfo
from Components import constants as consts, txt_configs as txt

'''Connection to Arduino'''
arduino = ArduinoConnection()
arduino.connect('COM3', 9600)

'''Connection to Updator'''
updator = UpdateNavigationInfo(1)
updator.connect('192.168.200.1', [5000])

''' Generating the time intervals '''
intervals = np.round(np.linspace(8, 10, STIMULI_NUMBER),0)
random.shuffle(intervals)
np.savetxt('intervals.txt',intervals, delimiter=',', fmt='%d')

pulse_index = 0

while True:

    #This one sends the pulses direclty to Arduino, without need of the navigation
    if consts.DEBUG_ARDUINO:
        arduino.send_to_arduino(1)
        time.sleep(5)
    else:
        if not arduino.arduino_connected:
            break

        if consts.START_SEQUENCE or keyboard.is_pressed('s'):
            print("Sequence Started")
            while pulse_index < consts.STIMULI_NUMBER:
                print(updator.target_status)
                if updator.target_status[0]:
                    arduino.send_to_arduino(1)
                    txt.file.write(f'{updator.marker_label[0]}\n')
                    print("disparando "+ str(updator.marker_label[0]) + " __ "+ str(pulse_index))
                    time.sleep(intervals[pulse_index])
                    pulse_index += 1

            txt.file.close()
            arduino.disconnect()
        #hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= consts.STIMULI_NUMBER:
            break
        time.sleep(0.01)

