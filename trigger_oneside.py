import os
import time
import keyboard
import random
from arduino_connection import ArduinoConnection
from update_navigation import UpdateNavigationInfo
import constants as consts

# File to register sequences
file_name = 'test.txt'

'''Connection to Arduino'''
arduino = ArduinoConnection()
arduino.connect('COM3', '9600')

'''Connection to Updator'''
updator = UpdateNavigationInfo()
updator.connect('192.168.200.202', '5000')

pulse_index = 0

# File configs
dir = 'Markers-sequence/' + file_name
if os.path.exists(dir):
    mode = 'a'
else:
    mode = 'w'
file = open(dir, mode)
file.write('---------------------------\n')

while True:

    #This one sends the pulses direclty to Arduino, without need of the navigation
    if consts.DEBUG_ARDUINO:
        arduino.send_to_arduino(4)
        time.sleep(5)
    else:
        if not arduino.arduino_connected:
            break

        if consts.START_SEQUENCE or keyboard.is_pressed('s'):
            print("Sequence Started")
            while pulse_index < consts.STIMULI_NUMBER:  #Esse while vai mudar para algo do tipo delivering target on, para poder pausar a sequencia
                print(updator.target_status)
                if updator.target_status:
                    arduino.send_to_arduino(1) #A mensagem se mofifica a partir da escolha do tipo de pulso (Simples, pareado, etc)
                    file.write(f'{updator.marker_label}\n')
                    print("disparando "+ str(updator.marker_label) + " __ "+ str(pulse_index))

                    time.sleep(random.uniform(7, 10))
                    pulse_index += 1

            file.close()
            arduino.disconnect()
        #hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= consts.STIMULI_NUMBER:
            break
        time.sleep(0.01)

