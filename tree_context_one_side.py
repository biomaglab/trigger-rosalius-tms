#THIS SCRIPT IS A WORK IN PROGRESS
#DO NOT CONSIDER

#TO DO: ADD MAG CONTROL (DON'T FORGET TO EDIT LIBRARY)


import pyautogui
import keyboard
import numpy as np
import random
import time
import magicpy.magicpy as mp
from Components.update_navigation import UpdateNavigationInfo
from random_seq_gen import total_number_of_stimuli,stimuli_mode
from Components.arduino_connection import ArduinoConnection
from Components.update_navigation import UpdateNavigationInfo
from Components import constants as consts, txt_configs as txt

#either pp or intensity
mode = "pp"
target_status = False
create_navigation_marker = True
debug_arduino_ppTMS = False

ISI_inib = 3  # Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option
ISI_exci = 11  # Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option

rmt_intensity = 20

intensity_0 = int(rmt_intensity - rmt_intensity * 0.1)
intensity_1 = int(rmt_intensity)
intensity_2 = int(rmt_intensity + rmt_intensity * 0.1)

intensities = {0: intensity_0,
               1: intensity_1,
               2: intensity_2}

pp_mode = {0: "single",
           1: "inibitorio",
           2: "excitatorio"}

target_intensity = 659, 189
target_stimuli = 490, 60
target_status = False

''' CONNECTION TO NAVIGATION UPDATES '''
updator = UpdateNavigationInfo(1)
updator.connect('192.168.200.201', [5000])

''' CONNECTION WITH MAGVENTURE'''
mp.list_serial_ports()                                              # imprime uma lista de portas disponíveis
input("Portas listadas. Certifique-se de que está conectando na porta correta. Pressione Enter para continuar...")         # Aguarda o usuário clicar Enter para continuar
stimulator = mp.MagVenture("COM1")                                  # Inicializa um objeto que se relaciona ao estimulador
stimulator.connect()
stimulator.set_page('Main', get_response=True)

''' LOAD PULSE TREE CONTEXT SEQUENCE '''
sequence = np.loadtxt('sequence_100.txt', delimiter=',', dtype='int')
print(sequence)

while True:
    if keyboard.is_pressed('s'):
        break
print("start sequence")
pulse_index = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

while True:
    if updator.target_status:
        if mode == "pp":
            start = time.time()
            if pp_mode[sequence[pulse_index]] == "single":
                print(pp_mode[sequence[pulse_index]])
                stimulator.set_mode(mode='Standard', current_dir='Normal', n_pulses_per_burst=2, ipi=5, baratio=80)
                time.sleep(1)
                stimulator.arm(get_response=False)
                time.sleep(1)
                stimulator.set_amplitude(int(1.2 * rmt_intensity),b_amp=None)
                time.sleep(1)
                stimulator.fire()


            elif pp_mode[sequence[pulse_index]] == "inibitorio":
                print(pp_mode[sequence[pulse_index]])
                stimulator.set_mode(mode='Dual', current_dir='Normal', n_pulses_per_burst=2, ipi=ISI_inib, baratio=80)
                time.sleep(1)
                stimulator.arm(get_response=False)
                time.sleep(1)
                stimulator.set_amplitude(int(0.9 * rmt_intensity), b_amp=int(1.2 * rmt_intensity), get_response=False)
                time.sleep(1)
                stimulator.fire()

                print("Process time: ", (time.time() - start))

            elif pp_mode[sequence[pulse_index]] == "excitatorio":
                print(pp_mode[sequence[pulse_index]])
                stimulator.set_mode(mode='Dual', current_dir='Normal', n_pulses_per_burst=2, ipi=ISI_exci, baratio=80)
                time.sleep(1)
                stimulator.arm(get_response=False)
                time.sleep(1)
                stimulator.set_amplitude(int(0.9 * rmt_intensity), b_amp=int(1.2 * rmt_intensity), get_response=False)
                time.sleep(1)
                stimulator.fire()

                #print("Process time: ", (time.time() - start))
                #time.sleep(ISI_exci)

        elif mode == "intensity":
            # set intensity
            pyautogui.click(target_intensity)
            print(intensities[sequence[pulse_index]])
            try:
                pyautogui.hotkey("ctrlleft", "a")
            except pyautogui.FailSafeException:
                pass
            pyautogui.typewrite(str(intensities[sequence[pulse_index]]))

        print("Process time: ", (time.time() - start))
        print("Process time: ", (time.time() - start))
        print("disparando")

        time.sleep(random.uniform(4, 8))
        pulse_index += 1

        # hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= len(sequence):
            break
        time.sleep(0.01)