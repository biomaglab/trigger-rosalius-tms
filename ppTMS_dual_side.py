import pyautogui
import keyboard
import numpy as np
import random
import time

from Components.constants import create_navigation_marker
#import magicpy.magicpy as mp
from Sequences.random_seq_gen import total_number_of_stimuli,stimuli_mode
from Components.arduino_connection import ArduinoConnection
from Components.update_navigation import UpdateNavigationInfo
from Components import txt_configs as txt
from Components import constants as consts, txt_configs as txt


print(total_number_of_stimuli)
#either pp or intensity
mode = "pp"
target_status = False
debug_arduino_ppTMS = False

pp_mode = {stimuli_mode[0]: "single",
           stimuli_mode[1]: "10ms",
           stimuli_mode[2]: "40ms",
           stimuli_mode[3]: "150ms"}


'''Connection to Arduino'''
arduino = ArduinoConnection()
arduino.connect('COM8', 9600)

'''Connection to Updator'''
updator = UpdateNavigationInfo(2)
updator.connect('169.254.100.20', [5000, 1000])

''' LOAD PULSE SEQUENCE '''
sequence = np.loadtxt('Sequences/random_sequence_20.txt', delimiter=',', dtype='int')
print(sequence)

while True:
    if keyboard.is_pressed('s'):
        break
print("start sequence")
pulse_index = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
ISI_measurements = []

while True:
    if updator.target_status[0]: ##CHECAR SE É ISSO MESMO
        print(updator.target_status)
        if mode == "pp":
            start = time.time()
            print(pp_mode[sequence[pulse_index]])
            if pp_mode[sequence[pulse_index]] == "single":
                print('Iniciando sequencia')
                #print(pp_mode[sequence[pulse_index]])
                arduino.send_to_arduino('single\n')

                if consts.create_navigation_marker:
                    updator.send_trigger_to_navigation()

                #measurements = arduino.read_from_arduino()
                #ISI_measurements.append(measurements)
                #print(ISI_measurements)
                #txt.file.write(f'{measurements}\n')


            elif pp_mode[sequence[pulse_index]] == "10ms":
                print('Iniciando sequencia')
                arduino.send_to_arduino('10')

                if consts.create_navigation_marker:
                    updator.send_trigger_to_navigation()

                #measurements = arduino.read_from_arduino()
                #ISI_measurements.append(measurements)
                #print(ISI_measurements)
                #txt.file.write(f'{measurements}\n')


            elif pp_mode[sequence[pulse_index]] == "40ms":
                print('Iniciando sequencia')
                arduino.send_to_arduino('40')

                if consts.create_navigation_marker:
                    updator.send_trigger_to_navigation()

                #measurements = arduino.read_from_arduino()
                #ISI_measurements.append(measurements)
                #print(ISI_measurements)
                #txt.file.write(f'{measurements}\n')

                #print("Process time: ", (time.time() - start))
                #time.sleep(ISI_exci)

            elif pp_mode[sequence[pulse_index]] == "150ms":
                print('Iniciando sequencia')
                arduino.send_to_arduino('150')

                if consts.create_navigation_marker:
                    updator.send_trigger_to_navigation()

                #measurements = arduino.read_from_arduino()
                #ISI_measurements.append(measurements)
                #print(ISI_measurements)
                #txt.file.write(f'{measurements}\n')


        print("Process time: ", (time.time() - start))
        print("Process time: ", (time.time() - start))
        print("disparando")

        time.sleep(random.uniform(4, 8))
        print(pulse_index)
        pulse_index += 1

        # hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= len(sequence):
            break
        time.sleep(0.01)